# ADR-001: Chunking Strategy and Retrieval Limitations

## Update: Offload blocking reranker inference from the event loop

The cross-encoder is a blocking inference call inside the asynchronous
`retrieve()` path. Both calling `reranker.rerank()` and consuming its lazy
scores now run inside `await asyncio.to_thread(lambda:
list(reranker.rerank(question, fused)))`. A single inference pass retains
the existing candidate pool, score sorting, top-N selection, and source
ordering.

This is an event-loop correctness decision: the event loop can yield while
inference runs in a worker thread. It is not a claim that `to_thread()` itself
provides multi-core execution or establishes a measured optimization gain.

The normal workload measured for this change continued increasing throughput
through concurrency 8 and did not establish a saturation threshold or a
performance-derived concurrency ceiling. The before baseline had only one
run, so the before/after difference is not evidence of an optimization gain.
The artificial five-pass rerank experiment was diagnostic only; its CPU and
RSS figures are neither a normal service footprint nor evidence for a
capacity ceiling. Production performs only one rerank pass. Detailed
measurements are retained in the corresponding task record.

Any downstream bulkhead value remains a separate protection or cost policy
decision, rather than a measured saturation threshold. Model-cache behavior
(persisting the FastEmbed/Hugging Face cache across restarts) is outside this
change and remains a separate follow-up.

## Context

RAG requires splitting documents into chunks small enough to embed and retrieve precisely, while preserving enough context for the LLM to generate a good answer. This is a different problem from the chunking done in the Document Summariser project — here, chunk boundaries directly affect *what can be found at all*, not just summary quality.

## Constraints (real vs. anticipated)

- **Real:** PDF text extraction includes repeated running headers/footers (page numbers, journal title) that can land in the middle of a sentence at page boundaries — verified directly: a chunk boundary split the sentence "ChatGPT achieved an [header text] average grade of C+" across two chunks, making the actual finding unretrievable as a complete unit in the initial (no-overlap) implementation.

- **Real:** small, local embedding models (`bge-small-en-v1.5`, 384 dimensions) have genuine precision limits on citation-dense, highly specific factual content. Verified directly: a targeted factual query
  ("What did the University of Minnesota Law School study find about
  ChatGPT?") failed to retrieve the relevant chunk even at `n_results=8`
  (out of 71 total chunks), despite the chunk containing the answer existing in the corpus.
- **Anticipated, not confirmed:** whether a larger embedding model or a reranking step would resolve the above — not tested in this session,
  documented as a follow-up.

## Decision

1. **Chunk size**: 1,000 characters (~250 tokens), within the commonly
   cited 256-512 token range for general-purpose RAG, though on the smaller end — appropriate for fact-based retrieval per current
   guidance, which favors smaller chunks for precise queries.
2. **Overlap**: added a 150-character overlap between chunks, to reduce
   the risk of a fact splitting across a chunk boundary (as observed with the PDF header issue above). Note: overlap's benefit is not
   universally agreed upon — at least one 2026 benchmark found no measurable retrieval improvement from overlap in their setup. This
   project's own header-splitting case is a concrete instance where
   overlap plausibly helped, but this hasn't been rigorously A/B tested here.

3. **Embedding model**: `bge-small-en-v1.5` via FastEmbed (ONNX-based, no PyTorch dependency, ~32MB quantized) — chosen for zero cost and minimal resource footprint over an API-based alternative (OpenAI embeddings). This is a deliberate trade-off: acceptable for portfolio purposes, with a known, demonstrated precision ceiling on specific factual retrieval.

## Initial consequences (historical; reranking subsequently implemented)

- The system reliably answers general/broad questions grounded in ingested content (verified: correctly summarized the paper's risk categories from retrieved context).
- The system can fail to retrieve highly specific facts embedded in citation-dense passages, even when that content exists in the corpus.
When this happens, the LLM correctly reports it cannot answer from the given context, rather than hallucinating — the failure mode is  a retrieval gap, not a generation/grounding failure.
- **Known limitation, documented as future work, not implemented:**
  reranking (retrieve a broader candidate set with the fast embedding model, then re-score with a slower, more precise cross-encoder) is the standard technique for this exact failure mode and would likely
  improve results on specific factual queries.
- **Known limitation:** chunk size and overlap values are initial, reasonable defaults based on general guidance, not tuned against this
  project's specific corpus or query patterns.

## Current retrieval path and strategy evidence

Production `retrieve()` searches dense top-20 candidates, optionally adds BM25
and an LLM-rewritten query, fuses enabled lists with reciprocal rank fusion
(k=60), then reranks with `Xenova/ms-marco-MiniLM-L-6-v2` to select top-N.
BM25 and rewriting add to dense search; neither is lexical-only retrieval.
Both remain opt-in and default to `False`.

The [current 55-article / 158-query strategy findings](../data/evaluations/mvp/2026-10-09-anthropic/comparison/findings.md)
record modest, category-dependent evidence gains and regressions in one sweep.
They do not establish a stable strategy ranking or answer accuracy. Scoring
semantics belong in [ADR-002](002-evaluation-methodology.md).

The [historical retrieval experiments](../data/archive/v1/retrieval-history.md)
preserve the early keyword checks, reranking development and V1 strategy tables,
including the BM25 regression and combined-run recovery. Those experiments
motivated the opt-in default; they are not current benchmark results.

## Update: LangChain replaces the Anthropic SDK

Both LLM call sites (grounded answering, query rewriting) moved from
`anthropic.AsyncAnthropic` to LangChain's `init_chat_model`. The provider
is now one model-string constant instead of an SDK choice spread across
code.

**Honest scope:** this makes the *code* provider-agnostic, not the
dependency tree — `anthropic` remains installed transitively via
`langchain-anthropic`, and switching providers also requires installing
the target integration package. What changes is that no repo code
imports a vendor SDK.

Verified non-regressive: `eval_golden.py --rewrite` produced no per-query
verdict changes across 111 scored queries at n=3 and n=8, covering both
the LLM call paths and a concurrent upgrade of the retrieval stack
(`fastembed`, `chromadb`). Note the harness compares verdicts, not raw
`retrieved_sources` ordering.

## Update: `sources` now preserves reranked order

`/query` previously deduplicated `sources` with `list(set(sources))`.
Python sets don't preserve insertion order, so the response silently
discarded the cross-encoder's relevance ranking — the same order
`sources` is documented (and, since this fix, correctly) as reflecting.

**Fix:** `list(dict.fromkeys(sources))`. Dicts preserve insertion order
(Python 3.7+), so the first — i.e. most relevant, post-rerank —
occurrence of each source is kept, and later duplicate chunks from the
same document are dropped without disturbing order.

**Correction to a note above:** the "harness compares verdicts, not raw
`retrieved_sources` ordering" note (LangChain migration update) is still
true of the evaluation harness, but should not be read as "sources
order carries no meaning" — it never carried meaning *at the API layer*
only because of this bug, not by design. The response contract (README)
has been updated accordingly.

## Update: `context_sufficient` — retrieval sufficiency as structured output

### The problem: source-emptiness is not a retrieval-failure signal

Chroma's `collection.query()` returns the n nearest neighbours by
distance with **no relevance cutoff** — there is always a "nearest"
chunk. `retrieve()` returns empty lists only when `ranked_lists` is
entirely empty (empty corpus or transient failure), never on a relevance
miss.

Measured: "What is the capital of Peru?" returns a correct refusal
alongside `sources: ["outlier-amr-surveillance.pdf"]`. Corroborated by
[eval_results_baseline.json](../data/archive/v1/evaluations/eval_results_baseline.json), where `unanswerable` queries
return fully-populated `retrieved_sources`.

**The failure mode is low-relevance results, not zero results.**

### Decision

The answering model is the only component that reads the chunks
*alongside* the question, and it already makes the sufficiency judgement
correctly — it was just trapped in prose. `/query` now captures it via
`with_structured_output` over a `GroundedAnswer` schema, returning
`context_sufficient` and an optional `insufficiency_reason`.

Field order in the schema is deliberate (`answer` before the flag) so the
judgement follows the answer rather than preceding it.


The flag is the answering model's self-assessment, not an independently judged
quality score. A useful partial answer can still report insufficient context;
correcting a false premise can report sufficient context even when the requested
fact is absent. The [historical sufficiency experiment](../data/archive/v1/retrieval-history.md#historical-sufficiency-flag-experiment)
records the prompt refinement, observed errors and saved-evidence limits.
Current retrieval evaluation does not judge this flag or generated answers.
