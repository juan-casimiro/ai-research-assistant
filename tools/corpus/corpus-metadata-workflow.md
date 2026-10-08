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

## Local run directory and original selection

Create a new ignored `build/corpus/<run-id>/` directory. Metadata records go in
`metadata/`, retained source responses in `provenance/`, PDFs in `pdfs/`, and
text/cache diagnostics in `extracted_text/`. The prepared manifest stays at
`$corpus_run_dir/corpus_manifest.json`; only successful publication installs it
at `data/corpus_manifest.json` (or the chosen final destination).

```sh
corpus_run_dir="build/corpus/<unique-run-id>"
mkdir -p "$corpus_run_dir/metadata" "$corpus_run_dir/provenance" "$corpus_run_dir/pdfs"
```

**Before any network call**, save the exact supplied PMCID list as
`$corpus_run_dir/candidates.json`. Keep this name for compatibility, but it is
now the original selection, not fetched candidate metadata. For example:

```json
{"articles": [{"pmcid": "PMC123456"}]}
```

Only add `cluster` and `search_query` when the user supplied them; preserve their
values verbatim. Do not fill this file from fetch results, add resolved versions
or proposed filenames, or remove failed PMCIDs. A user-requested explicit version
is passed to fetch with `--pmc-version`. Publication compares **PMCID sets only**
and names missing/extra PMCIDs. Changing the selection requires the user's
choice, not an automatic response to failed acquisition.

## Fetch, then review naming and topic

Without `--pmc-version`, the helper resolves the uniquely current/latest deposit
from the official ID Converter response, then pins that version for PMC Cloud
metadata and PDFs. It never assumes version 1 or guesses when resolution is
ambiguous. Retain the converter response and its hash as evidence of what latest
meant during this run. Explicit `--pmc-version <VERSION>` still works and is not
replaced by the current version. Downloader always uses the manifest's pinned
version and never re-resolves latest.

```sh
.venv/bin/python -m tools.corpus.fetch_article_metadata \
  --pmcid <PMCID> --selection-file "$corpus_run_dir/candidates.json" \
  --output "$corpus_run_dir/metadata/<PMCID>.json" \
  --archive-dir "$corpus_run_dir/provenance"
```

The helper looks up and validates PMC/ID Converter/PubMed identity, bibliography,
complete PubMed abstract, retractions and article licence evidence. It preserves
supplied cluster/query inputs. When discovery history is unavailable, the record
says `User supplied PMCID; original discovery query unavailable` rather than
inventing it. Failure returns nonzero; the original selection file stays intact.

After fetching, the helper proposes a filename from the title (PMCID plus the
first 1–7 lowercase alphanumeric words) and assigns matching `id`/`article_id`.
**Review the proposal against the title and abstract**: intervention, population
and study type should be clear. Assign a cluster from those sources if the user
did not supply one. Do not guess a cluster before lookup. Review/update the saved
record offline using the same helper, with no refetch:

```sh
.venv/bin/python -m tools.corpus.fetch_article_metadata \
  --review-record "$corpus_run_dir/metadata/<PMCID>.json" \
  --filename <PMCID-reviewed-title.pdf> --cluster <REVIEWED_TOPIC>
```

`--filename` can be omitted to accept the proposed name. `--cluster` can be
omitted only when a valid supplied cluster is already present. The command
updates IDs to match the reviewed filename. Naming/cluster checks belong to
complete-record validation before assembly; core fetched metadata is validated
without requiring those pre-lookup decisions. Missing/invalid filenames, IDs,
clusters or selection provenance prevent assembly output.

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
  --records-dir "$corpus_run_dir/metadata" --output "$corpus_run_dir/corpus_manifest.json"
.venv/bin/python -m tools.corpus.download_corpus \
  --manifest "$corpus_run_dir/corpus_manifest.json" --corpus-dir "$corpus_run_dir/pdfs"
.venv/bin/python -m tools.corpus.extract_corpus_text \
  --manifest "$corpus_run_dir/corpus_manifest.json" --corpus-dir "$corpus_run_dir/pdfs" \
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
  --finalize "$corpus_run_dir/corpus_manifest.json"
```

Validation preserves scientific metadata and IDs and writes atomically only after
all records pass. Extraction provenance is removed from the manifest; it belongs
in the local index. The downloader checks supplied PDF SHA-256 before skipping
existing files and before atomically replacing them. Archived V1 manifests without
hashes retain their original structural-check compatibility. For reused local
PDFs, just run extraction; no new download is required.

## Publication is the final gate

Prepare every artifact under `build/corpus/<run-id>/` first. Keep the supplied
selection in `candidates.json`; publication compares its PMCID
membership with the prepared manifest, so missing metadata cannot silently reduce
the corpus. Publication lists each missing and extra PMCID; versions and filenames
are fetch outputs and do not participate in selection comparison. Only after metadata, PDF checksums and extraction all pass, run:

```sh
.venv/bin/python -m tools.corpus.publish_corpus --run-dir "$corpus_run_dir" \
  --manifest-destination data/corpus_manifest.json --pdf-destination corpus/mvp
```

Use `--check` to validate without moving final artifacts. Publication revalidates
metadata, pinned PDF sources/checksums and the extraction cache. It aborts on
any failure or destination conflict before moving artifacts. Existing final
files are accepted only when manifest contents and PDF membership/hashes match;
there is no overwrite/force option. After success the manifest and PDFs live
outside build, and preparation originals are removed. Text/cache diagnostics stay
local under the run directory. To reuse that cache afterward, supply
`--corpus-dir corpus/mvp` to the extraction helper.

On failure, read local `publication_report.json` and `extraction_report.json`.
**Stop and prompt the user**, listing each PMCID/file, reason and affected
existing destination. Ask whether to resolve conflicting files or remove/replace
PMCIDs. Do not change selection, delete final files, overwrite conflicts or
retry publication until the user resolves the choice. If selection changes,
update candidates/metadata, rebuild the prepared manifest and rerun validation.
Keep final destinations intact while validation is incomplete. PDF promotion is
staged; a manifest-write failure rolls back newly installed PDFs. No downloaded
PDFs or local reports are committed.

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
