"""Reproduce isolated condition ingestion using production models and /ingest handler.

Run from repository root with PYTHONPATH=. and an unused CHROMA_PATH.
No server, seed, rewrite or generation is started.
"""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess

if os.environ.get('SEED_ON_EMPTY') != 'false':
    raise ValueError('SEED_ON_EMPTY=false is required')
collection_path = Path(os.environ['CHROMA_PATH'])
if collection_path.exists():
    raise ValueError('CHROMA_PATH must be a fresh, unused directory')

import main
from eval_benchmark import model_fingerprint, read_release, verify_collection, write_checkpoint

parser = argparse.ArgumentParser()
parser.add_argument('--condition', choices=['C1', 'C2'], required=True)
parser.add_argument('--receipt', type=Path, required=True)
args = parser.parse_args()
release = Path('benchmark/cardiology/v1')
benchmark, manifest, conditions, condition, tuples, texts = read_release(
    release, Path('corpus/cardiology-v1'), args.condition)
# Reserve receipt before model loading; never overwrite an earlier ingestion.
with args.receipt.open('x') as stream:
    json.dump({'status': 'setup', 'condition': args.condition}, stream)
main._load_models_and_index()
if main.collection.count() != 0:
    raise ValueError('isolated collection must be empty before ingestion')
models = {'embedding': model_fingerprint(main.embed_model),
          'reranker': model_fingerprint(main.reranker)}
main._ready = True
for source, text in texts.items():
    result = main.ingest(main.IngestRequest(text=text, source=source))
    print(source, result, flush=True)
receipt = verify_collection(main.collection, texts, main.chunk_text)
if len(main.bm25_documents) != receipt['chunk_count']:
    raise ValueError('BM25 index count differs from verified collection')
receipt.update(status='complete', condition=args.condition,
    collection_path=str(collection_path.resolve()), seed_on_empty=False,
    timestamp=datetime.now(timezone.utc).isoformat(), loaded_models=models,
    membership_sha256=condition['membership_sha256'], article_tuples=tuples,
    code_commit=subprocess.check_output(['git','rev-parse','HEAD'], text=True).strip(),
    ingestion='production main.ingest / main.embed / main.chunk_text; no HTTP server')
write_checkpoint(args.receipt, receipt)
print('Verified', receipt['chunk_count'], 'chunks', flush=True)
