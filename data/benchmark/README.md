# Evaluation benchmark

## Current benchmark: five topics, 55 articles, 158 questions

Use [the current release](../README.md) to prepare, verify and evaluate the current
benchmark. The [results report](../findings/retrieval.md) explains measured retrieval
outcomes, failures and limitations. The
[result and provenance summary](../findings/combined-benchmark-v2.json)
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

Browse the [readable case index](cases/README.md) for every question, expected
response, article role, evidence location and recorded distractor explanation.
These pages are generated from the current inputs; update the source JSON and
run `python -m tools.evaluation.render_case_index` to regenerate them.

Each topic directory here supplies `queries.json` with questions, categories,
required claims, expected responses and evidence anchors; `conditions.json`
defines its topic and combined-corpus membership. The
[shared manifest](../manifest.json) identifies selected article versions.
The [case dependency map](case_dependencies.json) connects questions
to required sources, alternatives, distractors and evidence.

Topic source directories preserve article selection, attribution and authoring
decisions. These remain relevant inputs; a topic directory's `v1` does not mean
its questions are obsolete. Use the combined v2 conditions for the current
combined evaluation rather than earlier topic-only placeholders.

| Topic | Selection and question decisions | Current evaluation inputs |
| --- | --- | --- |
| Cardiology | [Topic guide](sources/cardiology/v1/README.md), [case design](sources/cardiology/v1/BENCHMARK.md) | [Queries](cardiology/queries.json), [conditions](cardiology/conditions.json) |
| Diabetes | [Topic guide](sources/diabetes/v1/README.md), [legacy audit](sources/diabetes/v1/AUDIT.md) | [Queries](diabetes/queries.json), [conditions](diabetes/conditions.json) |
| Oncology | [Topic guide](sources/oncology/v1/README.md), [decision record](sources/oncology/v1/DECISIONS.md) | [Queries](oncology/queries.json), [conditions](oncology/conditions.json) |
| Outliers | [Topic guide](sources/outliers/v1/README.md) | [Queries](outliers/queries.json), [conditions](outliers/conditions.json) |
| ALS/FTD | [Topic guide](sources/als-ftd/v1/README.md) | [Queries](als-ftd/queries.json), [conditions](als-ftd/conditions.json) |

The [source-conflict report](../findings/source-conflicts.md) gives readable
question-by-question examples of competing claims, article identities, evidence
locations and expected handling. [Benchmark standards](../../docs/benchmark-standards.md) explains the
selection, authoring and comparison rules.

## Historical results and Docker demo

- **Original host benchmark:** `data/archive/v1/golden_qa.json` and `data/archive/v1/corpus_manifest.json`,
  133 questions against 19 articles. Its 96.4%/98.2% document/category-ranking
  figures belong to that experiment. The [historical V1 guide](../../docs/historical-benchmark.md) documents its commands.
- **Earlier combined experiment:** [combined/v1 report](../archive/development/combined-v1/REPORT.md),
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


## Archived review workflow and release integrity

Intermediate model-review prompts, orchestration, replies and superseded findings
are preserved in the [review archive](https://github.com/juan-casimiro/ai-research-assistant/tree/benchmark-epic-before-cleanup-2026-10-06/benchmark/validation/v1).
The [historical review summary](../archive/development/validation/v1/REPORT.md) retains the methodology,
limitations and links to final decisions and subsequent corrections.

The original experiment seal and release overlay remain unchanged. Frozen JSON
retains its original path records; [the layout inventory](../layout.json) maps
those records to the relocated files. `python -m tools.historical check` verifies
relocated immutable bytes against the pinned pre-move Git commit. The
[replay instructions](../README.md#verify-the-retained-experiment) explain how to
run the original seal and saved-context verifier in a temporary original-layout
view. Current utilities and documentation are reviewed separately; historical
verification uses the recorded historical source code. See [the tool guide](../../tools/README.md).
