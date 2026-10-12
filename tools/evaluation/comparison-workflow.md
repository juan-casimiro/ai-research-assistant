# Compare saved retrieval runs

Work offline from current result JSON files. Do not trigger ingestion or new
evaluations. Do not open provider response logs by default; inspect a specific
query log only when that query needs investigation.

Select a baseline first, then one or more experiment files from the same
benchmark/corpus sweep. Labels come from file stems, stripping `eval_results_`,
and must be unique. Configuration and provider/model differences are allowed; the source results
retain their configuration and model metadata. No current corpus or gold files are needed.

From the active repository root, use its Python environment. For the four saved
MVP runs, run this compatibility check:

```sh
.venv/bin/python -m tools.evaluation.compare_runs \
  data/evaluations/mvp/2026-10-09-anthropic/eval_results_baseline.json \
  data/evaluations/mvp/2026-10-09-anthropic/eval_results_bm25.json \
  data/evaluations/mvp/2026-10-09-anthropic/eval_results_rewrite.json \
  data/evaluations/mvp/2026-10-09-anthropic/eval_results_bm25_rewrite.json --check
```

The check requires complete runs, query/manifest hashes that match across runs,
unique requested/executed/result IDs with matching sets, depths 3 and 8 in every
query, matching categories and valid metrics. Query ordering may differ. A
failure stops comparison; select compatible files rather than repairing results
or changing benchmark pins. This checks recorded metadata, not the underlying
collection or reproducibility of the original evaluator.

Run the same command replacing `--check` with
`--output-dir data/evaluations/mvp/2026-10-09-anthropic/comparison` to save:

- `summary.md`: overall and category means, percentage-point deltas and counts
  of improved, regressed, unchanged and excluded queries for each metric/depth.
- `per_query.csv`: every paired metric, including unchanged and excluded cases,
  with before/after values, numeric delta and direction. Boolean metrics use 0/1.

An existing output directory is refused; use a new directory for another report.
Without an output option, the summary prints to stdout. Reports compare each
experiment to the first file; select another baseline to examine another pair.
Add a short interpretation beside these artifacts and link it from the saved
run README. Recompute summary values from per-query metrics, rather than trusting
cached run summaries. Each denominator includes only queries scored in both
runs for that metric; report excluded cases separately (never count them as
unchanged). Fact recall is a query mean, not a pooled fact-level score.

Describe findings as one observed sweep, not a stable strategy ranking or proof
of significance. Independent rewrite samples by depth/configuration prevent
attributing differences solely to BM25. Document coverage is separate from
pinned-excerpt coverage; literal misses do not prove absent semantic support.
Absent-fact cases have no positive score, false-premise cases measure correction
evidence, and source-conflict cases retain both attributed readings. Neither
retrieval metrics nor distractor ordering establish generated-answer quality.
Current results cannot replay or be directly compared to V1 scores. See the
[metric definitions](../../data/queries-schema.md#metrics).

Offline regression checks: `.venv/bin/python -m unittest tests.test_compare_runs -v`.
