# Diabetes benchmark and cardiology interference — v1

JUA-111 audits all 35 legacy cases using the six diabetes sources, then selects
**16 diabetes/overlap articles** and authors **49 cases**. The combined selected
corpus contains **32 articles**: the original 21 cardiology records and 11 new
verified diabetes articles. Target size follows the coverage gaps, rather than
matching the cardiology article count. Independent PR/clinical review is pending.

The retained sources cover adjunctive pharmacotherapy, zinc/hypoxia DKD,
sleep/cardiometabolic risk and CGM counseling. New sources add Cameroon hospital
epidemiology, sex-hormone genetics, sulfonylurea pharmacogenetic adverse response,
a primary semaglutide non-inferiority trial, digital DSMES+CGM patient outcomes,
three-cohort sleep/multimorbidity and a second HIF/zinc review. Five already-selected
cardiology sources supply SGLT2/CKD, geriatric HFpEF, cardiorenal therapy,
T2DM/BP genetics and resistant-hypertension overlap. Roles are query relative.

The restrictive original sex-specific GWAS (CC BY-NC 4.0 with a territorial USA
public-domain notice) and Raman epidemiology paper (CC BY 2.0) are excluded under
the exact CC BY 4.0/CC0 1.0 project gate. This is a selection policy, not a claim
that their reuse is illegal. New cohorts inherit none of their numerical gold.

## Release artifacts

- [AUDIT.md](AUDIT.md) and [legacy_audit.json](legacy_audit.json): all original
  cases, source hashes, findings and final dispositions.
- [manifest.json](manifest.json), [metadata/](metadata/) and
  [ATTRIBUTION.md](ATTRIBUTION.md): complete PubMed abstracts, distinct authored
  summaries, bibliographic identity, exact deposit/licence and source-byte pins,
  readable-PDF checks and credit-line review. Earlier discovery queries unavailable
  for transferred candidates are explicitly missing, never reconstructed as fact.
- [evidence_map.json](evidence_map.json): source selection locations.
- [queries.json](queries.json), [case_dependencies.json](case_dependencies.json)
  and [case_review.json](case_review.json): 23 revised legacy IDs, 12 retired
  IDs, 26 new IDs, 55 exact physical-page/offset anchors and query-relative roles.
  d025 accepts either of two complete single-article evidence sets. Four absent
  facts and three false premises are separate; corrections require positive evidence.
- [migration.json](migration.json): explicit ID mapping and original file hashes.
- [conditions.json](conditions.json): C1=C2 is the actual 16-article required/
  alternative source union; C3 contains all 32 articles. No extra competitor-only
  article is needed to create genuine related-source competition here.
- [cardio-regression/](cardio-regression/): an extended selection envelope with
  the original **45 questions and 77 anchors copied exactly**. C1 is the original
  21 articles; C2=C3 is 32. Historical cardiology run provenance is unchanged.
- [REPORT.md](REPORT.md) and [runs/](runs/): local vector/re-ranker results,
  receipts, compatible comparisons, manual context review and limitations.

Original `corpus_manifest.json`, `golden_qa.json` and the cardiology release remain
byte-identical. PDFs, raw article XML, extracted texts, rendered pages and Chroma
stores remain local and untracked. Supplements are not included. The release
pins evidence as printed, including source contradictions; it does not repair them
or certify medical conclusions. No generated answer or paid judge was evaluated.

## Acquire and verify

Run from the repository root using Python 3.12 and the project environment.
Use the supported PMC Cloud download route; never silently accept changed bytes:

```sh
.venv/bin/python download_corpus.py \
  --manifest benchmark/diabetes/v1/manifest.json --corpus-dir corpus/diabetes-v1
```

Acquire XML and extract text with the same pinned recipe described in the
[cardiology selection instructions](../../cardiology/v1/README.md#acquire-and-verify-local-pdfstext),
substituting `benchmark/diabetes/v1` and `corpus/diabetes-v1` throughout. The
metadata snapshots include the XML URLs; the manifest supplies exact hashes.
Then verify metadata, XML, PDF, extraction, attribution, conditions and baselines:

```sh
.venv/bin/python verify_cardiology_selection.py \
  --selection-dir benchmark/diabetes/v1 --corpus-dir corpus/diabetes-v1
.venv/bin/python verify_benchmark_reachability.py \
  --benchmark benchmark/diabetes/v1 --corpus-dir corpus/diabetes-v1 --condition C3
.venv/bin/python -m unittest discover -v
```

## Isolated local retrieval

The [ingestion helper](runs/ingest_isolated.py) requires `SEED_ON_EMPTY=false`
and a **fresh, unused** `CHROMA_PATH`. It uses production ingestion/chunking and
checks the exact stored chunk multiset, BM25 count and loaded model fingerprints.
It never starts a server. Keep the receipt and verify collection identity before
reusing it. Do not touch another task's stores.

Example for the combined corpus (choose your own unused directory and outputs):

```sh
SEED_ON_EMPTY=false CHROMA_PATH=/tmp/jua111-combined-fresh PYTHONPATH=. \
  .venv/bin/python benchmark/diabetes/v1/runs/ingest_isolated.py \
  --benchmark benchmark/diabetes/v1 --corpus-dir corpus/diabetes-v1 \
  --condition C3 --receipt /tmp/jua111-combined-ingestion.json
SEED_ON_EMPTY=false CHROMA_PATH=/tmp/jua111-combined-fresh \
  .venv/bin/python eval_golden.py --benchmark benchmark/diabetes/v1 \
  --corpus-dir corpus/diabetes-v1 --condition C3 --ids q003,d006,d010,d019 \
  --output /tmp/jua111-focused.json
```

Choose affected IDs from the dependency map during iteration. The released runs
provide complete coverage for the final topic and interference comparisons,
justified by broad article expansion. They use only vector retrieval plus the
production reranker at n=3 and n=8; BM25, rewriting, generation and judge runs are
omitted. `--ids` does not ingest a corpus. Outputs refuse overwrites; check exact
requested/executed IDs. Paid configurations need separate explicit approval.

For the full diabetes pair, ingest/evaluate C2 on 16 articles and C3 on 32 with
identical release/scorer/config. For frozen cardiology, ingest the regression
C1 (21) and evaluate C2 (32) using the combined store. The two envelope files
share identical 32-article manifest tuples. Compare each matching pair:

```sh
.venv/bin/python compare_evals.py --nested-corpus \
  benchmark/diabetes/v1/runs/diabetes-C2-reviewed.json \
  benchmark/diabetes/v1/runs/diabetes-C3-reviewed.json
.venv/bin/python compare_evals.py --nested-corpus \
  benchmark/diabetes/v1/runs/cardio-C1-vector.json \
  benchmark/diabetes/v1/runs/cardio-C2-vector.json
```

Historical cardiology C2 output cannot be directly paired with this expanded
selection envelope: its provenance differs. The fresh 21-article regression
baseline avoids relabelling historical results. Full-span coverage is a stricter
measure than semantic sufficiency; document presence alone is not evidence success.

The original frozen authoring envelope and local retrieval files are retained in
`runs/initial-authoring/` and `runs/*-vector.json`. A subsequent source/standards
review corrected four categories and two reference descriptions, without changing
questions, anchors, sources or evidence bindings. The annotation revisions are
recorded in `case_review.json`. [rescore_saved.py](runs/rescore_saved.py) checks
that invariance, recomputes metrics on the original contexts, requires identical
per-case scores and records parent hashes/provenance. The `*-reviewed.json` pair
contains the final category summaries; it makes **zero retrieval calls** and
is explicitly derived, rather than relabelling the original run.

## Descriptive corrections after review

Claude review identified rank wording, stale Guo selection-summary notes,
per-case freeze chronology and retrieved-list disclosure. The current manifests
and query review fields are corrected with linked fingerprints and explicit
case revisions. [review_corrections.json](review_corrections.json) records the
changes and preserved original output hashes. Questions, gold anchors, source
bytes, evidence bindings and membership tuples are unchanged.

All published evaluation outputs remain byte-identical. The preserved
[runs/evaluated-release/](runs/evaluated-release/) snapshot contains the envelopes
for the reviewed diabetes summaries and cardiology regression. Original diabetes
vector runs use `runs/initial-authoring/queries.json` and its conditions, with the
same frozen manifest preserved in `runs/evaluated-release/`. New runs
using the current descriptive revision have different release fingerprints and
must not be directly paired with those historical files. To reproduce their
original envelopes, substitute `--benchmark benchmark/diabetes/v1/runs/evaluated-release`
in the ingestion/evaluation commands; for cardiology use its `cardio-regression`
subdirectory. The source corpus is still `corpus/diabetes-v1`. Archived metadata
responses remain in this release's original `metadata/` directory.

The saved-context rescore can be reproduced without loading models or retrieving:

```sh
PYTHONPATH=. .venv/bin/python benchmark/diabetes/v1/runs/rescore_saved.py \
  benchmark/diabetes/v1/runs/diabetes-C2-vector.json /tmp/jua111-rescore-check.json \
  --benchmark benchmark/diabetes/v1/runs/evaluated-release
```

[retrieval_list_changes.json](runs/retrieval_list_changes.json) records five
changed case-depth lists despite unchanged verdicts. Each focused-review context
set identifies its exact original parent run. The q051 AF hit moves from rank 1
to rank 0; its underlying candidate-pool mechanism remains unconfirmed.

## Gold correction revision — 2026-10-05

The active query set incorporates the [source-grounded correction ledger](../../corrections/2026-10-05/README.md). Prior runs retain their original questions and fingerprints; they are not runs of this corrected revision. The corpus and evaluation strategy are unchanged.
