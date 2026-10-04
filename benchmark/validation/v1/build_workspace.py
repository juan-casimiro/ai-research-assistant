"""Build the review workspaces and batch manifest for the JUA-106 gold validation.

Two disposable workspaces are written outside the repository: one for blind
answering (article text and questions only) and one for the gold-aware stages.
The manifest written beside this script holds assignments only, never gold.
No model is called.
"""
from __future__ import annotations

import argparse
import json
import random
import shutil
from pathlib import Path

from stage0 import HERE, ROOT, SETS, dependencies, load, sha256

SEED = 106
BLIND_WS, GOLD_WS = "jua-106-blind-ws", "jua-106-gold-ws"
BATCH_SIZE = {"stage1_blind": 6, "stage2_audit": 6, "stage3_hunt": 8}
CATEGORIES = ("direct_lookup", "multi_hop", "cross_doc_synthesis",
              "cross_doc_distractor", "false_premise", "unanswerable")
DOUBLE_COVERAGE = {"cross_doc_synthesis": 5, "cross_doc_distractor": 5, "false_premise": 5}
RUNNERS = {
    "stage1_blind": {"cli": "claude", "model": "claude-sonnet-5-5", "workspace": BLIND_WS},
    "stage1_double": {"cli": "codex", "model": "gpt-6.1-sol", "reasoning_effort": "medium", "workspace": BLIND_WS},
    "stage2_audit": {"cli": "claude", "model": "claude-sonnet-5-5", "workspace": GOLD_WS},
    "stage3_hunt": {"cli": "codex", "model": "gpt-6.1-sol", "reasoning_effort": "medium", "workspace": GOLD_WS},
    "stage4_compare": {"cli": "claude", "model": "claude-sonnet-5-5", "workspace": GOLD_WS},
    "stage5_adjudicate": {"cli": "claude", "model": "claude-opus-5-5", "workspace": GOLD_WS},
}


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def copy_articles(files: list[str], corpus: Path, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    for relative in files:
        shutil.copyfile(corpus / relative, destination / Path(relative).name)


def chunks(items: list, size: int) -> list[list]:
    return [items[i:i + size] for i in range(0, len(items), size)]


def audit_record(query: dict, anchors: dict, name_of: dict, warnings: list[str]) -> dict:
    dep = dependencies(query)
    used = [a for s in query["evidence_sets"] for a in s["anchors"]]
    used += [d["anchor_id"] for d in query["related_distractors"] if d.get("anchor_id")]
    answerability = dict(query["answerability"])
    scope = answerability.get("search_scope")
    if isinstance(scope, dict) and "article_ids" in scope:
        answerability["search_scope"] = {**scope, "files": [name_of[a] for a in scope["article_ids"]]}
        del answerability["search_scope"]["article_ids"]
    return {
        "id": query["id"], "category": query["category"], "question": query["question"],
        "required_facts": query["required_facts"], "evidence_sets": query["evidence_sets"],
        "anchors": [{k: anchors[a].get(k) for k in ("id", "filename", "section", "text_start",
                                                    "text_end", "excerpt", "fact_ids", "role")}
                    | {"file": Path(anchors[a]["filename"]).stem + ".txt"}
                    for a in dict.fromkeys(used)],
        "reference_answer": query["reference_answer"], "answer_rubric": query["answer_rubric"],
        "answerability": answerability,
        "distractors": [{**d, "file": name_of[d["article_id"]]} for d in query["related_distractors"]],
        "dependencies": {k: [name_of[a] for a in v] for k, v in dep.items()},
        "stage0_warnings": warnings,
    }


def hunt_record(query: dict, name_of: dict) -> dict:
    dep = dependencies(query)
    answerability = {k: v for k, v in query["answerability"].items()
                     if k in ("status", "offending_premise", "missing_fact")}
    return {
        "id": query["id"], "category": query["category"], "question": query["question"],
        "required_facts": query["required_facts"], "reference_answer": query["reference_answer"],
        "answerability": answerability,
        "source_files": [name_of[a] for a in dep["required"] + dep["alternatives"]],
        "decoys": [{"file": name_of[d["article_id"]], "plausible_confusion": d["plausible_confusion"],
                    "reason_inapplicable": d["reason_inapplicable"]} for d in query["related_distractors"]],
    }


def pick_pilot(by_set: dict, rng: random.Random) -> list[tuple[str, str]]:
    """Two cases per category, rotating through the sets so each is represented."""
    names, picked, offset = list(by_set), [], 0
    for category in CATEGORIES:
        taken = 0
        for step in range(len(names)):
            name = names[(offset + step) % len(names)]
            pool = [q["id"] for q in by_set[name] if q["category"] == category]
            if pool and taken < 2:
                picked.append((name, rng.choice(sorted(pool))))
                taken += 1
        offset += 2
    return picked


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus-dir", type=Path, required=True,
                        help="Directory holding inventory.json and the topic folders of .txt files")
    parser.add_argument("--workspace-root", type=Path, required=True,
                        help="Directory outside the repository for the two disposable workspaces")
    args = parser.parse_args()
    root = args.workspace_root.resolve()
    if ROOT in root.parents or root == ROOT:
        raise SystemExit("workspace root must be outside the repository")
    stage0 = load(HERE / "results" / "stage0.json")
    if stage0["totals"]["fail"]:
        raise SystemExit("stage 0 has failures; resolve them before building batches")
    warnings = {(c["set"], c["id"]): c["warnings"] for c in stage0["cases"]}

    inventory = load(args.corpus_dir / "inventory.json")["articles"]
    path_of = {a["pmcid"]: a["txt"]["path"] for a in inventory}
    name_of = {pmcid: Path(p).name for pmcid, p in path_of.items()}
    rng = random.Random(SEED)
    blind, gold = root / BLIND_WS, root / GOLD_WS
    copy_articles(sorted(path_of.values()), args.corpus_dir, gold / "hunt" / "articles")

    by_set, records, manifest_sets = {}, {}, {}
    batches = {stage: [] for stage in BATCH_SIZE}
    for name, relative in SETS.items():
        benchmark = load(ROOT / relative)
        anchors = {a["id"]: a for a in benchmark["anchors"]}
        conditions = load(ROOT / Path(relative).parent / "conditions.json")["conditions"]
        files = sorted(path_of[a] for a in conditions["C2"]["article_ids"])
        copy_articles(files, args.corpus_dir, blind / name / "articles")
        copy_articles(files, args.corpus_dir, gold / "audit" / name / "articles")
        by_set[name] = benchmark["queries"]
        for query in benchmark["queries"]:
            key = (name, query["id"])
            records[key] = {
                "stage1_blind": {"id": query["id"], "question": query["question"]},
                "stage2_audit": audit_record(query, anchors, name_of, warnings[key]),
                "stage3_hunt": hunt_record(query, name_of),
            }
        manifest_sets[name] = {
            "queries_file": relative, "queries_sha256": sha256((ROOT / relative).read_bytes()),
            "cases": len(benchmark["queries"]), "articles": [Path(f).name for f in files],
            "conditions": {c: sorted(name_of[a] for a in v["article_ids"]) for c, v in conditions.items()},
        }
        for stage, size in BATCH_SIZE.items():
            order = [q["id"] for q in benchmark["queries"]]
            rng.shuffle(order)
            for number, ids in enumerate(chunks(order, size), 1):
                batches[stage].append({"batch_id": f"{stage.split('_')[0]}-{name}-{number:02d}",
                                       "set": name, "cases": ids})

    pilot = pick_pilot(by_set, rng)
    category = {(n, q["id"]): q["category"] for n, qs in by_set.items() for q in qs}
    double = []
    for wanted, count in DOUBLE_COVERAGE.items():
        pool = sorted(k for k, c in category.items() if c == wanted and k not in pilot)
        double += rng.sample(pool, count)

    def grouped(label: str, keys: list, size: int) -> list[dict]:
        out = []
        for name in SETS:
            ids = [i for n, i in keys if n == name]
            for number, part in enumerate(chunks(ids, size), 1):
                out.append({"batch_id": f"{label}-{name}-{number:02d}", "set": name, "cases": part})
        return out

    plan = {
        "stage1_blind": batches["stage1_blind"], "stage2_audit": batches["stage2_audit"],
        "stage3_hunt": batches["stage3_hunt"],
        "pilot_stage1_blind": grouped("pilot1", pilot, 6), "pilot_stage2_audit": grouped("pilot2", pilot, 6),
        "pilot_stage3_hunt": grouped("pilot3", pilot, 8),
        "stage1_double": grouped("double1", double, 6),
    }
    locations = {  # stage key -> (workspace directory relative to its set, record kind)
        "stage1_blind": (blind, "", "stage1_blind"), "pilot_stage1_blind": (blind, "", "stage1_blind"),
        "stage1_double": (blind, "", "stage1_blind"),
        "stage2_audit": (gold / "audit", "", "stage2_audit"), "pilot_stage2_audit": (gold / "audit", "", "stage2_audit"),
        "stage3_hunt": (gold / "hunt", None, "stage3_hunt"), "pilot_stage3_hunt": (gold / "hunt", None, "stage3_hunt"),
    }
    for stage, stage_batches in plan.items():
        base, per_set, kind = locations[stage]
        for batch in stage_batches:
            directory = base / "batches" if per_set is None else base / batch["set"] / "batches"
            body = [records[(batch["set"], i)][kind] for i in batch["cases"]]
            field = "questions" if kind == "stage1_blind" else "cases"
            write_json(directory / f"{batch['batch_id']}.json", {"batch_id": batch["batch_id"], field: body})
            batch["batch_file"] = str((directory / f"{batch['batch_id']}.json").relative_to(root))

    manifest = {
        "schema_version": "1.0", "seed": SEED, "stage0_totals": stage0["totals"],
        "workspaces": {"blind": BLIND_WS, "gold": GOLD_WS,
                       "note": "Relative to the workspace root given at build time; disposable and rebuilt from this manifest's inputs."},
        "runners": RUNNERS, "sets": manifest_sets,
        "briefs": {p.name: sha256(p.read_bytes()) for p in sorted((HERE / "briefs").glob("*.md"))},
        "schemas": {p.name: sha256(p.read_bytes()) for p in sorted((HERE / "schemas").glob("*.json"))},
        "pilot_cases": [{"set": n, "id": i, "category": category[(n, i)]} for n, i in pilot],
        "double_coverage_cases": [{"set": n, "id": i, "category": category[(n, i)]} for n, i in double],
        "batches": plan,
    }
    write_json(HERE / "manifest.json", manifest)
    print(json.dumps({k: len(v) for k, v in plan.items()}, indent=2))
    print("pilot:", ", ".join(f"{n}/{i} ({category[(n, i)]})" for n, i in pilot))


if __name__ == "__main__":
    main()
