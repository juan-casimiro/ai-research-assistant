# Corpus ingestion

Run from the active repository root using its Python environment. Defaults are
`data/corpus_manifest.json` and `corpus/mvp/`. This workflow ingests an already
acquired corpus on the host; it does not download PDFs, change the manifest or
apply to the Docker demo, which always seeds.

Ingestion runs in-process: the production models, chunker and `/ingest` handler
from `main.py` are loaded by the command itself. No server is started, no port
is used and `/health` is not involved. The service configuration is loaded as
usual, so the LLM provider settings in `.env` must be valid; ingestion makes no
provider calls.

1. Confirm the corpus is complete. Every manifest PDF must already be in the
   corpus directory; acquire and verify it with the
   [corpus workflow](corpus-metadata-workflow.md) first. Missing PDFs stop the
   run before any model is loaded.
2. Choose a new collection path that does not exist yet, under the ignored
   `build/corpus/` directory, for example `build/corpus/chroma/<run-id>`. Never
   reuse, reset or append to an existing collection.
3. Ingest with both variables set on the command line, not taken from `.env`:

```sh
SEED_ON_EMPTY=false CHROMA_PATH=build/corpus/chroma/<run-id> \
  python -m tools.corpus.ingest_corpus \
  --manifest data/corpus_manifest.json --corpus-dir corpus/mvp
```

The command refuses to run unless `SEED_ON_EMPTY=false` is set and `CHROMA_PATH`
is set to a path that does not exist. It ingests each article under its manifest
filename, rewrites the adjacent `.txt` with the same extracted text, then
compares the stored chunks with the corpus. Success prints the article count,
the verified chunk count and the absolute `CHROMA_PATH`.

A nonzero exit means the collection is incomplete: report the reason, leave the
manifest and PDFs unchanged and do not use that collection. Start again with
another new path; discard the failed directory only with the user's agreement.
`python -m tools.corpus.reset_collection` deletes the collection at the
`CHROMA_PATH` it is given and is never part of this workflow.

Report the manifest, corpus directory, article and chunk counts and the
collection path. Use that same `CHROMA_PATH` with `SEED_ON_EMPTY=false` for the
[retrieval evaluation](../evaluation/evaluation-workflow.md) or to serve the
collection with `uvicorn main:app`; `/health` then reports its chunk count.
Do not commit collections, PDFs or extracted text.
Offline verification: `python -m unittest discover -s tests -t . -v`.
