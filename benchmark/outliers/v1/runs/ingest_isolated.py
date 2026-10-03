"""Build a verified fresh Chroma store using the production ingest path.

Run from the repository root with SEED_ON_EMPTY=false, PYTHONPATH=., an unused
CHROMA_PATH and an unused receipt path. This helper never resets a collection.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))

if os.environ.get("SEED_ON_EMPTY") != "false":
    raise ValueError("SEED_ON_EMPTY=false is required")
if not os.environ.get("CHROMA_PATH"):
    raise ValueError("CHROMA_PATH must point to a fresh isolated directory")
collection_path = Path(os.environ["CHROMA_PATH"])
if collection_path.exists():
    raise ValueError("CHROMA_PATH must be fresh and unused")

import main
from eval_benchmark import model_fingerprint, read_release, verify_collection, write_checkpoint

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--benchmark", type=Path, default=Path("benchmark/outliers/v1"))
parser.add_argument("--corpus-dir", type=Path, default=Path("corpus/outliers-v1"))
parser.add_argument("--condition", choices=["C1", "C2", "C3"], required=True)
parser.add_argument("--receipt", type=Path, required=True)
args = parser.parse_args()

_, _, conditions, condition, tuples, texts = read_release(args.benchmark, args.corpus_dir, args.condition)
# The nested comparison envelope pins competition files even when C1 ingests
# only core membership. read_release verifies all hashes; store only members.
member_ids = set(condition["article_ids"])
manifest = json.loads((args.benchmark / "manifest.json").read_text(encoding="utf-8"))
member_filenames = {article["filename"] for article in manifest["articles"]
                    if article["article_id"] in member_ids}
texts = {name: text for name, text in texts.items() if name in member_filenames}
args.receipt.parent.mkdir(parents=True, exist_ok=True)
with args.receipt.open("x", encoding="utf-8") as stream:
    json.dump({"status": "setup", "condition": args.condition}, stream)
    stream.flush()

main._load_models_and_index()
if main.collection.count() != 0:
    raise ValueError("the isolated collection must be empty before ingestion")
models = {"embedding": model_fingerprint(main.embed_model), "reranker": model_fingerprint(main.reranker)}
main._ready = True
for source, text in texts.items():
    main.ingest(main.IngestRequest(text=text, source=source))
    print(f"Ingested {source}", flush=True)

receipt = verify_collection(main.collection, texts, main.chunk_text)
if len(main.bm25_documents) != receipt["chunk_count"]:
    raise ValueError("BM25 document count differs from the verified collection")
receipt.update(status="complete", condition=args.condition,
    benchmark=str(args.benchmark), corpus_dir=str(args.corpus_dir),
    collection_path=str(collection_path.resolve()), seed_on_empty=False,
    timestamp=datetime.now(timezone.utc).isoformat(), loaded_models=models,
    membership_sha256=condition["membership_sha256"], article_tuples=tuples,
    code_commit=subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
    ingestion="production main.ingest / main.embed / main.chunk_text; no HTTP server")
write_checkpoint(args.receipt, receipt)
print(f"Verified {receipt['chunk_count']} chunks across {len(texts)} articles", flush=True)
