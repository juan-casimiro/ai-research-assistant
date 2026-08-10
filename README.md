Research Assistant (RAG)

A FastAPI service for semantic search and question-answering over ingested documents, using local embeddings, Chroma for vector storage, and Claude for grounded generation.

The test corpus is 22 open-access biomedical research articles (PubMed Central Open Access subset and equivalent open-access journals), spanning diabetes, cardiology, oncology, and an outlier cluster covering antimicrobial resistance, gut microbiome/tuberculosis, and AI-assisted diagnosis — see corpus_manifest.json for full per-article metadata, licenses, and sourcing notes. The RAG pipeline itself is domain-agnostic; biomedical literature was chosen as a corpus with genuinely dense, citation-heavy, and terminology-specific text, useful for stress-testing retrieval precision.

## Features

- **POST /ingest** — chunk and embed a document, storing it for retrieval
- **POST /query** — retrieve relevant chunks for a question and generate
  a grounded answer, citing sources

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
├─ [if use_query_rewriting]  Claude rewrites the question,
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
Chunks + question → Claude → grounded answer + sources
```
BM25 and query rewriting are opt-in (use_bm25, use_query_rewriting on /query, both default False) — see ADR-001 for why they're not enabled by default. The diagram above shows the full pipeline with both enabled; with both off, retrieval is dense search → reranking only.

## Tech stack

- **FastAPI** — async web framework
- **FastEmbed** (`bge-small-en-v1.5`) — local, ONNX-based embeddings, no API cost
- **Chroma** — embedded-mode vector database, no server required
- **rank_bm25** (`BM25Okapi`) — in-memory sparse lexical retrieval, fused
  with dense search via reciprocal rank fusion (opt-in, `use_bm25`)
- **Anthropic SDK** — Claude for grounded generation, and for opt-in
  query rewriting (`use_query_rewriting`)


## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

`.env`:
ANTHROPIC_API_KEY=your-key-here

## Running

```bash
uvicorn main:app --reload
```

## Design decisions and known limitations
 
See [ADR-001](./adr/001-chunking-and-retrieval.md) for the full history:
chunking approach, the two-stage retrieval pipeline (dense embeddings +
cross-encoder reranking), BM25 hybrid search via reciprocal rank fusion,
and LLM-based query rewriting — including a full evaluation of BM25 and
rewriting against the golden QA set, with results and the decision to
keep both opt-in rather than default-on.

See [ADR-002](./adr/002-evaluation-methodology.md) for the golden QA
category design (what each of the five categories tests, and the
scoring logic behind them) and the evaluation harness's known
limitations.
 
In short: two-stage retrieval (embeddings + reranking) scores 96.4%
(n=3) / 98.2% (n=8) on the golden QA set (133 queries, 111 scored). BM25
and query rewriting were implemented and evaluated as opt-in additions
but did not improve retrieval on this corpus — see ADR-001 for the full
breakdown, including one attributable regression from BM25 alone and
why combining it with rewriting recovered it, re-confirmed after the
corpus expanded to 22 documents.


## Retrieval evaluation

`python eval_golden.py [--bm25] [--rewrite]` runs the golden QA
evaluation harness (`golden_qa.json`, 133 queries, 111 scored across 4
categories plus unanswerable) against the live `retrieve()` pipeline, so
evaluation always tests the exact code path used in production. Results
are written to `eval_results.json` with a config label and per-query
verdicts.

`python compare_evals.py <baseline.json> <experiment.json>` diffs two
result files and prints per-query pass/fail flips, for isolating the
effect of a single change.

Raw per-query results for all four tested configurations are committed
under `eval_results/` for inspection: `eval_results_baseline.json`,
`eval_results_bm25.json`, `eval_results_rewrite.json`, and
`eval_results_bm25_rewrite.json`.

## Possible future improvements

- Isolate BM25 as a standalone retrieval signal (no vector search in the
  fusion) to measure lexical-only retrieval quality on this corpus,
  separate from the "does adding BM25 to vector help" question already
  answered
- Add eval queries where dense retrieval + reranking demonstrably fails
  and lexical exact-match would succeed, to test BM25's upside fairly
  (the current BM25-favoring queries already pass on vector-only)
- HyDE (Hypothetical Document Embeddings) or corpus-aware query rewriting,
  as a way to address vocabulary-specific mismatches that generic
  rewriting does not fix (see ADR-001)
- File upload endpoint (currently text-only via JSON)
