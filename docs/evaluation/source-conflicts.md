# Source conflicts and competing evidence: query-by-query report

Updated 5 October 2026. This report is intended to remain in `docs/evaluation/` after the corpus/evaluation epic is merged to main. It contains the questions, article identities, competing claims, grading treatment and measured retrieval results directly; reading it does not require local corpus PDFs, temporary workspaces or retained run JSON files.

Conflicting resources do not always reach opposite scientific conclusions. This inventory distinguishes incompatible printed values or labels, unresolved statistical/provenance anomalies, and apparent disagreements explained by analysis scope. It summarizes source-grounded model review; it does not determine which biomedical claim is scientifically true.

## Scope and retained evidence

- Gold correction record: [57b23ff](https://github.com/juan-casimiro/ai-research-assistant/commit/57b23ffc2812b2a4bc346d39571c312f3e7fc2c2) on PR 46. This includes Claude’s follow-up commits 4d19bdc and 57b23ff.
- Historical retrieval snapshot: [bc0594e](https://github.com/juan-casimiro/ai-research-assistant/commit/bc0594e6c845116e4203a9467eb27f23c57ab621), the four-topic 51-article, 148-query combined run. Vector retrieval, production reranker, BM25 off, rewriting off; n3/n8 mean returned chunk depths.
- The report covers the conflict-bearing queries identified through the active gold and retained source-review notes, plus selected scope controls. It is not an exhaustive re-reading of every article or a clinical certification.
- Source locations below are physical PDF pages from pinned version-1 article anchors, with readable section/table names. Public article links and DOI identifiers identify the resources even if benchmark files are omitted from main. No PDFs are redistributed.
- Document coverage means accepted source articles were returned. Complete evidence means all required pinned passages of an accepted set matched. An exact-span failure can coexist with useful partial prose; neither metric judges generated answers.
- No generated answers, refusals or conflict explanations were judged in these runs. There is no measured conflict-resolution answer accuracy.
- Verified corrected-gold retrieval snapshot: 55 articles / 3,638 chunks, all 158 queries at n3/n8, vector retrieval with production reranking, BM25 and rewriting off. The [retained summary and fingerprints](combined-benchmark-v2.json) pin every topic run, query set, scorer and retrieval configuration. New results below supersede the uncommitted targeted observations; they do not certify those earlier observations. Historical and current results are not directly compatible.

## Inventory

| Query | Issue | Current category | Historical complete evidence n3 / n8 | Corrected 55-article evidence n3 / n8 |
| --- | --- | --- | --- | --- |
| [c004](#c004) | Cross-article numerical disagreement | `cross_doc_synthesis` | fail / fail | fail / fail |
| [q051](#q051) | Within-article sample-size inconsistency | `multi_hop` | fail / fail | fail / fail |
| [c012](#c012) | Within-article adjusted-estimate and design-label conflicts | `source_conflict` | fail / fail | fail / fail |
| [c013](#c013) | Within-article price-provenance discrepancy | `source_conflict` | fail / fail | fail / pass |
| [c024](#c024) | Within-article universal-control claim and target conflict | `false_premise` | fail / pass | fail / pass |
| [d003](#d003) | Within-article interaction-count discrepancy | `multi_hop` | fail / pass | fail / pass |
| [d005](#d005) | Within-table statistical reporting anomaly | `direct_lookup` | pass / pass | pass / pass |
| [x001](#x001) | Within-article significance-language conflict | `multi_hop` | fail / fail | fail / fail |
| [x005](#x005) | Within-article model-task conflict | `source_conflict` | fail / fail | fail / fail |
| [o002](#o002) | Within-article pathological-response count conflict | `multi_hop` | fail / fail | fail / fail |
| [o006](#o006) | Within-article reversed dose assignment | `multi_hop` | fail / fail | fail / fail |
| [o029](#o029) | Within-article analysis-label conflict | `multi_hop` | fail / fail | fail / fail |
| [q102](#q102) | Within-article flow-diagram arithmetic and age-label discrepancy | `direct_lookup` | fail / fail | fail / fail |
| [q097](#q097) | Associated within-article analysis-denominator discrepancy | `direct_lookup` | fail / pass | fail / pass |
| [q098](#q098) | Associated within-article analysis-denominator discrepancy | `direct_lookup` | fail / pass | fail / pass |
| [o011](#o011) | Ancillary within-article comparator-direction reversal | `false_premise` | fail / fail | fail / fail |
| [o012](#o012) | Comparator-orientation clarification, not an established biological contradiction | `direct_lookup` | fail / fail | fail / fail |
| [o005](#o005) | Explained denominator difference; not source conflict | `multi_hop` | fail / pass | fail / pass |
| [o017](#o017) | Different endpoints/populations/comparators; not source conflict | `cross_doc_synthesis` | fail / fail | fail / fail |
| [d020](#d020) | Primary versus sensitivity analysis; not source conflict | `false_premise` | fail / fail | fail / fail |
| [a010](#a010) | Different biological models and strands; not resolved source conflict | `multi_hop` | not run | fail / fail |

These historical scores use the historical gold contract. In particular c012, c013 and x005 were not evaluated as source_conflict in the frozen run. d020’s historical question also predates its primary-analysis clarification. The category column records the newer snapshot, not the historical run’s category.

## Case descriptions

### c004

**Question (revision 1, cardiology, `cross_doc_synthesis`):** How do the AF-management review and primary TAILORED-AF trial report the primary success percentages, and how should their difference be represented?

**Issue:** Cross-article numerical disagreement. The AF-management review reports 12-month freedom from AF of 89% versus 67% for TAILORED-AF. The primary randomized trial reports 88% versus 70% in its modified intention-to-treat population of 357. Both favour tailored ablation: this is a disagreement in reported estimates, not opposing treatment conclusions. The review mentions 374 randomized participants elsewhere but does not establish which analysis produced its percentages. The supplied text does not settle the difference.

**Resources and locations:**

- [PMC12880197](https://pmc.ncbi.nlm.nih.gov/articles/PMC12880197/), v1, PDF p. 6: AI mapping; review report of TAILORED-AF. Evidence identifier: `review_tailored`.
- [PMC12003177](https://pmc.ncbi.nlm.nih.gov/articles/PMC12003177/), v1, PDF p. 3: Results; mITT primary efficacy. Evidence identifier: `trial_primary`.

**Benchmark treatment:** Report each estimate with its article and analysis attribution. Use the primary trial’s 88%/70% when asked for its mITT result; do not average the pairs or treat them as interchangeable.

**Historical retrieval:**

| Depth | Accepted documents | Complete pinned evidence | Supported required facts |
| --- | --- | --- | --- |
| n3 | pass | fail | 0; fact recall 0% |
| n8 | pass | fail | 1; fact recall 50% |

At n3 both source documents were returned, but the review passage was introductory management text. At n8 the primary numerical evidence matched; the review numerical evidence still did not. Document presence therefore overstates conflict coverage.

**Corrected-gold retrieval (55 articles):**

| Depth | Accepted documents | Complete pinned evidence | Supported required facts |
| --- | --- | --- | --- |
| n3 | pass | fail | 0; fact recall 0.0% |
| n8 | pass | fail | 1; fact recall 50.0% |

This is saved-context evidence coverage under the current question and key, not generated-answer accuracy.

**Generated-answer handling:** Not evaluated.

### q051

**Question (revision 2, cardiology, `multi_hop`):** Which derivation sample-size statements appear in Gao’s CCTA paper, and how does the discussion frame its reported events-per-variable ratio?

**Issue:** Within-article sample-size inconsistency. Gao’s CCTA Results describe 280 patients and 46 MACE events. Discussion calls the derivation cohort n=131. Limitations describes EPV about 3.3 using 46 events/14 variables. No defined 131-person subset connecting these statements is established by the source.

**Resources and locations:**

- [PMC13433181](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433181/), v1, PDF p. 4: Results; one-year incidence. Evidence identifier: `ccta_incidence`.
- [PMC13433181](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433181/), v1, PDF p. 10: Discussion; proof-of-concept and EPV. Evidence identifier: `ccta_131`.
- [PMC13433181](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433181/), v1, PDF p. 12: Discussion; limitations / reported EPV. Evidence identifier: `ccta_limit`.

**Benchmark treatment:** Preserve both sample-size statements and the attributed EPV/overfitting discussion. Do not invent a complete-case subset or repair the source arithmetic.

**Historical retrieval:**

| Depth | Accepted documents | Complete pinned evidence | Supported required facts |
| --- | --- | --- | --- |
| n3 | fail | fail | 0; fact recall 0% |
| n8 | fail | fail | 0; fact recall 0% |

The required CCTA article disappeared at both depths in the 51-article run. Earlier source presence already lacked the complete evidence set; the new source loss must not be hidden by an unchanged evidence-fail score.

**Corrected-gold retrieval (55 articles):**

| Depth | Accepted documents | Complete pinned evidence | Supported required facts |
| --- | --- | --- | --- |
| n3 | fail | fail | 0; fact recall 0.0% |
| n8 | fail | fail | 0; fact recall 0.0% |

This is saved-context evidence coverage under the current question and key, not generated-answer accuracy.

**Generated-answer handling:** Not evaluated.

### c012

**Question (revision 2, cardiology, `source_conflict`):** What renal benefit and infection association were reported in the advanced-CKD SGLT2 cohort, and how does its evidential design compare with the HFpEF GLS cohort?

**Issue:** Within-article adjusted-estimate and design-label conflicts. The advanced-CKD abstract/Results report ESRD/dialysis aHR 0.35 (95% CI 0.19–0.67) and genitourinary infection aHR 1.78 (1.12–2.84). Its Table 2 instead reports 0.35 (0.19–0.66) and 1.80 (1.13–2.86). These are differently printed adjusted estimates for the same requested endpoints; no reconciliation is supplied. A second resource, the HFpEF GLS study, calls its design retrospective cohort in the abstract and retrospective case-control in Methods. It is a separate observational cardiac study, not competing evidence for the CKD numerical endpoints.

**Resources and locations:**

- [PMC11373557](https://pmc.ncbi.nlm.nih.gov/articles/PMC11373557/), v1, PDF p. 1: Results; ESRD/dialysis incidence and adjusted HR. Evidence identifier: `ckd_renal`.
- [PMC11373557](https://pmc.ncbi.nlm.nih.gov/articles/PMC11373557/), v1, PDF p. 1: Results; genitourinary infection incidence and adjusted HR. Evidence identifier: `ckd_infection`.
- [PMC11373557](https://pmc.ncbi.nlm.nih.gov/articles/PMC11373557/), v1, PDF p. 8: Discussion; residual confounding. Evidence identifier: `ckd_confounding`.
- [PMC13433862](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433862/), v1, PDF p. 3: Methods; retrospective case-control design. Evidence identifier: `hf_observational`.
- [PMC13433862](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433862/), v1, PDF p. 4: Results; six-month GLS change. Evidence identifier: `hf_gls`.
- [PMC11373557](https://pmc.ncbi.nlm.nih.gov/articles/PMC11373557/), v1, PDF p. 6: Results; Table 2 adjusted HRs for GUTIs and ESRD + dialysis. Evidence identifier: `ckd_table2`.
- HFpEF abstract p. 1 additionally uses the cohort design label; the current Methods anchor supplies the case-control label. This secondary label conflict is not a separately scored conflict fact.

**Benchmark treatment:** Current source_conflict gold requires both CKD readings, separately attributed, plus the observational HFpEF comparison. Retrospective observational is a neutral design description; attributed cohort/case-control labels are accepted. Neither study proves a causal treatment effect.

**Historical retrieval:**

| Depth | Accepted documents | Complete pinned evidence | Supported required facts |
| --- | --- | --- | --- |
| n3 | fail | fail | 0; fact recall 0% |
| n8 | fail | fail | 0; fact recall 0% |

The historical metrics above predate the source_conflict contract. The verified corrected-gold run below matches the CKD abstract renal span but misses Table 2, the complete infection/confounding spans and the required HFpEF evidence. It fails legitimately at both depths; no question or expectation is narrowed.

**Corrected-gold retrieval (55 articles):**

| Depth | Accepted documents | Complete pinned evidence | Supported required facts |
| --- | --- | --- | --- |
| n3 | fail | fail | 0; fact recall 0.0% |
| n8 | fail | fail | 0; fact recall 0.0% |

This is saved-context evidence coverage under the current question and key, not generated-answer accuracy.

**Generated-answer handling:** Not evaluated.

### c013

**Question (revision 2, cardiology, `source_conflict`):** What historical price basis and trial sources underlie the HFpEF cost-per-outcome analysis, and what CNTs were reported for its composite outcome?

**Issue:** Within-article price-provenance discrepancy. The HFpEF cost analysis abstract states 2022 US prices. Methods says drug costs were 75% of NADAC extracted in July 2023. A price year and an extraction date can differ in principle, but the article does not explain their relationship here; preserve this as an unresolved provenance discrepancy, not proof of opposite efficacy conclusions. The same analysis reports CNT $148,547.13 for dapagliflozin and $245,346.77 for sacubitril–valsartan using separate DELIVER and pooled PARAGLIDE-HF/PARAGON-HF data.

**Resources and locations:**

- [PMC10985250](https://pmc.ncbi.nlm.nih.gov/articles/PMC10985250/), v1, PDF p. 1: Abstract/Methods; historical US price year. Evidence identifier: `cost_year`.
- [PMC10985250](https://pmc.ncbi.nlm.nih.gov/articles/PMC10985250/), v1, PDF p. 3: Results; annualized cost needed to treat. Evidence identifier: `cost_values`.
- [PMC10985250](https://pmc.ncbi.nlm.nih.gov/articles/PMC10985250/), v1, PDF p. 2: Methods; drug cost basis. Evidence identifier: `cost_methods_nadac`.
- [PMC10985250](https://pmc.ncbi.nlm.nih.gov/articles/PMC10985250/), v1, PDF p. 1: Abstract; Methods and Results. Evidence identifier: `cost_abstract_complete`.

**Benchmark treatment:** Current source_conflict gold requires both attributed price-basis statements and the scoped CNTs. Do not infer current prices, head-to-head efficacy or a reconciliation of the dates.

**Historical retrieval:**

| Depth | Accepted documents | Complete pinned evidence | Supported required facts |
| --- | --- | --- | --- |
| n3 | pass | fail | 1; fact recall 50% |
| n8 | pass | fail | 1; fact recall 50% |

The verified corrected-gold run below retrieves the complete abstract at n3 but misses the Methods reading. At n8 the Methods NADAC passage also matches (zero-based rank 7), so both attributed readings are covered. This evidence pass does not judge whether an answer explained the discrepancy.

**Corrected-gold retrieval (55 articles):**

| Depth | Accepted documents | Complete pinned evidence | Supported required facts |
| --- | --- | --- | --- |
| n3 | pass | fail | 2; fact recall 66.7% |
| n8 | pass | pass | 3; fact recall 100.0% |

This is saved-context evidence coverage under the current question and key, not generated-answer accuracy.

**Generated-answer handling:** Not evaluated.

### c024

**Question (revision 1, cardiology, `false_premise`):** Since every spironolactone participant in the Cameroon trial achieved office BP below 130/80 mmHg after one month, what supports that universal control claim?

**Issue:** Within-article universal-control claim and target conflict. The spironolactone trial abstract says all participants were controlled below office BP 130/80 after one month. Results says one of nine had office BP 140/67 and missed its stated office target below 140/90. That participant met the different home/SBPM target below 135/85. The disagreement involves office versus home measurement as well as incompatible universal office-control claims.

**Resources and locations:**

- [PMC4804513](https://pmc.ncbi.nlm.nih.gov/articles/PMC4804513/), v1, PDF p. 1: Abstract; control claim. Evidence identifier: `spirono_abstract`.
- [PMC4804513](https://pmc.ncbi.nlm.nih.gov/articles/PMC4804513/), v1, PDF p. 4: Results; conflicting targets and uncontrolled participant. Evidence identifier: `spirono_exception`.

**Benchmark treatment:** Reject the question’s universal office-control premise, attribute the abstract/body conflict, and distinguish home control from office control. Do not conceal the Results’ different office-target definition.

**Historical retrieval:**

| Depth | Accepted documents | Complete pinned evidence | Supported required facts |
| --- | --- | --- | --- |
| n3 | pass | fail | 1; fact recall 50% |
| n8 | pass | pass | 2; fact recall 100% |

At n8 the abstract claim appeared at zero-based rank 6 and the exception at rank 2: both sides were available. At n3 only the exception fact met the pinned evidence test. No generated correction was judged.

**Corrected-gold retrieval (55 articles):**

| Depth | Accepted documents | Complete pinned evidence | Supported required facts |
| --- | --- | --- | --- |
| n3 | pass | fail | 1; fact recall 50.0% |
| n8 | pass | pass | 2; fact recall 100.0% |

This is saved-context evidence coverage under the current question and key, not generated-answer accuracy.

**Generated-answer handling:** Not evaluated.

### d003

**Question (revision 1, diabetes, `multi_hop`):** Are the male genome-wide interaction counts consistent between the abstract and Results of Dabbs-Brown et al.’s gene/sex-hormone study?

**Issue:** Within-article interaction-count discrepancy. Dabbs-Brown’s abstract reports three SNP-by-sex-hormone interactions in men and fourteen in women. The Results paragraph reports two male and fourteen female relevant loci. Interaction counts and locus counts are not necessarily identical units, but the supplied article does not resolve the difference for this benchmark; do not assert a demonstrated counting explanation.

**Resources and locations:**

- [PMC12419643](https://pmc.ncbi.nlm.nih.gov/articles/PMC12419643/), v1, PDF p. 1: Abstract; reported male/female interaction counts. Evidence identifier: `gene_abstract_count`.
- [PMC12419643](https://pmc.ncbi.nlm.nih.gov/articles/PMC12419643/), v1, PDF p. 5: Results; two male interaction loci. Evidence identifier: `gene_result_count`.

**Benchmark treatment:** Attribute the abstract and Results counts and retain the unresolved discrepancy rather than inventing a resolution.

**Historical retrieval:**

| Depth | Accepted documents | Complete pinned evidence | Supported required facts |
| --- | --- | --- | --- |
| n3 | pass | fail | 0; fact recall 0% |
| n8 | pass | pass | 2; fact recall 100% |

At n8 both pinned passages matched (abstract at rank 6, Results at rank 5). Neither complete fact matched at n3. This is a retrieval success at n8, not evidence that an answer described the discrepancy correctly.

**Corrected-gold retrieval (55 articles):**

| Depth | Accepted documents | Complete pinned evidence | Supported required facts |
| --- | --- | --- | --- |
| n3 | pass | fail | 0; fact recall 0.0% |
| n8 | pass | pass | 2; fact recall 100.0% |

This is saved-context evidence coverage under the current question and key, not generated-answer accuracy.

**Generated-answer handling:** Not evaluated.

### d005

**Question (revision 1, diabetes, `direct_lookup`):** Which OR, CI and crude/adjusted P values does Jan et al.’s Table 4 print for CYP2C9*2, and can that line be treated as an internally coherent risk estimate?

**Issue:** Within-table statistical reporting anomaly. Jan’s CYP2C9*2 Table 4 row prints OR 0.102, CI 0.08–3.08, crude P=.021 and adjusted P=.031. The interval crosses one while the printed P values are significant; the reported direction also requires caution. The table does not establish a reliable repair or a coherent single-model interpretation.

**Resources and locations:**

- [PMC10452755](https://pmc.ncbi.nlm.nih.gov/articles/PMC10452755/), v1, PDF p. 6: Table 4; reported anomalous OR/CI/p-value. Evidence identifier: `drug_table_conflict`.

**Benchmark treatment:** Report the printed row and identify the anomaly. Do not silently change the OR, confidence interval or P values, and do not convert it into a validated protective-effect conclusion.

**Historical retrieval:**

| Depth | Accepted documents | Complete pinned evidence | Supported required facts |
| --- | --- | --- | --- |
| n3 | pass | pass | 1; fact recall 100% |
| n8 | pass | pass | 1; fact recall 100% |

**Corrected-gold retrieval (55 articles):**

| Depth | Accepted documents | Complete pinned evidence | Supported required facts |
| --- | --- | --- | --- |
| n3 | pass | pass | 1; fact recall 100.0% |
| n8 | pass | pass | 1; fact recall 100.0% |

This is saved-context evidence coverage under the current question and key, not generated-answer accuracy.

**Generated-answer handling:** Not evaluated.

### x001

**Question (revision 1, outliers, `multi_hop`):** Yuan et al.’s abstract reports results for 195 taxa, 11 UK Biobank associations and three taxa validated in FinnGen. How does the UK-results section qualify those associations after multiple-comparison correction, and what does the later common-taxa section claim?

**Issue:** Within-article significance-language conflict. Yuan’s abstract describes 195 taxa, eleven potential UK Biobank associations and three taxa validated in FinnGen. UK Results calls the associations suggestive and says they lost significance after Bonferroni correction. The later common-taxa Results nevertheless calls three taxa significantly causally associated in both databases. The supplied text does not reconcile the multiple-testing statements.

**Resources and locations:**

- [PMC10765819](https://pmc.ncbi.nlm.nih.gov/articles/PMC10765819/), v1, PDF p. 1: Abstract: Methods and Results. Evidence identifier: `mr-summary`.
- [PMC10765819](https://pmc.ncbi.nlm.nih.gov/articles/PMC10765819/), v1, PDF p. 4: Results: UK Biobank. Evidence identifier: `mr-uk-correction`.
- [PMC10765819](https://pmc.ncbi.nlm.nih.gov/articles/PMC10765819/), v1, PDF p. 4: Results: UK Biobank. Evidence identifier: `mr-uk-bonferroni`.
- [PMC10765819](https://pmc.ncbi.nlm.nih.gov/articles/PMC10765819/), v1, PDF p. 8: Results: Common taxa across databases. Evidence identifier: `mr-common-taxa`.

**Benchmark treatment:** Attribute the abstract, correction statement and common-taxa claim. Do not treat Mendelian-randomization associations as an administered probiotic or a demonstrated reduction in TB incidence.

**Historical retrieval:**

| Depth | Accepted documents | Complete pinned evidence | Supported required facts |
| --- | --- | --- | --- |
| n3 | pass | fail | 0; fact recall 0% |
| n8 | pass | fail | 0; fact recall 0% |

At n8 the summary, common-taxa assertion and Bonferroni sentence matched, but the separate UK suggestive-qualification anchor did not. Complete pinned evidence failed even though useful opposing language was present.

**Corrected-gold retrieval (55 articles):**

| Depth | Accepted documents | Complete pinned evidence | Supported required facts |
| --- | --- | --- | --- |
| n3 | pass | fail | 0; fact recall 0.0% |
| n8 | pass | fail | 0; fact recall 0.0% |

This is saved-context evidence coverage under the current question and key, not generated-answer accuracy.

**Generated-answer handling:** Not evaluated.

### x005

**Question (revision 2, outliers, `source_conflict`):** In Ciftci et al.’s dual-model Alzheimer paper, what accuracies are reported for the clinical ANN and MRI CNN, and what distinct tasks do those figures describe?

**Issue:** Within-article model-task conflict. Ciftci’s abstract assigns ANN accuracy 87.08% to early-stage risk prediction and CNN accuracy 97% to disease staging. Detailed ANN results describe binary Alzheimer/no-Alzheimer detection at the same 87.08% accuracy. Risk prediction and current binary diagnosis are different endpoints; the source does not demonstrate that they are equivalent. The CNN is a separate MRI staging task, not a head-to-head comparison on the clinical ANN dataset.

**Resources and locations:**

- [PMC12823827](https://pmc.ncbi.nlm.nih.gov/articles/PMC12823827/), v1, PDF p. 1: Abstract. Evidence identifier: `alzheimer-summary`.
- [PMC12823827](https://pmc.ncbi.nlm.nih.gov/articles/PMC12823827/), v1, PDF p. 7: Results: ANN binary classification. Evidence identifier: `alzheimer-ann-binary`.
- [PMC12823827](https://pmc.ncbi.nlm.nih.gov/articles/PMC12823827/), v1, PDF p. 8: Results: ANN overall accuracy. Evidence identifier: `alzheimer-ann-accuracy`.

**Benchmark treatment:** Current source_conflict gold requires both attributed ANN task descriptions while retaining the two reported accuracies. Do not invent a prospective prediction horizon or assert clinical superiority from these different tasks.

**Historical retrieval:**

| Depth | Accepted documents | Complete pinned evidence | Supported required facts |
| --- | --- | --- | --- |
| n3 | pass | fail | 0; fact recall 0% |
| n8 | pass | fail | 0; fact recall 0% |

The historical n3/n8 scores above used the older abstract-only evidence contract. The verified corrected-gold run below returns the right article but neither complete required conflict reading at either depth. Its failures are retained without changing the question or grading requirement.

**Corrected-gold retrieval (55 articles):**

| Depth | Accepted documents | Complete pinned evidence | Supported required facts |
| --- | --- | --- | --- |
| n3 | pass | fail | 0; fact recall 0.0% |
| n8 | pass | fail | 0; fact recall 0.0% |

This is saved-context evidence coverage under the current question and key, not generated-answer accuracy.

**Generated-answer handling:** Not evaluated.

### o002

**Question (revision 3, oncology, `multi_hop`):** Are the Zhongshan stage III cohort’s narrative and Table 2 MPR counts consistent for the chemoimmunotherapy arm?

**Issue:** Within-article pathological-response count conflict. The Zhongshan stage III NSCLC Results narrative says 19 of 26 patients in the chemoimmunotherapy arm achieved major pathological response. Table 2 reports 17 of 26 (65.3%) for that arm and 5 of 33 (15.1%) for chemotherapy. The table also prints ORR 19 of 26, but the article does not establish that a label mix-up explains the MPR narrative.

**Resources and locations:**

- [PMC10770829](https://pmc.ncbi.nlm.nih.gov/articles/PMC10770829/), v1, PDF p. 5: Results; pathological response narrative and confidence intervals. Evidence identifier: `stage_narrative`.
- [PMC10770829](https://pmc.ncbi.nlm.nih.gov/articles/PMC10770829/), v1, PDF p. 5: Table 2; treatment columns, pCR and MPR rows. Evidence identifier: `stage_table`.

**Benchmark treatment:** Report narrative and table counts with their locations. Do not choose a favoured count or silently reinterpret MPR as ORR.

**Historical retrieval:**

| Depth | Accepted documents | Complete pinned evidence | Supported required facts |
| --- | --- | --- | --- |
| n3 | pass | fail | 0; fact recall 0% |
| n8 | pass | fail | 0; fact recall 0% |

**Corrected-gold retrieval (55 articles):**

| Depth | Accepted documents | Complete pinned evidence | Supported required facts |
| --- | --- | --- | --- |
| n3 | pass | fail | 0; fact recall 0.0% |
| n8 | pass | fail | 0; fact recall 0.0% |

This is saved-context evidence coverage under the current question and key, not generated-answer accuracy.

**Generated-answer handling:** Not evaluated.

### o006

**Question (revision 2, oncology, `multi_hop`):** Are the Vietnam afatinib abstract and Table 2 consistent about the 30-mg and 40-mg starting-dose shares?

**Issue:** Within-article reversed dose assignment. The Vietnam afatinib abstract assigns 58.6% to a 40-mg starting dose and 39.9% to 30 mg. Table 2 assigns 201/343 (58.6%) to 30 mg and 137/343 (39.9%) to 40 mg. Both report 5/343 (1.5%) at 20 mg. The dose-to-percentage mapping, not the percentages themselves, conflicts.

**Resources and locations:**

- [PMC10840225](https://pmc.ncbi.nlm.nih.gov/articles/PMC10840225/), v1, PDF p. 1: Abstract; starting-dose distribution. Evidence identifier: `afatinib_abstract`.
- [PMC10840225](https://pmc.ncbi.nlm.nih.gov/articles/PMC10840225/), v1, PDF p. 4: Results and Table 2; initial dose, mTTF and dose distribution. Evidence identifier: `afatinib_ttf`.

**Benchmark treatment:** Preserve both assignments with attribution. Do not silently flip the abstract’s labels or infer which printed version is medically correct.

**Historical retrieval:**

| Depth | Accepted documents | Complete pinned evidence | Supported required facts |
| --- | --- | --- | --- |
| n3 | pass | fail | 0; fact recall 0% |
| n8 | pass | fail | 0; fact recall 0% |

**Corrected-gold retrieval (55 articles):**

| Depth | Accepted documents | Complete pinned evidence | Supported required facts |
| --- | --- | --- | --- |
| n3 | pass | fail | 0; fact recall 0.0% |
| n8 | pass | fail | 0; fact recall 0.0% |

This is saved-context evidence coverage under the current question and key, not generated-answer accuracy.

**Generated-answer handling:** Not evaluated.

### o029

**Question (revision 3, oncology, `multi_hop`):** How did the Hunan study’s unadjusted two-year DFS comparison change after propensity matching, and how should its OS evidence be interpreted?

**Issue:** Within-article analysis-label conflict. The Hunan study reports unadjusted two-year DFS 79.3% versus 60.2% (P=.048), with significance disappearing after PSM (P=.096). Its OS Results calls the 93.8% versus 87.1% comparison weighted (P=.038), while Figure 1D calls those curves after PSM. The DFS change is an analysis difference; the unresolved conflict is the OS analysis label. Limitations says follow-up is too short for mature OS conclusions.

**Resources and locations:**

- [PMC9844597](https://pmc.ncbi.nlm.nih.gov/articles/PMC9844597/), v1, PDF p. 1: Abstract; unadjusted pathological response and DFS. Evidence identifier: `hunan_response`.
- [PMC9844597](https://pmc.ncbi.nlm.nih.gov/articles/PMC9844597/), v1, PDF p. 7: Results 3.4; unadjusted DFS and loss of significance after PSM. Evidence identifier: `hunan_matched`.
- [PMC9844597](https://pmc.ncbi.nlm.nih.gov/articles/PMC9844597/), v1, PDF p. 7: Results 3.4; unweighted and weighted two-year OS comparisons. Evidence identifier: `hunan_os_results`.
- [PMC9844597](https://pmc.ncbi.nlm.nih.gov/articles/PMC9844597/), v1, PDF p. 9: Figure 1 legend; panel D OS curves labelled after PSM (p=0.038). Evidence identifier: `hunan_fig1_legend`.
- [PMC9844597](https://pmc.ncbi.nlm.nih.gov/articles/PMC9844597/), v1, PDF p. 12: Discussion; limitations: follow-up too short for OS endpoint. Evidence identifier: `hunan_os_limitation`.

**Benchmark treatment:** Preserve the unadjusted/PSM DFS distinction, attribute the competing OS labels and retain follow-up limitations. Neither matching nor weighting establishes randomized causality.

**Historical retrieval:**

| Depth | Accepted documents | Complete pinned evidence | Supported required facts |
| --- | --- | --- | --- |
| n3 | fail | fail | 0; fact recall 0% |
| n8 | fail | fail | 0; fact recall 0% |

The Hunan source was absent at both depths in the combined run; unrelated CKD/HFpEF propensity-method passages cannot replace its outcomes. o030 reuses this source in a synthesis task but does not separately test the competing OS labels.

**Corrected-gold retrieval (55 articles):**

| Depth | Accepted documents | Complete pinned evidence | Supported required facts |
| --- | --- | --- | --- |
| n3 | fail | fail | 0; fact recall 0.0% |
| n8 | fail | fail | 0; fact recall 0.0% |

This is saved-context evidence coverage under the current question and key, not generated-answer accuracy.

**Generated-answer handling:** Not evaluated.

### q102

**Question (revision 3, oncology, `direct_lookup`):** What hysterectomy exclusion and final analysis-group counts appear in the US dual-screening study’s Appendix 1 flow diagram?

**Issue:** Within-article flow-diagram arithmetic and age-label discrepancy. The dual-screening Appendix 1 flow diagram starts at 67,473 women, prints exclusions of 19,011, 1, 29, 17 and 6, then labels 48,209 remaining. Those exclusions sum to 19,064, which would leave 48,409. Subtracting the next printed exclusion of 7,898 from 48,209 gives 40,311, while the diagram prints an analysis group of 40,511. The flow label says ages 50–65 while the main study describes 50–64.

**Resources and locations:**

- [PMC9239676](https://pmc.ncbi.nlm.nih.gov/articles/PMC9239676/), v1, PDF p. 17: Appendix 1 figure 1; exclusions and analysis group. Evidence identifier: `flow`.

**Benchmark treatment:** The query requests the printed hysterectomy and final-analysis counts: report 19,011 and 40,511 as printed, without fixing the diagram or treating it as verified cohort arithmetic.

**Historical retrieval:**

| Depth | Accepted documents | Complete pinned evidence | Supported required facts |
| --- | --- | --- | --- |
| n3 | pass | fail | 0; fact recall 0% |
| n8 | pass | fail | 0; fact recall 0% |

**Corrected-gold retrieval (55 articles):**

| Depth | Accepted documents | Complete pinned evidence | Supported required facts |
| --- | --- | --- | --- |
| n3 | pass | fail | 0; fact recall 0.0% |
| n8 | pass | fail | 0; fact recall 0.0% |

This is saved-context evidence coverage under the current question and key, not generated-answer accuracy.

**Generated-answer handling:** Not evaluated.

### q097

**Question (revision 3, oncology, `direct_lookup`):** In the US dual-screening study's multinomial regression, what adjusted odds ratios were reported for college graduation and for the highest income level when predicting dual screening versus neither screen?

**Issue:** Associated within-article analysis-denominator discrepancy. The same US dual-screening article describes an analysis cohort of 40,511 while Table 4 labels N=42,701. This query requests adjusted regression estimates, not a new reconstruction of cohort size. The source review records the denominator difference without establishing its cause.

**Resources and locations:**

- [PMC9239676](https://pmc.ncbi.nlm.nih.gov/articles/PMC9239676/), v1, PDF p. 6: Results; multinomial regression, single or dual screening compared with neither screen (1a–1b). Evidence identifier: `screen_regression`.
- [PMC9239676](https://pmc.ncbi.nlm.nih.gov/articles/PMC9239676/), v1, PDF p. 9: Table 4; outcome referents, education and income rows. Evidence identifier: `screen_table4_predictors`.
- The same article’s analysis-cohort/flow description and Table 4 heading are the denominator-conflict resources; the query anchors listed above score the requested regression estimates.

**Benchmark treatment:** Retain the scoped adjusted ORs and reference groups. If an answer mentions sample size, attribute the source location; do not force either denominator into an unasked mandatory claim.

**Historical retrieval:**

| Depth | Accepted documents | Complete pinned evidence | Supported required facts |
| --- | --- | --- | --- |
| n3 | pass | fail | 0; fact recall 0% |
| n8 | pass | pass | 1; fact recall 100% |

**Corrected-gold retrieval (55 articles):**

| Depth | Accepted documents | Complete pinned evidence | Supported required facts |
| --- | --- | --- | --- |
| n3 | pass | fail | 0; fact recall 0.0% |
| n8 | pass | pass | 1; fact recall 100.0% |

This is saved-context evidence coverage under the current question and key, not generated-answer accuracy.

**Generated-answer handling:** Not evaluated.

### q098

**Question (revision 3, oncology, `direct_lookup`):** In the US dual-screening study's adjusted analyses, how did the screening patterns of Black and Hispanic women differ, each compared with White women?

**Issue:** Associated within-article analysis-denominator discrepancy. The same US dual-screening article describes an analysis cohort of 40,511 while Table 4 labels N=42,701. This query requests adjusted regression estimates, not a new reconstruction of cohort size. The source review records the denominator difference without establishing its cause.

**Resources and locations:**

- [PMC9239676](https://pmc.ncbi.nlm.nih.gov/articles/PMC9239676/), v1, PDF p. 9: Table 4; outcome referents, White reference and race rows. Evidence identifier: `screen_table4_race`.
- [PMC9239676](https://pmc.ncbi.nlm.nih.gov/articles/PMC9239676/), v1, PDF p. 6: Results; multinomial regression, single or dual screening compared with neither screen (1a–1b). Evidence identifier: `screen_regression`.
- [PMC9239676](https://pmc.ncbi.nlm.nih.gov/articles/PMC9239676/), v1, PDF p. 11: Results 2a; Hispanic higher and Black lower cervical-only odds versus dual screening. Evidence identifier: `screen_hispanic_single`.
- The same article’s analysis-cohort/flow description and Table 4 heading are the denominator-conflict resources; the query anchors listed above score the requested regression estimates.

**Benchmark treatment:** Retain the scoped adjusted ORs and reference groups. If an answer mentions sample size, attribute the source location; do not force either denominator into an unasked mandatory claim.

**Historical retrieval:**

| Depth | Accepted documents | Complete pinned evidence | Supported required facts |
| --- | --- | --- | --- |
| n3 | pass | fail | 1; fact recall 50% |
| n8 | pass | pass | 2; fact recall 100% |

**Corrected-gold retrieval (55 articles):**

| Depth | Accepted documents | Complete pinned evidence | Supported required facts |
| --- | --- | --- | --- |
| n3 | pass | fail | 1; fact recall 50.0% |
| n8 | pass | pass | 2; fact recall 100.0% |

This is saved-context evidence coverage under the current question and key, not generated-answer accuracy.

**Generated-answer handling:** Not evaluated.

### o011

**Question (revision 2, oncology, `false_premise`):** Does the RCT meta-analysis prove ICIs cannot cause heart failure because that subgroup result was nonsignificant?

**Issue:** Ancillary within-article comparator-direction reversal. The RCT cardiotoxicity meta-analysis abstract describes dual ICI versus single ICI for RR 0.48, whereas detailed Results labels the comparison single ICI versus dual ICI. The heart-failure question itself concerns RR 1.11 (0.48–2.58), P=.80, not that third comparison. Overall cardiac adverse events and heart failure are different endpoints.

**Resources and locations:**

- [PMC11181582](https://pmc.ncbi.nlm.nih.gov/articles/PMC11181582/), v1, PDF p. 1: Abstract; pooled RCT cardiac adverse events and subtype outcomes. Evidence identifier: `rct_cv`.
- [PMC11181582](https://pmc.ncbi.nlm.nih.gov/articles/PMC11181582/), v1, PDF p. 3: Results; nonsignificant imprecise cardiac-failure estimate. Evidence identifier: `rct_failure_results`.
- [PMC11181582](https://pmc.ncbi.nlm.nih.gov/articles/PMC11181582/), v1, PDF p. 3: Results; single ICI and ICI plus chemotherapy versus chemotherapy. Evidence identifier: `rct_primary_results`.
- The ancillary Results comparison heading (single ICI versus dual ICI) is a review-note resource, not a required conflict anchor for this question.

**Benchmark treatment:** Do not require the ancillary RR 0.48 comparison to answer this question. If included, preserve attribution and comparator direction. A nonsignificant imprecise heart-failure result does not prove no risk.

**Historical retrieval:**

| Depth | Accepted documents | Complete pinned evidence | Supported required facts |
| --- | --- | --- | --- |
| n3 | pass | fail | 0; fact recall 0% |
| n8 | pass | fail | 0; fact recall 0% |

This direction issue comes from the retained validation note; it is not separately anchored or scored as conflict handling by this query.

**Corrected-gold retrieval (55 articles):**

| Depth | Accepted documents | Complete pinned evidence | Supported required facts |
| --- | --- | --- | --- |
| n3 | pass | fail | 0; fact recall 0.0% |
| n8 | pass | fail | 0; fact recall 0.0% |

This is saved-context evidence coverage under the current question and key, not generated-answer accuracy.

**Generated-answer handling:** Not evaluated.

### o012

**Question (revision 2, oncology, `direct_lookup`):** How did pembrolizumab versus nivolumab compare for cause-specific mortality in the older NSCLC cohort?

**Issue:** Comparator-orientation clarification, not an established biological contradiction. The older NSCLC cohort’s Table 2 uses pembrolizumab as reference. The CVD sHR 1.08 describes nivolumab versus pembrolizumab. Prose reports NSCLC sHR 0.67 for pembrolizumab versus nivolumab, reciprocal to Table 2’s approximately 1.49. Different ratio directions explain the NSCLC pair; they must not be mixed.

**Resources and locations:**

- [PMC12495207](https://pmc.ncbi.nlm.nih.gov/articles/PMC12495207/), v1, PDF p. 1: Abstract; causes of death and Fine–Gray estimates. Evidence identifier: `mortality`.
- [PMC12495207](https://pmc.ncbi.nlm.nih.gov/articles/PMC12495207/), v1, PDF p. 6: Results; comparator-specific CVD and NSCLC subdistribution HRs. Evidence identifier: `mortality_drug_results`.
- Table 2’s reference-drug column provides the additional orientation check; it is not a separate required conflict anchor in this query.

**Benchmark treatment:** Name the drug/reference orientation for each endpoint. Preserve the nonsignificant CVD estimate and distinguish a between-drug comparison from an untreated-control comparison.

**Historical retrieval:**

| Depth | Accepted documents | Complete pinned evidence | Supported required facts |
| --- | --- | --- | --- |
| n3 | pass | fail | 0; fact recall 0% |
| n8 | pass | fail | 0; fact recall 0% |

The orientation issue is a retained annotation note; a retrieval evidence pass is not a judged demonstration that the answer preserved ratio direction.

**Corrected-gold retrieval (55 articles):**

| Depth | Accepted documents | Complete pinned evidence | Supported required facts |
| --- | --- | --- | --- |
| n3 | pass | fail | 0; fact recall 0.0% |
| n8 | pass | fail | 0; fact recall 0.0% |

This is saved-context evidence coverage under the current question and key, not generated-answer accuracy.

**Generated-answer handling:** Not evaluated.

### o005

**Question (revision 2, oncology, `multi_hop`):** Why do postoperative pembrolizumab discontinuation percentages differ between the Helsinki abstract and results?

**Issue:** Explained denominator difference; not source conflict. The Helsinki pembrolizumab abstract reports eight postoperative discontinuations as 10.7% of all 75 patients. Results reports the same eight as 23.5% of the 34 who started postoperative therapy. Both percentages can be correct because the denominators differ.

**Resources and locations:**

- [PMC12931073](https://pmc.ncbi.nlm.nih.gov/articles/PMC12931073/), v1, PDF p. 1: Abstract; immune adverse events and discontinuation denominators. Evidence identifier: `breast_ae`.
- [PMC12931073](https://pmc.ncbi.nlm.nih.gov/articles/PMC12931073/), v1, PDF p. 7: Results; postoperative discontinuation and overall denominators. Evidence identifier: `breast_stop`.
- [PMC12931073](https://pmc.ncbi.nlm.nih.gov/articles/PMC12931073/), v1, PDF p. 5: Results; eight of 34 adjuvant discontinuations. Evidence identifier: `breast_stop_results`.

**Benchmark treatment:** Explain both denominators. Do not tag this as incompatible discontinuation counts.

**Historical retrieval:**

| Depth | Accepted documents | Complete pinned evidence | Supported required facts |
| --- | --- | --- | --- |
| n3 | pass | fail | 0; fact recall 0% |
| n8 | pass | pass | 1; fact recall 100% |

**Corrected-gold retrieval (55 articles):**

| Depth | Accepted documents | Complete pinned evidence | Supported required facts |
| --- | --- | --- | --- |
| n3 | pass | fail | 0; fact recall 0.0% |
| n8 | pass | pass | 1; fact recall 100.0% |

This is saved-context evidence coverage under the current question and key, not generated-answer accuracy.

**Generated-answer handling:** Not evaluated.

### o017

**Question (revision 4, oncology, `cross_doc_synthesis`):** Why can the observational CV-event meta-analysis and older PD-1 cause-specific mortality cohort not be read as the same cardiovascular endpoint?

**Issue:** Different endpoints/populations/comparators; not source conflict. The observational ICI meta-analysis reports HR 1.78 for cardiovascular events versus non-ICI treatment (four contributing HR studies), separately from 3% prevalence. The older PD-1 cohort reports nonsignificant CVD mortality sHR 1.08 comparing two PD-1 drugs. Event occurrence and cause-specific death, and treated-versus-untreated versus between-drug comparisons, are different questions. The prevalence passage itself loosely uses comparative wording; prevalence is not a relative effect estimate.

**Resources and locations:**

- [PMC11891047](https://pmc.ncbi.nlm.nih.gov/articles/PMC11891047/), v1, PDF p. 1: Abstract; observational studies, CV prevalence and pooled hazard. Evidence identifier: `obs_cv`.
- [PMC11891047](https://pmc.ncbi.nlm.nih.gov/articles/PMC11891047/), v1, PDF p. 14: Discussion; limitations: four studies contribute to HR. Evidence identifier: `obs_hr_scope`.
- [PMC12495207](https://pmc.ncbi.nlm.nih.gov/articles/PMC12495207/), v1, PDF p. 1: Abstract; causes of death and Fine–Gray estimates. Evidence identifier: `mortality`.
- [PMC12495207](https://pmc.ncbi.nlm.nih.gov/articles/PMC12495207/), v1, PDF p. 6: Results; comparator-specific CVD and NSCLC subdistribution HRs. Evidence identifier: `mortality_drug_results`.
- [PMC11891047](https://pmc.ncbi.nlm.nih.gov/articles/PMC11891047/), v1, PDF p. 4: Results 3.2; twelve observational studies and 23,621 patients. Evidence identifier: `obs_population_results`.
- [PMC11891047](https://pmc.ncbi.nlm.nih.gov/articles/PMC11891047/), v1, PDF p. 4: Results 3.4.1; 3% prevalence (noncomparative measure despite source wording). Evidence identifier: `obs_prevalence_results`.
- [PMC11891047](https://pmc.ncbi.nlm.nih.gov/articles/PMC11891047/), v1, PDF p. 4: Results 3.4.2; ICI versus non-ICI overall HR. Evidence identifier: `obs_hr_results`.

**Benchmark treatment:** Keep endpoints, populations, comparators and prevalence/HR/sHR measures separate. Do not manufacture a contradiction or pool them into one causal estimate.

**Historical retrieval:**

| Depth | Accepted documents | Complete pinned evidence | Supported required facts |
| --- | --- | --- | --- |
| n3 | fail | fail | 0; fact recall 0% |
| n8 | fail | fail | 0; fact recall 0% |

**Corrected-gold retrieval (55 articles):**

| Depth | Accepted documents | Complete pinned evidence | Supported required facts |
| --- | --- | --- | --- |
| n3 | fail | fail | 0; fact recall 0.0% |
| n8 | fail | fail | 0; fact recall 0.0% |

This is saved-context evidence coverage under the current question and key, not generated-answer accuracy.

**Generated-answer handling:** Not evaluated.

### d020

**Question (revision 2, diabetes, `false_premise`):** Since the primary intention-to-treat analysis of Berthoumieux’s DSMES+CGM trial showed statistically significant HbA1c improvement at both follow-up visits, what was the later benefit?

**Issue:** Primary versus sensitivity analysis; not source conflict. Berthoumieux’s primary intention-to-treat HbA1c comparison is significant at three months (P=.03) but not six months (P=.12; difference −0.6 percentage points, CI −1.4 to 0.2). A sensitivity analysis excludes nine intervention nonparticipants and reports a six-month difference −0.8 (CI −1.6 to −0.02; P=.046). Those are different analysis populations, not incompatible results for one declared analysis.

**Resources and locations:**

- [PMC13175446](https://pmc.ncbi.nlm.nih.gov/articles/PMC13175446/), v1, PDF p. 1: Abstract Results; ITT HbA1c timepoints. Evidence identifier: `cgm_timepoints`.
- Same article, Methods sensitivity-analysis restriction and Results sensitivity-analysis paragraph: exclusion of nine nonparticipants and the six-month P=.046 estimate. These passages explain the scope distinction; they are not required evidence for the corrected primary-analysis question.

**Benchmark treatment:** The corrected false-premise question explicitly asks about primary intention-to-treat results. Reject that scoped premise; optionally describe sensitivity results with their restriction. d007 and d010 also reuse the primary trial’s scoped endpoints.

**Historical retrieval:**

| Depth | Accepted documents | Complete pinned evidence | Supported required facts |
| --- | --- | --- | --- |
| n3 | pass | fail | 0; fact recall 0% |
| n8 | pass | fail | 0; fact recall 0% |

**Corrected-gold retrieval (55 articles):**

| Depth | Accepted documents | Complete pinned evidence | Supported required facts |
| --- | --- | --- | --- |
| n3 | pass | fail | 0; fact recall 0.0% |
| n8 | pass | fail | 0; fact recall 0.0% |

This is saved-context evidence coverage under the current question and key, not generated-answer accuracy.

**Generated-answer handling:** Not evaluated.

### a010

**Question (revision 2, als-ftd, `multi_hop`):** What model-related explanation did Parameswaran et al. give for differences between Drosophila reports and their vertebrate repeat-RNA toxicity findings, and what experiment supported their PKR interpretation?

**Issue:** Different biological models and strands; not resolved source conflict. Parameswaran discusses different repeat-RNA toxicities in Drosophila and vertebrate models, offering vertebrate PKR expression as a partial explanation. In zebrafish, reducing eif2ak2 mitigates antisense but not sense axonopathy. Models, species and RNA strands differ; this is not proof that the cited reports made incompatible claims under identical conditions.

**Resources and locations:**

- [PMC10188109](https://pmc.ncbi.nlm.nih.gov/articles/PMC10188109/), v1, PDF p. 13: Discussion: model-specific PKR expression. Evidence identifier: `model-pkr`.
- [PMC10188109](https://pmc.ncbi.nlm.nih.gov/articles/PMC10188109/), v1, PDF p. 11: Results: eif2ak2 knockdown. Evidence identifier: `zebrafish`.
- [PMC10188109](https://pmc.ncbi.nlm.nih.gov/articles/PMC10188109/), v1, PDF p. 16: Figure 7 legend: strand-specific toxicity result. Evidence identifier: `zebrafish-caption-result`.
- [PMC10188109](https://pmc.ncbi.nlm.nih.gov/articles/PMC10188109/), v1, PDF p. 17: Figure 7C-F legend: motor axon endpoints. Evidence identifier: `zebrafish-caption-endpoints`.

**Benchmark treatment:** Retain the authors’ tentative model explanation and the strand-specific experiment. Do not assert that all model discrepancies are resolved.

**Historical retrieval:** Not executed in the 51-article combined run.

ALS/FTD was excluded from the 51-article baseline; there is no retrieval result for a010 in that run.

**Corrected-gold retrieval (55 articles):**

| Depth | Accepted documents | Complete pinned evidence | Supported required facts |
| --- | --- | --- | --- |
| n3 | pass | fail | 1; fact recall 50.0% |
| n8 | pass | fail | 1; fact recall 50.0% |

This is saved-context evidence coverage under the current question and key, not generated-answer accuracy.

**Generated-answer handling:** Not evaluated.

## Related cases and retired legacy conflict

- **o030** uses the Hunan study alongside a reflex-testing consensus. It inherits the source’s limitations, but the gold does not separately require the weighted/PSM label discrepancy. Treat it as a dependency of o029, not an independently measured conflict-resolution case.
- **d007 / d010** use primary DSMES+CGM follow-up evidence; the sensitivity-analysis distinction in d020 applies when discussing those results. Different six-month HbA1c and time-in-range significance is an endpoint difference.
- **o009** uses the observational ICI meta-analysis. Its 3% prevalence and HR 1.78 are different measures; the Results’ comparative prevalence language must not be converted into a relative risk.
- **Legacy q062** asked about spot urine testing and resistant-hypertension referrals in `cardio-hypertension-guidelines.pdf`. Historical gold combined 43–55% endocrinology and 35–45% cardiology referral figures without a resolved source binding. The rebuilt benchmark retired that query with the excluded source; c006/c007 are replacement tasks, not corrected versions of those percentages. q062 was not in the 148-query combined run. This legacy entry records the retirement decision, not a newly verified article conflict.

## Review of the source-conflict contract changes

Commit 4d19bdc restores the original c012/c013/x005 wording, adds competing-source evidence, and splits d015/d016 into separately scored parts. Commit 57b23ff then replaces the either-reading alternatives with a source_conflict contract requiring both readings. The latter is a material grading change, not just descriptive metadata.

Useful changes: both readings are explicit, their passages are identified, and omissions can be measured. Splitting d015/d016 avoids bundling distinct requested facts into one all-or-nothing fact.

Accepted contract and remaining interpretation limits:

1. **Accepted conflict-evaluation contract — c012, c013, x005.** The questions retain their original wording and are categorized as source_conflict. The accepted grading contract requires both source readings with attribution. Missing a reading or failing to surface the discrepancy is a legitimate evaluation failure, not a reason to narrow the question, discard conflicting evidence or relax grading to obtain a pass. The earlier recommendation to rewrite these questions is withdrawn following the user’s clarification; it is not a merge blocker. Questions, facts, evidence sets and recorded results remain unchanged.
2. **Category consistency.** Only c012/c013/x005 use the new category. Existing explicit conflict tasks remain multi_hop, synthesis, lookup or false_premise. Consequently a source_conflict category aggregate is not an aggregate of all conflict cases in this inventory. A separate within-article/cross-article issue tag would preserve their retrieval structure; c012 still requires two articles despite losing its synthesis category label.
3. **Validation strength.** The new validator checks two facts and two anchors, but does not enforce independent reading-to-anchor bindings or prove that the anchors actually contain incompatible readings. Schema acceptance alone is not semantic conflict certification.
4. **Historical compatibility.** The scorer now recognizes an additional category while its version label remains pinned-span-coverage-v3. File fingerprints change, so old/new runs must still pass the existing compatibility checks; never merge their scores based solely on that unchanged label. Preserve revisions and source/gold hashes.
5. **Evidence retention.** The corrected 55-article results have a retained immutable summary with run hashes, query/revision/category hashes, source identities, evidence matches and scorer/model/dependency fingerprints. The historical 51-article metrics remain separately labelled. Unsupported earlier targeted observations are superseded, not retroactively verified.

All 224 offline tests pass, including saved-context corruption and copied-embedding checks. All 158 corrected-gold combined cases execute and their saved metrics and fingerprints are recomputed. Those checks do not measure generated-answer conflict handling. No new model-review session, generation or paid evaluation was launched.

## Article identity inventory

All entries below use the version-1 PMC deposit recorded in the benchmark. Links identify public articles; they do not certify that a live page still displays precisely the frozen deposit.

- **PMC10188109, v1** — [Antisense, but not sense, repeat expanded RNAs activate PKR/eIF2α-dependent ISR in C9ORF72 FTD/ALS](https://pmc.ncbi.nlm.nih.gov/articles/PMC10188109/). DOI: [10.7554/eLife.85902](https://doi.org/10.7554/eLife.85902). Repository alias: `als-ftd-pmc10188109.pdf`.
- **PMC10452755, v1** — [Association of CYP2C9*2 Allele with Sulphonylurea-Induced Hypoglycaemia in Type 2 Diabetes Mellitus Patients: A Pharmacogenetic Study in Pakistani Pashtun Population](https://pmc.ncbi.nlm.nih.gov/articles/PMC10452755/). DOI: [10.3390/biomedicines11082282](https://doi.org/10.3390/biomedicines11082282). Repository alias: `diabetes-cyp2c9-hypoglycaemia.pdf`.
- **PMC10765819, v1** — [Causal relationship between gut microbiota and tuberculosis: a bidirectional two-sample Mendelian randomization analysis](https://pmc.ncbi.nlm.nih.gov/articles/PMC10765819/). DOI: [10.1186/s12931-023-02652-7](https://doi.org/10.1186/s12931-023-02652-7). Repository alias: `outlier-microbiome-tb-mr.pdf`.
- **PMC10770829, v1** — [Comparison of neoadjuvant chemoimmunotherapy and chemotherapy alone for resectable stage III non-small cell lung cancer: a real-world cohort study](https://pmc.ncbi.nlm.nih.gov/articles/PMC10770829/). DOI: [10.3389/fimmu.2023.1343504](https://doi.org/10.3389/fimmu.2023.1343504). Repository alias: `onco-nsclc-neoadjuvant-stageiii.pdf`.
- **PMC10840225, v1** — [A real-world cohort study of first-line afatinib in patients with EGFR-mutant advanced non-small cell lung cancer in Vietnam](https://pmc.ncbi.nlm.nih.gov/articles/PMC10840225/). DOI: [10.1186/s12885-024-11891-w](https://doi.org/10.1186/s12885-024-11891-w). Repository alias: `onco-afatinib-vietnam.pdf`.
- **PMC10985250, v1** — [Dapagliflozin versus sacubitril–valsartan for heart failure with mildly reduced or preserved ejection fraction](https://pmc.ncbi.nlm.nih.gov/articles/PMC10985250/). DOI: [10.3389/fphar.2024.1357673](https://doi.org/10.3389/fphar.2024.1357673). Repository alias: `cardio-hfpef-dapagliflozin-cost-analysis.pdf`.
- **PMC11181582, v1** — [Immune checkpoint inhibitor-induced cardiotoxicity in patients with lung cancer: a systematic review and meta-analysis](https://pmc.ncbi.nlm.nih.gov/articles/PMC11181582/). DOI: [10.1186/s40959-024-00229-x](https://doi.org/10.1186/s40959-024-00229-x). Repository alias: `onco-ici-cardiac-rct-meta.pdf`.
- **PMC11373557, v1** — [Investigation of cardiorenal outcomes and incidence of genitourinary tract infection after combined SGLT2 inhibitor and ACEI/ARB use in patients with chronic kidney disease stages 3-5: A real-world retrospective cohort study in Taiwan](https://pmc.ncbi.nlm.nih.gov/articles/PMC11373557/). DOI: [10.7150/ijms.96969](https://doi.org/10.7150/ijms.96969). Repository alias: `cardio-ckd-sglt2-acei-arb.pdf`.
- **PMC11891047, v1** — [Cardiovascular toxicity induced by immunotherapy in non-small cell lung cancer: a systematic review and meta-analysis of observational studies](https://pmc.ncbi.nlm.nih.gov/articles/PMC11891047/). DOI: [10.3389/fonc.2025.1528950](https://doi.org/10.3389/fonc.2025.1528950). Repository alias: `onco-ici-cv-observational.pdf`.
- **PMC12003177, v1** — [Artificial intelligence for individualized treatment of persistent atrial fibrillation: a randomized controlled trial](https://pmc.ncbi.nlm.nih.gov/articles/PMC12003177/). DOI: [10.1038/s41591-025-03517-w](https://doi.org/10.1038/s41591-025-03517-w). Repository alias: `cardio-tailored-af-randomized-trial.pdf`.
- **PMC12419643, v1** — [Identification of gene-sex hormone interactions associated with type 2 diabetes among men and women](https://pmc.ncbi.nlm.nih.gov/articles/PMC12419643/). DOI: [10.1371/journal.pgen.1011470](https://doi.org/10.1371/journal.pgen.1011470). Repository alias: `diabetes-gene-sex-hormone-interactions.pdf`.
- **PMC12495207, v1** — [Factors Associated With Cause-specific Mortality in Older Patients With Advanced NSCLC Treated With PD-1 Inhibitors: A U.S. Population-based Cohort Study](https://pmc.ncbi.nlm.nih.gov/articles/PMC12495207/). DOI: [10.1177/10732748251380932](https://doi.org/10.1177/10732748251380932). Repository alias: `onco-pd1-cause-specific-mortality.pdf`.
- **PMC12823827, v1** — [A dual-model AI framework for Alzheimer’s disease diagnosis using clinical and MRI data](https://pmc.ncbi.nlm.nih.gov/articles/PMC12823827/). DOI: [10.3389/fmed.2025.1713062](https://doi.org/10.3389/fmed.2025.1713062). Repository alias: `outlier-alzheimer-dual-model.pdf`.
- **PMC12880197, v1** — [Artificial Intelligence–driven Detection, Mapping, and Personalized Therapy for Atrial Fibrillation](https://pmc.ncbi.nlm.nih.gov/articles/PMC12880197/). DOI: [10.19102/icrm.2026.17011](https://doi.org/10.19102/icrm.2026.17011). Repository alias: `cardio-ai-af-management-review.pdf`.
- **PMC12931073, v1** — [Real-world outcome of neoadjuvant therapy with or without pembrolizumab for triple-negative breast cancer](https://pmc.ncbi.nlm.nih.gov/articles/PMC12931073/). DOI: [10.2340/1651-226X.2026.44896](https://doi.org/10.2340/1651-226X.2026.44896). Repository alias: `onco-breast-pembrolizumab-helsinki.pdf`.
- **PMC13175446, v1** — [A Digital Diabetes Self-Management Education and Support Program Integrated With Continuous Glucose Monitoring for Type 2 Diabetes: Randomized Controlled Trial](https://pmc.ncbi.nlm.nih.gov/articles/PMC13175446/). DOI: [10.2196/78321](https://doi.org/10.2196/78321). Repository alias: `diabetes-digital-education-cgm-trial.pdf`.
- **PMC13433181, v1** — [Development of a MACE risk prediction model based on CCTA-derived quantitative parameters: a proof-of-concept study](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433181/). DOI: [10.3389/fcvm.2026.1884303](https://doi.org/10.3389/fcvm.2026.1884303). Repository alias: `cardio-cad-ct-angiography.pdf`.
- **PMC13433862, v1** — [Long-term SGLT2 inhibitor therapy improves myocardial strain and diastolic function in HFpEF: a retrospective study linking functional recovery to reduced myocardial fibrosis](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433862/). DOI: [10.3389/fcvm.2026.1858364](https://doi.org/10.3389/fcvm.2026.1858364). Repository alias: `cardio-heartfailure-biomarkers.pdf`.
- **PMC4804513, v1** — [Effect of low-dose spironolactone on resistant hypertension in type 2 diabetes mellitus: a randomized controlled trial in a sub-Saharan African population](https://pmc.ncbi.nlm.nih.gov/articles/PMC4804513/). DOI: [10.1186/s13104-016-1987-5](https://doi.org/10.1186/s13104-016-1987-5). Repository alias: `cardio-spironolactone-diabetes-trial.pdf`.
- **PMC9239676, v1** — [US women screen at low rates for both cervical and colorectal cancers than a single cancer: a cross-sectional population-based observational study](https://pmc.ncbi.nlm.nih.gov/articles/PMC9239676/). DOI: [10.7554/eLife.76070](https://doi.org/10.7554/eLife.76070). Repository alias: `onco-colorectal-screening.pdf`.
- **PMC9844597, v1** — [A real‐world comparison between neoadjuvant chemoimmunotherapy and chemotherapy alone for resectable non‐small cell lung cancer](https://pmc.ncbi.nlm.nih.gov/articles/PMC9844597/). DOI: [10.1002/cam4.4889](https://doi.org/10.1002/cam4.4889). Repository alias: `onco-nsclc-neoadjuvant-hunan.pdf`.

## Audit references and main-merge retention

- [PR 45: validation findings](https://github.com/juan-casimiro/ai-research-assistant/pull/45) and [PR 46: corrections and late follow-up](https://github.com/juan-casimiro/ai-research-assistant/pull/46).
- [Frozen combined evaluation report](https://github.com/juan-casimiro/ai-research-assistant/blob/bc0594e6c845116e4203a9467eb27f23c57ab621/benchmark/combined/v1/REPORT.md).
- [Reviewed cardiology queries](https://github.com/juan-casimiro/ai-research-assistant/blob/57b23ffc2812b2a4bc346d39571c312f3e7fc2c2/benchmark/cardiology/v1/queries.json), [diabetes queries](https://github.com/juan-casimiro/ai-research-assistant/blob/57b23ffc2812b2a4bc346d39571c312f3e7fc2c2/benchmark/diabetes/v1/queries.json), [oncology queries](https://github.com/juan-casimiro/ai-research-assistant/blob/57b23ffc2812b2a4bc346d39571c312f3e7fc2c2/benchmark/oncology/v1/queries.json), [outlier queries](https://github.com/juan-casimiro/ai-research-assistant/blob/57b23ffc2812b2a4bc346d39571c312f3e7fc2c2/benchmark/outliers/v1/queries.json).
- Retain this report and the root README link in the final epic-to-main PR. Experimental transcripts, local archives, run helpers and bulk epic artifacts need not be retained for the report to remain readable. Repository aliases and evidence identifiers are explanatory labels here, not required local links.
- Retention is an explicit requirement for the eventual main merge, not a claim that this open PR has already been merged. Update the case descriptions and add a separately identified answer-quality result if generated conflict handling is evaluated later.
