# First cardiology retrieval baseline

On 2026-10-02, vector retrieval with the production cross-encoder reranker
retrieved complete source sets much more often than complete pinned evidence.
In one execution per condition, adding two related competitors coincided with
one case (c007) losing complete pinned evidence at n=8: 4/38 → 3/38. Document
coverage stayed 31/38 at n=8; c008 lost document coverage at n=3. This single-run
observation does not establish a stable competition effect. This is a cardiology
retrieval baseline, not answer accuracy, a BM25 comparison or a full-corpus claim.

## Frozen release and experiment

Both historical experiments ran against commit `9910c2f` plus the
then-uncommitted ingestion helper, preserved as
[`ingest_isolated_20261002.py`](../../../../../tools/evaluation/historical/benchmark/cardiology/v1/runs/ingest_isolated_20261002.py) and bound by
its original SHA-256 in `artifacts.json`. The production evaluation code was
unchanged. The current reproduction helper adds explicit safety guards and atomic
receipt finalization; it was not used for these saved runs. Both experiments use
the unchanged
`cardiology-queries-v1` release, `pinned-span-coverage-v3` scorer and
`minimum-evidence-chunks-v3` feasibility contract. The original authoring and experiment fingerprints remain preserved. Clinical independent review remains a limit.

C1 is the 19-article union of required/accepted alternative answer sources. C2 is
that identical union plus `PMC10619268` (Korean resistant-hypertension consensus,
117 chunks) and `PMC12436478` (echo/AHRE prediction, 40 chunks). Membership, exact
PDF/text tuples and per-source counts are preserved in [ingestion receipts](runs).
C1 contains 1,113 chunks; C2 contains 1,270. Query-relative decoys already in C1
are not removed: for example both STEMI score papers answer their own cases.

The pinned 21-article metadata/XML/PDF/text verification passed. Each condition
used a fresh local Chroma directory, collection `documents`, `SEED_ON_EMPTY=false`,
production `main.ingest`, `embed` and `chunk_text`. No server or seed was started.
The stored source/text multiset matched production chunking exactly, including
multiplicities; the BM25 index count matched the collection. Production models
were fingerprinted during ingestion and evaluation. The runner checked collection
identity before executing production `retrieve()` with rewriting and BM25 off.
Production reranker threading and relevance order were unchanged.

[Results](runs/C1-vector.json) and [C2 results](runs/C2-vector.json) preserve all
contexts, zero-based ranks, anchor matches, facts, feasibility, query/scorer/source/
dependency/model hashes, exact membership, timestamps and requested/executed IDs.
[Artifact checksums](runs/artifacts.json) bind the original and current helpers,
receipts and results.
Both receipts' loaded-model fingerprints equal those of their evaluation run;
common model, query, scorer and retrieval fingerprints agree across conditions.

All 45 release IDs ran at both n=3 and n=8 (180 retrieval calls total), with zero
missing IDs. Complete coverage is necessary to establish this first nested-corpus
baseline; this is not a rerun of the historical 133 cases. There were no corrective
reruns or authoring changes. BM25, rewriting, generation and judge configurations
were omitted: this experiment isolates corpus competition in the baseline path.
No paid calls were made. C3 equals C2 and was omitted as redundant; other topics
and final combined-corpus interference remain later tasks.

## Coverage

| Condition / depth | Answerable document coverage | Complete pinned evidence | Feasible-only evidence | Macro fact recall | False-premise correction evidence |
| --- | --- | --- | --- | --- | --- |
| C1 / 3 | 25/38 | 2/38 | 2/27 | 11.84% | 1/4 (1/3 feasible) |
| C2 / 3 | 24/38 | 2/38 | 2/27 | 11.84% | 1/4 (1/3 feasible) |
| C1 / 8 | 31/38 | 4/38 | 4/38 | 19.74% | 2/4 |
| C2 / 8 | 31/38 | 3/38 | 3/38 | 17.11% | 2/4 |

The n=3 structural ceiling is 27/38 answerable cases and 3/4 correction cases.
At n=8 all 42 evidence-bearing cases fit. Full-set coverage retains infeasible
cases in its denominator; feasible-only coverage excludes them. Three absent-fact
cases ran but contribute to neither denominator. There were zero answer judgments.

| Category | Cases | C1 document / evidence, n=3 | C2 document / evidence, n=3 | C1 document / evidence, n=8 | C2 document / evidence, n=8 |
| --- | --- | --- | --- | --- | --- |
| Direct lookup | 14 | 9 / 2 | 9 / 2 | 11 / 3 | 11 / 2 |
| Same-document multi-hop | 9 | 7 / 0 | 7 / 0 | 9 / 0 | 9 / 0 |
| Related-document distractor | 7 | 7 / 0 | 7 / 0 | 7 / 1 | 7 / 1 |
| Cross-document synthesis | 8 | 2 / 0 | 1 / 0 | 4 / 0 | 4 / 0 |
| False premise | 4 | 4 / 1 | 4 / 1 | 4 / 2 | 4 / 2 |
| Absent fact | 3 | unscored | unscored | unscored | unscored |

Competitor ordering passes 6/7 in both conditions/depths. A competitor is actually
present in C1 for 1/7 at n=3 and 4/7 at n=8; C2 increases that to 2/7 and 5/7.
Ordering passes without a retrieved competitor are not demonstrations of rejection.
The category-ranking headline from `tools/evaluation/compare_evals.py` is therefore different from
pure document coverage: 24/38 → 23/38 at n=3 and 30/38 → 30/38 at n=8.

All released topic labels are cardiology. Clinical scope includes AF detection/
prediction/ablation and stroke, CCTA/STEMI risk discrimination, HFpEF biomarkers,
resistant hypertension, CKD/cardiorenal therapy and T2D–BP genetic overlap.
The passing pinned evidence at n=8 covers HFpEF biomarker changes (q056), ablation
procedure time (c005), CT-FFR diagnosis/prognosis (c014), plus Thai diagnostic checks
(c007) only in C1. Correction passes are TyG incremental discrimination (c018) and
spironolactone office-control conflict (c024). Multi-hop and synthesis have no
complete evidence passes. No evidence-completeness success should be claimed for
the uncovered AF prediction, genetic-overlap or synthesis scopes.

## Context review and failure analysis

Codex manually inspected saved contexts against gold for the cases below. This
is a focused author review, not exhaustive independent clinical adjudication of
all 45 cases and not a new semantic pass-rate estimate. Ranks below are zero-based.
Full contexts, scoped source identities and anchors remain in the run JSON.

| Case(s) | Observation and interpretation |
| --- | --- |
| q041, C1 n=8 | Review ranks 0 and 2 contain single/multiple ECG AUC 0.87/0.90 and documented paroxysmal AF history. The prose chunk starts midway through the pinned passage; exact evidence fails despite substantive answer content. This is a conservative-span miss, not a wrong gold value. |
| q044, C1 n=8 | Rashed STEMI chunks lead; Sun's abstract appears at rank 3, but the required stroke-review source is absent. A real incomplete synthesis and population/score-variant competition, not interchangeable AUC evidence. |
| q047, C1 n=8 | Rank 0 begins midway through the ROC-value list and contains combined AUC 0.936, but lacks the full variable-to-value mapping for plaque length 0.823. Right document does not establish both requested facts. |
| q053/q054/q058, C1 n=8 | Xu's required HFpEF source is absent. Geriatric HFpEF and other cardiorenal studies occupy the result set. These are scoped-source retrieval misses; their six-month biomarkers or general benefit statements cannot replace Xu's GLS, readmission or diabetes-interaction evidence. |
| q056, C1 n=8 | Xu ranks 0 and 3 include the biomarker passage/table: NT-proBNP −30.4% vs −9.7%, PIIINP −15.1% vs −5.8%, GDF-15 −20.5% vs −8.6%. This supports the positive pinned-evidence result. |
| c001, C1 n=8 | Retrieved Baj chunks include rounded abstract AUC 0.80 at 150,000 ECGs and discussion of five-year label constraints, alongside other studies' AUCs. The complete pinned 0.799 result/task passages are missed. Partial related content must not substitute another cohort's 0.90. |
| c006, C1 n=8 | Thai rank 0 contains 5.3%, 3.4% and the 33–37% pseudoresistance assumption. The anchor extends beyond the retrieved boundary. Substantive answer evidence exists despite the conservative exact-span miss. |
| c007, C1/C2 n=8 | C1 rank 3 contains the Thai four-part diagnostic work-up. C2 replaces that passage with Korean and other Thai material: Korean ranks 0/5 are topical but do not satisfy the question's Thai attribution. Thai source remains present; required diagnostic passage disappears. This explains evidence/fact recall 1 → 0. |
| c008, C1/C2 n=3 | C1 includes EMPEROR's white-coat/non-adherence limitation at rank 0 and Thai material. C2's three chunks are all Thai, including references and introductory material. Required EMPEROR source is lost, explaining document coverage pass → fail. C1 document pass itself does not imply complete synthesis evidence. |
| c017, C1 n=8 | Rank 0 establishes separate DELIVER and pooled PARAGLIDE/PARAGON data. Rank 5 starts the limitations but is cut before the full QALY qualification. Correction evidence is partial; cost-value prose and citations to other economic studies do not establish direct randomized comprehensive QALY comparison. |
| c018, C1 n=8 | Rank 1 explicitly reports 0.731 → 0.733, P=0.505 and no incremental benefit. Correction evidence is present; generated premise rejection was not tested. |
| c019, C1 n=8 | Rank 7 says no significant HFpEF class differences, indirect comparisons and lacking head-to-head evidence. Important correction content is retrieved, but the complete pinned methods/result sets are missed. No equivalence or randomized head-to-head superiority follows. |
| c020, C1 n=8 | Cameroon rank 0 identifies a four-week, 17-person trial. Related mortality discussions concern other studies, not five-year mortality in this cohort. No requested cohort-specific long-term result is established. |
| c021, C1 n=8 | TAILORED-AF chunks discuss 12-month single-/multiple-procedure endpoints; rank 2 explicitly uses 12-month sample-size assumptions. These cannot supply a five-year single-procedure result. |
| c022, C1 n=8 | Gao external-validation and limitation chunks concern its short-follow-up model. TyG rank 1 cites a different Framingham ten-year risk study. That is not externally validated ten-year hard-MACE risk for Gao's original cohort. |
| c024, C1 n=8 | Rank 6 preserves the abstract's universal below-130/80 claim; rank 2 contains one of nine at office 140/67 and a distinct home target. Both contradictory source locations are retrieved. The gold correctly retains the conflict; generated correction was not judged. |

No inspected case establishes a justified gold defect. Boundary misses and valid
alternate prose should be recorded as metric limits, not fixed by tuning anchors
to these outputs. No questions, evidence sets, retrieval settings or scorer were
changed. The two changed-score IDs c007/c008 would be the first targeted IDs for
an independently justified subsequent diagnostic experiment, selected from Thai/
EMPEROR dependencies and added Korean competition. Broader retrieval changes would
justify broader coverage; none were made here.

## Reproduction, verification and limits

From the repository root, with the already verified local PDFs/text and installed
virtual environment, use fresh collection directories and new receipt/output names:

```sh
SEED_ON_EMPTY=false OTEL_TRACES_EXPORTER=none PYTHONPATH=. \
 CHROMA_PATH=./chroma_db/<fresh-C1> .venv/bin/python \
 benchmark/cardiology/v1/runs/ingest_isolated.py --condition C1 --receipt <new-C1-receipt.json>
SEED_ON_EMPTY=false OTEL_TRACES_EXPORTER=none CHROMA_PATH=./chroma_db/<fresh-C1> \
 .venv/bin/python -m tools.evaluation.eval_golden --benchmark data/benchmark/sources/cardiology/v1 \
 --condition C1 --output <new-C1-vector.json>
# Repeat for C2 using a different fresh directory, condition and output names.
.venv/bin/python -m tools.evaluation.compare_evals <new-C1-vector.json> <new-C2-vector.json> --nested-corpus
```

The ingestion helper refuses existing paths and receipt overwrites. It uses the
production endpoint handler in-process, avoids HTTP port ownership, and makes no
LLM inference calls. The evaluation itself validates actual collection chunks
again. The current helper finalizes receipts atomically; the original run helper
used a plain write. Interrupted ingestion with the current helper leaves a setup
receipt and must use a fresh path;
it is not resumable. Physical PDFs, extracted corpus files, model caches and
Chroma stores are untracked. Only permitted evidence excerpts in results are
versioned, with article attribution retained in [ATTRIBUTION.md](ATTRIBUTION.md).

Verification: selected-corpus verifier passed all 21 records; 147 offline tests
passed; both runs completed 45/45 requested IDs and both depths; nested comparison
accepted matching provenance and common article tuples. Saved summaries were
checked against results; ingestion/evaluation model fingerprints matched. No API
service, production collection, downloaded PDF or historical result was modified.

This is one execution per condition, not a variance or latency study. Model-file
hashes and ingestion receipts establish the model used to create these fresh
collections, but the runner does not rederive every stored embedding. Exact-span
coverage is conservative and differs from semantic sufficiency. Negative cases
cannot be scored as successful refusals without generated answers; author review
cannot certify all-corpus absence independently. Paid rewriting/generation/judge
runs need separate purpose/provider/scale/cost approval. Historical 96.4%/98.2%
remain original full-corpus metrics and are not comparable to this rebuilt gold.

Post-review verification: 151 offline regressions passed, including four new
ingestion-helper tests. The four tests also passed under `python -O`; a simulated
atomic-replace failure preserved the setup receipt and removed the temporary file.
Artifact hashes and the byte-identical original receipts/results/helper snapshot
were verified. No retrieval or paid evaluation was repeated for these changes.
