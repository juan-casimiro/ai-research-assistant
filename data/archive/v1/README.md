# Original V1 evaluation assets

This archive preserves the original 19-article biomedical corpus metadata in
[corpus_manifest.json](corpus_manifest.json) and the 133-query golden Q&A in
[golden_qa.json](golden_qa.json) (111 retrieval-scored queries, plus unanswerable cases).
The JSON files retain their original contents and schemas.

Git tag `evaluation-v1-baseline` marks main at `91cee0c` before JUA-130
replaced the V1 evaluator. It preserves the original evaluator and archived
evidence for reference; historical replay is not required.

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

## Scoring and achievements

The 19-article V1 corpus covered cardiology, diabetes, oncology and outlier topics.
Its 133-question benchmark included 111 scored cases. Dense search with
cross-encoder reranking achieved **96.4% at depth 3 and 98.2% at depth 8**.
BM25 and query rewriting produced no net improvement on this corpus; their
incremental experiments remain in [ADR-001](../../../adr/001-chunking-and-retrieval.md).

| Case | V1 pass rule |
| --- | --- |
| Direct lookup / multi-hop | Expected article appears among retrieved sources |
| Cross-document synthesis | All expected articles appear |
| Cross-document distractor | Expected article appears before any retrieved decoy |
| Unanswerable | Recorded, not positively scored |

These were source-retrieval scores, not complete passage coverage or
generated-answer accuracy. They apply to V1, not the current 55-article corpus.

## High-level technical setup

Historical scripts and their matching inputs are preserved in the
`evaluation-v1-baseline` tag. Use a checkout of that tag for historical commands;
the current branch uses the new evaluation workflow.

V1 ran on the host using local embeddings, a Chroma collection and a cross-encoder
reranker, through production retrieval. PDFs were acquired separately: 17 articles
from PMC and two through publisher browser downloads. Text was extracted and
ingested before evaluation at depths 3 and 8. Optional query rewriting used an LLM.
The historical evaluator was `eval_golden.py`; it has since been replaced.
`compare_evals.py` remains a legacy utility for the saved V1 result format.
Historical replay is not required, and old scripts are not current setup guidance.

See [ADR-002](../../../adr/002-evaluation-methodology.md) for evaluation strategy
and the [current workflow](../../../tools/evaluation/evaluation-workflow.md)
for active commands.

Full historical records: [methodology](methodology.md) and
[corpus acquisition](corpus-acquisition.md).
