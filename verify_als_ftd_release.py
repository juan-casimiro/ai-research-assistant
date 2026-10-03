"""Verify the prepared ALS/FTD release against reacquired local source bytes.

No models, ingestion, network or paid calls. Manual scientific/rights review
remains separate from mechanical provenance and evidence checks.
"""
import argparse
import hashlib
from importlib.metadata import version
import json
from pathlib import Path
import xml.etree.ElementTree as ET

from benchmark_scoring import canonical_hash
from eval_benchmark import read_release
from fetch_article_metadata import parse_record
from pypdf import PdfReader


def verify(directory: Path, corpus: Path) -> dict:
    benchmark, manifest, conditions, _, tuples, _ = read_release(directory, corpus, "C2")
    ids = {a["article_id"] for a in manifest["articles"]}
    if len(ids) != len(manifest["articles"]):
        raise ValueError("duplicate selected article")
    for article in manifest["articles"]:
        aid = article["article_id"]
        if article["eligibility"] != "eligible" or article["third_party_review"]["status"] != "clear":
            raise ValueError(f"{aid}: incomplete eligibility")
        if article["licence"]["id"] != "CC-BY-4.0" or article["licence"]["url"] != "https://creativecommons.org/licenses/by/4.0/":
            raise ValueError(f"{aid}: licence differs from reviewed selection")
        sources = article["metadata_sources"]
        archived = {}
        for name, source in sources.items():
            path = directory / source["archive"] if source["archive"] else corpus / f"{aid}.{article['pmc_version']}.article.xml"
            data = path.read_bytes()
            if hashlib.sha256(data).hexdigest() != source["sha256"]:
                raise ValueError(f"{aid}: {name} hash mismatch")
            archived[name] = data
        cloud = json.loads(archived["cloud.json"])
        joined = parse_record(cloud, archived["article.xml"], archived["pubmed.xml"], json.loads(archived["id-converter.json"]))
        for field in ["pmcid", "pmc_version", "pmid", "doi", "title", "authors", "journal", "publication_date", "abstract", "license"]:
            if joined[field] != article[field]:
                raise ValueError(f"{aid}: {field} differs from authoritative metadata")
        if joined["license"] != "CC BY 4.0" or cloud["is_manuscript"]:
            raise ValueError(f"{aid}: unapproved licence or unexpected manuscript")
        pdf = corpus / article["filename"]
        data = pdf.read_bytes()
        if len(data) != article["download"]["byte_count"] or hashlib.md5(data).hexdigest() != article["download"]["provider_md5"]:
            raise ValueError(f"{aid}: provider PDF receipt changed")
        reader = PdfReader(pdf, strict=True)
        pages = [p.extract_text() or "" for p in reader.pages]
        if len(pages) != article["page_count"] or any(len(p.strip()) < 80 for p in pages):
            raise ValueError(f"{aid}: unreadable pages or page-count mismatch")
        text = "\n".join(pages)
        if text != pdf.with_suffix(".txt").read_text():
            raise ValueError(f"{aid}: extraction differs from verified PDF")
        if version("pypdf") != article["validation"]["parser_version"]:
            raise ValueError(f"{aid}: different parser; review extraction before changing hashes")
        root = ET.fromstring(archived["article.xml"])
        correction_ids = {el.get("{http://www.w3.org/1999/xlink}href")
                          for el in root.findall(".//related-article")
                          if el.get("related-article-type") == "correction-forward"}
        resolutions = article["provenance"]["discrepancy_resolutions"]
        if (len(resolutions) != len(correction_ids) or
                {r["notice_pmcid"] for r in resolutions} != correction_ids or
                any(not all(r.get(k) for k in
                            ["source_url", "reviewer", "reviewed_at", "change",
                             "impact_assessment", "resolution", "reviewed_case_ids"])
                    for r in resolutions)):
            raise ValueError(f"{aid}: incomplete correction impact review")
        caption_ids = [el.get("id") for el in root.findall(".//fig") + root.findall(".//table-wrap")]
        if caption_ids != [el["id"] for el in article["third_party_review"]["credit_inventory"]]:
            raise ValueError(f"{aid}: incomplete caption inventory")
        for anchor in [a for a in benchmark["anchors"] if a["article_id"] == aid]:
            physical_pages = []
            offset = 0
            for number, page in enumerate(pages, 1):
                end = offset + len(page)
                if anchor["text_start"] < end and anchor["text_end"] > offset:
                    physical_pages.append(number)
                offset = end + 1
            if anchor["pages"] != physical_pages or anchor["page"] != physical_pages[0]:
                raise ValueError(f"{anchor['id']}: physical page mismatch")
            bound = sorted(f["id"] for q in benchmark["queries"] for f in q["required_facts"]
                           if any(anchor["id"] in s["fact_anchors"][f["id"]] for s in q["evidence_sets"]))
            if sorted(anchor["fact_ids"]) != bound or not bound:
                raise ValueError(f"{anchor['id']}: orphan or incorrect fact bindings")
    anchors = {a["id"]: a for a in benchmark["anchors"]}
    for query in benchmark["queries"]:
        if query["answerability"]["status"] == "false_premise":
            answerability = query["answerability"]
            correction_anchors = answerability.get("correction_anchors", [])
            accepted = {aid for s in query["evidence_sets"] for aid in s["anchors"]}
            if (not answerability.get("offending_premise") or not correction_anchors or
                    not set(correction_anchors) <= accepted & anchors.keys()):
                raise ValueError(f"{query['id']}: incomplete false-premise correction record")
    required = {a["article_id"] for q in benchmark["queries"] for s in q["evidence_sets"]
                for a in benchmark["anchors"] if a["id"] in s["anchors"]}
    if set(conditions["conditions"]["C1"]["article_ids"]) != required:
        raise ValueError("C1 is not the exact accepted-source union")
    for name in ["C1", "C2", "C3"]:
        if (set(conditions["conditions"][name]["article_ids"]) != ids or
                conditions["conditions"][name]["membership_sha256"] != canonical_hash(tuples)):
            raise ValueError("prepared local conditions must equal reviewed selection")
    return {"articles": len(ids), "cases": len(benchmark["queries"]), "anchors": len(benchmark["anchors"]),
            "physical_pdf_pages": sum(a["page_count"] for a in manifest["articles"]),
            "pdf_bytes": sum(a["download"]["byte_count"] for a in manifest["articles"]),
            "selection_sha256": manifest["fingerprint_sha256"], "query_sha256": canonical_hash(benchmark),
            "membership_sha256": canonical_hash(tuples), "independent_review_complete": False,
            "retrieval_quality_measured": False}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--benchmark", type=Path, default=Path("benchmark/als-ftd/v1"))
    parser.add_argument("--corpus-dir", type=Path, default=Path("corpus/als-ftd-v1"))
    args = parser.parse_args()
    try:
        print(json.dumps(verify(args.benchmark, args.corpus_dir), indent=2))
        return 0
    except (OSError, ValueError, KeyError, ET.ParseError) as error:
        print(f"ERROR: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
