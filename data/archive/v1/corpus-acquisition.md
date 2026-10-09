# Original V1 corpus acquisition record

Moved from the README host guide on 2026-10-09; superseded by the current benchmark.
Run historical commands from the repository root.

Start the server:

```bash
uvicorn main:app --reload
```

In a separate terminal, populate the full corpus. PDFs remain untracked
(see `.gitignore`); per-article license terms are recorded in [corpus_manifest.json](corpus_manifest.json).

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
folder. Default paths are relative to the script, independent of your current
directory. The CLI uses Python and the existing `pypdf` dependency; no curl,
AWS credentials or additional browser automation dependency is needed.

Ingest everything:

```bash
python reset_collection.py    # resets the vector store (safe on a fresh clone)
python ingest_corpus.py --manifest data/archive/v1/corpus_manifest.json # original V1 corpus
```

   Expect one `INGESTED` line per file; `SKIP (file not found)` means
   that PDF hasn't been downloaded yet.

