# JUA-84: local ChatOllama feasibility spike

This is an opt-in experiment with SmolLM2-1.7B-Instruct. Anthropic remains the
default. No provider adapter or shared library is introduced.

## Run in Docker

Run from the repository root. These names, ports, and volumes are separate from
the normal demo stack. No `.env` or Anthropic credentials are passed to the RAG
container. The new Chroma volume is seeded with the bundled demo corpus.

```bash
docker network create jua84-spike
docker run -d --name jua84-ollama --network jua84-spike \
  --cpus 4 --memory 4g \
  -e OLLAMA_NUM_PARALLEL=1 -e OLLAMA_MAX_LOADED_MODELS=1 \
  -v jua84-ollama:/root/.ollama ollama/ollama:latest
docker exec jua84-ollama ollama pull smollm2:1.7b-instruct-q4_K_M

docker build -t ai-research-assistant:jua84 .
docker run -d --name jua84-rag --network jua84-spike \
  -p 127.0.0.1:18000:8000 \
  -e LLM_PROVIDER=ollama \
  -e OLLAMA_MODEL=smollm2:1.7b-instruct-q4_K_M \
  -e OLLAMA_BASE_URL=http://jua84-ollama:11434 \
  -e SEED_ON_EMPTY=true \
  -v jua84-chroma:/data/chroma_db ai-research-assistant:jua84
docker logs -f jua84-rag
```

Wait for startup to complete, then stop following logs with Ctrl+C and verify:

```bash
curl --fail http://localhost:18000/health
curl --fail --max-time 45 http://localhost:18000/query \
  -H 'Content-Type: application/json' \
  -d '{"question":"What does CT-FFR measure in coronary artery disease?","n_results":3}'
```

The Ollama client uses temperature 0, an 8,192-token context, at most 1,024
generated tokens, explicit JSON-schema structured output, and the existing
35-second answer deadline. Query rewriting uses Ollama's `num_predict=100` and
the existing 10-second deadline. No automatic paid fallback is configured.
HTTP and whole-operation timeouts map to the existing 504 response.

For an existing gateway image built from JUA-65:

```bash
docker run -d --name jua84-gateway --network jua84-spike \
  -p 127.0.0.1:18080:8080 \
  -e RAG_BASE_URL=http://jua84-rag:8000 spring-mcp-gateway:local
```

Connect MCP Inspector using Streamable HTTP to `http://localhost:18080/mcp`.
Start with `resultCount=3`; also check the normal default of 8 separately.
Too much input may exceed the small model's context; do not silently truncate
retrieval or increase timeouts to hide an unsuccessful spike.

The Inspector CLI can perform the same smoke check:

```bash
npx @modelcontextprotocol/inspector --cli http://localhost:18080/mcp \
  --transport http --method tools/call --tool-name query_research_corpus \
  --tool-arg 'question=What does CT-FFR measure in coronary artery disease?' \
  --tool-arg resultCount=3
```

## Checks

```bash
.venv/bin/python -m unittest discover -v
docker exec jua84-ollama ollama list
docker exec jua84-ollama ollama ps
docker stats --no-stream jua84-ollama jua84-rag
```

On Docker Desktop for macOS this Ollama container uses CPU inference. The CPU
and RAM limits above apply to Ollama, not the entire stack. Model download size
is not runtime memory consumption. Cold and warm latency can differ.

The sample is a feasibility check, not a benchmark or evidence of parity with
Claude. The existing golden retrieval scores do not measure generated answer
quality. Validate meaning as well as JSON shape, especially insufficient-evidence
responses. The readiness endpoint does not perform an LLM call.

To stop and remove only the spike containers (preserving downloaded models and
Chroma data for subsequent runs):

```bash
docker stop jua84-gateway jua84-rag jua84-ollama
docker rm jua84-gateway jua84-rag jua84-ollama
docker network rm jua84-spike
```

## Findings

Measured on 14 September 2026 using Linux ARM64 containers on Docker Desktop
for macOS. Ollama 0.34.0, image manifest digest
`sha256:684d8674b4315fa18f4f0e973a118ec2652ed96f67563277839985175858e0ba`;
model ID `8ea75f835db9`, 1.7B, Q4_K_M, native context 8,192 tokens.
The `latest` image tag in the commands is mutable; use this digest to reproduce
the tested runtime. RAG dependencies include `langchain-ollama==1.1.0` and
`ollama==0.6.2`; `pip check` passed without upgrading existing dependencies.

The separate Chroma volume seeded 429 chunks. The RAG container received no
Anthropic credentials. Existing host and demo databases were not used.

| Request | Chunks | Wall time | Result |
| --- | ---: | ---: | --- |
| What does CT-FFR measure in coronary artery disease? First generation | 3 | 22.56 s | HTTP 200, valid response |
| Same question, warm model | 3 | 6.80 s | HTTP 200, valid response |
| What is the recommended insulin dose for a pet hamster? | 3 | 17.22 s | HTTP 200, `context_sufficient=false` |
| CT-FFR question with the gateway's normal retrieval count | 8 | 35.73 s | HTTP 504 at the existing LLM deadline |

The successful lookup answered: “CT-FFR measures the fractional flow reserve
(FFR) in coronary artery disease.” It cited `cardio-cad-ct-angiography.txt`.
This is a terse identification rather than a full explanation. The unsupported
question was correctly described as absent from the context; however,
`insufficiency_reason` was null. That is allowed by the current schema, but is
a quality limitation. Sources are assigned by the RAG service from retrieval,
not generated or independently verified by the model.

MCP Inspector CLI discovery and `query_research_corpus` with `resultCount=3`
succeeded through the unchanged JUA-65 gateway image: `isError=false`, with
the expected camelCase MCP response fields and the same answer/source.

Sampled Docker memory was approximately 2.8–2.93 GiB for Ollama and
0.78–1.16 GiB for RAG; these are observations, not measured peaks. Ollama
reported 100% CPU inference and used approximately four cores during generation.
The 1.1 GB model download therefore understates the running stack's memory use.

All 62 offline tests passed (55 existing, seven added). New checks cover client
construction without Anthropic credentials, invalid-provider rejection, public
response shape, timeout/deadline handling, and the actual ChatOllama request
serialization using an in-memory HTTP transport. In particular, per-call rewrite
limits must be nested inside Ollama's `options`; a top-level `num_predict`
binding does not express the intended request correctly.

**Conclusion:** the local ChatOllama integration works for a small smoke sample,
including the MCP boundary, but SmolLM2 under these resource limits is not yet
a drop-in replacement for normal eight-chunk gateway requests. No timeout,
retrieval default, or prompt was relaxed to make the experiment pass. No wider
model comparison or answer-quality benchmark was performed. Before adapters
or adoption, decide whether this latency/resource/quality trade-off is acceptable
and evaluate representative questions. JSON-schema enforcement proves shape,
not factual correctness.
