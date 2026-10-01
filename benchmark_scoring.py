"""Versioned document and conservative pinned-excerpt retrieval metrics.

This does not judge generated answers or prove that a paraphrase lacks evidence.
Gold text never enters retrieval inputs. No models or network are needed here.
"""
import hashlib
import json
import unicodedata
from collections import Counter

SCORER_VERSION = "pinned-span-coverage-v3"
FEASIBILITY_VERSION = "minimum-evidence-chunks-v1"
CATEGORIES = {"direct_lookup", "multi_hop", "cross_doc_distractor",
              "cross_doc_synthesis", "unanswerable", "false_premise"}


def canonical_hash(value) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"),
                         ensure_ascii=False, allow_nan=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def normalize_excerpt(text: str) -> str:
    """Normalize typography/whitespace, retaining signs, numbers and qualifiers."""
    return " ".join(unicodedata.normalize("NFKC", text).split())


def validate_answerability(category: str, status: str) -> None:
    expected = {"unanswerable": "absent_fact", "false_premise": "false_premise"}.get(category, "answerable")
    if category not in CATEGORIES or status != expected:
        raise ValueError(f"{category}: inconsistent answerability {status!r}; expected {expected!r}")


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
        validate_answerability(category, query["answerability"]["status"])
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


def compile_anchor_spans(anchors: dict[str, dict], source_text: dict[str, str], chunker) -> dict:
    """Certify contiguous production chunk windows against pinned source offsets.

    Retrieval order is irrelevant to source adjacency. Each plan retains the
    physical chunk indices and whole normalized chunks needed for this span.
    No retrieved fragments are stitched together to infer source continuity.
    """
    indexed = {}
    for source, text in source_text.items():
        full = normalize_excerpt(text)
        chunks = [normalize_excerpt(c) for c in chunker(text)]
        occurrences = []
        for chunk in chunks:
            if not chunk:
                raise ValueError(f"{source}: empty production chunk")
            positions = []
            start = full.find(chunk)
            while start >= 0:
                positions.append((start, start + len(chunk)))
                start = full.find(chunk, start + 1)
            if not positions:
                raise ValueError(f"{source}: production chunk is not a source substring")
            occurrences.append(positions)
        indexed[source] = (full, chunks, occurrences)
    plans = {}
    for aid, anchor in anchors.items():
        source = anchor["filename"]
        text = source_text[source]
        raw_start, raw_end = anchor["text_start"], anchor["text_end"]
        if not 0 <= raw_start < raw_end <= len(text) or text[raw_start:raw_end] != anchor["excerpt"]:
            raise ValueError(f"{aid}: pinned source offset/excerpt mismatch")
        full, chunks, occurrences = indexed[source]
        excerpt = normalize_excerpt(anchor["excerpt"])
        start = len(normalize_excerpt(text[:raw_start]))
        # Prefix normalization trims a separator immediately before the span.
        if full[start:start + 1] == " ":
            start += 1
        end = start + len(excerpt)
        if not excerpt or full[start:end] != excerpt:
            raise ValueError(f"{aid}: normalized source offset/excerpt mismatch")
        windows = set()
        for first, positions in enumerate(occurrences):
            states = {(left, right) for left, right in positions if left <= start < right}
            for last in range(first, len(chunks)):
                if not states:
                    break
                if any(right >= end for _, right in states):
                    windows.add((first, last + 1))
                    break  # Longer windows add no evidence for this span.
                if last + 1 < len(chunks):
                    states = {(left, right) for left, right in occurrences[last + 1]
                              if any(left >= previous_left and right > covered and
                                     (left <= covered or not full[covered:left].strip())
                                     for previous_left, covered in states)}
        if not windows:
            raise ValueError(f"{aid}: pinned span is unreachable under production chunking")
        plans[aid] = [{"chunk_indices": list(range(first, stop)), "chunks": chunks[first:stop]}
                      for first, stop in sorted(windows)]
    return plans


def minimum_evidence_witness(query: dict, anchors: dict, span_plans: dict,
                             source_chunks: dict) -> Counter | None:
    """Smallest retrieved chunk multiset that passes one complete alternative.

    Whole normalized chunks are identified by source and content, just as in
    scoring. Counts preserve duplicate multiplicity within an anchor; different
    anchors can share retrieved chunks. Dominated partial requirements can be
    discarded because merging another anchor cannot make them cheaper.
    """
    if query["answerability"]["status"] == "absent_fact":
        return None
    options = {}
    for aid in {aid for s in query["evidence_sets"] for aid in s["anchors"]}:
        anchor = anchors[aid]
        source = anchor["filename"]
        excerpt = normalize_excerpt(anchor["excerpt"])
        chunks = [normalize_excerpt(c) for c in source_chunks.get(source, [])]
        available = Counter((source, chunk) for chunk in chunks)
        choices = [Counter({(source, chunk): 1}) for chunk in chunks if excerpt in chunk]
        choices += [Counter((source, chunk) for chunk in plan["chunks"])
                    for plan in span_plans.get(aid, []) if len(plan["chunks"]) > 1]
        options[aid] = [choice for choice in choices if choice <= available]
    witnesses = []
    for evidence_set in query["evidence_sets"]:
        states = [Counter()]
        for aid in evidence_set["anchors"]:
            merged = []
            for state in states:
                for choice in options[aid]:
                    candidate = state | choice  # Share chunks, retaining required multiplicity.
                    if not any(other <= candidate for other in merged):
                        merged = [other for other in merged if not candidate <= other]
                        merged.append(candidate)
            states = merged
        witnesses.extend(states)
    if not witnesses:
        raise ValueError(f"{query['id']}: no complete evidence alternative is reachable")
    return min(witnesses, key=lambda witness: witness.total())


def feasibility_from_minimum(minimum: int | None, depths=(3, 8)) -> dict:
    return {"minimum_chunks": minimum, "by_depth": {
        f"n{depth}": "not_scored" if minimum is None else "feasible" if minimum <= depth else "infeasible"
        for depth in depths}}


def compile_query_feasibility(queries: list[dict], anchors: dict, span_plans: dict,
                              source_chunks: dict, depths=(3, 8)) -> dict:
    result = {}
    for query in queries:
        witness = minimum_evidence_witness(query, anchors, span_plans, source_chunks)
        result[query["id"]] = feasibility_from_minimum(None if witness is None else witness.total(), depths)
    return result


def evidence_coverage_report(results: list[dict], depth: int) -> dict:
    """Retain the full-set denominator and explicitly expose depth eligibility."""
    scored = [r for r in results if r["answerability"] != "absent_fact"]
    feasible = [r for r in scored if r["evidence_feasibility"]["by_depth"][f"n{depth}"] == "feasible"]
    def coverage(entries):
        passed = sum(r[f"n{depth}"]["metrics"]["evidence_coverage"] == "pass" for r in entries)
        return {"pass": passed, "total": len(entries), "rate": passed / len(entries) if entries else None}
    return {"full_set": coverage(scored), "feasible_only": coverage(feasible),
            "structural_ceiling": {"pass": len(feasible), "total": len(scored),
                                   "rate": len(feasible) / len(scored) if scored else None},
            "infeasible_ids": sorted(r["id"] for r in scored
                                     if r["evidence_feasibility"]["by_depth"][f"n{depth}"] == "infeasible")}


def score_evidence(contexts: list[str], sources: list[str], query: dict,
                   anchors: dict[str, dict], span_plans: dict | None = None) -> dict:
    """OR across complete alternatives; AND across their anchors and facts.

    Match a source-bound excerpt or every whole chunk in a certified adjacent
    span. Without pinned-source plans, only single-chunk matching is allowed.
    """
    if len(contexts) != len(sources):
        raise ValueError("chunk/source counts differ")
    if query["answerability"]["status"] == "absent_fact":
        return {"document_coverage": "not_scored", "evidence_coverage": "not_scored",
                "fact_recall": None, "supported_facts": [], "anchor_matches": {}, "anchor_match_groups": {},
                "distractor_ordering": "not_scored", "present_distractors": []}
    sets = query["evidence_sets"]
    used = {aid for s in sets for aid in s["anchors"]}
    normalized = [normalize_excerpt(c) for c in contexts]
    matches = {}
    groups = {}
    for aid in sorted(used):
        anchor = anchors[aid]
        excerpt = normalize_excerpt(anchor["excerpt"])
        groups[aid] = [[i] for i, (chunk, source) in enumerate(zip(normalized, sources))
                       if source == anchor["filename"] and excerpt in chunk]
        for plan in (span_plans or {}).get(aid, []):
            if len(plan["chunks"]) < 2:
                continue
            indices = []
            for expected in plan["chunks"]:
                index = next((i for i, (chunk, source) in enumerate(zip(normalized, sources))
                              if i not in indices and source == anchor["filename"] and chunk == expected), None)
                if index is None:
                    break
                indices.append(index)
            if len(indices) == len(plan["chunks"]) and indices not in groups[aid]:
                groups[aid].append(indices)
        # Only indices belonging to a complete support group are reported.
        matches[aid] = sorted({i for group in groups[aid] for i in group})
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
            "supported_facts": sorted(supported), "anchor_matches": matches, "anchor_match_groups": groups,
            "distractor_ordering": ordering, "present_distractors": present_decoys}
