---
name: generate-corpus-metadata
description: Generate reviewed corpus metadata and acquire PDFs from a user-supplied PMCID list using this repository's helpers. Use for corpus acquisition and eligibility review, not ingestion or benchmark evaluation.
---

Work in the active assigned ai-research-assistant checkout, even if skill discovery
points elsewhere. Read its AGENTS.md and [the corpus metadata workflow](../../../corpus-metadata-workflow.md).
Resolve that document from the repository root; do not use another checkout's outputs.

Accept PMCIDs and any supplied versions, topics and discovery provenance.
Use the existing metadata, manifest and PDF helpers described in the workflow.
Do not invent missing discovery history or infer public reuse rights from PMC access.

Before calling build_corpus_manifest.py, verify every selected article against
all workflow gates, especially exact CC BY 4.0/CC0 1.0 rights, third-party material,
mandatory DOI/PMID/title/authors/journal/date and complete PubMed abstract.
Download candidate PDFs for this review before final manifest assembly.
Exclude failures and unresolved articles; record reasons. Never call pending drafts
an eligible corpus. Bind review evidence to the exact metadata and PDF hashes.
After assembly, recheck fetched metadata against reviewed evidence before publishing
the eligible manifest; the builder itself fetches drafts and does not certify rights.

Keep downloads and acquisition evidence local; preserve archived V1 data.
Report admitted/excluded/pending counts, output paths, checks and limitations.
