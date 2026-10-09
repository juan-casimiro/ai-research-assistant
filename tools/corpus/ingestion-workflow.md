# Corpus ingestion

Run from the active repository root. Defaults are `data/corpus_manifest.json`
and `corpus/<corpus_name>/`, taken from the manifest's top-level `corpus_name`
(currently `mvp`). This workflow ingests an already acquired corpus on the host;
it does not download PDFs, change the manifest or apply to the Docker demo,
which always seeds.

`python` below means the repository's Python environment: `.venv/bin/python` in
the active checkout, or the main checkout's `.venv/bin/python` when a worktree
has none (find the main checkout with `git worktree list`). PDFs and collections
are untracked, so in a worktree pass the directory that actually holds the PDFs
with `--corpus-dir`.

Ingestion runs in-process: the production embedding model, chunker and `/ingest`
handler from `main.py` are loaded by the command itself. No server is started,
no port is used, `/health` is not involved and no LLM provider settings or API
key are needed.

The collection follows the same rule as the PDFs and text: it lives beside them
at `corpus/<corpus_name>/chroma` (`corpus/mvp/chroma` for the current corpus).
Ingestion creates it there and evaluation reads it from there; neither needs
`CHROMA_PATH`. Only an exported `CHROMA_PATH` replaces that folder; a value in
`.env` does not. The service and Docker are separate: see the last section.

1. Confirm the corpus is complete. Every manifest PDF must already be in the
   corpus directory; acquire and verify it with the
   [corpus workflow](corpus-metadata-workflow.md) first. Missing PDFs stop the
   run before any model is loaded.
2. Confirm the collection folder does not exist yet. If it does, stop: never
   reuse, reset or append to it, and delete it only with the user's agreement
   before ingesting again.
3. Ingest with seeding disabled on the command line, not taken from `.env`:

```sh
SEED_ON_EMPTY=false python -m tools.corpus.ingest_corpus
```

The command refuses to run unless `SEED_ON_EMPTY=false` is set, and refuses an
existing collection folder. It ingests each article under its manifest
filename, rewrites the adjacent `.txt` with the same extracted text, then
compares the stored chunks with the corpus. Success prints the article count,
the verified chunk count and the absolute collection path.

A nonzero exit means the collection is incomplete: report the reason, leave the
manifest and PDFs unchanged and do not use that collection. Delete the failed
`chroma` folder only with the user's agreement, then start again.
`python -m tools.corpus.reset_collection` empties a collection but leaves its
folder, so it does not prepare a path for this workflow.

Report the manifest, corpus directory, article and chunk counts and the
collection path. The [retrieval evaluation](../evaluation/evaluation-workflow.md)
finds the collection by the same rule.
Do not commit collections, PDFs or extracted text.
Offline verification: `python -m unittest discover -s tests -t . -v`.

## Serving the collection

The service is not tied to a manifest: it opens whatever `CHROMA_PATH` names,
`./chroma_db` by default. To serve an ingested corpus on the host:

```sh
SEED_ON_EMPTY=false CHROMA_PATH=corpus/<corpus_name>/chroma uvicorn main:app
```

`/health` then reports its chunk count. Docker is the reviewer demo and keeps
its own location: `/data/chroma_db` on a named volume, always seeded.
