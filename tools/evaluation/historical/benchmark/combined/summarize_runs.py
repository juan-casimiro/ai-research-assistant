"""Verify complete nested comparisons and write corpus-interference diagnostics."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from benchmark_scoring import canonical_hash
from compare_evals import check_compatible
from eval_benchmark import summarize

TOPICS = ("cardiology", "diabetes", "oncology", "outliers")


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def analyze(release):
    release = release.resolve()
    report = {"schema_version": "1.0", "topics": {}, "answer_judgments": 0,
              "scope": "51-article four-finalized-topic vector-only comparison; ALS/FTD excluded",
              "artifacts": {}}
    ingestion = load(release / "runs/C3-ingestion.json")
    report["ingestion"] = ingestion
    outlier_files = {a["filename"] for a in load(ROOT / "benchmark/outliers/v1/manifest.json")["articles"]}
    for topic in TOPICS:
        baseline_name = "C1" if topic == "outliers" else "C2"
        before_path = release / "runs" / f"{topic}-{baseline_name}-parent.json"
        after_path = release / "runs" / f"{topic}-C3-vector.json"
        baseline, expanded = load(before_path), load(after_path)
        check_compatible(baseline, expanded, nested_corpus=True)
        benchmark = load(release / topic / "queries.json")
        conditions = load(release / topic / "conditions.json")
        provenance = expanded["provenance"]
        expected = sorted(q["id"] for q in benchmark["queries"])
        if (provenance["requested_ids"] != expected or provenance["query_sha256"] != canonical_hash(benchmark) or
                provenance["conditions_sha256"] != canonical_hash(conditions) or
                provenance["membership_sha256"] != ingestion["membership_sha256"] or
                provenance["loaded_models"] != ingestion["loaded_models"] or
                provenance["ingestion_verification"]["chunks_sha256"] != ingestion["chunks_sha256"]):
            raise ValueError(f"{topic}: freeze/ingestion/run mismatch")
        if expanded["summary"] != summarize(expanded["results"]):
            raise ValueError(f"{topic}: stored summary mismatch")
        anchors = {a["id"]: a for a in benchmark["anchors"]}
        queries = {q["id"]: q for q in benchmark["queries"]}
        before = {r["id"]: r for r in baseline["results"]}
        after = {r["id"]: r for r in expanded["results"]}
        values = {"baseline": baseline["summary"], "combined": expanded["summary"],
                  "metric_changes": [], "context_changes": [], "depths": {}}
        for depth in [3, 8]:
            label = f"n{depth}"
            requirements, needed_docs, seen_docs, needed_anchors, seen_anchors = {}, set(), set(), set(), set()
            outlier_exposure, added_exposure = [], []
            baseline_sources = set(baseline["provenance"]["ingestion_verification"]["per_source_chunks"])
            for qid, result in after.items():
                query = queries[qid]
                metrics = result[label]["metrics"]
                group = str(result["evidence_feasibility"]["minimum_chunks"])
                counts = requirements.setdefault(group, {"cases": 0, "evidence_scored": 0, "document_pass": 0, "evidence_pass": 0})
                counts["cases"] += 1
                counts["evidence_scored"] += metrics["evidence_coverage"] != "not_scored"
                counts["document_pass"] += metrics["document_coverage"] == "pass"
                counts["evidence_pass"] += metrics["evidence_coverage"] == "pass"
                used = {aid for e in query["evidence_sets"] for aid in e["anchors"]}
                docs = {anchors[aid]["filename"] for aid in used}
                needed_docs.update(docs)
                needed_anchors.update(used)
                seen_docs.update(docs & set(result[label]["retrieved_sources"]))
                seen_anchors.update(aid for aid in used if metrics.get("anchor_matches", {}).get(aid))
                for metric in ["document_coverage", "evidence_coverage", "fact_recall", "distractor_ordering"]:
                    old, new = before[qid][label]["metrics"][metric], metrics[metric]
                    if old != new:
                        values["metric_changes"].append({"id": qid, "depth": depth, "metric": metric, "before": old, "after": new})
                if before[qid][label]["retrieved_contexts"] != result[label]["retrieved_contexts"] or before[qid][label]["retrieved_sources"] != result[label]["retrieved_sources"]:
                    values["context_changes"].append({"id": qid, "depth": depth})
                added = sorted(set(result[label]["retrieved_sources"]) - baseline_sources)
                if added:
                    added_exposure.append({"id": qid, "sources": added})
                intrusion = [s for s in result[label]["retrieved_sources"] if s in outlier_files and s not in docs]
                if topic != "outliers" and intrusion:
                    outlier_exposure.append({"id": qid, "chunks": len(intrusion), "sources": sorted(set(intrusion))})
            values["depths"][label] = {"minimum_chunk_groups": requirements,
                "unique_accepted_source_union": {"retrieved_in_own_case": len(seen_docs), "total": len(needed_docs), "missed": sorted(needed_docs - seen_docs)},
                "unique_accepted_anchor_union": {"matched_in_own_case": len(seen_anchors), "total": len(needed_anchors), "missed": sorted(needed_anchors - seen_anchors)},
                "new_source_exposure": added_exposure, "outlier_intrusion": outlier_exposure}
        report["topics"][topic] = values
        for path in [before_path, after_path]:
            report["artifacts"][str(path.relative_to(ROOT))] = hashlib.sha256(path.read_bytes()).hexdigest()
    # Retain the old 18-case sample as a slice, not a new retrieval execution.
    sample = load(ROOT / "benchmark/outliers/v1/regression/queries.json")
    sample_ids = {q["id"] for q in sample["queries"]}
    entries = []
    for topic in TOPICS:
        entries.extend(r for r in load(release / "runs" / f"{topic}-C3-vector.json")["results"] if r["id"] in sample_ids)
    if sorted(r["id"] for r in entries) != sorted(sample_ids):
        raise ValueError("historical sample coverage is incomplete")
    report["historical_18_case_slice"] = {"ids": sorted(sample_ids), "summary": summarize(entries),
        "note": "Slice of complete C3 results. Original focused-run envelope differs; no direct compatible 46/51-article comparison claimed."}
    first = load(release / "runs/cardiology-C1-parent.json")
    final = load(release / "runs/cardiology-C3-vector.json")
    check_compatible(first, final, nested_corpus=True)
    report["cardiology_source_only"] = first["summary"]
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--release", type=Path, default=Path("benchmark/combined/v1"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = analyze(args.release)
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(report, stream, indent=2, ensure_ascii=False, allow_nan=False)
        stream.write("\n")
    print("Verified four complete nested comparisons, exact freeze/ingestion linkage and the historical sample slice")
