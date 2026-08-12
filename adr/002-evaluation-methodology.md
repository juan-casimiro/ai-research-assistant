# ADR-002: Evaluation Methodology

## Context

ADR-001 covers chunking and retrieval architecture decisions. This
document covers how those decisions are *measured*: the golden QA
dataset's category design, and the scoring logic used to turn raw
retrieval results into pass/fail verdicts.

Splitting this out from ADR-001 is itself a decision worth recording:
architecture and evaluation methodology are separate concerns, and
conflating them made ADR-001 harder to navigate as both grew. This
document is referenced by ADR-001's evaluation sections and by the
README.

## Category design

The golden QA set (`golden_qa.json`) uses five categories, each
targeting a distinct retrieval failure mode. Four are scored by
`eval_golden.py`; `unanswerable` is logged but not scored.

### `direct_lookup`

A single fact from a single document.

*Example:* "How many RCTs and total participants were included in this
systematic review?" — one document, one passage.

*Failure mode caught:* the floor. If this category isn't near 100%,
something basic is broken (chunking, embedding, or ingestion) — not a
sophistication problem.

*Scoring:* `expected_doc` must appear in the retrieved sources.

### `multi_hop`

Connecting two related facts within the same document.

*Example:* "How do the primary change-score analysis results compare
with the post-treatment sensitivity analysis?" — both facts live in the
same paper, in different sections.

*Failure mode caught:* whether chunking and retrieval preserve enough
surrounding context to link related-but-separated passages, rather than
only ever surfacing one isolated fact.

*Scoring:* same as `direct_lookup` — `expected_doc` must appear in the
retrieved sources. **Known limitation:** the harness checks that the
source document was retrieved; it does not currently verify that both
specific facts were retrievable as separate chunks. A query could pass
this category by retrieving only the chunk containing one of the two
facts. Tightening this would require per-query chunk-level ground
truth rather than document-level, not currently captured in the
dataset schema.

### `cross_doc_distractor`

The correct document sits next to a topically similar decoy.

*Example:* A question about CHA2DS2-VA scores in a no-reflow/STEMI
study, with a distractor AFib-detection review that also discusses
CHA2DS2-VASc — same score family, different clinical question.

*Failure mode caught:* the hardest case for embeddings specifically —
semantic similarity conflates "same topic" with "right answer." This is
where reranking and hybrid search earn their keep, or don't.

*Scoring (non-trivial):* it is not enough for the expected document to
appear — it must be **ranked at or above the distractor**:

```python
if distractor and distractor in sources:
    if sources.index(expected) >= sources.index(distractor):
        return "fail"
```

This is deliberately stricter than presence-only scoring. A system that
retrieves the right document but ranks a near-miss above it would still
hand a user the wrong answer first — ranking order is what actually
matters here, not mere recall.

### `cross_doc_synthesis`

The answer requires two documents together.

*Example:* q117 — the tension between a treatment strategy's
demonstrated clinical benefit (shown in one real-world cohort study)
and real-world delivery barriers (discussed in a separate editorial).

*Failure mode caught:* whether the system can assemble a synthesis view
instead of defaulting to whichever single document scores highest — a
different skill than distractor rejection, since here *both* documents
are correct and needed, not one correct and one wrong.

*Scoring (non-trivial):* an **AND condition** across both expected
documents:

```python
expected_docs = query.get("expected_docs", [])
return "pass" if all(doc in sources for doc in expected_docs) else "fail"
```

There is no partial credit. Retrieving only one of the two documents,
however well-ranked, is a fail — a synthesis answer built from a single
source isn't a partial synthesis, it's a single-document answer wearing
a synthesis question's clothes.

### `unanswerable`

The question sounds answerable but isn't, given the corpus.

*Example:* q141 — asking for confirmed cholera case counts in a
wastewater-contamination study that discusses resistance genes and
microbial shifts, never cholera or clinical case counts. Plausible
enough to sound real (cholera is a genuine wastewater-linked disease),
not obviously off-topic, and not actually reported.

*Failure mode caught:* hallucination under a near-miss. The harder
examples in this set are deliberately adjacent to real content, testing
whether the system distinguishes "related" from "actually reported,"
rather than testing trivial off-topic rejection.

*Scoring:* logged, `not_scored`. This is a conscious trade-off, not an
oversight: judging whether the *generated answer* correctly refused
requires either manual review or an LLM-judge pass over generated text.
The current harness only scores retrieval (which documents came back),
not generation (what the model said about them) — so an unanswerable
query can't be pass/failed by the same document-matching logic used for
the other four categories. Retrieved sources are still recorded for
every unanswerable query, so a human (or a future judge-model pass) can
review whether retrieval at least avoided confidently surfacing an
unrelated document as if it were relevant, even though the harness
doesn't auto-score that today.

## Consequences

- Evaluation always exercises the same `retrieve()` code path used in
  production (see ADR-001), so category-level results reflect real
  system behavior, not a separate test harness that could drift from
  what's shipped.
- The two non-trivial scoring rules (`cross_doc_distractor`'s ranking
  requirement, `cross_doc_synthesis`'s AND condition) are deliberately
  stricter than simple presence-checking, in different directions —
  order-sensitivity for one, no-partial-credit for the other — because
  presence-only scoring would have overstated retrieval quality on
  exactly the categories designed to be hard.
- **Known limitation:** `multi_hop` scoring does not verify that both
  connected facts were retrievable, only that the source document was.
- **Known limitation:** `unanswerable` correctness (did the system
  actually refuse, rather than merely "did retrieval avoid an unrelated
  doc") is not automatically scored. Closing this gap would require an
  LLM-judge pass over generated answers — a natural next step, and one
  that would also address the broader "evaluation methodology" gap
  flagged as unaddressed AI-theory ground.

  ## Update: `abstract_summary` field for golden QA authoring

`corpus_manifest.json` entries include an `abstract_summary` field to
support drafting new golden QA cases without opening full text for
every candidate query. It's sufficient for `direct_lookup` and
`cross_doc_distractor` first drafts (top-line findings, primary
outcomes), but not for cases depending on subgroup results or
table-level figures — e.g. `q128`/`q129`
(`cardio-mi-risk-stratification.pdf`) needed full-text verification
since the abstract didn't name the specific lab marker or mention
hypertension at all. Use the abstract for a first draft; verify
against full text before adding table/subgroup-dependent cases to
`golden_qa.json`.