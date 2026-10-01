"""Pinned benchmark adapter for eval_golden; uses production retrieve()."""
from collections import Counter
from datetime import datetime, timezone
import hashlib
from importlib.metadata import version
import json
import os
from pathlib import Path
import subprocess
from tempfile import NamedTemporaryFile
from uuid import uuid4

from chromadb.errors import ChromaError
from benchmark_scoring import SCORER_VERSION, canonical_hash, score_evidence, validate_benchmark

ROOT = Path(__file__).resolve().parent


def write_checkpoint(path: Path, output: dict) -> None:
    """Replace this run's reserved file atomically, preserving the last good snapshot."""
    temporary = None
    try:
        with NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent,
                                prefix=f".{path.name}.", suffix=".tmp", delete=False) as stream:
            temporary = Path(stream.name)
            json.dump(output, stream, indent=2, ensure_ascii=False, allow_nan=False)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def model_fingerprint(wrapper) -> dict:
    """Hash the files actually loaded by the installed FastEmbed backend."""
    backend = wrapper.model
    directory = Path(backend._model_dir)
    files = {str(p.relative_to(directory)): hashlib.sha256(p.read_bytes()).hexdigest()
             for p in sorted(directory.rglob("*")) if p.is_file() and ".cache" not in p.parts}
    if not files or not any(name.endswith(".onnx") for name in files):
        raise ValueError("cannot verify loaded model weights")
    return {"model_name": wrapper.model_name, "files": files, "sha256": canonical_hash(files)}


def read_release(directory: Path, corpus_dir: Path, condition_name: str):
    benchmark = json.loads((directory / "queries.json").read_text())
    validate_benchmark(benchmark)
    manifest = json.loads((directory / "manifest.json").read_text())
    if canonical_hash({k: v for k, v in manifest.items() if k != "fingerprint_sha256"}) != manifest["fingerprint_sha256"]:
        raise ValueError("selected manifest fingerprint changed")
    conditions = json.loads((directory / "conditions.json").read_text())
    condition = conditions["conditions"][condition_name]
    if (benchmark["selection_sha256"] != manifest["fingerprint_sha256"] or
            conditions.get("query_sha256") != canonical_hash(benchmark)):
        raise ValueError("query/selection/condition linkage changed; re-review membership")
    articles = {a["article_id"]: a for a in manifest["articles"]}
    members = condition["article_ids"]
    tuples = [t for t in conditions["article_tuples"] if t["article_id"] in members]
    if len(set(members)) != len(members) or {t["article_id"] for t in tuples} != set(members) or len(tuples) != len(members):
        raise ValueError("duplicate or missing condition article tuples")
    for t in tuples:
        a = articles[t["article_id"]]
        if t != {"article_id": a["article_id"], "pmc_version": a["pmc_version"],
                 "pdf_sha256": a["download"]["pdf_sha256"],
                 "text_sha256": a["validation"]["extracted_text_sha256"]}:
            raise ValueError("condition tuple differs from pinned manifest")
    if canonical_hash(tuples) != condition["membership_sha256"]:
        raise ValueError("condition membership fingerprint changed")
    text_by_source = {}
    # Verify every anchor source, including C2 competition when executing C1.
    for article in manifest["articles"]:
        pdf = corpus_dir / article["filename"]
        text_bytes = pdf.with_suffix(".txt").read_bytes()
        if hashlib.sha256(pdf.read_bytes()).hexdigest() != article["download"]["pdf_sha256"] or hashlib.sha256(text_bytes).hexdigest() != article["validation"]["extracted_text_sha256"]:
            raise ValueError(f"{article['article_id']}: pinned PDF/text changed")
        text_by_source[article["filename"]] = text_bytes.decode("utf-8")
    for anchor in benchmark["anchors"]:
        article = articles[anchor["article_id"]]
        if (anchor["filename"], anchor["pmc_version"], anchor["pdf_sha256"], anchor["text_sha256"]) != (article["filename"], article["pmc_version"], article["download"]["pdf_sha256"], article["validation"]["extracted_text_sha256"]):
            raise ValueError(f"{anchor['id']}: anchor source version changed")
        excerpt = text_by_source[anchor["filename"]][anchor["text_start"]:anchor["text_end"]]
        if excerpt != anchor["excerpt"] or hashlib.sha256(excerpt.encode()).hexdigest() != anchor["excerpt_sha256"]:
            raise ValueError(f"{anchor['id']}: anchor offset/hash changed")
    selected_text = {articles[aid]["filename"]: text_by_source[articles[aid]["filename"]] for aid in members}
    return benchmark, manifest, conditions, condition, tuples, selected_text


def verify_collection(collection, selected_text: dict, chunker) -> dict:
    """Check actual stored chunks, rather than trusting a receipt or path name."""
    expected = Counter((source, chunk) for source, text in selected_text.items() for chunk in chunker(text))
    stored = collection.get(include=["documents", "metadatas"])
    docs, metadata = stored["documents"], stored["metadatas"]
    if len(docs) != len(metadata):
        raise ValueError("stored chunk/source counts differ")
    actual = Counter((m["source"], d) for d, m in zip(docs, metadata))
    if not expected or actual != expected:
        raise ValueError("collection differs from pinned condition chunks (missing, stale, duplicate or extra sources); ingest an isolated collection first")
    return {"collection_name": collection.name, "chunk_count": len(docs),
            "per_source_chunks": dict(sorted(Counter(m["source"] for m in metadata).items())),
            "chunks_sha256": canonical_hash(sorted((s, d, count) for (s, d), count in actual.items()))}


def summarize(results: list[dict]) -> dict:
    summary = {}
    for depth in [3, 8]:
        groups = {}
        for status in ["answerable", "false_premise", "absent_fact"]:
            entries = [r for r in results if r["answerability"] == status]
            values = [r[f"n{depth}"]["metrics"] for r in entries]
            groups[status] = {"executed": len(entries), "answer_judged": 0}
            if status != "absent_fact":
                groups[status].update({
                    "document_coverage_pass": sum(v["document_coverage"] == "pass" for v in values),
                    "pinned_evidence_complete": sum(v["evidence_coverage"] == "pass" for v in values),
                    "macro_fact_recall": sum(v["fact_recall"] for v in values) / len(values) if values else None})
        decoys = [r[f"n{depth}"]["metrics"] for r in results if r["category"] == "cross_doc_distractor"]
        groups["distractor_ordering"] = {"total": len(decoys),
            "pass": sum(v["distractor_ordering"] == "pass" for v in decoys),
            "decoy_present": sum(bool(v["present_distractors"]) for v in decoys)}
        groups["categories"] = {}
        for category in sorted({r["category"] for r in results}):
            values = [r[f"n{depth}"]["metrics"] for r in results if r["category"] == category]
            groups["categories"][category] = {"executed": len(values),
                "document_scored": sum(v["document_coverage"] != "not_scored" for v in values),
                "document_pass": sum(v["document_coverage"] == "pass" for v in values),
                "evidence_scored": sum(v["evidence_coverage"] != "not_scored" for v in values),
                "evidence_pass": sum(v["evidence_coverage"] == "pass" for v in values)}
        summary[f"n{depth}"] = groups
    return summary


async def run_benchmark(args, retrieve, load_models) -> int:
    import main as production
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid4().hex[:8]
    output_path = args.output or Path("eval_results/runs") / f"{run_id}.json"
    output = None
    finished = False
    try:
        benchmark, manifest, conditions, condition, tuples, selected_text = read_release(
            args.benchmark, args.corpus_dir, args.condition)
        queries = benchmark["queries"]
        requested = sorted({i.strip() for i in args.ids.split(",") if i.strip()}) if args.ids is not None else sorted(q["id"] for q in queries)
        missing = set(requested) - {q["id"] for q in queries}
        if missing or not requested:
            raise ValueError(f"invalid requested IDs: {sorted(missing)}")
        queries = [q for q in queries if q["id"] in requested]
        anchors = {a["id"]: a for a in benchmark["anchors"]}
        # Reserve the exact destination exclusively before loading models or paid calls.
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("x", encoding="utf-8") as stream:
            json.dump({"run_id": run_id, "run_status": "setup", "results": []}, stream)
            stream.flush()
            os.fsync(stream.fileno())
        load_models()
        receipt = verify_collection(production.collection, selected_text, production.chunk_text)
        receipt["collection_path"] = str(Path(production.CHROMA_PATH).resolve())
        models = {"embedding": model_fingerprint(production.embed_model),
                  "reranker": model_fingerprint(production.reranker)}
        dependencies = {name: version(name) for name in ["fastembed", "chromadb", "pypdf", "rank-bm25", "onnxruntime"]}
        from llm_client import DEFAULT_MODELS_BY_PROVIDER
        provider = os.getenv("LLM_PROVIDER", "anthropic")
        rewrite_identity = {"provider": provider, "model": os.getenv("LLM_MODEL", DEFAULT_MODELS_BY_PROVIDER.get(provider, ""))}
        retrieval_fingerprint = canonical_hash({"source_sha256": hashlib.sha256((ROOT / "main.py").read_bytes()).hexdigest(),
            "llm_source_sha256": hashlib.sha256((ROOT / "llm_client.py").read_bytes()).hexdigest(), "dependencies": dependencies,
            "loaded_models": models, "rewrite_identity": rewrite_identity})
        provenance = {"query_version": benchmark["query_version"], "query_sha256": canonical_hash(benchmark),
            "subset_sha256": canonical_hash(queries), "scorer_version": SCORER_VERSION,
            "scorer_sha256": canonical_hash({"scoring": hashlib.sha256((ROOT / "benchmark_scoring.py").read_bytes()).hexdigest(),
                "adapter": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}),
            "retrieval_sha256": retrieval_fingerprint, "selection_sha256": manifest["fingerprint_sha256"],
            "conditions_sha256": canonical_hash(conditions), "condition": args.condition,
            "membership_sha256": condition["membership_sha256"], "article_tuples": tuples,
            "requested_ids": requested, "executed_ids": [], "missing_ids": [], "depths": [3, 8],
            "dependencies": dependencies, "loaded_models": models,
            "rewrite_identity": rewrite_identity, "ingestion_verification": receipt}
        results = []
        provenance["missing_ids"] = requested.copy()
        commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
        output = {"run_id": run_id, "run_status": "running", "created_at": datetime.now(timezone.utc).isoformat(), "code_commit": commit,
            "config_label": ("vector-bm25" if args.bm25 else "vector-only-baseline") + ("-rewrite" if args.rewrite else ""),
            "config": {"use_bm25": args.bm25, "use_query_rewriting": args.rewrite, "n_values": [3, 8]},
            "provenance": provenance, "results": results, "summary": None,
            "limitations": ["Exact pinned-excerpt coverage is conservative; a missed substring is not proof of absent semantic evidence.",
                "Collection verification checks stored text/source chunks; it does not recompute stored embeddings to certify their original embedding model. Isolated ingestion provenance remains required for quality claims.",
                "No generated answers, refusal judgments or premise-correction judgments.",
                "Remote rewrite model aliases cannot establish immutable provider weight versions."]}
        write_checkpoint(output_path, output)
        for query in queries:
            entry = {"id": query["id"], "revision": query["revision"], "question": query["question"],
                     "query_sha256": canonical_hash(query), "category": query["category"],
                     "answerability": query["answerability"]["status"]}
            results.append(entry)
            for depth in [3, 8]:
                contexts, sources = await retrieve(query["question"], n_results=depth,
                    use_query_rewriting=args.rewrite, use_bm25=args.bm25)
                metrics = score_evidence(contexts, sources, query, anchors)
                verdict = metrics["document_coverage"]
                if query["category"] == "cross_doc_distractor":
                    verdict = metrics["distractor_ordering"]
                elif query["category"] == "false_premise":
                    verdict = "not_scored"  # correction evidence is separate from judging the answer
                entry[f"n{depth}"] = {"retrieved_sources": sources, "retrieved_contexts": contexts,
                                       "verdict": verdict, "metrics": metrics}
                if depth == 8:
                    provenance["executed_ids"].append(query["id"])
                    provenance["executed_ids"].sort()
                provenance["missing_ids"] = sorted(set(requested) - set(provenance["executed_ids"]))
                write_checkpoint(output_path, output)
            print(f"{entry['id']}: " + "; ".join(f"n{n} document={entry[f'n{n}']['metrics']['document_coverage']} evidence={entry[f'n{n}']['metrics']['evidence_coverage']}" for n in [3, 8]))
        output["run_status"] = "complete"
        output["summary"] = summarize(results)
        write_checkpoint(output_path, output)
        finished = True
        print(f"Saved immutable run {output_path}; {len(results)}/{len(requested)} requested IDs executed")
        return 0
    except (OSError, ValueError, KeyError, TypeError, AttributeError, ChromaError,
            subprocess.CalledProcessError) as error:
        print(f"ERROR: {type(error).__name__}: {error}")
        return 1
    finally:
        if output is not None and not finished:
            output["run_status"] = "incomplete"
            output["summary"] = None
            try:
                write_checkpoint(output_path, output)
            except (OSError, ValueError, TypeError) as error:
                print(f"ERROR: cannot save checkpoint: {error}; last successful snapshot remains at {output_path}")
