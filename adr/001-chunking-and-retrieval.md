# ADR-001: Chunking Strategy and Retrieval Limitations

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

## Consequences

- The system reliably answers general/broad questions grounded in ingested content (verified: correctly summarized the paper's risk categories from retrieved context).
- The system can fail to retrieve highly specific facts embedded in citation-dense passages, even when that content exists in the corpus.
When this happens, the LLM correctly reports it cannot answer from the given context, rather than hallucinating — the failure mode is  a retrieval gap, not a generation/grounding failure.
- **Known limitation, documented as future work, not implemented:**
  reranking (retrieve a broader candidate set with the fast embedding model, then re-score with a slower, more precise cross-encoder) is the standard technique for this exact failure mode and would likely
  improve results on specific factual queries.
- **Known limitation:** chunk size and overlap values are initial, reasonable defaults based on general guidance, not tuned against this
  project's specific corpus or query patterns.
