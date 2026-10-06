# Oncology evaluation cases

Generated from the current combined v2 inputs. Regenerate with
`python render_case_index.py`; do not edit this page by hand.

[All topics](README.md) · [Article catalogue](articles.md) ·
[Authoritative questions](../combined/v2/oncology/queries.json) ·
[Dependency map](../combined/v2/case_dependencies.json)

Expected responses are model-reviewed references, not biomedical expert
certification or observed RAG responses. No new scoring is performed here.

## Find a question

| ID | Category | Question |
| --- | --- | --- |
| [q079](#q079) | direct_lookup | According to the liquid-biopsy review, distinguish the pooled CSF ctDNA detection rate from sensitivity and specificity for CNS metastases in NSCLC, and compare detection with cytology. |
| [q080](#q080) | direct_lookup | What did the liquid-biopsy review report about plasma versus tissue testing in NILE, including turnaround and biomarker identification? |
| [q081](#q081) | false_premise | Does the liquid-biopsy review establish that blood-based MCED has the same demonstrated lung-cancer mortality benefit as LDCT? |
| [q095](#q095) | direct_lookup | What four mutually exclusive screening categories and percentages did the US dual-screening study report for women ages 50–64? |
| [q096](#q096) | direct_lookup | In the US dual-screening study, how much more common was cervical-only than CRC-only screening? |
| [q102](#q102) | direct_lookup | What hysterectomy exclusion and final analysis-group counts appear in the US dual-screening study’s Appendix 1 flow diagram? |
| [o022](#o022) | direct_lookup | What population and treatment-group sizes were included in the Hunan neoadjuvant NSCLC cohort, and what surgical-selection restriction matters? |
| [o029](#o029) | multi_hop | How did the Hunan study’s unadjusted two-year DFS comparison change after propensity matching, and how should its OS evidence be interpreted? |
| [o028](#o028) | direct_lookup | What unadjusted MPR rates did the Hunan cohort report for PD-1 plus chemotherapy versus chemotherapy alone? |
| [o001](#o001) | false_premise | Did the Zhongshan stage III neoadjuvant cohort demonstrate statistically significant DFS improvement because its pathological responses were higher? |
| [o002](#o002) | multi_hop | Are the Zhongshan stage III cohort’s narrative and Table 2 MPR counts consistent for the chemoimmunotherapy arm? |
| [o003](#o003) | direct_lookup | How did pCR and study design differ between the Helsinki pembrolizumab and historical chemotherapy TNBC cohorts? |
| [o004](#o004) | multi_hop | In the Helsinki TNBC cohort, distinguish myocarditis from any new troponin elevation and explain the surveillance used. |
| [o005](#o005) | multi_hop | Why do postoperative pembrolizumab discontinuation percentages differ between the Helsinki abstract and results? |
| [o027](#o027) | direct_lookup | Did the Vietnam afatinib study’s higher ORR at a 40-mg starting dose also translate to significantly longer mTTF? |
| [o006](#o006) | multi_hop | Are the Vietnam afatinib abstract and Table 2 consistent about the 30-mg and 40-mg starting-dose shares? |
| [q108](#q108) | false_premise | Are the ADAURA hazard ratios in the nonmetastatic driver review outcomes measured by the review’s own newly enrolled cohort? |
| [o007](#o007) | direct_lookup | What five-year OS results does the driver-altered nonmetastatic review attribute to ADAURA, distinguishing stage populations? |
| [o023](#o023) | multi_hop | In the Gosney expert consensus, who initiates reflex NSCLC biomarker testing, what is agreed by the MDT, and is a formal oncologist request required? Explain the reported delay mechanism. |
| [o008](#o008) | direct_lookup | Why does the reflex-testing consensus also argue for early testing in resectable NSCLC? |
| [o009](#o009) | multi_hop | What CV-event estimates and study design did the observational NSCLC immunotherapy meta-analysis report? |
| [o010](#o010) | direct_lookup | In the lung-cancer RCT meta-analysis, how did single ICI and ICI plus chemotherapy compare with chemotherapy for cardiac adverse events? |
| [o011](#o011) | false_premise | Does the RCT meta-analysis prove ICIs cannot cause heart failure because that subgroup result was nonsignificant? |
| [o026](#o026) | direct_lookup | Among deaths in the older advanced-NSCLC PD-1 cohort, what shares were attributed to NSCLC and CVD, and which factors were associated with CVD mortality? |
| [o012](#o012) | direct_lookup | How did pembrolizumab versus nivolumab compare for cause-specific mortality in the older NSCLC cohort? |
| [q085](#q085) | direct_lookup | How does the immune-exclusion definition review distinguish inflamed, desert and excluded tumors spatially? |
| [o013](#o013) | false_premise | Does the immune-exclusion review establish a universal clinically validated numeric cutoff for every tumor? |
| [o014](#o014) | direct_lookup | In the ICD mini-review, what distinct dendritic-cell mechanisms are attributed to CALR, ATP and HMGB1? |
| [o015](#o015) | direct_lookup | How does the ICD mini-review distinguish excluded, desert and immunosuppressed cold tumors? |
| [o016](#o016) | multi_hop | How do the ICD review’s ER stress and autophagy pathways connect to the dendritic-cell effects of CALR and ATP? |
| [o030](#o030) | cross_doc_synthesis | Combine the Hunan neoadjuvant study with the reflex-testing consensus: what does each contribute to interpreting perioperative NSCLC treatment and biomarker readiness? |
| [o017](#o017) | cross_doc_synthesis | Why can the observational CV-event meta-analysis and older PD-1 cause-specific mortality cohort not be read as the same cardiovascular endpoint? |
| [o018](#o018) | cross_doc_synthesis | How should the Helsinki TNBC myocarditis frequency and lung-cancer RCT cardiac-adverse-event risks be compared? |
| [o024](#o024) | cross_doc_distractor | In the driver-altered NSCLC review’s stage II–IIIA ADAURA results, what absolute difference do the reported five-year OS rates imply between osimertinib and placebo, and what treatment setting does it describe? |
| [o025](#o025) | cross_doc_distractor | For NSCLC MRD assessment in the Batra liquid-biopsy review, how do tumor-informed and tumor-agnostic assays compare at landmark and longitudinal timepoints? |
| [o020](#o020) | unanswerable | How many Hunan patients failed to undergo surgery after starting neoadjuvant therapy, and why? |
| [o021](#o021) | false_premise | What randomized five-year pembrolizumab-versus-chemotherapy OS treatment effect did the Helsinki TNBC study measure? |
| [q083](#q083) | unanswerable | What FDA-validated early-stage sensitivity value for EarlyCDT-Lung is reported in the selected oncology corpus? |
| [q100](#q100) | unanswerable | What dual-screening rate for the Basque Country FIT programme is reported in the selected oncology corpus? |
| [q101](#q101) | false_premise | Are the HP2030 cervical and colorectal screening goals cited by Harper the study’s own achieved rates? |
| [q078](#q078) | direct_lookup | According to the liquid-biopsy review, how much does combining ctDNA with ctRNA analysis change gene-fusion detection yield compared with ctDNA alone, and what RNA-testing recommendation does the review connect to this? |
| [q097](#q097) | direct_lookup | In the US dual-screening study's multinomial regression, what adjusted odds ratios were reported for college graduation and for the highest income level when predicting dual screening versus neither screen? |
| [q098](#q098) | direct_lookup | In the US dual-screening study's adjusted analyses, how did the screening patterns of Black and Hispanic women differ, each compared with White women? |
| [q099](#q099) | direct_lookup | What decision levels does the US dual-screening study's Discussion propose to explain why cervical and colorectal screening diverge with age? |

## q079

**direct_lookup · revision 3 · answerable**

According to the liquid-biopsy review, distinguish the pooled CSF ctDNA detection rate from sensitivity and specificity for CNS metastases in NSCLC, and compare detection with cytology.

**Expected response**

The cited 26-study meta-analysis reports CSF ctDNA detection 86% (95% CI 79–91%) versus cytology 60% (36–81%); sensitivity 91.8% and specificity 93.5% are separate diagnostic measures.

**Required claims**

- `f1`: The cited 26-study meta-analysis reports CSF ctDNA detection 86% (95% CI 79–91%) versus cytology 60% (36–81%); sensitivity 91.8% and specificity 93.5% are separate diagnostic measures.

**Article roles declared by the question**

- Required: [PMC13429855](https://pmc.ncbi.nlm.nih.gov/articles/PMC13429855.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC13429855](https://pmc.ncbi.nlm.nih.gov/articles/PMC13429855.1/) | CNS/CSF liquid biopsy; cited pooled diagnostic evidence; p. 10 | `csf` |

**Response distinctions to preserve**

- Do not substitute another population or endpoint for Cited CNS/NSCLC pooled evidence: Detection, sensitivity and specificity.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../combined/v2/case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## q080

**direct_lookup · revision 3 · answerable**

What did the liquid-biopsy review report about plasma versus tissue testing in NILE, including turnaround and biomarker identification?

**Expected response**

In 282 untreated metastatic NSCLC patients, plasma testing was noninferior for guideline biomarkers, found at least one biomarker in more patients, and had median turnaround 9 versus 15 days for tissue.

**Required claims**

- `f1`: In 282 untreated metastatic NSCLC patients, plasma testing was noninferior for guideline biomarkers, found at least one biomarker in more patients, and had median turnaround 9 versus 15 days for tissue.

**Article roles declared by the question**

- Required: [PMC13429855](https://pmc.ncbi.nlm.nih.gov/articles/PMC13429855.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC13429855](https://pmc.ncbi.nlm.nih.gov/articles/PMC13429855.1/) | Advanced-disease genotyping; cited NILE study; p. 5 | `nile` |

**Response distinctions to preserve**

- Do not substitute another population or endpoint for 282 untreated metastatic NSCLC patients: Genotyping yield and turnaround.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../combined/v2/case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## q081

**false_premise · revision 3 · false_premise**

Does the liquid-biopsy review establish that blood-based MCED has the same demonstrated lung-cancer mortality benefit as LDCT?

**Expected response**

No. The review attributes a demonstrated mortality benefit to LDCT, including the NLST 20% relative reduction versus chest radiography. It states that no MCED test has shown mortality benefit to date; this is the pinned review’s evidence assessment, not a claim of proven ineffectiveness.

**Required claims**

- `f1`: No. The review attributes a demonstrated mortality benefit to LDCT, including the NLST 20% relative reduction versus chest radiography.
- `f2`: It states that no MCED test has shown mortality benefit to date; this is the pinned review’s evidence assessment, not a claim of proven ineffectiveness.

**Article roles declared by the question**

- Required: [PMC13429855](https://pmc.ncbi.nlm.nih.gov/articles/PMC13429855.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC13429855](https://pmc.ncbi.nlm.nih.gov/articles/PMC13429855.1/) | Screening; LDCT mortality evidence; p. 3 | `ldct` |
| primary | f2 | [PMC13429855](https://pmc.ncbi.nlm.nih.gov/articles/PMC13429855.1/) | Abstract; absence of mortality and randomized OS evidence; p. 1 | `mced` |

**Response distinctions to preserve**

- Do not substitute another population or endpoint for Cited screening trials: Lung-cancer mortality.
- Do not substitute another population or endpoint for MCED evidence reviewed: Mortality benefit.

**Premise to correct:** Does the liquid-biopsy review establish that blood-based MCED has the same demonstrated lung-cancer mortality benefit as LDCT?

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../combined/v2/case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## q095

**direct_lookup · revision 3 · answerable**

What four mutually exclusive screening categories and percentages did the US dual-screening study report for women ages 50–64?

**Expected response**

Dual screening 58.2%, cervical only 27.1%, CRC only 5.4%, neither 9.3%; dual screening is not the independent CRC screening rate.

**Required claims**

- `f1`: Dual screening 58.2%, cervical only 27.1%, CRC only 5.4%, neither 9.3%; dual screening is not the independent CRC screening rate.

**Article roles declared by the question**

- Required: [PMC9239676](https://pmc.ncbi.nlm.nih.gov/articles/PMC9239676.1/)
- Alternatives: [PMC9239676](https://pmc.ncbi.nlm.nih.gov/articles/PMC9239676.1/)
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC9239676](https://pmc.ncbi.nlm.nih.gov/articles/PMC9239676.1/) | Abstract; mutually exclusive screening categories, ages 50–64; p. 1 | `screen` |
| results | f1 | [PMC9239676](https://pmc.ncbi.nlm.nih.gov/articles/PMC9239676.1/) | Results; four mutually exclusive screening categories (continues across page break); p. 4, 5 | `screen_results` |
| table2 | f1 | [PMC9239676](https://pmc.ncbi.nlm.nih.gov/articles/PMC9239676.1/) | Table 2; category headings and totals; p. 6 | `screen_table2` |

**Response distinctions to preserve**

- Do not substitute another population or endpoint for US women aged 50–64: Screening categories.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../combined/v2/case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## q096

**direct_lookup · revision 3 · answerable**

In the US dual-screening study, how much more common was cervical-only than CRC-only screening?

**Expected response**

Cervical-only screening was approximately five times as common as CRC-only screening; the reported percentages are 27.1% versus 5.4%.

**Required claims**

- `f1`: Cervical-only screening was approximately five times as common as CRC-only screening; the reported percentages are 27.1% versus 5.4%.

**Article roles declared by the question**

- Required: [PMC9239676](https://pmc.ncbi.nlm.nih.gov/articles/PMC9239676.1/)
- Alternatives: [PMC9239676](https://pmc.ncbi.nlm.nih.gov/articles/PMC9239676.1/)
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC9239676](https://pmc.ncbi.nlm.nih.gov/articles/PMC9239676.1/) | Abstract; mutually exclusive screening categories, ages 50–64; p. 1 | `screen` |
| results | f1 | [PMC9239676](https://pmc.ncbi.nlm.nih.gov/articles/PMC9239676.1/) | Results; four mutually exclusive screening categories (continues across page break); p. 4, 5 | `screen_results` |
| table2 | f1 | [PMC9239676](https://pmc.ncbi.nlm.nih.gov/articles/PMC9239676.1/) | Table 2; category headings and totals; p. 6 | `screen_table2` |
| reported_ratio | f1 | [PMC9239676](https://pmc.ncbi.nlm.nih.gov/articles/PMC9239676.1/) | Results; explicitly reported fivefold single-screen comparison; p. 5 | `screen_single_results` |
| screen_single_discussion | f1 | [PMC9239676](https://pmc.ncbi.nlm.nih.gov/articles/PMC9239676.1/) | Discussion; explicitly stated fivefold single-screen comparison; p. 11 | `screen_single_discussion` |
| screen_single_healthsystem | f1 | [PMC9239676](https://pmc.ncbi.nlm.nih.gov/articles/PMC9239676.1/) | Discussion 2c; repeated fivefold single-screen comparison; p. 12 | `screen_single_healthsystem` |

**Response distinctions to preserve**

- Do not substitute another population or endpoint for US women aged 50–64: Single-screen prevalence.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../combined/v2/case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## q102

**direct_lookup · revision 3 · answerable**

What hysterectomy exclusion and final analysis-group counts appear in the US dual-screening study’s Appendix 1 flow diagram?

**Expected response**

The diagram excludes 19,011 for hysterectomy and labels the final analysis group 40,511. These are printed counts; do not silently correct them using inconsistent flow-chart arithmetic.

**Required claims**

- `f1`: The diagram excludes 19,011 for hysterectomy and labels the final analysis group 40,511. These are printed counts; do not silently correct them using inconsistent flow-chart arithmetic.

**Article roles declared by the question**

- Required: [PMC9239676](https://pmc.ncbi.nlm.nih.gov/articles/PMC9239676.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC9239676](https://pmc.ncbi.nlm.nih.gov/articles/PMC9239676.1/) | Appendix 1 figure 1; exclusions and analysis group; p. 17 | `flow` |

**Response distinctions to preserve**

- Do not substitute another population or endpoint for Appendix flow diagram and main study population: Exclusion and analysis counts.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../combined/v2/case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## o022

**direct_lookup · revision 2 · answerable**

What population and treatment-group sizes were included in the Hunan neoadjuvant NSCLC cohort, and what surgical-selection restriction matters?

**Expected response**

There were 190 resected NSCLC patients: 69 PD-1 inhibitor plus chemotherapy and 121 chemotherapy alone; ECOG was 0 or 1. Patients failing surgery for any reason were excluded, so this is not all patients starting neoadjuvant therapy.

**Required claims**

- `f1`: There were 190 resected NSCLC patients: 69 PD-1 inhibitor plus chemotherapy and 121 chemotherapy alone; ECOG was 0 or 1. Patients failing surgery for any reason were excluded, so this is not all patients starting neoadjuvant therapy.

**Article roles declared by the question**

- Required: [PMC9844597](https://pmc.ncbi.nlm.nih.gov/articles/PMC9844597.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC9844597](https://pmc.ncbi.nlm.nih.gov/articles/PMC9844597.1/) | Methods; eligibility, surgical selection and treatment groups; p. 3 | `hunan_population` |

**Response distinctions to preserve**

- Do not substitute another population or endpoint for Hunan retrospective resected cohort: Eligibility and cohort composition.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../combined/v2/case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## o029

**multi_hop · revision 3 · answerable**

How did the Hunan study’s unadjusted two-year DFS comparison change after propensity matching, and how should its OS evidence be interpreted?

**Expected response**

Unadjusted DFS was 79.3% versus 60.2% (p=0.048); after PSM the difference was no longer statistically significant (p=0.096). Two-year OS was 94.1% versus 85.7% in the unweighted population (p=0.012) and 93.8% versus 87.1% in the second comparison (p=0.038), PD-1 plus chemotherapy versus chemotherapy. The Results text calls that second comparison the weighted population, while the Figure 1D legend labels the same p=0.038 curves after PSM; attribute the label used and do not silently reconcile them. The Limitations state that follow-up was too short to make OS the primary endpoint and that mature conclusions need longer follow-up, so these comparisons are not mature causal survival evidence.

**Required claims**

- `f1`: Unadjusted DFS was 79.3% versus 60.2% (p=0.048); after PSM the difference was no longer statistically significant (p=0.096).
- `f2`: Two-year OS was 94.1% versus 85.7% in the unweighted population (p=0.012) and 93.8% versus 87.1% in the second comparison (p=0.038), PD-1 plus chemotherapy versus chemotherapy. The Results text calls that second comparison the weighted population, while the Figure 1D legend labels the same p=0.038 curves after PSM; attribute the label used and do not silently reconcile them. The Limitations state that follow-up was too short to make OS the primary endpoint and that mature conclusions need longer follow-up, so these comparisons are not mature causal survival evidence.

**Article roles declared by the question**

- Required: [PMC9844597](https://pmc.ncbi.nlm.nih.gov/articles/PMC9844597.1/)
- Alternatives: [PMC9844597](https://pmc.ncbi.nlm.nih.gov/articles/PMC9844597.1/)
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC9844597](https://pmc.ncbi.nlm.nih.gov/articles/PMC9844597.1/) | Abstract; unadjusted pathological response and DFS; p. 1 | `hunan_response` |
| primary | f1 | [PMC9844597](https://pmc.ncbi.nlm.nih.gov/articles/PMC9844597.1/) | Results 3.4; unadjusted DFS and loss of significance after PSM; p. 7 | `hunan_matched` |
| primary | f2 | [PMC9844597](https://pmc.ncbi.nlm.nih.gov/articles/PMC9844597.1/) | Results 3.4; unweighted and weighted two-year OS comparisons; p. 7 | `hunan_os_results` |
| primary | f2 | [PMC9844597](https://pmc.ncbi.nlm.nih.gov/articles/PMC9844597.1/) | Figure 1 legend; panel D OS curves labelled after PSM (p=0.038); p. 9 | `hunan_fig1_legend` |
| primary | f2 | [PMC9844597](https://pmc.ncbi.nlm.nih.gov/articles/PMC9844597.1/) | Discussion; limitations: follow-up too short for OS endpoint; p. 12 | `hunan_os_limitation` |
| results_dfs | f1 | [PMC9844597](https://pmc.ncbi.nlm.nih.gov/articles/PMC9844597.1/) | Results 3.4; unadjusted DFS and loss of significance after PSM; p. 7 | `hunan_matched` |
| results_dfs | f2 | [PMC9844597](https://pmc.ncbi.nlm.nih.gov/articles/PMC9844597.1/) | Results 3.4; unweighted and weighted two-year OS comparisons; p. 7 | `hunan_os_results` |
| results_dfs | f2 | [PMC9844597](https://pmc.ncbi.nlm.nih.gov/articles/PMC9844597.1/) | Figure 1 legend; panel D OS curves labelled after PSM (p=0.038); p. 9 | `hunan_fig1_legend` |
| results_dfs | f2 | [PMC9844597](https://pmc.ncbi.nlm.nih.gov/articles/PMC9844597.1/) | Discussion; limitations: follow-up too short for OS endpoint; p. 12 | `hunan_os_limitation` |

**Response distinctions to preserve**

- Do not substitute another population or endpoint for PD-1 plus chemotherapy versus chemotherapy: Two-year DFS.
- Do not substitute another population or endpoint for Hunan cohort: Two-year OS comparisons and attributed OS analysis-label conflict and OS maturity.
- Do not describe a separate weighting method: the Methods describe PSM only, and the Results/Figure 1D labels conflict.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../combined/v2/case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## o028

**direct_lookup · revision 2 · answerable**

What unadjusted MPR rates did the Hunan cohort report for PD-1 plus chemotherapy versus chemotherapy alone?

**Expected response**

49.3% versus 19.0% (p<0.001); these are pathological responses, not two-year DFS.

**Required claims**

- `f1`: 49.3% versus 19.0% (p<0.001); these are pathological responses, not two-year DFS.

**Article roles declared by the question**

- Required: [PMC9844597](https://pmc.ncbi.nlm.nih.gov/articles/PMC9844597.1/)
- Alternatives: [PMC9844597](https://pmc.ncbi.nlm.nih.gov/articles/PMC9844597.1/)
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC9844597](https://pmc.ncbi.nlm.nih.gov/articles/PMC9844597.1/) | Abstract; unadjusted pathological response and DFS; p. 1 | `hunan_response` |
| results | f1 | [PMC9844597](https://pmc.ncbi.nlm.nih.gov/articles/PMC9844597.1/) | Results 3.3; unadjusted MPR and pCR; p. 7 | `hunan_mpr_results` |
| table2 | f1 | [PMC9844597](https://pmc.ncbi.nlm.nih.gov/articles/PMC9844597.1/) | Table 2; before/after PSM treatment-group columns; p. 6 | `hunan_mpr_table_header` |
| table2 | f1 | [PMC9844597](https://pmc.ncbi.nlm.nih.gov/articles/PMC9844597.1/) | Table 2; pathological response rows; p. 6 | `hunan_mpr_table` |
| discussion_with_significance | f1 | [PMC9844597](https://pmc.ncbi.nlm.nih.gov/articles/PMC9844597.1/) | Discussion; unadjusted pathological response; p. 8 | `hunan_mpr_discussion` |
| discussion_with_significance | f1 | [PMC9844597](https://pmc.ncbi.nlm.nih.gov/articles/PMC9844597.1/) | Table 2; before/after PSM treatment-group columns; p. 6 | `hunan_mpr_table_header` |
| discussion_with_significance | f1 | [PMC9844597](https://pmc.ncbi.nlm.nih.gov/articles/PMC9844597.1/) | Table 2; pathological response rows; p. 6 | `hunan_mpr_table` |

**Response distinctions to preserve**

- Do not substitute another population or endpoint for Hunan PD-1 plus chemotherapy versus chemotherapy: MPR.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../combined/v2/case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## o001

**false_premise · revision 3 · false_premise**

Did the Zhongshan stage III neoadjuvant cohort demonstrate statistically significant DFS improvement because its pathological responses were higher?

**Expected response**

The Zhongshan cohort reports table/abstract MPR 65.3% versus 15.1% and pCR 34.6% versus 3.0%, while DFS was not statistically different (p=0.129). Response does not establish survival benefit.

**Required claims**

- `f1`: The Zhongshan cohort reports table/abstract MPR 65.3% versus 15.1% and pCR 34.6% versus 3.0%, while DFS was not statistically different (p=0.129). Response does not establish survival benefit.

**Article roles declared by the question**

- Required: [PMC10770829](https://pmc.ncbi.nlm.nih.gov/articles/PMC10770829.1/)
- Alternatives: [PMC10770829](https://pmc.ncbi.nlm.nih.gov/articles/PMC10770829.1/)
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC10770829](https://pmc.ncbi.nlm.nih.gov/articles/PMC10770829.1/) | Abstract; pathological outcomes versus DFS; p. 1 | `stage_response` |
| table_and_results | f1 | [PMC10770829](https://pmc.ncbi.nlm.nih.gov/articles/PMC10770829.1/) | Table 2; treatment columns, pCR and MPR rows; p. 5 | `stage_table` |
| table_and_results | f1 | [PMC10770829](https://pmc.ncbi.nlm.nih.gov/articles/PMC10770829.1/) | Results; recurrence counts and nonsignificant DFS; p. 5 | `stage_dfs_results` |
| table_and_discussion | f1 | [PMC10770829](https://pmc.ncbi.nlm.nih.gov/articles/PMC10770829.1/) | Table 2; treatment columns, pCR and MPR rows; p. 5 | `stage_table` |
| table_and_discussion | f1 | [PMC10770829](https://pmc.ncbi.nlm.nih.gov/articles/PMC10770829.1/) | Discussion; nonsignificant DFS comparison; p. 8 | `stage_dfs_discussion` |

**Response distinctions to preserve**

- Do not substitute another population or endpoint for Stage III neoadjuvant combo versus chemotherapy cohort: Pathological response versus DFS.

**Premise to correct:** Did the Zhongshan stage III neoadjuvant cohort demonstrate statistically significant DFS improvement because its pathological responses were higher?

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../combined/v2/case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## o002

**multi_hop · revision 3 · answerable**

Are the Zhongshan stage III cohort’s narrative and Table 2 MPR counts consistent for the chemoimmunotherapy arm?

**Expected response**

No. The narrative says 19 of 26, whereas Table 2 reports 17 (65.3%) for chemoimmunotherapy and 5 (15.1%) for chemotherapy. Attribute both and flag the conflict; do not silently reconcile them.

**Required claims**

- `f1`: No. The narrative says 19 of 26, whereas Table 2 reports 17 (65.3%) for chemoimmunotherapy and 5 (15.1%) for chemotherapy. Attribute both and flag the conflict; do not silently reconcile them.

**Article roles declared by the question**

- Required: [PMC10770829](https://pmc.ncbi.nlm.nih.gov/articles/PMC10770829.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC10770829](https://pmc.ncbi.nlm.nih.gov/articles/PMC10770829.1/) | Results; pathological response narrative and confidence intervals; p. 5 | `stage_narrative` |
| primary | f1 | [PMC10770829](https://pmc.ncbi.nlm.nih.gov/articles/PMC10770829.1/) | Table 2; treatment columns, pCR and MPR rows; p. 5 | `stage_table` |

**Response distinctions to preserve**

- Do not substitute another population or endpoint for Stage III NICT versus NCT: MPR count conflict.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../combined/v2/case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## o003

**direct_lookup · revision 2 · answerable**

How did pCR and study design differ between the Helsinki pembrolizumab and historical chemotherapy TNBC cohorts?

**Expected response**

pCR was 42 of 75 (56.0%) with pembrolizumab-based therapy and 47 of 102 (46.1%) without. The historical comparator was nonmatched and this was retrospective, so the difference is not a randomized treatment-effect estimate.

**Required claims**

- `f1`: pCR was 42 of 75 (56.0%) with pembrolizumab-based therapy and 47 of 102 (46.1%) without. The historical comparator was nonmatched and this was retrospective, so the difference is not a randomized treatment-effect estimate.

**Article roles declared by the question**

- Required: [PMC12931073](https://pmc.ncbi.nlm.nih.gov/articles/PMC12931073.1/)
- Alternatives: [PMC12931073](https://pmc.ncbi.nlm.nih.gov/articles/PMC12931073.1/)
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC12931073](https://pmc.ncbi.nlm.nih.gov/articles/PMC12931073.1/) | Abstract; retrospective pembrolizumab and nonmatched historical cohorts; p. 1 | `breast_pcr` |
| breast_pcr_results | f1 | [PMC12931073](https://pmc.ncbi.nlm.nih.gov/articles/PMC12931073.1/) | Methods; retrospective nonmatched cohorts; p. 2 | `breast_design` |
| breast_pcr_results | f1 | [PMC12931073](https://pmc.ncbi.nlm.nih.gov/articles/PMC12931073.1/) | Results; pCR in the two cohorts; p. 5 | `breast_pcr_results` |
| breast_pcr_table | f1 | [PMC12931073](https://pmc.ncbi.nlm.nih.gov/articles/PMC12931073.1/) | Methods; retrospective nonmatched cohorts; p. 2 | `breast_design` |
| breast_pcr_table | f1 | [PMC12931073](https://pmc.ncbi.nlm.nih.gov/articles/PMC12931073.1/) | Table 3; pCR/RCB-0 treatment columns; p. 5 | `breast_pcr_table` |

**Response distinctions to preserve**

- Do not substitute another population or endpoint for Helsinki TNBC cohorts: pCR and comparator design.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../combined/v2/case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## o004

**multi_hop · revision 2 · answerable**

In the Helsinki TNBC cohort, distinguish myocarditis from any new troponin elevation and explain the surveillance used.

**Expected response**

The cohort reported 11 myocarditis patients (14.7%), with no grade 3 or 4 cases, versus 23 patients with new troponin elevation; these are not interchangeable diagnoses. ECG was obtained before treatment and troponin before every pembrolizumab cycle; diagnosis used new troponin elevation plus one major or two minor criteria.

**Required claims**

- `f1`: The cohort reported 11 myocarditis patients (14.7%), with no grade 3 or 4 cases, versus 23 patients with new troponin elevation; these are not interchangeable diagnoses.
- `f2`: ECG was obtained before treatment and troponin before every pembrolizumab cycle; diagnosis used new troponin elevation plus one major or two minor criteria.

**Article roles declared by the question**

- Required: [PMC12931073](https://pmc.ncbi.nlm.nih.gov/articles/PMC12931073.1/)
- Alternatives: [PMC12931073](https://pmc.ncbi.nlm.nih.gov/articles/PMC12931073.1/)
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC12931073](https://pmc.ncbi.nlm.nih.gov/articles/PMC12931073.1/) | Results; myocarditis grades and new troponin elevations; p. 6, 7 | `breast_cardio` |
| primary | f1 | [PMC12931073](https://pmc.ncbi.nlm.nih.gov/articles/PMC12931073.1/) | Abstract; immune adverse events and discontinuation denominators; p. 1 | `breast_ae` |
| primary | f2 | [PMC12931073](https://pmc.ncbi.nlm.nih.gov/articles/PMC12931073.1/) | Methods; ECG, troponin surveillance and diagnostic criteria; p. 2 | `breast_monitor` |
| tables_with_monitoring | f1 | [PMC12931073](https://pmc.ncbi.nlm.nih.gov/articles/PMC12931073.1/) | Table 5; myocarditis count and zero severe events; p. 7 | `breast_cardio_table` |
| tables_with_monitoring | f1 | [PMC12931073](https://pmc.ncbi.nlm.nih.gov/articles/PMC12931073.1/) | Table 6; 23 troponin patients, 11 with myocarditis; p. 7 | `breast_troponin_table` |
| tables_with_monitoring | f2 | [PMC12931073](https://pmc.ncbi.nlm.nih.gov/articles/PMC12931073.1/) | Methods; ECG, troponin surveillance and diagnostic criteria; p. 2 | `breast_monitor` |

**Response distinctions to preserve**

- Do not substitute another population or endpoint for 75 pembrolizumab-treated TNBC patients: Myocarditis versus troponin elevation.
- Do not substitute another population or endpoint for Helsinki pembrolizumab cohort: Surveillance and diagnostic criteria.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../combined/v2/case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## o005

**multi_hop · revision 2 · answerable**

Why do postoperative pembrolizumab discontinuation percentages differ between the Helsinki abstract and results?

**Expected response**

Both describe eight patients: 10.7% of all 75 pembrolizumab patients in the abstract versus 23.5% of the 34 who started postoperative pembrolizumab in results. The denominators differ.

**Required claims**

- `f1`: Both describe eight patients: 10.7% of all 75 pembrolizumab patients in the abstract versus 23.5% of the 34 who started postoperative pembrolizumab in results. The denominators differ.

**Article roles declared by the question**

- Required: [PMC12931073](https://pmc.ncbi.nlm.nih.gov/articles/PMC12931073.1/)
- Alternatives: [PMC12931073](https://pmc.ncbi.nlm.nih.gov/articles/PMC12931073.1/)
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC12931073](https://pmc.ncbi.nlm.nih.gov/articles/PMC12931073.1/) | Abstract; immune adverse events and discontinuation denominators; p. 1 | `breast_ae` |
| primary | f1 | [PMC12931073](https://pmc.ncbi.nlm.nih.gov/articles/PMC12931073.1/) | Results; postoperative discontinuation and overall denominators; p. 7 | `breast_stop` |
| alternative_1 | f1 | [PMC12931073](https://pmc.ncbi.nlm.nih.gov/articles/PMC12931073.1/) | Abstract; immune adverse events and discontinuation denominators; p. 1 | `breast_ae` |
| alternative_1 | f1 | [PMC12931073](https://pmc.ncbi.nlm.nih.gov/articles/PMC12931073.1/) | Results; eight of 34 adjuvant discontinuations; p. 5 | `breast_stop_results` |

**Response distinctions to preserve**

- Do not substitute another population or endpoint for All treated versus postoperative starters: Adverse-event discontinuation.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../combined/v2/case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## o027

**direct_lookup · revision 2 · answerable**

Did the Vietnam afatinib study’s higher ORR at a 40-mg starting dose also translate to significantly longer mTTF?

**Expected response**

ORR was 83.9% at 40 mg versus 74.3% below 40 mg (p=0.034). mTTF was 16.7 versus 16.9 months (p=0.755), not significantly different; ORR and time to treatment failure are separate endpoints.

**Required claims**

- `f1`: ORR was 83.9% at 40 mg versus 74.3% below 40 mg (p=0.034).
- `f2`: mTTF was 16.7 versus 16.9 months (p=0.755), not significantly different; ORR and time to treatment failure are separate endpoints.

**Article roles declared by the question**

- Required: [PMC10840225](https://pmc.ncbi.nlm.nih.gov/articles/PMC10840225.1/)
- Alternatives: [PMC10840225](https://pmc.ncbi.nlm.nih.gov/articles/PMC10840225.1/)
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1, f2 | [PMC10840225](https://pmc.ncbi.nlm.nih.gov/articles/PMC10840225.1/) | Results; starting-dose ORR versus mTTF; p. 4 | `afatinib_dose_results` |
| separated_endpoints | f1 | [PMC10840225](https://pmc.ncbi.nlm.nih.gov/articles/PMC10840225.1/) | Abstract; response by initial dose; p. 1 | `afatinib_orr` |
| separated_endpoints | f2 | [PMC10840225](https://pmc.ncbi.nlm.nih.gov/articles/PMC10840225.1/) | Results and Table 2; initial dose, mTTF and dose distribution; p. 4 | `afatinib_ttf` |
| alternative_2 | f1 | [PMC10840225](https://pmc.ncbi.nlm.nih.gov/articles/PMC10840225.1/) | Abstract; response by initial dose; p. 1 | `afatinib_orr` |
| alternative_2 | f2 | [PMC10840225](https://pmc.ncbi.nlm.nih.gov/articles/PMC10840225.1/) | Discussion; nonsignificant starting-dose mTTF; p. 7 | `afatinib_ttf_discussion` |
| orr_table | f1 | [PMC10840225](https://pmc.ncbi.nlm.nih.gov/articles/PMC10840225.1/) | Table 3; ORR and statistical-test headings; p. 5 | `afatinib_orr_table_header` |
| orr_table | f1 | [PMC10840225](https://pmc.ncbi.nlm.nih.gov/articles/PMC10840225.1/) | Table 3; starting-dose ORR row; p. 5 | `afatinib_orr_table_row` |
| orr_table | f2 | [PMC10840225](https://pmc.ncbi.nlm.nih.gov/articles/PMC10840225.1/) | Results and Table 2; initial dose, mTTF and dose distribution; p. 4 | `afatinib_ttf` |

**Response distinctions to preserve**

- Do not substitute another population or endpoint for Advanced EGFR-mutant Vietnam cohort: ORR by starting dose.
- Do not substitute another population or endpoint for 40 mg versus below 40 mg: mTTF by initial dose.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../combined/v2/case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## o006

**multi_hop · revision 2 · answerable**

Are the Vietnam afatinib abstract and Table 2 consistent about the 30-mg and 40-mg starting-dose shares?

**Expected response**

No. The abstract assigns 58.6% to 40 mg and 39.9% to 30 mg; Table 2 assigns 201/343 (58.6%) to 30 mg and 137/343 (39.9%) to 40 mg. Both report 5/343 (1.5%) at 20 mg. Keep the conflict explicit.

**Required claims**

- `f1`: No. The abstract assigns 58.6% to 40 mg and 39.9% to 30 mg; Table 2 assigns 201/343 (58.6%) to 30 mg and 137/343 (39.9%) to 40 mg. Both report 5/343 (1.5%) at 20 mg. Keep the conflict explicit.

**Article roles declared by the question**

- Required: [PMC10840225](https://pmc.ncbi.nlm.nih.gov/articles/PMC10840225.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC10840225](https://pmc.ncbi.nlm.nih.gov/articles/PMC10840225.1/) | Abstract; starting-dose distribution; p. 1 | `afatinib_abstract` |
| primary | f1 | [PMC10840225](https://pmc.ncbi.nlm.nih.gov/articles/PMC10840225.1/) | Results and Table 2; initial dose, mTTF and dose distribution; p. 4 | `afatinib_ttf` |

**Response distinctions to preserve**

- Do not substitute another population or endpoint for 343 Vietnam first-line afatinib patients: Starting-dose distribution conflict.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../combined/v2/case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## q108

**false_premise · revision 3 · false_premise**

Are the ADAURA hazard ratios in the nonmetastatic driver review outcomes measured by the review’s own newly enrolled cohort?

**Expected response**

No. This is a review attributing results to ADAURA; initial stage II–IIIA DFS HR was 0.17 (99.06% CI 0.11–0.26), and overall stage IB–IIIA DFS HR 0.20 (99.12% CI 0.14–0.30).

**Required claims**

- `f1`: No. This is a review attributing results to ADAURA; initial stage II–IIIA DFS HR was 0.17 (99.06% CI 0.11–0.26), and overall stage IB–IIIA DFS HR 0.20 (99.12% CI 0.14–0.30).

**Article roles declared by the question**

- Required: [PMC11431721](https://pmc.ncbi.nlm.nih.gov/articles/PMC11431721.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC11431721](https://pmc.ncbi.nlm.nih.gov/articles/PMC11431721.1/) | Review; attributed initial ADAURA DFS results; p. 4 | `driver_dfs` |

**Response distinctions to preserve**

- Do not substitute another population or endpoint for Cited ADAURA trial populations: DFS attribution and population.

**Premise to correct:** Are the ADAURA hazard ratios in the nonmetastatic driver review outcomes measured by the review’s own newly enrolled cohort?

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../combined/v2/case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## o007

**direct_lookup · revision 2 · answerable**

What five-year OS results does the driver-altered nonmetastatic review attribute to ADAURA, distinguishing stage populations?

**Expected response**

Stage II–IIIA: osimertinib 85% versus placebo 73%, HR 0.49 (95.03% CI 0.33–0.73); overall stage IB–IIIA: 88% versus 78%, HR 0.49 (95.03% CI 0.34–0.70).

**Required claims**

- `f1`: Stage II–IIIA: osimertinib 85% versus placebo 73%, HR 0.49 (95.03% CI 0.33–0.73); overall stage IB–IIIA: 88% versus 78%, HR 0.49 (95.03% CI 0.34–0.70).

**Article roles declared by the question**

- Required: [PMC11431721](https://pmc.ncbi.nlm.nih.gov/articles/PMC11431721.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC11431721](https://pmc.ncbi.nlm.nih.gov/articles/PMC11431721.1/) | Review; attributed ADAURA five-year OS, stage-specific populations; p. 4 | `driver_os` |

**Response distinctions to preserve**

- Do not substitute another population or endpoint for Cited ADAURA stage II–IIIA versus IB–IIIA populations: Five-year OS.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../combined/v2/case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## o023

**multi_hop · revision 4 · answerable**

In the Gosney expert consensus, who initiates reflex NSCLC biomarker testing, what is agreed by the MDT, and is a formal oncologist request required? Explain the reported delay mechanism.

**Expected response**

The pathologist initiates an MDT-agreed prespecified biomarker panel without a formal oncologist request. Reporting delays risk deterioration and initiation of suboptimal therapy before complete status is known. This is expert consensus, not an intervention trial.

**Required claims**

- `f1`: The pathologist initiates an MDT-agreed prespecified biomarker panel without a formal oncologist request. Reporting delays risk deterioration and initiation of suboptimal therapy before complete status is known. This is expert consensus, not an intervention trial.

**Article roles declared by the question**

- Required: [PMC10485396](https://pmc.ncbi.nlm.nih.gov/articles/PMC10485396.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC10485396](https://pmc.ncbi.nlm.nih.gov/articles/PMC10485396.1/) | The case for change; definition of pathologist-initiated reflex testing; p. 2 | `reflex_def` |
| primary | f1 | [PMC10485396](https://pmc.ncbi.nlm.nih.gov/articles/PMC10485396.1/) | Introduction; delayed biomarker results, deterioration and suboptimal therapy; p. 2 | `reflex_delay` |

**Response distinctions to preserve**

- Do not substitute another population or endpoint for NSCLC diagnostic pathway: Ordering workflow and delay mechanism.
- Do not attribute the Gosney MDT-agreement, no-formal-request or delay details to POL-MOL; its reflex passage is partial support only.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../combined/v2/case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## o008

**direct_lookup · revision 2 · answerable**

Why does the reflex-testing consensus also argue for early testing in resectable NSCLC?

**Expected response**

ADAURA/adjuvant and emerging neoadjuvant targeted approaches make early EGFR identification important, in resected tissue or ideally an available presurgical specimen; the argument is not restricted to metastatic disease.

**Required claims**

- `f1`: ADAURA/adjuvant and emerging neoadjuvant targeted approaches make early EGFR identification important, in resected tissue or ideally an available presurgical specimen; the argument is not restricted to metastatic disease.

**Article roles declared by the question**

- Required: [PMC10485396](https://pmc.ncbi.nlm.nih.gov/articles/PMC10485396.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC10485396](https://pmc.ncbi.nlm.nih.gov/articles/PMC10485396.1/) | The case for change; early-stage resectable disease and EGFR testing; p. 2 | `reflex_early` |

**Response distinctions to preserve**

- Do not substitute another population or endpoint for Early-stage resectable NSCLC: Timing and rationale for EGFR testing.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../combined/v2/case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## o009

**multi_hop · revision 5 · answerable**

What CV-event estimates and study design did the observational NSCLC immunotherapy meta-analysis report?

**Expected response**

Twelve observational studies included 23,621 NSCLC patients; overall CV-event prevalence was 3%, a separate measure from the HR. Only four studies contributed to the pooled HR 1.78 (95% CI 1.46–2.17), I²=72%, comparing ICI with non-ICI treatment. Observational association is not proof of causation or CVD mortality.

**Required claims**

- `f1`: Twelve observational studies included 23,621 NSCLC patients; overall CV-event prevalence was 3%, a separate measure from the HR. Only four studies contributed to the pooled HR 1.78 (95% CI 1.46–2.17), I²=72%, comparing ICI with non-ICI treatment. Observational association is not proof of causation or CVD mortality.

**Article roles declared by the question**

- Required: [PMC11891047](https://pmc.ncbi.nlm.nih.gov/articles/PMC11891047.1/)
- Alternatives: [PMC11891047](https://pmc.ncbi.nlm.nih.gov/articles/PMC11891047.1/)
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC11891047](https://pmc.ncbi.nlm.nih.gov/articles/PMC11891047.1/) | Abstract; observational studies, CV prevalence and pooled hazard; p. 1 | `obs_cv` |
| primary | f1 | [PMC11891047](https://pmc.ncbi.nlm.nih.gov/articles/PMC11891047.1/) | Discussion; limitations: four studies contribute to HR; p. 14 | `obs_hr_scope` |
| results_with_hr_scope | f1 | [PMC11891047](https://pmc.ncbi.nlm.nih.gov/articles/PMC11891047.1/) | Results 3.2; twelve observational studies and 23,621 patients; p. 4 | `obs_population_results` |
| results_with_hr_scope | f1 | [PMC11891047](https://pmc.ncbi.nlm.nih.gov/articles/PMC11891047.1/) | Results 3.4.1; 3% prevalence (noncomparative measure despite source wording); p. 4 | `obs_prevalence_results` |
| results_with_hr_scope | f1 | [PMC11891047](https://pmc.ncbi.nlm.nih.gov/articles/PMC11891047.1/) | Results 3.4.2; ICI versus non-ICI overall HR; p. 4 | `obs_hr_results` |
| results_with_hr_scope | f1 | [PMC11891047](https://pmc.ncbi.nlm.nih.gov/articles/PMC11891047.1/) | Discussion; limitations: four studies contribute to HR; p. 14 | `obs_hr_scope` |

**Response distinctions to preserve**

- Do not substitute another population or endpoint for Observational NSCLC cohorts: CV-event prevalence and hazard.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../combined/v2/case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## o010

**direct_lookup · revision 2 · answerable**

In the lung-cancer RCT meta-analysis, how did single ICI and ICI plus chemotherapy compare with chemotherapy for cardiac adverse events?

**Expected response**

Thirty studies with 16,331 patients yielded RR 2.15 (95% CI 1.13–4.12) for single ICI and RR 1.38 (1.05–1.82) for ICI plus chemotherapy; both p=0.02. These are cardiac adverse events, not CVD mortality.

**Required claims**

- `f1`: Thirty studies with 16,331 patients yielded RR 2.15 (95% CI 1.13–4.12) for single ICI and RR 1.38 (1.05–1.82) for ICI plus chemotherapy; both p=0.02. These are cardiac adverse events, not CVD mortality.

**Article roles declared by the question**

- Required: [PMC11181582](https://pmc.ncbi.nlm.nih.gov/articles/PMC11181582.1/)
- Alternatives: [PMC11181582](https://pmc.ncbi.nlm.nih.gov/articles/PMC11181582.1/)
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC11181582](https://pmc.ncbi.nlm.nih.gov/articles/PMC11181582.1/) | Abstract; pooled RCT cardiac adverse events and subtype outcomes; p. 1 | `rct_cv` |
| results | f1 | [PMC11181582](https://pmc.ncbi.nlm.nih.gov/articles/PMC11181582.1/) | Results; 30 studies, 31 trials and 16,331 patients; p. 3 | `rct_population_results` |
| results | f1 | [PMC11181582](https://pmc.ncbi.nlm.nih.gov/articles/PMC11181582.1/) | Results; single ICI and ICI plus chemotherapy versus chemotherapy; p. 3 | `rct_primary_results` |

**Response distinctions to preserve**

- Do not substitute another population or endpoint for Lung-cancer RCT meta-analysis: Cardiac adverse-event risk.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../combined/v2/case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## o011

**false_premise · revision 2 · false_premise**

Does the RCT meta-analysis prove ICIs cannot cause heart failure because that subgroup result was nonsignificant?

**Expected response**

No. Heart-failure RR was 1.11 (95% CI 0.48–2.58), p=0.80. A nonsignificant imprecise estimate does not establish no risk; the broader cardiac-adverse-event comparisons were significant.

**Required claims**

- `f1`: No. Heart-failure RR was 1.11 (95% CI 0.48–2.58), p=0.80. A nonsignificant imprecise estimate does not establish no risk; the broader cardiac-adverse-event comparisons were significant.

**Article roles declared by the question**

- Required: [PMC11181582](https://pmc.ncbi.nlm.nih.gov/articles/PMC11181582.1/)
- Alternatives: [PMC11181582](https://pmc.ncbi.nlm.nih.gov/articles/PMC11181582.1/)
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC11181582](https://pmc.ncbi.nlm.nih.gov/articles/PMC11181582.1/) | Abstract; pooled RCT cardiac adverse events and subtype outcomes; p. 1 | `rct_cv` |
| results | f1 | [PMC11181582](https://pmc.ncbi.nlm.nih.gov/articles/PMC11181582.1/) | Results; nonsignificant imprecise cardiac-failure estimate; p. 3 | `rct_failure_results` |
| results | f1 | [PMC11181582](https://pmc.ncbi.nlm.nih.gov/articles/PMC11181582.1/) | Results; single ICI and ICI plus chemotherapy versus chemotherapy; p. 3 | `rct_primary_results` |

**Response distinctions to preserve**

- Do not substitute another population or endpoint for Lung-cancer RCT meta-analysis: Heart failure versus broader cardiac adverse events.

**Premise to correct:** Does the RCT meta-analysis prove ICIs cannot cause heart failure because that subgroup result was nonsignificant?

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../combined/v2/case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## o026

**direct_lookup · revision 2 · answerable**

Among deaths in the older advanced-NSCLC PD-1 cohort, what shares were attributed to NSCLC and CVD, and which factors were associated with CVD mortality?

**Expected response**

Of 3,746 deaths among 5,076 patients, 85.34% were NSCLC and 2.80% CVD. CHF history sHR 2.10 (95% CI 1.37–3.21) and Medicaid dual eligibility versus private insurance sHR 2.70 (1.28–5.56) were associated with CVD mortality. Percentages use deaths, not all patients.

**Required claims**

- `f1`: Of 3,746 deaths among 5,076 patients, 85.34% were NSCLC and 2.80% CVD. CHF history sHR 2.10 (95% CI 1.37–3.21) and Medicaid dual eligibility versus private insurance sHR 2.70 (1.28–5.56) were associated with CVD mortality. Percentages use deaths, not all patients.

**Article roles declared by the question**

- Required: [PMC12495207](https://pmc.ncbi.nlm.nih.gov/articles/PMC12495207.1/)
- Alternatives: [PMC12495207](https://pmc.ncbi.nlm.nih.gov/articles/PMC12495207.1/)
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC12495207](https://pmc.ncbi.nlm.nih.gov/articles/PMC12495207.1/) | Abstract; causes of death and Fine–Gray estimates; p. 1 | `mortality` |
| results | f1 | [PMC12495207](https://pmc.ncbi.nlm.nih.gov/articles/PMC12495207.1/) | Results; cohort and death counts, NSCLC death share and two CVD categories; p. 6 | `mortality_deaths_results` |
| results | f1 | [PMC12495207](https://pmc.ncbi.nlm.nih.gov/articles/PMC12495207.1/) | Results; Medicaid versus private insurance CVD mortality; p. 6 | `mortality_medicaid_results` |
| results | f1 | [PMC12495207](https://pmc.ncbi.nlm.nih.gov/articles/PMC12495207.1/) | Results; CHF-associated CVD and other-cause mortality; p. 6 | `mortality_chf_results` |

**Response distinctions to preserve**

- Do not substitute another population or endpoint for Older advanced-NSCLC PD-1 cohort: Cause-of-death shares and CVD mortality associations.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../combined/v2/case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## o012

**direct_lookup · revision 2 · answerable**

How did pembrolizumab versus nivolumab compare for cause-specific mortality in the older NSCLC cohort?

**Expected response**

CVD mortality was not significantly different, sHR 1.08 (95% CI 0.63–1.84); NSCLC mortality was lower with pembrolizumab, sHR 0.67 (0.60–0.74). These are associations between two PD-1 drugs, not comparison with untreated controls.

**Required claims**

- `f1`: CVD mortality was not significantly different, sHR 1.08 (95% CI 0.63–1.84); NSCLC mortality was lower with pembrolizumab, sHR 0.67 (0.60–0.74). These are associations between two PD-1 drugs, not comparison with untreated controls.

**Article roles declared by the question**

- Required: [PMC12495207](https://pmc.ncbi.nlm.nih.gov/articles/PMC12495207.1/)
- Alternatives: [PMC12495207](https://pmc.ncbi.nlm.nih.gov/articles/PMC12495207.1/)
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC12495207](https://pmc.ncbi.nlm.nih.gov/articles/PMC12495207.1/) | Abstract; causes of death and Fine–Gray estimates; p. 1 | `mortality` |
| results | f1 | [PMC12495207](https://pmc.ncbi.nlm.nih.gov/articles/PMC12495207.1/) | Results; comparator-specific CVD and NSCLC subdistribution HRs; p. 6 | `mortality_drug_results` |

**Response distinctions to preserve**

- Do not substitute another population or endpoint for Older advanced-NSCLC pembrolizumab versus nivolumab cohort: Cause-specific mortality.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../combined/v2/case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## q085

**direct_lookup · revision 3 · answerable**

How does the immune-exclusion definition review distinguish inflamed, desert and excluded tumors spatially?

**Expected response**

Inflamed tumors have lymphocytes in tumor parenchyma near tumor cells; desert tumors generally lack lymphocytes in both parenchyma and periphery; excluded tumors have immune cells confined to stroma without parenchymal penetration. The review notes inconsistent historical use of “cold.”

**Required claims**

- `f1`: Inflamed tumors have lymphocytes in tumor parenchyma near tumor cells; desert tumors generally lack lymphocytes in both parenchyma and periphery; excluded tumors have immune cells confined to stroma without parenchymal penetration. The review notes inconsistent historical use of “cold.”

**Article roles declared by the question**

- Required: [PMC10073666](https://pmc.ncbi.nlm.nih.gov/articles/PMC10073666.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC10073666](https://pmc.ncbi.nlm.nih.gov/articles/PMC10073666.1/) | Concept of immune exclusion; spatial phenotype distinctions; p. 2 | `exclusion` |

**Response distinctions to preserve**

- Do not substitute another population or endpoint for Tumor immune spatial phenotypes: Immune cell distribution.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../combined/v2/case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## o013

**false_premise · revision 3 · false_premise**

Does the immune-exclusion review establish a universal clinically validated numeric cutoff for every tumor?

**Expected response**

No. It identifies lack of consensus and often arbitrary cutoffs, compounded by tumor heterogeneity. It proposes outcome-linked cutoffs, assessment of multiple regions, and reporting infiltration and heterogeneity rather than a universal validated threshold.

**Required claims**

- `f1`: No. It identifies lack of consensus and often arbitrary cutoffs, compounded by tumor heterogeneity. It proposes outcome-linked cutoffs, assessment of multiple regions, and reporting infiltration and heterogeneity rather than a universal validated threshold.

**Article roles declared by the question**

- Required: [PMC10073666](https://pmc.ncbi.nlm.nih.gov/articles/PMC10073666.1/)
- Alternatives: [PMC10073666](https://pmc.ncbi.nlm.nih.gov/articles/PMC10073666.1/)
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC10073666](https://pmc.ncbi.nlm.nih.gov/articles/PMC10073666.1/) | Abstract; lack of consensus, cutoff and heterogeneity limitations; p. 1 | `exclusion_limits` |
| primary | f1 | [PMC10073666](https://pmc.ncbi.nlm.nih.gov/articles/PMC10073666.1/) | Proposed approach; outcome-linked cutoffs and multiple sampled regions; p. 7, 8 | `exclusion_solution` |
| alternative_1 | f1 | [PMC10073666](https://pmc.ncbi.nlm.nih.gov/articles/PMC10073666.1/) | Abstract; lack of consensus, cutoff and heterogeneity limitations; p. 1 | `exclusion_limits` |
| alternative_1 | f1 | [PMC10073666](https://pmc.ncbi.nlm.nih.gov/articles/PMC10073666.1/) | Conclusion; infiltration, heterogeneity and outcome-linked cutoffs; p. 9 | `exclusion_conclusion` |
| alternative_3 | f1 | [PMC10073666](https://pmc.ncbi.nlm.nih.gov/articles/PMC10073666.1/) | Discussion; no consensus, arbitrary cutoffs and heterogeneity; p. 7 | `exclusion_limits_discussion` |
| alternative_3 | f1 | [PMC10073666](https://pmc.ncbi.nlm.nih.gov/articles/PMC10073666.1/) | Conclusion; infiltration, heterogeneity and outcome-linked cutoffs; p. 9 | `exclusion_conclusion` |

**Response distinctions to preserve**

- Do not substitute another population or endpoint for Immune-exclusion definitions across tumors: Definition limitations and proposed improvements.

**Premise to correct:** Does the immune-exclusion review establish a universal clinically validated numeric cutoff for every tumor?

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../combined/v2/case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## o014

**direct_lookup · revision 2 · answerable**

In the ICD mini-review, what distinct dendritic-cell mechanisms are attributed to CALR, ATP and HMGB1?

**Expected response**

Surface CALR is an eat-me signal supporting phagocytosis; extracellular ATP activates P2RX7 and inflammasome signalling with IL-1β/IL-18; HMGB1 engages TLR4 to promote dendritic-cell maturation and antigen presentation. These are reviewed mechanisms, not a measured clinical treatment effect.

**Required claims**

- `f1`: Surface CALR is an eat-me signal supporting phagocytosis; extracellular ATP activates P2RX7 and inflammasome signalling with IL-1β/IL-18; HMGB1 engages TLR4 to promote dendritic-cell maturation and antigen presentation. These are reviewed mechanisms, not a measured clinical treatment effect.

**Article roles declared by the question**

- Required: [PMC13190586](https://pmc.ncbi.nlm.nih.gov/articles/PMC13190586.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC13190586](https://pmc.ncbi.nlm.nih.gov/articles/PMC13190586.1/) | ICD mechanisms; CALR, ATP, HMGB1 and dendritic-cell pathways; p. 3 | `icd_damp` |

**Response distinctions to preserve**

- Do not substitute another population or endpoint for Mechanistic ICD review: DAMP–dendritic cell pathways.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../combined/v2/case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## o015

**direct_lookup · revision 2 · answerable**

How does the ICD mini-review distinguish excluded, desert and immunosuppressed cold tumors?

**Expected response**

Excluded tumors retain immune cells at the periphery with failed penetration; desert tumors lack substantial infiltration; immunosuppressed tumors contain cells whose function is restrained by dominant suppressive signals.

**Required claims**

- `f1`: Excluded tumors retain immune cells at the periphery with failed penetration; desert tumors lack substantial infiltration; immunosuppressed tumors contain cells whose function is restrained by dominant suppressive signals.

**Article roles declared by the question**

- Required: [PMC13190586](https://pmc.ncbi.nlm.nih.gov/articles/PMC13190586.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC13190586](https://pmc.ncbi.nlm.nih.gov/articles/PMC13190586.1/) | Cold tumors; excluded, desert and immunosuppressed phenotypes; p. 2 | `icd_phenotype` |

**Response distinctions to preserve**

- Do not substitute another population or endpoint for Reviewed cold tumor phenotypes: Spatial versus functional immune barriers.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../combined/v2/case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## o016

**multi_hop · revision 2 · answerable**

How do the ICD review’s ER stress and autophagy pathways connect to the dendritic-cell effects of CALR and ATP?

**Expected response**

ER stress/PERK/eIF2α supports CALR exposure and an immunogenic state, while autophagy sustains ATP secretion; CALR supports dendritic-cell phagocytosis and ATP drives P2RX7/inflammasome signalling. This connects cellular stress to reviewed immune mechanisms, not proven clinical benefit.

**Required claims**

- `f1`: ER stress/PERK/eIF2α supports CALR exposure and an immunogenic state, while autophagy sustains ATP secretion; CALR supports dendritic-cell phagocytosis and ATP drives P2RX7/inflammasome signalling. This connects cellular stress to reviewed immune mechanisms, not proven clinical benefit.

**Article roles declared by the question**

- Required: [PMC13190586](https://pmc.ncbi.nlm.nih.gov/articles/PMC13190586.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC13190586](https://pmc.ncbi.nlm.nih.gov/articles/PMC13190586.1/) | ICD mechanisms; ER stress/PERK/eIF2α and autophagy; p. 3 | `icd_stress` |
| primary | f1 | [PMC13190586](https://pmc.ncbi.nlm.nih.gov/articles/PMC13190586.1/) | ICD mechanisms; CALR, ATP, HMGB1 and dendritic-cell pathways; p. 3 | `icd_damp` |

**Response distinctions to preserve**

- Do not substitute another population or endpoint for Mechanistic ICD pathways: Stress, DAMP release and dendritic-cell activation.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../combined/v2/case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## o030

**cross_doc_synthesis · revision 3 · answerable**

Combine the Hunan neoadjuvant study with the reflex-testing consensus: what does each contribute to interpreting perioperative NSCLC treatment and biomarker readiness?

**Expected response**

The resected Hunan cohort had higher MPR; unadjusted DFS significance disappeared after PSM. Two-year OS was 94.1% versus 85.7% in the unweighted population (p=0.012) and 93.8% versus 87.1% in a second comparison (p=0.038), PD-1 plus chemotherapy versus chemotherapy. The Limitations state that follow-up was too short to make OS the primary endpoint and that mature conclusions need longer follow-up, so these are not mature causal survival evidence. The consensus advocates pathologist-initiated MDT-agreed testing, identifies delays before complete biomarker status, and argues for early EGFR testing in resectable disease. It does not measure how testing caused the Hunan outcomes or establish a driver-positive treatment effect.

**Required claims**

- `f1`: The resected Hunan cohort had higher MPR; unadjusted DFS significance disappeared after PSM. Two-year OS was 94.1% versus 85.7% in the unweighted population (p=0.012) and 93.8% versus 87.1% in a second comparison (p=0.038), PD-1 plus chemotherapy versus chemotherapy. The Limitations state that follow-up was too short to make OS the primary endpoint and that mature conclusions need longer follow-up, so these are not mature causal survival evidence.
- `f2`: The consensus advocates pathologist-initiated MDT-agreed testing, identifies delays before complete biomarker status, and argues for early EGFR testing in resectable disease. It does not measure how testing caused the Hunan outcomes or establish a driver-positive treatment effect.

**Article roles declared by the question**

- Required: [PMC10485396](https://pmc.ncbi.nlm.nih.gov/articles/PMC10485396.1/), [PMC9844597](https://pmc.ncbi.nlm.nih.gov/articles/PMC9844597.1/)
- Alternatives: [PMC10485396](https://pmc.ncbi.nlm.nih.gov/articles/PMC10485396.1/), [PMC9844597](https://pmc.ncbi.nlm.nih.gov/articles/PMC9844597.1/)
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC9844597](https://pmc.ncbi.nlm.nih.gov/articles/PMC9844597.1/) | Abstract; unadjusted pathological response and DFS; p. 1 | `hunan_response` |
| primary | f1 | [PMC9844597](https://pmc.ncbi.nlm.nih.gov/articles/PMC9844597.1/) | Results 3.4; unadjusted DFS and loss of significance after PSM; p. 7 | `hunan_matched` |
| primary | f1 | [PMC9844597](https://pmc.ncbi.nlm.nih.gov/articles/PMC9844597.1/) | Results 3.4; unweighted and weighted two-year OS comparisons; p. 7 | `hunan_os_results` |
| primary | f1 | [PMC9844597](https://pmc.ncbi.nlm.nih.gov/articles/PMC9844597.1/) | Discussion; limitations: follow-up too short for OS endpoint; p. 12 | `hunan_os_limitation` |
| primary | f2 | [PMC10485396](https://pmc.ncbi.nlm.nih.gov/articles/PMC10485396.1/) | The case for change; definition of pathologist-initiated reflex testing; p. 2 | `reflex_def` |
| primary | f2 | [PMC10485396](https://pmc.ncbi.nlm.nih.gov/articles/PMC10485396.1/) | Introduction; delayed biomarker results, deterioration and suboptimal therapy; p. 2 | `reflex_delay` |
| primary | f2 | [PMC10485396](https://pmc.ncbi.nlm.nih.gov/articles/PMC10485396.1/) | The case for change; early-stage resectable disease and EGFR testing; p. 2 | `reflex_early` |
| results_response | f1 | [PMC9844597](https://pmc.ncbi.nlm.nih.gov/articles/PMC9844597.1/) | Results 3.3; unadjusted MPR and pCR; p. 7 | `hunan_mpr_results` |
| results_response | f1 | [PMC9844597](https://pmc.ncbi.nlm.nih.gov/articles/PMC9844597.1/) | Results 3.4; unadjusted DFS and loss of significance after PSM; p. 7 | `hunan_matched` |
| results_response | f1 | [PMC9844597](https://pmc.ncbi.nlm.nih.gov/articles/PMC9844597.1/) | Results 3.4; unweighted and weighted two-year OS comparisons; p. 7 | `hunan_os_results` |
| results_response | f1 | [PMC9844597](https://pmc.ncbi.nlm.nih.gov/articles/PMC9844597.1/) | Discussion; limitations: follow-up too short for OS endpoint; p. 12 | `hunan_os_limitation` |
| results_response | f2 | [PMC10485396](https://pmc.ncbi.nlm.nih.gov/articles/PMC10485396.1/) | The case for change; definition of pathologist-initiated reflex testing; p. 2 | `reflex_def` |
| results_response | f2 | [PMC10485396](https://pmc.ncbi.nlm.nih.gov/articles/PMC10485396.1/) | Introduction; delayed biomarker results, deterioration and suboptimal therapy; p. 2 | `reflex_delay` |
| results_response | f2 | [PMC10485396](https://pmc.ncbi.nlm.nih.gov/articles/PMC10485396.1/) | The case for change; early-stage resectable disease and EGFR testing; p. 2 | `reflex_early` |
| discussion_response | f1 | [PMC9844597](https://pmc.ncbi.nlm.nih.gov/articles/PMC9844597.1/) | Discussion; unadjusted pathological response; p. 8 | `hunan_mpr_discussion` |
| discussion_response | f1 | [PMC9844597](https://pmc.ncbi.nlm.nih.gov/articles/PMC9844597.1/) | Results 3.4; unadjusted DFS and loss of significance after PSM; p. 7 | `hunan_matched` |
| discussion_response | f1 | [PMC9844597](https://pmc.ncbi.nlm.nih.gov/articles/PMC9844597.1/) | Results 3.4; unweighted and weighted two-year OS comparisons; p. 7 | `hunan_os_results` |
| discussion_response | f1 | [PMC9844597](https://pmc.ncbi.nlm.nih.gov/articles/PMC9844597.1/) | Discussion; limitations: follow-up too short for OS endpoint; p. 12 | `hunan_os_limitation` |
| discussion_response | f2 | [PMC10485396](https://pmc.ncbi.nlm.nih.gov/articles/PMC10485396.1/) | The case for change; definition of pathologist-initiated reflex testing; p. 2 | `reflex_def` |
| discussion_response | f2 | [PMC10485396](https://pmc.ncbi.nlm.nih.gov/articles/PMC10485396.1/) | Introduction; delayed biomarker results, deterioration and suboptimal therapy; p. 2 | `reflex_delay` |
| discussion_response | f2 | [PMC10485396](https://pmc.ncbi.nlm.nih.gov/articles/PMC10485396.1/) | The case for change; early-stage resectable disease and EGFR testing; p. 2 | `reflex_early` |

**Response distinctions to preserve**

- Do not substitute another population or endpoint for Hunan resected cohort: Treatment outcomes and limitations.
- Do not substitute another population or endpoint for NSCLC testing consensus: Biomarker readiness and early-stage workflow.
- Do not describe a separate weighting method: the Methods describe PSM only, and the Results/Figure 1D labels conflict.

**Overlap review:** 53 other articles were considered; see the
[recorded dependency map](../combined/v2/case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## o017

**cross_doc_synthesis · revision 4 · answerable**

Why can the observational CV-event meta-analysis and older PD-1 cause-specific mortality cohort not be read as the same cardiovascular endpoint?

**Expected response**

The observational synthesis included twelve NSCLC studies, but only four contributed to HR 1.78 versus non-ICI treatment; overall CV-event prevalence 3% is a separate measure from the HR. The older cohort reports cause-specific deaths and compares pembrolizumab with nivolumab: CVD sHR 1.08 was nonsignificant. Different endpoints, populations and comparators prevent treating this as a contradiction or pooled causal estimate.

**Required claims**

- `f1`: The observational synthesis included twelve NSCLC studies, but only four contributed to HR 1.78 versus non-ICI treatment; overall CV-event prevalence 3% is a separate measure from the HR.
- `f2`: The older cohort reports cause-specific deaths and compares pembrolizumab with nivolumab: CVD sHR 1.08 was nonsignificant. Different endpoints, populations and comparators prevent treating this as a contradiction or pooled causal estimate.

**Article roles declared by the question**

- Required: [PMC11891047](https://pmc.ncbi.nlm.nih.gov/articles/PMC11891047.1/), [PMC12495207](https://pmc.ncbi.nlm.nih.gov/articles/PMC12495207.1/)
- Alternatives: [PMC11891047](https://pmc.ncbi.nlm.nih.gov/articles/PMC11891047.1/), [PMC12495207](https://pmc.ncbi.nlm.nih.gov/articles/PMC12495207.1/)
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC11891047](https://pmc.ncbi.nlm.nih.gov/articles/PMC11891047.1/) | Abstract; observational studies, CV prevalence and pooled hazard; p. 1 | `obs_cv` |
| primary | f1 | [PMC11891047](https://pmc.ncbi.nlm.nih.gov/articles/PMC11891047.1/) | Discussion; limitations: four studies contribute to HR; p. 14 | `obs_hr_scope` |
| primary | f2 | [PMC12495207](https://pmc.ncbi.nlm.nih.gov/articles/PMC12495207.1/) | Abstract; causes of death and Fine–Gray estimates; p. 1 | `mortality` |
| alternative_1 | f1 | [PMC11891047](https://pmc.ncbi.nlm.nih.gov/articles/PMC11891047.1/) | Abstract; observational studies, CV prevalence and pooled hazard; p. 1 | `obs_cv` |
| alternative_1 | f1 | [PMC11891047](https://pmc.ncbi.nlm.nih.gov/articles/PMC11891047.1/) | Discussion; limitations: four studies contribute to HR; p. 14 | `obs_hr_scope` |
| alternative_1 | f2 | [PMC12495207](https://pmc.ncbi.nlm.nih.gov/articles/PMC12495207.1/) | Results; comparator-specific CVD and NSCLC subdistribution HRs; p. 6 | `mortality_drug_results` |
| observational_results | f1 | [PMC11891047](https://pmc.ncbi.nlm.nih.gov/articles/PMC11891047.1/) | Results 3.2; twelve observational studies and 23,621 patients; p. 4 | `obs_population_results` |
| observational_results | f1 | [PMC11891047](https://pmc.ncbi.nlm.nih.gov/articles/PMC11891047.1/) | Results 3.4.1; 3% prevalence (noncomparative measure despite source wording); p. 4 | `obs_prevalence_results` |
| observational_results | f1 | [PMC11891047](https://pmc.ncbi.nlm.nih.gov/articles/PMC11891047.1/) | Results 3.4.2; ICI versus non-ICI overall HR; p. 4 | `obs_hr_results` |
| observational_results | f1 | [PMC11891047](https://pmc.ncbi.nlm.nih.gov/articles/PMC11891047.1/) | Discussion; limitations: four studies contribute to HR; p. 14 | `obs_hr_scope` |
| observational_results | f2 | [PMC12495207](https://pmc.ncbi.nlm.nih.gov/articles/PMC12495207.1/) | Abstract; causes of death and Fine–Gray estimates; p. 1 | `mortality` |
| both_results | f1 | [PMC11891047](https://pmc.ncbi.nlm.nih.gov/articles/PMC11891047.1/) | Results 3.2; twelve observational studies and 23,621 patients; p. 4 | `obs_population_results` |
| both_results | f1 | [PMC11891047](https://pmc.ncbi.nlm.nih.gov/articles/PMC11891047.1/) | Results 3.4.1; 3% prevalence (noncomparative measure despite source wording); p. 4 | `obs_prevalence_results` |
| both_results | f1 | [PMC11891047](https://pmc.ncbi.nlm.nih.gov/articles/PMC11891047.1/) | Results 3.4.2; ICI versus non-ICI overall HR; p. 4 | `obs_hr_results` |
| both_results | f1 | [PMC11891047](https://pmc.ncbi.nlm.nih.gov/articles/PMC11891047.1/) | Discussion; limitations: four studies contribute to HR; p. 14 | `obs_hr_scope` |
| both_results | f2 | [PMC12495207](https://pmc.ncbi.nlm.nih.gov/articles/PMC12495207.1/) | Results; comparator-specific CVD and NSCLC subdistribution HRs; p. 6 | `mortality_drug_results` |

**Response distinctions to preserve**

- Do not substitute another population or endpoint for Observational NSCLC cohorts: CV events.
- Do not substitute another population or endpoint for Older PD-1-treated advanced NSCLC: CVD mortality.

**Overlap review:** 53 other articles were considered; see the
[recorded dependency map](../combined/v2/case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## o018

**cross_doc_synthesis · revision 2 · answerable**

How should the Helsinki TNBC myocarditis frequency and lung-cancer RCT cardiac-adverse-event risks be compared?

**Expected response**

Helsinki reported 11/75 myocarditis cases (14.7%), no grade 3–4, with troponin monitoring each cycle. The lung-cancer synthesis reports comparator-relative broad cardiac-AE RRs (single ICI 2.15; plus chemotherapy 1.38). Different cancer populations, surveillance and endpoints preclude equating absolute myocarditis frequency with those RRs.

**Required claims**

- `f1`: Helsinki reported 11/75 myocarditis cases (14.7%), no grade 3–4, with troponin monitoring each cycle.
- `f2`: The lung-cancer synthesis reports comparator-relative broad cardiac-AE RRs (single ICI 2.15; plus chemotherapy 1.38). Different cancer populations, surveillance and endpoints preclude equating absolute myocarditis frequency with those RRs.

**Article roles declared by the question**

- Required: [PMC11181582](https://pmc.ncbi.nlm.nih.gov/articles/PMC11181582.1/), [PMC12931073](https://pmc.ncbi.nlm.nih.gov/articles/PMC12931073.1/)
- Alternatives: [PMC11181582](https://pmc.ncbi.nlm.nih.gov/articles/PMC11181582.1/), [PMC12931073](https://pmc.ncbi.nlm.nih.gov/articles/PMC12931073.1/)
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC12931073](https://pmc.ncbi.nlm.nih.gov/articles/PMC12931073.1/) | Abstract; immune adverse events and discontinuation denominators; p. 1 | `breast_ae` |
| primary | f1 | [PMC12931073](https://pmc.ncbi.nlm.nih.gov/articles/PMC12931073.1/) | Results; myocarditis grades and new troponin elevations; p. 6, 7 | `breast_cardio` |
| primary | f1 | [PMC12931073](https://pmc.ncbi.nlm.nih.gov/articles/PMC12931073.1/) | Methods; ECG, troponin surveillance and diagnostic criteria; p. 2 | `breast_monitor` |
| primary | f2 | [PMC11181582](https://pmc.ncbi.nlm.nih.gov/articles/PMC11181582.1/) | Abstract; pooled RCT cardiac adverse events and subtype outcomes; p. 1 | `rct_cv` |
| myocarditis_table | f1 | [PMC12931073](https://pmc.ncbi.nlm.nih.gov/articles/PMC12931073.1/) | Table 5; myocarditis count and zero severe events; p. 7 | `breast_cardio_table` |
| myocarditis_table | f1 | [PMC12931073](https://pmc.ncbi.nlm.nih.gov/articles/PMC12931073.1/) | Methods; ECG, troponin surveillance and diagnostic criteria; p. 2 | `breast_monitor` |
| myocarditis_table | f2 | [PMC11181582](https://pmc.ncbi.nlm.nih.gov/articles/PMC11181582.1/) | Abstract; pooled RCT cardiac adverse events and subtype outcomes; p. 1 | `rct_cv` |
| alternative_2 | f1 | [PMC12931073](https://pmc.ncbi.nlm.nih.gov/articles/PMC12931073.1/) | Abstract; immune adverse events and discontinuation denominators; p. 1 | `breast_ae` |
| alternative_2 | f1 | [PMC12931073](https://pmc.ncbi.nlm.nih.gov/articles/PMC12931073.1/) | Results; myocarditis grades and new troponin elevations; p. 6, 7 | `breast_cardio` |
| alternative_2 | f1 | [PMC12931073](https://pmc.ncbi.nlm.nih.gov/articles/PMC12931073.1/) | Methods; ECG, troponin surveillance and diagnostic criteria; p. 2 | `breast_monitor` |
| alternative_2 | f2 | [PMC11181582](https://pmc.ncbi.nlm.nih.gov/articles/PMC11181582.1/) | Results; single ICI and ICI plus chemotherapy versus chemotherapy; p. 3 | `rct_primary_results` |
| tables_and_results | f1 | [PMC12931073](https://pmc.ncbi.nlm.nih.gov/articles/PMC12931073.1/) | Table 5; myocarditis count and zero severe events; p. 7 | `breast_cardio_table` |
| tables_and_results | f1 | [PMC12931073](https://pmc.ncbi.nlm.nih.gov/articles/PMC12931073.1/) | Methods; ECG, troponin surveillance and diagnostic criteria; p. 2 | `breast_monitor` |
| tables_and_results | f2 | [PMC11181582](https://pmc.ncbi.nlm.nih.gov/articles/PMC11181582.1/) | Results; single ICI and ICI plus chemotherapy versus chemotherapy; p. 3 | `rct_primary_results` |

**Response distinctions to preserve**

- Do not substitute another population or endpoint for Helsinki TNBC cohort: Myocarditis frequency and surveillance.
- Do not substitute another population or endpoint for Lung-cancer RCT synthesis: Broad cardiac adverse-event relative risk.

**Overlap review:** 53 other articles were considered; see the
[recorded dependency map](../combined/v2/case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## o024

**cross_doc_distractor · revision 2 · answerable**

In the driver-altered NSCLC review’s stage II–IIIA ADAURA results, what absolute difference do the reported five-year OS rates imply between osimertinib and placebo, and what treatment setting does it describe?

**Expected response**

The cited stage II–IIIA ADAURA comparison reports five-year OS 85% with osimertinib versus 73% with placebo, an absolute difference of 12 percentage points (HR 0.49, 95.03% CI 0.33–0.73). This is adjuvant osimertinib in resected NSCLC, not first-line advanced afatinib mTTF by starting dose.

**Required claims**

- `f1`: The cited stage II–IIIA ADAURA comparison reports five-year OS 85% with osimertinib versus 73% with placebo, an absolute difference of 12 percentage points (HR 0.49, 95.03% CI 0.33–0.73). This is adjuvant osimertinib in resected NSCLC, not first-line advanced afatinib mTTF by starting dose.

**Article roles declared by the question**

- Required: [PMC11431721](https://pmc.ncbi.nlm.nih.gov/articles/PMC11431721.1/)
- Alternatives: None recorded.
- Decoys: [PMC10840225](https://pmc.ncbi.nlm.nih.gov/articles/PMC10840225.1/)

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC11431721](https://pmc.ncbi.nlm.nih.gov/articles/PMC11431721.1/) | Review; attributed ADAURA five-year OS, stage-specific populations; p. 4 | `driver_os` |
| primary | f1 | [PMC11431721](https://pmc.ncbi.nlm.nih.gov/articles/PMC11431721.1/) | Review; attributed initial ADAURA DFS results; p. 4 | `driver_dfs` |

**Why the distractors matter**

- [PMC10840225](https://pmc.ncbi.nlm.nih.gov/articles/PMC10840225.1/) — Both concern EGFR-directed NSCLC treatment and survival-like estimates.
  Advanced first-line afatinib mTTF by dose does not answer adjuvant osimertinib five-year OS.
  Passage: Results and Table 2; initial dose, mTTF and dose distribution; PDF p. 4; anchor `afatinib_ttf`.

**Response distinctions to preserve**

- Do not substitute another population or endpoint for Cited ADAURA trial: Five-year OS.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../combined/v2/case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## o025

**cross_doc_distractor · revision 3 · answerable**

For NSCLC MRD assessment in the Batra liquid-biopsy review, how do tumor-informed and tumor-agnostic assays compare at landmark and longitudinal timepoints?

**Expected response**

Tumor-informed versus tumor-agnostic landmark sensitivity is 42% versus 44%, longitudinal 76% versus 79%; specificity is 97% versus 93% and 96% versus 88%, respectively.

**Required claims**

- `f1`: Tumor-informed versus tumor-agnostic landmark sensitivity is 42% versus 44%, longitudinal 76% versus 79%; specificity is 97% versus 93% and 96% versus 88%, respectively.

**Article roles declared by the question**

- Required: [PMC13429855](https://pmc.ncbi.nlm.nih.gov/articles/PMC13429855.1/)
- Alternatives: None recorded.
- Decoys: [PMC11431721](https://pmc.ncbi.nlm.nih.gov/articles/PMC11431721.1/)

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC13429855](https://pmc.ncbi.nlm.nih.gov/articles/PMC13429855.1/) | MRD; cited landmark and longitudinal assay comparison; p. 5, 6 | `mrd` |

**Why the distractors matter**

- [PMC11431721](https://pmc.ncbi.nlm.nih.gov/articles/PMC11431721.1/) — Both concern postoperative ctDNA-MRD in resected NSCLC.
  Table 2 lists an ongoing adjuvant trial of ctDNA-MRD-guided osimertinib with a DFS endpoint; it reports no assay sensitivity or specificity and no tumor-informed versus tumor-agnostic comparison.
  Passage: Table 2; ongoing adjuvant trial with ctDNA-MRD-guided osimertinib; PDF p. 7; anchor `driver_mrd_trial`.

**Response distinctions to preserve**

- Do not substitute another population or endpoint for Cited NSCLC MRD assay studies: Sensitivity and specificity.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../combined/v2/case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## o020

**unanswerable · revision 2 · absent_fact**

How many Hunan patients failed to undergo surgery after starting neoadjuvant therapy, and why?

**Expected response**

No reference answer is recorded for this missing-fact case. Expected handling: Explain the study limitation without inventing a number.

**Article roles declared by the question**

- Required: None recorded.
- Alternatives: None recorded.
- Decoys: None recorded.

**Evidence:** No positive answer-evidence set is defined. See the
expected refusal and the recorded search scope below.

**Response distinctions to preserve**

- Do not infer the missing requested fact from a near-miss study or endpoint.

**Missing-fact search scope**

The cohort excludes those failing surgery, and discussion explicitly says their data were absent; do not infer an excluded-patient count from included treatment groups.

[PMC10073666](https://pmc.ncbi.nlm.nih.gov/articles/PMC10073666.1/), [PMC10485396](https://pmc.ncbi.nlm.nih.gov/articles/PMC10485396.1/), [PMC10770829](https://pmc.ncbi.nlm.nih.gov/articles/PMC10770829.1/), [PMC10840225](https://pmc.ncbi.nlm.nih.gov/articles/PMC10840225.1/), [PMC11181582](https://pmc.ncbi.nlm.nih.gov/articles/PMC11181582.1/), [PMC11431721](https://pmc.ncbi.nlm.nih.gov/articles/PMC11431721.1/), [PMC11547071](https://pmc.ncbi.nlm.nih.gov/articles/PMC11547071.1/), [PMC11891047](https://pmc.ncbi.nlm.nih.gov/articles/PMC11891047.1/), [PMC12495207](https://pmc.ncbi.nlm.nih.gov/articles/PMC12495207.1/), [PMC12931073](https://pmc.ncbi.nlm.nih.gov/articles/PMC12931073.1/), [PMC13190586](https://pmc.ncbi.nlm.nih.gov/articles/PMC13190586.1/), [PMC13429855](https://pmc.ncbi.nlm.nih.gov/articles/PMC13429855.1/), [PMC9239676](https://pmc.ncbi.nlm.nih.gov/articles/PMC9239676.1/), [PMC9844597](https://pmc.ncbi.nlm.nih.gov/articles/PMC9844597.1/)

Recorded search terms: failed to undergo, failed to receive surgery, excluded, surgery

**Overlap review:** 55 other articles were considered; see the
[recorded dependency map](../combined/v2/case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## o021

**false_premise · revision 4 · false_premise**

What randomized five-year pembrolizumab-versus-chemotherapy OS treatment effect did the Helsinki TNBC study measure?

**Expected response**

The Helsinki study retrospectively compares 75 consecutive pembrolizumab-treated TNBC patients with 102 nonmatched consecutive patients treated without pembrolizumab in preceding years. It is not randomized, so it cannot supply a randomized treatment effect. It reports no five-year OS: its survival endpoint is EFS by pCR within each cohort, with median follow-up of 22 months (range 9–31) in the pembrolizumab cohort and 35 months (range 2–53) in the cohort without pembrolizumab.

**Required claims**

- `f1`: The Helsinki study retrospectively compares 75 consecutive pembrolizumab-treated TNBC patients with 102 nonmatched consecutive patients treated without pembrolizumab in preceding years. It is not randomized, so it cannot supply a randomized treatment effect.
- `f2`: It reports no five-year OS: its survival endpoint is EFS by pCR within each cohort, with median follow-up of 22 months (range 9–31) in the pembrolizumab cohort and 35 months (range 2–53) in the cohort without pembrolizumab.

**Article roles declared by the question**

- Required: [PMC12931073](https://pmc.ncbi.nlm.nih.gov/articles/PMC12931073.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC12931073](https://pmc.ncbi.nlm.nih.gov/articles/PMC12931073.1/) | Abstract; retrospective pembrolizumab and nonmatched historical cohorts; p. 1 | `breast_pcr` |
| primary | f2 | [PMC12931073](https://pmc.ncbi.nlm.nih.gov/articles/PMC12931073.1/) | Results; EFS by pCR and median follow-up per cohort; p. 6 | `helsinki_followup` |

**Response distinctions to preserve**

- Do not substitute another population or endpoint for Helsinki TNBC cohorts: Design and limits of causal OS inference.
- Do not present EFS by pCR or cited KEYNOTE-522 OS as this study's five-year OS treatment effect.

**Premise to correct:** The Helsinki study measured a randomized five-year OS treatment effect of pembrolizumab versus chemotherapy.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../combined/v2/case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## q083

**unanswerable · revision 2 · absent_fact**

What FDA-validated early-stage sensitivity value for EarlyCDT-Lung is reported in the selected oncology corpus?

**Expected response**

No reference answer is recorded for this missing-fact case. Expected handling: Explain the study limitation without inventing a number.

**Article roles declared by the question**

- Required: None recorded.
- Alternatives: None recorded.
- Decoys: None recorded.

**Evidence:** No positive answer-evidence set is defined. See the
expected refusal and the recorded search scope below.

**Response distinctions to preserve**

- Do not infer the missing requested fact from a near-miss study or endpoint.

**Missing-fact search scope**

No selected source reports an FDA-validated early-stage sensitivity for EarlyCDT-Lung. The review describes an investigational autoantibody panel and setting-dependent study estimates, which do not establish the requested regulatory validation.

[PMC10073666](https://pmc.ncbi.nlm.nih.gov/articles/PMC10073666.1/), [PMC10485396](https://pmc.ncbi.nlm.nih.gov/articles/PMC10485396.1/), [PMC10770829](https://pmc.ncbi.nlm.nih.gov/articles/PMC10770829.1/), [PMC10840225](https://pmc.ncbi.nlm.nih.gov/articles/PMC10840225.1/), [PMC11181582](https://pmc.ncbi.nlm.nih.gov/articles/PMC11181582.1/), [PMC11431721](https://pmc.ncbi.nlm.nih.gov/articles/PMC11431721.1/), [PMC11547071](https://pmc.ncbi.nlm.nih.gov/articles/PMC11547071.1/), [PMC11891047](https://pmc.ncbi.nlm.nih.gov/articles/PMC11891047.1/), [PMC12495207](https://pmc.ncbi.nlm.nih.gov/articles/PMC12495207.1/), [PMC12931073](https://pmc.ncbi.nlm.nih.gov/articles/PMC12931073.1/), [PMC13190586](https://pmc.ncbi.nlm.nih.gov/articles/PMC13190586.1/), [PMC13429855](https://pmc.ncbi.nlm.nih.gov/articles/PMC13429855.1/), [PMC9239676](https://pmc.ncbi.nlm.nih.gov/articles/PMC9239676.1/), [PMC9844597](https://pmc.ncbi.nlm.nih.gov/articles/PMC9844597.1/)

Recorded search terms: EarlyCDT, FDA, autoantibod, validated

**Overlap review:** 55 other articles were considered; see the
[recorded dependency map](../combined/v2/case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## q100

**unanswerable · revision 2 · absent_fact**

What dual-screening rate for the Basque Country FIT programme is reported in the selected oncology corpus?

**Expected response**

No reference answer is recorded for this missing-fact case. Expected handling: Explain the study limitation without inventing a number.

**Article roles declared by the question**

- Required: None recorded.
- Alternatives: None recorded.
- Decoys: None recorded.

**Evidence:** No positive answer-evidence set is defined. See the
expected refusal and the recorded search scope below.

**Response distinctions to preserve**

- Do not infer the missing requested fact from a near-miss study or endpoint.

**Missing-fact search scope**

No selected article reports the requested Basque-programme dual-screening rate. The US BRFSS study is a different population and endpoint; generic FIT discussion does not supply the requested rate.

[PMC10073666](https://pmc.ncbi.nlm.nih.gov/articles/PMC10073666.1/), [PMC10485396](https://pmc.ncbi.nlm.nih.gov/articles/PMC10485396.1/), [PMC10770829](https://pmc.ncbi.nlm.nih.gov/articles/PMC10770829.1/), [PMC10840225](https://pmc.ncbi.nlm.nih.gov/articles/PMC10840225.1/), [PMC11181582](https://pmc.ncbi.nlm.nih.gov/articles/PMC11181582.1/), [PMC11431721](https://pmc.ncbi.nlm.nih.gov/articles/PMC11431721.1/), [PMC11547071](https://pmc.ncbi.nlm.nih.gov/articles/PMC11547071.1/), [PMC11891047](https://pmc.ncbi.nlm.nih.gov/articles/PMC11891047.1/), [PMC12495207](https://pmc.ncbi.nlm.nih.gov/articles/PMC12495207.1/), [PMC12931073](https://pmc.ncbi.nlm.nih.gov/articles/PMC12931073.1/), [PMC13190586](https://pmc.ncbi.nlm.nih.gov/articles/PMC13190586.1/), [PMC13429855](https://pmc.ncbi.nlm.nih.gov/articles/PMC13429855.1/), [PMC9239676](https://pmc.ncbi.nlm.nih.gov/articles/PMC9239676.1/), [PMC9844597](https://pmc.ncbi.nlm.nih.gov/articles/PMC9844597.1/)

Recorded search terms: Basque, FIT, dual-screen, Spain

**Overlap review:** 55 other articles were considered; see the
[recorded dependency map](../combined/v2/case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## q101

**false_premise · revision 3 · false_premise**

Are the HP2030 cervical and colorectal screening goals cited by Harper the study’s own achieved rates?

**Expected response**

No. The cited individual-screening goals are cervical 84.3% and CRC 74.4%, whereas the study reports observed dual screening 58.2%; targets, separate-screen rates and joint screening are different measures.

**Required claims**

- `f1`: No. The cited individual-screening goals are cervical 84.3% and CRC 74.4%, whereas the study reports observed dual screening 58.2%; targets, separate-screen rates and joint screening are different measures.

**Article roles declared by the question**

- Required: [PMC9239676](https://pmc.ncbi.nlm.nih.gov/articles/PMC9239676.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC9239676](https://pmc.ncbi.nlm.nih.gov/articles/PMC9239676.1/) | Discussion; cited HP2030 individual-screening goals versus observed dual screening; p. 11 | `screen_goals` |

**Response distinctions to preserve**

- Do not substitute another population or endpoint for HP2030 individual-screening targets versus US BRFSS cohort: Cited targets versus observed dual-screening rate.

**Premise to correct:** Cited population targets are study-achieved rates.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../combined/v2/case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## q078

**direct_lookup · revision 3 · answerable**

According to the liquid-biopsy review, how much does combining ctDNA with ctRNA analysis change gene-fusion detection yield compared with ctDNA alone, and what RNA-testing recommendation does the review connect to this?

**Expected response**

The review reports that combined ctDNA/ctRNA approaches increase fusion detection yield by approximately 28%–37% compared with ctDNA alone, citing several studies; ctRNA helps detect fusions and splice variants that DNA-based assays may miss. It notes that NCCN NSCLC guidelines recommend RNA-based testing when DNA-based profiling does not identify a driver oncogene.

**Required claims**

- `f1`: The review reports that combined ctDNA/ctRNA approaches increase fusion detection yield by approximately 28%–37% compared with ctDNA alone, citing several studies; ctRNA helps detect fusions and splice variants that DNA-based assays may miss. It notes that NCCN NSCLC guidelines recommend RNA-based testing when DNA-based profiling does not identify a driver oncogene.

**Article roles declared by the question**

- Required: [PMC13429855](https://pmc.ncbi.nlm.nih.gov/articles/PMC13429855.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC13429855](https://pmc.ncbi.nlm.nih.gov/articles/PMC13429855.1/) | Introduction; ctRNA and combined ctDNA/ctRNA fusion detection; p. 2 | `fusion_yield` |

**Response distinctions to preserve**

- Do not present the range as a single pooled estimate, as percentage points, or as the review's own measurement.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../combined/v2/case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## q097

**direct_lookup · revision 3 · answerable**

In the US dual-screening study's multinomial regression, what adjusted odds ratios were reported for college graduation and for the highest income level when predicting dual screening versus neither screen?

**Expected response**

For dual screening versus neither screen, college graduation versus less than high school had aOR 3.35 (95% CI 2.33–4.81) and income ≥$50K versus <$50K had aOR 3.32 (2.64–4.18).

**Required claims**

- `f1`: For dual screening versus neither screen, college graduation versus less than high school had aOR 3.35 (95% CI 2.33–4.81) and income ≥$50K versus <$50K had aOR 3.32 (2.64–4.18).

**Article roles declared by the question**

- Required: [PMC9239676](https://pmc.ncbi.nlm.nih.gov/articles/PMC9239676.1/)
- Alternatives: [PMC9239676](https://pmc.ncbi.nlm.nih.gov/articles/PMC9239676.1/)
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC9239676](https://pmc.ncbi.nlm.nih.gov/articles/PMC9239676.1/) | Results; multinomial regression, single or dual screening compared with neither screen (1a–1b); p. 6 | `screen_regression` |
| table4 | f1 | [PMC9239676](https://pmc.ncbi.nlm.nih.gov/articles/PMC9239676.1/) | Table 4; outcome referents, education and income rows; p. 9 | `screen_table4_predictors` |

**Response distinctions to preserve**

- Do not substitute the cervical-only aORs (college 2.02, income 2.19) or CRC-only aORs for the dual-versus-neither contrast.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../combined/v2/case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## q098

**direct_lookup · revision 3 · answerable**

In the US dual-screening study's adjusted analyses, how did the screening patterns of Black and Hispanic women differ, each compared with White women?

**Expected response**

Compared with White women and versus neither screen, Black women had aOR 2.25 (1.62–3.13) for dual screening and 1.73 (1.22–2.44) for cervical-only screening; Hispanic women had 1.68 (1.25–2.25) and 2.34 (1.72–3.18). Versus dual screening and compared with White women, Hispanic women had higher adjusted odds of cervical-only screening, aOR 1.39 (1.10–1.77), the only race group with significantly higher odds; Black women had lower odds, aOR 0.77 (0.64–0.92).

**Required claims**

- `f1`: Compared with White women and versus neither screen, Black women had aOR 2.25 (1.62–3.13) for dual screening and 1.73 (1.22–2.44) for cervical-only screening; Hispanic women had 1.68 (1.25–2.25) and 2.34 (1.72–3.18).
- `f2`: Versus dual screening and compared with White women, Hispanic women had higher adjusted odds of cervical-only screening, aOR 1.39 (1.10–1.77), the only race group with significantly higher odds; Black women had lower odds, aOR 0.77 (0.64–0.92).

**Article roles declared by the question**

- Required: [PMC9239676](https://pmc.ncbi.nlm.nih.gov/articles/PMC9239676.1/)
- Alternatives: [PMC9239676](https://pmc.ncbi.nlm.nih.gov/articles/PMC9239676.1/)
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1, f2 | [PMC9239676](https://pmc.ncbi.nlm.nih.gov/articles/PMC9239676.1/) | Table 4; outcome referents, White reference and race rows; p. 9 | `screen_table4_race` |
| results_subsections | f1 | [PMC9239676](https://pmc.ncbi.nlm.nih.gov/articles/PMC9239676.1/) | Results; multinomial regression, single or dual screening compared with neither screen (1a–1b); p. 6 | `screen_regression` |
| results_subsections | f2 | [PMC9239676](https://pmc.ncbi.nlm.nih.gov/articles/PMC9239676.1/) | Results 2a; Hispanic higher and Black lower cervical-only odds versus dual screening; p. 11 | `screen_hispanic_single` |

**Response distinctions to preserve**

- Do not present a direct Black-versus-Hispanic test; both are compared with White women.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../combined/v2/case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## q099

**direct_lookup · revision 3 · answerable**

What decision levels does the US dual-screening study's Discussion propose to explain why cervical and colorectal screening diverge with age?

**Expected response**

The Discussion proposes three levels. Physician level: the specialty seen (gynecologist versus primary care) may shape which screen is offered, as preventive gynecologist visits drop by about 90% from age 45. Patient level: after menopause a woman may stop speculum-based cervical screening, and may wait until 65 to start CRC screening, when Medicare visits discuss it. Health-system level: systems can drive screening, as with mailed FIT during COVID and home-based CRC tests.

**Required claims**

- `f1`: The Discussion proposes three levels. Physician level: the specialty seen (gynecologist versus primary care) may shape which screen is offered, as preventive gynecologist visits drop by about 90% from age 45. Patient level: after menopause a woman may stop speculum-based cervical screening, and may wait until 65 to start CRC screening, when Medicare visits discuss it. Health-system level: systems can drive screening, as with mailed FIT during COVID and home-based CRC tests.

**Article roles declared by the question**

- Required: [PMC9239676](https://pmc.ncbi.nlm.nih.gov/articles/PMC9239676.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC9239676](https://pmc.ncbi.nlm.nih.gov/articles/PMC9239676.1/) | Discussion; physician, patient and health-system decision levels; p. 11, 12 | `screen_levels` |

**Response distinctions to preserve**

- Do not present the hypothesised decision levels as tested study results.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../combined/v2/case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)
