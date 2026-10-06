"""Verify audit source bindings and frozen inputs without models or ingestion."""
import argparse
import hashlib
import json
from pathlib import Path
import tempfile


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
    outlier_dependencies = json.loads((release / "case_dependencies.json").read_text())
    als_dependencies = json.loads((root / "benchmark/als-ftd/v1/case_dependencies.json").read_text())
    expected = {(o, a) for o in groups["outliers"] for a in groups["als-ftd"]}
    if (len(pairs) != len(expected)
            or {(p["outlier_article"], p["als_ftd_article"]) for p in pairs} != expected):
        raise ValueError("Missing or duplicate article-pair review")
    for pair in pairs:
        if len(pair["evidence_spans"]) != len(set(pair["evidence_spans"])):
            raise ValueError("Duplicate pair evidence span")
        bound = {spans[s]["article_id"] for s in pair["evidence_spans"]}
        if not {pair["outlier_article"], pair["als_ftd_article"]} <= bound:
            raise ValueError("Pair lacks evidence from both articles")
        outlier_cases = {c["id"] for c in outlier_dependencies["cases"]
                         if pair["outlier_article"] in c["required"] + c["negative_evidence"]}
        als_cases = {qid for qid, c in als_dependencies["cases"].items()
                     if pair["als_ftd_article"] in c["required_articles"]}
        if (set(pair["outlier_case_ids"]) != outlier_cases
                or set(pair["als_ftd_case_ids"]) != als_cases):
            raise ValueError("Pair case dependencies differ from releases")
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
    for name in ["case_dependencies", "case_review"]:
        link = json.loads((release / f"{name}.json").read_text())["supplementary_als_ftd_review"]
        if (link["version"] != audit["audit_version"] or link["revision"] != audit["revision"]
                or link["record"] != "als-ftd-audit-v1/audit.json"
                or set(link["reviewed_article_ids"]) != groups["als-ftd"]
                or set(link["case_ids"]) != {q["id"] for q in queries}):
            raise ValueError(f"Supplementary link differs: {name}")
    relationships = json.loads((release / "topic_relationships.json").read_text())
    mapped_pairs = []
    for article in relationships["article_relationships"]:
        for link in article["als_ftd_relationships"]:
            pair = next(p for p in pairs if p["outlier_article"] == article["article_id"]
                        and p["als_ftd_article"] == link["article_id"])
            mapped_pairs.append((article["article_id"], link["article_id"]))
            if (link["relationship"] != pair["relationship"]
                    or link["related_benchmark_cases"] != pair["als_ftd_case_ids"]
                    or link["audit_pair"] != f"{article['article_id']}/{link['article_id']}"):
                raise ValueError("Relationship map differs from audit")
    if len(mapped_pairs) != len(expected) or set(mapped_pairs) != expected:
        raise ValueError("Incomplete relationship map")
    roles = relationships["external_article_roles"]
    if len(roles) != len(groups["als-ftd"]) or {r["article_id"] for r in roles} != groups["als-ftd"]:
        raise ValueError("Incomplete external role inventory")
    for role in roles:
        required = {qid for qid, c in als_dependencies["cases"].items()
                    if role["article_id"] in c["required_articles"]}
        decoys = {qid for qid, c in als_dependencies["cases"].items()
                  if role["article_id"] in c["decoy_articles"]}
        if set(role["answer_source_for"]) != required or set(role["named_decoy_for"]) != decoys:
            raise ValueError("External source/decoy roles differ from release")
    all_cases = {q["id"] for q in queries} | set(als_dependencies["cases"])
    targets = audit["handoff"]["targeted_ids"]
    if len(targets) != len(set(targets)) or not set(targets) <= all_cases:
        raise ValueError("Unknown or duplicate handoff case")
    return {"audit_sha256": digest(audit_path), "frozen_inputs_verified": 6,
            "source_pdf_text_pairs_verified": len(texts), "evidence_spans_verified": len(spans),
            "article_pairs_verified": len(pairs), "case_reviews_verified": len(checks),
            "retrieval_run": False, "integrated_absence_certified": False,
            "scientific_review_certified": False}


def corruption_checks(root, outlier_corpus, als_ftd_corpus):
    """Reject broken source offsets, missing coverage and misleading dependency links."""
    release = root / "benchmark/outliers/v1"
    rejected = []
    for mutation in ["span_offset", "missing_pair", "case_revision", "duplicate_span",
                     "missing_negative_dependency", "wrong_external_decoy"]:
        with tempfile.TemporaryDirectory() as temporary:
            fixture = Path(temporary)
            audit_dir = fixture / "benchmark/outliers/v1/als-ftd-audit-v1"
            audit_dir.mkdir(parents=True)
            (fixture / "benchmark/als-ftd").symlink_to(root / "benchmark/als-ftd")
            for name in ["queries", "manifest", "conditions", "case_dependencies",
                         "case_review", "topic_relationships"]:
                (audit_dir.parent / f"{name}.json").write_bytes((release / f"{name}.json").read_bytes())
            audit = json.loads((release / "als-ftd-audit-v1/audit.json").read_text())
            if mutation == "span_offset":
                audit["evidence_spans"][0]["text_start"] += 1
            elif mutation == "missing_pair":
                audit["article_pairs"].pop()
            elif mutation == "case_revision":
                audit["case_checks"][0]["revision"] += 1
            elif mutation == "duplicate_span":
                audit["article_pairs"][0]["evidence_spans"].append(audit["article_pairs"][0]["evidence_spans"][0])
            elif mutation == "missing_negative_dependency":
                audit["article_pairs"][0]["outlier_case_ids"].remove("x009")
            else:
                mapping_path = audit_dir.parent / "topic_relationships.json"
                mapping = json.loads(mapping_path.read_text())
                role = next(r for r in mapping["external_article_roles"] if r["article_id"] == "PMC11527445")
                role["named_decoy_for"] = []
                mapping_path.write_text(json.dumps(mapping))
            (audit_dir / "audit.json").write_text(json.dumps(audit))
            try:
                verify(fixture, outlier_corpus, als_ftd_corpus)
            except ValueError as error:
                rejected.append({"mutation": mutation, "rejected": True, "reason": str(error)})
            else:
                raise ValueError(f"Accepted corruption: {mutation}")
    return rejected


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outlier-corpus", type=Path, default=Path("corpus/outliers-v1"))
    parser.add_argument("--als-ftd-corpus", type=Path, default=Path("corpus/als-ftd-v1"))
    parser.add_argument("--corruption-checks", action="store_true")
    args = parser.parse_args()
    root = Path.cwd()
    outlier_corpus = args.outlier_corpus.resolve()
    als_ftd_corpus = args.als_ftd_corpus.resolve()
    result = verify(root, outlier_corpus, als_ftd_corpus)
    result["verifier_sha256"] = digest(Path(__file__))
    if args.corruption_checks:
        result["corruption_checks"] = corruption_checks(root, outlier_corpus, als_ftd_corpus)
    print(json.dumps(result, indent=2))
