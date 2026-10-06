# Benchmark tools

The [current benchmark](combined/v2/README.md) has 55 articles and 158 cases.
Its [case index](cases/README.md) explains the questions and expected evidence;
its [report](combined/v2/REPORT.md) states measured retrieval results and limits.
Run commands from the repository root with the Python 3.12 environment.

## Acquire and prepare sources

[download_corpus.py](../download_corpus.py) supports manifest-based PDF downloads;
[fetch_article_metadata.py](../fetch_article_metadata.py) acquires authoritative
PMC/PubMed metadata. Follow the topic guides for pinned article versions, licences,
manual exceptions and local XML acquisition. Downloaded PDFs/texts stay ignored.
Metadata acquisition alone does not establish source eligibility or integrity.

[prepare_corpus.py](combined/prepare_corpus.py) builds a local view from already
acquired topic files, checking every PDF/text against the selected manifest:

```sh
.venv/bin/python benchmark/combined/prepare_corpus.py \
  --benchmark benchmark/combined/v2/cardiology --corpus-dir corpus/combined-v2 \
  --sources corpus/cardiology-v1 corpus/diabetes-v1 corpus/oncology-v1 \
  corpus/outliers-v1 corpus/als-ftd-v1
```

Topic integrity tools remain useful: [cardiology](../verify_cardiology_selection.py),
[oncology](../verify_oncology_release.py), [ALS/FTD](../verify_als_ftd_release.py),
[ALS/FTD alternatives](../verify_als_ftd_alternatives.py), and
[evidence reachability](../verify_benchmark_reachability.py). Read their topic
instructions for required inputs. These verify source identities, metadata,
licences or evidence against pinned inputs; they do not judge generated answers.

## Fresh isolated ingestion and evaluation

[ingest_isolated.py](ingest_isolated.py) is the shared entry point for new stores.
It verifies the release inputs, ingests only the selected condition through
production `main.ingest`, fingerprints loaded models, verifies the chunk multiset
and BM25 count, and atomically finalizes a new receipt. It refuses existing store
and receipt paths before loading models. Failed runs retain a setup receipt for
inspection; retry with fresh paths. Importing the helper does not start ingestion.

```sh
SEED_ON_EMPTY=false OTEL_TRACES_EXPORTER=none CHROMA_PATH=<fresh-store> \
  .venv/bin/python benchmark/ingest_isolated.py \
  --benchmark benchmark/combined/v2/cardiology --corpus-dir corpus/combined-v2 \
  --condition C3 --receipt <new-ingestion.json>
SEED_ON_EMPTY=false OTEL_TRACES_EXPORTER=none CHROMA_PATH=<fresh-store> \
  .venv/bin/python eval_golden.py --benchmark benchmark/combined/v2/cardiology \
  --corpus-dir corpus/combined-v2 --condition C3 --output <new-cardio.json>
```

Use the appropriate topic adapter and condition for nested baselines.
[compare_evals.py](../compare_evals.py) checks compatible nested comparisons.
The original host [HTTP ingestion script](../ingest_corpus.py) remains a separate
server-based workflow described in the root README.

[reuse_store.py](combined/reuse_store.py) can reuse verified vectors from an
eligible retained store; see the current reproduction instructions. Its original
receipts additionally bind embedding digests, dependencies and source probes.
The shared fresh-store helper does not produce those extra fields: keep its new
receipts/results separate from the sealed experiment. Fresh runs have new IDs,
timestamps and possible approximate-index variation. Retrieval coverage does
not establish answer correctness; paid generation/rewrite/judge runs require
explicit run approval.

## Verify retained evidence and readable cases

```sh
# No corpus, models or network; requires the archive commit in local Git:
.venv/bin/python -m benchmark.combined.verify_release_artifacts
.venv/bin/python render_case_index.py --check
# Full saved-context replay requires the pinned ignored corpus and dependencies:
.venv/bin/python benchmark/combined/verify_corrected_release.py
```

The [artifact verifier](combined/verify_release_artifacts.py) checks original
sealed bytes and the versioned presentation overlay. The
[full verifier](combined/verify_corrected_release.py) rebuilds current envelopes,
replays saved contexts through scoring, checks source/receipt/attribution joins
and matches the durable summary. Its optional `--stores` additionally needs the
original stores. [verify_corrected_runs.py](combined/verify_corrected_runs.py)
can write recomputed analysis to a fresh output path. These checks make no new
retrieval or provider calls.

[render_case_index.py](../render_case_index.py) generates readable case pages;
source JSON remains authoritative. Regenerate only after explicit input changes.
Original scientific seals, gold, contexts and results remain immutable.

## Why historical tools and duplicate evidence remain

Historical helpers preserve the code used to create retained results and the
paths/hashes those results reference. They remain available for reproduction;
use the shared tools above for new ingestion and corpus preparation.

| Retained tool or evidence | Purpose |
| --- | --- |
| Topic `runs/ingest_isolated.py` and cardiology's dated helper | Original ingestion provenance and helper fingerprints; not replaced with wrappers. |
| [build_release.py](combined/build_release.py) | Historical four-topic envelope builder; also supplies frozen-write utilities to the current builder. |
| [build_corrected_release.py](combined/build_corrected_release.py) | Current five-topic envelopes and dependency map from retained topic sources. |
| [derive_baseline.py](combined/derive_baseline.py), [summarize_runs.py](combined/summarize_runs.py) | Historical parent-linked derived baselines and four-topic analysis. |
| Diabetes [rescore_saved.py](diabetes/v1/runs/rescore_saved.py) | Explicit annotation rescoring linked to original/evaluated inputs and raw parents. |
| Oncology [assemble_runs.py](oncology/v1/runs/assemble_runs.py) | Assemble disjoint raw run subsets without new retrieval. |
| Oncology [render_decisions.py](oncology/v1/render_decisions.py) | Substantive source selection/exclusion rationale, also used by its verifier. |
| Outlier [regression builder](outliers/v1/runs/build_topic_regression.py), [preparer](outliers/v1/runs/prepare_regression_corpus.py), [ALS/FTD audit verifier](outliers/v1/als-ftd-audit-v1/verify.py) | Historical mixed-topic envelope, preparation recipe and source audit. |
| Topic metadata, historical manifests, authoring/evaluated envelopes, raw and derived runs | Exact source archive paths, seals, parent chains and evidence supporting historical reports. |

Current combined v2 already uses one shared manifest with five topic symlinks.
Deduplicating older manifests or metadata would change sealed paths or original
input relationships. Retaining them avoids rewriting scientific provenance.
Intermediate review workflows live in the
[immutable archive](https://github.com/juan-casimiro/ai-research-assistant/tree/benchmark-epic-before-cleanup-2026-10-06);
[final review findings](validation/v1/REPORT.md) and later corrections remain local.
