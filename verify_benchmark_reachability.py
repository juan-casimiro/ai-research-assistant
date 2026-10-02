"""Offline structural check: all production chunks must cover all pinned gold.

This is an oracle, not a retrieval-quality measurement. It loads no models,
opens no collection and makes no API calls. Corpus files remain local/ignored.
"""
import argparse
import json
from pathlib import Path

from benchmark_scoring import (compile_anchor_spans, compile_query_feasibility,
                               minimum_evidence_witness, normalize_excerpt, score_evidence)
from eval_benchmark import read_release


def verify_reachability(benchmark: dict, source_text: dict, chunker) -> dict:
    anchors = {a["id"]: a for a in benchmark["anchors"]}
    available = {aid: a for aid, a in anchors.items() if a["filename"] in source_text}
    plans = compile_anchor_spans(available, source_text, chunker)
    source_chunks = {source: chunker(text) for source, text in source_text.items()}
    pairs = [(chunk, source) for source, chunks in source_chunks.items() for chunk in chunks]
    contexts, sources = [p[0] for p in pairs], [p[1] for p in pairs]
    single_chunk_misses = [aid for aid, a in available.items() if not any(
        source == a["filename"] and normalize_excerpt(a["excerpt"]) in normalize_excerpt(chunk)
        for chunk, source in pairs)]
    for aid in available:
        anchor_query = {"answerability": {"status": "answerable"}, "category": "direct_lookup",
                        "required_facts": [{"id": "span"}], "related_distractors": [],
                        "evidence_sets": [{"anchors": [aid], "fact_anchors": {"span": [aid]}}]}
        if score_evidence(contexts, sources, anchor_query, anchors, plans)["evidence_coverage"] != "pass":
            raise ValueError(f"{aid}: pinned span cannot be scored with every production chunk")
    scored = [q for q in benchmark["queries"] if q["evidence_sets"]]
    unreachable = []
    for query in scored:
        result = score_evidence(contexts, sources, query, anchors, plans)
        if result["evidence_coverage"] != "pass" or result["fact_recall"] != 1:
            unreachable.append(query["id"])
    if unreachable:
        raise ValueError(f"gold is unreachable even with every production chunk: {unreachable}")
    feasibility = compile_query_feasibility(benchmark["queries"], anchors, plans, source_chunks)
    # Exercise the scorer on each minimum-sized witness, not just on the corpus.
    for query in scored:
        witness = minimum_evidence_witness(query, anchors, plans, source_chunks)
        witness_pairs = [pair for pair, count in witness.items() for _ in range(count)]
        witness_sources = [source for source, _ in witness_pairs]
        witness_contexts = [chunk for _, chunk in witness_pairs]
        result = score_evidence(witness_contexts, witness_sources, query, anchors, plans)
        if result["evidence_coverage"] != "pass" or result["fact_recall"] != 1:
            raise ValueError(f"{query['id']}: minimum-chunk witness cannot be scored")
    by_depth = {}
    for depth in [3, 8]:
        feasible = sorted(q["id"] for q in scored if feasibility[q["id"]]["by_depth"][f"n{depth}"] == "feasible")
        infeasible = sorted(q["id"] for q in scored if q["id"] not in feasible)
        by_depth[f"n{depth}"] = {"feasible_queries": len(feasible), "total_queries": len(scored),
                                 "ceiling_rate": len(feasible) / len(scored) if scored else None,
                                 "feasible_ids": feasible, "infeasible_ids": infeasible}
    return {"available_anchors": len(available), "reachable_anchors": len(plans),
            "anchors_requiring_adjacent_chunks": len(single_chunk_misses),
            "evidence_queries": len(scored), "unlimited_reachable_evidence_queries": len(scored),
            "by_depth": by_depth, "query_feasibility": feasibility,
            "production_chunks": len(pairs), "retrieval_quality_measured": False}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--benchmark", type=Path, default=Path("benchmark/cardiology/v1"))
    parser.add_argument("--corpus-dir", type=Path, default=Path("corpus/cardiology-v1"))
    parser.add_argument("--condition", choices=["C1", "C2", "C3"], default="C2")
    args = parser.parse_args()
    try:
        benchmark, _, _, _, _, text = read_release(args.benchmark, args.corpus_dir, args.condition)
        from main import chunk_text
        print(json.dumps(verify_reachability(benchmark, text, chunk_text), indent=2))
        return 0
    except (OSError, ValueError, KeyError) as error:
        print(f"ERROR: {type(error).__name__}: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
