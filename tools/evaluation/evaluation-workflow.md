# Retrieval evaluation

Run from the active repository root using its Python environment. Defaults are
`data/queries.json`, `data/corpus_manifest.json`, and `corpus/<corpus_name>/`, taken
from the manifest's top-level `corpus_name` (currently `mvp`).

## Readiness and prerequisite routing

Before retrieval, check the manifest and Q&A inputs, local PDFs and adjacent text,
and the collection selected by the documented path rule. Use `--check` below for
input validation; it does not check Chroma. Folder existence alone does not prove
collection readiness: the evaluator verifies exact stored source/chunk membership
before any queries run.

If preparation is missing, explain only the missing steps in dependency order:

- Missing manifest or acquired/verified PDFs and text: follow
  [generate-corpus-metadata](../../.agents/skills/generate-corpus-metadata/SKILL.md),
  using its existing-manifest flow when a manifest is already available.
- Missing collection: follow
  [ingest-corpus](../../.agents/skills/ingest-corpus/SKILL.md), after acquisition
  is complete, then rerun evaluation validation.
- Invalid benchmark pins, hashes or evidence, or a stale/incomplete collection:
  report the specific conflict and stop. Do not rewrite gold, reset data or
  delete a collection to make evaluation pass.

An evaluation-only request does not authorize missing acquisition or ingestion
work. An explicit request for the whole flow authorizes the necessary preparation
within the linked workflows' safeguards. Explain missing steps before starting
that preparation. If all prerequisites pass, run the requested evaluation directly
without a prerequisite warning or an extra confirmation. Paid query rewriting
still requires the explicit approval described below.

## Evaluation

1. Validate Q&A and manifest inputs with `python -m tools.evaluation.evaluate --check`.
   This also checks every local PDF/text hash, evidence offset and span reachability; it runs no
   models, ingestion, retrieval or provider calls. Missing/changed files or
   conflicting source IDs stop the run. Report them; do not rewrite gold or pins.
2. Evaluation reads the collection beside the corpus, at
   `corpus/<corpus_name>/chroma`, and verifies exact source/chunk membership.
   It stops if that folder is missing; create it with the
   [ingestion workflow](../corpus/ingestion-workflow.md). `CHROMA_PATH` is not
   needed: only an exported value replaces the folder, and `.env` does not.
   Do not reset shared data.
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
See the [metric definitions and chunk-budget limitation](../../data/queries-schema.md#metrics).

Preserve the original archived V1 gold/results. New runs record input hashes and retrieval options and cannot be described as reproductions of historical scores.
Offline verification: `python -m unittest discover -s tests -t . -v`.
