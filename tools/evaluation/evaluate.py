"""Evaluate the current Q&A dataset using production retrieve()."""
import argparse
import asyncio
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile
from uuid import uuid4

from chromadb.errors import ChromaError
from anthropic import APIError
from httpx import HTTPError
from ollama import ResponseError
from llm_client import LlmTimeoutError
from tools.evaluation.scoring import (canonical_hash, compile_anchor_spans,
                                      score_evidence, validate_benchmark)

ROOT = Path(__file__).resolve().parents[2]


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


def read_inputs(query_path: Path, manifest_path: Path, corpus_dir: Path):
    benchmark = json.loads(query_path.read_text())
    validate_benchmark(benchmark)
    manifest = json.loads(manifest_path.read_text())
    from tools.corpus.download_corpus import named_corpus_dir
    from tools.corpus.fetch_article_metadata import validate_records
    validate_records(manifest["articles"])
    if corpus_dir is None:
        corpus_dir = named_corpus_dir(manifest)
    articles = {a["article_id"]: a for a in manifest["articles"]}
    if len(articles) != len(manifest["articles"]) or set(articles) != set(benchmark["sources"]):
        raise ValueError("query sources and corpus membership differ")
    text_by_source = {}
    for source_id, article in articles.items():
        pin = benchmark["sources"][source_id]
        if (pin["pmcid"], pin["pmc_version"]) != (article["pmcid"], article["pmc_version"]):
            raise ValueError(f"{source_id}: pinned deposit differs")
        pdf = corpus_dir / article["filename"]
        text_bytes = pdf.with_suffix(".txt").read_bytes()
        pdf_hash = hashlib.sha256(pdf.read_bytes()).hexdigest()
        if pdf_hash != pin["pdf_sha256"] or hashlib.sha256(text_bytes).hexdigest() != pin["text_sha256"]:
            raise ValueError(f"{source_id}: pinned PDF/text changed")
        recorded = article.get("metadata_sources", {}).get("pdf", {}).get("sha256")
        if recorded is not None and recorded != pdf_hash:
            raise ValueError(f"{source_id}: manifest PDF hash differs")
        text_by_source[article["filename"]] = text_bytes.decode("utf-8")
    for anchor in benchmark["anchors"]:
        article = articles[anchor["article_id"]]
        pin = benchmark["sources"][article["article_id"]]
        if (anchor["filename"], anchor["pmc_version"], anchor["pdf_sha256"], anchor["text_sha256"]) != (
                article["filename"], pin["pmc_version"], pin["pdf_sha256"], pin["text_sha256"]):
            raise ValueError(f"{anchor['id']}: anchor source version changed")
        excerpt = text_by_source[anchor["filename"]][anchor["text_start"]:anchor["text_end"]]
        if excerpt != anchor["excerpt"] or hashlib.sha256(excerpt.encode()).hexdigest() != anchor["excerpt_sha256"]:
            raise ValueError(f"{anchor['id']}: anchor offset/hash changed")
    return benchmark, manifest, text_by_source


def verify_collection(collection, selected_text: dict, chunker) -> dict:
    """Check actual stored chunks, rather than trusting a receipt or path name."""
    expected = Counter((source, chunk) for source, text in selected_text.items() for chunk in chunker(text))
    stored = collection.get(include=["documents", "metadatas"])
    docs, metadata = stored["documents"], stored["metadatas"]
    if len(docs) != len(metadata):
        raise ValueError("stored chunk/source counts differ")
    actual = Counter((m["source"], d) for d, m in zip(docs, metadata))
    if not expected or actual != expected:
        raise ValueError("collection differs from corpus chunks (missing, stale, duplicate or extra sources); ingest an isolated collection first")
    return len(docs)


def summarize(results):
    summary = {}
    for depth in (3, 8):
        values = [r[f"n{depth}"]["metrics"] for r in results]
        summary[f"n{depth}"] = {
            metric: {"pass": sum(v[metric] == "pass" for v in values),
                     "scored": sum(v[metric] != "not_scored" for v in values)}
            for metric in ("document_coverage", "evidence_coverage", "distractor_ordering")}
        recall = [v["fact_recall"] for v in values if v["fact_recall"] is not None]
        summary[f"n{depth}"]["mean_fact_recall"] = sum(recall) / len(recall) if recall else None
    return summary


async def run_evaluation(args, retrieve, load_models):
    import main as production
    path = args.output or ROOT / "build/corpus/evaluation-runs" / f"{uuid4().hex}.json"
    output = None
    try:
        benchmark, manifest, texts = read_inputs(args.queries, args.manifest, args.corpus_dir)
        requested = {i.strip() for i in args.ids.split(",")} if args.ids is not None else {q["id"] for q in benchmark["queries"]}
        if not requested or requested - {q["id"] for q in benchmark["queries"]}:
            raise ValueError("invalid requested query IDs")
        queries = [q for q in benchmark["queries"] if q["id"] in requested]
        anchors = {a["id"]: a for a in benchmark["anchors"]}
        spans = compile_anchor_spans(anchors, texts, production.chunk_text)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("x", encoding="utf-8") as stream:
            output = {"created_at": datetime.now(timezone.utc).isoformat(),
                      "run_status": "incomplete", "requested_ids": sorted(requested),
                      "executed_ids": [], "config": {"bm25": args.bm25, "rewrite": args.rewrite, "depths": [3, 8]},
                      "input_hashes": {"queries": canonical_hash(benchmark), "manifest": canonical_hash(manifest)},
                      "results": [], "summary": None}
            json.dump(output, stream)
        load_models()
        verify_collection(production.collection, texts, production.chunk_text)
        output["models"] = {"embedding": getattr(production.embed_model, "model_name", None),
                            "reranker": getattr(production.reranker, "model_name", None)}
        if args.rewrite:
            from llm_client import DEFAULT_MODELS_BY_PROVIDER
            provider = os.getenv("LLM_PROVIDER", "anthropic")
            output["models"]["rewrite"] = {"provider": provider, "model": os.getenv("LLM_MODEL", DEFAULT_MODELS_BY_PROVIDER.get(provider))}
        for query in queries:
            entry = {"id": query["id"], "category": query["category"]}
            output["results"].append(entry)
            for depth in (3, 8):
                try:
                    contexts, sources = await retrieve(query["question"], n_results=depth,
                        use_query_rewriting=args.rewrite, use_bm25=args.bm25)
                except (LlmTimeoutError, APIError, HTTPError, ResponseError) as error:
                    print(f"ERROR: {type(error).__name__}: retrieval failed for {query['id']} at n={depth}")
                    return 1
                if len(contexts) > depth:
                    raise ValueError("retrieval exceeded the chunk budget")
                entry[f"n{depth}"] = {"retrieved_sources": sources, "retrieved_contexts": contexts,
                                      "metrics": score_evidence(contexts, sources, query, anchors, spans)}
                write_checkpoint(path, output)
            output["executed_ids"].append(query["id"])
            print(query["id"], "complete")
        output["summary"] = summarize(output["results"])
        output["run_status"] = "complete"
        print(f"Saved {len(queries)} evaluated queries to {path}")
        return 0
    except (OSError, ValueError, KeyError, TypeError, AttributeError, ChromaError) as error:
        print(f"ERROR: missing required key {error}" if isinstance(error, KeyError) else f"ERROR: {error}")
        return 1
    finally:
        if output is not None:
            write_checkpoint(path, output)


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--queries", type=Path, default=ROOT / "data/queries.json")
    parser.add_argument("--manifest", type=Path, default=ROOT / "data/corpus_manifest.json")
    parser.add_argument("--corpus-dir", type=Path, help="Defaults to corpus/<corpus_name>/ from the manifest")
    parser.add_argument("--output", type=Path, help="New result file; existing files are refused")
    parser.add_argument("--ids", help="Comma-separated query IDs; defaults to all queries")
    parser.add_argument("--bm25", action="store_true")
    parser.add_argument("--rewrite", action="store_true")
    parser.add_argument("--check", action="store_true", help="Validate inputs and local PDF/text without models or retrieval")
    return parser.parse_args(argv)


async def main(argv=None):
    args = parse_args(argv)
    if args.check:
        try:
            benchmark, manifest, texts = read_inputs(args.queries, args.manifest, args.corpus_dir)
            from main import chunk_text
            compile_anchor_spans({a["id"]: a for a in benchmark["anchors"]}, texts, chunk_text)
            print(f"Validated {len(benchmark['queries'])} queries and {len(manifest['articles'])} articles")
            return 0
        except (OSError, ValueError, KeyError, TypeError) as error:
            print(f"ERROR: missing required key {error}" if isinstance(error, KeyError) else f"ERROR: {error}")
            return 1
    from main import retrieve, _load_models_and_index
    return await run_evaluation(args, retrieve, _load_models_and_index)


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
