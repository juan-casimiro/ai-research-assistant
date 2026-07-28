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

## Update: Retrieval evaluation findings (Session 2)

A retrieval evaluation harness was built (`eval_retrieval.py`) — a small,
hand-labeled test set of queries with expected keywords per query,
scored with a strict `all()` match (all expected keywords must appear
in retrieved context, not just any one) to avoid an earlier, overly
lenient version of this check that produced misleadingly high scores.

Tested against three different real documents:

| Document | Structure | Accuracy @ n=3 | Accuracy @ n=8 |
|---|---|---|---|
| AI-in-education paper | Real paragraph breaks | 62% (5/8) | 62% (5/8) |
| "Attention Is All You Need" | Little/no paragraph structure (required a chunking bug fix — see below) | Not fully evaluated | Severe miss persisted even at n=8 |
| Autism/AI equity review | Clean paragraph structure, narrative prose | 80% (4/5) | 100% (5/5) |

**Key finding: retrieval difficulty depends heavily on source document
structure and writing style, not only on chunk size or embedding model.**
Well-structured narrative prose (the equity review paper) was
comfortably retrievable by broadening `n_results` alone. Citation-dense,
LaTeX-typeset technical text (the Transformer paper) showed a much more
severe failure mode — the correct chunk did not surface even at
`n_results=8` out of 71 chunks, meaning the miss was a genuine precision
gap, not just a "needs more results" problem.

**Bug found and fixed during this testing**: `chunk_text()` lacked the
hard-split fallback for oversized single "paragraphs" (present in the
Document Summariser project, but omitted when this project's chunker
was written fresh). The Transformer paper's PDF extracted with no
double-newline paragraph breaks at all, causing the entire ~32,000
character document to be treated as one chunk before the fallback was
added back.

**Confirmed, still-unaddressed limitation**: for documents with severe
retrieval misses (the Minnesota Law School case), broadening
`n_results` does not help — this specifically requires reranking or a
larger/better embedding model, neither implemented in this session.

## Update: Reranking implementation and results (Session 3)

Implemented two-stage retrieval: broad candidate retrieval via
embeddings (`n_results=20`), followed by reranking with a cross-encoder
(`Xenova/ms-marco-MiniLM-L-6-v2`, via FastEmbed) to re-score and select
the final top-N. The retrieval logic was refactored into a shared
`retrieve()` function used by both the `/query` endpoint and the
evaluation harness, ensuring evaluation tests the exact same code path
as production — avoiding drift between what is measured and what is
shipped.

**Result, tested against the same 8-query evaluation set used in
Session 2 (AI-in-education paper):**

| Configuration | Accuracy |
|---|---|
| Embeddings only, n_results=3 | 62% (5/8) |
| Embeddings only, n_results=8 | 62% (5/8) |
| Embeddings + reranking, n_results=8 | 75% (6/8) |

Reranking resolved the Minnesota Law School case — the specific,
citation-dense factual query that broadening `n_results` alone could
not fix (Session 2 finding). This confirms the hypothesized mechanism:
the relevant chunk existed within the top-20 embedding-retrieved
candidates, but was not ranked highly enough by fast embedding
similarity alone; the more precise (but slower) cross-encoder correctly
identified it once given the opportunity to evaluate the candidate set
directly. No regressions were observed — all previously-passing queries
remained correct.

**Remaining limitation:** two queries (disabilities/neurodivergent
support, and bias) were not resolved by reranking. Hypothesis, not yet
tested: these queries use vocabulary that differs from the source
paper's own phrasing (e.g., the paper uses "EDI" as a section heading
rather than "disabilities," and describes a "left-libertarian
orientation" rather than "bias" as a plain term). Reranking improves
selection *among retrieved candidates* but cannot recover a chunk whose
content doesn't share query vocabulary in a form the model recognizes
as relevant — this points to query rewriting/expansion as a distinct,
separate technique from reranking, not yet implemented.

**Trade-off, worth noting:** reranking adds a second model inference
pass per query (cross-encoder scoring of 20 candidates), increasing
latency compared to embeddings-only retrieval. Not benchmarked
precisely in this session, but a real, expected cost of the accuracy
gain — consistent with reranking's known trade-off profile.

## Update: Query rewriting — implemented, evaluated, not enabled by default

Query rewriting (using Claude to reformulate the question toward more
formal/academic phrasing before retrieval, then merging results from
both the original and rewritten query before reranking) was
implemented and tested against the same 8-query evaluation set.

**Result: identical to reranking alone (75% at n=8) — no additional
queries were fixed.**

Diagnosis: the two remaining failures (disabilities/EDI, bias) are
vocabulary-specific mismatches — the source paper uses "EDI" and
"left-libertarian orientation" rather than "disabilities" or "bias."
Inspecting the actual rewrites Claude produced confirmed this: they
were well-formed, plausible academic paraphrases (e.g., "accessibility
accommodations," "algorithmic bias and fairness concerns"), but never
landed on the paper's specific terminology. This is a structural
limitation, not a prompting failure — Claude has no access to the
source corpus, so it can only guess at "how a formal source would
phrase this" in general, not "how *this* source actually phrased it."

This suggests query rewriting without corpus awareness helps with
*register* mismatches (casual vs. formal phrasing) but not *specific
vocabulary* mismatches — a different failure mode, better addressed by
techniques such as HyDE (Hypothetical Document Embeddings, where a
generated hypothetical answer is embedded instead of the question
itself) or corpus-aware rewriting (extracting real vocabulary from an
initial broad retrieval pass to inform the rewrite). Neither is
implemented in this session.

**Decision:** kept as an opt-in parameter (`use_query_rewriting`,
default `False`) rather than the default retrieval path, since it adds
real latency and cost (an additional LLM call) with no measured benefit
on this corpus. Available for cases where register mismatch, rather
than vocabulary specificity, is the dominant retrieval problem.

**Implementation note:** mixing synchronous and asynchronous retrieval
paths (single retrieval vs. dual retrieval-with-rewriting) introduced
two real bugs during development — a missing `await` on the `retrieve()`
call site, and a mismatched sync/async calling convention on
`_retrieve_candidates` depending on which code path executed. Both were
caught before shipping. This reinforces a recurring lesson from this
project: once any function in a call chain becomes `async def`, every
caller up the chain must be updated consistently — partial conversions
are a common, easy-to-miss source of bugs.