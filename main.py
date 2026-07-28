import os
import re
from dotenv import load_dotenv
from anthropic import AsyncAnthropic
from anthropic.types import TextBlock
from fastembed import TextEmbedding
import chromadb
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

load_dotenv()

app = FastAPI()
embed_model = TextEmbedding()
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


@app.post("/query")
async def query(request: QueryRequest) -> QueryResponse:
    query_embedding = embed(request.question)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=request.n_results,
    )

    retrieved_chunks = results["documents"][0]

    sources = [m["source"] for m in results["metadatas"][0]]

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
