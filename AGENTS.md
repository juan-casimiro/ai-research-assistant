# Agent guide — ai-research-assistant

Python 3.12 / FastAPI retrieval-augmented question-answering service.

## Shared development guidance

Follow `AGENTS.md` in the `development-config` checkout beside this repository's
main checkout (`../development-config` from the main checkout root; from a
worktree, find the main checkout with `git worktree list`). If it is
unavailable, report that and stop before task work.

## Sources

- [README](README.md): setup, run modes, API contract and evaluation commands.
- Relevant ADRs: [retrieval](adr/001-chunking-and-retrieval.md), [evaluation](adr/002-evaluation-methodology.md), [startup and Docker](adr/003-deployment-and-containerisation.md).

## Project map

- `main.py`: startup, ingestion, retrieval and endpoints; `llm_client.py`: provider configuration and bounded LLM calls.
- `tools/corpus/download_corpus.py`: PMC PDF downloads and browser instructions for the two Ovid exceptions; see [V1 acquisition record](data/archive/v1/corpus-acquisition.md). Missing manual downloads return nonzero status.
- `tools/evaluation/evaluate.py` and `scoring.py`: current production-path retrieval evaluation; `compare_evals.py`: result comparison.

- `tools/corpus/build_corpus_manifest.py` / `tools/corpus/fetch_article_metadata.py`: fetch the selection’s latest/pinned PMC metadata and assemble complete records; see the corpus workflow.
- `tools/corpus/extract_corpus_text.py`: production-equivalent extraction into text beside PDFs and a small failure report.
- `tools/corpus/ingest_corpus.py`: in-process ingestion into a new collection at `corpus/<corpus_name>/chroma` (`SEED_ON_EMPTY=false`, folder must not exist); see `tools/corpus/ingestion-workflow.md`. `.agents/skills/ingest-corpus/` routes agents there.
- `tools/corpus/publish_corpus.py`: final validation and local promotion; abort conflicts and ask the user before resolving them.
- `candidates.json` retains the original supplied PMCIDs before network calls; failed fetches cannot remove selected articles.
- Candidate and acquisition files are generated locally under ignored `build/corpus/<run-id>/`. The corpus metadata is in `data/corpus_manifest.json`; its `corpus_name` sets the local folder `corpus/<corpus_name>/` for PDFs, text and the `chroma` collection; `eligibility` reflects supported article licence evidence only.
- `tools/corpus/corpus-metadata-workflow.md`: metadata, licence and PDF checks; `.agents/skills/generate-corpus-metadata/` routes agents to this workflow.
- `data/queries.json` and `data/queries-schema.md`: current Q&A inputs and field guide; evaluation procedure is `tools/evaluation/evaluation-workflow.md`.
- `data/archive/v1/`: original corpus manifest, golden Q&A and saved evaluation evidence; corpus helpers live under `tools/corpus/` and run as modules from the repository root.

## Constraints

- Set `SEED_ON_EMPTY=false` for host full-corpus ingestion; overlapping seed articles use different filenames and can be duplicated. When changing seeding, verify chunk count and queryability, beyond CI health status.
- Full-corpus retrieval figures do not describe the Docker demo; see README before making quality claims.
- Keep evaluation on production `retrieve()`; preserve reranker inference and score consumption inside `asyncio.to_thread()`, and reranked source order during deduplication.
- Do not commit downloaded corpus PDFs; redistribution restrictions are documented in README.

- `tests/`: offline service and evaluation regressions; corpus acquisition tests are under `tests/corpus/`.

## Verification

Run `.venv/bin/python -m unittest discover -s tests -t . -v` for offline regressions. Golden evaluation is a separate manual quality check, not a CI gate; follow the Working Agreement's approval rule for paid external runs.
