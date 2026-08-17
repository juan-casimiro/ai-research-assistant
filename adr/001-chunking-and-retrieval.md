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

(**Superseded**: this early 8-query harness, `eval_retrieval.py`, was
later replaced by the category-aware `eval_golden.py` harness against
`golden_qa.json` — see the Hybrid Search Evaluation section below and
[ADR-002](./002-evaluation-methodology.md) for the current, much larger
evaluation set and its scoring logic. `eval_retrieval.py` has been
removed from the repo; kept here only as a historical record of how
evaluation started.)

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

**Correction (Session 4):** direct inspection of retrieved candidates
revealed the two remaining failures are not the same failure mode.
The "disabilities" query is a genuine **recall** failure — the
relevant chunk (discussing support for neurodivergent students) does
not appear anywhere in the top-20 embedding-retrieved candidates, so
no amount of reranking can recover it; reranking only reorders
candidates that were already retrieved. The "bias" query is closer to
a **precision/selection** issue — the relevant EDI paragraph was
present among the retrieved candidates, so its continued absence from
the final top-N is a ranking/selection question, not a retrieval-recall
one. This distinction matters because the two failure modes call for
different fixes: recall failures need either a better embedding model
or a larger candidate pool (n_results in the initial retrieval stage,
not the final n_results), while precision failures are exactly what
reranking is meant to address.

## Hybrid Search Evaluation (BM25 + Query Rewriting)

### Context

Following the baseline vector-only evaluation, BM25 sparse retrieval (via
reciprocal rank fusion, k=60) and LLM-based query rewriting were already
implemented as opt-in flags on `/query` (`use_bm25`, `use_query_rewriting`).
They were evaluated against the golden QA set (103 scored queries, 4
categories) in isolation and combined, to measure their actual effect
rather than assume a hybrid approach would outperform vector-only search.

New `cross_doc_distractor` queries were added to `golden_qa.json`
specifically to exercise exact-term matching (model names, biomarkers,
numeric thresholds) where BM25 should have a structural advantage over
dense embeddings.

Both flags are strictly additive to vector search, never a replacement
for it. `retrieve()`'s internal `_fetch_all` always runs dense retrieval;
`use_bm25=True` adds a BM25 candidate list alongside it via
`asyncio.gather`, and `use_query_rewriting=True` repeats the entire
`_fetch_all` step a second time on the rewritten query. All resulting
lists are fused together in one `reciprocal_rank_fusion` call before
reranking — so "BM25 enabled" means "vector + BM25 fused," and
"BM25 + rewrite" means four ranked lists (original-dense, original-BM25,
rewritten-dense, rewritten-BM25) fused at once, not BM25 running alone
at any point.

### Results

| Config                 | n=3 overall     | n=8 overall     | Δ vs baseline |
|------------------------|-----------------|------------------|---------------|
| vector-only (baseline) | 99/103 (96.1%)  | 101/103 (98.1%)  | —             |
| BM25 only              | 98/103 (95.1%)  | 100/103 (97.1%)  | **−1**        |
| rewrite only           | 99/103 (96.1%)  | 101/103 (98.1%)  | 0             |
| BM25 + rewrite         | 99/103 (96.1%)  | 101/103 (98.1%)  | 0             |

Full per-query results for all four configurations are committed under
`eval_results/` for inspection.

### Findings

1. **Neither technique improved retrieval on this corpus.** Query
   rewriting alone produced zero verdict changes across all 103 queries at
   both n=3 and n=8 — the rewritten queries retrieved byte-identical
   source lists to the original phrasing in every case tested.

2. **BM25 alone caused one regression.** Query q008 ("What HbA1c level or
   role does HbA1c play in relation to diabetic complications like
   retinopathy or nephropathy?") flipped pass→fail at both n=3 and n=8.
   The distractor document (`diabetes-pharmacotherapy-rct.pdf`) is an RCT
   whose primary subject is HbA1c reduction — dense, repeated use of the
   query's exact terms. In the two-list fusion (dense + BM25), BM25's
   term-frequency signal ranked the distractor above the correct document
   (`diabetes-epidemiology-prevalence.pdf`), inverting an ordering that
   vector search got right by weighting semantic intent ("HbA1c's role in
   complications") over raw lexical overlap. This is the predictable
   failure mode of lexical retrieval against a distractor that happens to
   be topically dense in the query's own vocabulary.

3. **Combining BM25 with rewriting recovered the regression.** With both
   enabled, q008 passed again. Confirmed against the code: the rewrite
   path expands the fusion from 2 ranked lists to 4 (original-dense,
   original-BM25, rewritten-dense, rewritten-BM25). Confirmed separately
   that rewriting alone (no BM25) leaves q008 byte-identical to baseline —
   isolating the fix to the larger fused candidate pool diluting BM25's
   single-query term-frequency pull, not to any change in what the
   rewritten query itself retrieves.

4. **The two known hard failures (q044, q050) did not move under any
   configuration.** Neither BM25, rewriting, nor the combination changed
   their verdicts. Having now tested three retrieval strategies against
   them without effect, these are best characterized as genuine embedding
   space / semantic ambiguity cases rather than a retrieval-strategy gap.

5. **The BM25-favoring queries did not exercise BM25's advantage.**
   Queries added specifically to showcase lexical exact-match
   (`q120`–`q124`: exact model names, biomarker tokens, numeric
   thresholds) already passed under vector-only search plus cross-encoder
   reranking — the reranker's contextual scoring was sufficient to
   surface them without needing lexical retrieval. The current eval set
   can demonstrate BM25's downside (q008) but not a clear upside.

### Decision

**`use_bm25` and `use_query_rewriting` remain opt-in and default to
`False`.** On this corpus and query set, hybrid search did not provide a
measurable net benefit and introduced one attributable regression in
isolation. Enabling it by default would trade a proven vector-only
baseline for added latency and complexity without evidence of improved
retrieval quality. The RRF fusion, BM25 index, and rewrite path remain
fully implemented and available for callers who want them (e.g. corpora
with more acronym-, ID-, or number-dense content than this one), and the
opt-in design means this decision can be revisited per-corpus without a
code change.

### Limitations of this evaluation

- Single corpus (19 biomedical papers, 4 topic clusters). Results may not
  generalize to corpora with denser exact-term retrieval needs (legal,
  codebases, structured IDs).
- **BM25 was not evaluated in isolation from vector search.** Every
  configuration includes the dense retrieval list in the fusion; no run
  tested BM25 as the sole retrieval signal. This would require a
  `retrieve()` change to skip dense retrieval entirely and is left as
  future work — it would answer "how good is lexical-only retrieval on
  this corpus" rather than "does adding BM25 to vector search help,"
  which is the question this evaluation actually answers.
- The rewrite-alone null result is based on this query set's phrasing
  gap being small; the rewrite prompt targets academic-vs-conversational
  terminology mismatches, which this golden set's queries mostly already
  avoid.

### Update: re-confirmed on expanded corpus (22 documents, 133 queries)

The same four configurations were re-run after the corpus and golden QA
set grew to 22 documents and 133 queries (111 scored). Results:

| Config                 | n=3 overall     | n=8 overall     | Δ vs baseline |
|------------------------|-----------------|------------------|---------------|
| vector-only (baseline) | 107/111 (96.4%) | 109/111 (98.2%)  | —             |
| BM25 only              | 106/111 (95.5%) | 108/111 (97.3%)  | **−1**        |
| rewrite only           | 107/111 (96.4%) | 109/111 (98.2%)  | 0             |
| BM25 + rewrite         | 107/111 (96.4%) | 109/111 (98.2%)  | 0             |

q008 is again the only query affected across all three configurations,
with the identical regress-under-BM25/recover-under-combined pattern
described above. No other query — including the queries added for the
expanded corpus — was affected by any configuration. This confirms the
original finding is a stable property of this pipeline and this query,
not an artifact of corpus size, and supports the decision to keep both
flags opt-in.

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
`eval_results/eval_results_baseline.json`, where `unanswerable` queries
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


### Known limitations (both measured, not hypothetical)

1. **Two states are sometimes too few.** A query against
   `cardio-mi-risk-stratification.pdf` asking which lab marker was used
   returned `false` — correctly, since the marker isn't named — but the
   answer was grounded, accurate, and useful. Consumers cannot
   distinguish "partial answer from the right document" from "total
   retrieval miss." An enum was considered and rejected: no clean third
   state is definable without a consumer that needs it.

2. **False-premise questions diverge from the golden labels.** `q083`
   presupposes an FDA validation that doesn't exist. The model rejected
   the premise and answered what the corpus does establish, returning
   `true`, while the golden set labels the query `unanswerable`. Both
   readings are defensible: the flag answers "was this context enough to
   produce a good answer," the label answers "does the corpus contain the
   requested fact." For the flag's actual consumer — a retry decision —
   `true` is the better outcome, since retrying would discard a correct
   answer.

3. **The flag depends on LLM self-assessment**, which is not perfectly
   reliable in either direction.