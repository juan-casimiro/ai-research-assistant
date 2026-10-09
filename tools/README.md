# Corpus helpers

Run modules from the repository root. The [corpus workflow](corpus/corpus-metadata-workflow.md)
owns the preparation order, selection evidence, validation and local output rules.

| Module | Duties |
| --- | --- |
| `tools.corpus.fetch_article_metadata` | Fetch the whole selection, retain lookup evidence, and print filenames; correct names in the selection file and refetch with repeatable `--pmcid`. |
| `tools.corpus.build_corpus_manifest` | Assemble existing complete metadata records; no lookup, downloads or extraction. |
| `tools.corpus.download_corpus` | Download the manifest's pinned PDFs and verify checksums. |
| `tools.corpus.extract_corpus_text` | Extract every PDF into adjacent text; report admission failures. |
| `tools.corpus.ingest_corpus` | Ingest a manifest's PDFs in-process into a new collection with seeding disabled, then verify stored chunks; see the [ingestion workflow](corpus/ingestion-workflow.md). |
| `tools.corpus.reset_collection` | Delete the collection at `CHROMA_PATH`; not part of isolated ingestion. |
| `tools.corpus.publish_corpus` | Compare prepared PMCID membership with the original selection and publish only after validation/conflict checks. |

Use each module's `--help`. Local preparation artifacts remain ignored; publication
and conflict resolution follow the workflow. The manifest's `corpus` name sets the corpus folder: publication moves PDFs and text into `corpus/<name>/`.
