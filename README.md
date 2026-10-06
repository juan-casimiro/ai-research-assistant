# Research Assistant (RAG)

[![CI](https://github.com/juan-casimiro/ai-research-assistant/actions/workflows/ci.yml/badge.svg)](https://github.com/juan-casimiro/ai-research-assistant/actions/workflows/ci.yml)

A FastAPI service for semantic search and question-answering over ingested documents, using local embeddings, Chroma for vector storage, and an LLM (via LangChain) for grounded generation.

The current evaluation benchmark contains **55 articles and 158 questions** across
cardiology, diabetes, oncology, outliers and ALS/FTD. Biomedical literature provides
dense, citation-heavy evidence for testing the domain-agnostic RAG pipeline.
Start with the [benchmark guide](data/benchmark/README.md) for the current inputs,
results and reproduction instructions.

Questions and expected answers were authored and reviewed by advanced LLMs against
the articles. They cover evidence lookup, reasoning, distractors, synthesis,
conflicting findings, false premises and missing facts. This is model-reviewed
reference material, not biomedical expert certification. Current automated scores
measure retrieved articles and evidence; generated-response correctness remains
a separate evaluation step.

CI runs offline unit tests, builds the Docker image, and smoke-tests `/health`
on pull requests and pushes to `main` and the active benchmark epic. Fresh
retrieval experiments remain manual; inference can vary and optional rewriting
or answer generation makes provider calls. Saved-evidence replay is an offline
check. Successful `main` builds publish commit-SHA and `latest` images to
`ghcr.io/juan-casimiro/ai-research-assistant`; nothing is deployed automatically.
See [ADR-003](adr/003-deployment-and-containerisation.md).

## What this project demonstrates

This portfolio connects a working RAG API to controlled retrieval experiments
and inspectable evidence. The engineering questions are whether the pipeline
finds the right sources, retrieves the passages needed to answer, and remains
consistent when unrelated or competing articles are added.

Read it in three layers:

- **Run and understand the service:** the Docker demo, API contract, architecture
  and [retrieval decisions](adr/001-chunking-and-retrieval.md).
- **Assess the methodology and findings:** the [evaluation methodology](adr/002-evaluation-methodology.md),
  [benchmark guide](data/benchmark/README.md) and [retrieval findings](data/findings/retrieval.md).
- **Inspect and verify the evidence:** the [case index](data/benchmark/cases/README.md),
  [saved evaluations](data/evaluations/) and [offline replay](data/README.md#verify-the-retained-experiment).

The current results expose a substantial gap between retrieving source articles
and assembling complete pinned evidence. Difficult synthesis and source-conflict
cases remain visible; the benchmark preserves their questions and requirements.
Generated-answer judging is a future evaluation layer.

## Current benchmark

The [five-topic report](data/findings/retrieval.md) records the finalized
55-article, 158-question retrieval evaluation. At n=8, complete article sets were
found for **115/129 answerable questions** and complete pinned evidence for
**37/129**. False-premise and missing-fact cases are reported separately; failures
remain visible. These figures do not score generated answers.

The [benchmark guide](data/benchmark/README.md) links the question/article dependencies,
selection records, results and reproduction instructions. The
[corpus and benchmark standards](docs/benchmark-standards.md) describe selection and
authoring rules. Topic directories hold source selections and question contracts;
`data/benchmark/` defines the current evaluation conditions. The current manifest,
evaluations and findings live under `data/`; earlier releases are kept under
`data/archive/`. Reusable utilities live under [tools/](tools/README.md).

The original 19-article / 133-question benchmark and the earlier four-topic
combined run are historical. Their questions, scoring and corpus differ from the
current benchmark, so their headline scores are not directly comparable. The
Docker seed corpus is a separate runnable demonstration.

## Evaluation evidence relationships

The [case index](data/benchmark/cases/README.md) connects all 158 questions to their
expected responses, required and alternative articles, evidence locations and
recorded distractors. It provides direct links for reviewing the sources.

The [query-by-query source-conflict report](data/findings/source-conflicts.md)
explains which articles and passages contribute competing claims to each
evaluation query, how the benchmark handles them, and what the saved retrieval
runs actually demonstrated. It distinguishes unresolved source inconsistencies
from differences in populations, endpoints, analyses and denominators.
This report is durable release documentation and is retained independently of
experimental benchmark run artifacts.

## Two ways to run this

| | Docker | Host |
|---|---|---|
| For | Reviewers — one command, bring your own Anthropic API key | Development & evaluation |
| Corpus | [Bundled seed corpus](adr/003-deployment-and-containerisation.md) (CC BY) | Current 55-article V2 corpus, downloaded or prepared locally |
| Command | `docker compose up --build` (no API key? see the [Ollama appendix](#appendix-local-llm-with-ollama)) | see below |
| Evaluation scope | Readiness smoke test; no benchmark quality claim | New V2 experiments or offline replay of pinned saved evidence |

## Run it (Docker)

```bash
cp .env.example .env   # set ANTHROPIC_API_KEY
docker compose up --build
```

Compose publishes the RAG API at `http://localhost:8000` on the host's
loopback interface only. Containers in the same Compose application, including
the MCP gateway's Compose `include` flow, still reach it at
`http://research-assistant:8000` over the Docker network. Localhost clients can
also call the RAG API directly and therefore bypass gateway authentication;
this binding reduces network exposure but does not provide complete isolation
or add authentication to the upstream service.

`/health` reports `{"status": "loading"}` (`503`) while models load and
the seed corpus is ingested, then `{"status": "ready", "chunks": ...}`
(`200`) once it's usable — expect roughly 30–60s on first run.

Try a query against the seed corpus once ready:

```bash
curl -X POST localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What does CT-FFR measure in coronary artery disease?"}'
```

`docker compose restart` reuses the same named volume — seeding is
skipped and existing data persists.

**The [seed corpus](adr/003-deployment-and-containerisation.md) bundled in the
image is a demo convenience.** It does not reproduce the current V2 results or
the original V1 scores. See [ADR-003](adr/003-deployment-and-containerisation.md)
for the Docker scope and startup decisions.

No Anthropic API key? See the [Ollama appendix](#appendix-local-llm-with-ollama)
for a Docker-based alternative that runs entirely locally, no credentials
required.

## Develop and evaluate (host)

Use Python 3.12 for development, the current V2 benchmark and offline verification.
The [original V1 setup](docs/historical-benchmark.md) is preserved separately.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

`.env`: defaults to `LLM_PROVIDER=anthropic` (set `ANTHROPIC_API_KEY`). To use
a local Ollama server instead, set `LLM_PROVIDER=ollama` and
`OLLAMA_BASE_URL=http://localhost:11434` — the shipped `.env.example` value
targets the Docker profile instead (see the
[Ollama appendix](#appendix-local-llm-with-ollama)).


**Confirm `SEED_ON_EMPTY=false` in your `.env`.** Docker pins
`SEED_ON_EMPTY=true` for reviewers regardless of what's in `.env` (see
`docker-compose.yml`), but nothing overrides it on the host. Leaving it
unset or `true` here will auto-ingest the [bundled seed
corpus](adr/003-deployment-and-containerisation.md)
alongside the full corpus, duplicating overlapping articles under different
filenames and skewing retrieval results.

Start the server:

```bash
uvicorn main:app --reload
```

In a separate terminal, download and ingest the current V2 selection:

```bash
python -m tools.corpus.download_corpus --manifest data/manifest.json --corpus-dir corpus/combined-v2
python -m tools.corpus.ingest_corpus --manifest data/manifest.json --corpus-dir corpus/combined-v2
```

Use a fresh, dedicated `CHROMA_PATH` with `SEED_ON_EMPTY=false`. The ingestion
utility reports each file's outcome; its exit status alone does not prove full
membership. Before evaluating, check the ingestion output and use the benchmark
evaluator's exact membership and pinned PDF/text checks. PDFs and extracted text
remain local, ignored build artifacts.

The [data guide](data/README.md#download-ingest-and-evaluate) explains current
benchmark commands and the difference between a new experiment and replay of
saved evidence. Downloaded PMC bytes may differ from the historically pinned
bytes even for the same deposit version. The [historical replay guide](data/README.md#verify-the-retained-experiment)
verifies the saved experiment offline when the pinned local inputs are available.

### Current benchmark evaluation

A current-topic evaluation against the full 55-article condition is:

```bash
python -m tools.evaluation.eval_golden --benchmark data/benchmark/cardiology \
  --corpus-dir corpus/combined-v2 --condition C3 --output data/evaluations/local/cardio.json
```

The harness calls production `retrieve()` in its own process; it does not need
Uvicorn for evaluation. The configured collection must already contain the exact
condition membership. Choose a fresh output path: versioned runs refuse overwrites.
Repeat with the other topic inputs only when a new experiment is intended.
BM25 and query rewriting are optional; rewriting makes provider calls and
requires explicit approval of that run. Saved-evidence verification needs neither
new retrieval inference nor paid calls.

### Historical retrieval evaluation

The [original V1 guide](docs/historical-benchmark.md) contains the 19-article
setup, manual-download exceptions, legacy scorer commands and committed results.
It is separate from the current benchmark and Docker demo.


## Features

- **POST /ingest** — chunk and embed a document, storing it for retrieval
- **POST /query** — retrieve relevant chunks for a question and generate
  a grounded answer, citing sources and reporting whether the retrieved
  context was sufficient to answer

## Response contract

`/query` returns:

| Field | Type | Meaning |
|---|---|---|
| `answer` | `str` | Grounded answer from the retrieved context |
| `sources` | `list[str]` | Source documents for the retrieved chunks |
| `context_sufficient` | `bool` | Whether the retrieved context was enough to answer |
| `insufficiency_reason` | `str \| null` | Set when `context_sufficient` is false |

`sources` is ordered by relevance, most-relevant first, as determined by the
cross-encoder reranker — see ADR-001.

Invalid query values return FastAPI's standard `422 Unprocessable Content`
response. `question` must contain 1–1,000 non-whitespace characters, and
`n_results` must be between 1 and the service's fused candidate-pool limit.

The service makes one bounded attempt at each LLM call; it does not retry
provider failures internally. A timed-out LLM request returns `504` with
`{"detail":"upstream LLM request timed out"}`. Callers own any retry budget
for transient upstream failures so they can enforce their end-to-end latency
limit and avoid multiplying retries across service boundaries. See ADR-003
for the measured timeout budgets and trade-offs.

## Architecture
```
Document text
│
▼
chunk_text() — paragraph-boundary splitting with overlap
│
▼
Embed each chunk (local model, FastEmbed/bge-small-en-v1.5)
│
▼
Store in Chroma (embedded mode, persisted locally)
│
▼
Rebuild BM25 index (rank_bm25, in-memory, rebuilt on every ingest
and at startup)


Question
│
▼
Embed the question (same model) ──► Chroma dense search (top-20)
│
├─ [if use_bm25]     BM25 sparse search (top-20)
│
├─ [if use_query_rewriting]  the LLM rewrites the question,
│                             then repeats both searches above
│                             on the rewritten query
│
▼
Reciprocal Rank Fusion — merges all enabled ranked lists (k=60),
capped to top 20 candidates
│
▼
Cross-encoder reranking (Xenova/ms-marco-MiniLM-L-6-v2) — re-scores
the fused candidates, selects final top-N
│
▼
Chunks + question → LLM → grounded answer + sources + sufficiency flag
```
BM25 and query rewriting are opt-in (use_bm25, use_query_rewriting on /query, both default False) — see ADR-001 for why they're not enabled by default. The diagram above shows the full pipeline with both enabled; with both off, retrieval is dense search → reranking only.

## Tech stack

- **FastAPI** — async web framework
- **FastEmbed** (`bge-small-en-v1.5`) — local, ONNX-based embeddings, no API cost
- **Chroma** — embedded-mode vector database, no server required
- **rank_bm25** (`BM25Okapi`) — in-memory sparse lexical retrieval, fused
  with dense search via reciprocal rank fusion (opt-in, `use_bm25`)
- **LangChain** — Anthropic and Ollama adapters behind a small LLM interface
  for grounded generation and opt-in query rewriting. Provider settings,
  structured-output options, and timeout translation live in `llm_client.py`.


## Design decisions and known limitations
 
See [ADR-001](adr/001-chunking-and-retrieval.md) for the full history:
chunking approach, the two-stage retrieval pipeline (dense embeddings +
cross-encoder reranking), BM25 hybrid search via reciprocal rank fusion,
and LLM-based query rewriting — including a full evaluation of BM25 and
rewriting against the golden QA set, with results and the decision to
keep both opt-in rather than default-on.

See [ADR-002](adr/002-evaluation-methodology.md) for evaluation methodology
and its historical development. The [benchmark guide](data/benchmark/README.md)
identifies the current inputs and measured results.
 
Historically, two-stage retrieval (embeddings + reranking) scored 96.4%
(n=3) / 98.2% (n=8) on the golden QA set (133 queries, 111 scored). BM25
and query rewriting were implemented and evaluated as opt-in additions
but did not improve retrieval on this corpus — see ADR-001 for the full
breakdown, including one attributable regression from BM25 alone and
why combining it with rewriting recovered it, re-confirmed after the
corpus expanded from 16 to 19 documents (outlier cluster).


## Possible future improvements

- Isolate BM25 as a standalone retrieval signal (no vector search in the
  fusion) to measure lexical-only retrieval quality on this corpus,
  separate from the "does adding BM25 to vector help" question already
  answered
- Author eval queries with realistic lexical ambiguity, to test sparse retrieval after gold
  is reviewed and frozen; no query should be labelled BM25-dependent from observed
  baseline failures
- HyDE (Hypothetical Document Embeddings) or corpus-aware query rewriting,
  as a way to address vocabulary-specific mismatches that generic
  rewriting does not fix (see ADR-001)
- File upload endpoint (currently text-only via JSON)

## Distributed tracing

FastAPI continues incoming W3C `traceparent` context automatically and creates
server spans with `service.name=ai-research-assistant`. Network export defaults
to disabled, so a collector is not required for local development or tests.

To enable the bundled OTLP **gRPC** exporter, configure the process environment
or `.env`:

```dotenv
OTEL_TRACES_EXPORTER=otlp
OTEL_EXPORTER_OTLP_TRACES_ENDPOINT=http://localhost:4317
OTEL_EXPORTER_OTLP_TRACES_TIMEOUT=2
```

Use the collector's reachable hostname when running in a container. The SDK
also accepts standard OTLP headers and TLS settings; `https://` selects a secure
connection. This integration supports `OTEL_TRACES_EXPORTER=none` (default) or
`otlp`; it uses gRPC regardless of `OTEL_EXPORTER_OTLP_PROTOCOL`. Spans are batched
and the provider shuts down on application exit. Collector failures do not make
the RAG service unready, but enabled export can log connection failures.

The offline tracing tests verify the production FastAPI app's incoming parent
context with an in-memory exporter and OTLP export against a temporary local
gRPC collector. Compose/Jaeger setup and the real cross-service demo remain
follow-up work: the one-command Compose stack with Jaeger, and the end-to-end
Spring → FastAPI trace proof in Jaeger.

## Deterministic regression tests

Run `.venv/bin/python -m unittest discover -v` for the offline regression suite.
See [the test-strength audit](quality/test-strength-audit.md) for the
behaviour map, verification-first mutation evidence, optional coverage/complexity
commands, and remaining gaps. These tests do not replace the live golden evaluations.

## Appendix: Local LLM with Ollama

An optional, local alternative to Anthropic — no API key, but slower and
less reliable (see the caveat below). Requires explicitly setting
`LLM_PROVIDER=ollama`; `OLLAMA_BASE_URL` in `.env.example` already targets
the Docker profile below.

```bash
cp .env.example .env   # set LLM_PROVIDER=ollama
docker compose --profile ollama up --build --wait
docker compose --profile ollama exec ollama ollama pull smollm2:1.7b-instruct-q4_K_M
```

`--wait` blocks (detached) until both containers pass their healthchecks,
so the pull runs against a server that's actually up. **`/health` on
`research-assistant` only confirms RAG startup — not Ollama's availability
or that a query will actually succeed**; run the query from
["Run it (Docker)"](#run-it-docker) once the pull finishes to confirm
inference works.

Model selection is fixed per provider via `DEFAULT_MODELS_BY_PROVIDER` in
`llm_client.py`: SmolLM2 (`smollm2:1.7b-instruct-q4_K_M`) for Ollama, Claude
Haiku (`claude-haiku-4-5-20251001`) for Anthropic — switching `LLM_PROVIDER`
switches the model too, and only the selected provider's settings are read.
The model pull is a one-time step (a multi-gigabyte download kept out of the
image build and out of `up`'s critical path); it persists in the
`ollama_data` volume, so restarts don't repeat it.

**Not yet reliable for production use.** SmolLM2 has timed out under normal
retrieval loads (see the [spike](spikes/local-ollama-smollm2-spike.md)) and hasn't always
followed the structured-output contract — treat it as a local/demo path.

<details>
<summary>Manual two-container setup (advanced: resource limits, an independently managed Ollama)</summary>

```bash
docker network create rag-local
docker run -d --name rag-ollama --network rag-local --cpus 4 --memory 4g \
  -v rag-ollama-models:/root/.ollama ollama/ollama:0.34.0
docker exec rag-ollama ollama pull smollm2:1.7b-instruct-q4_K_M
docker build -t ai-research-assistant:local .
docker run -d --name rag-local --network rag-local -p 127.0.0.1:8000:8000 \
  -e LLM_PROVIDER=ollama -e OLLAMA_BASE_URL=http://rag-ollama:11434 \
  -e SEED_ON_EMPTY=true -v rag-local-data:/data/chroma_db ai-research-assistant:local
curl --fail http://localhost:8000/health
```

Use a free host port if another RAG instance is running. Wait for
readiness, then use the query above — `/health` checks RAG startup, not LLM
availability.

</details>
