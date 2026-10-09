---
name: generate-corpus-metadata
description: Generate corpus metadata from PMCIDs, or acquire PDFs and adjacent text from an existing corpus manifest using this repository's helpers. Use for corpus acquisition and eligibility review, not ingestion or benchmark evaluation.
---

Follow [the corpus metadata workflow](../../../tools/corpus/corpus-metadata-workflow.md)
in the active ai-research-assistant checkout. Select the PMCID-list or existing-
manifest flow from the supplied input and state which applies. When the user
says the corpus is already generated, use `data/corpus_manifest.json` if present;
validate it and skip metadata fetching/assembly. All acquisition, verification
and adjacent `.txt` generation steps are defined in the workflow.
