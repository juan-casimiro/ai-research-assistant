# Corpus and evaluation tools

Run modules from the repository root. The [corpus workflow](corpus/corpus-metadata-workflow.md)
owns the preparation order, selection evidence, validation and local output rules.

| Module | Duties |
| --- | --- |
| `tools.corpus.fetch_article_metadata` | Fetch the whole selection, retain lookup evidence, and print filenames; correct names in the selection file and refetch with repeatable `--pmcid`. |
| `tools.corpus.build_corpus_manifest` | Assemble existing complete metadata records under a required `--corpus-name`; no lookup, downloads or extraction. |
| `tools.corpus.download_corpus` | Download the manifest's pinned PDFs and verify checksums. |
| `tools.corpus.extract_corpus_text` | Extract every PDF into adjacent text; report admission failures. |
| `tools.corpus.ingest_corpus` | Ingest a manifest's PDFs in-process into a new collection at `corpus/<corpus_name>/chroma` with seeding disabled, then verify stored chunks; see the [ingestion workflow](corpus/ingestion-workflow.md). |
| `tools.corpus.reset_collection` | Delete the collection at `CHROMA_PATH`; not part of isolated ingestion. |
| `tools.corpus.publish_corpus` | Compare prepared PMCID membership with the original selection and publish only after validation/conflict checks. |

Use each module's `--help`. Local preparation artifacts remain ignored; publication
and conflict resolution follow the workflow. The manifest's `corpus_name` sets the corpus folder: publication moves PDFs and text into `corpus/<corpus_name>/`.

## Retrieval evaluation and saved comparisons

The current inputs are [55-article metadata](../data/corpus_manifest.json) and
[158 queries](../data/queries.json), explained by the [Q&A field guide](../data/queries-schema.md).
After acquisition and fresh ingestion, follow the
[evaluation workflow](evaluation/evaluation-workflow.md) for `tools.evaluation.evaluate`
and `tools.evaluation.evaluate_combinations`. The latter stages batches locally
and publishes only complete result files; paid rewriting requires approval.

For saved JSON files, `tools.evaluation.compare_runs` works offline without
models or provider calls; use the [comparison workflow](evaluation/comparison-workflow.md).
Read the [saved MVP results](../data/evaluations/mvp/2026-10-09-anthropic/README.md)
and [strategy findings](../data/evaluations/mvp/2026-10-09-anthropic/comparison/findings.md)
for category gains, regressions and limits. Retrieval metrics do not judge answers.
Historical V1 commands and scoring belong in the [V1 archive](../data/archive/v1/README.md).
