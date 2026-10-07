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
candidate list local; the builder reports and omits unsupported licences.

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
`eligibility` from the article licence evidence: `eligible` for explicit CC BY 4.0
or CC0 1.0, otherwise `excluded`. This field does not represent a wider review.

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

## Assemble or complete the manifest

For a new output, run:

```sh
.venv/bin/python build_corpus_manifest.py --candidates "$corpus_run_dir/candidates.json" \
  --output data/corpus_manifest.json
```

The builder fetches metadata, computes licence eligibility and reports/omits
unsupported or missing licence evidence. It fails without writing a manifest if
none qualify. `eligible` requires the exact licence URL as well as the licence
name; a generic label or claimed status alone is insufficient. Check mandatory
identifiers, bibliography and the complete PubMed abstract before accepting its
output, and download/check one matching readable PDF per included article.

For an existing manifest, skip the builder's creation command: it refuses existing
output. Complete metadata in place without deleting/refetching the whole file.
Recompute eligibility using fetch_article_metadata.licence_eligibility and exclude
unsupported articles; preserve all other scientific values. Existing 55 records
have explicit supported article licence evidence. Their status describes only
that check, not figure/table reuse or public PDF distribution.

Verify unique identifiers/filenames, mandatory metadata, exact licence evidence
and matching readable PDFs. Report included/excluded articles and output paths.
Keep citation, source links and licence notices for attribution; temporary files
remain local; commit only the final corpus manifest, not generated per-run
reports or duplicate manifests. No separate review inventories, receipts or
admission workflow is required for this MVP.

## Sources and checks

Adapted from the epic's [eligibility gates and article record contract](https://github.com/juan-casimiro/ai-research-assistant/blob/6bfed40218fcdf94c4bbc0dbdd44c817760f63dd/docs/benchmark-standards.md#eligibility-gates-and-provenance)
and [JUA-128](https://linear.app/juan-casimiro-agent/issue/JUA-128/add-repository-owned-corpus-management-and-ingestion-skills-for),
with the user's mandatory PMID/PubMed abstract requirements and narrower current
scope: detailed figure/table review is deferred until that material is used.

Use CLI --help to confirm options. Offline helper coverage:

```sh
.venv/bin/python -m unittest tests.corpus.test_download_corpus tests.corpus.test_fetch_article_metadata tests.corpus.test_build_corpus_manifest -v
```

Mocked tests do not certify live acquisition, public reuse of every element in an article. No paid calls or bulk downloads are needed to validate
the skill instructions themselves.
