#!/usr/bin/env python3
"""Compare two eval_results.json files side-by-side.

Usage:
    python compare_evals.py eval_results_baseline.json eval_results_bm25.json
"""
import argparse
import json
from pathlib import Path


def load_results(path: Path) -> dict:
    data = json.loads(path.read_text())
    return {r["id"]: r for r in data["results"]}


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare two eval result files.")
    parser.add_argument("baseline", type=Path)
    parser.add_argument("experiment", type=Path)
    args = parser.parse_args()

    base = load_results(args.baseline)
    exp = load_results(args.experiment)

    scored = [qid for qid in base if base[qid]["category"] != "unanswerable"]
    scored.sort()

    # Overall delta
    for n in [3, 8]:
        base_pass = sum(1 for qid in scored if base[qid][f"n{n}"]["verdict"] == "pass")
        exp_pass = sum(1 for qid in scored if exp[qid][f"n{n}"]["verdict"] == "pass")
        print(f"\nn={n}: {base_pass}/{len(scored)} → {exp_pass}/{len(scored)}  (Δ {exp_pass - base_pass:+d})")

    # Per-query flips
    print("\n" + "=" * 70)
    print("PER-QUERY CHANGES")
    print("=" * 70)
    flips = []
    for qid in scored:
        for n in [3, 8]:
            b = base[qid][f"n{n}"]["verdict"]
            e = exp[qid][f"n{n}"]["verdict"]
            if b != e:
                flips.append((qid, n, b, e, base[qid]["category"]))

    if not flips:
        print("No changes between runs.")
        return

    for qid, n, b, e, cat in flips:
        marker = "✓ IMPROVED" if e == "pass" else "✗ REGRESSED"
        print(f"{marker}  {qid} ({cat}) @ n={n}: {b} → {e}")


if __name__ == "__main__":
    main()