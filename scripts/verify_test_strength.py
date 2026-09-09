"""Curated behavioural mutations, each checked pass -> fail -> restored pass.

Uses isolated copies of production source and tests, leaving the checkout untouched.
This is targeted test-strength analysis, not an exhaustive mutation score. Run from
repo root with the repository Python and --output-dir outside the repository.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

# name, source, original, replacement, selected unittest, expected failure diagnostic
MUTATIONS = [
    ("question-bound", "main.py", "max_length=1000", "max_length=1001",
     "test_api.ApiTests.test_invalid_query_is_422_before_retrieval", "200 != 422"),
    ("readiness-gate", "main.py", "async def query(request: QueryRequest) -> QueryResponse:\n    _require_ready()",
     "async def query(request: QueryRequest) -> QueryResponse:\n    pass",
     "test_api.ApiTests.test_health_and_endpoints_report_loading_and_startup_error", "200 != 503"),
    ("timeout-status", "main.py",
     '        raise HTTPException(\n'
     '            status_code=504,\n'
     '            detail="upstream LLM request timed out",\n'
     '        ) from exc\n'
     '\n'
     '    return QueryResponse(',
     '        raise HTTPException(\n'
     '            status_code=500,\n'
     '            detail="upstream LLM request timed out",\n'
     '        ) from exc\n'
     '\n'
     '    return QueryResponse(',
     "test_api.ApiTests.test_grounded_timeout_is_504_without_retry", "500 != 504"),
    ("rewrite-timeout-status", "main.py",
     '        raise HTTPException(\n'
     '            status_code=504,\n'
     '            detail="upstream LLM request timed out",\n'
     '        ) from exc\n'
     '\n'
     '    context =',
     '        raise HTTPException(\n'
     '            status_code=500,\n'
     '            detail="upstream LLM request timed out",\n'
     '        ) from exc\n'
     '\n'
     '    context =',
     "test_api.ApiTests.test_real_rewrite_path_timeout_stops_before_answer_generation", "500 != 504"),
    ("sufficiency-signal", "main.py", "context_sufficient=result.context_sufficient", "context_sufficient=True",
     "test_api.ApiTests.test_insufficient_context_keeps_retrieved_sources_and_reason", "FAIL:"),
    ("source-order", "main.py", "sources=list(dict.fromkeys(sources))", "sources=sorted(set(sources), reverse=True)",
     "test_main.QueryContractTests.test_query_preserves_ranked_context_and_deduplicated_sources", "FAIL:"),
    ("pool-cap", "main.py", "reciprocal_rank_fusion(ranked_lists)[:FUSED_CANDIDATE_POOL]", "reciprocal_rank_fusion(ranked_lists)",
     "test_retrieval.RetrievalPipelineTests.test_candidate_pool_is_capped_before_reranking", "expected call not found"),
    ("disable-rewrite", "main.py", "    if use_query_rewriting:", "    if False:",
     "test_retrieval.RetrievalPipelineTests.test_optional_retrievers_fuse_variants_and_keep_original_rerank_question", "FAIL:"),
    ("disable-sparse", "main.py", "if use_bm25 and bm25_index is not None:", "if False:",
     "test_retrieval.RetrievalPipelineTests.test_optional_retrievers_fuse_variants_and_keep_original_rerank_question", "FAIL:"),
    ("fusion-consensus", "main.py", "scores.get(doc, 0.0) + 1.0 / (k + rank)", "1.0 / (k + rank)",
     "test_retrieval.FusionTests.test_consensus_promotes_lower_ranked_document_and_deduplicates", "Lists differ"),
    ("seed-opt-out", "main.py", "if SEED_ON_EMPTY:", "if True:",
     "test_startup_ingest.StartupTests.test_disabled_seeding_never_touches_seed_path", "Expected '_seed_if_empty' to not have been called"),
    ("seed-populated-store", "main.py", "if collection.count() > 0:", "if False:",
     "test_startup_ingest.SeedAndIngestTests.test_seed_reads_only_nonempty_text_and_does_not_reingest_populated_store", "1 != 0"),
    ("startup-failure-signal", "main.py", '_startup_error = f"{type(exc).__name__}: {exc}"', "_startup_error = None",
     "test_startup_ingest.StartupTests.test_failure_in_any_startup_phase_keeps_service_unready", "None !="),
    ("long-paragraph-continue", "main.py", "chunks.append(para[i : i + chunk_size])\n            continue", "chunks.append(para[i : i + chunk_size])",
     "test_startup_ingest.ChunkingTests.test_long_paragraph_preserves_preceding_and_trailing_text_once", "Lists differ"),
    ("lazy-rerank-on-loop", "main.py", "scores = await asyncio.to_thread(\n        lambda: list(reranker.rerank(question, fused))\n    )", "scores = list(reranker.rerank(question, fused))",
     "test_main.RetrievalTests.test_rerank_runs_off_loop_and_preserves_top_n_order", "is not true"),
    ("llm-retries", "main.py", "max_retries=0", "max_retries=2",
     "test_main.LlmConfigurationTests.test_load_models_bounds_llm_client", "expected call not found"),
    ("distractor-order", "eval_golden.py", "sources.index(expected) >= sources.index(distractor)", "sources.index(expected) < sources.index(distractor)",
     "test_evaluation.ScoringTests.test_category_scoring_including_missing_metadata_and_distractor_order", "FAIL:"),
    ("synthesis-all-sources", "eval_golden.py", "all(doc in sources for doc in expected_docs)", "any(doc in sources for doc in expected_docs)",
     "test_evaluation.ScoringTests.test_category_scoring_including_missing_metadata_and_distractor_order", "FAIL:"),
    ("false-premise-exclusion", "eval_context_sufficient.py", 'FALSE_PREMISE_EXCLUSIONS = {"q083"}', "FALSE_PREMISE_EXCLUSIONS = set()",
     "test_evaluation.SufficiencyEvaluationTests.test_buckets_exclude_false_premise_and_sample_only_n8_passes_reproducibly", "Lists differ"),
    ("false-positive-denominator", "eval_context_sufficient.py", "false_positives / false_bucket_total", "false_positives / len(samples)",
     "test_evaluation.SufficiencyEvaluationTests.test_error_rates_use_separate_denominators_and_id_filter", "FAIL:"),
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--only", nargs="+", choices=[m[0] for m in MUTATIONS])
    args = parser.parse_args()
    root = Path.cwd()
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)
    report = []
    for name, filename, old, new, test, diagnostic in MUTATIONS:
        if args.only and name not in args.only:
            continue
        with tempfile.TemporaryDirectory(prefix=name + "-", dir=output) as directory:
            work = Path(directory)
            for path in root.glob("*.py"):
                shutil.copyfile(path, work / path.name)
            target = work / filename
            original = target.read_bytes()
            source = original.decode()
            matches = source.count(old)
            if matches != 1:
                raise RuntimeError(f"{name}: expected exactly one mutation target, found {matches}")
            phases = {}
            try:
                for phase in ("before", "broken", "restored"):
                    target.write_bytes(source.replace(old, new, 1).encode() if phase == "broken" else original)
                    # Supported by pinned python-dotenv 1.2.2; prevents ancestor .env discovery.
                    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "TMPDIR": str(output),
                           "PYTHON_DOTENV_DISABLED": "1"}
                    result = subprocess.run([sys.executable, "-B", "-m", "unittest", test, "-v"],
                                            cwd=work, env=env, capture_output=True, text=True, timeout=45)
                    log = result.stdout + result.stderr
                    (output / f"{name}-{phase}.log").write_text(log)
                    phases[phase] = result.returncode
                    if phase == "broken":
                        if result.returncode != 1 or "FAIL:" not in log or diagnostic not in log:
                            raise RuntimeError(f"{name}: did not fail for expected reason; inspect log")
                    elif result.returncode:
                        raise RuntimeError(f"{name}: {phase} failed; inspect log")
            finally:
                target.write_bytes(original)
            report.append({"mutation": name, "file": filename, "test": test, "exit_codes": phases,
                           "expected_diagnostic": diagnostic,
                           "restored_sha256": hashlib.sha256(target.read_bytes()).hexdigest()})
            (output / "mutations.json").write_text(json.dumps(report, indent=2))
            print(f"{name}: pass -> expected failure -> restored pass", flush=True)
    print(f"{len(report)} curated mutations detected; no exhaustive mutation percentage claimed.")


if __name__ == "__main__":
    main()
