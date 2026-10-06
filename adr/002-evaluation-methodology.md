# ADR-002: Evaluation Methodology

## Context

A retrieval-augmented answer can fail because it finds the wrong articles,
misses necessary passages, or generates an unsupported interpretation. These
are different failure modes and need separate measurements. Biomedical papers
provide dense, citation-heavy material with similar terminology, competing
claims and scoped numerical results for testing a domain-agnostic pipeline.

The current [V2 benchmark](../data/benchmark/README.md) contains 55 articles and
158 questions across five topics. Its references were LLM-authored and
model-reviewed against the articles; they are inspectable judgments, not
biomedical expert certification. The [standards](../docs/benchmark-standards.md)
define selection and authoring rules. The [historical methodology](../docs/historical-evaluation-methodology.md)
preserves the original V1 category design and the sequence of topic/combined
experiments; those inputs and results retain their original schemas.

## Decision: measure sources, evidence and answers separately

| Layer | What is measured | What it cannot establish |
| --- | --- | --- |
| Source retrieval | At least one complete accepted source set is present in reranked results | That the necessary passages are present |
| Evidence retrieval | One complete accepted evidence set covers every required fact using pinned excerpts | That a generated response interprets the evidence correctly |
| Generated answer | Required facts, scope, attribution and unsupported-claim handling | Not yet measured by the current automated retrieval experiment |

Alternative evidence sets use OR; all members of a chosen set are required.
The scorer records document coverage, complete pinned evidence, partial fact
recall and named-distractor ordering independently. Missing facts are unscored
by retrieval completeness. False-premise correction evidence is measured
separately from whether an answer actually corrects the premise. The service's
`context_sufficient` flag is a model signal, not an answer-correctness oracle.

`n=3` and `n=8` are chunk budgets, not unique-document counts. An offline oracle
checks whether each accepted evidence set can fit under production chunking.
Full-set denominators retain structurally infeasible cases; feasible-only
coverage is reported separately. Conservative exact excerpt matching can miss
valid paraphrases, so a failed evidence match requires context inspection and
does not by itself prove that an answer would be wrong.

## Decision: freeze evidence relationships before evaluation

Each question records required facts, expected response, accepted alternatives,
source identities, evidence locations and plausible distractors. The generated
[case index](../data/benchmark/cases/README.md) makes those relationships readable;
the versioned JSON remains authoritative. Select cases for coverage and realistic
difficulty, then freeze gold and grading before observing retrieval outcomes.
Record genuine reference defects as explicit revisions with preserved originals.

The categories exercise direct lookup, separated facts within an article,
cross-document synthesis, distractor discrimination, source conflicts, false
premises and absent facts. For accepted source-conflict cases c012/c013/x005,
the original questions and both attributed readings are required. Do not select
one reading as uncontested, merge incompatible values, narrow the question or
relax grading to turn a failure into a pass. The [source-conflict findings](../data/findings/source-conflicts.md)
show exact questions, source roles, locations and measured retrieval limits.

## Decision: compare controlled conditions on production retrieval

The harness calls the same `retrieve()` used by the API, retaining reranker
inference and score consumption inside `asyncio.to_thread()` and reranked source
order during deduplication. Do not index gold, anchors or expected responses as
retrieval inputs. Fresh stores disable seeding and must match the declared
article/chunk membership; filtered probes establish queryability, not QA success.

Configuration comparisons hold corpus, gold, scorer and component fingerprints
fixed. Nested-corpus comparisons vary only declared article membership, retaining
identical shared article versions, questions, retrieval flags, scorer and model
provenance. Both require complete requested/executed IDs and depths. The
comparison utility rejects incompatible versioned runs. A changed benchmark is
not evidence of a performance gain; legacy pairs require explicit opt-in and are
labelled unverifiable.

The current saved experiment used one local vector-only configuration with
production reranking, BM25 and rewriting off, at n=3/n=8. It contains complete
combined runs and six compatible nested baselines. This is a snapshot, not a
repeat-run stability estimate or a completed four-configuration comparison.
Future paid rewriting or generated-answer judging requires approval of that run.

## Evidence and consequences

At n=8, the saved experiment retrieves complete source sets for **115/129**
answerable questions and complete pinned evidence for **37/129**. No synthesis
case has complete pinned evidence (0/17), and source-conflict evidence passes
1/3. Failures remain visible. These findings establish a gap between source
retrieval and complete evidence; they do not establish answer accuracy or the
mechanism of upstream candidate displacement.

The [findings](../data/findings/retrieval.md) provide scoped results, compatible
comparisons and saved-context inspection. The [minimal summary](../data/findings/combined-benchmark-v2.json)
retains source/query/run/configuration provenance. Raw contexts, receipts,
analysis, seals and verification are under [evaluations](../data/evaluations/).
Original V1, earlier combined results and the Docker seed demo have different
scopes and must not share one accuracy headline.

Use the [data guide](../data/README.md#verify-the-retained-experiment) to check
immutable relocated bytes and replay the saved analysis. Original paths/hashes
stay in frozen records; the layout map and historical runner resolve them in a
temporary original-layout view with the recorded historical code. Maintained
utilities produce new source fingerprints for new experiments. Offline replay
can reproduce saved evidence and analysis; fresh approximate-index inference
is not promised to be byte-identical.

Biomedical expert review, semantic adjudication, generated-answer correctness,
refusal/correction behavior and repeat-run stability remain separate limitations
or later evaluation work. Preserving these boundaries keeps the portfolio's
claims auditable and directs improvements toward demonstrated failures.
