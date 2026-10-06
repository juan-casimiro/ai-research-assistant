# Original V1 host benchmark

This guide preserves reproduction details for the original **19-article / 133-question**
benchmark. Its 96.4% at n=3 and 98.2% at n=8 are legacy document/category-ranking
scores on 111 scored questions. They are not current V2 evidence-coverage scores,
answer-correctness scores or Docker-demo results.

Use the [host environment setup](../../../README.md#develop-and-evaluate-host), then
configure a separate fresh CHROMA_PATH with SEED_ON_EMPTY=false for this corpus.
Run commands from the repository root. Preserve the archived manifest, gold and
results with their original schemas; do not extend them with new authoring.
Current work starts from the [V2 benchmark guide](../../benchmark/README.md).

In a separate terminal, populate the full corpus. PDFs remain untracked
(see `.gitignore`); per-article license terms are recorded in `data/archive/v1/corpus_manifest.json`.

```bash
python -m tools.corpus.download_corpus --manifest data/archive/v1/corpus_manifest.json
```

The downloader fetches the 17 PMC articles through the public
[PMC AWS dataset](https://pmc.ncbi.nlm.nih.gov/tools/pmcaws/), verifies the
metadata DOI and available MD5 checksum, and validates PDF structure before
saving. It skips readable existing PDFs and removes failed partial downloads.
The manifest pins version 1 for these articles; versions are distinct deposits,
so the downloader does not guess a replacement version when a source fails.

Two articles have no recorded PMC ID and need a browser download. Run
`python -m tools.corpus.download_corpus --manifest data/archive/v1/corpus_manifest.json --open-manual` to open only the missing publisher
pages. On each Ovid page, select **Download PDF**, then the download icon in
the PDF viewer toolbar, and save into `./corpus/` with the exact name below:

| Article page | Save as |
| --- | --- |
| [Resistant hypertension survey](https://www.ovid.com/10.4103/singaporemedj.SMJ-2025-248) | `cardio-hypertension-guidelines.pdf` |
| [GPT-5 / plasma tau 217 study](https://www.ovid.com/10.4103/singaporemedj.SMJ-2025-289) | `outlier-gpt5-tau217-diagnosis.pdf` |

This browser workflow was reported successful in the initial manifest notes on
30 September 2026. On 1 October, both DOI redirects to Ovid were confirmed,
but Ovid returned HTTP 403 to scripted requests; browser verification was
unavailable. No direct automated PDF route has been verified for these two.

Rerun the downloader after saving them. Missing manual files or failed downloads
produce exit status 1; success means all selected files are readable PDFs.
Existing files are checked for readability, not article identity: when saving
manually, check the first-page title against the manifest. Use `--filename NAME`
(repeatable) for selected articles, and `--corpus-dir PATH` for another output
folder. Default paths are rooted at the repository, independent of your current
directory. The CLI uses Python and the existing `pypdf` dependency; no curl,
AWS credentials or additional browser automation dependency is needed.

Ingest everything:

```bash
python -m tools.corpus.reset_collection    # resets the vector store (safe on a fresh clone)
python -m tools.corpus.ingest_corpus --manifest data/archive/v1/corpus_manifest.json  # ingests every PDF listed in the manifest
```

   Expect one `INGESTED` line per file; `SKIP (file not found)` means
   that PDF hasn't been downloaded yet.

## Retrieval evaluation

The commands below use the original 133-case set and the historical host corpus.
They do not run the current five-topic benchmark.

```bash
python -m tools.evaluation.eval_golden [--bm25] [--rewrite]
```

Runs the golden QA evaluation harness (`data/archive/v1/golden_qa.json`, 133 queries,
111 scored across 4 categories plus unanswerable) against the production
`retrieve()` pipeline. The script imports `retrieve()` and
`_load_models_and_index()` from `main.py`, loads the models and existing
Chroma collection in its own process, and does not require a separate
Uvicorn server. The full corpus must already be ingested at the configured
`CHROMA_PATH`; this script does not run startup seeding. Configure the
selected LLM provider as described above (`ANTHROPIC_API_KEY` is required
for the default Anthropic provider). The `--rewrite` option makes LLM
requests and may incur provider usage. Results are written to
`eval_results.json` with a config label and per-query verdicts. See
[V1 methodology](methodology.md) for the category design
and scoring logic.

```bash
python -m tools.evaluation.compare_evals <baseline.json> <experiment.json> --allow-legacy
```

Diffs two result files and prints per-query pass/fail flips, for
isolating the effect of a single change.

Raw per-query results for all four tested configurations are committed
under `data/archive/v1/evaluations/` for inspection: `eval_results_baseline.json`,
`eval_results_bm25.json`, `eval_results_rewrite.json`, and
`eval_results_bm25_rewrite.json`.
