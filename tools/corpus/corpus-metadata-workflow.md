# Local corpus metadata workflow

Run these modules from the repository root. Prepare the whole selection under
ignored `build/corpus/<run-id>/`; do not publish a reduced selection after a
failed fetch. No ingestion or retrieval changes are part of this workflow.

## 1. Save selection

Save `candidates.json` before fetching, containing the supplied PMCIDs, clusters
and discovery queries (or explicit selection provenance):

```json
{"articles": [{"pmcid": "PMC123456", "cluster": "test-topic", "search_query": "User selected PMCID; original query unavailable"}]}
```

Use each actual selected PMCID. Optional `filename` supplies a reviewed basename
with PMCID plus 1–7 lowercase hyphen-separated words and `.pdf`; optional
`pmc_version` pins a deposit. Otherwise fetch selects the latest PMC version.

## 2. Fetch and assemble

```sh
corpus_run_dir=build/corpus/<run-id>
python -m tools.corpus.fetch_article_metadata \
  --selection-file "$corpus_run_dir/candidates.json" \
  --records-dir "$corpus_run_dir/metadata" \
  --archive-dir "$corpus_run_dir/provenance"
python -m tools.corpus.build_corpus_manifest \
  --records-dir "$corpus_run_dir/metadata"
```

Fetch loops over the selection and prints each proposed filename. Correct a
filename in `candidates.json`, then rerun the fetch command with
`--pmcid <PMCID>` before assembly. Repeat `--pmcid` to correct several articles
without refetching others. Assembly rebuilds the prepared manifest in place.
Cluster always comes from the selection.
Fetch, assembly and publication use the same complete-record validator.

Every record requires PMCID, pinned PMC version, PMID, DOI, title, authors,
journal, publication date/year, PubMed abstract and identity URL, consistent
filename/IDs, cluster and selection provenance. Only the existing
`licence_eligibility` rules for CC BY 4.0 and CC0 1.0 are accepted. Raw responses
remain under `provenance/`; per-source SHA-256 values stay in the manifest.

## 3. Download

```sh
python -m tools.corpus.download_corpus \
  --manifest "$corpus_run_dir/corpus_manifest.json" \
  --corpus-dir "$corpus_run_dir/pdfs"
```

Downloads use the manifest's pinned version and verify provider MD5 and any
pinned PDF SHA-256. A missing or failed article returns nonzero; resolve it
before continuing.

## 4. Extract

```sh
python -m tools.corpus.extract_corpus_text \
  --manifest "$corpus_run_dir/corpus_manifest.json" \
  --corpus-dir "$corpus_run_dir/pdfs"
```

Every run extracts every PDF through `tools/corpus/pdf_text.py`. Text is written
beside each PDF as `<article-id>.txt`, matching ingestion. The small
`pdfs/extraction_report.json` records pass/fail and names failed PMCIDs/reasons.
Empty text, parser failures and pages without text block admission. The sole
approved exception remains PMC12003177 version 1 with its exact PDF SHA-256;
its reporting-summary pages are not searchable. No OCR or replacement exception
is implied.

## 5. Publish locally

```sh
python -m tools.corpus.publish_corpus --run-dir "$corpus_run_dir" --check
python -m tools.corpus.publish_corpus --run-dir "$corpus_run_dir"
```

Publication validates every record and PDF again, computes PDF SHA-256 directly,
compares the manifest PMCID set with the saved selection, and checks all final
destinations before moving anything. Defaults are `data/corpus_manifest.json`
and `corpus/mvp/`, with both PDFs and adjacent text. Missing/extra PMCIDs and
conflicting files are named. Only expected PDF/text files are compared; unrelated
files are ignored, and matching text left by ingestion is accepted.

Different existing content aborts without overwrite. Resolve each named conflict
with the user. The prepared manifest and selection remain for reruns. A failed
move can be resumed by running publication again; successfully moved files are
validated at their destination. A rerun after success also exits zero. There is
no staging directory, rollback or concurrent-modification detection.

Do not commit PDFs or generated preparation artifacts. Publication and real
network acquisition require the task's authorization. Offline verification:

```sh
python -m unittest discover -s tests -t . -v
```
