"""Stage 0 of the JUA-106 gold validation plan: mechanical checks, no models.

Reads the five reviewed query sets and the extracted article text, and writes
one record per case. Nothing under benchmark/<topic>/ or the corpus is changed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent

SETS = {
    "cardiology": "benchmark/cardiology/v1/queries.json",
    "diabetes": "benchmark/diabetes/v1/queries.json",
    "oncology": "benchmark/oncology/v1/queries.json",
    "outliers": "benchmark/outliers/v1/queries.json",
    "als-ftd": "benchmark/als-ftd/v1/queries.json",
}
# Snapshot the combined release scores against; questions and anchors must match.
EVALUATED = {"diabetes": "benchmark/diabetes/v1/runs/evaluated-release/queries.json"}
EXPECTED_STATUS = {"unanswerable": "absent_fact", "false_premise": "false_premise"}
# Standalone figures only: digits inside names such as CHA2DS2 or T2DM are not answers.
NUMBER = re.compile(r"(?<![A-Za-z0-9.,-])\d+(?:[.,]\d+)*(?![A-Za-z0-9])")
WORD = re.compile(r"[a-z0-9]+")
STOP = set("a an and are as at by did do does for from how in is it its of on or "
           "that the their this to was were what which who with".split())
DUPLICATE_JACCARD = 0.6


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def dependencies(query: dict) -> dict:
    """Normalise the two dependency spellings used across releases."""
    dep = query["dependencies"]
    return {
        "required": dep.get("required", dep.get("required_articles", [])),
        "alternatives": dep.get("alternatives", dep.get("alternative_articles", [])),
        "decoys": dep.get("decoys", dep.get("decoy_articles", [])),
    }


def fact_key(query_id: str, fact_id: str) -> str:
    return fact_id.split(":")[-1] if fact_id.startswith(f"{query_id}:") else fact_id


def tokens(text: str) -> set[str]:
    return {w for w in WORD.findall(text.lower()) if w not in STOP}


def check_anchor(anchor: dict, texts: dict, inventory: dict) -> list[str]:
    problems = []
    stem = Path(anchor["filename"]).stem
    raw = texts.get(stem)
    if raw is None:
        return [f"anchor {anchor['id']}: no extracted text for {anchor['filename']}"]
    text = raw.decode("utf-8")
    if text[anchor["text_start"]:anchor["text_end"]] != anchor["excerpt"]:
        problems.append(f"anchor {anchor['id']}: excerpt differs from text at recorded offsets")
    if sha256(anchor["excerpt"].encode("utf-8")) != anchor["excerpt_sha256"]:
        problems.append(f"anchor {anchor['id']}: excerpt_sha256 mismatch")
    if sha256(raw) != anchor["text_sha256"]:
        problems.append(f"anchor {anchor['id']}: text_sha256 differs from corpus file")
    entry = inventory.get(anchor["article_id"])
    if entry is None:
        problems.append(f"anchor {anchor['id']}: {anchor['article_id']} not in corpus inventory")
    else:
        if Path(entry["txt"]["path"]).stem != stem:
            problems.append(f"anchor {anchor['id']}: filename does not belong to {anchor['article_id']}")
        if entry["pdf"]["sha256"] != anchor["pdf_sha256"]:
            problems.append(f"anchor {anchor['id']}: pdf_sha256 differs from inventory")
    return problems


def check_case(query: dict, anchors: dict, condition_c2: set[str]) -> tuple[list[str], list[str]]:
    failures, warnings = [], []
    qid, category = query["id"], query["category"]
    dep = dependencies(query)
    facts = [fact_key(qid, f["id"]) for f in query["required_facts"]]
    status = query["answerability"]["status"]
    if status != EXPECTED_STATUS.get(category, "answerable"):
        failures.append(f"answerability {status!r} does not fit category {category}")

    source_articles = set()
    for evidence_set in query["evidence_sets"]:
        label = evidence_set["id"]
        missing = [a for a in evidence_set["anchors"] if a not in anchors]
        if missing:
            failures.append(f"set {label}: unknown anchors {missing}")
            continue
        mapped = {fact_key(qid, k): v for k, v in evidence_set["fact_anchors"].items()}
        for fact in facts:
            if not mapped.get(fact):
                failures.append(f"set {label}: fact {fact} has no anchor")
        for fact, ids in mapped.items():
            if fact not in facts:
                failures.append(f"set {label}: anchors mapped to undeclared fact {fact}")
            for anchor_id in ids:
                if anchor_id not in evidence_set["anchors"]:
                    failures.append(f"set {label}: fact anchor {anchor_id} not in set")
                    continue
                claimed = {fact_key(qid, f) for f in anchors[anchor_id].get("fact_ids", [])
                           if ":" not in f or f.startswith(f"{qid}:")}
                if fact not in claimed:
                    warnings.append(f"set {label}: anchor {anchor_id} does not list fact {fact}")
        unused = set(evidence_set["anchors"]) - {a for ids in mapped.values() for a in ids}
        if unused:
            warnings.append(f"set {label}: anchors bound to no fact {sorted(unused)}")
        articles = {anchors[a]["article_id"] for a in evidence_set["anchors"]}
        source_articles |= articles
        if category == "cross_doc_synthesis" and len(articles) < 2:
            failures.append(f"set {label}: synthesis evidence comes from one article")
        if category == "multi_hop":
            if len(evidence_set["anchors"]) < 2:
                failures.append(f"set {label}: multi-hop with fewer than two anchors")
            elif len(articles) > 1:
                warnings.append(f"set {label}: multi-hop anchors span {len(articles)} articles")

    declared = set(dep["required"]) | set(dep["alternatives"])
    if source_articles - declared:
        failures.append(f"anchor articles not declared as sources: {sorted(source_articles - declared)}")
    if declared - source_articles:
        failures.append(f"declared sources without anchors: {sorted(declared - source_articles)}")

    if status == "answerable" and not (facts and query["evidence_sets"]):
        failures.append("answerable case without facts or evidence sets")
    if category == "unanswerable":
        if query["evidence_sets"] or facts:
            failures.append("unanswerable case carries facts or evidence sets")
        scope = query["answerability"].get("search_scope")
        if not scope:
            failures.append("unanswerable case has no recorded search scope")
        elif not isinstance(scope, dict):
            warnings.append("search scope is free text, without searched terms or article list")
        elif not (scope.get("searched_terms") and scope.get("article_ids")):
            warnings.append("search scope lacks searched terms or article list")
    if category == "false_premise":
        if not query["answerability"].get("offending_premise"):
            warnings.append("false premise without a recorded offending premise")
        if not query["evidence_sets"]:
            failures.append("false premise without correction evidence")
    if category == "cross_doc_synthesis" and len(dep["required"]) < 2 and not dep["alternatives"]:
        failures.append("synthesis with fewer than two required articles")
    if category == "cross_doc_distractor":
        if not query["related_distractors"] or not dep["decoys"]:
            failures.append("distractor case without a named decoy")
        if set(dep["decoys"]) & declared:
            failures.append(f"decoy is also an answer source: {sorted(set(dep['decoys']) & declared)}")
        if set(dep["decoys"]) - condition_c2:
            failures.append(f"decoy outside C2: {sorted(set(dep['decoys']) - condition_c2)}")
    elif query["related_distractors"]:
        warnings.append("named distractor outside the distractor category")
    for distractor in query["related_distractors"]:
        anchor_id = distractor.get("anchor_id")
        if anchor_id and anchor_id not in anchors:
            failures.append(f"distractor anchor {anchor_id} unknown")
        elif anchor_id and anchors[anchor_id]["article_id"] != distractor["article_id"]:
            failures.append(f"distractor anchor {anchor_id} is not in {distractor['article_id']}")
        if distractor["article_id"] not in dep["decoys"]:
            warnings.append(f"distractor {distractor['article_id']} missing from dependency decoys")

    expected = " ".join(f.get("expected_text") or f.get("expected") or "" for f in query["required_facts"])
    expected = f"{expected} {query['reference_answer']}"
    leaked = sorted(set(NUMBER.findall(query["question"])) & set(NUMBER.findall(expected)))
    if leaked:
        warnings.append(f"numbers shared by question and expected answer: {leaked}")
    return failures, warnings


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus-dir", type=Path, default=ROOT / "corpus" / "JUA-106",
                        help="Directory holding the topic folders of extracted .txt files")
    parser.add_argument("--output", type=Path, default=HERE / "results" / "stage0.json")
    args = parser.parse_args()

    texts = {p.stem: p.read_bytes() for p in sorted(args.corpus_dir.glob("*/*.txt"))}
    inventory = {a["pmcid"]: a for a in load(args.corpus_dir / "inventory.json")["articles"]}
    cases, questions, set_summaries = [], [], {}
    for name, relative in SETS.items():
        benchmark = load(ROOT / relative)
        anchors = {a["id"]: a for a in benchmark["anchors"]}
        conditions = load(ROOT / Path(relative).parent / "conditions.json")["conditions"]
        c2 = set(conditions["C2"]["article_ids"])
        anchor_problems = {a["id"]: check_anchor(a, texts, inventory) for a in benchmark["anchors"]}
        set_notes = []
        if name in EVALUATED:
            evaluated = load(ROOT / EVALUATED[name])
            same = ([q["question"] for q in evaluated["queries"]] == [q["question"] for q in benchmark["queries"]]
                    and evaluated["anchors"] == benchmark["anchors"])
            set_notes.append("questions and anchors identical to evaluated snapshot" if same
                             else "QUESTIONS OR ANCHORS DIFFER from evaluated snapshot")
        for query in benchmark["queries"]:
            failures, warnings = check_case(query, anchors, c2)
            used = {a for s in query["evidence_sets"] for a in s["anchors"]}
            used |= {d["anchor_id"] for d in query["related_distractors"] if d.get("anchor_id")}
            for anchor_id in sorted(used):
                failures.extend(anchor_problems.get(anchor_id, []))
            cases.append({"set": name, "id": query["id"], "revision": query["revision"],
                          "category": query["category"], "failures": failures, "warnings": warnings})
            questions.append((name, query["id"], tokens(query["question"])))
        set_summaries[name] = {
            "queries_file": relative, "queries_sha256": sha256((ROOT / relative).read_bytes()),
            "cases": len(benchmark["queries"]), "anchors": len(anchors),
            "anchors_failing": sum(1 for p in anchor_problems.values() if p), "notes": set_notes,
        }

    by_key = {(c["set"], c["id"]): c for c in cases}
    for i, (set_a, id_a, tok_a) in enumerate(questions):
        for set_b, id_b, tok_b in questions[i + 1:]:
            score = len(tok_a & tok_b) / len(tok_a | tok_b)
            if score >= DUPLICATE_JACCARD:
                by_key[(set_a, id_a)]["warnings"].append(f"question overlaps {set_b}/{id_b} (Jaccard {score:.2f})")
                by_key[(set_b, id_b)]["warnings"].append(f"question overlaps {set_a}/{id_a} (Jaccard {score:.2f})")

    for case in cases:
        case["status"] = "fail" if case["failures"] else "warn" if case["warnings"] else "pass"
    result = {
        "stage": 0, "method": "mechanical checks; no model calls",
        "corpus_text_files": len(texts), "sets": set_summaries,
        "totals": {s: sum(1 for c in cases if c["status"] == s) for s in ("pass", "warn", "fail")},
        "cases": cases,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"totals": result["totals"], "sets": set_summaries}, indent=2))
    for case in cases:
        for kind in ("failures", "warnings"):
            for message in case[kind]:
                print(f"{kind[:-1].upper():8} {case['set']}/{case['id']} [{case['category']}] {message}")


if __name__ == "__main__":
    main()
