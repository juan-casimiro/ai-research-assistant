#!/usr/bin/env python3
"""Batch ingestion script for the biomedical RAG corpus.

Usage:
    The FastAPI server must be up: uvicorn main:app --reload
"""
import argparse
import json
import sys
from pathlib import Path

import chromadb
import httpx
from pypdf import PdfReader

CHROMA_PATH = "./chroma_db"
COLLECTION_NAME = "documents"
INGEST_URL = "http://localhost:8000/ingest"
DEFAULT_MANIFEST = Path("./corpus_manifest.json")
DEFAULT_CORPUS_DIR = Path("./corpus")


def ingest_file(client: httpx.Client, pdf_path: Path, source: str) -> int | None:
    """Extract text from a PDF and POST it to the local /ingest endpoint."""
    try:
        reader = PdfReader(str(pdf_path))
    except Exception as exc:
        print(f"  ERROR reading {pdf_path.name}: {exc}")
        return None

    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    if not text.strip():
        print(f"  WARNING: {pdf_path.name} extracted empty text — skipping.")
        return 0

    response = client.post(
        INGEST_URL,
        json={"text": text, "source": source},
        timeout=60.0,
    )
    response.raise_for_status()
    return response.json().get("chunks_ingested", 0)


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingest biomedical corpus into the RAG system.")
    parser.add_argument(
        "--corpus-dir",
        type=Path,
        default=DEFAULT_CORPUS_DIR,
        help="Directory containing PDF files (default: ./corpus)",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=DEFAULT_MANIFEST,
        help="Path to corpus_manifest.json (default: ./corpus_manifest.json)",
    )
    args = parser.parse_args()

    if not args.manifest.exists():
        print(f"Manifest not found: {args.manifest}")
        return 1

    manifest = json.loads(args.manifest.read_text())
    articles = manifest.get("articles", [])

    stats = {
        "ingested": 0,
        "skipped_outlier": 0,
        "missing": 0,
        "total_chunks": 0,
    }

    print(f"\nIngesting from: {args.corpus_dir.resolve()}\n")

    with httpx.Client() as client:
        for article in articles:
            filename = article["filename"]
            cluster = article.get("cluster", "unknown")

            pdf_path = args.corpus_dir / filename
            if not pdf_path.exists():
                print(f"SKIP (file not found): {filename}")
                stats["missing"] += 1
                continue

            chunks = ingest_file(client, pdf_path, source=filename)
            if chunks is None:
                stats["missing"] += 1
                continue

            print(f"INGESTED: {filename} | cluster={cluster} | chunks={chunks}")
            stats["ingested"] += 1
            stats["total_chunks"] += chunks

    # 6. Final summary table
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  Ingested:        {stats['ingested']}")
    print(f"  Skipped outlier: {stats['skipped_outlier']}")
    print(f"  Missing/empty:   {stats['missing']}")
    print(f"  Total chunks:    {stats['total_chunks']}")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())