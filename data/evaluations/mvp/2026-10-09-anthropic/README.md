# MVP evaluation results — 9 October 2026

Four completed runs over 55 articles, 3,638 chunks and all 158 queries, at depths 3 and 8. All use dense retrieval and cross-encoder reranking. Rewriting uses Anthropic `claude-haiku-4-5-20251001`. Input hashes match across the four runs.

| Configuration | Depth | Document coverage | Pinned-excerpt coverage | Mean fact recall | Distractor ordering |
| --- | ---: | ---: | ---: | ---: | ---: |
| [baseline](eval_results_baseline.json) | 3 | 122/147 (83.0%) | 21/147 (14.3%) | 19.2% | 14/15 (93.3%) |
| [baseline](eval_results_baseline.json) | 8 | 132/147 (89.8%) | 43/147 (29.3%) | 35.4% | 14/15 (93.3%) |
| [bm25](eval_results_bm25.json) | 3 | 124/147 (84.4%) | 24/147 (16.3%) | 21.2% | 14/15 (93.3%) |
| [bm25](eval_results_bm25.json) | 8 | 135/147 (91.8%) | 48/147 (32.7%) | 39.2% | 14/15 (93.3%) |
| [rewrite](eval_results_rewrite.json) | 3 | 124/147 (84.4%) | 21/147 (14.3%) | 18.9% | 14/15 (93.3%) |
| [rewrite](eval_results_rewrite.json) | 8 | 128/147 (87.1%) | 46/147 (31.3%) | 37.5% | 14/15 (93.3%) |
| [bm25_rewrite](eval_results_bm25_rewrite.json) | 3 | 125/147 (85.0%) | 24/147 (16.3%) | 20.9% | 14/15 (93.3%) |
| [bm25_rewrite](eval_results_bm25_rewrite.json) | 8 | 135/147 (91.8%) | 50/147 (34.0%) | 39.5% | 14/15 (93.3%) |

Each JSON preserves full retrieved contexts, source IDs, per-query scores, model/configuration settings and input hashes. The interrupted preliminary rewrite run is excluded.

Document and excerpt coverage score 147 queries; 11 absent-fact cases are not positively scored. False-premise cases measure correction evidence, not successful premise correction. Source-conflict cases retain both attributed readings. Excerpt misses do not prove absent semantic support. No answers or answer judging were generated.

The four combinations mirror V1, but these scores are not directly comparable: corpus, questions and scoring changed. This is one sweep per configuration; queries are rewritten independently for each depth and configuration.

Full provider responses are retained locally under ignored `build/corpus/evaluation-runs/20261009T203516Z-combinations/{rewrite_full,bm25_rewrite}.responses/<query-id>.jsonl`. Each rewriting run has 158 query files and 316 verified successful responses. Agents should not load logs by default; inspect a query log only for a specific investigation.

For a new run, follow the evaluate-retrieval skill and run `python -m tools.evaluation.evaluate_combinations --output-dir <new-directory>`. It generates all four V1-style result files and per-query rewrite logs. Set `LLM_PROVIDER=anthropic LLM_MODEL=claude-haiku-4-5-20251001` for this model; use the same corpus and unset exported `CHROMA_PATH`. Paid rewriting reruns require explicit approval. These saved runs used the same evaluator and a run-scoped response-capture launcher; the checked-in batch script now provides that orchestration.
