# Evaluation benchmark

## Current benchmark: five topics, 55 articles, 158 questions

Use [combined/v2](combined/v2/README.md) to prepare, verify and evaluate the current
benchmark. The [results report](combined/v2/REPORT.md) explains measured retrieval
outcomes, failures and limitations. The
[result and provenance summary](../docs/evaluation/combined-benchmark-v2.json)
provides a structured record of the reported experiment.

The questions test direct lookup, multi-hop reasoning, cross-document synthesis,
distractor discrimination, source conflicts, false premises and missing facts.
Expected answers and evidence were authored and reviewed by advanced LLMs reading
the articles. They are inspectable reference judgments, not biomedical expert
validation, and may need explicit corrections as defects are discovered.

Current automated scores measure whether the relevant articles and supporting
passages were retrieved. They do not yet judge whether the generated response
correctly explains those findings, handles conflicts or refuses unsupported claims.

## Questions, articles and evidence

Each topic in `combined/v2/` supplies `queries.json` with questions, categories,
required claims, expected responses and evidence anchors; `conditions.json`
defines its topic and combined-corpus membership. The
[shared manifest](combined/v2/manifest.json) identifies selected article versions.
The [case dependency map](combined/v2/case_dependencies.json) connects questions
to required sources, alternatives, distractors and evidence.

Topic source directories preserve article selection, attribution and authoring
decisions. These remain relevant inputs; a topic directory's `v1` does not mean
its questions are obsolete. Use the combined v2 conditions for the current
combined evaluation rather than earlier topic-only placeholders.

| Topic | Selection and question decisions | Current evaluation inputs |
| --- | --- | --- |
| Cardiology | [Topic guide](cardiology/v1/README.md), [case design](cardiology/v1/BENCHMARK.md) | [Queries](combined/v2/cardiology/queries.json), [conditions](combined/v2/cardiology/conditions.json) |
| Diabetes | [Topic guide](diabetes/v1/README.md), [legacy audit](diabetes/v1/AUDIT.md) | [Queries](combined/v2/diabetes/queries.json), [conditions](combined/v2/diabetes/conditions.json) |
| Oncology | [Topic guide](oncology/v1/README.md), [decision record](oncology/v1/DECISIONS.md) | [Queries](combined/v2/oncology/queries.json), [conditions](combined/v2/oncology/conditions.json) |
| Outliers | [Topic guide](outliers/v1/README.md) | [Queries](combined/v2/outliers/queries.json), [conditions](combined/v2/outliers/conditions.json) |
| ALS/FTD | [Topic guide](als-ftd/v1/README.md) | [Queries](combined/v2/als-ftd/queries.json), [conditions](combined/v2/als-ftd/conditions.json) |

The [source-conflict report](../docs/evaluation/source-conflicts.md) gives readable
question-by-question examples of competing claims, article identities, evidence
locations and expected handling. [STANDARDS.md](STANDARDS.md) explains the
selection, authoring and comparison rules.

## Historical results and Docker demo

- **Original host benchmark:** root `golden_qa.json` and `corpus_manifest.json`,
  133 questions against 19 articles. Its 96.4%/98.2% document/category-ranking
  figures belong to that experiment. The root README labels its legacy commands.
- **Earlier combined experiment:** [combined/v1 report](combined/v1/REPORT.md),
  51 articles and 148 questions across four topics, excluding ALS/FTD. Changed
  gold, scorer and corpus prevent direct comparison with combined v2.
- **Earlier topic runs:** retained in topic directories as development and
  comparison evidence. The current v2 report identifies compatible current-gold
  baselines; use those for its nested-corpus comparisons.
- **Docker demo:** a smaller bundled seed corpus for trying the service. It does
  not reproduce either host benchmark's quality figures.

The complete committed epic before release cleanup is preserved at
[benchmark-epic-before-cleanup-2026-10-06](https://github.com/juan-casimiro/ai-research-assistant/tree/benchmark-epic-before-cleanup-2026-10-06).
This archive contains development history; it does not include ignored local PDFs
or replace the current benchmark's reproduction instructions.
