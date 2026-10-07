# JUA-116 — fresh corpus acquisition and review

Direct execution of the repository generate-corpus-metadata skill and corpus-metadata-workflow.md for the 55 PMCIDs supplied in this chat. All article metadata, PDFs and supplements were fetched afresh. The existing candidate file supplied only version pins and preserved discovery queries; existing drafts, downloaded PDFs and epic eligibility approvals were not reused.

## Result

- **43 admitted**, **0 definitively excluded**, **12 pending** outside the final manifest. Pending is an unresolved gate, not an eligibility approval.
- [manifest.json](manifest.json): passing-only manifest with complete DOI, PMID, ordered bibliography, exact full PubMed abstracts, attribution and inline gate evidence.
- [selection-log.json](selection-log.json): all pending cases, unresolved gate and required follow-up.
- [reviews/](reviews/): 55 separate fresh review records, including the pending metadata.
- [filename-review.json](filename-review.json): all 55 titles, reviewed descriptive names, unchanged PDF hashes and original-to-new filename mapping.
- [source-reverification.json](source-reverification.json): the final builder refresh compared against the reviewed source responses.
- [verification.json](verification.json): joins, exact PDF membership/checksums, abstracts, attribution, tests and preservation receipts.

The existing data/corpus_manifest.json and earlier review/draft evidence are preserved. This new manifest has its own explicit path; default ingestion still points at the existing file. No ingestion or benchmark evaluation was run.

## Local acquisition evidence

All generated raw artifacts are ignored by Git under `build/corpus/jua-116-fresh-20261007T221623Z/`:

- `pdfs/`: all 55 freshly acquired candidate PDFs with reviewed names.
- `eligible-pdfs/`: exactly the 43 admitted PDFs, byte-identical copies of the reviewed originals.
- `sources/` and `assembly-sources/`: pinned PMC Cloud metadata/JATS, official ID Converter and complete PubMed XML responses.
- `text/`, `analysis/`, `renders/`: two text extraction tools, table/identity checks and rendered main-PDF contact sheets.
- `supplements/`, `supplement-inspection/`: 108 freshly fetched supplement objects, recursive content inspection and rendered supplement sheets.
- `corrections/`: fresh correction records for the two unresolved correction cases.
- `download-receipts.json`, `supplement-receipts.json`, `filename-review-receipts.json`: timestamps where recorded, sizes, provider MD5, SHA-256 and naming evidence.
- `run-relocation.json`: the unique fresh run was moved to the workflow-required build/corpus location. It maps the original receipt prefix to the current location; no pre-existing run was moved.
- `inspection-recipes/`: temporary acquisition/inspection scripts and test/assembly logs retained locally.

PDFs, extracted text, renders, supplements and provider responses are not committed. The durable manifest/reviews retain the notices, source URLs/hashes and decisions needed to understand admission without relying solely on local raw artifacts.

## Pending cases

| PMCID | Gate | Unresolved evidence |
| --- | --- | --- |
| [PMC10188109](reviews/PMC10188109.json) | third party rights | Supplement/source-data review incomplete: two actual TIFF members in the fresh source-data ZIPs cannot be decoded (Figure 2-source data/Unlabelled/2A GAPDH.tif; Figure 5-figure supplement 1-source data/Unlabelled/A phospho-PKR-high exposure_3.tif). The source-data gallery has not been fully visually cleared. macOS resource forks are not counted as article failures. |
| [PMC10802081](reviews/PMC10802081.json) | licence | Pinned PDF has only a Sage journals-permissions notice, with no CC BY 4.0 notice or licence annotation link. JATS specifies CC BY 4.0; coverage of the actual PDF remains unresolved. |
| [PMC11047104](reviews/PMC11047104.json) | identity | Correction PMC12704798 (2025-12-09) changes antisense ddPCR probe sequences in SI Appendix Table S2. Reconciliation of the freshly downloaded pinned supplement with that corrected appendix is unresolved; no retraction was found. |
| [PMC11527445](reviews/PMC11527445.json) | identity | Correction PMC11645136 (2024-12-16) adds a patent/conflict disclosure; correction PMC13132388 (2026-05-01) relabels four C9 ALS iPSC/iMN groups in SI Figure 3C. Corrected PDF/supplement versus pinned objects has not been reconciled; no retraction was found. |
| [PMC11847805](reviews/PMC11847805.json) | third party rights | Acknowledgments explicitly say Figure by figdraw. Figure-specific publication and downstream reuse rights were not established by the article CC BY notice. |
| [PMC12003177](reviews/PMC12003177.json) | third party rights | Supplementary Information contains a Volta Medical clinical investigation plan with CONFIDENTIAL watermarks and proprietary/confidential notices. Article CC BY 4.0 does not resolve these conflicting supplement terms. |
| [PMC12823827](reviews/PMC12823827.json) | third party rights | Figures 7–8 include MRI/Grad-CAM images from an augmented Kaggle dataset derived from OASIS. The exact image licence/authorization chain has not been established. The source dataset version and exact image licence/authorization chain remain unresolved; official OASIS restrictions must not be assumed to apply identically to every dataset version. |
| [PMC13175446](reviews/PMC13175446.json) | third party rights | The supplement reproduces the separately credited CONSORT-EHEALTH V1.6.1 Google submission/publication form. Its cited 2011 source is CC BY 2.0, but coverage of this specific later form and complete required third-party licence attribution have not been established. Do not infer clearance of the form solely from the 2026 article licence. |
| [PMC13311226](reviews/PMC13311226.json) | licence | First-page notice specifies CC BY 4.0, while subsequent PDF footers say For non-profit purposes. These conflicting notices require publisher clarification before admission. |
| [PMC13433218](reviews/PMC13433218.json) | third party rights | Acknowledgments explicitly say Figures were created with BioRender.com. No required figure-specific BioRender publication-licence/figure URL evidence is supplied; compatible downstream reuse has not been verified. |
| [PMC9239676](reviews/PMC9239676.json) | third party rights | The STROBE checklist supplement reproduces separately authored reporting recommendations. The official STROBE site asks users to contact the authors for republication. Independent downstream permission/licence coverage for the exact checklist remains unresolved; article accessibility does not clear it. |

| [PMC10765819](reviews/PMC10765819.json) | third party rights | Supplementary Table S1 reproduces the separately authored STROBE-MR checklist and cites the 2021 JAMA statement. The official checklist page labels downloads open-access but does not establish exact licence/attribution coverage for this completed XLSX version; a separately hosted fillable checklist is marked CC BY 3.0. Exact compatible third-party coverage is unresolved under the project selection policy. |

These records are neither in the passing-only builder input nor in the final eligible manifest. No pages or figures were stripped to obtain admission. No retraction or metadata-acquisition failure was found.

For the separately credited checklist cases, the 2011 [CONSORT-EHEALTH source](https://www.jmir.org/2011/4/e126/) specifies CC BY 2.0 and the [STROBE site](https://www.strobe-statement.org/) asks authors to be contacted for republication. These do not independently establish exact coverage of the later forms bundled here. The [STROBE-MR site](https://www.strobe-mr.org/) likewise labels its checklist downloads open-access, without resolving the exact reuse terms of the completed XLSX version. The PRISMA 2020 checklist in PMC13423648 was separately cleared under [the official CC BY 4.0 notice](https://www.prisma-statement.org/prisma-2020-checklist); its existing Page et al. source credit and DOI are retained in attribution. [BioRender guidance](https://help.biorender.com/hc/en-gb/articles/21283116932765-CC-BY-publishing-and-reader-permissions) requires a publication licence and figure URL for the relevant CC BY publication/reuse route. [OASIS data-use terms](https://sites.wustl.edu/oasisbrains/home/access/) identify commercial-use restrictions and redistribution restrictions for OASIS-3/4; applicability to this augmented-image version is unresolved. The live page returned HTTP 502, so the reviewed search-indexed terms are supporting evidence, not definitive image authorization. These are project admission findings, not universal declarations that the articles cannot lawfully be used.

## Verification and limits

Each admitted article has eight passing gates. Identity is joined across pinned Cloud/JATS, ID Converter, PubMed and the actual PDF title/DOI. Complete PubMed sections are compared directly with fresh XML; abstracts are not summaries. Publication dates retain their source precision. Each PDF has validated bytes, nonzero pages, readable article text, a useful table-text sample where applicable, provider MD5 and SHA-256. The specific article licence was checked in JATS and the actual PDF notice/link; only CC BY 4.0 or CC0 1.0 qualifies.

All main-PDF pages were visually inspected via rendered contact sheets; captions, tables, credits, acknowledgments, licence notices and supplements were checked using fresh text/JATS and rendered supplemental pages/embedded images for passing cases. This is a rights, identity and readability review, not an assessment of scientific validity or a guarantee of perfect table-grid extraction. PMC13328407 has 13/15 matching sampled cells in one table and 14/15 in another table, with all other sampled cells matching; useful text remains readable. The Hernandez-Martínez PDF font variant was resolved through explicit Unicode normalization. The pending TAILORED-AF group-author entry was repaired from the direct JATS collaboration name and its raw helper output was preserved.

The unchanged manifest builder was called directly on the passing-only input and the unique final path. Two live assembly refreshes stopped on NCBI HTTP 429 after bounded retries, including a slower retry with 1.2 seconds of extra request spacing; neither wrote a manifest. Their complete response sets and failure receipts are preserved. Final assembly uses only original provider-response bytes freshly acquired in this same unique run, preferring the latest complete response set, with exact URL matching. The original helper re-parses and checks these bytes. Provider archive times, source set and hashes are retained per article; metadata assembly time is recorded separately from source acquisition time. No pre-run drafts, PDFs or approvals are consumed. Sources are compared before eligible labels/evidence are attached; a changed substantive source requires renewed review. ID Converter response-date-only changes are recorded and the complete semantic identifier/version mapping is checked. The final transport cache does not establish whether PubMed changed after each recorded source-acquisition time; it preserves the freshly retrieved evidence for this run.

**99 offline tests passed** using the main checkout Python environment and the active worktree test layout. No corpus ingestion, benchmark or paid LLM evaluation, service startup or merge occurred. Existing tracked files at the delivery baseline remain unchanged by this acquisition; all eight archived V1 files remain byte-identical. Unrelated JUA-116 commits made during acquisition changed instructions/test layout and moved the existing pending metadata; those changes were preserved and are explicitly listed in verification.json.

The workflow was narrowed by concurrent JUA-116 commits while this acquisition was running. Those committed changes were preserved. This run follows the explicit stricter instructions in this chat: third-party rights and useful table extraction remain admission gates. Review findings support this selection; they do not authorize public PDF distribution.
