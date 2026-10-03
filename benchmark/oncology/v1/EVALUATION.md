# Oncology retrieval baseline and topic regression — JUA-112

**Adding the POL-MOL competition article changes some returned passages but no scored oncology outcomes.** At n=8, vector retrieval finds the expected documents for 32/34 answerable cases and complete pinned evidence for 15/34. These are retrieval measurements, not answer-correctness or clinical-quality claims.

The reviewed PR #33 merge (`17dd21b`) is the fixed authoring boundary. [runs/freeze.json](runs/freeze.json) records the exact source/query/scorer/adapter hashes and initial selection rationale. No source, question, reference, anchor, alternative, category, scorer or retrieval implementation was changed after retrieval began. C3 and final combined-corpus negative review remain JUA-114 work.

Fresh task-owned stores contain 771 chunks for C1's 13 answer-source articles and 853 for C2's 14 articles. Production `main.ingest`, `main.embed`, `main.chunk_text` and `retrieve()` were used, with seeding disabled and no HTTP server. [Ingestion receipts](runs/C1-ingestion.json) and [C2 receipt](runs/C2-ingestion.json) record exact membership, source/chunk counts and loaded model file fingerprints. Ingestion and evaluation fingerprints match. No shared collection was changed.

The initial 14 IDs were o001/o002/o003/o006/o009/o013/o017/o021/o024/o025/o029/o030/q098/q100: treatment response/survival and count conflicts, TNBC, dose conflict, cardiovascular scope/synthesis, immune exclusion, biomarker/MRD contrast, Hunan synthesis, screening correction and an absent-fact control. The remaining 30 IDs were then executed once per condition to obtain complete baseline coverage; successful IDs were not rerun. All 44 IDs execute at n=3 and n=8 in both conditions: 176 local retrieval calls, zero missing IDs. BM25, rewriting, generation and judges were omitted. No paid calls occurred.

The immutable focused/remaining parent files preserve raw ranked contexts and results. [C1 complete](runs/C1-complete.json) and [C2 complete](runs/C2-complete.json) assemble those disjoint subsets without further retrieval; parent hashes and run IDs are recorded. `PYTHONPATH=. .venv/bin/python benchmark/oncology/v1/runs/assemble_runs.py` reproduces or verifies these assemblies. [The nested comparison](runs/C1-C2-comparison.txt) passes the existing compatibility guards.

| Condition / depth | Answerable documents | Complete answerable evidence | Feasible-only evidence | Macro fact recall | False-premise correction evidence |
| --- | --- | --- | --- | --- | --- |
| C1 / 3 | 31/34 | 7/34 | 7/28 | 23.53% | 0/7 |
| C2 / 3 | 31/34 | 7/34 | 7/28 | 23.53% | 0/7 |
| C1 / 8 | 32/34 | 15/34 | 15/34 | 45.59% | 3/7 |
| C2 / 8 | 32/34 | 15/34 | 15/34 | 45.59% | 3/7 |

At n3, six answerable cases and two false-premise cases need more than three chunks: o016/o017/o018/o029/o030/q099 and o013/q081 respectively. All 41 evidence-bearing cases fit at n8. Infeasible cases stay in full-set denominators. Three absent-fact cases are unscored; no refusal or generated premise-correction answer was judged.

Document, complete-evidence, fact-recall and distractor-ordering outcomes are identical per case/depth across C1/C2. Ranked context lists change in 12/88 case-depth pairs, covering seven IDs. Thus unchanged scores do not mean unchanged retrieval. The two named distractors are never returned at either depth: ordering passes do not demonstrate rejecting a retrieved competitor.

[Saved-context review](runs/saved_context_review.json) records seven focused n8 checks against the C2 parent artifact. o017 returns only the mortality cohort and misses the observational source. o030 misses the required Gosney consensus; POL-MOL remains partial support. o009 retrieves the abstract estimates but misses the pinned four-study limitations passage. o024 retrieves the OS values and adjuvant/resected context but fails the full pinned-span requirement: exact coverage is conservative and is not proof that every semantically sufficient answer passage is absent. o013, o025 and corrected q098 pass pinned coverage at n8. No observed failure was used to weaken gold or move anchors.

The topic regression compares the existing 32-article cardiology/diabetes corpus with that same corpus plus the 14 reviewed oncology articles (46 total), in fresh stores of 2,074 and 2,927 chunks. The [regression envelopes](runs/topic-regression/README.md) preserve original questions/anchors and exact common article bytes. The original topic releases and prior outputs remain untouched.

The initial cardiology IDs q051/q054/c012/c016 cover a previously vulnerable CCTA case, HFpEF, renal/infection endpoints and cardiometabolic genetic interpretation. All four already fail document coverage at baseline, so q056 (SGLT2 biomarkers) and q067 (no-reflow incidence) were added as previously passing controls, without rerunning the initial cases. Diabetes q030/d012/d016 cover cardiovascular risk, renal/therapy synthesis and cardiorenal drug-class interpretation; d022 is an unscored absent-fact mortality control. Ten unique IDs in each corpus, both depths: 40 local retrieval calls. This is a focused regression sample, not full-topic coverage.

| Regression sample / depth | Baseline documents / evidence | Expanded documents / evidence |
| --- | --- | --- |
| Cardiology, 6 answerable / 3 | 1/6 / 1/6 | 1/6 / 1/6 |
| Cardiology, 6 answerable / 8 | 2/6 / 1/6 | 2/6 / 1/6 |
| Diabetes, 3 answerable / 3 | 3/3 / 0/3 | 3/3 / 0/3 |
| Diabetes, 3 answerable / 8 | 3/3 / 1/3 | 3/3 / 1/3 |

No scored outcome changes in this sample. q051's returned lists change at both depths; other sampled lists stay identical. Existing baseline failures limit the sensitivity of the sample. d022 remains unscored, so it establishes no refusal or negative-answer correctness. The three saved nested comparisons pass compatibility checks.

Across oncology and regressions, 216 local retrieval calls were made. All 206 offline tests and release verification pass. The next decision is whether to investigate the documented retrieval failures; this report makes no claim that vector retrieval now supplies complete answers reliably. Further configuration changes should be evaluated separately against this fixed baseline. Paid runs still require explicit approval.
