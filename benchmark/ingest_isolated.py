"""Ingest one benchmark condition into a fresh verified production store.

Run from the repository root with SEED_ON_EMPTY=false and an unused CHROMA_PATH.
No server, seed, rewriting, generation or provider call is started.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def ingest(benchmark, corpus_dir, condition_name, receipt_path):
    if os.environ.get("SEED_ON_EMPTY") != "false":
        raise ValueError("SEED_ON_EMPTY=false is required")
    if not os.environ.get("CHROMA_PATH"):
        raise ValueError("CHROMA_PATH must point to a fresh isolated directory")
    collection_path = Path(os.environ["CHROMA_PATH"])
    if collection_path.exists() or collection_path.is_symlink():
        raise ValueError("CHROMA_PATH must be fresh and unused")
    receipt_path = Path(receipt_path)
    if receipt_path.exists() or receipt_path.is_symlink():
        raise ValueError("receipt path must be fresh and unused")

    sys.path.insert(0, str(ROOT))
    from eval_benchmark import model_fingerprint, read_release, verify_collection, write_checkpoint

    benchmark, corpus_dir = Path(benchmark), Path(corpus_dir)
    _, manifest, _, condition, tuples, texts = read_release(benchmark, corpus_dir, condition_name)
    member_ids = set(condition["article_ids"])
    member_filenames = {article["filename"] for article in manifest["articles"]
                        if article["article_id"] in member_ids}
    texts = {name: text for name, text in texts.items() if name in member_filenames}
    if set(texts) != member_filenames:
        raise ValueError("condition source texts are incomplete")
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    # Reserve before importing/loading production models; never replace a receipt.
    with receipt_path.open("x", encoding="utf-8") as stream:
        json.dump({"status": "setup", "condition": condition_name}, stream)

    import main

    main._load_models_and_index()
    if main.collection.count() != 0:
        raise ValueError("the isolated collection must be empty before ingestion")
    models = {"embedding": model_fingerprint(main.embed_model),
              "reranker": model_fingerprint(main.reranker)}
    main._ready = True
    for source, text in texts.items():
        main.ingest(main.IngestRequest(text=text, source=source))
        print(f"Ingested {source}", flush=True)
    receipt = verify_collection(main.collection, texts, main.chunk_text)
    if len(main.bm25_documents) != receipt["chunk_count"]:
        raise ValueError("BM25 index count differs from the verified collection")
    receipt.update(status="complete", condition=condition_name,
                   benchmark=str(benchmark), corpus_dir=str(corpus_dir),
                   collection_path=str(collection_path.resolve()), seed_on_empty=False,
                   timestamp=datetime.now(timezone.utc).isoformat(), loaded_models=models,
                   membership_sha256=condition["membership_sha256"], article_tuples=tuples,
                   code_commit=subprocess.check_output(["git", "rev-parse", "HEAD"],
                                                       cwd=ROOT, text=True).strip(),
                   helper_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                   ingestion="production main.ingest / main.embed / main.chunk_text; no HTTP server")
    write_checkpoint(receipt_path, receipt)
    print(f"Verified {receipt['chunk_count']} chunks across {len(texts)} articles", flush=True)


def cli():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--benchmark", type=Path, required=True)
    parser.add_argument("--corpus-dir", type=Path, required=True)
    parser.add_argument("--condition", choices=["C1", "C2", "C3"], required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    ingest(args.benchmark, args.corpus_dir, args.condition, args.receipt)


if __name__ == "__main__":
    cli()
