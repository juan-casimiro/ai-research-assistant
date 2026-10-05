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

**Update: the category is not a clean sufficiency-flag oracle.** With
`context_sufficient` now returned by `/query` (ADR-001), it was expected
that `unanswerable` queries would all report `false`. They do not, and
the category is not at fault — it conflates two distinct cases:

- **Fact genuinely absent** (e.g. `q138`, FMT treatment-duration
  reduction): reports `false`, as expected.
- **False premise** (e.g. `q083`, EarlyCDT-Lung FDA validation): the
  question presupposes something untrue. Correctly rejecting the premise
  *is* a sufficient answer, so the flag reports `true`.

Scoring the category as an all-false expectation would therefore
mislabel correct behaviour as a flag failure. Splitting `false_premise`
into its own category is the natural fix, deferred as it would require
re-labelling existing entries.

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

## Versioned cardiology benchmark rebuild

[Corpus and benchmark standards v1](../benchmark/STANDARDS.md) governs JUA-106.
JUA-109 adds the separate [45-case cardiology query release](../benchmark/cardiology/v1/BENCHMARK.md),
subject to independent PR review and freeze before experiments. The historical
schema/scoring above remains unchanged for `golden_qa.json`; it is not a measure
of passage sufficiency or answer correctness.

In versioned mode, `eval_golden.py` still calls production `retrieve()` and records
reranked chunks/sources at depths 3 and 8. Document coverage, conservative pinned
excerpt coverage, fact recall and competitor ordering are distinct. Complete
alternatives use OR; each set requires all its anchors. An excerpt spanning chunks
requires every whole chunk in a contiguous production window certified against
its pinned source offsets, regardless of retrieval rank. The offline oracle
checks unlimited coverage and minimum complete-evidence chunk budgets. V3
reports full-set and feasible-only coverage at each depth, with structural
ceilings and infeasible IDs; document coverage and partial fact recall retain
all scored cases. All 42 evidence-bearing cases fit at n=8, but only 30 fit at
n=3 (27/38 answerable and 3/4 false-premise correction cases). These are
structural assertions, not retrieval-quality results. Absent facts are unscored;
false-premise correction evidence is reported separately from judging generated
corrections. Exact matching cannot exclude valid paraphrases, so failures require
context inspection. JUA-40 retains separately sequenced answer-judge work.

`compare_evals.py` now rejects changed queries/revisions, scorer/retrieval/corpus
fingerprints, depths, changed/missing feasibility and incomplete executed-ID sets.
Explicit nested comparisons
hold retrieval flags fixed and preserve common article tuples. Historical pairs
require `--allow-legacy`, are labelled unverifiable and cannot be mixed with the
new release. This prevents a repaired reference or changed corpus from appearing
as an improvement to the old benchmark. No new quality results are claimed.

## Diabetes expansion and frozen cardiology interference

JUA-111 adds the [versioned diabetes release](../benchmark/diabetes/v1/README.md):
16 topic/overlap sources, 49 cases and 55 pinned anchors, with the original
21-article cardiology selection extended by 11 verified permissive articles.
Legacy sources/cases are audited and migrated explicitly; new cohorts cannot
inherit retired numerical gold. Four absent-fact cases are scoped to selected
main PDFs; three false-premise cases require affirmative correction evidence.
A generic HIF question accepts either complete review evidence set.

The diabetes pair compares 16 with 32 articles. The frozen cardiology pair
compares 21 with 32 using the exact original questions and anchors inside a
common extended selection envelope. A fresh 21-article baseline is required
because historical results have incompatible selection/envelope fingerprints.
No historical output is relabelled. Only local vector retrieval and production
reranking are run; complete final coverage is justified by corpus expansion,
with no four-configuration sweep or paid calls. See the release report for
source-aware context review, feasibility ceilings and evidence limitations.

## Combined four-topic comparison

The [combined report](../benchmark/combined/v1/REPORT.md) evaluates the frozen
cardiology, diabetes, oncology and outlier releases against 51 unique articles
and 3,350 chunks. All 148 IDs execute at both depths; 120 answerable cases,
17 false-premise cases and 11 absent-fact cases keep separate denominators.
The prepared ALS/FTD strand was excluded from this historical snapshot.
Question-specific original source/topic scopes remain explicit for negatives;
an integrated collection does not broaden a named-study question automatically.

The common comparison envelopes preserve per-query objects, anchors and common
article tuples. Compatible historical baselines can be retained without new
retrieval through a verified derivation: complete ID coverage, identical query
hashes, scorer and feasibility, pinned source versions, actual production chunks
and recomputed metrics must agree. Derived artifacts retain their parent hash,
run ID, timestamp, commit and original provenance and explicitly record zero
retrieval calls. They are not fresh executions. New C3 runs also require model,
retrieval, configuration and ingestion fingerprints compatible with the parents.

Per-topic/category and minimum-evidence-chunk groups distinguish source loss,
passage loss, infeasible budgets and conservative whole-span misses. Unique
source/anchor unions count retrieval only in cases that use those sources or
anchors; their breadth is not per-case completeness, and optional alternatives
remain optional. Context changes and competitor exposure are reported even when
scores do not change. No outlier chunks appeared in the other three topics'
returned contexts, so this run does not establish resistance to outlier
interference. Pre-rerank candidates were not recorded; mechanism claims remain
unverified. Positive document changes can still lack complete evidence, and
literal-span losses can still retain substantive answer content.

This is one local vector-only corpus comparison, with BM25/rewriting off and
zero answer/refusal judgments. Answer-judge work retains its separate sequencing;
paid rewriting/generation/judge runs require explicit run approval. The original
96.4%/98.2% host-corpus metrics and Docker demo remain separate from rebuilt gold.

## Corrected five-topic snapshot

The [corrected combined report](../benchmark/combined/v2/REPORT.md) freezes the
current model-reviewed gold and accepted correction ledger for all 158 cases in
a 55-article / 3,638-chunk corpus, including ALS/FTD. Its canonical source query
objects and anchors are preserved; the comparison envelope, conditions and
dependency map receive new fingerprints. The original 51/148 runs remain
historical. Changed questions, categories, scorer fingerprint and corpus prevent
a direct historical performance comparison, despite an unchanged scorer version
label. New complete nested runs pass the existing compatibility guard.

One local vector-only configuration with production reranking evaluates every
case at n3/n8 and six complete topic baselines (722 retrieval calls, zero paid
provider calls). Existing production embeddings are reused only after checking
the original model/dependency/code/source/chunk provenance; new source chunks
use production ingestion. Fresh stores disable seeding, verify exact source/chunk
multiplicities, hash copied and final vectors, and record per-source filtered
query probes. Those probes prove queryability, not unfiltered QA success.

Saved contexts, metrics, summaries, gold and all provenance joins are independently
recomputed. Offline replay reproduces envelopes/dependency metadata and analysis;
fresh approximate-index inference is not promised to be byte-identical. At n8,
answerable document coverage is 115/129 and pinned evidence 37/129; correction
evidence is 6/18 and eleven absent-fact cases are unscored. c012/c013/x005 retain
both attributed readings, with valid failures preserved. No answer/refusal or
conflict-handling accuracy is inferred from retrieval. The durable
[source-conflict report](../docs/evaluation/source-conflicts.md) and
[minimal provenance summary](../docs/evaluation/combined-benchmark-v2.json) are
intended for retention independently of bulk experiment files. Biomedical expert
review, semantic adjudication and answer judging remain separate limitations.
