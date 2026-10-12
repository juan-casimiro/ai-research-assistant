# Benchmark integration record

This records selected capabilities extracted from the corpus-benchmark epic to
main through 12 October 2026. It is a capability summary, not a complete retained-file
inventory or final epic release gate. Live task and CI status belongs in Linear
and pull requests.

| Delivered capability | Authoritative entry point / delivery evidence |
| --- | --- |
| Fresh 55-article PMCID manifest, licence/identity/checksum/readability checks and V1 preservation | [Corpus workflow](../tools/corpus/corpus-metadata-workflow.md); PR [#56](https://github.com/juan-casimiro/ai-research-assistant/pull/56) |
| Consolidated 158-query inputs, accepted alternatives and production document/evidence scoring | [Q&A schema](../data/queries-schema.md), [evaluation workflow](../tools/evaluation/evaluation-workflow.md); PR [#60](https://github.com/juan-casimiro/ai-research-assistant/pull/60) |
| In-process fresh ingestion beside a named corpus, with seeding disabled and exact chunk checks | [Ingestion workflow](../tools/corpus/ingestion-workflow.md); PR [#61](https://github.com/juan-casimiro/ai-research-assistant/pull/61) |
| Prerequisite routing, four-strategy batch evaluation, local response logs and complete-result publication | [Evaluation workflow](../tools/evaluation/evaluation-workflow.md); PRs [#64](https://github.com/juan-casimiro/ai-research-assistant/pull/64), [#66](https://github.com/juan-casimiro/ai-research-assistant/pull/66), [#67](https://github.com/juan-casimiro/ai-research-assistant/pull/67) |
| Offline compatible-run comparison with category/per-query accounting and saved findings | [Comparison workflow](../tools/evaluation/comparison-workflow.md), [findings](../data/evaluations/mvp/2026-10-09-anthropic/comparison/findings.md); PR [#68](https://github.com/juan-casimiro/ai-research-assistant/pull/68) |

## Candidates for later selection

The epic retains a readable case/article catalogue, cross-topic and source-conflict
analysis, historical experiment/replay evidence and a complete release inventory.
Their main integration or consolidation needs a separate dependency and scope
review; none is implied by the current four-strategy findings. The pinned
[epic scope rationale](https://github.com/juan-casimiro/ai-research-assistant/blob/6bfed40218fcdf94c4bbc0dbdd44c817760f63dd/docs/release-scope.md)
is reference evidence, not the current main setup guide.

Reusable corpus-addition impact review and provider-neutral skill installation
remain follow-up candidates; current `.agents/skills/` already routes acquisition,
ingestion, evaluation and comparison to delivered workflows. Preserve operational
instructions until an authoritative replacement exists. Generated-answer judging
is separate work and is not supplied by retrieval scoring.

Final epic-to-main retained-file selection, divergence resolution and release-gate
review remain separate decisions after integration choices settle.
