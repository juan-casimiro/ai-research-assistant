"""Verify audit source bindings and frozen inputs without models or ingestion."""
import argparse
import hashlib
import json
from pathlib import Path


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify(root, outlier_corpus, als_ftd_corpus):
    release = root / "benchmark/outliers/v1"
    audit_path = release / "als-ftd-audit-v1/audit.json"
    audit = json.loads(audit_path.read_text())
    for filename, expected in audit["frozen_inputs"].items():
        if digest(root / filename) != expected:
            raise ValueError(f"Frozen input changed: {filename}")
    texts = {}
    groups = {"outliers": set(), "als-ftd": set()}
    for group, corpus in [("outliers", outlier_corpus), ("als-ftd", als_ftd_corpus)]:
        manifest = json.loads((root / f"benchmark/{group}/v1/manifest.json").read_text())
        for article in manifest["articles"]:
            aid = article["article_id"]
            groups[group].add(aid)
            record = audit["articles"][aid]
            pdf = corpus / article["filename"]
            txt = pdf.with_suffix(".txt")
            if (record["group"] != group or record["filename"] != article["filename"]
                    or record["pmc_version"] != article["pmc_version"]
                    or digest(pdf) != record["pdf_sha256"]
                    or record["pdf_sha256"] != article["download"]["pdf_sha256"]
                    or digest(txt) != record["text_sha256"]
                    or record["text_sha256"] != article["validation"]["extracted_text_sha256"]):
                raise ValueError(f"Source binding changed: {aid}")
            texts[aid] = txt.read_text()
    if set(texts) != set(audit["articles"]):
        raise ValueError("Audit source inventory differs from manifests")
    spans = {}
    for span in audit["evidence_spans"]:
        excerpt = texts[span["article_id"]][span["text_start"]:span["text_end"]]
        if (span["id"] in spans or not excerpt or excerpt != span["excerpt"]
                or hashlib.sha256(excerpt.encode()).hexdigest() != span["excerpt_sha256"]):
            raise ValueError(f"Invalid evidence span: {span['id']}")
        spans[span["id"]] = span
    pairs = audit["article_pairs"]
    expected = {(o, a) for o in groups["outliers"] for a in groups["als-ftd"]}
    if (len(pairs) != len(expected)
            or {(p["outlier_article"], p["als_ftd_article"]) for p in pairs} != expected):
        raise ValueError("Missing or duplicate article-pair review")
    for pair in pairs:
        bound = {spans[s]["article_id"] for s in pair["evidence_spans"]}
        if not {pair["outlier_article"], pair["als_ftd_article"]} <= bound:
            raise ValueError("Pair lacks evidence from both articles")
    queries = json.loads((release / "queries.json").read_text())["queries"]
    checks = audit["case_checks"]
    if len(checks) != len(queries) or {c["id"] for c in checks} != {q["id"] for q in queries}:
        raise ValueError("Missing or duplicate case review")
    for query in queries:
        check = next(c for c in checks if c["id"] == query["id"])
        if (check["revision"] != query["revision"]
                or check["answerability"] != query["answerability"]["status"]
                or set(check["reviewed_als_ftd_articles"]) != groups["als-ftd"]):
            raise ValueError(f"Case review scope changed: {query['id']}")
    return {"audit_sha256": digest(audit_path), "frozen_inputs_verified": 6,
            "source_pdf_text_pairs_verified": len(texts), "evidence_spans_verified": len(spans),
            "article_pairs_verified": len(pairs), "case_reviews_verified": len(checks),
            "retrieval_run": False, "integrated_absence_certified": False,
            "scientific_review_certified": False}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outlier-corpus", type=Path, default=Path("corpus/outliers-v1"))
    parser.add_argument("--als-ftd-corpus", type=Path, default=Path("corpus/als-ftd-v1"))
    args = parser.parse_args()
    print(json.dumps(verify(Path.cwd(), args.outlier_corpus, args.als_ftd_corpus), indent=2))
