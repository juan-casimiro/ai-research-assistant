# Corpus helpers

Run modules from the repository root. The [corpus workflow](corpus/corpus-metadata-workflow.md)
owns the preparation order, selection evidence, validation and local output rules.

| Module | Duties |
| --- | --- |
| `tools.corpus.fetch_article_metadata` | Fetch latest or explicitly pinned metadata; retain lookup evidence; `--review-record` assigns reviewed naming/topic offline. |
| `tools.corpus.build_corpus_manifest` | Assemble existing complete metadata records; no lookup, downloads or extraction. |
| `tools.corpus.download_corpus` | Download the manifest's pinned PDFs and verify checksums. |
| `tools.corpus.extract_corpus_text` | Extract and verify the reusable local text cache. |
| `tools.corpus.publish_corpus` | Compare prepared PMCID membership with the original selection and publish only after validation/conflict checks. |

Use each module's `--help`. Local preparation artifacts remain ignored; publication
and conflict resolution follow the workflow. Ingestion cache integration is deferred.
