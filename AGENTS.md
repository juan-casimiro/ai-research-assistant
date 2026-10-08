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
- `tools/corpus/download_corpus.py`: PMC PDF downloads and browser instructions for the two Ovid exceptions; see [host setup](README.md#develop-and-evaluate-host). Missing manual downloads return nonzero status.
- `eval_golden.py`: production-path retrieval evaluation; `compare_evals.py`: result comparison.

- `tools/corpus/build_corpus_manifest.py` / `tools/corpus/fetch_article_metadata.py`: corpus manifest from explicitly selected PMC candidates; see README.
- `tools/corpus/extract_corpus_text.py`: local production-equivalent text cache and extraction failures; ingestion cache consumption is deferred.
- `tools/corpus/publish_corpus.py`: final validation and local promotion; abort conflicts and ask the user before resolving them.
- Candidate and acquisition files are generated locally under ignored `build/corpus/<run-id>/`. The corpus metadata is in `data/corpus_manifest.json`; `eligibility` reflects supported article licence evidence only.
- `tools/corpus/corpus-metadata-workflow.md`: metadata, licence and PDF checks; `.agents/skills/generate-corpus-metadata/` routes agents to this workflow.
- `data/archive/v1/`: original corpus manifest, golden Q&A and saved evaluation evidence; corpus helpers live under `tools/corpus/` and run as modules from the repository root.

## Constraints

- Set `SEED_ON_EMPTY=false` for host full-corpus ingestion; overlapping seed articles use different filenames and can be duplicated. When changing seeding, verify chunk count and queryability, beyond CI health status.
- Full-corpus retrieval figures do not describe the Docker demo; see README before making quality claims.
- Keep evaluation on production `retrieve()`; preserve reranker inference and score consumption inside `asyncio.to_thread()`, and reranked source order during deduplication.
- Do not commit downloaded corpus PDFs; redistribution restrictions are documented in README.

- `tests/`: offline service and evaluation regressions; corpus acquisition tests are under `tests/corpus/`.

## Verification

Run `.venv/bin/python -m unittest discover -s tests -t . -v` for offline regressions. Golden evaluation is a separate manual quality check, not a CI gate; follow the Working Agreement's approval rule for paid external runs.
