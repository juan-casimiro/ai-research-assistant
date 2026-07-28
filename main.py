import asyncio
import re
from dotenv import load_dotenv
from anthropic import AsyncAnthropic
from anthropic.types import TextBlock
from fastembed import TextEmbedding
from fastembed.rerank.cross_encoder import TextCrossEncoder
import chromadb
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

load_dotenv()

app = FastAPI()
embed_model = TextEmbedding()
reranker = TextCrossEncoder(model_name="Xenova/ms-marco-MiniLM-L-6-v2")
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection("documents")
anthropic_client = AsyncAnthropic()


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
    use_query_rewriting: bool = False  # opt-in, not default — see ADR-001


class QueryResponse(BaseModel):
    answer: str
    sources: list[str]


@app.post("/ingest")
def ingest(request: IngestRequest):
    chunks = chunk_text(request.text)
    embeddings = [embed(chunk) for chunk in chunks]

    collection.add(
        ids=[f"{request.source}_{i}" for i in range(len(chunks))],
        embeddings=embeddings,
        documents=chunks,
        metadatas=[{"source": request.source} for _ in chunks],
    )

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

    response = await anthropic_client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=100,
        system=system_prompt,
        messages=[{"role": "user", "content": question}],
    )
    match response.content[0]:
        case TextBlock(text=rewritten):
            return rewritten
        case _:
            return question  # fall back to original on unexpected response


def _retrieve_candidates(query_text: str, n: int = 20) -> tuple[list[str], list[str]]:
    query_embedding = embed(query_text)
    results = collection.query(query_embeddings=[query_embedding], n_results=n)
    return results["documents"][0], [m["source"] for m in results["metadatas"][0]]


async def retrieve(
    question: str, n_results: int = 3, use_query_rewriting: bool = False
) -> tuple[list[str], list[str]]:

    seen = {}
    if use_query_rewriting:
        rewritten = await rewrite_query(question)
        # retrieve for both phrasings concurrently — cheap, since it's just embedding + Chroma
        (orig_docs, orig_sources), (rewritten_docs, rewritten_sources) = (
            await asyncio.gather(
                asyncio.to_thread(_retrieve_candidates, question),
                asyncio.to_thread(_retrieve_candidates, rewritten),
            )
        )
        # merge, deduping by chunk text
        for doc, src in zip(
            orig_docs + rewritten_docs, orig_sources + rewritten_sources
        ):
            seen[doc] = (
                src  # last write wins; fine since content is identical for dupes
            )
    else:
        orig_docs, orig_sources = _retrieve_candidates(question)
        for doc, src in zip(orig_docs, orig_sources):
            seen[doc] = src

    candidates = list(seen.keys())
    candidate_sources = list(seen.values())

    # rerank the MERGED pool against the ORIGINAL question — that's the true user intent
    scores = list(reranker.rerank(question, candidates))
    ranked = sorted(
        zip(candidates, candidate_sources, scores), key=lambda x: x[2], reverse=True
    )
    top_n = ranked[:n_results]

    return [c for c, _, _ in top_n], [s for _, s, _ in top_n]


@app.post("/query")
async def query(request: QueryRequest) -> QueryResponse:
    retrieved_chunks, sources = await retrieve(
        request.question, request.n_results, request.use_query_rewriting
    )

    context = "\n\n---\n\n".join(retrieved_chunks)

    system_prompt = (
        "Answer the user's question using only the provided context. "
        "If the context doesn't contain enough information to answer, say so clearly."
    )
    prompt = f"Context:\n{context}\n\nQuestion: {request.question}"

    response = await anthropic_client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        system=system_prompt,
        messages=[{"role": "user", "content": prompt}],
    )

    match response.content[0]:
        case TextBlock(text=answer):
            pass
        case _:
            raise HTTPException(500, "Unexpected response type from Claude")

    return QueryResponse(answer=answer, sources=list(set(sources)))
