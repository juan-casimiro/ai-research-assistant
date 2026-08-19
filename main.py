import asyncio
import os
import re
from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from fastembed import TextEmbedding
from fastembed.rerank.cross_encoder import TextCrossEncoder
import chromadb
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from rank_bm25 import BM25Okapi

load_dotenv()

LLM_MODEL = "anthropic:claude-haiku-4-5-20251001"
CHROMA_PATH = os.getenv("CHROMA_PATH", "./chroma_db")
SEED_CORPUS_DIR = Path(os.getenv("SEED_CORPUS_DIR", "./seed_corpus"))
SEED_ON_EMPTY = os.getenv("SEED_ON_EMPTY", "true").lower() != "false"

# Built during startup, not at import time — see lifespan below.
embed_model = None
reranker = None
chroma_client = None
collection = None
llm = None

_ready = False
_startup_error: str | None = None

bm25_index: BM25Okapi | None = None
bm25_documents: list[str] = []
bm25_sources: list[str] = []

FUSED_CANDIDATE_POOL = 20  # cap before reranking — bounds cross-encoder latency

def _log(message: str) -> None:
    """Startup/seed progress — plain stdout, visible in the same terminal
    running `uvicorn`, interleaved with its own request logs."""
    print(f"[startup] {message}")


def _load_models() -> None:
    """Blocking model construction — runs in a worker thread, not the event loop."""
    global embed_model, reranker, chroma_client, collection, llm
    _log("loading embedding model (FastEmbed bge-small-en-v1.5)...")
    embed_model = TextEmbedding()
    _log("loading cross-encoder reranker (Xenova/ms-marco-MiniLM-L-6-v2)...")
    reranker = TextCrossEncoder(model_name="Xenova/ms-marco-MiniLM-L-6-v2")
    _log(f"connecting to Chroma at {CHROMA_PATH}...")
    chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = chroma_client.get_or_create_collection("documents")
    _log(f"collection ready — {collection.count()} chunks already stored")
    _log(f"initializing LLM client ({LLM_MODEL})...")
    llm = init_chat_model(LLM_MODEL, max_tokens=1024)
    _log("models loaded")


def _seed_if_empty() -> int:
    """First run only: ingest the committed demo corpus into an empty store."""
    if collection.count() > 0:
        _log("collection already has data — skipping seed corpus")
        return 0
    _log(f"collection is empty — seeding from {SEED_CORPUS_DIR}...")
    seeded = 0
    for path in sorted(SEED_CORPUS_DIR.glob("*.txt")):
        text = path.read_text(encoding="utf-8")
        if not text.strip():
            _log(f"  skipping {path.name} — empty file")
            continue
        chunks = chunk_text(text)
        collection.add(
            ids=[f"{path.name}_{i}" for i in range(len(chunks))],
            embeddings=[embed(c) for c in chunks],
            documents=chunks,
            metadatas=[{"source": path.name} for _ in chunks],
        )
        _log(f"  seeded {path.name} — {len(chunks)} chunks")
        seeded += 1
    _log(f"seeding complete — {seeded} document(s) added")
    return seeded

def _load_models_and_index() -> None:
    """Build models and the BM25 index, synchronously.

    Used by two callers with different needs:
      - _startup() calls this, then optionally seeds, then rebuilds the BM25
        index a second time so seeded chunks are included.
      - Scripts that import main directly without going through the ASGI
        app (e.g. eval_golden.py) call this alone — they assume the
        corpus is already populated and deliberately skip seeding.
    """
    _load_models()
    _log("building BM25 index...")
    _rebuild_bm25_index()
    _log(f"BM25 index built — {len(bm25_documents)} chunks indexed")


def _startup() -> None:
    global _ready, _startup_error
    _log("startup beginning (background thread)")
    try:
        _load_models_and_index()
        if SEED_ON_EMPTY:
            seeded = _seed_if_empty()
            if seeded:
                _log("rebuilding BM25 index to include seeded chunks...")
                _rebuild_bm25_index()
        else:
            _log("SEED_ON_EMPTY=false — skipping seed check")
        _ready = True
        _log(f"startup complete — ready, {collection.count()} chunks total")
    except Exception as exc:
        _startup_error = f"{type(exc).__name__}: {exc}"
        _log(f"startup FAILED — {_startup_error}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(asyncio.to_thread(_startup))
    yield


app = FastAPI(lifespan=lifespan)

def _require_ready() -> None:
    if _startup_error:
        raise HTTPException(status_code=503, detail=f"startup failed: {_startup_error}")
    if not _ready:
        raise HTTPException(status_code=503, detail="models still loading")


@app.get("/health")
def health():
    if _startup_error:
        return JSONResponse(status_code=503, content={"status": "error", "detail": _startup_error})
    if not _ready:
        return JSONResponse(status_code=503, content={"status": "loading"})
    return {"status": "ready", "chunks": collection.count()}

def _tokenize(text: str) -> list[str]:
    return re.findall(r"\w+", text.lower())


def _rebuild_bm25_index() -> None:
    global bm25_index, bm25_documents, bm25_sources
    data = collection.get()
    bm25_documents = data["documents"]
    bm25_sources = [m["source"] for m in data["metadatas"]]
    bm25_index = (
        BM25Okapi([_tokenize(doc) for doc in bm25_documents])
        if bm25_documents
        else None
    )

def embed(text: str) -> list[float]:
    return list(embed_model.embed([text]))[0].tolist()


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 150) -> list[str]:
    paragraphs = re.split(r"\n\s*\n", text)
    chunks: list[str] = []
    current = ""

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue

        if len(para) > chunk_size:
            if current:
                chunks.append(current.strip())
                current = ""
            for i in range(0, len(para), chunk_size):
                chunks.append(para[i : i + chunk_size])
            continue

        if current and len(current) + len(para) > chunk_size:
            chunks.append(current.strip())
            current = current[-overlap:] + "\n\n" + para
        else:
            current += ("\n\n" if current else "") + para

    if current:
        chunks.append(current.strip())

    return chunks


class IngestRequest(BaseModel):
    text: str
    source: str


class QueryRequest(BaseModel):
    question: str
    n_results: int = 3
    use_query_rewriting: bool = False  # opt-in — LLM query expansion
    use_bm25: bool = False             # opt-in — sparse lexical retrieval


class QueryResponse(BaseModel):
    answer: str
    sources: list[str]
    context_sufficient: bool
    insufficiency_reason: str | None = None  # debug/demo only — not a routing signal
    
class GroundedAnswer(BaseModel):
    answer: str = Field(
        description="The answer to the user's question, using only the provided context."
    )
    context_sufficient: bool = Field(
        description=(
            "True if the provided context contained enough information to answer "
            "the question. False if it did not — including when the context is "
            "empty, or covers a related topic without addressing what was asked."
        )
    )
    # Debug/demo only — no consumer branches on this value.
    insufficiency_reason: str | None = Field(
        default=None,
        description=(
            "When context_sufficient is False, one short sentence naming what the "
            "context covered instead of what was asked. Null otherwise."
        ),
    )
    
@app.post("/ingest")
def ingest(request: IngestRequest):
    _require_ready()

    chunks = chunk_text(request.text)
    embeddings = [embed(chunk) for chunk in chunks]

    collection.add(
        ids=[f"{request.source}_{i}" for i in range(len(chunks))],
        embeddings=embeddings,
        documents=chunks,
        metadatas=[{"source": request.source} for _ in chunks],
    )
    _rebuild_bm25_index()
    return {"chunks_ingested": len(chunks)}


async def rewrite_query(question: str) -> str:
    system_prompt = (
        "You are helping improve semantic search retrieval for a RAG system. "
        "The user's question will be converted into an embedding and compared "
        "against chunks of a document using vector similarity search. "
        "Academic and technical documents often use different terminology than "
        "everyday questions — for example, a paper might discuss 'EDI' or "
        "'diversity and inclusion' rather than 'disabilities,' or describe a "
        "'left-libertarian orientation' rather than simply 'bias.'\n\n"
        "Your job: rewrite the user's question to maximize the chance of "
        "matching how a formal academic or technical source would actually "
        "phrase the relevant content. Consider: domain-specific terminology, "
        "formal/academic phrasing instead of conversational phrasing, and "
        "likely section headings or technical terms an author would use. "
        "Return only the rewritten query, nothing else — no explanation, "
        "no preamble."
    )

    response = await llm.bind(max_tokens=100).ainvoke(
        [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ]
    )
    content = response.content
    return content if isinstance(content, str) else question  # fall back to original


def _retrieve_candidates(query_text: str, n: int = 20) -> tuple[list[str], list[str]]:
    query_embedding = embed(query_text)
    results = collection.query(query_embeddings=[query_embedding], n_results=n)
    return results["documents"][0], [m["source"] for m in results["metadatas"][0]]


def _retrieve_bm25_candidates(query_text: str, n: int = 20) -> tuple[list[str], list[str]]:
    if bm25_index is None:
        return [], []
    scores = bm25_index.get_scores(_tokenize(query_text))
    top_idx = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:n]
    return [bm25_documents[i] for i in top_idx], [bm25_sources[i] for i in top_idx]


def reciprocal_rank_fusion(ranked_lists: list[list[str]], k: int = 60) -> list[str]:
    scores: dict[str, float] = {}
    for ranked_list in ranked_lists:
        for rank, doc in enumerate(ranked_list, start=1):
            scores[doc] = scores.get(doc, 0.0) + 1.0 / (k + rank)
    return sorted(scores, key=lambda d: scores[d], reverse=True)


# Sanity check against a silent fusion bug corrupting eval results downstream
assert reciprocal_rank_fusion([["a", "b"], ["a", "c"]])[0] == "a"
assert reciprocal_rank_fusion([["x", "y"], []]) == ["x", "y"]


async def retrieve(
    question: str,
    n_results: int = 3,
    use_query_rewriting: bool = False,
    use_bm25: bool = False,
) -> tuple[list[str], list[str]]:
    """
    Composable retrieval pipeline.
    
    Baseline: dense vector search only.
    Incremental strategies:
      - use_bm25=True           → adds BM25 sparse retrieval via RRF fusion
      - use_query_rewriting=True → adds LLM-rewritten dense (+ BM25 if enabled)
    """
    doc_to_source: dict[str, str] = {}
    ranked_lists: list[list[str]] = []

    async def _fetch_all(query: str) -> None:
        """Run every enabled retriever for this query variant concurrently."""
        tasks = [asyncio.to_thread(_retrieve_candidates, query)]
        if use_bm25 and bm25_index is not None:
            tasks.append(asyncio.to_thread(_retrieve_bm25_candidates, query))

        for docs, sources in await asyncio.gather(*tasks):
            if docs:                       # skip empty results to keep RRF clean
                ranked_lists.append(docs)
            for doc, src in zip(docs, sources):
                doc_to_source.setdefault(doc, src)

    # 1. Base query retrieval
    await _fetch_all(question)

    # 2. Optional query-rewriting branch
    if use_query_rewriting:
        rewritten = await rewrite_query(question)
        await _fetch_all(rewritten)

    # 3. Fuse — guard against empty corpus
    if not ranked_lists:
        return [], []

    fused = reciprocal_rank_fusion(ranked_lists)[:FUSED_CANDIDATE_POOL]
    if not fused:
        return [], []

    candidate_sources = [doc_to_source[d] for d in fused]

    # 4. Cross-encoder rerank
    scores = list(reranker.rerank(question, fused))
    ranked = sorted(
        zip(fused, candidate_sources, scores),
        key=lambda x: x[2],
        reverse=True,
    )
    top_n = ranked[:n_results]

    return [c for c, _, _ in top_n], [s for _, s, _ in top_n]


@app.post("/query")
async def query(request: QueryRequest) -> QueryResponse:
    _require_ready()

    retrieved_chunks, sources = await retrieve(
        question=request.question,
        n_results=request.n_results,
        use_query_rewriting=request.use_query_rewriting,
        use_bm25=request.use_bm25,
    )

    context = "\n\n---\n\n".join(retrieved_chunks)

    system_prompt = (
        "Answer the user's question using only the provided context. "
        "If the context doesn't contain enough information to answer, say so "
        "clearly in your answer and set context_sufficient to false. Judge "
        "sufficiency against what was actually asked — context on a related "
        "topic that doesn't address the specific question is not sufficient."
    )
    prompt = f"Context:\n{context}\n\nQuestion: {request.question}"

    result = await llm.with_structured_output(GroundedAnswer).ainvoke(
        [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ]
    )

    return QueryResponse(
        answer=result.answer,
        sources=list(dict.fromkeys(sources)),
        context_sufficient=result.context_sufficient,
        insufficiency_reason=result.insufficiency_reason,
    )