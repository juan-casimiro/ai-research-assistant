#!/usr/bin/env python3
"""Category-aware retrieval evaluation harness against golden_qa.json.

Usage:
    python eval_golden.py                  # vector-only baseline
    python eval_golden.py --bm25           # enable BM25 hybrid fusion
    python eval_golden.py --rewrite        # enable LLM query rewriting
    python eval_golden.py --bm25 --rewrite # both strategies on
"""
import argparse
import asyncio
import json
from pathlib import Path

from main import retrieve

GOLDEN_QA_PATH = Path("./golden_qa.json")
RESULTS_PATH = Path("./eval_results.json")
N_VALUES = [3, 8]


def build_config_label(use_bm25: bool, use_rewrite: bool) -> str:
    """Generate a human-readable config label from runtime flags."""
    parts = ["vector"]
    if use_bm25:
        parts.append("bm25")
    if use_rewrite:
        parts.append("rewrite")
    return "-".join(parts) if len(parts) > 1 else "vector-only-baseline"


def score_query(sources: list[str], query: dict) -> str:
    """Return 'pass', 'fail', or 'not_scored' for a single query."""
    category = query.get("category")

    if category == "unanswerable":
        return "not_scored"

    if category in ("direct_lookup", "multi_hop"):
        expected = query.get("expected_doc")
        if not expected:
            return "fail"
        return "pass" if expected in sources else "fail"

    if category == "cross_doc_distractor":
        expected = query.get("expected_doc")
        distractor = query.get("distractor_doc")
        if not expected:
            return "fail"
        if expected not in sources:
            return "fail"
        if distractor and distractor in sources:
            if sources.index(expected) >= sources.index(distractor):
                return "fail"
        return "pass"

    if category == "cross_doc_synthesis":
        expected_docs = query.get("expected_docs", [])
        if not expected_docs:
            return "fail"
        return "pass" if all(doc in sources for doc in expected_docs) else "fail"

    return "fail"


async def main() -> int:
    parser = argparse.ArgumentParser(
        description="Evaluate retrieval against the golden QA dataset."
    )
    parser.add_argument(
        "--bm25",
        action="store_true",
        default=False,
        help="Enable BM25 sparse retrieval via reciprocal rank fusion",
    )
    parser.add_argument(
        "--rewrite",
        action="store_true",
        default=False,
        help="Enable LLM query rewriting before retrieval",
    )
    args = parser.parse_args()

    use_bm25: bool = args.bm25
    use_rewrite: bool = args.rewrite
    config_label = build_config_label(use_bm25, use_rewrite)

    # ------------------------------------------------------------------
    # Runtime config banner
    # ------------------------------------------------------------------
    print("=" * 70)
    print("RETRIEVAL EVALUATION HARNESS")
    print("=" * 70)
    print(f"  Config label : {config_label}")
    print(f"  BM25         : {use_bm25}")
    print(f"  Query rewrite: {use_rewrite}")
    print(f"  N values     : {N_VALUES}")
    print("=" * 70)
    print()

    if not GOLDEN_QA_PATH.exists():
        print(f"Golden QA file not found: {GOLDEN_QA_PATH}")
        return 1

    golden = json.loads(GOLDEN_QA_PATH.read_text())
    queries = golden.get("queries", [])

    results: list[dict] = []
    scored_categories = [
        "direct_lookup",
        "multi_hop",
        "cross_doc_distractor",
        "cross_doc_synthesis",
    ]

    # ------------------------------------------------------------------
    # Run every query at both n=3 and n=8
    # ------------------------------------------------------------------
    for q in queries:
        q_id = q["id"]
        question = q["question"]
        category = q["category"]

        print(f"  {q_id} ({category:<22}) ... ", end="", flush=True)

        entry = {
            "id": q_id,
            "question": question,
            "category": category,
            "expected_doc": q.get("expected_doc"),
            "expected_docs": q.get("expected_docs"),
            "distractor_doc": q.get("distractor_doc"),
        }

        for n in N_VALUES:
            _, sources = await retrieve(
                question,
                n_results=n,
                use_query_rewriting=use_rewrite,
                use_bm25=use_bm25,
            )
            verdict = score_query(sources, q)
            entry[f"n{n}"] = {
                "retrieved_sources": sources,
                "verdict": verdict,
            }

        results.append(entry)
        print(f"n3={entry['n3']['verdict']:<12} n8={entry['n8']['verdict']}")

    # ------------------------------------------------------------------
    # Aggregate
    # ------------------------------------------------------------------
    stats = {
        cat: {3: {"pass": 0, "total": 0}, 8: {"pass": 0, "total": 0}}
        for cat in scored_categories
    }
    overall = {3: {"pass": 0, "total": 0}, 8: {"pass": 0, "total": 0}}
    unanswerable_count = 0

    for entry in results:
        cat = entry["category"]
        if cat == "unanswerable":
            unanswerable_count += 1
            continue

        for n in N_VALUES:
            verdict = entry[f"n{n}"]["verdict"]
            if cat in stats:
                stats[cat][n]["total"] += 1
                if verdict == "pass":
                    stats[cat][n]["pass"] += 1
            overall[n]["total"] += 1
            if verdict == "pass":
                overall[n]["pass"] += 1

    # ------------------------------------------------------------------
    # Console report
    # ------------------------------------------------------------------
    print("\n" + "=" * 70)
    print("RETRIEVAL EVALUATION SUMMARY")
    print(f"Config: {config_label}")
    print(f"BM25: {use_bm25} | Rewrite: {use_rewrite}")
    print("=" * 70)
    print(f"{'Category':<25} {'n=3':>20} {'n=8':>20}")
    print("-" * 70)

    for cat in scored_categories:
        p3, t3 = stats[cat][3]["pass"], stats[cat][3]["total"]
        p8, t8 = stats[cat][8]["pass"], stats[cat][8]["total"]
        a3 = (p3 / t3 * 100) if t3 else 0.0
        a8 = (p8 / t8 * 100) if t8 else 0.0
        print(f"{cat:<25} {p3:>3}/{t3:<3} ({a3:>5.1f}%)   {p8:>3}/{t8:<3} ({a8:>5.1f}%)")

    print("-" * 70)
    print(f"{'unanswerable':<25} {unanswerable_count} logged, not scored")
    print("-" * 70)

    o3, o8 = overall[3], overall[8]
    oa3 = (o3["pass"] / o3["total"] * 100) if o3["total"] else 0.0
    oa8 = (o8["pass"] / o8["total"] * 100) if o8["total"] else 0.0
    print(f"{'OVERALL':<25} {o3['pass']:>3}/{o3['total']:<3} ({oa3:>5.1f}%)   {o8['pass']:>3}/{o8['total']:<3} ({oa8:>5.1f}%)")
    print("=" * 70)

    # ------------------------------------------------------------------
    # Write JSON artifact
    # ------------------------------------------------------------------
    output = {
        "config_label": config_label,
        "config": {
            "use_bm25": use_bm25,
            "use_query_rewriting": use_rewrite,
            "n_values": N_VALUES,
        },
        "results": results,
    }
    RESULTS_PATH.write_text(json.dumps(output, indent=2))
    print(f"\nPer-query details written to {RESULTS_PATH}")

    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))