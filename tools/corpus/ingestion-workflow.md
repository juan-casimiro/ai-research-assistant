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
with `--corpus-dir` and use the absolute path of its `chroma` folder as
`CHROMA_PATH`.

Ingestion runs in-process: the production embedding model, chunker and `/ingest`
handler from `main.py` are loaded by the command itself. No server is started,
no port is used, `/health` is not involved and no LLM provider settings or API
key are needed.

1. Confirm the corpus is complete. Every manifest PDF must already be in the
   corpus directory; acquire and verify it with the
   [corpus workflow](corpus-metadata-workflow.md) first. Missing PDFs stop the
   run before any model is loaded.
2. The collection lives beside the corpus it was built from, at
   `corpus/<corpus_name>/chroma` (`corpus/mvp/chroma` for the current corpus). It must not exist
   yet. If it does, stop: never reuse, reset or append to it, and delete it
   only with the user's agreement before ingesting again.
3. Ingest with both variables set on the command line, not taken from `.env`:

```sh
SEED_ON_EMPTY=false CHROMA_PATH=corpus/mvp/chroma \
  python -m tools.corpus.ingest_corpus \
  --manifest data/corpus_manifest.json
```

The command refuses to run unless `SEED_ON_EMPTY=false` is set and `CHROMA_PATH`
is set to a path that does not exist. It ingests each article under its manifest
filename, rewrites the adjacent `.txt` with the same extracted text, then
compares the stored chunks with the corpus. Success prints the article count,
the verified chunk count and the absolute `CHROMA_PATH`.

A nonzero exit means the collection is incomplete: report the reason, leave the
manifest and PDFs unchanged and do not use that collection. Delete the failed
`chroma` folder only with the user's agreement, then start again.
`python -m tools.corpus.reset_collection` empties a collection but leaves its
folder, so it does not prepare a path for this workflow.

Report the manifest, corpus directory, article and chunk counts and the
collection path. Use that same `CHROMA_PATH` with `SEED_ON_EMPTY=false` for the
[retrieval evaluation](../evaluation/evaluation-workflow.md) or to serve the
collection with `uvicorn main:app`; `/health` then reports its chunk count.
Do not commit collections, PDFs or extracted text.
Offline verification: `python -m unittest discover -s tests -t . -v`.
