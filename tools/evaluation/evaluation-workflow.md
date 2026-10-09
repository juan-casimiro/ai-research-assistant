# Retrieval evaluation

Run from the active repository root using its Python environment. Defaults are
`data/queries.json`, `data/corpus_manifest.json`, and `corpus/mvp/`.

1. Validate Q&A and manifest inputs with `python -m tools.evaluation.evaluate --check`.
   This also checks every local PDF/text hash and evidence offset; it runs no
   models, ingestion, retrieval or provider calls. Missing/changed files or
   conflicting source IDs stop the run. Report them; do not rewrite gold or pins.
2. Use a previously ingested isolated collection at the selected `CHROMA_PATH`,
   with `SEED_ON_EMPTY=false`. Evaluation verifies exact source/chunk membership.
   Creating or resetting a collection is separate work; do not reset shared data.
3. Run the evaluator. `--bm25` enables hybrid retrieval; `--ids` selects a
   comma-separated query subset. `--rewrite` invokes the configured LLM provider;
   obtain explicit approval for the provider and run scale/cost before paid calls.

```sh
python -m tools.evaluation.evaluate --check
python -m tools.evaluation.evaluate
python -m tools.evaluation.evaluate --bm25 --ids q041,q042
```

Explicit inputs use `--queries`, `--manifest`, `--corpus-dir`; `--output` selects
a new result path. The default is a unique ignored JSON file under
`build/corpus/evaluation-runs/`. Existing outputs are refused. Failed runs retain
completed results as an incomplete checkpoint; never report it as a complete run.

Report requested/executed counts, depths (3 and 8), configuration, separate
source-document and pinned-excerpt coverage, fact recall and distractor ordering.
Absent-fact cases have no positive retrieval score. False-premise cases measure
correction evidence, not successful premise correction. Source-conflict cases
retain both attributed readings. No generated answers or answer judge are run.
Missed literal excerpts do not prove absent semantic support.

Preserve the original archived V1 gold/results. New runs record input hashes and retrieval options and cannot be described as reproductions of historical scores.
Offline verification: `python -m unittest discover -s tests -t . -v`.
