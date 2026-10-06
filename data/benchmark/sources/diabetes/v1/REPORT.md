# Diabetes evaluation and frozen cardiology interference

**Diabetes coverage is unchanged after corpus expansion; cardiology q051 loses its expected document at both depths.** These are retrieval results, not answer-correctness or clinical-quality claims. These historical retrieval results have not been independently clinically certified.

## Selection, audit and run boundaries

All 35 legacy diabetes-dependent cases and six sources were reviewed. The [audit](AUDIT.md) records full original cases, factual/category issues and final dispositions. Twenty-three IDs are revised, twelve retired, and twenty-six new cases added. Raman CC BY 2.0 and the restrictive/territorial GWAS are excluded; the replacement papers do not inherit their gold.

The selection is 16 diabetes/overlap articles, including five already-selected cardiology sources, within 32 combined articles. All eleven additions passed pinned PMC Cloud PDF/XML, PubMed/converter identity, exact CC BY 4.0/CC0 1.0, readable-page and notice/credit checks. Thirty-two selection pages and twelve additional gold pages were rendered and inspected. Full metadata/abstracts and attribution are committed; PDFs/XML/text/renders are local and untracked. Original corpus/query files and the cardiology release remain unchanged.

Fresh task-owned collections contain 1,119 chunks (diabetes C2), 1,270 (21-article cardiology regression C1), and 2,074 (combined corpus). Production ingestion/chunking and exact source/text multiplicities were verified, with seeding disabled and no HTTP server. Embedding and reranker file fingerprints match every ingestion/evaluation pair; the combined store serves both enlarged-corpus evaluations.

Four original full retrieval runs executed all requested IDs at n=3/n=8: 49/49 diabetes cases per corpus and 45/45 frozen cardiology cases per corpus, **376 local retrieval calls**, zero missing IDs. Broad article expansion and complete final benchmark/interference claims justify this coverage; no iterative retrieval reruns or configuration sweep occurred. BM25, rewriting, generation and judges were omitted; no paid calls were made. C1=C2 diabetes and C2=C3 cardio conditions were not redundantly run.

The [dependency map](case_dependencies.json) governed the [focused saved-context review](runs/focused_context_review.json): q001/q019/q036/q039, d003/d005/d006/d007/d010/d011/d025/d019/d023 plus frozen q051. Each context set explicitly names its parent file, run ID, hash, condition and depth: diabetes cases use the original combined C3 run and q051 uses the original enlarged cardiology C2 run. This is a manual review subset, not a separately executed retrieval run or full-suite percentage.

After the initial retrieval freeze, source/standards review corrected q036/d014/d015/d016 from lookup to multi-hop and clarified q005/d018 reference scope. Questions, anchors, sources and evidence bindings did not change. Original authoring envelopes and runs are preserved. [Offline rescoring](runs/rescore_saved.py) checked invariance and identical per-case metrics, recorded parent/helper hashes, and made zero retrieval calls. Final [C2](runs/diabetes-C2-reviewed.json)/[C3](runs/diabetes-C3-reviewed.json) files are explicit derived artifacts. No observed retrieval failure drove gold-anchor changes. Subsequent Claude review corrected descriptive metadata and per-case freeze wording; [review_corrections.json](review_corrections.json) records the before/after fingerprints. The evaluated release is preserved in [runs/evaluated-release/](runs/evaluated-release/). All original retrieval, derived-score and ingestion files remain byte-identical: the original diabetes vector query/condition envelope is in `runs/initial-authoring/`, while reviewed diabetes and cardiology envelopes are in `runs/evaluated-release/`, which also preserves their shared manifest. They are not relabelled as runs of the current descriptive revision. Questions, anchors, source bytes, memberships and evidence bindings are unchanged, and no new retrieval was run.

The cardio comparison uses identical original 45 questions/77 anchors inside one extended selection envelope. A fresh 21-article baseline makes fingerprints compatible; historical the isolated cardiology evaluation output is not relabelled. Both [diabetes](runs/diabetes-comparison.txt) and [cardiology](runs/cardio-comparison.txt) nested comparisons passed the provenance/configuration guards.

## Coverage

| Topic / corpus / depth | Answerable documents | Complete pinned evidence | Feasible-only evidence | Macro fact recall | False-premise correction evidence |
| --- | --- | --- | --- | --- | --- |
| Diabetes / 16 / 3 | 40/42 | 8/42 | 8/35 | 20.24% | 0/3 |
| Diabetes / 16 / 8 | 41/42 | 14/42 | 14/42 | 38.10% | 1/3 |
| Diabetes / 32 / 3 | 40/42 | 8/42 | 8/35 | 20.24% | 0/3 |
| Diabetes / 32 / 8 | 41/42 | 14/42 | 14/42 | 38.10% | 1/3 |
| Cardio / 21 / 3 | 24/38 | 2/38 | 2/27 | 11.84% | 1/4 |
| Cardio / 21 / 8 | 31/38 | 3/38 | 3/38 | 17.11% | 2/4 |
| Cardio / 32 / 3 | 23/38 | 2/38 | 2/27 | 11.84% | 1/4 |
| Cardio / 32 / 8 | 30/38 | 3/38 | 3/38 | 17.11% | 2/4 |

Diabetes has 42 answerable, 3 false-premise and 4 absent-fact cases. At n3 the answerable structural ceiling is 35/42; q004/q039/d009/d010/d012/d013/d016 need more than three chunks. All 45 evidence-bearing cases fit at n8. Cardiology retains its 27/38 n3 answerable ceiling and 3/4 correction ceiling; all 42 evidence-bearing cases fit at n8. Infeasible cases remain in full-set denominators.

| Diabetes category | Cases | Documents / evidence, n3 | Documents / evidence, n8 |
| --- | --- | --- | --- |
| direct_lookup | 23 | 22 / 7 | 23 / 11 |
| multi_hop | 10 | 10 / 0 | 10 / 1 |
| cross_doc_distractor | 4 | 4 / 1 | 4 / 2 |
| cross_doc_synthesis | 5 | 4 / 0 | 4 / 0 |
| false_premise | 3 | 2 / 0 | 3 / 1 |
| absent_fact | 4 | unscored | unscored |

Both diabetes corpus sizes have identical per-case document/evidence/fact/ordering verdicts, not merely equal totals. Retrieved lists nevertheless change for five case-depths: d002 at n3/n8 changes chunks within the same source; q030, d005 and d014 at n8 gain AF/stroke, TyG/CCTA and Korean resistant-hypertension source text respectively. [Saved-list changes](runs/retrieval_list_changes.json) record these differences separately from verdict changes; unchanged scores do not imply unchanged contexts. Four distractor cases pass ordering at both depths, but their named decoys appear in **0/4**: this does not demonstrate successful rejection of retrieved competitors. Related competition exists in the selected corpus; these queries did not expose it in the returned depths.

| Diabetes primary scope | Cases | Answerable documents, n8 | Complete answerable evidence, n8 |
| --- | --- | --- | --- |
| Pharmacotherapy | 11 | 7/8 | 3/8 |
| Epidemiology/metabolic syndrome | 3 | 3/3 | 1/3 |
| Nephropathy/zinc/hypoxia | 10 | 9/9 | 3/9 |
| Genetics/sex/drug adverse response | 6 | 6/6 | 3/6 |
| Management/CGM | 9 | 6/6 | 1/6 |
| Sleep/cardiometabolic | 7 | 7/7 | 3/7 |
| SGLT2/cardiorenal/BP overlap | 3 | 3/3 | 0/3 |

Scopes are mutually exclusive reporting groups only; source/case dependencies retain clinical overlap. Absent facts and false premises are excluded from the answerable columns. No genuine cross-document synthesis achieves complete pinned evidence. The sole n8 multi-hop evidence pass is d003 (source count discrepancy).

## Focused evidence and interference review

- **q001:** Right source throughout, but pinned Abstract outcome boundary is missing. Retrieved Results distinguish primary HbA1c/secondary FPG/2hPG; this is not proof that semantically sufficient evidence is absent.
- **q019:** Rank 0 supplies ZnT7 knockdown/EMT and MAPK/ERK/TGF-beta, renal ZnT8/TGF-beta and beginning of TNF-induced protein-3 sentence. Neighboring end of the body NF-kappaB statement is not fully retrieved; bibliography is not a substitute for the complete experimental claim.
- **q036:** Ranks 0 and 4 expose the named embedding model, 500/100 characters, FAISS/top_k=2 and L2 distance. The full pinned architecture span is not present. Manual context inspection finds the requested configuration even though conservative span scoring fails.
- **q039:** Source masking vocabulary is retrieved, but the 697/864 versus 697/797 identification denominators and practical-blinding limitation are not supplied completely. Source presence does not establish this distinction.
- **d003:** Both abstract three-male and Results two-male counts are retrieved at n8. The full evidence set passes; preserve the discrepancy rather than reconcile it.
- **d005:** Rank 0 includes Table 4 OR .102, CI .08-3.08 and P=.021/.031. Full evidence passes. This printed anomaly is evidence for source attribution, not a valid coherent risk estimate.
- **d006:** Correct semaglutide source, but prominent contexts summarize non-inferiority rather than supply the precise prespecified upper-CI rule and adjusted result. Neither pinned fact is complete.
- **d007:** Rank 1 contains the requested three-month and six-month ITT HbA1c estimates/CIs/P values in the body Results. The chosen Abstract anchor is not fully present: a clear example of semantically useful alternative location with a pinned-span miss. Gold is not expanded after observing this.
- **d010:** Both articles appear, but Guo quality contrast and Berthoumieux time-in-range/late HbA1c conjunction are incomplete. Broad intervention/vignette vocabulary alone cannot complete the cross-article synthesis.
- **d011:** Both source filenames appear, but Jan hits are largely bibliography and Dabbs-Brown title/notice hits do not bind the UK Biobank population. Document-set success is not evidence success.
- **d025:** Qin dominates retrieved contexts, with mechanistic fibrosis and zinc/HIF text. Neither accepted whole review anchor is complete. Alternative-source eligibility prevents demanding both reviews; it does not make source presence alone sufficient.
- **d019:** At n8 the two-trial/196-person primary result and nonsignificant HbA1c finding provide complete corrective evidence. This is not a judged generated correction.
- **d023:** Related DSMES trial contexts report six-month follow-up, not the requested twelve-month result. Retrieval is expected; no generated refusal was judged.

**Frozen cardiology q051** asks for Gao CCTA derivation sample-size statements and its events-per-variable discussion. The 21-article run contains the expected CCTA document at n3/n8. With eleven diabetes additions, AF calibration moves from rank 1 to rank 0, GQD review extraction methods appears rank 1, and Buea hospital sampling appears rank 2; Guo methodological text also appears at n8. The expected CCTA document is absent at both depths. These returned method/sample-size passages are not alternative evidence for Gao. The baseline document pass includes CCTA front-matter/citation chunks, not complete sample-size evidence. Saved outputs establish the returned-list displacement but do not record pre-rerank candidates, so its mechanism is unconfirmed; embedding-stage candidate-pool displacement is a plausible explanation, not a measured result.

Cardiology document coverage falls 24/38 → 23/38 at n3 and 31/38 → 30/38 at n8. Complete evidence stays 2/38 and 3/38 because q051 already lacked the full gold set in the baseline. Its evidence invariance must not hide the new document regression. All other frozen document/evidence/fact/ordering verdicts remain unchanged. Cardiology distractor ordering remains 6/7 with named decoys present in 2/7 at n3 and 5/7 at n8. [Per-ID changes](runs/interference_changes.json) preserve the exact before/after sources.

## Verification and limits

`verify_cardiology_selection.py` passed for all 32 articles, including archived metadata/XML, PDF/text hashes, offsets, attribution, nested conditions and preserved baseline files. The production-chunk reachability oracle reached all 55 diabetes anchors and all 45 evidence-bearing cases with unlimited budget; finite-depth ceilings remain explicit. All 151 repository offline tests passed. Rescore guard checks accepted annotation-only corrections and rejected changed questions, anchors, fact bindings and incomplete parents. Artifact checksums are recorded in [runs/artifacts.json](runs/artifacts.json).

Pinned whole-span scoring is conservative: q036 and d007 demonstrate useful requested evidence at alternative/incomplete pinned locations. These manual observations do not overwrite automated scores or prove generated-answer correctness. Numeric source conflicts remain as printed. Negative cases were source-reviewed across the selected main PDFs; no generated refusal or correction was judged. Author review is not independent clinical adjudication. This is one local retrieval configuration and one combined cardiology/diabetes snapshot; it does not establish final oncology/outlier interference or Docker demo quality. No further gold tuning or retrieval rerun was performed.
