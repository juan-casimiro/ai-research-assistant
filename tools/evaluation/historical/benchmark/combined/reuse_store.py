"""Create a fresh condition store from verified historical production embeddings.

Only missing articles are embedded through main.ingest. The parent is read-only;
the exact source/chunk multiset, original model receipt and copied embedding
bytes are verified. No seed articles, paid API calls, or HTTP service are used.
"""
import argparse
from datetime import datetime, timezone
import hashlib
from importlib.metadata import version
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from benchmark_scoring import canonical_hash
from eval_benchmark import model_fingerprint, read_release, verify_collection


def embedding_hash(stored):
    if len({len(stored[k]) for k in ["ids", "metadatas", "documents", "embeddings"]}) != 1:
        raise ValueError("embedding/source/document lengths differ")
    if len(set(stored["ids"])) != len(stored["ids"]):
        raise ValueError("duplicate stored IDs")
    return canonical_hash(sorted((i, s["source"], d, list(map(float, e)))
        for i, s, d, e in zip(stored["ids"], stored["metadatas"], stored["documents"], stored["embeddings"])))


def create(args):
    target = Path(os.environ["CHROMA_PATH"])
    if os.environ.get("SEED_ON_EMPTY") != "false" or target.exists() or args.receipt.exists():
        raise ValueError("seeding must be disabled and target/receipt must be fresh")
    import chromadb
    import main
    _, _, _, condition, tuples, texts = read_release(args.benchmark, args.corpus_dir, args.condition)
    parent_receipt = json.loads(args.parent_receipt.read_text())
    if parent_receipt["status"] != "complete" or parent_receipt["seed_on_empty"] is not False:
        raise ValueError("parent ingestion is incomplete or seed-enabled")
    parent_run = json.loads((ROOT / "benchmark/combined/v1/runs/cardiology-C3-vector.json").read_text())
    dependencies = {name: version(name) for name in parent_run["provenance"]["dependencies"]}
    if dependencies != parent_run["provenance"]["dependencies"]:
        raise ValueError("dependencies differ from historical ingestion/evaluation environment")
    for name in ["main.py", "llm_client.py"]:
        original = subprocess.check_output(["git", "show", parent_receipt["code_commit"] + ":" + name], cwd=ROOT)
        if original != (ROOT / name).read_bytes():
            raise ValueError(f"production {name} differs from parent ingestion")
    # Verify all parent input tuples and chunks against its immutable envelope.
    _, _, _, parent_condition, parent_tuples, parent_texts = read_release(
        ROOT / "benchmark/combined/v1/cardiology", args.parent_corpus, "C3")
    if parent_receipt["membership_sha256"] != parent_condition["membership_sha256"] or parent_receipt["article_tuples"] != parent_tuples:
        raise ValueError("parent membership receipt mismatch")
    parent = chromadb.PersistentClient(path=str(args.parent_store)).get_collection("documents")
    checked = verify_collection(parent, parent_texts, main.chunk_text)
    for key in ["chunks_sha256", "chunk_count", "per_source_chunks", "collection_name"]:
        if checked[key] != parent_receipt[key]:
            raise ValueError(f"parent receipt differs from stored {key}")
    shared = {t["article_id"]: t for t in parent_tuples}
    if any(t != shared[t["article_id"]] for t in tuples if t["article_id"] in shared):
        raise ValueError("reused article version changed")
    stored = parent.get(include=["documents", "metadatas", "embeddings"])
    main._load_models_and_index()
    models = {"embedding": model_fingerprint(main.embed_model), "reranker": model_fingerprint(main.reranker)}
    if models != parent_receipt["loaded_models"]:
        raise ValueError("loaded model files differ from original ingestion")
    take = [i for i, m in enumerate(stored["metadatas"]) if m["source"] in texts]
    copied = {key: [stored[key][i] for i in take] for key in ["ids", "metadatas", "documents", "embeddings"]}
    for start in range(0, len(take), 256):
        main.collection.add(**{key: values[start:start + 256] for key, values in copied.items()})
    actual_copy = main.collection.get(include=["documents", "metadatas", "embeddings"])
    if embedding_hash(actual_copy) != embedding_hash(copied):
        raise ValueError("copied embeddings differ")
    main._ready = True
    for source in sorted(set(texts) - set(parent_texts)):
        main.ingest(main.IngestRequest(text=texts[source], source=source))
    receipt = verify_collection(main.collection, texts, main.chunk_text)
    # Query Chroma directly using a production embedding of each source's first
    # chunk. This proves every article has a queryable vector; it is not a QA score.
    probes = {}
    for source, text in texts.items():
        result = main.collection.query(query_embeddings=[main.embed(main.chunk_text(text)[0])],
                                       where={"source": source}, n_results=1)
        if not result["ids"][0] or result["metadatas"][0][0]["source"] != source:
            raise ValueError(f"source is not queryable: {source}")
        probes[source] = result["ids"][0][0]
    receipt.update(status="complete", condition=args.condition, seed_on_empty=False,
        timestamp=datetime.now(timezone.utc).isoformat(), loaded_models=models, dependencies=dependencies,
        membership_sha256=condition["membership_sha256"], article_tuples=tuples,
        collection_path=str(target.resolve()), code_commit=subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        ingestion="verified copies of historical production embeddings; new sources via production main.ingest/embed/chunk_text",
        source_query_probes=probes, parent_receipt=str(args.parent_receipt),
        parent_receipt_sha256=hashlib.sha256(args.parent_receipt.read_bytes()).hexdigest(),
        parent_chunks_sha256=checked["chunks_sha256"], reused_chunks=len(take),
        new_chunks=receipt["chunk_count"] - len(take), reused_embeddings_sha256=embedding_hash(copied),
        embeddings_sha256=embedding_hash(main.collection.get(include=["documents", "metadatas", "embeddings"])),
        limitations=["Original embedding provenance is inherited from the pinned production-ingestion receipt; historical vectors were not recomputed.",
                     "Per-source filtered vector probes prove index queryability, not unfiltered QA retrieval success."])
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    with args.receipt.open("x") as stream:
        json.dump(receipt, stream, indent=2)
        stream.write("\n")
    print(f"Verified {receipt['chunk_count']} chunks / {len(texts)} queryable articles; reused {len(take)} embeddings")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ["benchmark", "corpus-dir", "parent-store", "parent-receipt", "parent-corpus", "receipt"]:
        parser.add_argument("--" + name, type=Path, required=True)
    parser.add_argument("--condition", choices=["C1", "C2", "C3"], required=True)
    create(parser.parse_args())
