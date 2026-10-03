# Frozen combined four-topic comparison

Read [REPORT.md](REPORT.md) for the results, changed-case evidence review,
failure taxonomy and unresolved work. [PRE_RUN_REVIEW.md](PRE_RUN_REVIEW.md)
records the pre-retrieval source/negative-scope review. The selection contains
51 articles; four ALS/FTD articles and ten prepared cases await independent
review/freeze and are excluded. No 55-article quality claim is made.

Each topic directory is a comparison envelope with an identical merged manifest
and its original frozen query objects/anchors. C1/C2 retain original topic
membership; C3 is the 51-article union. Cardiology C1/C2 contain 19/21 sources;
diabetes C1=C2 has 16; oncology C1/C2 contain 13/14; outliers C1=C2 has five.
Diabetes's evaluated snapshot is preserved in its original topic release.
Historical raw runs remain untouched; `runs/*-parent.json` are explicitly derived
artifacts with original parent provenance and zero new retrieval calls.

The manifests retain original article records, including metadata archive paths
relative to their original topic releases. `source_releases` identifies those
authoritative manifests; metadata archives are not duplicated here.
Attribution/notice/third-party inventories cover every selected article:
[cardiology](../../cardiology/v1/ATTRIBUTION.md),
[diabetes](../../diabetes/v1/ATTRIBUTION.md),
[oncology](../../oncology/v1/ATTRIBUTION.md),
[outliers](../../outliers/v1/ATTRIBUTION.md).
Shared articles are counted once. Exact versions, licence links, download routes
and byte hashes stay in the manifests. PDFs/full text remain ignored local files;
publication requires separate authorization.

## Reproduce without overwriting saved evidence

Use the repository's Python 3.12 virtual environment and already verified topic
PDFs/texts. The builder checks shared source identity and refuses to replace a
different frozen envelope. Input views verify every PDF/text hash; they never
silently accept drift. The following preparation makes no model/provider call:

```sh
.venv/bin/python benchmark/combined/build_release.py --output benchmark/combined/v1
.venv/bin/python benchmark/combined/prepare_corpus.py \
  --benchmark benchmark/combined/v1/cardiology --corpus-dir corpus/combined-v1 \
  --sources corpus/cardiology-v1 corpus/diabetes-v1 corpus/oncology-v1 corpus/outliers-v1
```

Use new receipt/output/store paths for a rerun. The saved results were generated
with the existing isolated ingestion helper; it rejects pre-existing stores and
receipts. The runner checks exact stored chunk multiplicities again before any
retrieval. No HTTP server is required. `SEED_ON_EMPTY=false` is mandatory:

```sh
SEED_ON_EMPTY=false OTEL_TRACES_EXPORTER=none PYTHONPATH=. \
  CHROMA_PATH=<fresh-store> .venv/bin/python \
  benchmark/outliers/v1/runs/ingest_isolated.py \
  --benchmark benchmark/combined/v1/cardiology --corpus-dir corpus/combined-v1 \
  --condition C3 --receipt <new-ingestion.json>
SEED_ON_EMPTY=false OTEL_TRACES_EXPORTER=none CHROMA_PATH=<fresh-store> \
  .venv/bin/python eval_golden.py --benchmark benchmark/combined/v1/cardiology \
  --corpus-dir corpus/combined-v1 --condition C3 --output <new-cardio.json>
# Repeat evaluation for diabetes, oncology and outliers in the same verified store.
# Use --ids only for justified targeted iteration, preserving new immutable outputs.
```

Baseline derivation verifies saved context bytes and metrics with unchanged gold.
Use a fresh output path; repeat for the other listed raw parents as needed:

```sh
.venv/bin/python benchmark/combined/derive_baseline.py \
  benchmark/cardiology/v1/runs/C1-vector.json \
  --benchmark benchmark/combined/v1/cardiology --corpus-dir corpus/combined-v1 \
  --condition C1 --output <new-C1-parent.json>
.venv/bin/python compare_evals.py <new-C1-parent.json> <new-cardio.json> --nested-corpus
```

The other immutable parents are cardiology `runs/C2-vector.json`, diabetes
`runs/diabetes-C2-reviewed.json`, oncology `runs/C2-complete.json`, and outliers
`runs/outliers-C1-vector-reviewed.json`. These preserve original source/scorer/
query fingerprints; derivation must fail if they no longer agree.
The summarizer verifies four complete nested pairs, input fingerprints, all
model/ingestion joins, stored summaries and the complete historical 18-case slice:

```sh
.venv/bin/python benchmark/combined/summarize_runs.py --output <new-analysis.json>
.venv/bin/python -m unittest discover -v
```

`analysis.json` is a committed snapshot. A later summarizer output must equal it
for the preserved artifacts. `artifact_hashes.json` pins every delivered envelope,
run, receipt, analysis, report and helper, plus the original parent runs and
production scorer/retrieval files. Rebuilding/analysis does not rerun retrieval.
One fresh execution per topic was made: 296 calls, all 148 IDs at both depths.
No BM25/rewrite sweep, generation, refusal scoring or paid judge was executed.
