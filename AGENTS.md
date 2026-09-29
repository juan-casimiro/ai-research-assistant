# Agent guide — ai-research-assistant

Repository-specific guidance for developing, running, and evaluating this service. Read the [README](README.md) for the full setup and API instructions; use the [ADRs](adr/) for the reasoning behind design decisions.

Team-wide development process, review, verification, and Git conventions are in the [Working Agreement — Development Process](https://linear.app/juan-casimiro-agent/document/working-agreement-development-process-fd6dfa17284a). This file covers the repository-specific details agents need to work safely and effectively.

## Service and code map

This is a Python 3.12 / FastAPI retrieval-augmented question-answering service. It embeds and stores ingested text in Chroma, retrieves relevant chunks, reranks them, then asks a configured LLM for a grounded answer.

| File | What to look at |
| --- | --- |
| `main.py` | FastAPI lifespan and startup, ingestion, chunking, retrieval, reranking, and `/health`, `/ingest`, `/query` endpoints. |
| `llm_client.py` | Provider selection, structured answers, query rewriting, timeout handling, and Anthropic/Ollama adapters. |
| `eval_golden.py` | Golden-set retrieval evaluation. Loads the index and calls the production retrieval path from `main.py`. |
| `golden_qa.json` | Golden queries and their expected source documents and categories. |
| `corpus_manifest.json`, `ingest_corpus.py` | Full-corpus metadata and PDF ingestion by exact manifest filename. Corpus PDFs are not committed. |
| `seed_corpus/` | Small, committed CC BY text corpus used by the Docker demo. |
| `docker-compose.yml`, `Dockerfile` | Reviewer runtime, service configuration, health check, and build-time model caching. |
| `adr/001-chunking-and-retrieval.md` | Chunking, retrieval, reranking, and measured search-strategy results. |
| `adr/002-evaluation-methodology.md` | Golden-set categories, scoring, and limitations. |
| `adr/003-deployment-and-containerisation.md` | Runtime and container choices, scope boundaries, and trade-offs. |

## Run and evaluate

The README has the complete instructions. These commands are the common entry points:

| Purpose | Command |
| --- | --- |
| Offline regression suite | `.venv/bin/python -m unittest discover -v` |
| Host development server | `uvicorn main:app --reload` |
| Reviewer/demo service | `docker compose up --build` |
| Golden retrieval evaluation | `python eval_golden.py [--bm25] [--rewrite]` |
| Compare evaluation runs | `python compare_evals.py <baseline.json> <experiment.json>` |

For host development, set `SEED_ON_EMPTY=false` before loading the full corpus. The seed corpus and full corpus share four articles but use different filenames; host auto-seeding can ingest them twice and skew the evaluation. Docker intentionally pins `SEED_ON_EMPTY=true` and `CHROMA_PATH=/data/chroma_db` so local `.env` values cannot change the demo setup.

The CI Docker smoke test starts with empty storage and waits for `/health` to return `200`, exercising startup and the seed check. It does not assert that the seed corpus produced chunks: it checks the status code, not the `chunks` value in the response. If changing demo seeding or relying on seeded content, verify that `/health` reports chunks and that a query can use the demo corpus.

The full PDFs are downloaded manually and must use the exact filenames in `corpus_manifest.json`. Some have non-commercial or no-derivatives license terms, so do not commit or redistribute them. Never commit `.env` files or credentials.

The Docker seed corpus is a demo aid, not the evaluation corpus. The reported retrieval results (96.4% at n=3 and 98.2% at n=8 across 111 scored queries) were measured host-side against the full 19-document corpus. Do not attribute those figures to the Docker seed corpus.

`eval_golden.py` loads models and the populated Chroma index in its own process; it does not call a running API server. It evaluates retrieval using the production `retrieve()` implementation. The evaluation is manual, and query rewriting makes paid LLM calls. Run it when the change warrants evaluation, and compare results with the committed baselines in `eval_results/`.

## Runtime and implementation boundaries

- Startup loads models and the index in a background worker thread. `/health` returns `503` while startup is in progress or after a startup failure, and `200` once the service is ready. Readiness does not make an LLM request; a ready service may still fail `/query` if its provider or credentials are unavailable.
- Runtime objects, including the embedding model, reranker, Chroma collection, LLM client, and BM25 index, are module-level state in `main.py`. Startup and the evaluation harness use different setup paths; keep their intended seeding behavior distinct.
- Baseline retrieval is dense search followed by cross-encoder reranking. BM25 and query rewriting are opt-in flags, both defaulting to `False`; they are additive to dense search. The measured evaluations found no net benefit on this corpus, with one BM25-only regression. Read ADR-001 and use the evaluation harness before changing defaults or making retrieval-quality claims.
- Reranker inference and score consumption block. Keep them inside `asyncio.to_thread()` in `retrieve()` so they do not block the event loop. Preserve async consistency up the whole call chain when changing a function to `async`.
- `/query` returns sources in reranker relevance order. Preserve that order when deduplicating (the current implementation uses `dict.fromkeys`, not a set).
- `context_sufficient` is not an oracle for the unanswerable evaluation category. A false-premise question can be answered correctly by rejecting its premise while still having sufficient context; see ADR-002.
- LLM calls have bounded attempts and timeouts; the service does not retry provider failures internally. Timeouts become HTTP `504` responses, and callers own retries. Keep changes consistent with the timeout and latency boundaries in `llm_client.py` and ADR-003.
- A low-priority host-side reliability concern remains: after several days of uptime, a Uvicorn restart can occasionally re-download the embedding and reranker models. Confirm the actual cache behavior before changing cache settings.
- The Docker image caches embedding and reranker weights at build time and runs with `HF_HUB_OFFLINE=1`. If a model name changes in `main.py`, update the matching Dockerfile cache step. Keep `PYTHONUNBUFFERED=1` so startup progress reaches container logs.
- The Compose service binds to host loopback at port `8000`; it has no endpoint authentication. A successful `/health` check confirms service startup, not external LLM connectivity.

## Development checks

- Tests use `unittest`; run the offline regression suite above for relevant code changes. Check `requirements.txt` before adding dependencies.
- Keep evaluation on the production path: do not add a separate copy of retrieval logic to `eval_golden.py`.
- Keep retrieval claims tied to measured golden-set results. The seed corpus has not been evaluated with the full golden set.
- Before changing startup, seeding, or corpus loading, preserve the separate host-evaluation and Docker-demo behaviors described above and in ADR-003.
