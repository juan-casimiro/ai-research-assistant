# Agent guide — ai-research-assistant

Python 3.12 / FastAPI retrieval-augmented question-answering service.

## Shared development guidance

Follow `AGENTS.md` in the `development-config` checkout beside this repository's
main checkout (`../development-config` from the main checkout root; from a
worktree, find the main checkout with `git worktree list`).

If that checkout is unavailable, read the
[development guidance index](https://github.com/juan-casimiro/development-config/blob/main/AGENTS.md)
from GitHub `main` through authenticated access (private repository).
If neither is accessible, report that before work that depends on it.

## Sources

- [README](README.md): setup, run modes, API contract and evaluation commands.
- Relevant ADRs: [retrieval](adr/001-chunking-and-retrieval.md), [evaluation](adr/002-evaluation-methodology.md), [startup and Docker](adr/003-deployment-and-containerisation.md).

## Project map

- `main.py`: startup, ingestion, retrieval and endpoints; `llm_client.py`: provider configuration and bounded LLM calls.
- `download_corpus.py`: PMC PDF downloads and browser instructions for the two Ovid exceptions; see [host setup](README.md#develop-and-evaluate-host). Missing manual downloads return nonzero status.
- `eval_golden.py`: production-path retrieval evaluation; `compare_evals.py`: result comparison.

## Constraints

- Set `SEED_ON_EMPTY=false` for host full-corpus ingestion; overlapping seed articles use different filenames and can be duplicated. When changing seeding, verify chunk count and queryability, beyond CI health status.
- Full-corpus retrieval figures do not describe the Docker demo; see README before making quality claims.
- Keep evaluation on production `retrieve()`; preserve reranker inference and score consumption inside `asyncio.to_thread()`, and reranked source order during deduplication.
- Do not commit downloaded corpus PDFs; redistribution restrictions are documented in README.

## Verification

Run `.venv/bin/python -m unittest discover -v` for offline regressions. Golden evaluation is a separate manual quality check, not a CI gate; follow the Working Agreement's approval rule for paid external runs.
