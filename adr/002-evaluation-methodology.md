# ADR-002: Evaluation Methodology

## Context

Retrieval architecture and evaluation methodology are separate concerns.
Evaluation must exercise production `retrieve()` so its results describe the
shipped retrieval path. Finding a relevant article and retrieving its supporting
passages are different measurements; neither establishes generated-answer quality.

## Decision

Use questions targeting distinct retrieval failure modes:

| Category | Purpose |
| --- | --- |
| Direct lookup | Find a scoped fact in one article |
| Multi-hop | Retrieve evidence connecting related facts |
| Cross-document distractor | Prefer applicable evidence over a similar decoy |
| Cross-document synthesis | Retrieve all sources needed for a combined answer |
| Unanswerable | Record cases whose requested fact is absent from the reviewed corpus |
| False premise | Retrieve evidence correcting a mistaken premise |
| Source conflict | Preserve differing attributed findings without inventing a reconciliation |

Score document coverage separately from pinned-evidence coverage and fact recall.
A complete alternative evidence set suffices; partial pieces from different sets
do not establish complete evidence. For distractor cases, required sources must
rank ahead of retrieved competitors. Ordering prevents a similar but inapplicable
source from taking precedence over supporting evidence. Synthesis receives no
partial credit because one source cannot support a claim requiring several.
Preserve source attribution, population,
endpoint and scientific qualifiers in the benchmark.

Absent facts receive no positive retrieval score because source presence cannot
establish that a generated answer correctly refused an unsupported claim.
Correct refusal and premise
correction in generated answers require a separate answer evaluation.
Abstracts can support initial question drafting; full-text verification is needed
for supporting passages, subgroup results and table-level figures.

Current commands and input rules belong in the
[evaluation workflow](../tools/evaluation/evaluation-workflow.md) and
[Q&A schema](../data/queries-schema.md).

## Evaluation milestones

The current benchmark uses [55-article corpus metadata](../data/corpus_manifest.json)
and [158 self-contained queries](../data/queries.json). The
[saved four-strategy sweep](../data/evaluations/mvp/2026-10-09-anthropic/README.md)
and [canonical findings](../data/evaluations/mvp/2026-10-09-anthropic/comparison/findings.md)
separate source coverage from complete evidence and partial fact support.
Observed direct-lookup gains coexist with regressions and persistent synthesis
and multi-hop limits; this is one sweep, not a stable ranking or answer evaluation.

The [V1 archive](../data/archive/v1/README.md) owns the original 19-article /
133-query baseline, document-only pass rules, saved results and experiment history.
Corpus, questions and metrics differ, so its scores are not directly comparable.
Historical commands require the `evaluation-v1-baseline` tag.

## Consequences

- Retrieval evaluation remains separate from generated-answer evaluation.
- Complete synthesis and distractor ordering prevent presence-only scoring from
  overstating performance on difficult cases.
- Literal pinned-evidence matching can miss semantic support; retrieval depth can
  also limit complete evidence coverage. Interpret results using the schema's
  metric definitions and benchmark review status.

## Record relocation — 2026-10-09

The original V1 methodology detail was moved verbatim, with relative links
adjusted, to the [V1 methodology record](../data/archive/v1/methodology.md).
