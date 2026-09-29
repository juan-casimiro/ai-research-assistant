# Agent guide — ai-research-assistant

Repository-specific guidance for agents working on this Python 3.12 / FastAPI retrieval-augmented question-answering service.

## Start with the relevant source

- **Team process, task workflow, verification, and Git/PR conventions:** [Working Agreement — Development Process](https://linear.app/juan-casimiro-agent/document/working-agreement-development-process-fd6dfa17284a), the canonical source for cross-repository process.
- **Setup, run modes, configuration, API contract, and evaluation commands:** [README](README.md). See [Docker quickstart](README.md#run-it-docker), [host development and evaluation](README.md#develop-and-evaluate-host), and [retrieval evaluation](README.md#retrieval-evaluation) as needed.
- **Architecture decisions:** read only the relevant record when changing that area: [ADR-001](adr/001-chunking-and-retrieval.md) for chunking/retrieval, [ADR-002](adr/002-evaluation-methodology.md) for golden-set design/scoring, or [ADR-003](adr/003-deployment-and-containerisation.md) for startup, seeding, and Docker boundaries.

## Project map

- `main.py` contains service startup, ingestion, retrieval, and API endpoints; `llm_client.py` contains provider setup and bounded LLM calls.
- `eval_golden.py` evaluates retrieval through the production `retrieve()` path; `compare_evals.py` compares result files. Search with `rg` for other code locations as needed.

## Guardrails agents are likely to miss

- **Keep host and Docker data paths distinct.** For host evaluation, set `SEED_ON_EMPTY=false` before ingesting the full corpus: the Docker seed and full corpus overlap but use different filenames, so auto-seeding can skew results. Docker intentionally enables seeding. The zero-config auto-seed path for a genuinely empty store remains unverified; CI checks `/health` status, not seeded chunk count or queryability. Verify those before changing or claiming seeded demo behavior. See the [README run modes](README.md#two-ways-to-run-this) and ADR-003.
- **Do not attribute full-corpus results to the demo.** Published retrieval figures were measured against the full 19-document corpus; the smaller Docker seed corpus has not been evaluated with the full golden set. Tie quality claims to measured evaluations; see [README evaluation](README.md#retrieval-evaluation) and ADR-001.
- **Preserve production-path evaluation.** `eval_golden.py` loads the index and models in its own process; it does not call a running API server. Do not duplicate retrieval logic in the harness. Query rewriting can make paid LLM calls; run evaluation when the change warrants it and compare against `eval_results/`.
- **Preserve async and ranking behavior.** Reranker inference and score consumption must stay inside `asyncio.to_thread()` in `retrieve()`, and `sources` must retain reranker order when deduplicated. See ADR-001 before changing retrieval.
- **Do not commit corpus PDFs or credentials.** PDFs are downloaded separately and some cannot be redistributed; never commit `.env` files or secrets. See the [README host setup](README.md#develop-and-evaluate-host).

## Verification

Set up the environment as described in the README. Run `.venv/bin/python -m unittest discover -v` for the deterministic offline regression suite. The golden evaluation is a separate manual quality check, not a routine substitute for the unit suite or a CI gate.
