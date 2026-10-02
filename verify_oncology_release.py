"""Verify the oncology release offline, without models, ingestion or API calls."""
import argparse
import hashlib
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

from pypdf import PdfReader

from benchmark_scoring import canonical_hash
from eval_benchmark import read_release
from fetch_article_metadata import element_text, parse_record


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def verify_metadata(article: dict, cloud: dict, xml: bytes, pubmed: bytes, identifiers: dict) -> None:
    """Reject self-consistent manifest edits that contradict archived sources."""
    parsed = parse_record(cloud, xml, pubmed, identifiers)
    for field in ["title", "authors", "abstract", "journal", "publication_date", "license", "license_notes"]:
        if article[field] != parsed[field]:
            raise ValueError(f"{article['article_id']}: archived {field} disagrees with manifest")
    if article["licence"]["notice"] != parsed["license_notes"] or article["licence"]["url"] not in parsed["licence_urls"]:
        raise ValueError(f"{article['article_id']}: licence notice/URL differs from source")
    root = ET.fromstring(xml)
    inventory = []
    for tag in ["fig", "table-wrap"]:
        for item in root.findall(".//" + tag):
            inventory.append({"type": tag, "id": item.get("id"),
                              "label": element_text(item.find("label")),
                              "caption": element_text(item.find("caption")),
                              "credits": [element_text(e) for e in item.findall(".//attrib") + item.findall(".//permissions")]})
    if inventory != article["third_party_review"]["inventory"]:
        raise ValueError(f"{article['article_id']}: figure/table credit inventory differs from source")


def verify_linkage(release: Path, benchmark: dict, manifest: dict, conditions: dict) -> None:
    query_hash = canonical_hash(benchmark)
    for name in ["case_dependencies.json", "case_review.json", "evidence_map.json", "revision_ledger.json"]:
        value = json.loads((release / name).read_text())
        if value["query_sha256"] != query_hash:
            raise ValueError(f"{name}: stale query linkage")
    dependencies = json.loads((release / "case_dependencies.json").read_text())["cases"]
    expected = [dict(id=q["id"], revision=q["revision"], category=q["category"], **q["dependencies"]) for q in benchmark["queries"]]
    if dependencies != expected:
        raise ValueError("case_dependencies.json: dependency content differs from queries")
    evidence = json.loads((release / "evidence_map.json").read_text())
    if {a["article_id"] for a in evidence["articles"]} != {a["article_id"] for a in manifest["articles"]}:
        raise ValueError("evidence_map.json: article membership differs")
    query_ids = {q["id"] for q in benchmark["queries"]}
    evidence_ids = {q["id"] for q in benchmark["queries"] if q.get("evidence_sets")}
    for condition in ["C1", "C2"]:
        result = json.loads((release / "results" / f"offline-{condition}.json").read_text())
        if (result["query_sha256"] != query_hash or
                result["selection_sha256"] != manifest["fingerprint_sha256"] or
                result["conditions_sha256"] != canonical_hash(conditions)):
            raise ValueError(f"offline-{condition}.json: stale oracle linkage")
        oracle = result["result"]
        if (result["condition"] != condition or
                result["membership_sha256"] != conditions["conditions"][condition]["membership_sha256"] or
                set(oracle["query_feasibility"]) != query_ids or oracle["evidence_queries"] != len(evidence_ids) or
                {qid for qid, f in oracle["query_feasibility"].items() if f["minimum_chunks"] is not None} != evidence_ids or
                any(set(depth["feasible_ids"]) | set(depth["infeasible_ids"]) != evidence_ids
                    for depth in oracle["by_depth"].values())):
            raise ValueError(f"offline-{condition}.json: oracle content does not cover the evidence cases")


def verify_attribution(articles: list[dict], attribution: str) -> None:
    markers = list(re.finditer(r'<a id="([^"]+)"></a>', attribution))
    if (len(markers) != len(articles) or
            {match.group(1) for match in markers} != {a["attribution_id"] for a in articles}):
        raise ValueError("Attribution inventory membership differs from manifest")
    citations = {match.group(1): attribution[match.end():markers[i + 1].start() if i + 1 < len(markers) else len(attribution)]
                 for i, match in enumerate(markers)}
    for article in articles:
        for citation in [article["title"], article["doi"], article["article_url"], article["licence"]["url"], *article["authors"]]:
            if citation not in citations[article["attribution_id"]]:
                raise ValueError(f"{article['article_id']}: missing attribution citation component")


def verify_query_roles(benchmark: dict) -> None:
    """Keep dependency, decoy and overlap records consistent with the gold evidence."""
    anchors = {a["id"]: a for a in benchmark["anchors"]}
    for query in benchmark["queries"]:
        qid, dependencies = query["id"], query["dependencies"]
        primary = {anchors[aid]["article_id"] for aid in query["evidence_sets"][0]["anchors"]} if query["evidence_sets"] else set()
        alternatives = {anchors[aid]["article_id"] for s in query["evidence_sets"][1:] for aid in s["anchors"]}
        if set(dependencies["required"]) != primary or set(dependencies["alternatives"]) != alternatives:
            raise ValueError(f"{qid}: evidence and dependency source sets differ")
        decoys = {d["article_id"] for d in query["related_distractors"]}
        if set(dependencies["decoys"]) != decoys:
            raise ValueError(f"{qid}: decoy dependencies differ")
        findings = dependencies.get("overlap_findings", [])
        for record in findings + dependencies.get("negative_context", []):
            anchor = anchors.get(record["anchor_id"])
            if anchor is None or anchor["article_id"] != record.get("article_id", anchor["article_id"]):
                raise ValueError(f"{qid}: overlap or negative-context anchor does not resolve")
        if any(f["article_id"] in decoys and f["role"] != "decoy" for f in findings):
            raise ValueError(f"{qid}: article is both a named decoy and supporting overlap")
        involved = set(dependencies["required"]) | alternatives | decoys | {f["article_id"] for f in findings}
        if not involved <= set(dependencies["overlap_review"]):
            raise ValueError(f"{qid}: overlap review omits a source, decoy or overlap article")
        evidence = {aid for s in query["evidence_sets"] for aid in s["anchors"]}
        if not set(query["answerability"].get("correction_anchors", [])) <= evidence:
            raise ValueError(f"{qid}: correction anchor is not gold evidence")


def verify_migration(audit: dict, active: dict, legacy: dict) -> None:
    if {case["id"] for case in audit["cases"]} != {f"q{n:03d}" for n in range(78, 120)}:
        raise ValueError("Legacy oncology cases are not fully accounted for")
    for case in audit["cases"]:
        if case["question"] != legacy[case["id"]]["question"]:
            raise ValueError(f"{case['id']}: migration does not preserve legacy question")
        if not set(case["replacement_cases"]) <= active.keys():
            raise ValueError(f"{case['id']}: unknown replacement case")
        if case["action"] == "retire_legacy_case" and case["id"] in active:
            raise ValueError(f"{case['id']}: retired ID remains active")
        if case["action"] == "revise_in_v1":
            revised = active.get(case["id"])
            if revised is None or revised["revision"] < 2:
                raise ValueError(f"{case['id']}: missing revised case")
            if case.get("revised_question") != revised["question"]:
                raise ValueError(f"{case['id']}: audit revised question differs from active query")
            if (case["legacy_category"] == "unanswerable" and
                    case["negative_scope_review"] != revised["answerability"]["status"]):
                raise ValueError(f"{case['id']}: audit answerability differs from active query")
        if case["action"] not in {"retire_legacy_case", "revise_in_v1"}:
            raise ValueError(f"{case['id']}: invalid migration action")


def verify_ledger(ledger: dict, active: dict, audit: dict) -> None:
    """Cross-check renamed, withdrawn and retained-ID records against the active release."""
    actions = {case["id"]: case for case in audit["cases"]}
    renamed = ledger["renamed_coverage_cases"]
    superseding = {q["supersedes_coverage_of"]: qid for qid, q in active.items() if "supersedes_coverage_of" in q}
    if superseding != renamed:
        raise ValueError("revision_ledger.json: renamed coverage differs from active supersedes_coverage_of")
    for old, new in renamed.items():
        if old in active or actions[old]["action"] != "retire_legacy_case" or new not in actions[old]["replacement_cases"]:
            raise ValueError(f"revision_ledger.json: {old} is not retired in favour of {new}")
    for qid, record in ledger["withdrawn_cases"].items():
        if qid in active or record["coverage_retained_by"] not in active:
            raise ValueError(f"revision_ledger.json: withdrawn {qid} is active or has no active coverage")
        if qid in actions and actions[qid]["action"] != "retire_legacy_case":
            raise ValueError(f"revision_ledger.json: withdrawn legacy {qid} is not retired")
    for qid in ledger["retained_id_task_changes"]:
        if qid not in active or actions[qid]["action"] != "revise_in_v1":
            raise ValueError(f"revision_ledger.json: retained-ID note for inactive or unrevised {qid}")
    latest = ledger["revisions"][-1]
    if latest["query_sha256"] != ledger["query_sha256"] or not set(latest["changed_cases"]) <= active.keys():
        raise ValueError("revision_ledger.json: latest revision does not describe the active queries")


def verify_decision_record(record: str, benchmark: dict, audit: dict, candidates: dict, ledger: dict) -> None:
    """Every article, candidate and case decision must be explained, not left as shared boilerplate."""
    rationales = [q["selection_rationale"] for q in benchmark["queries"]]
    if not all(r.strip() for r in rationales) or len(set(rationales)) != len(rationales):
        raise ValueError("Case selection rationales are missing or shared boilerplate")
    overlap = [q["review"].get("duplicate_leakage_check", "") for q in benchmark["queries"]]
    if not all(o.strip() for o in overlap):
        raise ValueError("Case near-duplicate review is missing")
    for case in audit["cases"]:
        if case["action"] == "retire_legacy_case" and case["replacement_cases"] and not case.get("replacement_basis"):
            raise ValueError(f"{case['id']}: replacement link has no recorded basis")
    expected = ({f"#### {q['id']} " for q in benchmark["queries"]} |
                {f"**{qid}:**" for qid in ledger["withdrawn_cases"]} |
                {f"| {case['id']} |" for case in audit["cases"]} |
                {f"| {c['pmcid']} |" for c in candidates["candidates"] if c["disposition"] != "selected"} |
                {f"### {c['pmcid']} " for c in candidates["candidates"] if c["disposition"] == "selected"})
    missing = sorted(item for item in expected if item not in record)
    if missing:
        raise ValueError(f"DECISIONS.md does not record: {missing[:5]}")


def verify(release: Path, corpus: Path) -> dict:
    benchmark, manifest, conditions, _, _, _ = read_release(release, corpus, "C2")
    articles = manifest["articles"]
    by_id = {a["article_id"]: a for a in articles}
    if {p.name for p in corpus.glob("*.pdf")} != {a["filename"] for a in articles}:
        raise ValueError("Corpus directory has missing or unselected PDFs; archive acquisition candidates separately")
    verify_attribution(articles, (release / "ATTRIBUTION.md").read_text())
    for field in ["article_id", "filename", "doi", "pmid"]:
        if len({a[field] for a in articles}) != len(articles):
            raise ValueError(f"Duplicate {field}")
    for article in articles:
        aid = article["article_id"]
        if (article["eligibility"] != "eligible" or
                article["licence"]["spdx"] != "CC-BY-4.0" or
                article["licence"]["id"] != "CC-BY-4.0" or article["licence"]["version"] != "4.0" or
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
        pubmed = (release / article["metadata_sources"]["pubmed.xml"]["archive"]).read_bytes()
        identifiers = json.loads((release / article["metadata_sources"]["id-converter.json"]["archive"]).read_text())
        verify_metadata(article, cloud, xml.read_bytes(), pubmed, identifiers)
        pdf = corpus / article["filename"]
        receipt = article["download"]
        if (len(pdf.read_bytes()) != receipt["byte_count"] or
                hashlib.md5(pdf.read_bytes()).hexdigest() != receipt["provider_checksum"]["value"]):
            raise ValueError(f"{aid}: provider checksum/size mismatch")
        try:
            pages = [page.extract_text() or "" for page in PdfReader(pdf, strict=True).pages]
        except Exception as error:
            raise ValueError(f"{aid}: unreadable PDF") from error
        if len(pages) != article["page_count"] or not all(p.strip() for p in pages):
            raise ValueError(f"{aid}: page count/readability changed")
        if digest("\n".join(pages).encode()) != article["validation"]["extracted_text_sha256"]:
            raise ValueError(f"{aid}: extraction differs from pinned text")
    anchors = {a["id"]: a for a in benchmark["anchors"]}
    required = {anchors[aid]["article_id"] for q in benchmark["queries"] for s in q["evidence_sets"] for aid in s["anchors"]}
    verify_query_roles(benchmark)
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
    root = release.resolve().parents[2]
    active = {q["id"]: q for q in benchmark["queries"]}
    legacy = {q["id"]: q for q in json.loads((root / "golden_qa.json").read_text())["queries"]}
    verify_migration(audit, active, legacy)
    ledger = json.loads((release / "revision_ledger.json").read_text())
    verify_ledger(ledger, active, audit)
    verify_decision_record((release / "DECISIONS.md").read_text(), benchmark, audit,
                           json.loads((release / "candidate_log.json").read_text()), ledger)
    for name, expected in audit["baseline_hashes"].items():
        if digest((root / name).read_bytes()) != expected:
            raise ValueError(f"Preserved legacy baseline changed: {name}")
    verify_linkage(release, benchmark, manifest, conditions)
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
