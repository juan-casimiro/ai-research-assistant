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
    if len({r["id"] for r in data["results"]}) != len(data["results"]):
        raise ValueError("duplicate result IDs")
    return {r["id"]: r for r in data["results"]}


def check_compatible(baseline: dict, experiment: dict, *, allow_legacy=False,
                     nested_corpus=False) -> None:
    """Reject mismatched coverage, revised cases and unverified provenance."""
    pairs = []
    for data in [baseline, experiment]:
        results = data["results"]
        ids = [r["id"] for r in results]
        if not ids or len(set(ids)) != len(ids):
            raise ValueError("empty or duplicate result IDs")
        pairs.append({r["id"]: r for r in results})
    base, exp = pairs
    if base.keys() != exp.keys():
        raise ValueError("requested/executed query sets differ; partial comparisons are not supported")
    for qid in base:
        for field in ["question", "category", "revision", "query_sha256", "expected_doc",
                      "expected_docs", "distractor_doc", "answerability"]:
            if base[qid].get(field) != exp[qid].get(field):
                raise ValueError(f"{qid}: incompatible question, revision or gold labels ({field})")
        for depth in ["n3", "n8"]:
            if depth not in base[qid] or depth not in exp[qid]:
                raise ValueError(f"{qid}: missing depth {depth}")
            for result in [base[qid][depth], exp[qid][depth]]:
                if result.get("verdict") not in {"pass", "fail", "not_scored"}:
                    raise ValueError(f"{qid}: missing or invalid verdict")
    provenance = [data.get("provenance") for data in [baseline, experiment]]
    if not all(provenance):
        if any(provenance) or not allow_legacy or nested_corpus:
            raise ValueError("missing provenance; historical pairs require --allow-legacy and cannot be mixed with versioned runs")
        return
    bp, ep = provenance
    from benchmark_scoring import canonical_hash, validate_answerability
    for field in ["query_version", "query_sha256", "scorer_version", "scorer_sha256",
                  "retrieval_sha256", "selection_sha256", "subset_sha256", "conditions_sha256", "depths"]:
        if not bp.get(field) or bp[field] != ep.get(field):
            raise ValueError(f"incompatible or missing {field}")
    for data, prov in zip([baseline, experiment], provenance):
        if data.get("run_status", "complete") != "complete":
            raise ValueError("incomplete run/checkpoint cannot be compared")
        if prov.get("missing_ids") != [] or sorted(prov.get("requested_ids", [])) != sorted(base) or sorted(prov.get("executed_ids", [])) != sorted(base):
            raise ValueError("incomplete requested-ID coverage")
        if prov["depths"] != [3, 8] or data["config"].get("n_values") != [3, 8]:
            raise ValueError("incompatible depths")
        tuples = prov.get("article_tuples", [])
        if (not tuples or len({t["article_id"] for t in tuples}) != len(tuples) or
                canonical_hash(tuples) != prov.get("membership_sha256")):
            raise ValueError("missing or inconsistent corpus membership fingerprint")
        for result in data["results"]:
            if not result.get("revision") or not result.get("query_sha256") or not result.get("answerability"):
                raise ValueError("missing per-query revision/fingerprint/answerability")
            validate_answerability(result["category"], result["answerability"])
            for depth in ["n3", "n8"]:
                metrics = result[depth].get("metrics", {})
                if any(metrics.get(m) not in {"pass", "fail", "not_scored"}
                       for m in ["document_coverage", "evidence_coverage", "distractor_ordering"]):
                    raise ValueError("missing or invalid versioned retrieval metrics")
                recall = metrics.get("fact_recall")
                if result["answerability"] != "absent_fact" and (type(recall) not in {int, float} or not 0 <= recall <= 1):
                    raise ValueError("missing or invalid fact recall")
    if nested_corpus:
        if baseline["config"] != experiment["config"]:
            raise ValueError("nested-corpus comparison requires identical retrieval flags/settings")
        bt, et = bp.get("article_tuples"), ep.get("article_tuples")
        if not bt or not et or not bp.get("conditions_sha256") or bp["conditions_sha256"] != ep.get("conditions_sha256"):
            raise ValueError("missing or incompatible declared nested conditions")
        if not {canonical_hash(t) for t in bt} <= {canonical_hash(t) for t in et}:
            raise ValueError("experiment is not a superset with identical common article versions/hashes")
    elif not bp.get("membership_sha256") or bp["membership_sha256"] != ep.get("membership_sha256"):
        raise ValueError("configuration comparison requires identical corpus membership")


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare two eval result files.")
    parser.add_argument("baseline", type=Path)
    parser.add_argument("experiment", type=Path)
    parser.add_argument("--allow-legacy", action="store_true", help="Explicitly inspect an unverifiable historical pair")
    parser.add_argument("--nested-corpus", action="store_true", help="Compare declared nested corpora with identical settings")
    args = parser.parse_args()

    try:
        baseline = json.loads(args.baseline.read_text())
        experiment = json.loads(args.experiment.read_text())
        check_compatible(baseline, experiment, allow_legacy=args.allow_legacy,
                         nested_corpus=args.nested_corpus)
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.error(str(error))
    if not baseline.get("provenance"):
        print("HISTORICAL / UNVERIFIABLE: matching saved cases, without corpus/scorer fingerprints")

    base = load_results(args.baseline)
    exp = load_results(args.experiment)

    scored = [qid for qid in base if base[qid]["category"] not in {"unanswerable", "false_premise"}]
    scored.sort()

    print("Document-level/category-ranking pass rate; this does not measure answer correctness.")
    # Overall delta
    for n in [3, 8]:
        base_pass = sum(1 for qid in scored if base[qid][f"n{n}"]["verdict"] == "pass")
        exp_pass = sum(1 for qid in scored if exp[qid][f"n{n}"]["verdict"] == "pass")
        print(f"\nn={n}: {base_pass}/{len(scored)} → {exp_pass}/{len(scored)}  (Δ {exp_pass - base_pass:+d})")
        if baseline.get("provenance"):
            for metric in ["document_coverage", "evidence_coverage"]:
                counts = [sum(data[qid][f"n{n}"]["metrics"][metric] == "pass" for qid in scored)
                          for data in [base, exp]]
                print(f"  {metric}: {counts[0]}/{len(scored)} → {counts[1]}/{len(scored)}")

    # Per-query flips
    print("\n" + "=" * 70)
    print("PER-QUERY CHANGES")
    print("=" * 70)
    flips = []
    change_ids = [qid for qid in base if base[qid]["category"] != "unanswerable"] if baseline.get("provenance") else scored
    for qid in sorted(change_ids):
        for n in [3, 8]:
            b = base[qid][f"n{n}"]["verdict"]
            e = exp[qid][f"n{n}"]["verdict"]
            if b != e:
                flips.append((qid, n, "category verdict", b, e, base[qid]["category"]))
            if baseline.get("provenance"):
                for metric in ["document_coverage", "evidence_coverage", "fact_recall", "distractor_ordering"]:
                    b = base[qid][f"n{n}"]["metrics"][metric]
                    e = exp[qid][f"n{n}"]["metrics"][metric]
                    if b != e:
                        flips.append((qid, n, metric, b, e, base[qid]["category"]))

    if not flips:
        print("No changes between runs.")
        return

    for qid, n, metric, b, e, cat in flips:
        if isinstance(b, (int, float)) and isinstance(e, (int, float)):
            marker = "IMPROVED" if e > b else "REGRESSED"
        else:
            marker = "IMPROVED" if e == "pass" else "REGRESSED"
        print(f"{marker}  {qid} ({cat}) @ n={n} {metric}: {b} → {e}")


if __name__ == "__main__":
    main()
