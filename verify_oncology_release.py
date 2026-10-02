"""Verify the oncology release offline, without models, ingestion or API calls."""
import argparse
import hashlib
import json
from pathlib import Path

from pypdf import PdfReader

from benchmark_scoring import canonical_hash
from eval_benchmark import read_release


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def verify(release: Path, corpus: Path) -> dict:
    benchmark, manifest, conditions, _, _, _ = read_release(release, corpus, "C2")
    articles = manifest["articles"]
    by_id = {a["article_id"]: a for a in articles}
    for field in ["article_id", "filename", "doi", "pmid"]:
        if len({a[field] for a in articles}) != len(articles):
            raise ValueError(f"Duplicate {field}")
    for article in articles:
        aid = article["article_id"]
        if (article["eligibility"] != "eligible" or
                article["licence"]["spdx"] != "CC-BY-4.0" or
                article["third_party_review"]["status"] != "clear"):
            raise ValueError(f"{aid}: eligibility gate failed")
        if not all(article[k] for k in ["authors", "abstract", "abstract_summary", "search_query"]):
            raise ValueError(f"{aid}: incomplete metadata")
        for name in ["cloud.json", "pubmed.xml", "id-converter.json"]:
            source = article["metadata_sources"][name]
            if digest((release / source["archive"]).read_bytes()) != source["sha256"]:
                raise ValueError(f"{aid}: {name} archive changed")
        cloud = json.loads((release / article["metadata_sources"]["cloud.json"]["archive"]).read_text())
        if (cloud["pmcid"], cloud["version"], cloud["doi"], str(cloud["pmid"])) != (
                aid, article["pmc_version"], article["doi"], article["pmid"]):
            raise ValueError(f"{aid}: archived identifiers differ")
        xml = corpus / f"{aid}.{article['pmc_version']}.cloud.xml"
        if digest(xml.read_bytes()) != article["metadata_sources"]["article.xml"]["sha256"]:
            raise ValueError(f"{aid}: article XML changed")
        pdf = corpus / article["filename"]
        receipt = article["download"]
        if (len(pdf.read_bytes()) != receipt["byte_count"] or
                hashlib.md5(pdf.read_bytes()).hexdigest() != receipt["provider_checksum"]["value"]):
            raise ValueError(f"{aid}: provider checksum/size mismatch")
        pages = [page.extract_text() or "" for page in PdfReader(pdf, strict=True).pages]
        if len(pages) != article["page_count"] or not all(p.strip() for p in pages):
            raise ValueError(f"{aid}: page count/readability changed")
        if digest("\n".join(pages).encode()) != article["validation"]["extracted_text_sha256"]:
            raise ValueError(f"{aid}: extraction differs from pinned text")
    required = {aid for q in benchmark["queries"] for aid in q["dependencies"]["required"]}
    if required != set(conditions["conditions"]["C1"]["article_ids"]):
        raise ValueError("C1 is not the exact answer-source union")
    c2 = conditions["conditions"]["C2"]
    if not required <= set(c2["article_ids"]) or set(c2["article_ids"]) != set(by_id):
        raise ValueError("C1/C2 are not nested or do not cover the selection")
    previous = set()
    for name in ["C1", "C2", "C3"]:
        condition = conditions["conditions"][name]
        ids = condition["article_ids"]
        tuples = [t for t in conditions["article_tuples"] if t["article_id"] in ids]
        if (ids != sorted(set(ids)) or not previous <= set(ids) or
                not set(ids) <= set(by_id) or
                canonical_hash(tuples) != condition["membership_sha256"]):
            raise ValueError(f"{name}: invalid nested membership or fingerprint")
        previous = set(ids)
    audit = json.loads((release / "legacy_audit.json").read_text())
    if {case["id"] for case in audit["cases"]} != {f"q{n:03d}" for n in range(78, 120)}:
        raise ValueError("Legacy oncology cases are not fully accounted for")
    root = release.resolve().parents[2]
    for name, expected in audit["baseline_hashes"].items():
        if digest((root / name).read_bytes()) != expected:
            raise ValueError(f"Preserved legacy baseline changed: {name}")
    return {"articles": len(articles), "queries": len(benchmark["queries"]),
            "anchors": len(benchmark["anchors"]), "selection_sha256": manifest["fingerprint_sha256"],
            "query_sha256": canonical_hash(benchmark), "retrieval_quality_measured": False}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--release", type=Path, default=Path("benchmark/oncology/v1"))
    parser.add_argument("--corpus-dir", type=Path, default=Path("corpus/oncology-v1"))
    args = parser.parse_args()
    try:
        print(json.dumps(verify(args.release, args.corpus_dir), indent=2))
        return 0
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"ERROR: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
