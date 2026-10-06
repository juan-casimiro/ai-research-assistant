"""Verify and re-envelope historical contexts without repeating retrieval.

The derived result names/hashes its immutable parent and keeps original
provenance. It is never represented as a fresh retrieval execution.
"""
from __future__ import annotations

import argparse
from collections import Counter
import copy
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from benchmark_scoring import (canonical_hash, compile_anchor_spans,
                               compile_query_feasibility, score_evidence)
from eval_benchmark import read_release, summarize
from main import chunk_text


def derive(parent_path, release, corpus, condition_name, output_path):
    parent_bytes = parent_path.read_bytes()
    parent = json.loads(parent_bytes)
    benchmark, _, conditions, condition, tuples, texts = read_release(release, corpus, condition_name)
    provenance = parent["provenance"]
    queries = benchmark["queries"]
    expected = sorted(q["id"] for q in queries)
    if (parent["run_status"] != "complete" or provenance["missing_ids"] != [] or
            sorted(provenance["requested_ids"]) != expected or
            sorted(provenance["executed_ids"]) != expected or
            sorted(r["id"] for r in parent["results"]) != expected):
        raise ValueError("parent coverage is incomplete or duplicated")
    if provenance["query_sha256"] != benchmark["parent"]["query_sha256"]:
        raise ValueError("parent does not match frozen topic snapshot")
    if {canonical_hash(t) for t in provenance["article_tuples"]} != {canonical_hash(t) for t in tuples}:
        raise ValueError("parent corpus differs from baseline condition")
    if canonical_hash(provenance["article_tuples"]) != provenance["membership_sha256"]:
        raise ValueError("parent membership hash is inconsistent")
    scorer_hash = canonical_hash({"scoring": hashlib.sha256((ROOT / "benchmark_scoring.py").read_bytes()).hexdigest(),
                                 "adapter": hashlib.sha256((ROOT / "eval_benchmark.py").read_bytes()).hexdigest()})
    if scorer_hash != provenance["scorer_sha256"]:
        raise ValueError("parent scorer differs; separate reviewed rescoring required")
    anchors = {a["id"]: a for a in benchmark["anchors"]}
    used = {aid for q in queries for e in q["evidence_sets"] for aid in e["anchors"]}
    plans = compile_anchor_spans({aid: anchors[aid] for aid in used}, texts, chunk_text)
    feasibility = compile_query_feasibility(queries, anchors, plans,
        {source: chunk_text(text) for source, text in texts.items()})
    if canonical_hash(feasibility) != provenance["feasibility_sha256"]:
        raise ValueError("parent evidence feasibility differs")
    by_id = {q["id"]: q for q in queries}
    source_chunks = {source: chunk_text(text) for source, text in texts.items()}
    available = Counter((source, chunk) for source, chunks in source_chunks.items() for chunk in chunks)
    for entry in parent["results"]:
        query = by_id[entry["id"]]
        if entry["query_sha256"] != canonical_hash(query) or entry["question"] != query["question"]:
            raise ValueError(f"{query['id']}: changed query/gold")
        for depth in [3, 8]:
            result = entry[f"n{depth}"]
            if len(result["retrieved_contexts"]) > depth:
                raise ValueError("parent exceeds chunk budget")
            contexts, sources = result["retrieved_contexts"], result["retrieved_sources"]
            if len(contexts) != len(sources) or not Counter(zip(sources, contexts)) <= available:
                raise ValueError("parent context is not a pinned production chunk")
            if score_evidence(result["retrieved_contexts"], result["retrieved_sources"], query, anchors, plans) != result["metrics"]:
                raise ValueError(f"{query['id']}: parent metrics differ from verified saved contexts")
    output = copy.deepcopy(parent)
    output["run_id"] += "-combined-envelope"
    output["derivation"] = {"kind": "verified_comparison_envelope", "retrieval_calls": 0,
        "parent_path": str(parent_path), "parent_sha256": hashlib.sha256(parent_bytes).hexdigest(),
        "parent_run_id": parent["run_id"], "parent_provenance": provenance,
        "helper_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "reason": "Identical per-query hashes, source tuples, scorer and feasibility; saved contexts rechecked. Only selection/query/condition envelope linkage changes."}
    output["provenance"].update(query_version=benchmark["query_version"],
        query_sha256=canonical_hash(benchmark), subset_sha256=canonical_hash(queries),
        selection_sha256=benchmark["selection_sha256"], conditions_sha256=canonical_hash(conditions),
        condition=condition_name, membership_sha256=condition["membership_sha256"], article_tuples=tuples)
    output["summary"] = summarize(output["results"])
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("x", encoding="utf-8") as stream:
        json.dump(output, stream, indent=2, ensure_ascii=False, allow_nan=False)
        stream.write("\n")
    print(f"Verified {len(queries)} unchanged cases; derived {output_path}; zero retrieval calls")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("parent", type=Path)
    parser.add_argument("--benchmark", type=Path, required=True)
    parser.add_argument("--corpus-dir", type=Path, required=True)
    parser.add_argument("--condition", choices=["C1", "C2"], required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    derive(args.parent, args.benchmark, args.corpus_dir, args.condition, args.output)
