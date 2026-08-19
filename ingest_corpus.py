#!/usr/bin/env python3
"""Batch ingestion script for the biomedical RAG corpus.

Usage:
    1. Run `python reset_collection.py` to reset the collection when
       ingesting the corpus from scratch.
    2. Start the FastAPI server:
       `uvicorn main:app --reload`
    3. Run this script to ingest the corpus.
"""
import argparse
import json
import sys
from pathlib import Path

import httpx
from pypdf import PdfReader

INGEST_URL = "http://localhost:8000/ingest"
HEALTH_URL = "http://localhost:8000/health"
DEFAULT_MANIFEST = Path("./corpus_manifest.json")
DEFAULT_CORPUS_DIR = Path("./corpus")

def check_existing_chunks(client: httpx.Client) -> int:
    """Query /health for current chunk count. Exits if the server isn't
    reachable or isn't ready yet — ingesting against a not-ready server
    would just fail on every request anyway."""
    try:
        response = client.get(HEALTH_URL, timeout=10.0)
    except httpx.ConnectError:
        print("ERROR: could not reach the server — is `uvicorn main:app` running?")
        sys.exit(1)

    if response.status_code == 503:
        body = response.json()
        print(f"Server not ready yet: {body}. Wait for /health to report 'ready', then retry.")
        sys.exit(1)

    return response.json().get("chunks", 0)

def ingest_file(client: httpx.Client, pdf_path: Path, source: str) -> int | None:
    """Extract text from a PDF and POST it to the local /ingest endpoint."""
    try:
        reader = PdfReader(str(pdf_path))
    except Exception as exc:
        print(f"  ERROR reading {pdf_path.name}: {exc}")
        return None

    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    pdf_path.with_suffix(".txt").write_text(text, encoding="utf-8") # saves the parsed pdf txt for reference
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
        "missing": 0,
        "total_chunks": 0,
    }

    print(f"\nIngesting from: {args.corpus_dir.resolve()}\n")
    with httpx.Client() as client:
        existing = check_existing_chunks(client)
        if existing > 0:
            answer = input(
                f"Collection already has {existing} chunks. Ingesting now will "
                f"add to it, not replace it — if any of these articles are "
                f"already in there, you'll get duplicates. Continue? [y/N] "
            )
            if answer.strip().lower() not in ("y", "yes"):
                print(
                    "Aborted — run reset_collection.py first if you want a clean ingest.\n"
                    "For a full clean-slate rebuild, see the fresh-start recipe in the README."
                )
                return 1

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
    print(f"  Missing/empty:   {stats['missing']}")
    print(f"  Total chunks:    {stats['total_chunks']}")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())