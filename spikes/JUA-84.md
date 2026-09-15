# Local LLM feasibility spike

September 2026: running SmolLM2-1.7B-Instruct (Q4_K_M) locally through LangChain
ChatOllama is feasible. The Docker experiment successfully answered a RAG query
directly and through the MCP gateway, and returned an insufficient-context
response for an unsupported question.

With CPU inference on Docker Desktop for macOS, a three-chunk request took
22.56 seconds initially and 6.80 seconds when repeated warm. The same question
with the normal eight-chunk retrieval count exceeded the existing 35-second
LLM deadline and returned HTTP 504. The repeated request may also benefit from
prompt caching; it does not predict latency for new questions.

Sampled memory use was approximately 2.8–2.93 GiB for Ollama and 0.78–1.16 GiB
for RAG. These were observations, not peak measurements. All 62 offline tests
passed, but the small smoke sample does not establish answer quality or
production suitability.

Local integration is promising, with timeout and resource limitations.
Production adapters, representative quality checks, and evaluation of model
warmup remain follow-up work. Full measurements, setup instructions, and
development references are recorded in [JUA-84](https://linear.app/juan-casimiro-agent/issue/JUA-84/spike-verify-local-chatollama-with-smollm2-in-the-rag-service).
