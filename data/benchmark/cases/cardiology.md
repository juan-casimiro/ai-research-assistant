# Cardiology evaluation cases

Generated from the current combined v2 inputs. Regenerate with
`python -m tools.evaluation.render_case_index`; do not edit this page by hand.

[All topics](README.md) · [Article catalogue](articles.md) ·
[Authoritative questions](../cardiology/queries.json) ·
[Dependency map](../case_dependencies.json)

Expected responses are model-reviewed references, not biomedical expert
certification or observed RAG responses. No new scoring is performed here.

## Find a question

| ID | Category | Question |
| --- | --- | --- |
| [q041](#q041) | direct_lookup | According to the 2026 review of AF management, what AUCs did the cited Attia study report when using one versus multiple sinus-rhythm ECGs to identify a history of paroxysmal AF? |
| [q042](#q042) | multi_hop | In TAILORED-AF, how was the primary efficacy endpoint defined, and what were its 12-month results in the modified intention-to-treat population? |
| [q044](#q044) | cross_doc_synthesis | How do the review-cited CHA2DS2-VASc thromboembolism discrimination and the Sun STEMI study’s CHA2DS2-VA no-reflow discrimination differ, including the latter’s sex subgroups? |
| [q047](#q047) | direct_lookup | In Gao’s CCTA derivation cohort, how did the combined nomogram’s AUC compare with the strongest individual imaging predictor? |
| [q048](#q048) | multi_hop | What external discrimination and calibration results did Gao’s CCTA nomogram report, and why might lower-risk outpatient settings still need recalibration? |
| [q049](#q049) | direct_lookup | Which CCTA variables does Gao’s conclusion identify as independent MACE risk factors, and which variable is protective? |
| [q050](#q050) | cross_doc_synthesis | Compare the combined-model discrimination reported by Gao’s CCTA MACE study and Sun’s CHA2DS2-VA no-reflow study, including the latter’s male subgroup. Why are these different prediction tasks? |
| [q051](#q051) | multi_hop | Which derivation sample-size statements appear in Gao’s CCTA paper, and how does the discussion frame its reported events-per-variable ratio? |
| [q053](#q053) | direct_lookup | What six-month GLS changes did the retrospective HFpEF biomarker study report for SGLT2 inhibitor users and controls? |
| [q054](#q054) | direct_lookup | At the reported follow-up, what HF rehospitalization proportions and counts were observed in the HFpEF SGLT2 biomarker cohort? |
| [q055](#q055) | direct_lookup | How does the HFpEF biomarker study’s aggregate GLS–PIIINP correlation compare with its within-treatment-group correlations, and what inference does that support? |
| [q056](#q056) | direct_lookup | What six-month reductions in NT-proBNP, PIIINP and GDF-15 were reported in the HFpEF SGLT2 biomarker study, compared with controls? |
| [q058](#q058) | direct_lookup | What did the HFpEF SGLT2 biomarker study report about interaction by diabetes status, and does that establish independence from glycemic changes? |
| [q065](#q065) | multi_hop | In Sun’s STEMI primary-PCI cohort, what was the overall no-reflow incidence and how did CHA2DS2-VA discrimination differ between men and women? |
| [q066](#q066) | direct_lookup | What adjusted CHA2DS2-VA associations with no-reflow were reported overall and in women in Sun’s STEMI cohort? |
| [q067](#q067) | direct_lookup | What proportion of Sun’s STEMI primary-PCI cohort developed no-reflow? |
| [q069](#q069) | direct_lookup | Which variable remained independently associated with no-reflow among men in Sun’s study, and what was its adjusted estimate? |
| [q124](#q124) | multi_hop | For CACS in Gao’s derivation cohort, what were the individual-predictor AUC and the multivariable odds ratio for one-year MACE? |
| [q126](#q126) | multi_hop | How was FAI measured in Gao’s CCTA study, and what multivariable MACE odds ratio was reported for it? |
| [q128](#q128) | direct_lookup | In Sun’s male-subgroup regression table, how did hemoglobin’s no-reflow association change after adjustment? |
| [q129](#q129) | cross_doc_distractor | In Sun’s 725-patient STEMI cohort, was pre-existing hypertension significantly more common in patients with no-reflow, and what comparison supports the answer? |
| [c001](#c001) | cross_doc_distractor | In the 2023 ECG study of sample size and class balancing for new-onset AF prediction, what was the CNN AUC at the largest original-ratio training sample, and what event horizon was labelled? |
| [c002](#c002) | multi_hop | How did random undersampling affect calibration in the 2023 ECG future-AF study, and which model had the lowest ICI at the original event ratio? |
| [c003](#c003) | multi_hop | What Lorenz-scattergram-level external AF-detection sensitivity, specificity and accuracy did the Lorenz-plot CNN report, and what limitation applies to its external paroxysmal-AF patient sample? |
| [c004](#c004) | cross_doc_synthesis | How do the AF-management review and primary TAILORED-AF trial report the primary success percentages, and how should their difference be represented? |
| [c005](#c005) | direct_lookup | What procedure-time trade-off did TAILORED-AF report for tailored versus anatomical ablation? |
| [c006](#c006) | cross_doc_distractor | What apparent and true resistant-hypertension prevalence estimates does the Thai consensus give, and what assumption underlies the latter? |
| [c007](#c007) | direct_lookup | What diagnostic checks does the Thai consensus require to exclude pseudoresistance in apparent treatment-resistant hypertension? |
| [c008](#c008) | cross_doc_synthesis | Compare the Thai consensus requirements for confirming resistant hypertension with the BP-phenotype limitation in EMPEROR-Preserved’s resistant-hypertension analysis. |
| [c009](#c009) | cross_doc_distractor | In the Cameroon fourth-line spironolactone trial, what four-week office BP reductions were observed relative to alternative added therapy? |
| [c010](#c010) | cross_doc_synthesis | How do the Cameroon spironolactone trial and EMPEROR-Preserved resHTN analysis differ in added drug, follow-up and reported BP change? |
| [c011](#c011) | cross_doc_distractor | In the geriatric SGLT2 observational study, which oxidative-stress markers changed over follow-up, and what baseline-to-follow-up values were reported? |
| [c012](#c012) | source_conflict | What renal benefit and infection association were reported in the advanced-CKD SGLT2 cohort, and how does its evidential design compare with the HFpEF GLS cohort? |
| [c013](#c013) | source_conflict | What historical price basis and trial sources underlie the HFpEF cost-per-outcome analysis, and what CNTs were reported for its composite outcome? |
| [c014](#c014) | cross_doc_distractor | In the T2D unstable-angina CT-FFR study, what AUCs were reported for per-patient diagnosis and for MACCE prognosis? |
| [c015](#c015) | cross_doc_synthesis | How do the MACE definitions and follow-up in the TyG/CAD-RADS study differ from Gao’s CCTA nomogram study? |
| [c016](#c016) | cross_doc_synthesis | How does the genetic inverse T2D–BP cluster relate to cardiometabolic risk, what environmental limitation do its authors identify, and how does this evidence differ from the advanced-CKD SGLT2 cohort’s renal and infection findings when interpreting drug response? |
| [c017](#c017) | false_premise | How did the HFpEF cost analysis’s direct randomized comparison of dapagliflozin with sacubitril–valsartan establish comprehensive QALY cost-effectiveness? |
| [c018](#c018) | false_premise | Since adding TyG to CAD-RADS 2.0 significantly improved prognostic discrimination, how large was the improvement? |
| [c019](#c019) | false_premise | What randomized head-to-head evidence in the network meta-analysis establishes SGLT2 inhibitors’ superiority over the other drug classes for HFpEF mortality? |
| [c020](#c020) | unanswerable | What was the five-year cardiovascular mortality effect in the Cameroon fourth-line spironolactone randomized trial? |
| [c021](#c021) | unanswerable | What was five-year freedom from AF after a single procedure in the randomized TAILORED-AF cohort? |
| [c022](#c022) | unanswerable | What externally validated ten-year hard-MACE risk does Gao’s CCTA nomogram assign to its original study cohort? |
| [c023](#c023) | cross_doc_distractor | In Rashed’s 150-patient STEMI study, what were the no-reflow AUCs for CHA2DS2-VASc alone and its combination with brachial FMD? |
| [c024](#c024) | false_premise | Since every spironolactone participant in the Cameroon trial achieved office BP below 130/80 mmHg after one month, what supports that universal control claim? |

## q041

**direct_lookup · revision 2 · answerable**

According to the 2026 review of AF management, what AUCs did the cited Attia study report when using one versus multiple sinus-rhythm ECGs to identify a history of paroxysmal AF?

**Expected response**

The review reports AUC 0.87 for one ECG and 0.90 for multiple ECGs, for identifying documented paroxysmal AF history rather than predicting new-onset AF.

**Required claims**

- `f1`: The review reports AUC 0.87 for one ECG and 0.90 for multiple ECGs, for identifying documented paroxysmal AF history rather than predicting new-onset AF.

**Article roles declared by the question**

- Required: [PMC12880197](https://pmc.ncbi.nlm.nih.gov/articles/PMC12880197.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC12880197](https://pmc.ncbi.nlm.nih.gov/articles/PMC12880197.1/) | AI detection; cited Attia 2019 study; p. 2 | `review_attia` |

**Response distinctions to preserve**

- Do not generalize a source-specific estimate to other cohorts, endpoints or timeframes.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## q042

**multi_hop · revision 2 · answerable**

In TAILORED-AF, how was the primary efficacy endpoint defined, and what were its 12-month results in the modified intention-to-treat population?

**Expected response**

The primary endpoint was freedom from documented AF lasting more than 30 seconds after a three-month blanking period, at 12 months after a single procedure, with or without antiarrhythmic drugs. In the mITT population of 357, success was 88% with tailored ablation versus 70% with anatomical ablation; this primary AF outcome must not be substituted for freedom from any atrial arrhythmia.

**Required claims**

- `f1`: The primary endpoint was freedom from documented AF lasting more than 30 seconds after a three-month blanking period, at 12 months after a single procedure, with or without antiarrhythmic drugs.
- `f2`: In the mITT population of 357, success was 88% with tailored ablation versus 70% with anatomical ablation; this primary AF outcome must not be substituted for freedom from any atrial arrhythmia.

**Article roles declared by the question**

- Required: [PMC12003177](https://pmc.ncbi.nlm.nih.gov/articles/PMC12003177.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC12003177](https://pmc.ncbi.nlm.nih.gov/articles/PMC12003177.1/) | Methods; primary endpoint and blanking period; p. 1 | `trial_definition` |
| primary | f1 | [PMC12003177](https://pmc.ncbi.nlm.nih.gov/articles/PMC12003177.1/) | Methods; endpoint duration and blanking period; p. 10 | `trial_definition_full` |
| primary | f2 | [PMC12003177](https://pmc.ncbi.nlm.nih.gov/articles/PMC12003177.1/) | Results; mITT primary efficacy; p. 3 | `trial_primary` |

**Response distinctions to preserve**

- Do not generalize a source-specific estimate to other cohorts, endpoints or timeframes.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## q044

**cross_doc_synthesis · revision 2 · answerable**

How do the review-cited CHA2DS2-VASc thromboembolism discrimination and the Sun STEMI study’s CHA2DS2-VA no-reflow discrimination differ, including the latter’s sex subgroups?

**Expected response**

The stroke-risk review cites a CHA2DS2-VASc c-statistic of 0.578 for thromboembolism. The CHA2DS2-VA no-reflow study reports AUC 0.613 overall, 0.569 in men (P=0.099), and 0.673 in women (P=0.002). The score variants, populations and outcomes differ; these are not interchangeable validations.

**Required claims**

- `f1`: The stroke-risk review cites a CHA2DS2-VASc c-statistic of 0.578 for thromboembolism.
- `f2`: The CHA2DS2-VA no-reflow study reports AUC 0.613 overall, 0.569 in men (P=0.099), and 0.673 in women (P=0.002). The score variants, populations and outcomes differ; these are not interchangeable validations.

**Article roles declared by the question**

- Required: [PMC10607686](https://pmc.ncbi.nlm.nih.gov/articles/PMC10607686.1/), [PMC13439631](https://pmc.ncbi.nlm.nih.gov/articles/PMC13439631.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC10607686](https://pmc.ncbi.nlm.nih.gov/articles/PMC10607686.1/) | Section 6; cited thromboembolism discrimination; p. 11 | `stroke_cstat` |
| primary | f2 | [PMC13439631](https://pmc.ncbi.nlm.nih.gov/articles/PMC13439631.1/) | Results 3.4; overall ROC; p. 3 | `nrp_auc_overall` |
| primary | f2 | [PMC13439631](https://pmc.ncbi.nlm.nih.gov/articles/PMC13439631.1/) | Results 3.4; sex-stratified ROC; p. 3, 4 | `nrp_auc_sex` |

**Response distinctions to preserve**

- Do not treat CHA2DS2-VASc and CHA2DS2-VA as the same score or assert a universal score ceiling.

**Overlap review:** 53 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## q047

**direct_lookup · revision 2 · answerable**

In Gao’s CCTA derivation cohort, how did the combined nomogram’s AUC compare with the strongest individual imaging predictor?

**Expected response**

The combined model AUC was 0.936; plaque length was the strongest individual predictor by AUC, at 0.823.

**Required claims**

- `f1`: The combined model AUC was 0.936; plaque length was the strongest individual predictor by AUC, at 0.823.

**Article roles declared by the question**

- Required: [PMC13433181](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433181.1/)
- Alternatives: [PMC13433181](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433181.1/)
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC13433181](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433181.1/) | Results; Table 5, combined model; p. 7 | `ccta_auc` |
| primary | f1 | [PMC13433181](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433181.1/) | Results; Table 5, plaque length; p. 7 | `ccta_plaque_auc` |
| abstract_same_estimates | f1 | [PMC13433181](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433181.1/) | Abstract; derivation discrimination; p. 1 | `ccta_abstract_auc` |

**Response distinctions to preserve**

- Do not generalize a source-specific estimate to other cohorts, endpoints or timeframes.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## q048

**multi_hop · revision 2 · answerable**

What external discrimination and calibration results did Gao’s CCTA nomogram report, and why might lower-risk outpatient settings still need recalibration?

**Expected response**

External AUC was 0.932 and Hosmer–Lemeshow P=0.382. The external cohort had higher MACE incidence (31.6% versus 16.4%) and greater comorbidity burden, reflecting tertiary referrals; the discussion says lower-risk outpatient application may require recalibration.

**Required claims**

- `f1`: External AUC was 0.932 and Hosmer–Lemeshow P=0.382.
- `f2`: The external cohort had higher MACE incidence (31.6% versus 16.4%) and greater comorbidity burden, reflecting tertiary referrals; the discussion says lower-risk outpatient application may require recalibration.

**Article roles declared by the question**

- Required: [PMC13433181](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433181.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC13433181](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433181.1/) | Results; external validation / Table 7; p. 9 | `ccta_external_auc` |
| primary | f1 | [PMC13433181](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433181.1/) | Results; external calibration; p. 10 | `ccta_external_calibration` |
| primary | f2 | [PMC13433181](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433181.1/) | Discussion; limitations; p. 12 | `ccta_risk_shift` |

**Response distinctions to preserve**

- Do not generalize a source-specific estimate to other cohorts, endpoints or timeframes.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## q049

**direct_lookup · revision 2 · answerable**

Which CCTA variables does Gao’s conclusion identify as independent MACE risk factors, and which variable is protective?

**Expected response**

The conclusion lists stenosis severity, lesion length, fibrous plaque volume, plaque burden, CACS, FAI and MAS as independent risk factors, and larger MLA as protective.

**Required claims**

- `f1`: The conclusion lists stenosis severity, lesion length, fibrous plaque volume, plaque burden, CACS, FAI and MAS as independent risk factors, and larger MLA as protective.

**Article roles declared by the question**

- Required: [PMC13433181](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433181.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC13433181](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433181.1/) | Conclusions; multivariable predictor summary; p. 12 | `ccta_predictors` |

**Response distinctions to preserve**

- Do not reinterpret observational associations as causal effects or silently correct inconsistent coefficient/OR rows.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## q050

**cross_doc_synthesis · revision 2 · answerable**

Compare the combined-model discrimination reported by Gao’s CCTA MACE study and Sun’s CHA2DS2-VA no-reflow study, including the latter’s male subgroup. Why are these different prediction tasks?

**Expected response**

Gao reports combined AUC 0.936 for one-year MACE. Sun reports combined-model AUC 0.689 overall and 0.721 in men for post-PCI no-reflow; neither is the CCTA MACE AUC. Different cohorts and endpoints preclude a direct performance ranking.

**Required claims**

- `f1`: Gao reports combined AUC 0.936 for one-year MACE.
- `f2`: Sun reports combined-model AUC 0.689 overall and 0.721 in men for post-PCI no-reflow; neither is the CCTA MACE AUC. Different cohorts and endpoints preclude a direct performance ranking.

**Article roles declared by the question**

- Required: [PMC13433181](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433181.1/), [PMC13439631](https://pmc.ncbi.nlm.nih.gov/articles/PMC13439631.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC13433181](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433181.1/) | Results; Table 5, combined model; p. 7 | `ccta_auc` |
| primary | f2 | [PMC13439631](https://pmc.ncbi.nlm.nih.gov/articles/PMC13439631.1/) | Results 3.4; combined models and sex subgroups; p. 4 | `nrp_combined` |

**Response distinctions to preserve**

- Do not accept the legacy premise that both combined models exceeded 0.93.

**Overlap review:** 53 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## q051

**multi_hop · revision 2 · answerable**

Which derivation sample-size statements appear in Gao’s CCTA paper, and how does the discussion frame its reported events-per-variable ratio?

**Expected response**

The results describe 280 patients and 46 MACE events, while the discussion calls the cohort n=131. The paper does not establish that 131 is a defined subset of 280; retain the unresolved inconsistency. The limitations report EPV approximately 3.3 from 46 events/14 variables and warn of overfitting; this is proof-of-concept evidence requiring larger multicentre validation.

**Required claims**

- `f1`: The results describe 280 patients and 46 MACE events, while the discussion calls the cohort n=131. The paper does not establish that 131 is a defined subset of 280; retain the unresolved inconsistency.
- `f2`: The limitations report EPV approximately 3.3 from 46 events/14 variables and warn of overfitting; this is proof-of-concept evidence requiring larger multicentre validation.

**Article roles declared by the question**

- Required: [PMC13433181](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433181.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC13433181](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433181.1/) | Results; one-year incidence; p. 4 | `ccta_incidence` |
| primary | f1 | [PMC13433181](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433181.1/) | Discussion; proof-of-concept and EPV; p. 10 | `ccta_131` |
| primary | f2 | [PMC13433181](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433181.1/) | Discussion; limitations / reported EPV; p. 12 | `ccta_limit` |

**Response distinctions to preserve**

- Do not assert that n=131 is an imaging subgroup or complete-case subset of n=280.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## q053

**direct_lookup · revision 2 · answerable**

What six-month GLS changes did the retrospective HFpEF biomarker study report for SGLT2 inhibitor users and controls?

**Expected response**

Reported GLS change was −2.49 percentage points in users versus −0.44 in controls (between-group P<0.001); baseline/follow-up group means in the same passage are −16.08% and −18.57% for users.

**Required claims**

- `f1`: Reported GLS change was −2.49 percentage points in users versus −0.44 in controls (between-group P<0.001); baseline/follow-up group means in the same passage are −16.08% and −18.57% for users.

**Article roles declared by the question**

- Required: [PMC13433862](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433862.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC13433862](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433862.1/) | Results; six-month GLS change; p. 4 | `hf_gls` |

**Response distinctions to preserve**

- Do not generalize a source-specific estimate to other cohorts, endpoints or timeframes.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## q054

**direct_lookup · revision 2 · answerable**

At the reported follow-up, what HF rehospitalization proportions and counts were observed in the HFpEF SGLT2 biomarker cohort?

**Expected response**

Over median 12-month follow-up, HF rehospitalization was 24.7% (23/93) in users versus 55.4% (51/92) in controls, P<0.001. These are observational group comparisons.

**Required claims**

- `f1`: Over median 12-month follow-up, HF rehospitalization was 24.7% (23/93) in users versus 55.4% (51/92) in controls, P<0.001. These are observational group comparisons.

**Article roles declared by the question**

- Required: [PMC13433862](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433862.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC13433862](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433862.1/) | Results; median 12-month HF rehospitalization; p. 4 | `hf_readmission` |

**Response distinctions to preserve**

- Do not generalize a source-specific estimate to other cohorts, endpoints or timeframes.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## q055

**direct_lookup · revision 2 · answerable**

How does the HFpEF biomarker study’s aggregate GLS–PIIINP correlation compare with its within-treatment-group correlations, and what inference does that support?

**Expected response**

Across all patients r=0.554 (P<0.001), but r=0.013 (P=0.896) in users and r=−0.099 (P=0.365) in controls. The aggregate association is largely driven by group differences and does not demonstrate an individual within-group linear relationship.

**Required claims**

- `f1`: Across all patients r=0.554 (P<0.001), but r=0.013 (P=0.896) in users and r=−0.099 (P=0.365) in controls. The aggregate association is largely driven by group differences and does not demonstrate an individual within-group linear relationship.

**Article roles declared by the question**

- Required: [PMC13433862](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433862.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC13433862](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433862.1/) | Results; correlation paragraph / Table 4; p. 5 | `hf_correlation` |

**Response distinctions to preserve**

- Do not generalize a source-specific estimate to other cohorts, endpoints or timeframes.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## q056

**direct_lookup · revision 2 · answerable**

What six-month reductions in NT-proBNP, PIIINP and GDF-15 were reported in the HFpEF SGLT2 biomarker study, compared with controls?

**Expected response**

NT-proBNP reduction was 30.4% versus 9.7%, PIIINP 15.1% versus 5.8%, and GDF-15 20.5% versus 8.6%, all between-group P<0.001.

**Required claims**

- `f1`: NT-proBNP reduction was 30.4% versus 9.7%, PIIINP 15.1% versus 5.8%, and GDF-15 20.5% versus 8.6%, all between-group P<0.001.

**Article roles declared by the question**

- Required: [PMC13433862](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433862.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC13433862](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433862.1/) | Results; six-month biomarker changes / Table 3; p. 4 | `hf_ntprobnp` |
| primary | f1 | [PMC13433862](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433862.1/) | Results; GDF-15 / Table 3; p. 4 | `hf_gdf` |

**Response distinctions to preserve**

- Do not generalize a source-specific estimate to other cohorts, endpoints or timeframes.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## q058

**direct_lookup · revision 3 · answerable**

What did the HFpEF SGLT2 biomarker study report about interaction by diabetes status, and does that establish independence from glycemic changes?

**Expected response**

The study reported no significant diabetes-status interaction (all interaction P values >0.05) for ΔGLS, ΔE/e’, ΔLAVI, ΔNT-proBNP and ΔPIIINP. Lack of detected diabetes-status interaction does not establish independence from glycemic change or causal mediation.

**Required claims**

- `f1`: The study reported no significant diabetes-status interaction (all interaction P values >0.05) for ΔGLS, ΔE/e’, ΔLAVI, ΔNT-proBNP and ΔPIIINP. Lack of detected diabetes-status interaction does not establish independence from glycemic change or causal mediation.

**Article roles declared by the question**

- Required: [PMC13433862](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433862.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC13433862](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433862.1/) | Results; diabetes status interaction / Table 6; p. 5 | `hf_subgroups` |

**Response distinctions to preserve**

- Do not equate absence of diabetes-status interaction with proof of glycemic independence.
- Do not extend the interaction finding to GDF-15 or HF rehospitalization, which have no reported diabetes-status interaction result.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## q065

**multi_hop · revision 2 · answerable**

In Sun’s STEMI primary-PCI cohort, what was the overall no-reflow incidence and how did CHA2DS2-VA discrimination differ between men and women?

**Expected response**

Overall no-reflow incidence was 11.7% (85/725). Score AUC was 0.569 in men (P=0.099) and 0.673 in women (P=0.002), with female sensitivity 78.1% and specificity 47.6%.

**Required claims**

- `f1`: Overall no-reflow incidence was 11.7% (85/725).
- `f2`: Score AUC was 0.569 in men (P=0.099) and 0.673 in women (P=0.002), with female sensitivity 78.1% and specificity 47.6%.

**Article roles declared by the question**

- Required: [PMC13439631](https://pmc.ncbi.nlm.nih.gov/articles/PMC13439631.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC13439631](https://pmc.ncbi.nlm.nih.gov/articles/PMC13439631.1/) | Results 3.2; incidence; p. 3 | `nrp_incidence` |
| primary | f2 | [PMC13439631](https://pmc.ncbi.nlm.nih.gov/articles/PMC13439631.1/) | Results 3.4; sex-stratified ROC; p. 3, 4 | `nrp_auc_sex` |

**Response distinctions to preserve**

- Do not generalize a source-specific estimate to other cohorts, endpoints or timeframes.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## q066

**direct_lookup · revision 2 · answerable**

What adjusted CHA2DS2-VA associations with no-reflow were reported overall and in women in Sun’s STEMI cohort?

**Expected response**

Overall adjusted OR was 1.295 (95% CI 1.098–1.527; P=0.002). In women, adjusted OR was 1.597 (95% CI 1.187–2.149; P=0.002).

**Required claims**

- `f1`: Overall adjusted OR was 1.295 (95% CI 1.098–1.527; P=0.002).
- `f2`: In women, adjusted OR was 1.597 (95% CI 1.187–2.149; P=0.002).

**Article roles declared by the question**

- Required: [PMC13439631](https://pmc.ncbi.nlm.nih.gov/articles/PMC13439631.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC13439631](https://pmc.ncbi.nlm.nih.gov/articles/PMC13439631.1/) | Results 3.3; overall adjusted CV score; p. 3 | `nrp_adjusted` |
| primary | f2 | [PMC13439631](https://pmc.ncbi.nlm.nih.gov/articles/PMC13439631.1/) | Results 3.3; female adjusted CV score; p. 3 | `nrp_female_adjusted` |

**Response distinctions to preserve**

- Do not generalize a source-specific estimate to other cohorts, endpoints or timeframes.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## q067

**direct_lookup · revision 2 · answerable**

What proportion of Sun’s STEMI primary-PCI cohort developed no-reflow?

**Expected response**

85 of 725 patients developed no-reflow, or 11.7%.

**Required claims**

- `f1`: 85 of 725 patients developed no-reflow, or 11.7%.

**Article roles declared by the question**

- Required: [PMC13439631](https://pmc.ncbi.nlm.nih.gov/articles/PMC13439631.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC13439631](https://pmc.ncbi.nlm.nih.gov/articles/PMC13439631.1/) | Results 3.2; incidence; p. 3 | `nrp_incidence` |

**Response distinctions to preserve**

- Do not generalize a source-specific estimate to other cohorts, endpoints or timeframes.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## q069

**direct_lookup · revision 2 · answerable**

Which variable remained independently associated with no-reflow among men in Sun’s study, and what was its adjusted estimate?

**Expected response**

Only platelet count remained an independent predictor among men: adjusted OR 0.993, 95% CI 0.987–0.999, P=0.033; the CHA2DS2-VA score was not independently associated.

**Required claims**

- `f1`: Only platelet count remained an independent predictor among men: adjusted OR 0.993, 95% CI 0.987–0.999, P=0.033; the CHA2DS2-VA score was not independently associated.

**Article roles declared by the question**

- Required: [PMC13439631](https://pmc.ncbi.nlm.nih.gov/articles/PMC13439631.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC13439631](https://pmc.ncbi.nlm.nih.gov/articles/PMC13439631.1/) | Results 3.3; male adjusted platelet predictor; p. 3 | `nrp_male_platelets` |

**Response distinctions to preserve**

- Do not generalize a source-specific estimate to other cohorts, endpoints or timeframes.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## q124

**multi_hop · revision 2 · answerable**

For CACS in Gao’s derivation cohort, what were the individual-predictor AUC and the multivariable odds ratio for one-year MACE?

**Expected response**

CACS individual AUC was 0.808. Table 4 reports adjusted OR 2.563 (95% CI 1.273–3.852; P=0.025).

**Required claims**

- `f1`: CACS individual AUC was 0.808.
- `f2`: Table 4 reports adjusted OR 2.563 (95% CI 1.273–3.852; P=0.025).

**Article roles declared by the question**

- Required: [PMC13433181](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433181.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC13433181](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433181.1/) | Table 5; CACS AUC; p. 7 | `ccta_cacs_auc` |
| primary | f2 | [PMC13433181](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433181.1/) | Table 4; column bindings; p. 6 | `ccta_table4_header` |
| primary | f2 | [PMC13433181](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433181.1/) | Table 4; adjusted CACS row; p. 6 | `ccta_cacs_adjusted` |

**Response distinctions to preserve**

- Do not generalize a source-specific estimate to other cohorts, endpoints or timeframes.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## q126

**multi_hop · revision 2 · answerable**

How was FAI measured in Gao’s CCTA study, and what multivariable MACE odds ratio was reported for it?

**Expected response**

FAI was measured using Syngo.via software (VB30). Table 4 reports FAI OR 7.501 (95% CI 1.785–12.348; P<0.001).

**Required claims**

- `f1`: FAI was measured using Syngo.via software (VB30).
- `f2`: Table 4 reports FAI OR 7.501 (95% CI 1.785–12.348; P<0.001).

**Article roles declared by the question**

- Required: [PMC13433181](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433181.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC13433181](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433181.1/) | Methods; FAI measurement; p. 3 | `ccta_fai_method` |
| primary | f2 | [PMC13433181](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433181.1/) | Table 4; column bindings; p. 6 | `ccta_table4_header` |
| primary | f2 | [PMC13433181](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433181.1/) | Table 4; adjusted FAI row; p. 6 | `ccta_fai_adjusted` |

**Response distinctions to preserve**

- Do not generalize a source-specific estimate to other cohorts, endpoints or timeframes.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## q128

**direct_lookup · revision 2 · answerable**

In Sun’s male-subgroup regression table, how did hemoglobin’s no-reflow association change after adjustment?

**Expected response**

Hemoglobin had unadjusted OR 0.977 (95% CI 0.960–0.994; P=0.008), but adjusted OR 0.990 (95% CI 0.970–1.010; P=0.318), so its unadjusted significance did not persist.

**Required claims**

- `f1`: Hemoglobin had unadjusted OR 0.977 (95% CI 0.960–0.994; P=0.008), but adjusted OR 0.990 (95% CI 0.970–1.010; P=0.318), so its unadjusted significance did not persist.

**Article roles declared by the question**

- Required: [PMC13439631](https://pmc.ncbi.nlm.nih.gov/articles/PMC13439631.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC13439631](https://pmc.ncbi.nlm.nih.gov/articles/PMC13439631.1/) | Table 6; male logistic regression header; p. 9 | `nrp_male_candidates` |
| primary | f1 | [PMC13439631](https://pmc.ncbi.nlm.nih.gov/articles/PMC13439631.1/) | Table 6; male unadjusted/adjusted hemoglobin, platelet and lymphocyte rows; p. 9 | `nrp_male_hemoglobin` |

**Response distinctions to preserve**

- Do not generalize a source-specific estimate to other cohorts, endpoints or timeframes.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## q129

**cross_doc_distractor · revision 2 · answerable**

In Sun’s 725-patient STEMI cohort, was pre-existing hypertension significantly more common in patients with no-reflow, and what comparison supports the answer?

**Expected response**

Hypertension was present in 52.7% (337/640) with normal reflow and 56.5% (48/85) with no-reflow, P=0.508; this unadjusted difference was not significant.

**Required claims**

- `f1`: Hypertension was present in 52.7% (337/640) with normal reflow and 56.5% (48/85) with no-reflow, P=0.508; this unadjusted difference was not significant.

**Article roles declared by the question**

- Required: [PMC13439631](https://pmc.ncbi.nlm.nih.gov/articles/PMC13439631.1/)
- Alternatives: None recorded.
- Decoys: [PMC8866621](https://pmc.ncbi.nlm.nih.gov/articles/PMC8866621.1/)

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC13439631](https://pmc.ncbi.nlm.nih.gov/articles/PMC13439631.1/) | Table 3; flow-group column bindings; p. 6 | `nrp_table3_header` |
| primary | f1 | [PMC13439631](https://pmc.ncbi.nlm.nih.gov/articles/PMC13439631.1/) | Table 3; hypertension by flow group; p. 6 | `nrp_hypertension` |

**Why the distractors matter**

- [PMC8866621](https://pmc.ncbi.nlm.nih.gov/articles/PMC8866621.1/) — Another STEMI/no-reflow cohort reports significant hypertension association.
  Rashed’s 150-patient cohort is not Sun’s 725-patient cohort; its result cannot supply this comparison.
  Passage: Results; unadjusted hypertension comparison; PDF p. 1; anchor `vasc_hypertension`.

**Response distinctions to preserve**

- Do not generalize a source-specific estimate to other cohorts, endpoints or timeframes.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## c001

**cross_doc_distractor · revision 1 · answerable**

In the 2023 ECG study of sample size and class balancing for new-onset AF prediction, what was the CNN AUC at the largest original-ratio training sample, and what event horizon was labelled?

**Expected response**

The CNN AUC was 0.799 at the largest 150,000-ECG training sample with original event ratio. Each ECG label represented development of AF within five years.

**Required claims**

- `f1`: The CNN AUC was 0.799 at the largest 150,000-ECG training sample with original event ratio.
- `f2`: Each ECG label represented development of AF within five years.

**Article roles declared by the question**

- Required: [PMC10363301](https://pmc.ncbi.nlm.nih.gov/articles/PMC10363301.1/)
- Alternatives: None recorded.
- Decoys: [PMC11265054](https://pmc.ncbi.nlm.nih.gov/articles/PMC11265054.1/), [PMC12436478](https://pmc.ncbi.nlm.nih.gov/articles/PMC12436478.1/)

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC10363301](https://pmc.ncbi.nlm.nih.gov/articles/PMC10363301.1/) | Results; largest unbalanced training sample; p. 5 | `ecg_auc` |
| primary | f2 | [PMC10363301](https://pmc.ncbi.nlm.nih.gov/articles/PMC10363301.1/) | Methods; five-year future-AF label; p. 3 | `ecg_task` |

**Why the distractors matter**

- [PMC11265054](https://pmc.ncbi.nlm.nih.gov/articles/PMC11265054.1/) — High AF detection performance also uses deep learning and ECG.
  Lorenz results detect AF in records, not new AF over five years.
  Passage: Results; internal/external episode detection; PDF p. 1; anchor `lorenz_metrics`.
- [PMC12436478](https://pmc.ncbi.nlm.nih.gov/articles/PMC12436478.1/) — AF-related AI model with high AUCs.
  AHRE duration thresholds from echocardiographic inputs are neither this ECG population nor its five-year outcome.
  Passage: Results; AHRE thresholds and test-set performance; PDF p. 6; anchor `ahre_auc`.

**Response distinctions to preserve**

- Do not generalize a source-specific estimate to other cohorts, endpoints or timeframes.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## c002

**multi_hop · revision 1 · answerable**

How did random undersampling affect calibration in the 2023 ECG future-AF study, and which model had the lowest ICI at the original event ratio?

**Expected response**

At the original event ratio XGB had the lowest ICI, 0.008. Increasing the positive-sample ratio using random undersampling increased ICI, worsening calibration, especially for XGB and logistic regression; discrimination and calibration must be assessed separately.

**Required claims**

- `f1`: At the original event ratio XGB had the lowest ICI, 0.008.
- `f2`: Increasing the positive-sample ratio using random undersampling increased ICI, worsening calibration, especially for XGB and logistic regression; discrimination and calibration must be assessed separately.

**Article roles declared by the question**

- Required: [PMC10363301](https://pmc.ncbi.nlm.nih.gov/articles/PMC10363301.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC10363301](https://pmc.ncbi.nlm.nih.gov/articles/PMC10363301.1/) | Results; calibration at original event ratio; p. 5 | `ecg_ici` |
| primary | f2 | [PMC10363301](https://pmc.ncbi.nlm.nih.gov/articles/PMC10363301.1/) | Results; random undersampling calibration; p. 6 | `ecg_balancing` |

**Response distinctions to preserve**

- Do not generalize a source-specific estimate to other cohorts, endpoints or timeframes.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## c003

**multi_hop · revision 2 · answerable**

What Lorenz-scattergram-level external AF-detection sensitivity, specificity and accuracy did the Lorenz-plot CNN report, and what limitation applies to its external paroxysmal-AF patient sample?

**Expected response**

External Lorenz-scattergram-level sensitivity, specificity and accuracy were 0.989, 0.956 and 0.967, respectively. The external MS-AF dataset contained only five paroxysmal-AF patients; the authors warn that this small number and proportion may affect test results.

**Required claims**

- `f1`: External Lorenz-scattergram-level sensitivity, specificity and accuracy were 0.989, 0.956 and 0.967, respectively.
- `f2`: The external MS-AF dataset contained only five paroxysmal-AF patients; the authors warn that this small number and proportion may affect test results.

**Article roles declared by the question**

- Required: [PMC11265054](https://pmc.ncbi.nlm.nih.gov/articles/PMC11265054.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC11265054](https://pmc.ncbi.nlm.nih.gov/articles/PMC11265054.1/) | Results; internal/external episode detection; p. 1 | `lorenz_metrics` |
| primary | f2 | [PMC11265054](https://pmc.ncbi.nlm.nih.gov/articles/PMC11265054.1/) | Limitations; external paroxysmal sample; p. 7 | `lorenz_limit` |

**Response distinctions to preserve**

- Do not generalize a source-specific estimate to other cohorts, endpoints or timeframes.
- Do not label scattergram-level estimates as ECG-record-level performance.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## c004

**cross_doc_synthesis · revision 1 · answerable**

How do the AF-management review and primary TAILORED-AF trial report the primary success percentages, and how should their difference be represented?

**Expected response**

The review reports 89% versus 67%. The primary trial’s mITT result reports 88% versus 70% in 357 patients. Preserve attribution and use the primary mITT estimate for a mITT question; do not average or declare the review figures an equivalent alternative.

**Required claims**

- `f1`: The review reports 89% versus 67%.
- `f2`: The primary trial’s mITT result reports 88% versus 70% in 357 patients. Preserve attribution and use the primary mITT estimate for a mITT question; do not average or declare the review figures an equivalent alternative.

**Article roles declared by the question**

- Required: [PMC12003177](https://pmc.ncbi.nlm.nih.gov/articles/PMC12003177.1/), [PMC12880197](https://pmc.ncbi.nlm.nih.gov/articles/PMC12880197.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC12880197](https://pmc.ncbi.nlm.nih.gov/articles/PMC12880197.1/) | AI mapping; review report of TAILORED-AF; p. 6 | `review_tailored` |
| primary | f2 | [PMC12003177](https://pmc.ncbi.nlm.nih.gov/articles/PMC12003177.1/) | Results; mITT primary efficacy; p. 3 | `trial_primary` |

**Response distinctions to preserve**

- Do not generalize a source-specific estimate to other cohorts, endpoints or timeframes.

**Overlap review:** 53 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## c005

**direct_lookup · revision 1 · answerable**

What procedure-time trade-off did TAILORED-AF report for tailored versus anatomical ablation?

**Expected response**

Procedure duration was 178±60 versus 92±36 minutes, and RF time 42±17 versus 20±11 minutes; tailored procedures took longer.

**Required claims**

- `f1`: Procedure duration was 178±60 versus 92±36 minutes, and RF time 42±17 versus 20±11 minutes; tailored procedures took longer.

**Article roles declared by the question**

- Required: [PMC12003177](https://pmc.ncbi.nlm.nih.gov/articles/PMC12003177.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC12003177](https://pmc.ncbi.nlm.nih.gov/articles/PMC12003177.1/) | Results; procedure and RF time; p. 4 | `trial_times` |

**Response distinctions to preserve**

- Do not generalize a source-specific estimate to other cohorts, endpoints or timeframes.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## c006

**cross_doc_distractor · revision 1 · answerable**

What apparent and true resistant-hypertension prevalence estimates does the Thai consensus give, and what assumption underlies the latter?

**Expected response**

Estimated apparent treatment-RH was 5.3% of the treated Thai hypertensive population; estimated true RH was about 3.4%, assuming the reported 33–37% pseudoresistance fraction also applies in Thailand. These are estimates, not a directly measured confirmed-RH survey proportion.

**Required claims**

- `f1`: Estimated apparent treatment-RH was 5.3% of the treated Thai hypertensive population; estimated true RH was about 3.4%, assuming the reported 33–37% pseudoresistance fraction also applies in Thailand. These are estimates, not a directly measured confirmed-RH survey proportion.

**Article roles declared by the question**

- Required: [PMC11374717](https://pmc.ncbi.nlm.nih.gov/articles/PMC11374717.1/)
- Alternatives: None recorded.
- Decoys: [PMC10619268](https://pmc.ncbi.nlm.nih.gov/articles/PMC10619268.1/)

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC11374717](https://pmc.ncbi.nlm.nih.gov/articles/PMC11374717.1/) | Epidemiology; estimated apparent/true RH; p. 3 | `thai_prevalence` |

**Why the distractors matter**

- [PMC10619268](https://pmc.ncbi.nlm.nih.gov/articles/PMC10619268.1/) — RH consensus with nearby prevalence estimates.
  Korean primary-care and tertiary-referral estimates apply to different populations and must not replace Thai estimates.
  Passage: Epidemiology; Korean studies; PDF p. 3; anchor `korean_prevalence`.

**Response distinctions to preserve**

- Do not generalize a source-specific estimate to other cohorts, endpoints or timeframes.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## c007

**direct_lookup · revision 1 · answerable**

What diagnostic checks does the Thai consensus require to exclude pseudoresistance in apparent treatment-resistant hypertension?

**Expected response**

Standardize office BP measurement, confirm adherence, exclude drug/substance-induced RH, and use 24-hour ambulatory BP monitoring (or home monitoring if unavailable) to exclude white-coat effect.

**Required claims**

- `f1`: Standardize office BP measurement, confirm adherence, exclude drug/substance-induced RH, and use 24-hour ambulatory BP monitoring (or home monitoring if unavailable) to exclude white-coat effect.

**Article roles declared by the question**

- Required: [PMC11374717](https://pmc.ncbi.nlm.nih.gov/articles/PMC11374717.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC11374717](https://pmc.ncbi.nlm.nih.gov/articles/PMC11374717.1/) | Evaluation; pseudoresistance exclusion; p. 3 | `thai_workup` |

**Response distinctions to preserve**

- Do not generalize a source-specific estimate to other cohorts, endpoints or timeframes.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## c008

**cross_doc_synthesis · revision 1 · answerable**

Compare the Thai consensus requirements for confirming resistant hypertension with the BP-phenotype limitation in EMPEROR-Preserved’s resistant-hypertension analysis.

**Expected response**

The consensus requires pseudoresistance exclusion, including ambulatory/home measurement to exclude white-coat effect. EMPEROR-Preserved classified resHTN from baseline BP rather than ambulatory/home recordings and could not exclude white-coat hypertension or other pseudoresistance. Its subgroup cannot automatically be called confirmed true RH.

**Required claims**

- `f1`: The consensus requires pseudoresistance exclusion, including ambulatory/home measurement to exclude white-coat effect.
- `f2`: EMPEROR-Preserved classified resHTN from baseline BP rather than ambulatory/home recordings and could not exclude white-coat hypertension or other pseudoresistance. Its subgroup cannot automatically be called confirmed true RH.

**Article roles declared by the question**

- Required: [PMC11374717](https://pmc.ncbi.nlm.nih.gov/articles/PMC11374717.1/), [PMC11973566](https://pmc.ncbi.nlm.nih.gov/articles/PMC11973566.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC11374717](https://pmc.ncbi.nlm.nih.gov/articles/PMC11374717.1/) | Evaluation; pseudoresistance exclusion; p. 3 | `thai_workup` |
| primary | f2 | [PMC11973566](https://pmc.ncbi.nlm.nih.gov/articles/PMC11973566.1/) | Discussion; BP phenotype limitations; p. 12 | `emperor_limit` |

**Response distinctions to preserve**

- Do not generalize a source-specific estimate to other cohorts, endpoints or timeframes.

**Overlap review:** 53 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## c009

**cross_doc_distractor · revision 1 · answerable**

In the Cameroon fourth-line spironolactone trial, what four-week office BP reductions were observed relative to alternative added therapy?

**Expected response**

Office systolic BP fell by 33 versus 14 mmHg (P=0.024) and diastolic BP by 14 versus 5 mmHg (P=0.006).

**Required claims**

- `f1`: Office systolic BP fell by 33 versus 14 mmHg (P=0.024) and diastolic BP by 14 versus 5 mmHg (P=0.006).

**Article roles declared by the question**

- Required: [PMC4804513](https://pmc.ncbi.nlm.nih.gov/articles/PMC4804513.1/)
- Alternatives: None recorded.
- Decoys: [PMC11973566](https://pmc.ncbi.nlm.nih.gov/articles/PMC11973566.1/)

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC4804513](https://pmc.ncbi.nlm.nih.gov/articles/PMC4804513.1/) | Results; four-week office BP reductions; p. 4 | `spirono_results` |

**Why the distractors matter**

- [PMC11973566](https://pmc.ncbi.nlm.nih.gov/articles/PMC11973566.1/) — Another RH-related added-drug BP study.
  Empagliflozin in HF EF>40% at weeks 4–32 is a different drug, cohort and comparison.
  Passage: Results; resistant hypertension SBP weeks 4-32; PDF p. 7; anchor `emperor_bp`.

**Response distinctions to preserve**

- Do not generalize a source-specific estimate to other cohorts, endpoints or timeframes.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## c010

**cross_doc_synthesis · revision 1 · answerable**

How do the Cameroon spironolactone trial and EMPEROR-Preserved resHTN analysis differ in added drug, follow-up and reported BP change?

**Expected response**

Cameroon added spironolactone 25 mg daily and followed visits at two and four weeks; four-week office SBP reductions were 33 versus 14 mmHg. EMPEROR-Preserved randomized HF patients with EF>40% to empagliflozin 10 mg or placebo; resHTN SBP between-treatment differences were 2.4–3.3 mmHg at weeks 4–32, with similar BP later at weeks 52–172. These are not comparable measures of fourth-line efficacy in the same cohort.

**Required claims**

- `f1`: Cameroon added spironolactone 25 mg daily and followed visits at two and four weeks; four-week office SBP reductions were 33 versus 14 mmHg.
- `f2`: EMPEROR-Preserved randomized HF patients with EF>40% to empagliflozin 10 mg or placebo; resHTN SBP between-treatment differences were 2.4–3.3 mmHg at weeks 4–32, with similar BP later at weeks 52–172. These are not comparable measures of fourth-line efficacy in the same cohort.

**Article roles declared by the question**

- Required: [PMC11973566](https://pmc.ncbi.nlm.nih.gov/articles/PMC11973566.1/), [PMC4804513](https://pmc.ncbi.nlm.nih.gov/articles/PMC4804513.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC4804513](https://pmc.ncbi.nlm.nih.gov/articles/PMC4804513.1/) | Methods; trial dose and four-week follow-up; p. 2, 3 | `spirono_design` |
| primary | f1 | [PMC4804513](https://pmc.ncbi.nlm.nih.gov/articles/PMC4804513.1/) | Results; four-week office BP reductions; p. 4 | `spirono_results` |
| primary | f2 | [PMC11973566](https://pmc.ncbi.nlm.nih.gov/articles/PMC11973566.1/) | Methods; EMPEROR-Preserved inclusion; p. 3 | `emperor_definition` |
| primary | f2 | [PMC11973566](https://pmc.ncbi.nlm.nih.gov/articles/PMC11973566.1/) | Results; resistant hypertension SBP weeks 4-32; p. 7 | `emperor_bp` |

**Response distinctions to preserve**

- Do not generalize a source-specific estimate to other cohorts, endpoints or timeframes.

**Overlap review:** 53 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## c011

**cross_doc_distractor · revision 1 · answerable**

In the geriatric SGLT2 observational study, which oxidative-stress markers changed over follow-up, and what baseline-to-follow-up values were reported?

**Expected response**

Nox-2 decreased from 1.24 to 1.01 nmol/L and 8-isoprostane from 70.41 to 65.67 pg/mL, both P<0.0001. These are observational before/after findings.

**Required claims**

- `f1`: Nox-2 decreased from 1.24 to 1.01 nmol/L and 8-isoprostane from 70.41 to 65.67 pg/mL, both P<0.0001. These are observational before/after findings.

**Article roles declared by the question**

- Required: [PMC11354916](https://pmc.ncbi.nlm.nih.gov/articles/PMC11354916.1/)
- Alternatives: None recorded.
- Decoys: [PMC13433862](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433862.1/)

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC11354916](https://pmc.ncbi.nlm.nih.gov/articles/PMC11354916.1/) | Results; six-month oxidative/platelet markers; p. 4 | `geriatric_markers` |

**Why the distractors matter**

- [PMC13433862](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433862.1/) — SGLT2 HFpEF biomarker study over six months.
  GDF-15/fibrosis-marker percentages are different markers and a different cohort, not these oxidative-stress concentrations.
  Passage: Results; GDF-15 / Table 3; PDF p. 4; anchor `hf_gdf`.

**Response distinctions to preserve**

- Do not generalize a source-specific estimate to other cohorts, endpoints or timeframes.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## c012

**source_conflict · revision 2 · answerable**

What renal benefit and infection association were reported in the advanced-CKD SGLT2 cohort, and how does its evidential design compare with the HFpEF GLS cohort?

**Expected response**

The advanced-CKD study’s abstract and Results text report ESRD/dialysis adjusted HR 0.35 (95% CI 0.19–0.67) and GUTI adjusted HR 1.78 (95% CI 1.12–2.84); the authors cannot exclude unmeasured confounding. The HFpEF biomarker study is retrospective observational and reports GLS changes, not these renal or infection endpoints. Neither observational comparison proves a causal treatment effect or supplies the other cohort’s endpoint estimates. Table 2 of the same article reports different adjusted estimates for the same outcomes: ESRD/dialysis 0.35 (95% CI 0.19–0.66) and GUTI 1.80 (95% CI 1.13–2.86). The article does not reconcile the two sets, so both are reported with their source location.

**Required claims**

- `f1`: The advanced-CKD study’s abstract and Results text report ESRD/dialysis adjusted HR 0.35 (95% CI 0.19–0.67) and GUTI adjusted HR 1.78 (95% CI 1.12–2.84); the authors cannot exclude unmeasured confounding.
- `f2`: The HFpEF biomarker study is retrospective observational and reports GLS changes, not these renal or infection endpoints. Neither observational comparison proves a causal treatment effect or supplies the other cohort’s endpoint estimates.
- `f3`: Table 2 of the same article reports different adjusted estimates for the same outcomes: ESRD/dialysis 0.35 (95% CI 0.19–0.66) and GUTI 1.80 (95% CI 1.13–2.86). The article does not reconcile the two sets, so both are reported with their source location.

**Article roles declared by the question**

- Required: [PMC11373557](https://pmc.ncbi.nlm.nih.gov/articles/PMC11373557.1/), [PMC13433862](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433862.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC11373557](https://pmc.ncbi.nlm.nih.gov/articles/PMC11373557.1/) | Results; ESRD/dialysis incidence and adjusted HR; p. 1 | `ckd_renal` |
| primary | f1 | [PMC11373557](https://pmc.ncbi.nlm.nih.gov/articles/PMC11373557.1/) | Results; genitourinary infection incidence and adjusted HR; p. 1 | `ckd_infection` |
| primary | f1 | [PMC11373557](https://pmc.ncbi.nlm.nih.gov/articles/PMC11373557.1/) | Discussion; residual confounding; p. 8 | `ckd_confounding` |
| primary | f2 | [PMC13433862](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433862.1/) | Methods; retrospective case-control design; p. 3 | `hf_observational` |
| primary | f2 | [PMC13433862](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433862.1/) | Results; six-month GLS change; p. 4 | `hf_gls` |
| primary | f3 | [PMC11373557](https://pmc.ncbi.nlm.nih.gov/articles/PMC11373557.1/) | Results; Table 2 adjusted HRs for GUTIs and ESRD + dialysis; p. 6 | `ckd_table2` |

**Response distinctions to preserve**

- Do not generalize a source-specific estimate to other cohorts, endpoints or timeframes.
- Do not report one reading as uncontested, and do not average or merge the two readings.

**Overlap review:** 53 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## c013

**source_conflict · revision 2 · answerable**

What historical price basis and trial sources underlie the HFpEF cost-per-outcome analysis, and what CNTs were reported for its composite outcome?

**Expected response**

The abstract states that costs were based on 2022 US prices, with efficacy data from the DELIVER trial for dapagliflozin and a pooled analysis of PARAGLIDE-HF and PARAGON-HF for sacubitril–valsartan. Annualized cost needed to treat to prevent one total worsening-HF/CV-death composite event was $148,547.13 for dapagliflozin versus $245,346.77 for sacubitril–valsartan. Methods instead describes drug costs as 75% of the US National Average Drug Acquisition Cost (NADAC) extracted in July 2023. The article does not reconcile this with the 2022 price statement, so both are reported with their source location.

**Required claims**

- `f1`: The abstract states that costs were based on 2022 US prices, with efficacy data from the DELIVER trial for dapagliflozin and a pooled analysis of PARAGLIDE-HF and PARAGON-HF for sacubitril–valsartan.
- `f2`: Annualized cost needed to treat to prevent one total worsening-HF/CV-death composite event was $148,547.13 for dapagliflozin versus $245,346.77 for sacubitril–valsartan.
- `f3`: Methods instead describes drug costs as 75% of the US National Average Drug Acquisition Cost (NADAC) extracted in July 2023. The article does not reconcile this with the 2022 price statement, so both are reported with their source location.

**Article roles declared by the question**

- Required: [PMC10985250](https://pmc.ncbi.nlm.nih.gov/articles/PMC10985250.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC10985250](https://pmc.ncbi.nlm.nih.gov/articles/PMC10985250.1/) | Abstract/Methods; historical US price year; p. 1 | `cost_year` |
| primary | f2 | [PMC10985250](https://pmc.ncbi.nlm.nih.gov/articles/PMC10985250.1/) | Results; annualized cost needed to treat; p. 3 | `cost_values` |
| primary | f3 | [PMC10985250](https://pmc.ncbi.nlm.nih.gov/articles/PMC10985250.1/) | Methods; drug cost basis; p. 2 | `cost_methods_nadac` |
| abstract | f1, f2 | [PMC10985250](https://pmc.ncbi.nlm.nih.gov/articles/PMC10985250.1/) | Abstract; Methods and Results; p. 1 | `cost_abstract_complete` |
| abstract | f3 | [PMC10985250](https://pmc.ncbi.nlm.nih.gov/articles/PMC10985250.1/) | Methods; drug cost basis; p. 2 | `cost_methods_nadac` |

**Response distinctions to preserve**

- Do not generalize a source-specific estimate to other cohorts, endpoints or timeframes.
- Do not report one reading as uncontested, and do not average or merge the two readings.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## c014

**cross_doc_distractor · revision 1 · answerable**

In the T2D unstable-angina CT-FFR study, what AUCs were reported for per-patient diagnosis and for MACCE prognosis?

**Expected response**

Per-patient diagnostic AUC was 84.8% (0.848), whereas the MACCE prognostic AUC was 0.938. These are different endpoints, not alternative estimates of one task.

**Required claims**

- `f1`: Per-patient diagnostic AUC was 84.8% (0.848), whereas the MACCE prognostic AUC was 0.938. These are different endpoints, not alternative estimates of one task.

**Article roles declared by the question**

- Required: [PMC11549774](https://pmc.ncbi.nlm.nih.gov/articles/PMC11549774.1/)
- Alternatives: None recorded.
- Decoys: [PMC13433181](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433181.1/)

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC11549774](https://pmc.ncbi.nlm.nih.gov/articles/PMC11549774.1/) | Results; per-patient diagnostic performance vs invasive FFR; p. 1 | `ctffr_diagnostic` |
| primary | f1 | [PMC11549774](https://pmc.ncbi.nlm.nih.gov/articles/PMC11549774.1/) | Results; three-year MACCE prognostic ROC; p. 9 | `ctffr_prognostic` |

**Why the distractors matter**

- [PMC13433181](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433181.1/) — CCTA-based combined model with nearby AUC.
  Gao’s combined one-year MACE model does not report this CT-FFR diagnostic or three-year MACCE AUC.
  Passage: Results; Table 5, combined model; PDF p. 7; anchor `ccta_auc`.

**Response distinctions to preserve**

- Do not generalize a source-specific estimate to other cohorts, endpoints or timeframes.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## c015

**cross_doc_synthesis · revision 1 · answerable**

How do the MACE definitions and follow-up in the TyG/CAD-RADS study differ from Gao’s CCTA nomogram study?

**Expected response**

TyG study MACE comprises MI, all-cause mortality and stroke; median follow-up was 50.4 months, with 212 events (6.0%). Gao defines one-year MACE as cardiac death, nonfatal MI, revascularization for unstable angina, or rehospitalization for unstable angina. These composites and horizons differ.

**Required claims**

- `f1`: TyG study MACE comprises MI, all-cause mortality and stroke; median follow-up was 50.4 months, with 212 events (6.0%).
- `f2`: Gao defines one-year MACE as cardiac death, nonfatal MI, revascularization for unstable angina, or rehospitalization for unstable angina. These composites and horizons differ.

**Article roles declared by the question**

- Required: [PMC11514186](https://pmc.ncbi.nlm.nih.gov/articles/PMC11514186.1/), [PMC13433181](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433181.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC11514186](https://pmc.ncbi.nlm.nih.gov/articles/PMC11514186.1/) | Follow up; hard-endpoint MACE; p. 2 | `tyg_definition` |
| primary | f1 | [PMC11514186](https://pmc.ncbi.nlm.nih.gov/articles/PMC11514186.1/) | Association between TyG and MACE; follow-up; p. 1 | `tyg_followup` |
| primary | f2 | [PMC13433181](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433181.1/) | Methods; endpoint definition; p. 3 | `ccta_endpoints` |

**Response distinctions to preserve**

- Do not generalize a source-specific estimate to other cohorts, endpoints or timeframes.

**Overlap review:** 53 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## c016

**cross_doc_synthesis · revision 2 · answerable**

How does the genetic inverse T2D–BP cluster relate to cardiometabolic risk, what environmental limitation do its authors identify, and how does this evidence differ from the advanced-CKD SGLT2 cohort’s renal and infection findings when interpreting drug response?

**Expected response**

The inverse cluster has 353 SNVs whose T2D-risk alleles associate with lower BP and lower AF, CAD, stroke and HF risk; it represents genetic associations. The genetic study’s authors state that environmental factors also influence T2D/high-BP mechanisms. The advanced-CKD SGLT2 cohort instead reports treatment-exposure associations with renal and infection outcomes; these different analyses do not establish that the inverse genetic cluster predicts SGLT2 response.

**Required claims**

- `f1`: The inverse cluster has 353 SNVs whose T2D-risk alleles associate with lower BP and lower AF, CAD, stroke and HF risk; it represents genetic associations.
- `f2`: The genetic study’s authors state that environmental factors also influence T2D/high-BP mechanisms. The advanced-CKD SGLT2 cohort instead reports treatment-exposure associations with renal and infection outcomes; these different analyses do not establish that the inverse genetic cluster predicts SGLT2 response.

**Article roles declared by the question**

- Required: [PMC11373557](https://pmc.ncbi.nlm.nih.gov/articles/PMC11373557.1/), [PMC12886974](https://pmc.ncbi.nlm.nih.gov/articles/PMC12886974.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC12886974](https://pmc.ncbi.nlm.nih.gov/articles/PMC12886974.1/) | Results; inverse T2D-BP cluster; p. 3 | `pgs_inverse` |
| primary | f2 | [PMC12886974](https://pmc.ncbi.nlm.nih.gov/articles/PMC12886974.1/) | Discussion; environmental and external factors; p. 8 | `pgs_caveat` |
| primary | f2 | [PMC11373557](https://pmc.ncbi.nlm.nih.gov/articles/PMC11373557.1/) | Results; ESRD/dialysis incidence and adjusted HR; p. 1 | `ckd_renal` |
| primary | f2 | [PMC11373557](https://pmc.ncbi.nlm.nih.gov/articles/PMC11373557.1/) | Results; genitourinary infection incidence and adjusted HR; p. 1 | `ckd_infection` |

**Response distinctions to preserve**

- Do not generalize a source-specific estimate to other cohorts, endpoints or timeframes.

**Overlap review:** 53 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## c017

**false_premise · revision 1 · false_premise**

How did the HFpEF cost analysis’s direct randomized comparison of dapagliflozin with sacubitril–valsartan establish comprehensive QALY cost-effectiveness?

**Expected response**

The analysis used separate DELIVER and pooled PARAGLIDE-HF/PARAGON-HF data, not a direct randomized drug-to-drug comparison. The authors explicitly say the CNT analysis does not substitute for comprehensive cost-effectiveness assessment in relation to QALY and hospitalization cost savings.

**Required claims**

- `f1`: The analysis used separate DELIVER and pooled PARAGLIDE-HF/PARAGON-HF data, not a direct randomized drug-to-drug comparison.
- `f2`: The authors explicitly say the CNT analysis does not substitute for comprehensive cost-effectiveness assessment in relation to QALY and hospitalization cost savings.

**Article roles declared by the question**

- Required: [PMC10985250](https://pmc.ncbi.nlm.nih.gov/articles/PMC10985250.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC10985250](https://pmc.ncbi.nlm.nih.gov/articles/PMC10985250.1/) | Abstract/Methods; historical US price year; p. 1 | `cost_year` |
| primary | f2 | [PMC10985250](https://pmc.ncbi.nlm.nih.gov/articles/PMC10985250.1/) | Discussion; incomplete cost-effectiveness assessment; p. 6 | `cost_limitation` |

**Response distinctions to preserve**

- Do not answer as though a head-to-head RCT or comprehensive QALY model was conducted.

**Premise to correct:** Direct head-to-head randomization and comprehensive QALY assessment were performed.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## c018

**false_premise · revision 1 · false_premise**

Since adding TyG to CAD-RADS 2.0 significantly improved prognostic discrimination, how large was the improvement?

**Expected response**

The premise is contradicted by the source: C-statistic rose from 0.731 to 0.733 but not significantly (P=0.505). Independent risk association did not establish incremental prognostic benefit.

**Required claims**

- `f1`: The premise is contradicted by the source: C-statistic rose from 0.731 to 0.733 but not significantly (P=0.505). Independent risk association did not establish incremental prognostic benefit.

**Article roles declared by the question**

- Required: [PMC11514186](https://pmc.ncbi.nlm.nih.gov/articles/PMC11514186.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC11514186](https://pmc.ncbi.nlm.nih.gov/articles/PMC11514186.1/) | Results; incremental C-statistic comparisons; p. 4 | `tyg_increment_values` |
| primary | f1 | [PMC11514186](https://pmc.ncbi.nlm.nih.gov/articles/PMC11514186.1/) | Results; incremental prediction; p. 4 | `tyg_increment` |

**Response distinctions to preserve**

- Do not generalize a source-specific estimate to other cohorts, endpoints or timeframes.

**Premise to correct:** The incremental discrimination improvement was statistically significant.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## c019

**false_premise · revision 1 · false_premise**

What randomized head-to-head evidence in the network meta-analysis establishes SGLT2 inhibitors’ superiority over the other drug classes for HFpEF mortality?

**Expected response**

Comparisons were indirect, using placebo as the common comparator; all included trials were placebo-controlled. The HFpEF NMA found no significant class differences for CV mortality, all-cause mortality or HF hospitalization/event. Absence of significance is not equivalence, and no head-to-head superiority is established.

**Required claims**

- `f1`: Comparisons were indirect, using placebo as the common comparator; all included trials were placebo-controlled.
- `f2`: The HFpEF NMA found no significant class differences for CV mortality, all-cause mortality or HF hospitalization/event. Absence of significance is not equivalence, and no head-to-head superiority is established.

**Article roles declared by the question**

- Required: [PMC12683810](https://pmc.ncbi.nlm.nih.gov/articles/PMC12683810.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC12683810](https://pmc.ncbi.nlm.nih.gov/articles/PMC12683810.1/) | Methods; placebo-anchored indirect comparisons; p. 3 | `nma_indirect` |
| primary | f2 | [PMC12683810](https://pmc.ncbi.nlm.nih.gov/articles/PMC12683810.1/) | Results; indirect HFpEF class comparisons; p. 9 | `nma_hfpef` |

**Response distinctions to preserve**

- Do not infer equivalence from nonsignificance or transfer CKD/ASCVD findings to HFpEF.

**Premise to correct:** Randomized head-to-head evidence established mortality superiority in HFpEF.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## c020

**unanswerable · revision 1 · absent_fact**

What was the five-year cardiovascular mortality effect in the Cameroon fourth-line spironolactone randomized trial?

**Expected response**

The specified fact is not reported in the pinned selected corpus; state the evidence limit without inventing an estimate.

**Article roles declared by the question**

- Required: None recorded.
- Alternatives: None recorded.
- Decoys: None recorded.

**Evidence:** No positive answer-evidence set is defined. See the
expected refusal and the recorded search scope below.

**Response distinctions to preserve**

- Do not substitute another cohort’s or shorter-horizon result for this absent fact.

**Missing-fact search scope**

The selected trial reports four-week BP outcomes; no selected paper supplies five-year mortality results for these randomized participants.

[PMC10363301](https://pmc.ncbi.nlm.nih.gov/articles/PMC10363301.1/), [PMC10607686](https://pmc.ncbi.nlm.nih.gov/articles/PMC10607686.1/), [PMC10619268](https://pmc.ncbi.nlm.nih.gov/articles/PMC10619268.1/), [PMC10985250](https://pmc.ncbi.nlm.nih.gov/articles/PMC10985250.1/), [PMC11265054](https://pmc.ncbi.nlm.nih.gov/articles/PMC11265054.1/), [PMC11354916](https://pmc.ncbi.nlm.nih.gov/articles/PMC11354916.1/), [PMC11373557](https://pmc.ncbi.nlm.nih.gov/articles/PMC11373557.1/), [PMC11374717](https://pmc.ncbi.nlm.nih.gov/articles/PMC11374717.1/), [PMC11514186](https://pmc.ncbi.nlm.nih.gov/articles/PMC11514186.1/), [PMC11549774](https://pmc.ncbi.nlm.nih.gov/articles/PMC11549774.1/), [PMC11973566](https://pmc.ncbi.nlm.nih.gov/articles/PMC11973566.1/), [PMC12003177](https://pmc.ncbi.nlm.nih.gov/articles/PMC12003177.1/), [PMC12436478](https://pmc.ncbi.nlm.nih.gov/articles/PMC12436478.1/), [PMC12683810](https://pmc.ncbi.nlm.nih.gov/articles/PMC12683810.1/), [PMC12880197](https://pmc.ncbi.nlm.nih.gov/articles/PMC12880197.1/), [PMC12886974](https://pmc.ncbi.nlm.nih.gov/articles/PMC12886974.1/), [PMC13433181](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433181.1/), [PMC13433862](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433862.1/), [PMC13439631](https://pmc.ncbi.nlm.nih.gov/articles/PMC13439631.1/), [PMC4804513](https://pmc.ncbi.nlm.nih.gov/articles/PMC4804513.1/), [PMC8866621](https://pmc.ncbi.nlm.nih.gov/articles/PMC8866621.1/)

Recorded search terms: Cameroon, Djoumessi, spironolactone, mortality, five-year

**Overlap review:** 55 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## c021

**unanswerable · revision 1 · absent_fact**

What was five-year freedom from AF after a single procedure in the randomized TAILORED-AF cohort?

**Expected response**

The specified fact is not reported in the pinned selected corpus; state the evidence limit without inventing an estimate.

**Article roles declared by the question**

- Required: None recorded.
- Alternatives: None recorded.
- Decoys: None recorded.

**Evidence:** No positive answer-evidence set is defined. See the
expected refusal and the recorded search scope below.

**Response distinctions to preserve**

- Do not substitute another cohort’s or shorter-horizon result for this absent fact.

**Missing-fact search scope**

The primary and review report 12-month outcomes; the other AF studies concern detection, prediction or different cohorts, not five-year trial follow-up.

[PMC10363301](https://pmc.ncbi.nlm.nih.gov/articles/PMC10363301.1/), [PMC10607686](https://pmc.ncbi.nlm.nih.gov/articles/PMC10607686.1/), [PMC10619268](https://pmc.ncbi.nlm.nih.gov/articles/PMC10619268.1/), [PMC10985250](https://pmc.ncbi.nlm.nih.gov/articles/PMC10985250.1/), [PMC11265054](https://pmc.ncbi.nlm.nih.gov/articles/PMC11265054.1/), [PMC11354916](https://pmc.ncbi.nlm.nih.gov/articles/PMC11354916.1/), [PMC11373557](https://pmc.ncbi.nlm.nih.gov/articles/PMC11373557.1/), [PMC11374717](https://pmc.ncbi.nlm.nih.gov/articles/PMC11374717.1/), [PMC11514186](https://pmc.ncbi.nlm.nih.gov/articles/PMC11514186.1/), [PMC11549774](https://pmc.ncbi.nlm.nih.gov/articles/PMC11549774.1/), [PMC11973566](https://pmc.ncbi.nlm.nih.gov/articles/PMC11973566.1/), [PMC12003177](https://pmc.ncbi.nlm.nih.gov/articles/PMC12003177.1/), [PMC12436478](https://pmc.ncbi.nlm.nih.gov/articles/PMC12436478.1/), [PMC12683810](https://pmc.ncbi.nlm.nih.gov/articles/PMC12683810.1/), [PMC12880197](https://pmc.ncbi.nlm.nih.gov/articles/PMC12880197.1/), [PMC12886974](https://pmc.ncbi.nlm.nih.gov/articles/PMC12886974.1/), [PMC13433181](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433181.1/), [PMC13433862](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433862.1/), [PMC13439631](https://pmc.ncbi.nlm.nih.gov/articles/PMC13439631.1/), [PMC4804513](https://pmc.ncbi.nlm.nih.gov/articles/PMC4804513.1/), [PMC8866621](https://pmc.ncbi.nlm.nih.gov/articles/PMC8866621.1/)

Recorded search terms: TAILORED-AF, five-year, long-term follow-up, freedom from AF

**Overlap review:** 55 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## c022

**unanswerable · revision 1 · absent_fact**

What externally validated ten-year hard-MACE risk does Gao’s CCTA nomogram assign to its original study cohort?

**Expected response**

The specified fact is not reported in the pinned selected corpus; state the evidence limit without inventing an estimate.

**Article roles declared by the question**

- Required: None recorded.
- Alternatives: None recorded.
- Decoys: None recorded.

**Evidence:** No positive answer-evidence set is defined. See the
expected refusal and the recorded search scope below.

**Response distinctions to preserve**

- Do not substitute another cohort’s or shorter-horizon result for this absent fact.

**Missing-fact search scope**

The source’s horizon is one year and composite includes unstable-angina utilization; no selected paper validates ten-year hard-MACE prediction for that original cohort.

[PMC10363301](https://pmc.ncbi.nlm.nih.gov/articles/PMC10363301.1/), [PMC10607686](https://pmc.ncbi.nlm.nih.gov/articles/PMC10607686.1/), [PMC10619268](https://pmc.ncbi.nlm.nih.gov/articles/PMC10619268.1/), [PMC10985250](https://pmc.ncbi.nlm.nih.gov/articles/PMC10985250.1/), [PMC11265054](https://pmc.ncbi.nlm.nih.gov/articles/PMC11265054.1/), [PMC11354916](https://pmc.ncbi.nlm.nih.gov/articles/PMC11354916.1/), [PMC11373557](https://pmc.ncbi.nlm.nih.gov/articles/PMC11373557.1/), [PMC11374717](https://pmc.ncbi.nlm.nih.gov/articles/PMC11374717.1/), [PMC11514186](https://pmc.ncbi.nlm.nih.gov/articles/PMC11514186.1/), [PMC11549774](https://pmc.ncbi.nlm.nih.gov/articles/PMC11549774.1/), [PMC11973566](https://pmc.ncbi.nlm.nih.gov/articles/PMC11973566.1/), [PMC12003177](https://pmc.ncbi.nlm.nih.gov/articles/PMC12003177.1/), [PMC12436478](https://pmc.ncbi.nlm.nih.gov/articles/PMC12436478.1/), [PMC12683810](https://pmc.ncbi.nlm.nih.gov/articles/PMC12683810.1/), [PMC12880197](https://pmc.ncbi.nlm.nih.gov/articles/PMC12880197.1/), [PMC12886974](https://pmc.ncbi.nlm.nih.gov/articles/PMC12886974.1/), [PMC13433181](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433181.1/), [PMC13433862](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433862.1/), [PMC13439631](https://pmc.ncbi.nlm.nih.gov/articles/PMC13439631.1/), [PMC4804513](https://pmc.ncbi.nlm.nih.gov/articles/PMC4804513.1/), [PMC8866621](https://pmc.ncbi.nlm.nih.gov/articles/PMC8866621.1/)

Recorded search terms: Gao, 1884303, ten-year, hard MACE, external validation

**Overlap review:** 55 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## c023

**cross_doc_distractor · revision 1 · answerable**

In Rashed’s 150-patient STEMI study, what were the no-reflow AUCs for CHA2DS2-VASc alone and its combination with brachial FMD?

**Expected response**

CHA2DS2-VASc AUC was 0.800, versus 0.885 when combined with brachial FMD.

**Required claims**

- `f1`: CHA2DS2-VASc AUC was 0.800, versus 0.885 when combined with brachial FMD.

**Article roles declared by the question**

- Required: [PMC8866621](https://pmc.ncbi.nlm.nih.gov/articles/PMC8866621.1/)
- Alternatives: None recorded.
- Decoys: [PMC13439631](https://pmc.ncbi.nlm.nih.gov/articles/PMC13439631.1/)

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC8866621](https://pmc.ncbi.nlm.nih.gov/articles/PMC8866621.1/) | Results; ROC for score, FMD and combined model; p. 4, 5 | `vasc_auc` |

**Why the distractors matter**

- [PMC13439631](https://pmc.ncbi.nlm.nih.gov/articles/PMC13439631.1/) — Another STEMI score-based combined no-reflow model.
  Sun uses CHA2DS2-VA with laboratory/procedural variables in 725 patients, not VASc plus FMD in this cohort.
  Passage: Results 3.4; combined models and sex subgroups; PDF p. 4; anchor `nrp_combined`.

**Response distinctions to preserve**

- Do not generalize a source-specific estimate to other cohorts, endpoints or timeframes.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## c024

**false_premise · revision 1 · false_premise**

Since every spironolactone participant in the Cameroon trial achieved office BP below 130/80 mmHg after one month, what supports that universal control claim?

**Expected response**

The abstract claims all patients were controlled below 130/80, but the Results describe one of nine participants with office BP 140/67, not reaching its stated office target below 140/90. That participant did meet the separate home/SBPM target below 135/85. Preserve the abstract/body conflict rather than treating home control as universal office control.

**Required claims**

- `f1`: The abstract claims all patients were controlled below 130/80, but the Results describe one of nine participants with office BP 140/67, not reaching its stated office target below 140/90.
- `f2`: That participant did meet the separate home/SBPM target below 135/85. Preserve the abstract/body conflict rather than treating home control as universal office control.

**Article roles declared by the question**

- Required: [PMC4804513](https://pmc.ncbi.nlm.nih.gov/articles/PMC4804513.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC4804513](https://pmc.ncbi.nlm.nih.gov/articles/PMC4804513.1/) | Abstract; control claim; p. 1 | `spirono_abstract` |
| primary | f1, f2 | [PMC4804513](https://pmc.ncbi.nlm.nih.gov/articles/PMC4804513.1/) | Results; conflicting targets and uncontrolled participant; p. 4 | `spirono_exception` |

**Response distinctions to preserve**

- Do not silently replace office targets with home targets or reconcile the inconsistent abstract and body.

**Premise to correct:** All participants achieved office BP below 130/80 after one month.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)
