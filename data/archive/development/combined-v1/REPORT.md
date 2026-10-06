# Combined four-topic retrieval evaluation

**The 51-article corpus preserves most document-level scores but exposes several source and passage losses.** Complete pinned evidence at n=8 is 32/120 answerable cases; generated answers and refusals were not evaluated. This is one vector-only snapshot, not a stability study or a comparison of retrieval flags.

## Frozen scope and reproducibility

The 51 unique articles yield 3,350 production chunks: 21 cardiology, 11 additional diabetes, 14 oncology and five outliers. All 50 CC BY 4.0 and one CC0 sources retain their exact PMC versions, PDF/text hashes, eligibility and attribution records. The four prepared ALS/FTD articles and ten unfrozen cases are excluded pending independent review/freeze. This report completes the original four-topic retrieval comparison; it does not cover the full 55-article local inventory.

[Pre-run review](PRE_RUN_REVIEW.md) records integrated validity checks, dependency-based scope selection and omissions. The four envelopes preserve 148 full original query objects and anchors: 120 answerable, 17 false-premise and 11 absent-fact cases. Diabetes uses its preserved final evaluated snapshot, before descriptive annotations. No semantic query, gold, alternative or scorer change followed integrated retrieval. Negative questions keep their explicit original paper/topic scope; x009 asks only about five outliers, not universal absence in 51 articles.

All 148 IDs executed once at n=3 and n=8 (296 local retrieval calls), zero missing IDs. Complete final topic claims and broad corpus expansion justify full declared coverage; no successful query was rerun during iteration. The original 18-case outlier regression sample is retained as a slice of these complete outputs: 15/17 document coverage at both depths, 4/17 evidence at n=3 and 6/17 at n=8, one unscored absent-fact case. Its envelope differs from historical focused runs, so this slice is not presented as a directly compatible 46-to-51 comparison.

Production `main.ingest`, `embed`, `chunk_text` and `retrieve()` were used, with `SEED_ON_EMPTY=false`, reranking, BM25 off and rewriting off. The isolated store source/text multiset equals production chunks exactly. Ingestion and all four runs match model file fingerprints; all nested comparisons pass `check_compatible`. Production retrieval/reranker threading was unchanged. No HTTP server, shared collection or paid call was started.

Compatible saved baselines are explicit derived comparison artifacts, not new retrieval executions. [The derivation helper](../derive_baseline.py) rejects incomplete/duplicate IDs, revised per-query hashes, altered source tuples, changed scorer/feasibility, fabricated chunks and inconsistent metrics. It records the unchanged original timestamp/commit, parent path/hash/run ID/provenance and zero retrieval calls. This avoids 386 repeated baseline calls (two 45-case cardio conditions plus 49 diabetes, 44 oncology and ten outlier cases, at both depths). Raw parents remain unchanged in their topic releases.

## Topic and nested-corpus results

The cells below are answerable document/evidence counts; false-premise correction evidence is separate. Fractions retain structurally infeasible cases in their full-set denominator.

| Topic / corpus | n=3 documents | n=3 evidence | n=8 documents | n=8 evidence |
| --- | --- | --- | --- | --- |
| cardiology / 21 | 24/38 | 2/38 | 31/38 | 3/38 |
| cardiology / 51 | 24/38 | 2/38 | 30/38 | 3/38 |
| diabetes / 16 | 40/42 | 8/42 | 41/42 | 14/42 |
| diabetes / 51 | 40/42 | 8/42 | 41/42 | 13/42 |
| oncology / 14 | 31/34 | 7/34 | 32/34 | 15/34 |
| oncology / 51 | 30/34 | 7/34 | 31/34 | 14/34 |
| outliers / 5 | 6/6 | 2/6 | 6/6 | 2/6 |
| outliers / 51 | 6/6 | 2/6 | 6/6 | 2/6 |

Cardiology source-only C1 has 19 articles / 1,113 chunks; C2 has 21 / 1,270. On the same frozen cases, C1 document/evidence counts are 25/38 and 2/38 at n=3, 31/38 and 4/38 at n=8. C3 has 24/38 and 2/38 at n=3, 30/38 and 3/38 at n=8. C1-to-C3 and C2-to-C3 both pass nested compatibility. The additional c007 evidence loss and c008 n3 document loss relative to C1 already occurred in the related-cardio C2 baseline.

| Topic | Feasible-only answerable evidence n3 | Macro fact recall n3 / n8 | Correction evidence n3 / n8 | Absent cases (unscored) |
| --- | --- | --- | --- | --- |
| cardiology | 2/27 | 11.84% / 17.11% | 1/4 / 2/4 | 3 |
| diabetes | 8/35 | 20.24% / 35.71% | 0/3 / 1/3 | 4 |
| oncology | 7/28 | 23.53% / 44.12% | 0/7 / 3/7 | 3 |
| outliers | 2/5 | 33.33% / 33.33% | 0/3 / 0/3 | 1 |

All evidence-bearing cases are structurally feasible at n8, so full-set and feasible-only denominators agree there. At n3, 25/120 answerable cases are infeasible; correction evidence additionally excludes three infeasible cases from feasible-only denominators (one cardio, two oncology). [analysis.json](analysis.json) supplies per-ID eligibility and minimum-chunk reporting groups. The n8 evidence-bearing groups requiring four or more chunks achieve 3/28 complete sets (all three in oncology); lower-budget groups achieve 35/109. These groups include false-premise correction evidence and are not answer-accuracy strata.

## Category coverage

Each cell is document passes / exact-evidence passes, with the category denominator shown separately. False-premise evidence tests source correction support; absent facts remain unscored.

| Topic / category | Cases | n3 document / evidence | n8 document / evidence |
| --- | --- | --- | --- |
| cardiology / cross_doc_distractor | 7 | 7 / 0 | 7 / 1 |
| cardiology / cross_doc_synthesis | 8 | 2 / 0 | 4 / 0 |
| cardiology / direct_lookup | 14 | 9 / 2 | 11 / 2 |
| cardiology / false_premise | 4 | 4 / 1 | 4 / 2 |
| cardiology / multi_hop | 9 | 6 / 0 | 8 / 0 |
| cardiology / absent_fact | 3 | unscored | unscored |
| diabetes / cross_doc_distractor | 4 | 4 / 1 | 4 / 2 |
| diabetes / cross_doc_synthesis | 5 | 4 / 0 | 4 / 0 |
| diabetes / direct_lookup | 23 | 22 / 7 | 23 / 10 |
| diabetes / false_premise | 3 | 2 / 0 | 3 / 1 |
| diabetes / multi_hop | 10 | 10 / 0 | 10 / 1 |
| diabetes / absent_fact | 4 | unscored | unscored |
| oncology / cross_doc_distractor | 2 | 2 / 0 | 2 / 1 |
| oncology / cross_doc_synthesis | 3 | 0 / 0 | 1 / 0 |
| oncology / direct_lookup | 21 | 21 / 7 | 21 / 11 |
| oncology / false_premise | 7 | 6 / 0 | 6 / 3 |
| oncology / multi_hop | 8 | 7 / 0 | 7 / 2 |
| oncology / absent_fact | 3 | unscored | unscored |
| outliers / cross_doc_distractor | 1 | 1 / 1 | 1 / 1 |
| outliers / direct_lookup | 4 | 4 / 1 | 4 / 1 |
| outliers / false_premise | 3 | 2 / 0 | 3 / 0 |
| outliers / multi_hop | 1 | 1 / 0 | 1 / 0 |
| outliers / absent_fact | 1 | unscored | unscored |

## Unique source/passage coverage and competition

A unique accepted source or anchor counts as seen only when returned/matched for at least one case that uses it. The unions include complete alternative sets; they do not require every optional alternative for each answer. They are inventory breadth diagnostics, not a substitute for per-case completeness. Unused/named-decoy-only anchors are excluded.

| Topic | Accepted source union, n3 / n8 | Accepted anchor union, n3 / n8 | Named-decoy ordering n3 / n8 | Named decoy present n3 / n8 |
| --- | --- | --- | --- | --- |
| cardiology | 18/19 / 18/19 | 15/74 / 19/74 | 6/7 / 6/7 | 2/7 / 5/7 |
| diabetes | 16/16 / 16/16 | 11/51 / 19/51 | 4/4 / 4/4 | 0/4 / 0/4 |
| oncology | 13/13 / 13/13 | 14/80 / 30/80 | 2/2 / 2/2 | 0/2 / 0/2 |
| outliers | 5/5 / 5/5 | 4/12 / 5/12 | 1/1 / 1/1 | 0/1 / 1/1 |

Named-decoy ordering is unchanged versus each topic baseline. Passing cases without a returned decoy do not demonstrate distractor rejection. No outlier-source chunk appears in any finalized cardiology, diabetes or oncology context at either depth (zero exposures across 276 case-depth executions). This cannot establish resistance when outliers rank below the cutoff. The reverse exposure occurs: x008 returns AF AI material at n3/n8 and CGM AI material at n8; x001 returns a diabetes genetics source at n8. Related cross-topic source exposure, complete missed-source/anchor lists and per-query metric changes are in [analysis.json](analysis.json).

Context lists change in 17/90 cardiology, 7/98 diabetes, 9/88 oncology and 6/20 outlier case-depth pairs compared with their topic baselines. Most changes leave the scored metrics unchanged. No pre-rerank candidate trace is available: candidate-pool displacement is a hypothesis, not a measured mechanism.

## Saved-context review and failure taxonomy

The following Codex review checks the immutable C3 outputs and their derived baselines against source-bound gold. Ranks are zero-based. It neither changes automated verdicts nor assigns a semantic sufficiency pass rate.

| Case / taxonomy | Observed evidence and interpretation |
| --- | --- |
| q051: required-source loss | Gao CCTA disappears at both depths. n3 now returns AF sample-size text, Buea diabetes sample-size calculation and TAILORED-AF power calculations. n8 additionally returns GQD/CGM methods and oncology observational material. These cannot supply Gao's sample-size/EPV facts. Baseline source presence already lacked complete evidence. |
| c004: document gain without evidence completion | Both primary TAILORED-AF and AF-review sources now fit n3. The review at rank 2 is introductory ABC/AF management, rather than the pinned primary-success comparison. Document improvement does not establish the requested synthesis. |
| c007/c008: related competition | c007 still lacks the Thai diagnostic passage; Korean/Thai material is present. c008 still loses EMPEROR at n3 and returns it at n8. These losses predate other-topic additions and must not be newly attributed to them. |
| q006: passage loss within the right source | The baseline returned the GQD all-trials-high-risk and S1–S3 random-number-table passage plus its adjacent concealment chunk. C3 loses the first chunk while keeping the concealment continuation at rank 3 and generic high-risk/GRADE material. Another GQD PRISMA/outcome-bias chunk enters at rank 7. No new-topic source enters this returned n8 set; the upstream mechanism is unmeasured. |
| o029: cross-topic method confusion | Hunan disappears at both depths. n8 is dominated by CKD propensity-matching limitations, GQD significance/heterogeneity prose and HFpEF propensity tables. Generic PSM/statistical wording cannot replace Hunan's DFS/OS values, conflicting weighted/PSM labels or follow-up limitation. |
| o004: conservative whole-span loss | n8 retains Table 6 (23 new troponin rises / 11 myocarditis), ESC monitoring/diagnostic criteria at rank 2 and Discussion myocarditis 14.7% / no serious cardiac AEs at rank 4. The complete accepted primary/table spans are not retrieved. Substantive requested evidence remains distributed across returned passages; an exact-span loss is not proof of a wrong generated answer. |
| x006: pinned correction loss with useful alternative prose retained | The explicit absence-of-independent-validation paragraph disappears at n3/n8. Rank 0 still says ADNI/OASIS-3 external validation is an essential next step and distinguishes OASIS-derived training data. This supports caution/premise rejection, but is not the frozen complete anchor; no gold relaxation or judged rejection is claimed. |
| q056, c014, c024, d003, o013, x004: positive controls | Full pinned evidence survives for HFpEF biomarker changes, CT-FFR diagnosis/prognosis, the spironolactone source conflict, genetic abstract/Results count conflict, immune-exclusion qualification and WWTP abundance normalization respectively. These successes do not extend to the uncovered evidence families. |
| absent/false-premise cases: separate correctness gap | Relevant source retrieval does not establish correct refusal or correction. Negative/positive source scope was reviewed before the run; no generated answer was produced or judged. |

The change review identifies true scoped-source losses, pinned-passage losses, conservative-span failures, document gains without complete evidence, incomplete synthesis and untested answer/refusal behavior separately. No observed failure justified tuning gold or changing retrieval. Representative review covers every new metric-change ID and controls; it is not independent scientific adjudication of every answer.

## Unresolved work and claims

The later [five-topic evaluation](../v2/REPORT.md) completed ALS/FTD integration.
The historical plan was to: independently review/freeze a001–a010, review cross-topic alternatives/negative scope across 55 articles, then use the 20 x/a cases and original 18-topic sample plus justified controls for iteration; complete declared coverage is needed for final 55-article claims. This report does not certify that extension.

Required-source losses q051/o029 and passage losses q006/o004/x006 remain diagnostic follow-ups tracked in this report and the combined evaluation. Target those IDs and dependency/control families first for a justified later retrieval experiment. Global retriever/scorer changes would justify broader runs. No additional issue or scope expansion is silently created.

Answer-judge work remains separately sequenced in the separate generated-answer evaluation follow-up. There are zero generated answers, zero judged refusals and zero judged premise corrections; no answer/refusal accuracy is reported. Any rewriting/generation/judge run needs explicit purpose/provider/scale/cost approval. BM25 and rewriting comparisons are not part of this corpus-only baseline and remain unmeasured on this combined release. Public PDF delivery and domain-expert certification remain outside this report.

All 213 offline regressions pass, including seven new saved-evidence corruption tests. Historical 96.4%/98.2% metrics remain original 19-document/133-query results; this rebuilt benchmark measures different gold and evidence sufficiency and does not support those claims or Docker-demo quality.
