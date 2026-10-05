"""Join stage results: build Stage 4 and Stage 5 inputs, then the findings.

  compare   Stage 1 results + gold  -> Stage 4 batches
  escalate  Stages 0-4              -> Stage 5 case files for disputed cases
  findings  everything              -> results/<label>_findings.json

Seeded calibration cases (--seed-key) never reach Stage 4 or 5; they are scored
for detection in the findings. No model is called here.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from build_workspace import GOLD_WS, audit_record, chunks, write_json
from stage0 import HERE, ROOT, SETS, load

BREAKING = {"H1", "H2", "H3", "H4", "H6"}
BLIND_STATUS = {"answerable": "answerable", "not_in_articles": "absent_fact", "premise_wrong": "false_premise"}
COMPARE_BATCH = 10


def group_results(group: str) -> tuple[dict, list[dict], dict]:
    """Accepted case outputs, coverage gaps and run totals of one result group."""
    cases, gaps = {}, []
    totals = {"batches_ok": 0, "batches_gap": 0, "duration_s": 0.0, "quotes_verified": 0, "quotes_total": 0, "usage": []}
    for path in sorted((HERE / "results" / group).glob("*.json")):
        record = load(path)
        if path.name.endswith(".gap.json"):
            gaps.append(record)
            totals["batches_gap"] += 1
            continue
        totals["batches_ok"] += 1
        totals["duration_s"] += record["duration_s"]
        totals["quotes_verified"] += record["quotes"]["verified"]
        totals["quotes_total"] += record["quotes"]["total"]
        totals["usage"].append({"batch_id": record["batch_id"], "attempts": record["attempts"], "usage": record["usage"]})
        output = record["output"]
        for case in output["cases"] if "cases" in output else [output]:
            cases[case["id"]] = case
    return cases, gaps, totals


def gold_records(corpus_dir: Path) -> dict:
    """Audit-form gold record and set name for every real case, keyed by ID."""
    stage0 = {(c["set"], c["id"]): c for c in load(HERE / "results" / "stage0.json")["cases"]}
    name_of = {a["pmcid"]: Path(a["txt"]["path"]).name for a in load(corpus_dir / "inventory.json")["articles"]}
    records = {}
    for name, relative in SETS.items():
        benchmark = load(ROOT / relative)
        anchors = {a["id"]: a for a in benchmark["anchors"]}
        for query in benchmark["queries"]:
            if query["id"] in records:
                raise SystemExit(f"case ID {query['id']} is not unique across sets")
            records[query["id"]] = {"set": name, "stage0": stage0[(name, query["id"])],
                                    "gold": audit_record(query, anchors, name_of, stage0[(name, query["id"])]["warnings"])}
    return records


def condition_of(file: str, set_name: str, manifest: dict) -> str:
    """Smallest corpus condition of the case's set in which this article appears."""
    conditions = manifest["sets"][set_name]["conditions"]
    for label in ("C1", "C2"):
        if file in conditions[label]:
            return label
    if set_name != "als-ftd" and file in manifest["sets"]["als-ftd"]["articles"]:
        return "als_ftd_only"
    return "C3"


def tagged_hunt(case: dict | None, set_name: str, manifest: dict) -> dict | None:
    if case is None:
        return None
    findings = [{**f, "condition": condition_of(Path(f["file"]).name, set_name, manifest)} for f in case["findings"]]
    return {**case, "findings": findings}


def escalation_reasons(record: dict, blind, audit, hunt, compare) -> list[str]:
    reasons = [f"stage 0: {m}" for m in record["stage0"]["failures"]]
    if compare and compare["escalate"]:
        reasons += [f"compare: {r}" for r in compare["reasons"]] or ["compare: escalated"]
    if audit and audit["verdict"] not in ("valid", "valid_minor"):
        reasons.append(f"audit: {audit['verdict']} ({audit['severity']}) — {audit['summary']}")
    for finding in (hunt or {}).get("findings", []):
        if finding["type"] in BREAKING and finding["strength"] != "weak":
            verified = "" if finding.get("quote_verified") else ", quote not verified"
            reasons.append(f"hunt: {finding['type']} {finding['strength']} in {finding['file']} "
                           f"[{finding['condition']}{verified}]")
    return reasons


def load_stages(args, manifest: dict, records: dict) -> dict:
    seeds = load(args.seed_key) if args.seed_key else {}
    blind, blind_gaps, blind_run = group_results(args.blind_group)
    audit, audit_gaps, audit_run = group_results(args.audit_group)
    hunt, hunt_gaps, hunt_run = group_results(args.hunt_group)
    compare, compare_gaps, compare_run = group_results(f"{args.label}_stage4")
    final, final_gaps, final_run = group_results(f"{args.label}_stage5")
    in_scope = sorted((set(blind) | set(audit) | set(hunt)) - set(seeds))
    in_scope += sorted({i for g in blind_gaps + audit_gaps + hunt_gaps for i in g["cases"]} - set(seeds) - set(in_scope))
    unknown = [i for i in in_scope if i not in records]
    if unknown:
        raise SystemExit(f"results name cases that are neither gold nor seeds: {unknown}")
    hunt = {i: tagged_hunt(c, records[i]["set"] if i in records else seeds[i]["set"], manifest) for i, c in hunt.items()}
    return {"seeds": seeds, "blind": blind, "audit": audit, "hunt": hunt, "compare": compare, "final": final,
            "in_scope": in_scope,
            "runs": {args.blind_group: blind_run, args.audit_group: audit_run, args.hunt_group: hunt_run,
                     f"{args.label}_stage4": compare_run, f"{args.label}_stage5": final_run},
            "gaps": blind_gaps + audit_gaps + hunt_gaps + compare_gaps + final_gaps}


def build_compare(args, stages: dict, records: dict) -> None:
    gold_ws = args.workspace_root / GOLD_WS / "compare"
    cases = []
    for case_id in stages["in_scope"]:
        if case_id not in stages["blind"]:
            continue
        gold = records[case_id]["gold"]
        cases.append({"id": case_id, "question": gold["question"], "required_facts": gold["required_facts"],
                      "reference_answer": gold["reference_answer"],
                      "answerability": {"status": gold["answerability"]["status"],
                                        "blind_equivalent": [k for k, v in BLIND_STATUS.items()
                                                             if v == gold["answerability"]["status"]][0]},
                      "source_files": gold["dependencies"]["required"] + gold["dependencies"]["alternatives"],
                      "blind_answer": stages["blind"][case_id]})
    batches = []
    for number, part in enumerate(chunks(cases, COMPARE_BATCH), 1):
        batch_id = f"{args.label}4-{number:02d}"
        path = gold_ws / "batches" / f"{batch_id}.json"
        write_json(path, {"batch_id": batch_id, "cases": part})
        batches.append({"batch_id": batch_id, "cases": [c["id"] for c in part],
                        "batch_file": str(path.relative_to(args.workspace_root))})
    write_json(gold_ws / f"{args.label}_batches.json", {"stage4_compare": batches})
    print(json.dumps({"compare_batches": len(batches), "cases": len(cases),
                      "batch_list": str(gold_ws / f"{args.label}_batches.json")}))


def build_escalations(args, stages: dict, records: dict) -> None:
    case_dir = args.workspace_root / GOLD_WS / "hunt" / "cases"
    batches = []
    for case_id in stages["in_scope"]:
        parts = {k: stages[k].get(case_id) for k in ("blind", "audit", "hunt", "compare")}
        reasons = escalation_reasons(records[case_id], **parts)
        if not reasons:
            continue
        path = case_dir / f"{args.label}5-{case_id}.json"
        write_json(path, {**records[case_id]["gold"], "stage0": records[case_id]["stage0"],
                          "blind_answer": parts["blind"], "audit": parts["audit"], "hunt": parts["hunt"],
                          "compare": parts["compare"], "escalation_reasons": reasons})
        batches.append({"batch_id": f"{args.label}5-{case_id}", "cases": [case_id],
                        "batch_file": str(path.relative_to(args.workspace_root))})
    batch_list = case_dir / f"{args.label}_batches.json"
    write_json(batch_list, {"stage5_adjudicate": batches})
    print(json.dumps({"escalated": [b["cases"][0] for b in batches], "of": len(stages["in_scope"]),
                      "batch_list": str(batch_list)}))


def seed_calibration(stages: dict) -> dict:
    rows = []
    for seed_id, expected in stages["seeds"].items():
        audit, hunt = stages["audit"].get(seed_id), stages["hunt"].get(seed_id)
        row = {"seed": seed_id, "set": expected["set"], "defect": expected["defect"]}
        if expected["audit"]:
            row["audit_verdict"] = audit["verdict"] if audit else "unreviewed"
            row["audit_detected"] = bool(audit) and audit["verdict"] not in ("valid", "valid_minor")
            row["audit_verdict_as_expected"] = bool(audit) and audit["verdict"] in expected["audit"]
        if "hunt" in expected:
            wanted = expected["hunt"]
            hits = [f for f in (hunt or {}).get("findings", []) if f["type"] == wanted["type"] and f["strength"] != "weak"
                    and (wanted["file"] is None or Path(f["file"]).name == wanted["file"])]
            row["hunt_detected"] = bool(hits)
            row["hunt_findings"] = [f"{f['type']} {f['strength']} {f['file']}" for f in (hunt or {}).get("findings", [])]
        rows.append(row)
    audit_rows = [r for r in rows if "audit_detected" in r]
    hunt_rows = [r for r in rows if "hunt_detected" in r]
    return {"audit_detected": f"{sum(r['audit_detected'] for r in audit_rows)}/{len(audit_rows)}",
            "hunt_detected": f"{sum(r['hunt_detected'] for r in hunt_rows)}/{len(hunt_rows)}", "seeds": rows}


def build_findings(args, stages: dict, records: dict) -> None:
    cases = []
    for case_id in stages["in_scope"]:
        parts = {k: stages[k].get(case_id) for k in ("blind", "audit", "hunt", "compare")}
        final = stages["final"].get(case_id)
        reasons = escalation_reasons(records[case_id], **parts)
        missing = [k for k in ("blind", "audit", "hunt", "compare") if parts[k] is None]
        if final:
            verdict, severity = final["verdict"], final["severity"]
        elif reasons:
            verdict, severity = "pending_adjudication", None
        elif missing:
            verdict, severity = "unreviewed", None
        elif parts["audit"]["verdict"] == "valid_minor":
            verdict, severity = "valid_minor", "non_blocking"
        else:
            verdict, severity = "valid", "none"
        hunt = parts["hunt"] or {"findings": [], "stable": None}
        cases.append({
            "set": records[case_id]["set"], "id": case_id, "category": records[case_id]["gold"]["category"],
            "verdict": verdict, "severity": severity, "stages_missing": missing,
            "stage0": records[case_id]["stage0"]["status"],
            "blind": parts["blind"] and {"answerability": parts["blind"]["answerability"],
                                         "confidence": parts["blind"]["confidence"],
                                         "ambiguity": parts["blind"]["ambiguity"]},
            "compare": parts["compare"] and {"answerability_agrees": parts["compare"]["answerability_agrees"],
                                             "facts": {f["fact_id"]: f["result"] for f in parts["compare"]["facts"]},
                                             "different_source": parts["compare"]["different_source"],
                                             "ambiguity_changes_answer": parts["compare"]["ambiguity_changes_answer"]},
            "audit": parts["audit"] and {"verdict": parts["audit"]["verdict"], "severity": parts["audit"]["severity"],
                                         "summary": parts["audit"]["summary"],
                                         "cannot_tell": [c["check"] for c in parts["audit"]["checks"] if c["result"] == "cannot_tell"],
                                         "failed_checks": [c["check"] for c in parts["audit"]["checks"] if c["result"] == "fail"],
                                         "proposed_correction": parts["audit"]["proposed_correction"]},
            "hunt": {"stable": hunt["stable"],
                     "findings": [{k: f.get(k) for k in ("type", "strength", "file", "condition", "quote_verified", "explanation")}
                                  for f in hunt["findings"]]},
            "escalation_reasons": reasons,
            "adjudication": final,
        })
    verdicts = {}
    for case in cases:
        verdicts[case["verdict"]] = verdicts.get(case["verdict"], 0) + 1
    result = {"label": args.label, "cases_in_scope": len(cases), "verdicts": verdicts,
              "escalated": sum(1 for c in cases if c["escalation_reasons"]),
              "coverage_gaps": stages["gaps"], "runs": stages["runs"],
              "calibration": seed_calibration(stages) if stages["seeds"] else None, "cases": cases}
    out = HERE / "results" / f"{args.label}_findings.json"
    write_json(out, result)
    print(json.dumps({k: result[k] for k in ("cases_in_scope", "verdicts", "escalated")}
                     | {"calibration": result["calibration"] and {k: result["calibration"][k] for k in ("audit_detected", "hunt_detected")},
                        "gaps": len(stages["gaps"]), "written": str(out.relative_to(ROOT))}, indent=1))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("step", choices=["compare", "escalate", "findings"])
    parser.add_argument("--label", required=True, help="Run label, e.g. pilot or full; names Stage 4/5 groups")
    parser.add_argument("--blind-group", required=True)
    parser.add_argument("--audit-group", required=True)
    parser.add_argument("--hunt-group", required=True)
    parser.add_argument("--seed-key", type=Path, help="seed_key.json of the calibration seeds, if any were mixed in")
    parser.add_argument("--corpus-dir", type=Path, required=True)
    parser.add_argument("--workspace-root", type=Path, required=True)
    args = parser.parse_args()
    args.workspace_root = args.workspace_root.resolve()
    manifest = load(HERE / "manifest.json")
    records = gold_records(args.corpus_dir)
    stages = load_stages(args, manifest, records)
    {"compare": build_compare, "escalate": build_escalations, "findings": build_findings}[args.step](args, stages, records)


if __name__ == "__main__":
    main()
