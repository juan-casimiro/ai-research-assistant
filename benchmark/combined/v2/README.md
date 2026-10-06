# Corrected five-topic benchmark snapshot

[REPORT.md](REPORT.md) describes verified 55-article / 158-query results, compatible
nested comparisons, valid failures, verification and limitations. The preserved
[51/148 report](../v1/REPORT.md) is historical and not directly comparable.
[PRE_RUN_REVIEW.md](PRE_RUN_REVIEW.md) fixes scope and review boundaries before
interpretation. No gold is edited by this experiment.

Five topic directories share one 55-article manifest. They preserve current
source query objects/anchors and declare original C1/C2 membership plus combined
C3. [case_dependencies.json](case_dependencies.json) rebuilds current query,
source/evidence/distractor/negative/overlap dependencies with canonical hashes.
[reachability.json](reachability.json) records current source/ALS metadata and
alternative verification and all five production-chunker feasibility checks.
[runs](runs) contains eleven complete production retrieval outputs and seven
verified ingestion receipts. [analysis.json](analysis.json) is the deterministic
recomputed comparison, including category/evidence-budget groups and exposure.
[artifact_hashes.json](artifact_hashes.json) seals the files and relevant sources.
The retained [durable summary](../../../docs/evaluation/combined-benchmark-v2.json)
and [source-conflict report](../../../docs/evaluation/source-conflicts.md) support
later release selection without requiring bulk run contexts.

## Reproduce verification

Use the repository's Python 3.12 environment and pinned local topic inputs.
Preparation verifies source bytes and refuses changed frozen envelopes. This
requires no model/provider call:

```sh
.venv/bin/python benchmark/combined/build_corrected_release.py --output benchmark/combined/v2
.venv/bin/python benchmark/combined/prepare_corpus.py \
  --benchmark benchmark/combined/v2/cardiology --corpus-dir corpus/combined-v2 \
  --sources corpus/cardiology-v1 corpus/diabetes-v1 corpus/oncology-v1 \
  corpus/outliers-v1 corpus/als-ftd-v1
.venv/bin/python benchmark/combined/verify_corrected_release.py
# Also check the saved local stores and embedding digests, when still available:
.venv/bin/python benchmark/combined/verify_corrected_release.py --stores
.venv/bin/python benchmark/combined/verify_corrected_runs.py --output <new-analysis.json>
# The new analysis must equal the committed analysis.json byte for byte.
.venv/bin/python -m unittest discover -v
```

The full source inputs are ignored local files, not shipped in Git. Original
attribution/metadata archive paths resolve in the topic releases named by the
manifest's `source_releases`. Retain their licence/notice inventories if selecting
these manifests for a release. Source verification needs all manifest inputs,
even for a smaller nested condition. ALS/FTD metadata revalidation additionally
needs the four pinned local article XML files; its original source instructions
provide the acquisition recipe. No public PDF redistribution is authorized.

## Fresh retrieval execution

Always use fresh store, receipt and output paths. The evaluator refuses to
replace an existing run and validates the actual collection before retrieval.
Set `SEED_ON_EMPTY=false`. A retained valid 51-article production store can supply
unchanged embeddings; the reuse helper checks its original receipt, model files,
dependency versions, source bytes, production code and chunk multiset. Only
missing articles are newly ingested; copied vectors are hash-checked. Example:

```sh
SEED_ON_EMPTY=false OTEL_TRACES_EXPORTER=none CHROMA_PATH=<fresh-store> \
  .venv/bin/python benchmark/combined/reuse_store.py \
  --benchmark benchmark/combined/v2/cardiology --corpus-dir corpus/combined-v2 \
  --condition C3 --parent-store <preserved-51-article-store> \
  --parent-receipt benchmark/combined/v1/runs/C3-ingestion.json \
  --parent-corpus corpus/combined-v1 --receipt <new-ingestion.json>
SEED_ON_EMPTY=false OTEL_TRACES_EXPORTER=none CHROMA_PATH=<fresh-store> \
  .venv/bin/python eval_golden.py --benchmark benchmark/combined/v2/cardiology \
  --corpus-dir corpus/combined-v2 --condition C3 --output <new-cardio.json>
# Repeat the same C3 store for diabetes, oncology, outliers and als-ftd.
```

If the parent is unavailable/incompatible, use the existing production-ingestion
helper `benchmark/ingest_isolated.py` with the same benchmark,
corpus, condition and fresh receipt/store arguments, from the repository root. This
embeds the whole selected condition rather than copying historical vectors; it
still makes no paid provider call. Its receipt lacks the reuse-specific embedding
and per-source probe fields, so do not silently substitute it into this sealed
experiment. Preserve and verify that new experiment separately.

Current-gold nested baselines use a fresh verified store for cardiology C1/C2,
diabetes C2, oncology C2, outliers C1 and ALS/FTD C1. They execute complete topic
coverage, holding the current gold/scorer/models/flags fixed. The existing
`compare_evals.py <before> <after> --nested-corpus` verifies compatibility; do not
compare these results directly to v1 or relabel old contexts as fresh executions.
A fresh run has new run IDs/timestamps and may have approximate-index variation;
byte-identical reproduction here refers to saved-evidence verification/analysis.

Only one vector-only configuration was executed. BM25, rewriting, generation and
judging are omitted; paid evaluations require explicit approval for the run.
The 722 local retrieval calls, 576 new chunk embeddings, 134 filtered source
probes, zero provider calls and $0 paid cost are recorded in the report.
