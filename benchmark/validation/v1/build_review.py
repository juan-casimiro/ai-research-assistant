"""Build the Stage 6 external-review cases: a second opinion from another model.

Selects the cases whose verdict rests on Claude's judgment alone: every
adjudicated case, every minor note the auditor recorded without adjudication,
and every case whose gold Claude authored. Each case file carries the gold, the
first review and the article text around each anchor, so the reviewer rarely
needs to search. No model is called here.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from assemble import gold_records
from build_workspace import GOLD_WS, write_json
from stage0 import HERE, ROOT, SETS, load

CONTEXT_CHARS = 2500
RUNNER = {"cli": "codex", "model": "gpt-6.1-sol", "reasoning_effort": "medium",
          "extra_args": ["--ignore-user-config"], "workspace": GOLD_WS}


def context_windows(anchors: list[dict], articles: Path) -> list[dict]:
    """Text around each anchor, merged where windows in one file overlap."""
    spans = {}
    for anchor in anchors:
        spans.setdefault(anchor["file"], []).append(
            (max(0, anchor["text_start"] - CONTEXT_CHARS), anchor["text_end"] + CONTEXT_CHARS, anchor["id"]))
    windows = []
    for file, items in spans.items():
        text = (articles / file).read_text(encoding="utf-8")
        merged = []
        for start, end, anchor_id in sorted(items):
            if merged and start <= merged[-1][1]:
                merged[-1] = (merged[-1][0], max(end, merged[-1][1]), merged[-1][2] + [anchor_id])
            else:
                merged.append((start, end, [anchor_id]))
        for start, end, ids in merged:
            end = min(end, len(text))
            windows.append({"file": file, "anchors": ids,
                            "lines": [text.count("\n", 0, start) + 1, text.count("\n", 0, end) + 1],
                            "text": text[start:end]})
    return windows


def first_review(case: dict) -> tuple[dict, str]:
    final, audit = case["adjudication"], case["audit"]
    if final:
        return ({"stage": "adjudication", "verdict": final["verdict"], "severity": final["severity"],
                 "gold_stands": final["gold_stands"], "rationale": final["rationale"],
                 "evidence": [{k: e[k] for k in ("file", "quote", "point")} for e in final["evidence"]],
                 "proposed_correction": final["proposed_correction"]},
                "Reviewers disagreed about this case and it was adjudicated.")
    review = {"stage": "audit", "verdict": audit["verdict"], "severity": audit["severity"],
              "rationale": audit["summary"], "evidence": [], "proposed_correction": audit["proposed_correction"]}
    if case["verdict"] == "valid_minor":
        return review, "One reviewer recorded a minor note and no second reviewer checked it."
    return review, "The answer key and its only review come from the same model family."


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus-dir", type=Path, required=True)
    parser.add_argument("--workspace-root", type=Path, required=True)
    args = parser.parse_args()
    root = args.workspace_root.resolve()
    hunt = root / GOLD_WS / "hunt"
    findings = {c["id"]: c for c in load(HERE / "results" / "full_findings.json")["cases"]}
    records = gold_records(args.corpus_dir)
    author = {q["id"]: q["review"].get("author") for rel in SETS.values() for q in load(ROOT / rel)["queries"]}

    selected = {}
    for case_id, case in findings.items():
        reasons = []
        if case["adjudication"]:
            reasons.append("adjudicated")
        elif case["verdict"] == "valid_minor":
            reasons.append("audit_minor_note")
        if author[case_id] == "Claude":
            reasons.append("claude_authored_gold")
        if reasons:
            selected[case_id] = reasons

    batches = []
    for case_id in sorted(selected):
        gold = records[case_id]["gold"]
        review, why = first_review(findings[case_id])
        path = hunt / "cases" / f"review6-{case_id}.json"
        write_json(path, {**gold, "context": context_windows(gold["anchors"], hunt / "articles"),
                          "first_review": {**review, "why_reviewed": why}})
        batches.append({"batch_id": f"review6-{case_id}", "cases": [case_id], "selected_for": selected[case_id],
                        "batch_file": str(path.relative_to(root))})
    write_json(hunt / "cases" / "review6_batches.json", {"runner": RUNNER, "stage6_review": batches})
    counts = {}
    for reasons in selected.values():
        for reason in reasons:
            counts[reason] = counts.get(reason, 0) + 1
    print(json.dumps({"cases": len(batches), "by_reason": counts,
                      "batch_list": str(hunt / "cases" / "review6_batches.json")}))


if __name__ == "__main__":
    main()
