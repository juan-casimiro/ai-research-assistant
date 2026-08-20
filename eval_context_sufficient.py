#!/usr/bin/env python3
"""Measures context_sufficient flag accuracy against golden QA ground truth.

Requires a running server: `uvicorn main:app` in a separate terminal.

Usage:
    python eval_context_sufficient.py
"""
import json
import random
from pathlib import Path

import httpx

GOLDEN_QA_PATH = Path("./golden_qa.json")
BASELINE_RESULTS_PATH = Path("./eval_results/eval_results_baseline.json")
OUTPUT_PATH = Path("./context_sufficient_eval_results.json")
QUERY_URL = "http://localhost:8000/query"

# Known false-premise case (ADR-001/ADR-002): the model correctly reports
# `true` here even though the golden label is `unanswerable`. Counting it
# would mislabel correct behaviour as a flag error.
FALSE_PREMISE_EXCLUSIONS = {"q083"}

SAMPLE_SEED = 42  # fixed for reproducibility across runs
N_PASSING_SAMPLE = 29


def build_false_bucket() -> list[dict]:
    """All valid unanswerable queries (expected_sufficient=False)."""
    golden = json.loads(GOLDEN_QA_PATH.read_text())
    queries = [
        q for q in golden["queries"]
        if q["category"] == "unanswerable" and q["id"] not in FALSE_PREMISE_EXCLUSIONS
    ]
    return [{"id": q["id"], "question": q["question"], "expected_sufficient": False} for q in queries]

def build_true_bucket() -> list[dict]:
    """Random sample of queries that passed retrieval at n=8 in the baseline eval.
    Ground truth: context_sufficient should be True.
    """
    baseline = json.loads(BASELINE_RESULTS_PATH.read_text())
    passing = [r for r in baseline["results"] if r.get("n8", {}).get("verdict") == "pass"]

    rng = random.Random(SAMPLE_SEED)
    sampled = rng.sample(passing, min(N_PASSING_SAMPLE, len(passing)))

    return [{"id": r["id"], "question": r["question"], "expected_sufficient": True} for r in sampled]

def query_service(question: str) -> bool:
    """Hit /query with the production-matching config and return context_sufficient."""
    response = httpx.post(
        QUERY_URL,
        json={"question": question, "n_results": 8},
        timeout=60.0,  # retrieval + reranking + an LLM call
    )
    response.raise_for_status()
    return response.json()["context_sufficient"]


def main() -> int:
    print("=" * 70)
    print("CONTEXT_SUFFICIENT ACCURACY EVALUATION")
    print("=" * 70)

    samples = build_false_bucket() + build_true_bucket()
    print(f"  Sample size  : {len(samples)}  "
          f"({sum(1 for s in samples if not s['expected_sufficient'])} expected-False, "
          f"{sum(1 for s in samples if s['expected_sufficient'])} expected-True)")
    print("=" * 70)
    print()

    results: list[dict] = []
    false_positives = 0  # flag says True, should've been False
    false_negatives = 0  # flag says False, should've been True

    for s in samples:
        print(f"  {s['id']:<6} expected={s['expected_sufficient']!s:<5} ... ", end="", flush=True)
        actual = query_service(s["question"])
        correct = actual == s["expected_sufficient"]

        if not correct and s["expected_sufficient"] is False:
            false_positives += 1
        elif not correct and s["expected_sufficient"] is True:
            false_negatives += 1

        print(f"actual={actual!s:<5} {'OK' if correct else 'MISMATCH'}")
        results.append({**s, "actual_sufficient": actual, "correct": correct})

    # ------------------------------------------------------------------
    false_bucket_total = sum(1 for s in samples if not s["expected_sufficient"])
    true_bucket_total = sum(1 for s in samples if s["expected_sufficient"])

    fp_rate = false_positives / false_bucket_total if false_bucket_total else 0.0
    fn_rate = false_negatives / true_bucket_total if true_bucket_total else 0.0

    print()
    print("=" * 70)
    print("RESULTS")
    print("=" * 70)
    print(f"  False positives (flag=True, should be False): {false_positives}/{false_bucket_total} ({fp_rate:.1%})")
    print(f"  False negatives (flag=False, should be True): {false_negatives}/{true_bucket_total} ({fn_rate:.1%})")
    print("=" * 70)

    OUTPUT_PATH.write_text(json.dumps({
        "sample_size": len(samples),
        "false_positive_rate": fp_rate,
        "false_negative_rate": fn_rate,
        "false_positives": false_positives,
        "false_bucket_total": false_bucket_total,
        "false_negatives": false_negatives,
        "true_bucket_total": true_bucket_total,
        "results": results,
    }, indent=2))
    print(f"\nPer-query details written to {OUTPUT_PATH}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())