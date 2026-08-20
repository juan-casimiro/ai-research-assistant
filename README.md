Research Assistant (RAG)

A FastAPI service for semantic search and question-answering over ingested documents, using local embeddings, Chroma for vector storage, and an LLM (via LangChain) for grounded generation.

The test corpus is 19 open-access biomedical research articles (PubMed Central Open Access subset and equivalent open-access journals), spanning diabetes, cardiology, oncology, and an outlier cluster covering antimicrobial resistance, gut microbiome/tuberculosis, and AI-assisted diagnosis — see corpus_manifest.json for full per-article metadata, licenses, and sourcing notes. The RAG pipeline itself is domain-agnostic; biomedical literature was chosen as a corpus with genuinely dense, citation-heavy, and terminology-specific text, useful for stress-testing retrieval precision.

**Retrieval accuracy: 96.4% @ n=3, 98.2% @ n=8** on a 133-query golden QA set (111 scored), spanning direct lookup, multi-hop, cross-document distractor, and cross-document synthesis cases. BM25 hybrid search and LLM query rewriting were implemented and evaluated as opt-in additions but measured no net benefit on this corpus — see [ADR-001](./adr/001-chunking-and-retrieval.md) for the full evaluation, including one attributable regression from BM25 alone.

## Two ways to run this

| | Docker | Host |
|---|---|---|
| For | Reviewers — one command, zero setup | Development & evaluation |
| Corpus | 3 seed documents (CC BY, bundled) | Full 19-document corpus (downloaded manually) |
| Command | `docker compose up --build` | see below |
| Reproduces 96.4% / 98.2%? | No — the seed corpus has never been run through `eval_golden.py` | Yes — this is how those figures were measured |

## Run it (Docker)

```bash
cp .env.example .env   # add your ANTHROPIC_API_KEY
docker compose up --build
```

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

**The seed corpus (3 documents, bundled in the image) is a demo
convenience only.** The retrieval accuracy figures above (96.4% @ n=3,
98.2% @ n=8) were measured against the full 19-document corpus loaded
via the manual process below, run outside Docker — not against the
seed corpus. See [ADR-003](./adr/003-deployment-and-containerisation.md)
for the full reasoning behind the Docker setup, including what was
deliberately left out of it.

## Develop and evaluate (host)

This is the path the headline retrieval figures (96.4% @ n=3, 98.2% @
n=8) were measured on. It runs against the full 19-document corpus,
not the 3-document Docker seed corpus.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

`.env`:
ANTHROPIC_API_KEY=your-key-here


**Confirm `SEED_ON_EMPTY=false` in your `.env`.** Docker pins
`SEED_ON_EMPTY=true` for reviewers regardless of what's in `.env` (see
`docker-compose.yml`), but nothing overrides it on the host. Leaving it
unset or `true` here will auto-ingest the 3-document seed corpus
alongside the full corpus you're about to load below — not instead of
it — silently duplicating articles under two filenames and skewing
retrieval results.

Start the server:

```bash
uvicorn main:app --reload
```

In a separate terminal, populate the full corpus. The PDFs aren't
committed to this repo (see `.gitignore`) — some articles carry NC/ND
license terms, so downloading is a manual step by design:

1. Open `corpus_manifest.json`. Each entry lists a `doi` and a `filename`.
2. For each article, resolve the DOI (e.g. `https://doi.org/<doi>`) and
   download the PDF from the publisher/journal page.
3. Save it into `./corpus/` using the **exact filename** from the
   manifest (e.g. `diabetes-cgm-management.pdf`) — `ingest_corpus.py`
   matches files by this name.
4. Ingest everything:

```bash
python reset_collection.py    # resets the vector store (safe on a fresh clone)
python ingest_corpus.py       # ingests every PDF listed in the manifest
```

   Expect one `INGESTED` line per file; `SKIP (file not found)` means
   that PDF hasn't been downloaded yet.

### Retrieval evaluation

```bash
python eval_golden.py [--bm25] [--rewrite]
```

Runs the golden QA evaluation harness (`golden_qa.json`, 133 queries,
111 scored across 4 categories plus unanswerable) against the live
`retrieve()` pipeline — evaluation always tests the exact code path
used in production. Results are written to `eval_results.json` with a
config label and per-query verdicts. See
[ADR-002](./adr/002-evaluation-methodology.md) for the category design
and scoring logic.

```bash
python compare_evals.py <baseline.json> <experiment.json>
```

Diffs two result files and prints per-query pass/fail flips, for
isolating the effect of a single change.

Raw per-query results for all four tested configurations are committed
under `eval_results/` for inspection: `eval_results_baseline.json`,
`eval_results_bm25.json`, `eval_results_rewrite.json`, and
`eval_results_bm25_rewrite.json`.


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
- **LangChain** (`init_chat_model`) — provider-agnostic LLM access for
  grounded generation, opt-in query rewriting, and structured output.
  The provider is a single model-string constant (`LLM_MODEL`); switching
  providers means changing that string and installing the matching
  integration package (e.g. `langchain-openai`)


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
corpus expanded from 16 to 19 documents (outlier cluster).


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
