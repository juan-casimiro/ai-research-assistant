"""Verify the sealed corrected release; optionally inspect its retained stores."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from benchmark_scoring import canonical_hash
from benchmark.combined.build_corrected_release import TOPICS, build, load
from benchmark.combined.reuse_store import embedding_hash
from benchmark.combined.verify_corrected_runs import analyze
from eval_benchmark import read_release, verify_collection
from main import chunk_text


def verify(release, corpus, stores=False):
    hashes = load(release / "artifact_hashes.json")
    for name, expected in hashes["files"].items():
        if hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != expected:
            raise ValueError(f"artifact drift: {name}")
    # Builder refuses any nonidentical envelope or dependency metadata.
    build(release)
    actual = analyze(release, corpus)
    if actual != load(release / "analysis.json"):
        raise ValueError("saved analysis is not reproducible")
    durable = load(ROOT / "docs/evaluation/combined-benchmark-v2.json")
    if (canonical_hash({k: v for k, v in durable.items() if k != "fingerprint_sha256"}) != durable["fingerprint_sha256"] or
            durable["combined_summary"] != actual["combined_summary"]):
        raise ValueError("durable summary fingerprint/results differ")
    for topic in TOPICS:
        run_path = release / "runs" / f"{topic}-C3-vector.json"
        data = load(run_path)
        snapshot = durable["snapshots"][topic]
        if (snapshot["run_sha256"] != hashlib.sha256(run_path.read_bytes()).hexdigest() or
                snapshot["query_sha256"] != data["provenance"]["query_sha256"] or
                snapshot["summary"] != data["summary"]):
            raise ValueError("durable topic snapshot differs")
        queries = {q["id"]: q for q in load(release / topic / "queries.json")["queries"]}
        for entry in data["results"]:
            if entry["id"] in durable["conflict_inventory"]:
                retained = durable["conflict_inventory"][entry["id"]]
                query = queries[entry["id"]]
                for key in ["question", "revision", "category", "required_facts", "evidence_sets"]:
                    if retained[key] != query[key]:
                        raise ValueError("durable conflict contract differs")
                if retained["case_sha256"] != canonical_hash(query) or any(
                        retained[depth] != entry[depth]["metrics"] for depth in ["n3", "n8"]):
                    raise ValueError("durable conflict metrics differ")
    dependencies = load(release / "case_dependencies.json")
    if canonical_hash({k: v for k, v in dependencies.items() if k != "fingerprint_sha256"}) != dependencies["fingerprint_sha256"]:
        raise ValueError("dependency map fingerprint differs")
    unique = {}
    for topic in TOPICS:
        manifest = load(ROOT / "benchmark" / topic / "v1/manifest.json")
        attribution = (ROOT / "benchmark" / topic / "v1/ATTRIBUTION.md").read_text()
        for a in manifest["articles"]:
            if (a["eligibility"] != "eligible" or a["third_party_review"]["status"] != "clear" or
                    a["licence"]["id"] not in ["CC-BY-4.0", "CC0-1.0"] or a["article_id"] not in attribution):
                raise ValueError(f"incomplete eligibility/attribution: {a['article_id']}")
            unique[a["article_id"]] = a
    if len(unique) != 55:
        raise ValueError("attribution/manifest union differs from 55")
    if stores:
        import chromadb
        for path in sorted((release / "runs").glob("*-ingestion.json")):
            receipt = load(path)
            condition = receipt["condition"]
            topic = "cardiology" if path.name == "C3-ingestion.json" else path.name.split("-C")[0]
            _, _, _, _, _, texts = read_release(release / topic, corpus, condition)
            store_path = Path(receipt["collection_path"])
            if not (store_path / "chroma.sqlite3").is_file():
                raise ValueError(f"saved store is missing: {path.name}")
            collection = chromadb.PersistentClient(path=str(store_path)).get_collection("documents")
            checked = verify_collection(collection, texts, chunk_text)
            if checked["chunks_sha256"] != receipt["chunks_sha256"]:
                raise ValueError("stored chunk multiset differs")
            stored = collection.get(include=["documents", "metadatas", "embeddings"])
            if embedding_hash(stored) != receipt["embeddings_sha256"]:
                raise ValueError("stored embedding bytes differ")
            by_id = dict(zip(stored["ids"], stored["metadatas"], strict=True))
            if any(by_id.get(i, {}).get("source") != s for s, i in receipt["source_query_probes"].items()):
                raise ValueError("source query probe differs from stored source identity")
    print(f"Verified {len(hashes['files'])} artifact hashes, 55 attribution joins, 158 IDs, nested compatibility and byte-identical analysis" +
          ("; seven retained stores/embedding digests checked" if stores else ""))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--release", type=Path, default=Path("benchmark/combined/v2"))
    parser.add_argument("--corpus-dir", type=Path, default=Path("corpus/combined-v2"))
    parser.add_argument("--stores", action="store_true")
    args = parser.parse_args()
    verify(args.release, args.corpus_dir, args.stores)
