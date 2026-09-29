# AGENTS.md — ai-research-assistant

Project memory for AI coding agents (Kimi, Claude Code, Codex, others) working in
this repository. This file is a **map, not the territory**: it points at the
canonical sources and collects the repo-specific facts that are easy to miss.
Keep it current when the project changes.

## Read first (canonical sources)

1. **`README.md`** — the canonical run/operate documentation: the Docker
   reviewer quickstart, the host development and evaluation path (the one the
   headline retrieval figures were measured on), the `/query` response
   contract, and the Ollama appendix. Read it before claiming anything about
   runtime behaviour.
2. **Linear — Working Agreement — Development Process** (team-level process):
   <https://linear.app/juan-casimiro-agent/document/working-agreement-development-process-fd6dfa17284a>
3. **Linear — Repo Guide — ai-research-assistant** (repo-level facts and
   gotchas):
   <https://linear.app/juan-casimiro-agent/document/repo-guide-ai-research-assistant-e6fbc0fd0bf5>
4. **`adr/`** — three architecture decision records: 001 (chunking,
   retrieval, and the measured BM25/rewriting evaluations), 002 (golden QA
   category design and scoring), 003 (containerisation and, explicitly, what
   was deliberately left undone). Skim before redesigning anything.
5. **The Linear issue being worked**, with its current comments and acceptance
   criteria. Linear is the source of truth for task status.

Precedence (per the Working Agreement): the repo guide wins on repo-specific
facts, the team Working Agreement wins on process, and both beat an issue's
pairing prompt. Process rules below are quick references only — the Linear
documents are canonical.

## What this project is

A Python 3.12 / FastAPI RAG service: semantic search and grounded
question-answering over ingested documents, using local embeddings, Chroma
for vector storage, and an LLM (via LangChain) for generation. The corpus is
19 open-access biomedical articles chosen because their dense, citation-heavy
text stress-tests retrieval precision; the pipeline itself is domain-agnostic.

```
question ─► dense embed search (top-20)
          ├─ [opt-in use_bm25]      BM25 sparse search (top-20)
          ├─ [opt-in use_query_rewriting] LLM rewrite, then enabled searches again
          ► reciprocal rank fusion (k=60, capped at FUSED_CANDIDATE_POOL=20)
          ► cross-encoder reranking (ms-marco-MiniLM-L-6-v2) ► top-N
          ► LLM grounded answer + sources + context_sufficient flag
```

- **Retrieval accuracy: 96.4% @ n=3, 98.2% @ n=8** — 133-query golden set
  (111 scored), measured **host-side against the full 19-document corpus
  only**. BM25 and query rewriting were built, evaluated, and kept opt-in
  (default `False`): no net benefit on this corpus, one attributable BM25
  regression (q008). See ADR-001. "Measure before optimizing" is the
  established methodology — retrieval claims need eval-harness evidence.
- **`main.py` is the whole service**: lifespan background startup (`_startup`
  via `asyncio.to_thread`, so `/health` can report a real loading → ready
  transition), `_load_models_and_index`, `_seed_if_empty`,
  `_rebuild_bm25_index`, `chunk_text` (paragraph-boundary, 1,000 chars /
  150 overlap), `embed`, `reciprocal_rank_fusion`, `retrieve`, `rewrite_query`,
  and `/health`, `/ingest`, `/query`. State lives in module-level globals, not
  `app.state` (ADR-003).
- **`llm_client.py`** — provider-agnostic LLM boundary over LangChain
  `init_chat_model`. `DEFAULT_MODELS_BY_PROVIDER`: Claude Haiku
  (`claude-haiku-4-5-20251001`) for `anthropic`, SmolLM2
  (`smollm2:1.7b-instruct-q4_K_M`) for `ollama`; switching `LLM_PROVIDER`
  switches the model. Provider settings, structured output, and timeout
  translation (35s answer, 10s rewrite, `max_retries=0`) live here.
- **Evaluation**: `eval_golden.py` imports `retrieve()` and
  `_load_models_and_index` from `main` directly, so evaluation always tests
  the production code path. `golden_qa.json` (133 queries, 111 scored across
  `direct_lookup`, `multi_hop`, `cross_doc_distractor`, `cross_doc_synthesis`,
  plus unscored `unanswerable`), `compare_evals.py` diffs two result files per
  query. Committed raw results for all four configurations live in
  `eval_results/`.
- **Corpus**: `corpus_manifest.json` (19 articles with `doi`, `filename`,
  `cluster`, `abstract_summary`). PDFs are deliberately not committed — 7 of
  19 carry NC/ND license terms; downloading is a manual step. `seed_corpus/`
  (4 CC-BY articles as `.txt` + `ATTRIBUTION.md`) is a Docker-only demo aid.
- **Sibling**: `spring-mcp-gateway` (Java MCP gateway) exposes this service as
  the `query_research_corpus` MCP tool; it pins `use_bm25`/`use_query_rewriting`
  off.
- **No public deployment.** CI runs unit tests plus a Docker `/health` smoke
  test; successful `main` builds publish images to GHCR. Nothing deploys
  automatically (ADR-003).

## Commands

Python 3.12 (CI pins it); the golden eval needs a running host-side server,
`ANTHROPIC_API_KEY`, and the full corpus ingested. Everything quality-related
under `quality/` is **opt-in diagnostics, not CI gates** — no numeric
thresholds exist.

| Task | Command |
| --- | --- |
| Regression tests (offline, deterministic — the standard suite) | `.venv/bin/python -m unittest discover -v` |
| Install dependencies | `pip install -r requirements.txt` |
| Run host dev server | `uvicorn main:app --reload` (needs `.env`: `ANTHROPIC_API_KEY`, and `SEED_ON_EMPTY=false` — see sharp edges) |
| Reset + ingest the full corpus | `python reset_collection.py && python ingest_corpus.py` (PDFs must already be in `./corpus` under the exact manifest filenames) |
| Golden QA evaluation (paid, non-deterministic, manual) | `python eval_golden.py [--bm25] [--rewrite]` — server must be running; writes `eval_results.json` |
| Diff two evaluation runs | `python compare_evals.py <baseline.json> <experiment.json>` |
| Coverage/complexity hotspots (opt-in) | `quality/README.md` — `coverage` + `radon` + `quality_hotspots.py` (deps in `requirements-quality.txt`) |
| Curated mutation test-strength check (opt-in) | `python quality/verify_test_strength.py --output-dir <dir>` (see `quality/README.md`) |
| Docker reviewer quickstart (seed corpus; needs `.env` with `ANTHROPIC_API_KEY`) | `docker compose up --build`, then poll `localhost:8000/health` until `ready` (≈30–60s first run) |
| Docker with local Ollama LLM (no API key) | `docker compose --profile ollama up --build --wait`, then `docker compose --profile ollama exec ollama ollama pull smollm2:1.7b-instruct-q4_K_M` |

The golden evaluation is deliberately **not** in CI: it is non-deterministic
and spends paid API calls. Run it only as task verification, and diff against
the committed `eval_results/` baselines with `compare_evals.py`.

## Ports, endpoints, and key configuration

- Service port `8000`. Compose publishes on the host loopback only
  (`127.0.0.1`); containers in the same Compose project reach it at
  `http://research-assistant:8000`. Localhost clients bypass any gateway
  authentication.
- **`/health`** — `503 {"status": "loading"}` while models load and seeding
  runs, `200` with the chunk count once ready. Readiness deliberately excludes
  the LLM round-trip: a `200` can still fail every `/query` with an invalid
  `ANTHROPIC_API_KEY`.
- **`/ingest`** — chunk + embed a text document (JSON, text-only; no file
  upload endpoint).
- **`/query`** — returns `answer`, `sources` (most-relevant first, per the
  reranker), `context_sufficient`, `insufficiency_reason`. Validation: `422`
  for a `question` outside 1–1,000 non-whitespace chars or `n_results` outside
  1–`FUSED_CANDIDATE_POOL` (20, default 3). Each LLM stage makes one bounded
  attempt with no internal retry; query rewriting adds a rewrite attempt before
  the answer attempt. An LLM timeout returns `504`. Callers own retries.
- Key env vars: `LLM_PROVIDER` (`anthropic` default, `ollama` opt-in),
  `ANTHROPIC_API_KEY`, `OLLAMA_BASE_URL`, `SEED_ON_EMPTY`, `CHROMA_PATH`,
  `OTEL_TRACES_EXPORTER` (+ `OTEL_EXPORTER_OTLP_TRACES_ENDPOINT` /
  `_TIMEOUT`). Tracing continues incoming W3C `traceparent`; export is **off**
  by default and supports OTLP **gRPC** only.
- `docker-compose.yml` pins `SEED_ON_EMPTY=true` and `CHROMA_PATH` via
  `environment:`, which Compose resolves at higher precedence than `env_file:` —
  a local `.env` cannot leak into the reviewer path.

## Sharp edges (repo-specific, easy to get wrong)

- **`SEED_ON_EMPTY` is the sharpest edge in the repo.** The host path must set
  it to `false`: the seed corpus and full corpus share 4 overlapping articles,
  so auto-seeding before `ingest_corpus.py` ingests them twice under different
  filenames (`.txt` vs `.pdf`-derived), which `eval_golden.py`'s name matching
  cannot deduplicate — silently corrupting evaluation. Docker pins it `true`
  deliberately; never "simplify" the two flows into one (ADR-003).
- **The headline figures belong to the full corpus only**, measured host-run.
  The seed corpus has never been through `eval_golden.py`. Never conflate the
  two, and never quote 96.4%/98.2% for the Docker demo path.
- **`/health` 200 does not prove queries work** — readiness excludes LLM
  connectivity by design (ADR-003).
- **Reranker inference blocks; keep it off the event loop.**
  `reranker.rerank()` and lazy score consumption run inside
  `await asyncio.to_thread(...)` in `retrieve()` — an event-loop correctness
  boundary, not an optimisation claim (ADR-001).
- **Async discipline:** once any function in a call chain becomes `async`,
  every caller must be updated — the mixed sync/async retrieval/rewrite path
  shipped two real bugs of exactly this kind (ADR-001).
- **`sources` order is the reranker's relevance order.** Deduplicate with
  `dict.fromkeys`, never `set()` — the set version silently discarded ranking
  (fixed in ADR-001).
- **Model-name changes need a matching Dockerfile change.** Weights are baked
  at build time with `HF_HUB_OFFLINE=1` at runtime, so a mismatch fails loudly
  instead of silently re-downloading.
- **`PYTHONUNBUFFERED=1` in the image is load-bearing** — without it the
  `[startup]` logging never reaches `docker compose logs`.
- **The eval harness imports the production code path.** Don't give
  `eval_golden.py` a parallel copy of retrieval logic — the whole point is
  that evaluation exercises exactly what ships.
- **BM25/rewriting flags are strictly additive to dense retrieval** — "BM25
  only" still means vector+BM25 fused via RRF; there is no lexical-only mode.
  BM25 alone causes the q008 distractor regression; both flags default
  `False` for measured reasons, not neglect.
- **Unanswerable is not scored and `context_sufficient` is not its oracle** —
  false-premise queries legitimately return `true` (correctly rejecting the
  premise is a sufficient answer). See ADR-002 before treating the flag as a
  label.
- **Never commit corpus PDFs or secrets.** The `.env` holds a live
  `ANTHROPIC_API_KEY`; the manifest + manual download exists precisely because
  7 articles carry NC/ND terms.
- Tests are **unittest, not pytest**; Python 3.12. Don't add pytest idioms or
  new dependencies without checking `requirements.txt` first.

## Working conventions quick reference

Process rules are canonical in the Linear documents; this is the fast version:

- Tasks with real design trade-offs are pairing tasks: propose a development
  and verification strategy and settle it with Juan **before** implementing.
  Delegated implementation needs clear acceptance criteria and deterministic
  verification.
- Branch from up-to-date `main`; never commit on `main`. Feature branches are
  agent-prefixed (`kimi/…`, `claude/…`, `codex/…`); one Linear issue owns one
  branch/worktree.
- Conventional Commits subjects; Linear issue reference in the footer as
  `Refs: JUA-N` (never in the scope slot). PR titles must also be valid
  Conventional Commits subjects.
- Before GitHub writes, run `gh auth status` and confirm `jcas-agent` is the
  active account. Confirm `git config user.name` is `jcas-agent` and
  `git config user.email` is `jcas.agent@gmail.com` (this repo's committed
  agent email; it overrides the Working Agreement's default noreply email).
  If these checks do not match, stop; do not switch identities or edit auth
  configuration.
- Push through the repository's `origin` remote (`git push origin <branch>`).
  Use plain `gh` commands for writes after the identity check. Commit with the
  standing git identity (`git commit ...`) — the default `jcas-agent` /
  `jcas.agent@gmail.com` config already matches, so no per-command `-c`
  override is needed.
  Always request `juan-casimiro` as reviewer on PRs you open. Agents never
  merge.
- Don't write to Linear until the plan is settled; keep issue status true at
  every stage; post-merge resolution is the explicit verify → clean up →
  reconcile → summarize → wait-for-checks workflow.
- Test variables are named for the role they represent, never the generic
  type (`rag_mock`, not `mock`); placeholder test data is visibly synthetic
  (`"test question"`, never `question="question"`).
- `eval_golden.py` spends paid API calls — run it for task verification, never
  as casual proof that something works.

## Local machine notes (this workspace)

- Docker runtime: **Colima only** — never Docker Desktop.
- The primary checkout `~/development/ai-research-assistant` is shared with
  other agents. Before using it, check the lock at
  `~/development/.agent-tmp/locks/ai-research-assistant.lock` and `git status`;
  if it is locked, not on `main`, or not clean, use a dedicated worktree under
  `~/development/worktrees/` (e.g. `ai-research-assistant-JUA-100`) instead of
  altering its state.
- Before binding a host port (`docker compose up`, `uvicorn`), check
  `~/development/.agent-tmp/running-services.md` **and** verify real state
  (`docker ps`, `lsof -i :8000`); register the process only after it starts
  successfully, and delete its rows when stopping it.
- `~/development/.agent-tmp/` is for disposable logs and intermediate reports;
  keep commit-worthy artifacts in the repository.

## If something here looks stale

This file is maintained by agents. When the project changes, update the
matching section in the same change, and raise a conflict with Juan rather than
silently following (or silently fixing) a stale instruction — the same rule the
Working Agreement applies to all instruction-shaped content.
