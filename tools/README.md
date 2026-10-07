# Corpus and evaluation utilities

Run maintained utilities as Python modules **from the repository root**. They
accept explicit manifest/release, corpus and output paths so they can work with
the current corpus, an archived version or a newly assembled manifest. Current
research assets are described in [data/README.md](../data/README.md); repository
selection and benchmark rules are in [the standards](../docs/benchmark-standards.md).
PDFs, extracted text and new local outputs are build artifacts, not Git inputs.

| Task | Entry point | Notes |
| --- | --- | --- |
| Fetch a draft article record | `python -m tools.corpus.fetch_article_metadata` | Requires PMCID, explicit PMC version, search query, filename, cluster and output file; includes PMID, PubMed abstract and licence evidence. Does not merge drafts into the frozen manifest. |
| Download manifest PDFs | `python -m tools.corpus.download_corpus` | `--manifest`, `--corpus-dir`, optional repeated `--filename`; defaults to the current manifest. Legacy manual exceptions remain supported. |
| Prepare pinned local PDF/text pairs | `python -m tools.corpus.prepare_corpus` | `--benchmark` points to a directory containing a manifest; `--sources` are already acquired local inputs. Verifies hashes and creates local symlinks; does not assemble the manifest or acquire articles. |
| Ingest a complete manifest | `python -m tools.corpus.ingest_corpus` | `--manifest`, `--corpus-dir`; defaults to the current manifest. Extracts text and uses the service's `/ingest` endpoint. |
| Reset a local collection | `python -m tools.corpus.reset_collection` | Uses configured `CHROMA_PATH`; removes collection contents. |
| Evaluate retrieval | `python -m tools.evaluation.eval_golden` | `--benchmark`, `--corpus-dir`, `--condition`, `--output`; production retrieval adapter is `tools.evaluation.eval_benchmark`. Without `--benchmark`, uses archived V1 gold. |
| Compare evaluations | `python -m tools.evaluation.compare_evals` | Checks provenance compatibility; `--nested-corpus` is for matching-gold nested membership. |
| Inspect legacy context sufficiency | `python -m tools.evaluation.eval_context_sufficient` | Defaults to archived V1 gold/results. Generated-answer judging is not implemented. |
| Regenerate readable cases | `python -m tools.evaluation.render_case_index` | Reads current manifest/questions/dependencies; `--check` writes nothing. |
| Inspect legacy failures/BM25 | `python -m tools.evaluation.show_failures`, `python -m tools.evaluation.debug_bm25` | Small diagnostic scripts; read their configured input/service state before running. |

The topic selection/release integrity utilities also remain under `tools/corpus/`:
`verify_cardiology_selection`, `verify_oncology_release`, `verify_als_ftd_release`,
`verify_als_ftd_alternatives` and `verify_benchmark_reachability`. They retain their
existing topic-specific validation scope. Archived path records are resolved
through `tools.layout.recorded_path`; raw provenance JSON is not rewritten.

## Full-corpus ingestion

New draft records use filenames such as
`PMC13403371-diabetes-genetic-risk-gwas.pdf`: the matching PMCID plus a reviewed
brief title summary of 1–7 lowercase, hyphen-separated words (PMCID excluded).
The metadata tool validates the format before fetching, but relevance of the
summary requires author review. It derives `id` from the basename without `.pdf`
and emits the same value as `article_id` for existing epic consumers. Keep the
full title, PMCID and pinned PMC version separately. Use this ID in new Q&A,
retrieval metadata and citations; downstream migration is a separate change.
Once referenced, keep IDs stable; rename only with an explicit reference migration.
Existing frozen manifests, Q&A and results retain their recorded identities.

Start the service against a fresh local collection with `SEED_ON_EMPTY=false`.
Download PDFs using the intended manifest, then pass that same manifest and
corpus directory to the ingestion module. For example:

```sh
python -m tools.corpus.download_corpus --manifest data/manifest.json --corpus-dir corpus/combined-v2
python -m tools.corpus.ingest_corpus --manifest data/manifest.json --corpus-dir corpus/combined-v2
```

The current ingestion utility keeps its existing missing-file/error handling;
its return status alone is not proof of complete corpus ingestion. Before an
evaluation, inspect ingestion output and let the benchmark evaluator check actual
collection membership and pinned extracted text. Do not combine seed filenames
with full-corpus filenames in one collection. Licence admission checks and draft
review happen before freezing a manifest; the downloader is not a replacement
for them. Evaluations using paid rewriting/generation need approval for that run.

## Preserved historical tools

`tools/evaluation/historical/` contains the original combined-release builders,
reuse/replay/analysis helpers, topic run helpers and their regression tests.
Their bytes are part of recorded provenance, so they retain their original
imports and path assumptions. Run them through the original-layout runner:

```sh
python -m tools.historical check
python -m tools.historical test
python -m tools.historical verify --corpus-dir /absolute/path/to/corpus/combined-v2
# To inspect a specific archived helper's arguments:
python -m tools.historical script benchmark/combined/build_release.py --help
```

The runner uses the pinned pre-move Git source and verified relocated inputs in
a temporary tree. Archived command examples use that tree's original `benchmark/`
namespace. Use absolute paths for external corpus inputs, fresh stores, receipts
and outputs when invoking a historical script; relative outputs in the temporary
view are removed when it exits. Do not invoke archived files directly at their
new locations or use historical hashes to claim a new run used adapted code.

The original fresh-store helper remains
`tools/evaluation/historical/benchmark/outliers/v1/runs/ingest_isolated.py`;
no duplicate ingestion implementation is introduced. Its cross-topic CLI requires
condition and receipt plus explicit benchmark/corpus paths for other topics.
Its original top-level production imports still require an ingestion environment.
For everyday full-corpus ingestion, use the maintained service ingestion module.
