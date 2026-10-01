"""Versioned document and conservative pinned-excerpt retrieval metrics.

This does not judge generated answers or prove that a paraphrase lacks evidence.
Gold text never enters retrieval inputs. No models or network are needed here.
"""
import hashlib
import json
import unicodedata

SCORER_VERSION = "pinned-excerpt-coverage-v1"
CATEGORIES = {"direct_lookup", "multi_hop", "cross_doc_distractor",
              "cross_doc_synthesis", "unanswerable", "false_premise"}


def canonical_hash(value) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"),
                         ensure_ascii=False, allow_nan=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def normalize_excerpt(text: str) -> str:
    """Normalize typography/whitespace, retaining signs, numbers and qualifiers."""
    return " ".join(unicodedata.normalize("NFKC", text).split())


def validate_benchmark(benchmark: dict) -> None:
    queries = benchmark["queries"]
    if not queries or len({q["id"] for q in queries}) != len(queries):
        raise ValueError("empty benchmark or duplicate query IDs")
    anchors = benchmark["anchors"]
    if len({a["id"] for a in anchors}) != len(anchors):
        raise ValueError("duplicate anchor IDs")
    by_id = {a["id"]: a for a in anchors}
    for anchor in anchors:
        if not anchor["excerpt"].strip() or not anchor["filename"]:
            raise ValueError(f"{anchor['id']}: empty evidence or source")
    for query in queries:
        qid = query["id"]
        if not qid or not query["question"].strip():
            raise ValueError("empty query ID or question")
        category = query["category"]
        if category not in CATEGORIES or type(query["revision"]) is not int or query["revision"] < 1:
            raise ValueError(f"{qid}: invalid category/revision")
        facts = query["required_facts"]
        fact_ids = {f["id"] for f in facts}
        if len(fact_ids) != len(facts):
            raise ValueError(f"{qid}: duplicate required facts")
        sets = query["evidence_sets"]
        absent = query["answerability"]["status"] == "absent_fact"
        if absent:
            if category != "unanswerable" or facts or sets or not query["answerability"].get("search_scope"):
                raise ValueError(f"{qid}: absent-fact case needs explicit search scope and no invented evidence")
            continue
        status = query["answerability"]["status"]
        if status not in {"answerable", "false_premise"} or (category == "false_premise") != (status == "false_premise"):
            raise ValueError(f"{qid}: inconsistent answerability")
        if not facts or not sets:
            raise ValueError(f"{qid}: missing facts or complete evidence sets")
        for evidence_set in sets:
            members = evidence_set["anchors"]
            if not members or len(set(members)) != len(members) or not set(members) <= by_id.keys():
                raise ValueError(f"{qid}: empty, duplicate or unknown evidence anchor")
            mapping = evidence_set["fact_anchors"]
            if set(mapping) != fact_ids or any(not ids or not set(ids) <= set(members) for ids in mapping.values()):
                raise ValueError(f"{qid}: complete set does not cover each required fact")
            if set(members) != {aid for ids in mapping.values() for aid in ids}:
                raise ValueError(f"{qid}: unbound evidence anchor")
            docs = {by_id[aid]["article_id"] for aid in members}
            if category == "cross_doc_synthesis" and len(docs) < 2:
                raise ValueError(f"{qid}: synthesis needs multiple articles in every alternative")
            if category == "multi_hop" and (len(members) < 2 or len(docs) != 1 or not query.get("reasoning")):
                raise ValueError(f"{qid}: multi-hop needs separated same-article evidence and rationale")
            if category == "multi_hop" and not any(
                by_id[a]["text_end"] <= by_id[b]["text_start"] or
                by_id[b]["text_end"] <= by_id[a]["text_start"]
                for a in members for b in members if a != b
            ):
                raise ValueError(f"{qid}: multi-hop anchors all overlap")
        decoys = query["related_distractors"]
        if category == "cross_doc_distractor" and not decoys:
            raise ValueError(f"{qid}: distractor case has no competitor")
        accepted_docs = {by_id[aid]["filename"] for s in sets for aid in s["anchors"]}
        for decoy in decoys:
            anchor = by_id.get(decoy.get("anchor_id"))
            if (not decoy["reason_inapplicable"] or not decoy["plausible_confusion"] or
                    decoy["filename"] in accepted_docs or not anchor or
                    (anchor["filename"], anchor["article_id"]) != (decoy["filename"], decoy["article_id"])):
                raise ValueError(f"{qid}: decoy lacks scope rationale or is accepted evidence")


def score_evidence(contexts: list[str], sources: list[str], query: dict,
                   anchors: dict[str, dict]) -> dict:
    """OR across complete alternatives; AND across their anchors and facts.

    Match each excerpt inside one source-bound chunk. Never match naked numbers,
    combine different documents, or concatenate chunks into fabricated passages.
    """
    if len(contexts) != len(sources):
        raise ValueError("chunk/source counts differ")
    if query["answerability"]["status"] == "absent_fact":
        return {"document_coverage": "not_scored", "evidence_coverage": "not_scored",
                "fact_recall": None, "supported_facts": [], "anchor_matches": {},
                "distractor_ordering": "not_scored", "present_distractors": []}
    sets = query["evidence_sets"]
    used = {aid for s in sets for aid in s["anchors"]}
    normalized = [normalize_excerpt(c) for c in contexts]
    matches = {}
    for aid in sorted(used):
        anchor = anchors[aid]
        excerpt = normalize_excerpt(anchor["excerpt"])
        matches[aid] = [i for i, (chunk, source) in enumerate(zip(normalized, sources))
                        if source == anchor["filename"] and excerpt in chunk]
    supported = set()
    document_sets = []
    for evidence_set in sets:
        for fact, ids in evidence_set["fact_anchors"].items():
            if all(matches[aid] for aid in ids):
                supported.add(fact)
        document_sets.append({anchors[aid]["filename"] for aid in evidence_set["anchors"]})
    complete = any(all(matches[aid] for aid in s["anchors"]) for s in sets)
    docs_present = any(docs <= set(sources) for docs in document_sets)
    present_decoys = [d["filename"] for d in query["related_distractors"] if d["filename"] in sources]
    ordering = "not_scored"
    if query["category"] == "cross_doc_distractor":
        ordering_ok = any(docs <= set(sources) and all(
            max(sources.index(doc) for doc in docs) < sources.index(decoy)
            for decoy in present_decoys) for docs in document_sets)
        ordering = "pass" if ordering_ok else "fail"
    return {"document_coverage": "pass" if docs_present else "fail",
            "evidence_coverage": "pass" if complete else "fail",
            "fact_recall": len(supported) / len(query["required_facts"]),
            "supported_facts": sorted(supported), "anchor_matches": matches,
            "distractor_ordering": ordering, "present_distractors": present_decoys}
