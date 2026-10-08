# Local corpus metadata workflow

Run these modules from the active repository root with its Python environment.
Choose the flow from the supplied input and state it before execution:

- **PMCID list:** fetch metadata, generate a draft manifest, download PDFs, verify
  and extract, then publish only after every selected article passes.
- **Existing manifest:** validate metadata, download missing PDFs, verify and
  generate adjacent `.txt` files. Preserve the manifest, versions and IDs; skip
  metadata fetching, assembly and publication.

If the user says the corpus is already generated, use `data/corpus_manifest.json`
when present. Report missing or ambiguous inputs rather than generating a new
selection. No ingestion or retrieval changes are part of either flow.

## Existing manifest

Set the supplied manifest and PDF directory; defaults for the current corpus are:

```sh
corpus_manifest=data/corpus_manifest.json
corpus_pdf_dir=corpus/mvp
```

Validate the entire manifest offline before acquisition, without rewriting it:

```sh
python - "$corpus_manifest" <<'PYTHON'
import json
import sys
from pathlib import Path
from tools.corpus.fetch_article_metadata import validate_records

articles = validate_records(json.loads(Path(sys.argv[1]).read_text())["articles"])
print(f"Validated {len(articles)} articles")
PYTHON
```

A validation failure stops this flow; report the reason without refetching or
repairing metadata. Continue at **3. Download**, then perform mandatory PDF
verification and **4. Extract**. Completion requires every manifest article to
pass and `extraction_report.json` to report `complete: true`. Keep the existing
manifest unchanged; do not run **5. Publish**.

## PMCID list

Prepare the whole supplied selection under a new ignored
`build/corpus/<run-id>/`; preserve earlier runs. Do not publish a reduced
selection after a failed fetch.

## 1. Save selection

Save `candidates.json` before fetching, containing the supplied PMCIDs and any
supplied reference fields:

```json
{"articles": [{"pmcid": "PMC123456", "cluster": "test-topic", "search_query": "User selected PMCID; original query unavailable"}]}
```

Use each actual selected PMCID. Optional `filename` supplies a reviewed basename
with PMCID plus 1–7 lowercase hyphen-separated words and `.pdf`; optional
`pmc_version` pins a deposit. Otherwise fetch selects the latest PMC version.

## 2. Fetch and generate a draft manifest

```sh
corpus_run_dir=build/corpus/<run-id>
corpus_manifest="$corpus_run_dir/corpus_manifest.json"
corpus_pdf_dir="$corpus_run_dir/pdfs"
python -m tools.corpus.fetch_article_metadata \
  --selection-file "$corpus_run_dir/candidates.json" \
  --records-dir "$corpus_run_dir/metadata" \
  --archive-dir "$corpus_run_dir/provenance"
python -m tools.corpus.build_corpus_manifest \
  --records-dir "$corpus_run_dir/metadata"
```

Fetch loops over the selection and prints each proposed filename. Correct a
filename in `candidates.json`, then rerun the fetch command with
`--pmcid <PMCID>` before draft assembly. Repeat `--pmcid` to correct several articles
without refetching others. Assembly rebuilds the draft manifest in place at
`build/corpus/<run-id>/corpus_manifest.json`. This draft drives acquisition; it
is not the reviewed final corpus manifest.
`cluster`, `selection_rationale` and `search_query` are reference fields and
non-critical; missing or empty values never block fetch, assembly or publication.

- `cluster`: after fetching, assign a high-level grouping from the abstract,
  reusing an existing value where one fits. Set it in the article's record under
  `metadata/` and in `candidates.json`, then assemble.
- `selection_rationale`: take it from the user's request or ask once; otherwise
  leave it blank. Do not invent one.
- `search_query`: record a discovery query only when one was supplied. Fetch
  retains its explicit user-selection fallback when no query is supplied.

Assembly preserves editorial fields; they do not affect ingestion.
Optional `topic_rationale` describes topic assignment and is preserved on refetch
unless the selection supplies a replacement.
Fetch, assembly and publication use the same complete-record validator.

Every record requires PMCID, pinned PMC version, PMID, DOI, title, authors,
journal, publication date/year, PubMed abstract and identity URL, consistent
filename/IDs. Only the existing
`licence_eligibility` rules for CC BY 4.0 and CC0 1.0 are accepted. Raw responses
remain under `provenance/`; per-source SHA-256 values stay in the manifest.

## 3. Download (both flows)

```sh
python -m tools.corpus.download_corpus \
  --manifest "$corpus_manifest" \
  --corpus-dir "$corpus_pdf_dir"
```

Before downloading, inspect existing selected PDF paths. Report invalid PDFs,
recorded-hash mismatches or conflicting paths and stop rather than allowing the
downloader to replace them. Valid PDFs are skipped; when no SHA-256 is recorded,
verify them against the available provider checksum before accepting reuse.

Downloads use the manifest's pinned version and verify provider MD5 and any
pinned PDF SHA-256. A missing or failed article returns nonzero; resolve it
before continuing.

## Mandatory verification before final admission

Before final admission, verify every selected article against its actual local
PDF: first-page identity must agree with the pinned metadata, article/PDF licence
notices must support CC BY 4.0 or CC0 1.0 without unresolved conflicts, and the
PDF must have nonzero pages and readable article text. Retain the evidence under
the run directory for the PMCID-list flow, or an ignored review directory under
`build/corpus/` for the existing-manifest flow. Then run extraction below.

Any failed check, unavailable evidence or unresolved conflict leaves the run
incomplete and prevents publication of the reviewed final manifest. Report each
affected PMCID and reason; do not silently reduce the selection or apply recovery
workarounds.

## 4. Extract (both flows)

```sh
python -m tools.corpus.extract_corpus_text \
  --manifest "$corpus_manifest" \
  --corpus-dir "$corpus_pdf_dir"
```

Every run extracts every PDF through `tools/corpus/pdf_text.py`. Text is written
beside each PDF as `<article-id>.txt`, matching ingestion. The small
`$corpus_pdf_dir/extraction_report.json` records pass/fail and names failed
PMCIDs/reasons.
Empty text, parser failures and pages without text block admission. The sole
approved exception remains PMC12003177 version 1 with its exact PDF SHA-256;
its reporting-summary pages are not searchable. No OCR or replacement exception
is implied.

## 5. Publish the reviewed final manifest locally (PMCID list only)

Confirm that metadata, PDF identity/licence verification and extraction passed
for every supplied PMCID before running publication. A successful automated
`--check` does not replace the identity/licence review above. Only after all gates
pass may the draft be published as `data/corpus_manifest.json`.

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
