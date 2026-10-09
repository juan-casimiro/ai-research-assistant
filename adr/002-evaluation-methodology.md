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

**V1 established a production-path retrieval baseline:** 19 biomedical articles,
133 questions and 111 scored cases. Dense retrieval with cross-encoder reranking
achieved **96.4% at depth 3 and 98.2% at depth 8**. BM25 and query rewriting
were tested as opt-in improvements without a net gain on that corpus; the
incremental experiments and ranking decisions remain recorded in
[ADR-001](001-chunking-and-retrieval.md).

V1 used document-level rules: lookup and multi-hop required the expected source;
synthesis required every expected source; distractor cases additionally required
the expected source ahead of the decoy. Unanswerable cases were recorded without
positive scoring. This baseline did not prove that every supporting passage was
retrieved, or that generated answers were correct.

The current benchmark expands to 55 articles and 158 questions, with pinned
excerpts and separate evidence metrics. This closes the document-only scoring
gap and distinguishes absent facts from false premises. Scores from these two
benchmarks are not directly comparable because corpus, questions and metrics differ.
The [V1 evaluation record](../data/archive/v1/README.md) preserves its corpus,
scoring rules, saved results and high-level technical setup.
Git tag `evaluation-v1-baseline` identifies the main baseline before the evaluator
transition.

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
