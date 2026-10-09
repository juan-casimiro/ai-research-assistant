#!/usr/bin/env python3
"""Ingest a manifest's PDFs into a new, isolated collection, in-process.

Run from the repository root with the service's Python environment:

    SEED_ON_EMPTY=false python -m tools.corpus.ingest_corpus

The corpus folder defaults to corpus/<corpus_name>/ from the manifest, and the
collection is created beside the PDFs at <corpus folder>/chroma.

No server is started and no port is used: the production models, chunker and
/ingest handler from main.py run in this process. No LLM provider settings are
needed. Safeguards:

    1. SEED_ON_EMPTY=false must be set in the environment, not only in .env.
    2. The collection folder must not exist yet and is created atomically
       before any model loads, so an existing collection is never appended
       to. Delete it before ingesting there again;
       `python -m tools.corpus.reset_collection` only empties a collection.
       An exported CHROMA_PATH replaces the default folder; .env does not.
    3. Manifest filenames must be unique plain .pdf basenames, and every PDF
       must be present, before any model is loaded.
    4. The stored chunks are compared with the corpus before reporting success.
"""
import argparse
import json
import os
from pathlib import Path

from pypdf import PdfReader
from tools.corpus.download_corpus import collection_path, named_corpus_dir, unique_pdf_basenames
from tools.corpus.pdf_text import extract_pages

ROOT = Path(__file__).resolve().parents[2]


def load_production(chroma_path: Path):
    """Load the production retrieval models and collection: no LLM client, no seeding."""
    import main
    main.CHROMA_PATH = str(chroma_path)
    main._load_retrieval()
    main._ready = True
    return main


def ingest_file(production, pdf_path: Path, source: str) -> str:
    """Extract text from a PDF and pass it to the production /ingest handler."""
    text = "\n".join(extract_pages(PdfReader(str(pdf_path))))
    pdf_path.with_suffix(".txt").write_text(text, encoding="utf-8") # saves the parsed pdf txt for reference
    if not text.strip():
        raise ValueError(f"{pdf_path.name} extracted empty text")
    result = production.ingest(production.IngestRequest(text=text, source=source))
    print(f"INGESTED: {source} | chunks={result['chunks_ingested']}")
    return text


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Ingest a corpus manifest into a new isolated collection.")
    parser.add_argument("--manifest", type=Path, default=ROOT / "data/corpus_manifest.json")
    parser.add_argument("--corpus-dir", type=Path, help="Defaults to corpus/<corpus_name>/ from the manifest")
    args = parser.parse_args(argv)

    if os.environ.get("SEED_ON_EMPTY", "").lower() != "false":
        print("ERROR: set SEED_ON_EMPTY=false in the environment.")
        return 1
    exported = os.environ.get("CHROMA_PATH")  # read before main.py loads .env
    try:
        manifest = json.loads(args.manifest.read_text())
        filenames = unique_pdf_basenames([article["filename"] for article in manifest["articles"]])
        if args.corpus_dir is None:
            args.corpus_dir = named_corpus_dir(manifest)
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"ERROR: manifest {args.manifest}: {error}")
        return 1
    missing = [name for name in filenames if not (args.corpus_dir / name).is_file()]
    if not filenames or missing:
        print(f"ERROR: no articles, or {len(missing)} PDFs missing from {args.corpus_dir}: {missing[:5]}")
        return 1
    chroma_path = collection_path(args.corpus_dir, exported)
    try:
        chroma_path.mkdir(parents=True, exist_ok=False)  # atomic: claims the folder or fails
    except FileExistsError:
        print(f"ERROR: a collection already exists at {chroma_path}; it is never reused or appended to.")
        return 1

    from tools.evaluation.evaluate import verify_collection
    try:
        production = load_production(chroma_path)
        texts = {name: ingest_file(production, args.corpus_dir / name, name) for name in filenames}
        chunks = verify_collection(production.collection, texts, production.chunk_text)
    except Exception as error:
        print(f"FAILED: {error}\nThe collection at {chroma_path} is incomplete; do not use it.")
        return 1
    print(f"Ingested {len(texts)} articles; {chunks} stored chunks match the corpus.")
    print(f"CHROMA_PATH={chroma_path.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
