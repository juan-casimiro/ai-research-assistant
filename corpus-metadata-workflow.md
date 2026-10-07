# Generate corpus metadata and acquire PDFs

Use a supplied PMCID list to create a reviewed, publicly reusable corpus. Run
helpers from the active repository root with its Python environment. This
procedure covers acquisition and admission, not ingestion or benchmark authoring.
The skill routes here; this document owns all process and verification instructions.
Use the active assigned ai-research-assistant checkout/worktree even when skill
discovery points to another checkout. Read its AGENTS.md first and resolve helpers
and outputs from that checkout. Preserve archived V1 data and frozen records.
The existing scripts remain alongside this document.

Accept the PMCID list and any supplied versions, topics and discovery provenance.
Download/ingestion defaults reserve data/corpus_manifest.json for the reviewed
corpus. Use explicit paths for drafts or archived V1 acquisition. The V1 evaluation
helper still reads archived Q&A; its scores do not describe a newly acquired corpus.

## Local run directory

Place all generated intermediate files in `build/corpus/<run-id>/`, ignored by
Git. Choose a unique run ID (for example a UTC timestamp plus a short label) and
create a new directory; preserve earlier runs. Honour an explicit user-selected
output location instead when supplied. Only the verified final manifest is
promoted to `data/corpus_manifest.json` or the user's chosen final path.

```text
build/corpus/<run-id>/
├── candidates.json
├── passed-candidates.json
├── acquisition.json
├── metadata/                 # one <PMCID>.<version>.json per article
├── provenance/               # original provider responses
├── pdfs/
├── text/                     # extracted text
├── reviews/                  # per-article checks and attribution
└── selection-log.json
```

In the commands below, set `corpus_run_dir` to this run's directory:

```sh
corpus_run_dir="build/corpus/<unique-run-id>"
mkdir -p build/corpus
mkdir "$corpus_run_dir"
mkdir "$corpus_run_dir/metadata" "$corpus_run_dir/provenance" \
  "$corpus_run_dir/pdfs" "$corpus_run_dir/text" "$corpus_run_dir/reviews"
```

Replace placeholders before execution. If the run directory already exists,
stop and choose a new ID; resume it only when explicitly continuing that run.
Use the same directory throughout acquisition, review and assembly. Keep durable
review provenance needed by the final manifest in its admitted article records;
do not make a committed manifest depend solely on disposable local files.

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
complete candidate list local, including pending/excluded candidates for the
selection log; create a separate passing-only input after verification.

Fetch per-article metadata into the run directory, retaining source responses:

```sh
.venv/bin/python fetch_article_metadata.py --pmcid <PMCID> --pmc-version <VERSION> \
  --search-query '<actual query or explicit selection provenance>' \
  --filename <PMCID-descriptive-title.pdf> --cluster <TOPIC> \
  --output "$corpus_run_dir/metadata/<PMCID>.<VERSION>.json" \
  --archive-dir "$corpus_run_dir/provenance"
```

The helper cross-checks PMC, ID Converter and PubMed identity and retractions,
preserves PubMed abstract sections, and records metadata URLs/hashes. It leaves
eligibility pending. Its licence summary is evidence, not admission approval.

## Mandatory verification before manifest assembly

Every included article must pass every gate. Missing values, unresolved conflicts
or unavailable evidence fail admission; record them as pending/excluded outside
the eligible manifest. PMID and PubMed abstract have no missing-value exception.

| Gate | Required verification and retained evidence |
| --- | --- |
| Identity | Valid resolved PMCID, positive pinned PMC version, nonempty DOI and numeric PMID; agreement across pinned PMC metadata/JATS, official ID Converter, PubMed and actual PDF. Resolve corrections/discrepancies; reject retractions. |
| Bibliography | Exact nonempty title, complete ordered authors, journal, publication date and date precision. Do not invent missing date components. |
| Abstract | Nonempty complete abstract from the matching PubMed record, including labelled sections. Retain source URL/response hash. Abstract summaries do not substitute for the source abstract. |
| Licence — critical | Exactly CC BY 4.0 or CC0 1.0 for this deposit. Verify authoritative metadata/JATS and article/PDF notices; retain exact URL, notice, evidence locations, check date and reviewer. Unversioned BY, earlier BY, NC, ND, SA, custom/ambiguous terms and unresolved conflicts fail this project's selection policy. |
| Third-party rights | Inspect figures, tables, captions, credit lines, supplements and notices for excluded material. Record inspected locations and resolutions. Unresolved incompatible material fails admission of the complete PDF; do not silently strip it and claim the original PDF passed. |
| Automatic acquisition | Use the supported PMC Cloud metadata/PDF route. Retain pinned metadata/PDF object URLs and available provider checksum. Manual publisher routes, XML-only records or missing PDFs do not qualify. |
| PDF and extraction | Validate actual PDF bytes, nonzero pages, readable text, first-page identity and useful table extraction. Record acquisition UTC time, byte count, SHA-256, parser/version and extraction checks. Extracted text needs its own SHA-256 and tool/version. |
| Attribution and selection | Full citation, identifiers/version, source and exact licence links, copyright/credit/disclaimer notices, modifications, topic/inclusion rationale and reviewer. Verify one attribution entry per admitted article. |

Licence sources: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
permits sharing/adaptation including commercial use subject to attribution,
licence links, change notices and other terms. [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/)
provides a public-domain dedication/waiver; retain attribution as project provenance.
Neither article licence automatically clears separately credited third-party
material or other rights. PMC accessibility alone does not establish reuse rights.
See [PMC acquisition documentation](https://pmc.ncbi.nlm.nih.gov/tools/textmining/).
These are project admission rules; they do not classify every excluded licence as
universally unusable. Publishing PDFs is a separate requested action, not part of
acquisition or skill validation.

## Candidate PDF acquisition and review record

Assemble `$corpus_run_dir/acquisition.json`, a local acquisition envelope, `{"articles": [<draft records>]}`, solely
for the downloader. This is not the final corpus manifest. Download candidates
before the rights/PDF review and before build_corpus_manifest.py:

```sh
.venv/bin/python download_corpus.py --manifest "$corpus_run_dir/acquisition.json" \
  --corpus-dir "$corpus_run_dir/pdfs"
```

The downloader checks identity metadata, available MD5 and PDF structure, but
skips already readable files without checking their identity/hash. Verify reused
files against the review receipt. Its legacy manual fallback never counts as
admission for this PMC-only workflow.

Keep a per-article record in `$corpus_run_dir/reviews/` with all gate decisions, reviewer/date,
metadata source hashes, PDF/text hashes, exact licence evidence and attribution.
Maintain `$corpus_run_dir/selection-log.json` for failed/pending candidates. Only pass records proceed.
Existing data/drafts/corpus_metadata.json
contains 55 freshly fetched **pending**
records; successful downloads did not make them eligible. Review them using these
same gates before inclusion; archived V1 material is not grandfathered in.

## Assemble and publish only passing articles

Create `$corpus_run_dir/passed-candidates.json` containing only articles with completed passing reviews:
pmcid, pmc_version, filename, cluster and search_query. Keep any source provenance.
After all selected articles pass verification, invoke the builder directly with
the final manifest path. There is no separate draft or staged manifest:

```sh
.venv/bin/python build_corpus_manifest.py --candidates "$corpus_run_dir/passed-candidates.json" \
  --output data/corpus_manifest.json
```

The builder validates input and refuses existing output, but emits pending
eligibility. It does not enforce rights or review gates; the workflow must complete
them before invoking it and attach their evidence to the final file afterward.
Compare its records/source hashes to the reviewed metadata; changed source content
requires renewed checks. Do not publish merely because the command succeeded.
Attach the completed rights, third-party, acquisition, validation, attribution and
review evidence to admitted records and mark them eligible only after the checks.
Finish the manifest at the user-selected final path (normally
`data/corpus_manifest.json`); every member must have all mandatory values and a
matching passing review. Do not treat the file as ready until these post-build
checks and evidence attachment succeed. If refreshed sources invalidate a review,
stop and report the incomplete file; do not commit it as an eligible manifest. Pending/excluded articles belong only in the selection
log or drafts. Never overwrite frozen manifests or archived evidence implicitly.

Verify unique PMCIDs/IDs/filenames, candidate-to-review-to-manifest joins, exact
PDF directory membership and hashes, attribution completeness and zero unreviewed
members. Report admitted/excluded/pending counts, output and evidence locations, checks
and remaining limitations. Keep
PDFs, extracted text and raw acquisition artifacts untracked. Helper/schema
changes are separate implementation work; this skill does not pretend those
checks are automated by the current builder.

## Sources and checks

Adapted from the epic's [eligibility gates and article record contract](https://github.com/juan-casimiro/ai-research-assistant/blob/6bfed40218fcdf94c4bbc0dbdd44c817760f63dd/docs/benchmark-standards.md#eligibility-gates-and-provenance)
and [JUA-128](https://linear.app/juan-casimiro-agent/issue/JUA-128/add-repository-owned-corpus-management-and-ingestion-skills-for),
with the user's stricter mandatory PMID and PubMed abstract requirement.

Use CLI --help to confirm options. Offline helper coverage:

```sh
.venv/bin/python -m unittest tests.corpus.test_download_corpus tests.corpus.test_fetch_article_metadata tests.corpus.test_build_corpus_manifest -v
```

Mocked tests do not certify live acquisition, legal eligibility or the review of
any particular article. No paid calls or bulk downloads are needed to validate
the skill instructions themselves.
