"""Run the four V1-style retrieval combinations with per-query rewrite logs."""
import argparse
import asyncio
from collections import Counter
from copy import copy
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import shutil

from tools.evaluation import evaluate

COMBINATIONS = (("baseline", False, False), ("bm25", True, False),
                ("rewrite", False, True), ("bm25_rewrite", True, True))


async def run_combination(args, *, inputs=None):
    """Capture the existing provider invocation; do not make additional calls."""
    import main as production
    import llm_client

    inputs = inputs if inputs is not None else evaluate.read_inputs(args.queries, args.manifest, args.corpus_dir)
    if not args.rewrite:
        return await evaluate.run_evaluation(args, production.retrieve, production._load_models_and_index, inputs=inputs)

    benchmark, _, _ = inputs
    selected = set(args.ids.split(",")) if args.ids else None
    queries = [q for q in benchmark["queries"] if selected is None or q["id"] in selected]
    response_dir = args.output.with_suffix(".responses")
    response_dir.mkdir(exist_ok=False)
    original_invoke = llm_client._invoke
    current = {}
    call_count = 0
    recorded = Counter()

    async def logged_retrieve(question, **kwargs):
        nonlocal call_count
        query = queries[call_count // 2]
        if question != query["question"]:
            raise ValueError("response log query order differs from evaluation")
        current.update(query_id=query["id"], depth=kwargs["n_results"])
        call_count += 1
        result = await production.retrieve(question, **kwargs)
        if recorded[(current["query_id"], current["depth"])] != 1:
            raise ValueError("expected one rewrite response log for this query/depth")
        return result

    async def logged_invoke(runnable, messages, timeout):
        key = (current["query_id"], current["depth"])
        if recorded[key]:
            raise ValueError("duplicate rewrite invocation for this query/depth")
        provider = os.getenv("LLM_PROVIDER", "anthropic").strip().lower()
        record = {"timestamp": datetime.now(timezone.utc).isoformat(), **current,
                  "provider": provider,
                  "model": llm_client.DEFAULT_MODELS_BY_PROVIDER.get(provider),
                  "request_messages": messages}
        try:
            response = await original_invoke(runnable, messages, timeout)
            record["response"] = response.model_dump(mode="json")
            return response
        except Exception as error:
            record["error_type"] = type(error).__name__
            raise
        finally:
            with (response_dir / f"{current['query_id']}.jsonl").open("a", encoding="utf-8") as stream:
                stream.write(json.dumps(record, ensure_ascii=False) + "\n")
            if "response" in record:
                recorded[key] += 1

    # This CLI runs sequentially in its own process; always restore the hook.
    llm_client._invoke = logged_invoke
    try:
        status = await evaluate.run_evaluation(args, logged_retrieve, production._load_models_and_index, inputs=inputs)
    finally:
        llm_client._invoke = original_invoke
    if status == 0:
        expected = {(q["id"], depth) for q in queries for depth in (3, 8)}
        if set(recorded) != expected or any(count != 1 for count in recorded.values()):
            print("ERROR: evaluation completed but rewrite response logs are incomplete")
            return 1
    return status


def publish_results(run_dir, destination, requested, inputs):
    """Validate the whole batch before copying only results into a new directory."""
    hashes = {"queries": evaluate.canonical_hash(inputs[0]),
              "manifest": evaluate.canonical_hash(inputs[1])}
    paths = []
    for name, bm25, rewrite in COMBINATIONS:
        path = run_dir / f"eval_results_{name}.json"
        result = json.loads(path.read_text(encoding="utf-8"))
        ids = [row["id"] for row in result["results"]]
        if (result["run_status"] != "complete" or result["summary"] is None
                or result["requested_ids"] != sorted(requested)
                or sorted(result["executed_ids"]) != sorted(requested)
                or sorted(ids) != sorted(requested)
                or result["config"] != {"bm25": bm25, "rewrite": rewrite, "depths": [3, 8]}
                or result["input_hashes"] != hashes
                or any(not all(f"n{depth}" in row for depth in (3, 8)) for row in result["results"])):
            raise ValueError(f"incomplete or inconsistent evaluation: {path}")
        paths.append(path)
    destination.mkdir(parents=True, exist_ok=False)
    try:
        for path in paths:
            shutil.copy2(path, destination / path.name)
    except Exception:
        # Only remove the directory we just created; retain all staged evidence.
        shutil.rmtree(destination)
        raise


async def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--queries", type=Path, default=evaluate.ROOT / "data/queries.json")
    parser.add_argument("--manifest", type=Path, default=evaluate.ROOT / "data/corpus_manifest.json")
    parser.add_argument("--corpus-dir", type=Path)
    parser.add_argument("--ids", help="Comma-separated query subset; defaults to all queries")
    parser.add_argument("--output-dir", type=Path, help="Final results directory; existing paths are refused. Runs/logs stay under build/corpus.")
    args = parser.parse_args(argv)
    args.chroma_path = os.environ.get("CHROMA_PATH")
    try:
        inputs = evaluate.read_inputs(args.queries, args.manifest, args.corpus_dir)
        benchmark, manifest, _ = inputs
        requested = {i.strip() for i in args.ids.split(",")} if args.ids is not None else {q["id"] for q in benchmark["queries"]}
        if not requested or requested - {q["id"] for q in benchmark["queries"]}:
            raise ValueError("invalid requested query IDs")
        args.ids = ",".join(sorted(requested))
        from tools.corpus.download_corpus import collection_path, named_corpus_dir, corpus_name
        chroma = collection_path(args.corpus_dir or named_corpus_dir(manifest), args.chroma_path)
        if not chroma.is_dir():
            raise ValueError(f"no collection at {chroma}; ingest the corpus first")
        name = corpus_name(manifest)
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        output_dir = evaluate.ROOT / "build/corpus/evaluation-runs" / name / timestamp
        destination = args.output_dir or evaluate.ROOT / "data/evaluations" / name / timestamp
        if destination.exists() or destination.is_symlink():
            raise FileExistsError(f"final destination already exists: {destination}")
        output_dir.mkdir(parents=True, exist_ok=False)
        for name, bm25, rewrite in COMBINATIONS:
            run_args = copy(args)
            run_args.bm25, run_args.rewrite = bm25, rewrite
            run_args.output = output_dir / f"eval_results_{name}.json"
            print(f"START {name}")
            status = await run_combination(run_args, inputs=inputs)
            if status:
                print(f"Stopped at {name}; preserve incomplete results and logs in {output_dir}")
                return status
        publish_results(output_dir, destination, requested, inputs)
        print(f"Saved all four evaluations to {destination.resolve()}; logs remain in {output_dir.resolve()}")
        return 0
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"ERROR: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
