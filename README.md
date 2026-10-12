Research Assistant (RAG)

[![CI](https://github.com/juan-casimiro/ai-research-assistant/actions/workflows/ci.yml/badge.svg)](https://github.com/juan-casimiro/ai-research-assistant/actions/workflows/ci.yml)

A FastAPI service for semantic search and question-answering over ingested documents, using local embeddings, Chroma for vector storage, and an LLM (via LangChain) for grounded generation.

The current host benchmark contains **55 biomedical articles and 158 queries**.
[Corpus metadata](data/corpus_manifest.json) records public source identities,
pinned PMC versions, licences and acquisition provenance; [Q&A inputs](data/queries.json)
retain reference answers, required facts and accepted evidence alternatives.
The pipeline is domain-agnostic; biomedical literature exercises dense,
citation-heavy and terminology-specific retrieval.

## Current benchmark reading path

1. Start with the [Q&A field guide and metric definitions](data/queries-schema.md).
2. Prepare local PDFs/text using the [corpus metadata workflow](tools/corpus/corpus-metadata-workflow.md),
   then create a fresh collection with the [ingestion workflow](tools/corpus/ingestion-workflow.md).
3. Use the production-path [retrieval evaluation workflow](tools/evaluation/evaluation-workflow.md)
   or compare saved runs offline with the [comparison workflow](tools/evaluation/comparison-workflow.md).
4. Read the [four saved strategy runs](data/evaluations/mvp/2026-10-09-anthropic/README.md)
   and canonical [strategy findings](data/evaluations/mvp/2026-10-09-anthropic/comparison/findings.md),
   with category summaries and per-query gains/regressions linked there.

In this one observed sweep, BM25 configurations improve depth-8 pinned-excerpt
coverage mainly on direct lookup. At depth 8, rewriting alone loses document
coverage; all configurations leave substantial multi-hop and synthesis evidence gaps.
The combined run has the highest observed depth-8 excerpt coverage, but small,
category-dependent differences and independent rewrites do not establish a
stable strategy ranking. These are document/evidence retrieval measurements,
not generated-answer accuracy; literal excerpt misses can retain semantic support.

The [original V1 archive](data/archive/v1/README.md) owns the earlier 19-article /
133-query results, scoring interpretation and experiment history. V1 scores
are not directly comparable to the current benchmark. Neither benchmark describes
the bundled Docker demo.

CI runs unit tests, builds the Docker image, and smoke-tests `/health` on every pull request and push to `main`. Retrieval evaluation remains manual; optional query rewriting is non-deterministic and can call a paid API. Successful `main` builds publish commit-SHA and `latest` images to `ghcr.io/juan-casimiro/ai-research-assistant`; nothing is deployed automatically. See [ADR-003](./adr/003-deployment-and-containerisation.md).

## Two ways to run this

| | Docker | Host |
|---|---|---|
| For | Reviewers — one command, bring your own Anthropic API key | Development & evaluation |
| Corpus | [Bundled seed corpus](./adr/003-deployment-and-containerisation.md) (CC BY) | Current 55-article corpus (locally acquired) |
| Command | `docker compose up --build` (no API key? see the [Ollama appendix](#appendix-local-llm-with-ollama)) | see below |
| Evaluation | Demo corpus; benchmark figures do not apply | Current corpus and Q&A benchmark |

## Run it (Docker)

```bash
cp .env.example .env   # set ANTHROPIC_API_KEY
docker compose up --build
```

An `ANTHROPIC_API_KEY` already exported in your shell is passed to the container
and takes precedence, so the key can stay out of `.env`.

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

**The bundled seed corpus is a demo convenience only.** Current and historical
benchmark results describe separately acquired host corpora.

No Anthropic API key? See the [Ollama appendix](#appendix-local-llm-with-ollama)
for a Docker-based alternative that runs entirely locally, no credentials
required.

## Corpus metadata and PDFs

Give a PMCID list or an existing corpus manifest to the [generate-corpus-metadata skill](./.agents/skills/generate-corpus-metadata/SKILL.md)
to generate metadata when needed, acquire PDFs and generate adjacent text files. The process and
verification requirements are described in [the corpus metadata workflow](./tools/corpus/corpus-metadata-workflow.md).

## Develop and evaluate (host)

Use the current corpus manifest and an isolated retrieval collection.

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
corpus](./adr/003-deployment-and-containerisation.md)
alongside the full corpus you're about to load below — not instead of
it — silently duplicating articles under two filenames and skewing
retrieval results.

Acquire and verify PDFs and adjacent text using the
[corpus workflow](tools/corpus/corpus-metadata-workflow.md). PDFs remain untracked;
article licence terms are recorded in [the manifest](data/corpus_manifest.json).
Ingest into a new collection beside the corpus with seeding disabled; no server is needed
(see the [ingestion workflow](tools/corpus/ingestion-workflow.md)):

```bash
SEED_ON_EMPTY=false python -m tools.corpus.ingest_corpus
```

The corpus folder comes from the manifest's `corpus_name` (`mvp`), and the
collection is created beside the PDFs at `corpus/mvp/chroma`. Evaluation reads
it from there. The command refuses an existing collection folder; do not reset
or append to a shared collection, because the evaluator checks exact corpus
membership. To serve it, start the service with
`SEED_ON_EMPTY=false CHROMA_PATH=corpus/mvp/chroma uvicorn main:app`.

### Retrieval evaluation

```bash
python -m tools.evaluation.evaluate
```

Evaluates all 158 questions in [queries.json](data/queries.json) against production
`retrieve()`. [queries-schema.md](data/queries-schema.md) documents the inputs;
[the evaluation workflow](tools/evaluation/evaluation-workflow.md) describes
setup, verification and optional BM25/query rewriting. Results separate document
coverage from pinned-evidence coverage; they do not measure generated-answer
accuracy. Outputs are ignored under `build/corpus/evaluation-runs/`.

Saved current retrieval runs can be compared offline with the
[comparison workflow](tools/evaluation/comparison-workflow.md) and
[compare-retrieval-runs skill](.agents/skills/compare-retrieval-runs/SKILL.md).

V1 corpus details, scoring rules and saved results are preserved in the
[V1 evaluation record](data/archive/v1/README.md), including the original
[methodology](data/archive/v1/methodology.md) and
[acquisition steps](data/archive/v1/corpus-acquisition.md).


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
 
[ADR-001](adr/001-chunking-and-retrieval.md) explains chunking, dense search,
reranking and opt-in BM25/query rewriting. [ADR-002](adr/002-evaluation-methodology.md)
explains document/evidence scoring and its limits. The current
[strategy findings](data/evaluations/mvp/2026-10-09-anthropic/comparison/findings.md)
show why source coverage alone overstates evidence completeness, especially for
multi-hop and synthesis. Generated-answer evaluation remains separate work.

See the [integration record](docs/benchmark-integration.md) for capabilities
extracted to main and remaining candidates for selection.

## Possible future improvements

- Isolate BM25 as a standalone retrieval signal (no vector search in the
  fusion) to measure lexical-only retrieval quality on a fixed benchmark,
  separately from the additive BM25 experiments
- Add eval queries where dense retrieval + reranking demonstrably fails
  and lexical exact-match would succeed, to test BM25's upside fairly
  (the historical V1 exact-match cases already passed on vector-only)
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

Run `.venv/bin/python -m unittest discover -s tests -t . -v` for the offline regression suite.
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
