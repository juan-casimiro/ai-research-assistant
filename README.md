# Research Assistant (RAG)

A FastAPI service for semantic search and question-answering over
ingested documents, using local embeddings, Chroma for vector storage,
and Claude for grounded generation.

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

Question
│
▼
Embed the question (same model)
│
▼
Retrieve top-N most similar chunks
│
▼
Chunks + question → Claude → grounded answer + sources
```

## Tech stack

- **FastAPI** — async web framework
- **FastEmbed** (`bge-small-en-v1.5`) — local, ONNX-based embeddings, no API cost
- **Chroma** — embedded-mode vector database, no server required
- **Anthropic SDK** — Claude for grounded generation

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

See [ADR-001](./adr/001-chunking-and-retrieval.md). In short: retrieval
works well for broad questions but can miss highly specific facts in
citation-dense text, due to the local embedding model's precision
limits. Reranking is identified as the standard next step to address
this, not yet implemented.

## Possible future improvements

- Reranking step (cross-encoder re-scoring of a broader candidate set)
- File upload endpoint (currently text-only via JSON)
- Comparison against a larger embedding model or OpenAI embeddings
- Query rewriting/expansion for better recall on narrow factual questions