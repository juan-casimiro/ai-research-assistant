"""Recheck saved corrected-gold runs and summarize compatible nested comparisons.

No retrieval, provider calls or models. Source bytes, chunks, per-case hashes,
metrics, feasibility, coverage, code/dependency/model and receipt joins are checked.
"""
import argparse
from collections import Counter
import hashlib
from importlib.metadata import version
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from benchmark_scoring import (SCORER_VERSION, FEASIBILITY_VERSION, canonical_hash,
    compile_anchor_spans, compile_query_feasibility, score_evidence)
from compare_evals import check_compatible
from eval_benchmark import read_release, summarize
from main import chunk_text
from benchmark.combined.build_corrected_release import TOPICS, load


def verify_run(path, release, corpus, condition, receipt):
    data = load(path)
    b, manifest, conditions, member, tuples, texts = read_release(release, corpus, condition)
    p = data["provenance"]
    queries = b["queries"]
    expected = sorted(q["id"] for q in queries)
    if (data["run_status"] != "complete" or p["missing_ids"] != [] or
            p["requested_ids"] != expected or p["executed_ids"] != expected or
            sorted(r["id"] for r in data["results"]) != expected):
        raise ValueError("incomplete/duplicate requested-ID coverage")
    if data["config"] != {"use_bm25": False, "use_query_rewriting": False, "n_values": [3, 8]}:
        raise ValueError("unexpected configuration")
    anchors = {a["id"]: a for a in b["anchors"]}
    used = {aid for q in queries for e in q["evidence_sets"] for aid in e["anchors"]}
    plans = compile_anchor_spans({aid: anchors[aid] for aid in used}, texts, chunk_text)
    chunks = {s: chunk_text(t) for s, t in texts.items()}
    available = Counter((s, c) for s, values in chunks.items() for c in values)
    feasibility = compile_query_feasibility(queries, anchors, plans, chunks)
    wanted = {"query_version": b["query_version"], "query_sha256": canonical_hash(b),
        "subset_sha256": canonical_hash(queries), "selection_sha256": manifest["fingerprint_sha256"],
        "conditions_sha256": canonical_hash(conditions), "condition": condition,
        "membership_sha256": member["membership_sha256"], "article_tuples": tuples,
        "depths": [3, 8], "scorer_version": SCORER_VERSION, "feasibility_version": FEASIBILITY_VERSION,
        "feasibility_sha256": canonical_hash(feasibility),
        "scorer_sha256": canonical_hash({"scoring": hashlib.sha256((ROOT / "benchmark_scoring.py").read_bytes()).hexdigest(),
            "adapter": hashlib.sha256((ROOT / "eval_benchmark.py").read_bytes()).hexdigest()})}
    for key, value in wanted.items():
        if p.get(key) != value:
            raise ValueError(f"saved provenance differs: {key}")
    if p["dependencies"] != {name: version(name) for name in p["dependencies"]}:
        raise ValueError("installed dependency versions differ")
    fingerprint = canonical_hash({"source_sha256": hashlib.sha256((ROOT / "main.py").read_bytes()).hexdigest(),
        "llm_source_sha256": hashlib.sha256((ROOT / "llm_client.py").read_bytes()).hexdigest(),
        "dependencies": p["dependencies"], "loaded_models": p["loaded_models"], "rewrite_identity": p["rewrite_identity"]})
    if fingerprint != p["retrieval_sha256"]:
        raise ValueError("retrieval/code/dependency/model fingerprint differs")
    if (receipt["status"] != "complete" or receipt["seed_on_empty"] is not False or
            receipt["membership_sha256"] != member["membership_sha256"] or receipt["article_tuples"] != tuples or
            receipt["loaded_models"] != p["loaded_models"] or
            receipt.get("dependencies") != p["dependencies"] or
            set(receipt["source_query_probes"]) != set(texts)):
        raise ValueError("ingestion/run/source-probe linkage differs")
    actual_chunks = canonical_hash(sorted((s, c, count) for (s, c), count in available.items()))
    for evidence in [receipt, p["ingestion_verification"]]:
        if (evidence["chunks_sha256"] != actual_chunks or evidence["chunk_count"] != sum(available.values()) or
                evidence["per_source_chunks"] != {s: len(c) for s, c in sorted(chunks.items())}):
            raise ValueError("receipt differs from actual production chunks")
    by_id = {q["id"]: q for q in queries}
    for entry in data["results"]:
        q = by_id[entry["id"]]
        for key, value in {"question": q["question"], "revision": q["revision"], "query_sha256": canonical_hash(q),
                           "category": q["category"], "answerability": q["answerability"]["status"],
                           "evidence_feasibility": feasibility[q["id"]]}.items():
            if entry.get(key) != value:
                raise ValueError(f"{q['id']}: changed query metadata {key}")
        for n in [3, 8]:
            result = entry[f"n{n}"]
            contexts, sources = result["retrieved_contexts"], result["retrieved_sources"]
            if len(contexts) != len(sources) or len(contexts) > n or not Counter(zip(sources, contexts)) <= available:
                raise ValueError(f"{q['id']}: invalid production contexts")
            metrics = score_evidence(contexts, sources, q, anchors, plans)
            verdict = (metrics["distractor_ordering"] if q["category"] == "cross_doc_distractor" else
                       "not_scored" if q["category"] == "false_premise" else metrics["document_coverage"])
            if result["metrics"] != metrics or result["verdict"] != verdict:
                raise ValueError(f"{q['id']}: saved metrics/verdict differ")
    if data["summary"] != summarize(data["results"]):
        raise ValueError("saved summary differs")
    return data


def analyze(release, corpus):
    release = release.resolve()
    ingestion = load(release / "runs/C3-ingestion.json")
    report = {"schema_version": "1.0", "scope": "55 articles / 158 corrected-gold cases, five topics",
              "answer_judgments": 0, "paid_calls": 0, "topics": {}, "retrieval_calls": 0,
              "ingestion": ingestion, "artifacts": {}}
    combined_entries = []
    outliers = {a["filename"] for a in load(ROOT / "benchmark/outliers/v1/manifest.json")["articles"]}
    als = {a["filename"] for a in load(ROOT / "benchmark/als-ftd/v1/manifest.json")["articles"]}
    for topic in TOPICS:
        baseline = "C1" if topic in ["outliers", "als-ftd"] else "C2"
        runs = {}
        for condition in (["C1", "C2", "C3"] if topic == "cardiology" else [baseline, "C3"]):
            path = release / "runs" / f"{topic}-{condition}-vector.json"
            receipt_path = release / "runs" / ("C3-ingestion.json" if condition == "C3" else f"{topic}-{condition}-ingestion.json")
            runs[condition] = verify_run(path, release / topic, corpus, condition, load(receipt_path))
            report["retrieval_calls"] += 2 * len(runs[condition]["results"])
            for artifact in [path, receipt_path]:
                report["artifacts"][str(artifact.relative_to(ROOT))] = hashlib.sha256(artifact.read_bytes()).hexdigest()
        before, after = runs[baseline], runs["C3"]
        check_compatible(before, after, nested_corpus=True)
        if topic == "cardiology":
            check_compatible(runs["C1"], after, nested_corpus=True)
        combined_entries.extend(after["results"])
        b = load(release / topic / "queries.json")
        anchors = {a["id"]: a for a in b["anchors"]}
        old = {r["id"]: r for r in before["results"]}
        old_sources = set(before["provenance"]["ingestion_verification"]["per_source_chunks"])
        values = {"baseline_condition": baseline, "summaries": {c: d["summary"] for c, d in runs.items()},
                  "metric_changes": [], "context_changes": [], "depths": {}}
        for depth in [3, 8]:
            label = f"n{depth}"
            needed_docs, seen_docs, needed_anchors, seen_anchors = set(), set(), set(), set()
            exposures, outlier_intrusion, als_intrusion = [], [], []
            requirements = {}
            for q, r in zip(b["queries"], after["results"], strict=True):
                if q["id"] != r["id"]:
                    raise ValueError("query/result order differs")
                m = r[label]["metrics"]
                required = {aid for e in q["evidence_sets"] for aid in e["anchors"]}
                docs = {anchors[aid]["filename"] for aid in required}
                sources = set(r[label]["retrieved_sources"])
                needed_docs.update(docs); seen_docs.update(docs & sources)
                needed_anchors.update(required)
                seen_anchors.update(aid for aid in required if m["anchor_matches"].get(aid))
                group = str(r["evidence_feasibility"]["minimum_chunks"])
                counts = requirements.setdefault(group, {"cases": 0, "evidence_pass": 0, "document_pass": 0})
                counts["cases"] += 1
                counts["evidence_pass"] += m["evidence_coverage"] == "pass"
                counts["document_pass"] += m["document_coverage"] == "pass"
                for metric in ["document_coverage", "evidence_coverage", "fact_recall", "distractor_ordering"]:
                    prior = old[r["id"]][label]["metrics"][metric]
                    if prior != m[metric]:
                        values["metric_changes"].append({"id": r["id"], "depth": depth, "metric": metric, "before": prior, "after": m[metric]})
                if any(old[r["id"]][label][key] != r[label][key] for key in ["retrieved_sources", "retrieved_contexts"]):
                    values["context_changes"].append({"id": r["id"], "depth": depth})
                if sources - old_sources:
                    exposures.append({"id": r["id"], "sources": sorted(sources - old_sources)})
                if topic != "outliers" and (sources - docs) & outliers:
                    outlier_intrusion.append({"id": r["id"], "sources": sorted((sources - docs) & outliers)})
                if topic != "als-ftd" and (sources - docs) & als:
                    als_intrusion.append({"id": r["id"], "sources": sorted((sources - docs) & als)})
            values["depths"][label] = {"minimum_chunk_groups": requirements,
                "accepted_sources": {"total": len(needed_docs), "retrieved": len(seen_docs), "missed": sorted(needed_docs - seen_docs)},
                "accepted_anchors": {"total": len(needed_anchors), "retrieved": len(seen_anchors), "missed": sorted(needed_anchors - seen_anchors)},
                "new_source_exposure": exposures, "outlier_intrusion": outlier_intrusion, "als_ftd_intrusion": als_intrusion}
        report["topics"][topic] = values
    if len(combined_entries) != 158 or len({r["id"] for r in combined_entries}) != 158:
        raise ValueError("combined coverage differs from 158 unique IDs")
    report["combined_summary"] = summarize(combined_entries)
    report["combined_ids"] = sorted(r["id"] for r in combined_entries)
    report["historical_comparability"] = "No direct v1 performance comparison: corpus, current gold, categories and scorer fingerprint differ. Only v2 nested pairs pass compatibility."
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--release", type=Path, default=Path("benchmark/combined/v2"))
    parser.add_argument("--corpus-dir", type=Path, default=Path("corpus/combined-v2"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = analyze(args.release, args.corpus_dir)
    with args.output.open("x") as stream:
        json.dump(result, stream, indent=2, ensure_ascii=False, allow_nan=False)
        stream.write("\n")
    print(f"Verified 158 combined IDs and {result['retrieval_calls']} local calls with all nested comparisons")
