# Generate corpus metadata and acquire PDFs

Use a supplied PMCID list to generate article metadata and acquire PDFs locally. Run
helpers from the active repository root with its Python environment. This
procedure covers acquisition and admission, not ingestion or benchmark authoring.
The skill routes here; this document owns all process and verification instructions.
Use the active assigned ai-research-assistant checkout/worktree even when skill
discovery points to another checkout. Read its AGENTS.md first and resolve helpers
and outputs from that checkout. Preserve archived V1 data and frozen records.
The existing scripts remain alongside this document.

This workflow currently covers
metadata and article text, not figure/table reuse or public PDF distribution.

Accept the PMCID list and any supplied versions, topics and discovery provenance.
Download/ingestion defaults reserve data/corpus_manifest.json for the reviewed
corpus. Use explicit paths for drafts or archived V1 acquisition. The V1 evaluation
helper still reads archived Q&A; its scores do not describe a newly acquired corpus.

## Local run directory

Use a new ignored `build/corpus/<run-id>/` directory for candidates.json,
per-article JSON in metadata/, source responses in provenance/ and PDFs in pdfs/.
Create the directories before running helpers. Preserve earlier runs. The final
manifest goes directly to `data/corpus_manifest.json` or the user's chosen path.

```sh
corpus_run_dir="build/corpus/<unique-run-id>"
mkdir -p build/corpus
mkdir "$corpus_run_dir"
mkdir "$corpus_run_dir/metadata" "$corpus_run_dir/provenance" "$corpus_run_dir/pdfs"
```

## Article metadata

Resolve each PMCID to the actual article and explicitly choose its PMC deposit
version. Do not silently assume version 1 or latest. Preserve supplied discovery
queries verbatim; if only PMCIDs were supplied, record that selection source and
that the original query is unavailable rather than inventing search history.
The helper's required search-query argument can contain this explicit provenance
statement. Derive a reviewed descriptive filename: PMCID plus 1–7 lowercase
hyphen-separated words and .pdf. Check the title, intervention, population and
study type; inherited filenames are not authoritative. IDs match the basename.

Generate a local candidate file from the supplied PMCID list, normally
`build/corpus/<run-id>/candidates.json`. For each article include `pmcid`, explicitly
resolved `pmc_version`, title-reviewed `filename`, `cluster` and `search_query`
(actual discovery query or explicit selection provenance). The top-level object
contains an `articles` array and optional `source` provenance. Do not copy an
existing list unless the user requested that selection. This file is generated
by the skill and remains untracked; it is not a committed corpus input.

For example, after resolving these fields, an entry has this shape:

```json
{
  "articles": [
    {
      "pmcid": "PMC123456",
      "pmc_version": 2,
      "filename": "PMC123456-descriptive-study-title.pdf",
      "cluster": "selected-topic",
      "search_query": "User supplied PMCID; original discovery query unavailable"
    }
  ]
}
```

The values above are illustrative, not verified article metadata. Keep the
candidate list local; unsupported licences fail metadata validation.

Fetch per-article metadata into the run directory, retaining source responses:

```sh
.venv/bin/python -m tools.corpus.fetch_article_metadata --pmcid <PMCID> --pmc-version <VERSION> \
  --search-query '<actual query or explicit selection provenance>' \
  --filename <PMCID-descriptive-title.pdf> --cluster <TOPIC> \
  --output "$corpus_run_dir/metadata/<PMCID>.<VERSION>.json" \
  --archive-dir "$corpus_run_dir/provenance"
```

The helper cross-checks PMC, ID Converter and PubMed identity and retractions,
preserves PubMed abstract sections, and records metadata URLs/hashes. It leaves
`eligibility` from the article licence evidence: `eligible` for explicit CC BY 4.0
or CC0 1.0. Missing mandatory fields or unsupported licences fail before a record
is written. This field does not represent extraction success.

## Mandatory verification before manifest assembly

Every included article must pass every gate. Missing values, unresolved conflicts
or unavailable evidence prevent inclusion. Report excluded articles and reasons. PMID and PubMed abstract have no missing-value exception.

| Gate | Required verification and retained evidence |
| --- | --- |
| Identity | Valid resolved PMCID, positive pinned PMC version, nonempty DOI and numeric PMID; agreement across pinned PMC metadata/JATS, official ID Converter, PubMed and actual PDF. Resolve corrections/discrepancies; reject retractions. |
| Bibliography | Exact nonempty title, complete ordered authors, journal, publication date and date precision. Do not invent missing date components. |
| Abstract | Nonempty complete abstract from the matching PubMed record, including labelled sections. Retain source URL/response hash. Abstract summaries do not substitute for the source abstract. |
| Licence — critical | Exactly CC BY 4.0 or CC0 1.0 for this deposit. Verify authoritative metadata/JATS and article/PDF notices; retain the exact licence URL and article notice. Unversioned BY, earlier BY, NC, ND, SA, custom/ambiguous terms and unresolved conflicts fail this project's selection policy. |
| Automatic acquisition | Use the supported PMC Cloud metadata/PDF route. Retain pinned metadata/PDF object URLs and available provider checksum. Manual publisher routes, XML-only records or missing PDFs do not qualify. |
| PDF and extraction | Validate actual PDF bytes, nonzero pages, readable article text and first-page identity. Check the actual local file rather than relying only on an HTTP success or PDF header. |

Licence sources: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
permits sharing/adaptation including commercial use subject to attribution,
licence links, change notices and other terms. [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/)
provides a public-domain dedication/waiver; retain attribution as project provenance.
PMC accessibility alone does not establish reuse rights. Detailed figure/table
credit inventories are not required for this current workflow. If public PDF
distribution or figure/table reuse is later requested, verify separately credited
material and any licence exclusions before that use. Do not treat article-level
licence verification as clearance of every element in the complete PDF.
See [PMC acquisition documentation](https://pmc.ncbi.nlm.nih.gov/tools/textmining/).
These are project admission rules; they do not classify every excluded licence as
universally unusable. Publishing PDFs is a separate requested action, not part of
acquisition or skill validation.

## Assemble metadata, download, then extract

The scripts have separate jobs: fetch validates metadata; build assembles existing
records; download verifies PDF checksums; extract manages the local text cache.
The builder never fetches metadata, downloads PDFs or extracts text. For a new
manifest, after fetching one record for every selected PMCID:

```sh
.venv/bin/python -m tools.corpus.build_corpus_manifest \
  --records-dir "$corpus_run_dir/metadata" --output data/corpus_manifest.json
.venv/bin/python -m tools.corpus.download_corpus \
  --manifest data/corpus_manifest.json --corpus-dir "$corpus_run_dir/pdfs"
.venv/bin/python -m tools.corpus.extract_corpus_text \
  --manifest data/corpus_manifest.json --corpus-dir "$corpus_run_dir/pdfs" \
  --cache-dir "$corpus_run_dir/extracted_text"
```

Before assembly, compare the metadata record membership with the supplied PMCID
list: a missing record must not quietly reduce the selected corpus. Metadata
fetch failures require replacement and a nonzero result; do not call preparation
complete while selected articles are missing. Assembly reports selected/included/
excluded counts and reasons; invalid records prevent any output. It validates
identity, bibliography, PubMed abstract, filename/IDs and licence evidence.
Creation refuses an existing output. To validate an existing manifest offline:

```sh
.venv/bin/python -m tools.corpus.build_corpus_manifest \
  --finalize data/corpus_manifest.json
```

Validation preserves scientific metadata and IDs and writes atomically only after
all records pass. Extraction provenance is removed from the manifest; it belongs
in the local index. The downloader checks supplied PDF SHA-256 before skipping
existing files and before atomically replacing them. Archived V1 manifests without
hashes retain their original structural-check compatibility. For reused local
PDFs, just run extraction; no new download is required.

## Text cache and failure policy

Extraction uses only pypdf, exactly as production ingestion:
`PdfReader(str(pdf_path))`, `page.extract_text() or ""`, and a single `"\n"`
between pages. Hash the UTF-8 bytes without trimming or adding a final newline.
The small shared extraction function prevents preparation/ingestion drift;
ingestion otherwise keeps its previous behavior. **Ingestion cache consumption
is a later integration step**; ingestion does not yet read this cache.

Local outputs are:

```text
build/corpus/<run-id>/
  pdfs/
  extracted_text/
    <article-id>.txt
    index.json
    extraction_report.json
```

`index.json` contains `schema_version` and successful article entries with
`source_id`, `pdf_sha256`, relative `text_file`, `text_sha256`, and extractor
`tool`, `version`, `method`. Diagnostics belong only in
`extraction_report.json`: PMCID/deposit, missing-text pages, failures, accepted
exception and limitation, plus corpus completeness. All outputs stay ignored.
Do not commit PDFs, text, index, reports or raw acquisition responses.

Reuse requires verified local PDF and text hashes and the same extractor version
and method. A changed/corrupt text file, changed PDF or stale entry is not reused.
A current failure removes the prior cache entry/text so previous success cannot
conceal it. Successful articles may be cached during an incomplete run; the
report marks the corpus incomplete and the command returns nonzero.

Parsing/extraction errors, empty document text, missing PDFs, mismatched recorded
PDF hashes or any page without text fail that article. Report its PMCID and
reason as **requiring replacement**; publish no reusable text for it. Do not
perform OCR, change extractors or attempt text recovery. Replacement selection
and other PDF-processing changes are separate work.

The sole user-approved exception is **PMC12003177, version 1**, PDF SHA-256
`d977b0dc0b6e1642cdf840e3980a7049b2705efea8c3673b1966228426b00747`.
Accept its pypdf output as-is. Pages 22–24 are reporting-summary forms without
extracted text and are not searchable. Record actual missing pages and this
limitation in the extraction report, not the manifest/index. No workaround is
applied. The exception cannot apply to another deposit or PDF. Revisit it at the
next corpus expansion and remove the special case when the article is replaced
or excluded.

## Verification

Check selection membership, mandatory metadata and exact licence evidence, PDF
identity/checksums and a complete extraction report. Preserve attribution, source
links and article licence notices. This workflow covers metadata and article text,
not figure/table reuse or public PDF distribution.

```sh
.venv/bin/python -m unittest discover -s tests -t . -v
```

Tests mock acquisition and do not establish live availability. No paid evaluations
are needed. The article metadata contract was adapted from the epic's
[benchmark standards](https://github.com/juan-casimiro/ai-research-assistant/blob/6bfed40218fcdf94c4bbc0dbdd44c817760f63dd/docs/benchmark-standards.md),
with mandatory PMID/PubMed abstracts and the user's narrower MVP scope.
