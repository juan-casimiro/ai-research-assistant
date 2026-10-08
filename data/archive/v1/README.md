# Original V1 evaluation assets

This archive preserves the original 19-article biomedical corpus metadata in
[corpus_manifest.json](corpus_manifest.json) and the 133-query golden Q&A in
[golden_qa.json](golden_qa.json) (111 retrieval-scored queries, plus unanswerable cases).
The JSON files retain their original contents and schemas.

All four retrieval result files use dense search and cross-encoder reranking,
evaluated at n=3 and n=8. BM25 adds hybrid fusion; rewriting adds an LLM-rewritten
search query. Neither flag replaces dense retrieval.

| Result file | BM25 | Query rewriting |
| --- | --- | --- |
| [eval_results_baseline.json](evaluations/eval_results_baseline.json) | Off | Off |
| [eval_results_bm25.json](evaluations/eval_results_bm25.json) | On | Off |
| [eval_results_rewrite.json](evaluations/eval_results_rewrite.json) | Off | On |
| [eval_results_bm25_rewrite.json](evaluations/eval_results_bm25_rewrite.json) | On | On |

[context_sufficient_eval_results.json](evaluations/context_sufficient_eval_results.json)
is the saved sufficiency-flag evaluation: it contains 29 expected-True samples
and no expected-False samples. The helper uses n=8 with both retrieval flags off;
the saved file does not record a full model/configuration provenance envelope.
It is not the complete before/after experiment described in ADR-001.

These results describe **V1**, not the forthcoming 55-article corpus, and do not
measure generated-answer accuracy. Historical replay is **not required**.
Existing root-level evaluation helpers still read this archive; new evaluation
outputs go to the repository root. Download/ingestion helpers now default to the
fresh MVP manifest: pass `--manifest data/archive/v1/corpus_manifest.json` for V1.

See [ADR-001](../../../adr/001-chunking-and-retrieval.md) for retrieval decisions
and historical findings, [ADR-002](../../../adr/002-evaluation-methodology.md)
for category/scoring decisions, and the [host guide](../../../README.md#develop-and-evaluate-host)
for the existing commands. ADRs remain in place.
