# Oncology v1 decision record

This record explains every article, case and migration decision in this release. It is generated from
[manifest.json](manifest.json), [candidate_log.json](candidate_log.json), [queries.json](queries.json),
[legacy_audit.json](legacy_audit.json) and [revision_ledger.json](revision_ledger.json), which remain the
sources of truth. Regenerate it from the repository root with `.venv/bin/python benchmark/oncology/v1/render_decisions.py`.
[REVIEW.md](REVIEW.md) records the independent review rounds.

## Open decisions

None.

### Resolved

- **q078**: Restored on 2026-10-02 at Juan's request after the original author confirmed no case-specific retirement reason; revised on the retained source with pinned evidence.
  - Original author's rationale: No case-specific reason for this retirement was recorded, and I cannot substantiate one from the audit history. I recommend restoring q078 with pinned evidence from the retained liquid-biopsy review for the approximately 28%–37% fusion-yield gain from combined ctDNA/ctRNA analysis.
- **q097**: Restored on 2026-10-02 at Juan's request after the original author confirmed no case-specific retirement reason; revised on the retained source with pinned evidence.
  - Original author's rationale: No case-specific reason for this retirement was recorded, and I cannot substantiate one from the audit history. I recommend restoring q097 with pinned evidence from the retained screening study for the multinomial-regression adjusted odds ratios for college graduation and highest income.
- **q098**: Restored on 2026-10-02 at Juan's request after the original author confirmed no case-specific retirement reason; revised on the retained source with pinned evidence.
  - Original author's rationale: No case-specific reason for this retirement was recorded, and I cannot substantiate one from the audit history. I recommend restoring q098 with pinned evidence from the retained screening study for Hispanic versus Black women’s screening patterns, preserving the reported comparison groups.
- **q099**: Restored on 2026-10-02 at Juan's request after the original author confirmed no case-specific retirement reason; revised on the retained source with pinned evidence.
  - Original author's rationale: No case-specific reason for this retirement was recorded, and I cannot substantiate one from the audit history. I recommend restoring q099 with pinned evidence from the retained screening study’s Discussion for its individual, clinician and health-system levels of age-driven screening decision-making.

## Decision principles

- **Eligibility:** Only exactly CC BY 4.0 or CC0 1.0 articles with a pinned PMC version, verified PDF and clear third-party review are selected (STANDARDS gates 1–6). NC/ND licences are rejected. Articles crediting BioRender figures are deferred, because complete-PDF reuse rights are unresolved. Resemblance to BioRender artwork without a credit is not treated as a blocker.
- **Coverage, not counts:** No fixed article or case count. Articles were chosen for evidence relationships: same intervention in different populations, response versus survival, adjusted versus unadjusted results, cited-trial attribution, and competing cardio-oncology endpoints. Cases were authored from full text before any retrieval run.
- **Legacy migration:** All five legacy articles and 42 legacy cases are accounted for. Two articles are retained after re-verification; three are replaced or deferred. A legacy ID is kept only when its task stays on the same source family and the ledger notes any task change. Changed study-specific tasks get new oncology-local o-IDs. Replacement links are kept only when the new case tests the same evidence type or reasoning task; topic similarity alone is not enough.
- **Source conflicts:** Internal source conflicts are made explicit in gold and accepted when attributed: Hunan weighted/PSM label, Zhongshan narrative/table MPR, Vietnam abstract/Table 2 dose shares, Helsinki discontinuation denominators and the screening flow diagram. Gold never invents a reconciliation.
- **Answerability:** Absent facts are scoped to the whole selected oncology corpus and record near-miss context. False premises need positive correction anchors. Combined-corpus negative claims are rechecked in JUA-114.
- **Near-duplicates:** A strict subset or duplicate of another case is withdrawn (q082, o019; legacy q084). Overlapping cases are retained only with a distinct failure mode, recorded per case below.
- **Categories:** Categories follow STANDARDS: a direct lookup uses one local passage, and separated passages in one article make a case multi-hop. o009 and o023 were recategorised for this reason.
- **Evidence budget:** Every evidence case must be completely retrievable at n=8. Where a required span would exceed that, the fact is tested in a companion case instead (o030 attributes the Hunan OS label conflict that o029 requires).
- **Conditions:** C1 is the exact answer-source union; C2 adds POL-MOL as competition; C3 is an oncology-only placeholder until JUA-114.
- **Provenance honesty:** Each article's search string is labelled legacy, topical or targeted lookup. Unpreserved discovery queries are stated as unpreserved, not reconstructed.
- **No tuning exposure:** No retrieval output, generated answer or paid call informed selection or gold. Two Claude reviews (8b1adbe, a226bba) drove the recorded corrections.

## Legacy articles

| Legacy file | PMCID | Licence | Disposition |
| --- | --- | --- | --- |
| onco-breast-immunotherapy.pdf | PMC13438349 | CC BY-NC 4.0 | replace_restricted |
| onco-lung-liquidbiopsy.pdf | PMC13429855 | CC BY 4.0 | retain_verified_cc_by |
| onco-colorectal-screening.pdf | PMC9239676 | CC BY 4.0 | retain_verified_cc_by |
| onco-tumor-microenvironment.pdf | PMC13430506 | CC BY 4.0 | defer_third_party_terms |
| onco-genomics-precision-medicine.pdf | PMC13434091 | CC BY-NC 4.0 | replace_restricted |

## Selected articles

### PMC13429855 — onco-lung-liquidbiopsy

*Liquid biopsy biomarkers for cancer detection, treatment monitoring, and clinical outcome prediction*

- **Why selected:** Retained legacy article after re-verifying CC BY 4.0, version and PDF. A dense review of cited liquid-biopsy evidence (CSF ctDNA, NILE, LDCT versus MCED, MRD assays, EarlyCDT), so it supports attribution-to-cited-study cases and a scoped absent fact.
- **Answer source for:** q079, q080, q081, o025, q078
- **Named decoy for:** none
- **Partial-support overlap for:** none
- **Conditions:** C1, C2, C3
- **Search provenance:** legacy_manifest — Discovery query preserved verbatim from the legacy corpus_manifest.json record. Search strings are not eligibility evidence.

### PMC9239676 — onco-colorectal-screening

*US women screen at low rates for both cervical and colorectal cancers than a single cancer: a cross-sectional population-based observational study*

- **Why selected:** Retained legacy article after re-verification. The only screening source: mutually exclusive screening categories, printed flow-diagram counts with internal inconsistencies, and cited targets versus observed rates.
- **Answer source for:** q095, q096, q102, q101, q097, q098, q099
- **Named decoy for:** none
- **Partial-support overlap for:** none
- **Conditions:** C1, C2, C3
- **Search provenance:** legacy_manifest — Discovery query preserved verbatim from the legacy corpus_manifest.json record. Search strings are not eligibility evidence.

### PMC9844597 — onco-nsclc-neoadjuvant-hunan

*A real‐world comparison between neoadjuvant chemoimmunotherapy and chemotherapy alone for resectable non‐small cell lung cancer*

- **Why selected:** Replaces the restricted perioperative NSCLC study. A resected real-world cohort with unadjusted versus PSM DFS, MPR, OS comparisons with conflicting labels, and a resected-only selection restriction. Treatment partner for the q117 synthesis replacement (o030).
- **Answer source for:** o022, o029, o028, o030
- **Named decoy for:** none
- **Partial-support overlap for:** none
- **Conditions:** C1, C2, C3
- **Search provenance:** targeted_lookup — Quoted title-phrase lookup for this article; it also returned PMC10770829. The original topical discovery query was not preserved. Search strings are not eligibility evidence.

### PMC10770829 — onco-nsclc-neoadjuvant-stageiii

*Comparison of neoadjuvant chemoimmunotherapy and chemotherapy alone for resectable stage III non-small cell lung cancer: a real-world cohort study*

- **Why selected:** Second neoadjuvant chemoimmunotherapy cohort (stage III, EGFR/ALK-negative). Same intervention as Hunan in a different population, so the two compete realistically; it adds a response gain with nonsignificant DFS and a narrative/table MPR conflict.
- **Answer source for:** o001, o002
- **Named decoy for:** none
- **Partial-support overlap for:** none
- **Conditions:** C1, C2, C3
- **Search provenance:** targeted_lookup — Recorded string is the PMC9844597 title-phrase lookup that also returned this article. The original topical discovery query was not preserved. Search strings are not eligibility evidence.

### PMC12931073 — onco-breast-pembrolizumab-helsinki

*Real-world outcome of neoadjuvant therapy with or without pembrolizumab for triple-negative breast cancer*

- **Why selected:** Actual breast immunotherapy evidence, replacing the mislabelled legacy breast file. Nonmatched historical cohorts, myocarditis surveillance and discontinuation denominators; also a cardio-oncology source.
- **Answer source for:** o003, o004, o005, o018, o021
- **Named decoy for:** none
- **Partial-support overlap for:** none
- **Conditions:** C1, C2, C3
- **Search provenance:** topical_search — Topical search string recorded during the JUA-112 audit; it contains no publication-specific values. The "4.0" term filters for the licence notice. Search strings are not eligibility evidence.

### PMC10840225 — onco-afatinib-vietnam

*A real-world cohort study of first-line afatinib in patients with EGFR-mutant advanced non-small cell lung cancer in Vietnam*

- **Why selected:** Advanced EGFR-mutant first-line afatinib cohort. Separates ORR from time to treatment failure by starting dose and contains an abstract/Table 2 dose-share reversal. Replaces the restricted source's afatinib-dosing coverage and serves as the o024 decoy.
- **Answer source for:** o027, o006
- **Named decoy for:** o024
- **Partial-support overlap for:** none
- **Conditions:** C1, C2, C3
- **Search provenance:** targeted_lookup — Lookup with publication-specific values ("Vietnam", "21.5", "37.9"). The original topical discovery query was not preserved. Search strings are not eligibility evidence.

### PMC11891047 — onco-ici-cv-observational

*Cardiovascular toxicity induced by immunotherapy in non-small cell lung cancer: a systematic review and meta-analysis of observational studies*

- **Why selected:** Observational meta-analysis of cardiovascular events with ICIs in NSCLC: noncomparative prevalence versus a pooled HR from only four studies. Needed for cardio-oncology endpoint distinctions.
- **Answer source for:** o009, o017
- **Named decoy for:** none
- **Partial-support overlap for:** none
- **Conditions:** C1, C2, C3
- **Search provenance:** targeted_lookup — Lookup with a publication-specific value ("4.602") that also returned PMC11181582. The original topical discovery query was not preserved. Search strings are not eligibility evidence.

### PMC11181582 — onco-ici-cardiac-rct-meta

*Immune checkpoint inhibitor-induced cardiotoxicity in patients with lung cancer: a systematic review and meta-analysis*

- **Why selected:** RCT meta-analysis of ICI cardiotoxicity in lung cancer: comparator-relative cardiac adverse-event RRs and a null, imprecise heart-failure subgroup.
- **Answer source for:** o010, o011, o018
- **Named decoy for:** none
- **Partial-support overlap for:** none
- **Conditions:** C1, C2, C3
- **Search provenance:** targeted_lookup — Recorded string is a lookup with a publication-specific value ("4.602") that also returned this article. The original topical discovery query was not preserved. Search strings are not eligibility evidence.

### PMC11431721 — onco-driver-nonmetastatic-review

*Management of Non-Metastatic Non-Small Cell Lung Cancer (NSCLC) with Driver Gene Alterations: An Evolving Scenario*

- **Why selected:** Review of nonmetastatic driver-altered NSCLC that attributes ADAURA results by stage population. Supports attribution and stage-scope cases and supplies the ctDNA-MRD trial row used as the o025 decoy.
- **Answer source for:** q108, o007, o024
- **Named decoy for:** o025
- **Partial-support overlap for:** none
- **Conditions:** C1, C2, C3
- **Search provenance:** topical_search — Topical search string recorded during the JUA-112 audit; it contains no publication-specific values. Search strings are not eligibility evidence.

### PMC11547071 — onco-polmol-testing

*The Detailed Analysis of Polish Patients with Non-Small Cell Lung Cancer Through Insights from Molecular Testing (POL-MOL Study)*

- **Why selected:** Additional competition only (C2): POL-MOL describes pathologist-ordered testing of agreed biomarkers, which overlaps the Gosney consensus. No case uses it as an answer; it is recorded as partial support so that attribution to the consensus is tested.
- **Answer source for:** none (competition only)
- **Named decoy for:** none
- **Partial-support overlap for:** o023, o030
- **Conditions:** C2, C3
- **Search provenance:** targeted_lookup — Lookup with an author name ("Marjanski"). The original topical discovery query was not preserved. Search strings are not eligibility evidence.

### PMC10485396 — onco-reflex-biomarker-consensus

*Pathologist-initiated reflex testing for biomarkers in non-small-cell lung cancer: expert consensus on the rationale and considerations for implementation*

- **Why selected:** Gosney expert consensus on pathologist-initiated reflex testing: workflow, delays and early-stage EGFR testing. Real-world readiness partner for the q117 synthesis replacement (o030).
- **Answer source for:** o023, o008, o030
- **Named decoy for:** none
- **Partial-support overlap for:** none
- **Conditions:** C1, C2, C3
- **Search provenance:** topical_search — Topical search string recorded during the JUA-112 audit; it contains no publication-specific values. The "4.0" term filters for the licence notice. Search strings are not eligibility evidence.

### PMC13190586 — onco-icd-cold-tumor-review

*Immunogenic cell death in cold tumors: transforming immune-excluded tumors into immunotherapy-sensitive lesions*

- **Why selected:** ICD mini-review on cold phenotypes and danger signals. Replaces the deferred microenvironment coverage with mechanistic content; cited trial claims were deliberately not used as efficacy gold. Its notice, captions and credits show no BioRender credit.
- **Answer source for:** o014, o015, o016
- **Named decoy for:** none
- **Partial-support overlap for:** none
- **Conditions:** C1, C2, C3
- **Search provenance:** topical_search — Topical search string recorded during the JUA-112 audit; it contains no publication-specific values. The same string also returned PMC10073666. Search strings are not eligibility evidence.

### PMC10073666 — onco-immune-exclusion-definition

*Towards a consensus definition of immune exclusion in cancer*

- **Why selected:** Consensus-definition review of immune exclusion: spatial phenotypes, arbitrary cutoffs and heterogeneity. Competes with the ICD review's phenotype definitions.
- **Answer source for:** q085, o013
- **Named decoy for:** none
- **Partial-support overlap for:** none
- **Conditions:** C1, C2, C3
- **Search provenance:** topical_search — Topical search string recorded during the JUA-112 audit; it contains no publication-specific values. The same string also returned PMC13190586. Search strings are not eligibility evidence.

### PMC12495207 — onco-pd1-cause-specific-mortality

*Factors Associated With Cause-specific Mortality in Older Patients With Advanced NSCLC Treated With PD-1 Inhibitors: A U.S. Population-based Cohort Study*

- **Why selected:** Older advanced-NSCLC PD-1 cohort with competing-risk cause-specific mortality. Replaces the restricted source's CVD-mortality coverage and keeps mortality distinct from cardiac events.
- **Answer source for:** o026, o012, o017
- **Named decoy for:** none
- **Partial-support overlap for:** none
- **Conditions:** C1, C2, C3
- **Search provenance:** targeted_lookup — Lookup with a publication-specific term ("Medicaid dual eligibility"). The original topical discovery query was not preserved. Search strings are not eligibility evidence.

## Candidates not selected

| PMCID | Title | Disposition | Reason |
| --- | --- | --- | --- |
| PMC10000935 | Assessment of Barriers and Challenges to Screening, Diagnosis, and Biomarker Testing in Early-Stage Lung Cancer | deferred_third_party_terms | BioRender credit identified; complete-PDF reuse terms unresolved. |
| PMC10239871 | Cancer immune exclusion: breaking the barricade for a successful immunotherapy | deferred_third_party_terms | BioRender credit identified; complete-PDF reuse terms unresolved. |
| PMC12491816 | Temporal trends in treatment-related cardiopulmonary disease-specific mortality in NSCLC based on pathological subtypes: a retrospective population-based cohort study | rejected_project_licence_policy | NC/ND fails CC BY 4.0/CC0 selection policy. |
| PMC12603450 | Strategies for improving biomarker testing rates in non-small cell lung cancer in north America: a scoping review | rejected_project_licence_policy | NC/ND fails CC BY 4.0/CC0 selection policy. |
| PMC12608942 | The Evolving Interplay Between Targeted Therapy and Surgery for Resectable Lung Cancer | not_selected_redundant_or_lower_priority | Not acquired: its main relationship (targeted therapy and surgery in resectable disease) is already supplied by selected PMC11431721 and PMC10485396, which also passed every eligibility gate. Its own eligibility was not certified. Basis recorded post hoc on 2026-10-02 from titles and selected coverage; the original author recorded only a generic redundancy reason. |
| PMC12758337 | Trends in initial primary treatment approach and biomarker testing across social determinants of health in early-stage non-small cell lung cancer | rejected_project_licence_policy | NC/ND fails CC BY 4.0/CC0 selection policy. |
| PMC12883722 | State of the art of perioperative assessment in early non-small-cell lung cancer in Poland in the emerging era of perioperative protocols | rejected_project_licence_policy | NC/ND fails CC BY 4.0/CC0 selection policy. |
| PMC13186651 | Assessing current diagnostic, staging, and treatment practices in community and academic centers for individuals with stage IB–IIIA non-small cell lung cancer | rejected_project_licence_policy | NC/ND fails CC BY 4.0/CC0 selection policy. |
| PMC13378168 | Standardized protocols for reflexing to a multigene panel for patients with non–small cell lung cancer: prevalence and perceived barriers to comprehensive, pathologist-ordered biomarker reflex testing | rejected_project_licence_policy | NC/ND fails CC BY 4.0/CC0 selection policy. |
| PMC13430506 | Turning Cold Tumors Into Hot Tumors: Implications for Cancer Therapy | deferred_third_party_terms | BioRender credit identified; complete-PDF reuse terms unresolved. |
| PMC13434091 | Lung cancer across borders: From molecular epidemiology to precision treatment strategies | rejected_project_licence_policy | NC/ND fails CC BY 4.0/CC0 selection policy. |
| PMC13438349 | Real-world analysis of perioperative strategies for driver gene-positive resectable non-small cell lung cancer | rejected_project_licence_policy | NC/ND fails CC BY 4.0/CC0 selection policy. |
| PMC7873485 | Next Generation Imaging Techniques to Define Immune Topographies in Solid Tumors | not_selected_redundant_or_lower_priority | Not acquired: its main relationship (spatial immune topography definitions) is already supplied by selected PMC10073666 and PMC13190586, which also passed every eligibility gate. Its own eligibility was not certified. Basis recorded post hoc on 2026-10-02 from titles and selected coverage; the original author recorded only a generic redundancy reason. |
| PMC9316935 | Stakeholders Perceptions of Barriers to Precision Medicine Adoption in the United States | not_selected_redundant_or_lower_priority | Not acquired: its main relationship (barriers to precision-medicine and biomarker-testing adoption) is already supplied by selected PMC10485396 and PMC11547071, which also passed every eligibility gate. Its own eligibility was not certified. Basis recorded post hoc on 2026-10-02 from titles and selected coverage; the original author recorded only a generic redundancy reason. |

## Active cases

### direct_lookup (19)

#### q079 (revision 2)

> According to the liquid-biopsy review, distinguish the pooled CSF ctDNA detection rate from sensitivity and specificity for CNS metastases in NSCLC, and compare detection with cytology.

- **Why this case:** Tests separating the cited meta-analysis's pooled CSF ctDNA detection rate (versus cytology) from its sensitivity and specificity, which are different diagnostic measures. Direct lookup: one passage holds all values.
- **Evidence:** csf
- **Near-duplicate review:** Shares no evidence anchor with another case; the question identifies the source without disclosing target values. Absorbs retired legacy q084, whose detection-rate fact is required here.

#### q080 (revision 2)

> What did the liquid-biopsy review report about plasma versus tissue testing in NILE, including turnaround and biomarker identification?

- **Why this case:** Tests attributing NILE plasma-versus-tissue results to the cited trial population (untreated metastatic NSCLC), including noninferiority, biomarker identification and turnaround. Direct lookup: one passage.
- **Evidence:** nile
- **Near-duplicate review:** Shares no evidence anchor with another case; the question identifies the source without disclosing target values.

#### q095 (revision 2)

> What four mutually exclusive screening categories and percentages did the US dual-screening study report for women ages 50–64?

- **Why this case:** Tests reporting the study's four mutually exclusive screening categories and not treating dual screening as the CRC screening rate. Direct lookup: one table passage.
- **Evidence:** screen
- **Near-duplicate review:** Shares the screen anchor with q096 and the q100 negative context. Distinct: q095 asks for the category distribution; q096 asks for a derived comparison; q100 is an absent-fact near miss.

#### q096 (revision 2)

> In the US dual-screening study, how much more common was cervical-only than CRC-only screening?

- **Why this case:** Tests a derived comparison between the mutually exclusive cervical-only and CRC-only categories (about fivefold) rather than overall single-cancer rates. Direct lookup: one passage, light arithmetic.
- **Evidence:** screen
- **Near-duplicate review:** Near-duplicate of q095 (same anchor). Retained for a distinct failure mode: comparing mutually exclusive categories correctly. The question does not disclose either percentage.

#### q102 (revision 2)

> What hysterectomy exclusion and final analysis-group counts appear in the US dual-screening study’s Appendix 1 flow diagram?

- **Why this case:** Tests reporting printed flow-diagram counts without silently correcting the diagram's inconsistent subtraction or age label. Direct lookup on a figure; exercises figure extraction.
- **Evidence:** flow
- **Near-duplicate review:** Shares no evidence anchor with another case; the question identifies the source without disclosing target values.

#### o022 (revision 1)

> What population and treatment-group sizes were included in the Hunan neoadjuvant NSCLC cohort, and what surgical-selection restriction matters?

- **Why this case:** Tests population size, treatment-group counts and the surgical-selection restriction (resected patients only) that limits generalisation. Replaces legacy q103's population/group-size coverage on an eligible study. Direct lookup: one passage.
- **Evidence:** hunan_population
- **Near-duplicate review:** Shares no evidence anchor with another case; the question identifies the source without disclosing target values.
- **Replaces coverage of:** legacy q103

#### o028 (revision 1)

> What unadjusted MPR rates did the Hunan cohort report for PD-1 plus chemotherapy versus chemotherapy alone?

- **Why this case:** Tests endpoint separation: unadjusted MPR rates are pathological responses, not DFS. Replaces legacy q105's response-rate coverage. Direct lookup: one passage.
- **Evidence:** hunan_response
- **Near-duplicate review:** Shares hunan_response with o029 and o030, which use it for DFS context and state only "higher MPR". o028 alone asks for the MPR values.
- **Replaces coverage of:** legacy q105

#### o003 (revision 1)

> How did pCR and study design differ between the Helsinki pembrolizumab and historical chemotherapy TNBC cohorts?

- **Why this case:** Tests TNBC pCR by cohort with the design caveat (retrospective, nonmatched historical comparator), so the difference is not a randomized effect. Actual breast immunotherapy evidence replaces the mislabelled legacy file. Direct lookup: one abstract passage.
- **Evidence:** breast_pcr
- **Near-duplicate review:** Shares breast_pcr with o021. Distinct: o003 asks pCR values; o021 is a false-premise correction about randomized five-year OS.

#### o007 (revision 1)

> What five-year OS results does the driver-altered nonmetastatic review attribute to ADAURA, distinguishing stage populations?

- **Why this case:** Tests stage-population-specific five-year OS attributed to ADAURA (stage II–IIIA versus IB–IIIA), with HR and CI. Direct lookup: one passage.
- **Evidence:** driver_os
- **Near-duplicate review:** Shares driver_os with o024. Distinct: o024 derives the absolute difference for one stage population, identifies the adjuvant setting and must outrank an afatinib decoy.

#### o008 (revision 1)

> Why does the reflex-testing consensus also argue for early testing in resectable NSCLC?

- **Why this case:** Tests why the consensus argues for early EGFR testing in resectable disease, not only metastatic disease. Direct lookup: one passage.
- **Evidence:** reflex_early
- **Near-duplicate review:** Shares reflex_early with o030, which needs it only as part of its synthesis.

#### o010 (revision 1)

> In the lung-cancer RCT meta-analysis, how did single ICI and ICI plus chemotherapy compare with chemotherapy for cardiac adverse events?

- **Why this case:** Tests comparator-relative cardiac adverse-event RRs by regimen versus chemotherapy, not CVD mortality. Direct lookup: one passage.
- **Evidence:** rct_cv
- **Near-duplicate review:** Shares rct_cv with o011 and o018. Distinct: o011 is a false premise about the null heart-failure subgroup; o018 compares across documents.

#### o026 (revision 1)

> Among deaths in the older advanced-NSCLC PD-1 cohort, what shares were attributed to NSCLC and CVD, and which factors were associated with CVD mortality?

- **Why this case:** Tests cause-specific death shares (denominator: deaths, not patients) and factors associated with CVD mortality, including the insurance comparator. Replaces legacy q112's CVD-mortality coverage. Direct lookup: one passage.
- **Evidence:** mortality
- **Near-duplicate review:** Shares mortality with o012 and o017. Distinct: o012 asks the between-drug comparison; o017 uses it in a cross-document endpoint contrast.
- **Replaces coverage of:** legacy q112

#### o012 (revision 1)

> How did pembrolizumab versus nivolumab compare for cause-specific mortality in the older NSCLC cohort?

- **Why this case:** Tests that pembrolizumab-versus-nivolumab cause-specific mortality is a comparison between two PD-1 drugs, not with untreated controls; CVD sHR null, NSCLC sHR lower. Direct lookup: one passage.
- **Evidence:** mortality
- **Near-duplicate review:** Shares mortality with o026 and o017, which use different facts from the passage.

#### q085 (revision 2)

> How does the immune-exclusion definition review distinguish inflamed, desert and excluded tumors spatially?

- **Why this case:** Tests the spatial distinction among inflamed, desert and excluded tumours in the immune-exclusion review, and its note on inconsistent use of "cold". Revised onto an eligible source because the legacy source is deferred. Direct lookup: one passage.
- **Evidence:** exclusion
- **Near-duplicate review:** Shares no evidence anchor with another case; the question identifies the source without disclosing target values. o015 covers a different review's phenotypes; each question names its source.

#### o014 (revision 1)

> In the ICD mini-review, what distinct dendritic-cell mechanisms are attributed to CALR, ATP and HMGB1?

- **Why this case:** Tests distinct dendritic-cell mechanisms of CALR, ATP and HMGB1 as reviewed mechanisms, not clinical treatment effects. Direct lookup: one passage.
- **Evidence:** icd_damp
- **Near-duplicate review:** Shares icd_damp with o016, which links these mechanisms to separate cellular-stress pathways.

#### o015 (revision 1)

> How does the ICD mini-review distinguish excluded, desert and immunosuppressed cold tumors?

- **Why this case:** Tests the ICD review's cold-tumour phenotypes, including the immunosuppressed phenotype absent from q085's source. Direct lookup: one passage.
- **Evidence:** icd_phenotype
- **Near-duplicate review:** Shares no evidence anchor with another case; the question identifies the source without disclosing target values.

#### q078 (revision 2)

> According to the liquid-biopsy review, how much does combining ctDNA with ctRNA analysis change gene-fusion detection yield compared with ctDNA alone, and what RNA-testing recommendation does the review connect to this?

- **Why this case:** Restored legacy case. Tests attributing a cited-study range (about 28%–37% higher fusion yield with combined ctDNA/ctRNA) without converting it into a single pooled or absolute value, and linking it to the NCCN RNA-testing recommendation. Direct lookup: one passage.
- **Evidence:** fusion_yield
- **Near-duplicate review:** Shares no evidence anchor with another case; the question names the comparison without disclosing the range.

#### q097 (revision 2)

> In the US dual-screening study's multinomial regression, what adjusted odds ratios were reported for college graduation and for the highest income level when predicting dual screening versus neither screen?

- **Why this case:** Restored legacy case. Tests binding adjusted odds ratios to the correct outcome contrast (dual versus neither), because the same predictors have different aORs for cervical-only and CRC-only screening. Direct lookup: one Results passage.
- **Evidence:** screen_regression
- **Near-duplicate review:** Shares screen_regression with q098, which uses its race findings instead. Distinct from q095/q096, which ask descriptive category percentages, not adjusted odds.

#### q099 (revision 2)

> What decision levels does the US dual-screening study's Discussion propose to explain why cervical and colorectal screening diverge with age?

- **Why this case:** Restored legacy case. Tests reporting the Discussion's three proposed decision levels (physician, patient, health system) as hypotheses rather than findings. Direct lookup: one contiguous Discussion section spanning adjacent chunks.
- **Evidence:** screen_levels
- **Near-duplicate review:** Shares no evidence anchor with another case; the question asks for the levels without disclosing them.

### multi_hop (10)

#### o029 (revision 2)

> How did the Hunan study’s unadjusted two-year DFS comparison change after propensity matching, and how should its OS evidence be interpreted?

- **Why this case:** Tests response-versus-survival reasoning in one cohort: unadjusted DFS significance lost after PSM, the reported OS comparisons with their conflicting weighted/PSM labels, and the Limitations statement that OS is immature. Multi-hop: five separated anchors in one article.
- **Evidence:** hunan_response + hunan_matched + hunan_os_results + hunan_fig1_legend + hunan_os_limitation
- **Multi-hop link:** Join the unadjusted DFS result to the separate matched analysis, then the OS results with their conflicting Figure 1D label and the Limitations statement on OS maturity.
- **Near-duplicate review:** Shares Hunan anchors with o028 (hunan_response) and o030 (DFS/OS anchors). Distinct: o028 asks only MPR values; o030 is a cross-document synthesis that accepts either OS label; o029 alone requires the label conflict.
- **Replaces coverage of:** legacy q104

#### o002 (revision 2)

> Are the Zhongshan stage III cohort’s narrative and Table 2 MPR counts consistent for the chemoimmunotherapy arm?

- **Why this case:** Tests detecting and attributing an internal numeric conflict (narrative 19/26 versus Table 2 17/26) instead of reconciling it. Multi-hop: narrative and table are separated.
- **Evidence:** stage_narrative + stage_table
- **Multi-hop link:** Compare the narrative count with the separately positioned table row and its treatment columns.
- **Near-duplicate review:** Evidence is a subset of o001's. Retained because o002 isolates conflict detection, while o001 tests causal overreach; o001's question does not ask about the conflict.

#### o004 (revision 1)

> In the Helsinki TNBC cohort, distinguish myocarditis from any new troponin elevation and explain the surveillance used.

- **Why this case:** Tests distinguishing myocarditis (11, 14.7%) from new troponin elevation (23) and explaining the surveillance and diagnostic criteria. Multi-hop: methods and results anchors.
- **Evidence:** breast_cardio + breast_ae + breast_monitor
- **Multi-hop link:** Connect diagnostic monitoring in methods to the distinct outcomes reported in results.
- **Near-duplicate review:** Shares Helsinki cardiac anchors with o018 and breast_ae with o005. Distinct: o018 compares these with RCT risk ratios across documents; o005 reconciles discontinuation denominators.

#### o005 (revision 1)

> Why do postoperative pembrolizumab discontinuation percentages differ between the Helsinki abstract and results?

- **Why this case:** Tests reconciling apparently conflicting percentages (10.7% versus 23.5%) by binding the same count (eight patients) to different denominators. Multi-hop: abstract and results.
- **Evidence:** breast_ae + breast_stop
- **Multi-hop link:** Resolve apparently conflicting percentages by joining each count to its separate denominator.
- **Near-duplicate review:** Shares breast_ae with o004 and o018, which use it for cardiac adverse events, not discontinuation.

#### o027 (revision 1)

> Did the Vietnam afatinib study’s higher ORR at a 40-mg starting dose also translate to significantly longer mTTF?

- **Why this case:** Tests that higher ORR at 40 mg (p=0.034) did not translate into longer mTTF (p=0.755); ORR and time to treatment failure are separate endpoints. Replaces legacy q113's afatinib-dosing coverage. Multi-hop: abstract response and separate TTF analysis.
- **Evidence:** afatinib_orr + afatinib_ttf
- **Multi-hop link:** Compare response in the abstract with the separate time-to-failure analysis.
- **Near-duplicate review:** Shares afatinib_ttf with o006 and with o024 (decoy). Distinct: o006 tests the dose-share conflict; o024 uses the passage as a wrong-setting competitor.
- **Replaces coverage of:** legacy q113

#### o006 (revision 1)

> Are the Vietnam afatinib abstract and Table 2 consistent about the 30-mg and 40-mg starting-dose shares?

- **Why this case:** Tests keeping an abstract/Table 2 reversal of 30-mg and 40-mg starting-dose shares explicit. Multi-hop: abstract and table are separated.
- **Evidence:** afatinib_abstract + afatinib_ttf
- **Multi-hop link:** Bind each percentage to its dose in two separated source locations.
- **Near-duplicate review:** Shares afatinib_ttf with o027 and o024 (decoy), which use other values from the same table region.

#### o023 (revision 3)

> In the Gosney expert consensus, who initiates reflex NSCLC biomarker testing, what is agreed by the MDT, and is a formal oncologist request required? Explain the reported delay mechanism.

- **Why this case:** Tests the Gosney consensus reflex-testing workflow (pathologist initiates an MDT-agreed panel without a formal oncologist request) and its delay mechanism. POL-MOL is recorded as partial support, so attribution to the consensus is required. Multi-hop: definition and delay passages are separated (recategorised from direct lookup).
- **Evidence:** reflex_def + reflex_delay
- **Multi-hop link:** Join the definition of pathologist-initiated reflex testing to the separate Introduction passage on delays and suboptimal therapy.
- **Overlap:** PMC11547071 `polmol_reflex` (partial_support). Implies no oncologist request (agreed biomarkers are ordered automatically by the pathologist rather than the treating physician) but omits the MDT agreement and the delay/deterioration mechanism. Attribution to the Gosney consensus is required, so POL-MOL does not complete this task.
- **Near-duplicate review:** Absorbs withdrawn o019, a strict subset. Shares reflex_def and reflex_delay with o030, which needs them only for its synthesis.
- **Replaces coverage of:** legacy q111

#### o009 (revision 3)

> What CV-event estimates and study design did the observational NSCLC immunotherapy meta-analysis report?

- **Why this case:** Tests separating overall CV-event prevalence (3%, noncomparative) from the pooled HR, which only four of twelve observational studies contribute. Association is not causation or CVD mortality. Multi-hop: abstract and Limitations anchors (recategorised from direct lookup).
- **Evidence:** obs_cv + obs_hr_scope
- **Multi-hop link:** Join the abstract's prevalence and pooled HR to the Limitations statement that only four studies contribute to that HR.
- **Near-duplicate review:** Evidence is a subset of o017's. Retained because o017 tests cross-document endpoint separation, while o009 tests single-source scope of the HR.

#### o016 (revision 1)

> How do the ICD review’s ER stress and autophagy pathways connect to the dendritic-cell effects of CALR and ATP?

- **Why this case:** Tests linking ER stress/PERK and autophagy pathways to CALR exposure and ATP secretion and then to dendritic-cell effects. Multi-hop: requires four production chunks (see REVIEW.md).
- **Evidence:** icd_stress + icd_damp
- **Multi-hop link:** Link separate cellular-stress and extracellular-danger-signal sections.
- **Near-duplicate review:** Shares icd_damp with o014; o016 alone requires the cellular-stress anchor.

#### q098 (revision 2)

> In the US dual-screening study's adjusted analyses, how did the screening patterns of Black and Hispanic women differ, each compared with White women?

- **Why this case:** Restored legacy case, reframed to the paper's design: Black and Hispanic women are each compared with White women, not with each other. Tests keeping reference groups and outcome contrasts straight across two Results subsections. Multi-hop: the "versus neither" and "versus dual" results are separated.
- **Evidence:** screen_regression + screen_hispanic_single
- **Multi-hop link:** Join the regression results versus neither screen for both groups to the separate result versus dual screening, where only Hispanic women differ.
- **Near-duplicate review:** Shares screen_regression with q097, which uses its education and income findings. Only q098 needs the separate cervical-only-versus-dual result.

### cross_doc_synthesis (3)

#### o030 (revision 2)

> Combine the Hunan neoadjuvant study with the reflex-testing consensus: what does each contribute to interpreting perioperative NSCLC treatment and biomarker readiness?

- **Why this case:** Synthesis replacing legacy q117: treatment outcomes and limitations from the Hunan cohort combined with the consensus on biomarker readiness and early testing, without claiming the consensus explains the cohort's outcomes. Cross-document synthesis: both articles contribute required facts.
- **Evidence:** hunan_response + hunan_matched + hunan_os_results + hunan_os_limitation + reflex_def + reflex_delay + reflex_early
- **Overlap:** PMC11547071 `polmol_reflex` (partial_support). Implies no oncologist request (agreed biomarkers are ordered automatically by the pathologist rather than the treating physician) but omits the MDT agreement and the delay/deterioration mechanism. Attribution to the Gosney consensus is required, so POL-MOL does not complete this task. It also lacks the early-stage EGFR rationale.
- **Near-duplicate review:** Shares anchors with o028, o029, o023 and o008, each of which tests one component. Retained as the only case requiring the treatment/readiness synthesis.
- **Replaces coverage of:** legacy q117

#### o017 (revision 2)

> Why can the observational CV-event meta-analysis and older PD-1 cause-specific mortality cohort not be read as the same cardiovascular endpoint?

- **Why this case:** Synthesis: observational CV events (prevalence and four-study HR) and cause-specific mortality between two PD-1 drugs are different endpoints, populations and comparators, so they do not contradict each other. Cross-document synthesis.
- **Evidence:** obs_cv + obs_hr_scope + mortality
- **Near-duplicate review:** Contains o009's evidence plus the mortality passage; distinct because the failure mode is cross-document endpoint conflation.

#### o018 (revision 1)

> How should the Helsinki TNBC myocarditis frequency and lung-cancer RCT cardiac-adverse-event risks be compared?

- **Why this case:** Synthesis: TNBC absolute myocarditis frequency under intensive surveillance versus lung-cancer RCT comparator-relative cardiac adverse-event RRs. Cross-document synthesis.
- **Evidence:** breast_ae + breast_cardio + breast_monitor + rct_cv
- **Near-duplicate review:** Contains o004's cardiac evidence and o010's rct_cv; distinct because it tests cross-population, cross-endpoint comparison.

### cross_doc_distractor (2)

#### o024 (revision 1)

> In the driver-altered NSCLC review’s stage II–IIIA ADAURA results, what absolute five-year OS difference is reported between osimertinib and placebo, and what treatment setting does it describe?

- **Why this case:** Named distractor replacing legacy q118: absolute five-year OS difference for stage II–IIIA adjuvant osimertinib (12 points) must outrank an advanced first-line afatinib time-to-treatment-failure passage. Cross-document distractor.
- **Evidence:** driver_os + driver_dfs
- **Named decoy:** PMC10840225 `afatinib_ttf`. Both concern EGFR-directed NSCLC treatment and survival-like estimates. Advanced first-line afatinib mTTF by dose does not answer adjuvant osimertinib five-year OS.
- **Near-duplicate review:** Shares driver_os with o007 and driver_dfs with q108; o024 alone derives the absolute difference and faces a decoy.
- **Replaces coverage of:** legacy q118

#### o025 (revision 2)

> For NSCLC MRD assessment in the Batra liquid-biopsy review, how do tumor-informed and tumor-agnostic assays compare at landmark and longitudinal timepoints?

- **Why this case:** Named distractor replacing legacy q119: tumour-informed versus tumour-agnostic MRD assay performance must outrank a same-field ctDNA-MRD-guided adjuvant trial listing that reports no assay performance. Cross-document distractor.
- **Evidence:** mrd
- **Named decoy:** PMC11431721 `driver_mrd_trial`. Both concern postoperative ctDNA-MRD in resected NSCLC. Table 2 lists an ongoing adjuvant trial of ctDNA-MRD-guided osimertinib with a DFS endpoint; it reports no assay sensitivity or specificity and no tumor-informed versus tumor-agnostic comparison.
- **Near-duplicate review:** Sole MRD assay-performance case after q082 was withdrawn as its duplicate.
- **Replaces coverage of:** legacy q119

### false_premise (7)

#### q081 (revision 2)

> Does the liquid-biopsy review establish that blood-based MCED has the same demonstrated lung-cancer mortality benefit as LDCT?

- **Why this case:** False premise: that MCED shares LDCT's demonstrated mortality benefit. The correction needs the LDCT/NLST benefit and the statement that no MCED test has shown mortality benefit, without overstating that as proven ineffectiveness.
- **Evidence:** ldct + mced
- **Near-duplicate review:** Shares no evidence anchor with another case; the question identifies the source without disclosing target values.

#### o001 (revision 2)

> Did the Zhongshan stage III neoadjuvant cohort demonstrate statistically significant DFS improvement because its pathological responses were higher?

- **Why this case:** False premise: that higher pathological response caused significant DFS improvement in the Zhongshan stage III cohort. Correction: response gain with nonsignificant DFS (p=0.129), plus the explicit narrative/table MPR conflict.
- **Evidence:** stage_response + stage_narrative + stage_table
- **Near-duplicate review:** Shares stage_narrative and stage_table with o002. Distinct failure modes: o001 rejects a response-to-survival causal premise; o002 detects an internal numeric conflict without the DFS question.

#### q108 (revision 2)

> Are the ADAURA hazard ratios in the nonmetastatic driver review outcomes measured by the review’s own newly enrolled cohort?

- **Why this case:** False premise: that the review's ADAURA hazard ratios come from its own cohort. Correction attributes the DFS HRs to the cited trial. Migrated from a legacy unanswerable case on an ineligible source.
- **Evidence:** driver_dfs
- **Near-duplicate review:** Shares driver_dfs with o024. Distinct: q108 tests source attribution; o024 asks an absolute OS difference with a distractor.

#### o011 (revision 1)

> Does the RCT meta-analysis prove ICIs cannot cause heart failure because that subgroup result was nonsignificant?

- **Why this case:** False premise: that a nonsignificant heart-failure subgroup RR proves no risk. Correction: an imprecise null estimate does not establish absence of risk.
- **Evidence:** rct_cv
- **Near-duplicate review:** Shares rct_cv with o010 and o018; o011 alone uses the heart-failure subgroup.

#### o013 (revision 1)

> Does the immune-exclusion review establish a universal clinically validated numeric cutoff for every tumor?

- **Why this case:** False premise: that the review establishes a universal clinically validated numeric cutoff. Correction: lack of consensus, arbitrary cutoffs and heterogeneity, with the review's proposed reporting approach.
- **Evidence:** exclusion_limits + exclusion_solution
- **Near-duplicate review:** Shares no evidence anchor with another case; the question identifies the source without disclosing target values.

#### o021 (revision 3)

> What randomized five-year pembrolizumab-versus-chemotherapy OS treatment effect did the Helsinki TNBC study measure?

- **Why this case:** False premise: that the Helsinki study measured a randomized five-year OS effect. Correction: retrospective nonmatched design, and no OS at all (EFS by pCR; median follow-up 22 and 35 months).
- **Evidence:** breast_pcr + helsinki_followup
- **Near-duplicate review:** Shares breast_pcr with o003, which asks pCR values rather than design and follow-up.

#### q101 (revision 2)

> Are the HP2030 cervical and colorectal screening goals cited by Harper the study’s own achieved rates?

- **Why this case:** False premise: that the cited HP2030 targets are the study's achieved rates. Correction: targets (cervical 84.3%, CRC 74.4%) versus observed dual screening 58.2%.
- **Evidence:** screen_goals
- **Near-duplicate review:** Shares no evidence anchor with another case; the question identifies the source without disclosing target values.

### unanswerable (3)

#### o020 (revision 2)

> How many Hunan patients failed to undergo surgery after starting neoadjuvant therapy, and why?

- **Why this case:** Absent fact: the number and reasons of Hunan patients who started neoadjuvant therapy but did not undergo surgery. The paper excludes them and states their data are absent; no count may be inferred. Scope: whole selected oncology corpus.
- **Evidence:** none (absent fact)
- **Near-miss context:** `hunan_absence`. Explicit absence of data about those who failed to receive surgery. Other-study failure percentages and patients found unresectable after receiving surgery do not supply this missing excluded-patient denominator.
- **Near-duplicate review:** Uses hunan_absence only as negative context; no other case uses it.

#### q083 (revision 2)

> What FDA-validated early-stage sensitivity value for EarlyCDT-Lung is reported in the selected oncology corpus?

- **Why this case:** Absent fact on a retained source: an FDA-validated early-stage EarlyCDT-Lung sensitivity. The review describes an investigational panel with setting-dependent estimates; the question's "FDA-validated" wording itself presupposes a status the corpus does not report. Scope: whole selected oncology corpus.
- **Evidence:** none (absent fact)
- **Near-miss context:** `earlycdt`. No selected source reports an FDA-validated early-stage sensitivity for EarlyCDT-Lung. The review describes an investigational autoantibody panel and setting-dependent study estimates, which do not establish the requested regulatory validation.
- **Near-duplicate review:** Uses earlycdt only as negative context.

#### q100 (revision 2)

> What dual-screening rate for the Basque Country FIT programme is reported in the selected oncology corpus?

- **Why this case:** Absent fact on a retained source: a Basque FIT-programme dual-screening rate. The US BRFSS study reports a different population and endpoint. Scope: whole selected oncology corpus.
- **Evidence:** none (absent fact)
- **Near-miss context:** `screen`. No selected article reports the requested Basque-programme dual-screening rate. The US BRFSS study is a different population and endpoint; generic FIT discussion does not supply the requested rate.
- **Near-duplicate review:** Uses screen (q095/q096 evidence) only as near-miss negative context.

## Withdrawn before freeze

- **q082:** Same mrd anchor, facts and near-identical wording as o025; retained only one MRD assay-performance case. Coverage retained by o025.
- **o019:** Strict subset of o023 (same reflex_def anchor and Gosney MDT/pathologist/oncologist-request task); it also used POL-MOL as a decoy while other cases record it as partial support. Coverage retained by o023.

## Legacy case migration

| Legacy ID | Action | Linked cases | Reason | Link basis |
| --- | --- | --- | --- | --- |
| q078 | revise_in_v1 | q078 | Restored on 2026-10-02 at Juan's request after the original author confirmed no case-specific retirement reason; revised on the retained source with pinned evidence. | Revised in place. |
| q079 | revise_in_v1 | q079 | Revised on the retained review: detection rate versus cytology and diagnostic sensitivity/specificity are now required as separately attributed measures. | Revised in place. |
| q080 | revise_in_v1 | q080 | Revised on the retained review: adds the NILE population and noninferiority framing to turnaround and biomarker identification. | Revised in place. |
| q081 | revise_in_v1 | q081 | Revised on the retained review into a false-premise check of MCED versus LDCT mortality benefit; task change recorded in revision_ledger.json. | Revised in place. |
| q082 | retire_legacy_case | o025 | Withdrawn before freeze as a duplicate of o025 (same anchor and facts). | o025 carries the same MRD assay-performance task. |
| q083 | revise_in_v1 | q083 | Revised on the retained review as a scoped absent fact; the "FDA-validated" presupposition is recorded in the case rationale. | Revised in place. |
| q084 | retire_legacy_case | q079 | Retired as a near-duplicate: its CSF detection-rate fact is required by revised q079. | q079 requires the same detection-rate fact. |
| q085 | revise_in_v1 | q085 | Revised onto the eligible immune-exclusion review (PMC10073666) for the same desert/excluded distinction. Legacy source onco-tumor-microenvironment.pdf (PMC13430506) is deferred: its acknowledgements credit BioRender, so complete-PDF reuse rights are unresolved. | Revised in place. |
| q086 | retire_legacy_case | — | Retired: RELATIVITY-047 melanoma PFS appears only in the deferred source. Legacy source onco-tumor-microenvironment.pdf (PMC13430506) is deferred: its acknowledgements credit BioRender, so complete-PDF reuse rights are unresolved. No selected case tests the same evidence type, so no replacement is linked. | — |
| q087 | retire_legacy_case | — | Retired: KEYNOTE-942 melanoma RFS appears only in the deferred source. Legacy source onco-tumor-microenvironment.pdf (PMC13430506) is deferred: its acknowledgements credit BioRender, so complete-PDF reuse rights are unresolved. No selected case tests the same evidence type, so no replacement is linked. | — |
| q088 | retire_legacy_case | o014 | Retired: IDO1 trial-failure discussion appears only in the deferred source. Legacy source onco-tumor-microenvironment.pdf (PMC13430506) is deferred: its acknowledgements credit BioRender, so complete-PDF reuse rights are unresolved. | o014 tests the same reasoning task: reviewed mechanisms are not clinical treatment benefit. |
| q089 | retire_legacy_case | q085, o015 | Retired: the static-versus-dynamic biomarker framework appears only in the deferred source. Legacy source onco-tumor-microenvironment.pdf (PMC13430506) is deferred: its acknowledgements credit BioRender, so complete-PDF reuse rights are unresolved. | q085 and o015 cover cold/hot tumour phenotype definitions in eligible reviews. |
| q090 | retire_legacy_case | — | Retired: the chemo/radiotherapy maturity comparison appears only in the deferred source. Legacy source onco-tumor-microenvironment.pdf (PMC13430506) is deferred: its acknowledgements credit BioRender, so complete-PDF reuse rights are unresolved. No selected case tests the same evidence type, so no replacement is linked. | — |
| q091 | retire_legacy_case | — | Retired: Legacy source onco-tumor-microenvironment.pdf (PMC13430506) is deferred: its acknowledgements credit BioRender, so complete-PDF reuse rights are unresolved. The question is not recast onto another study, so no replacement case is linked. | — |
| q092 | retire_legacy_case | — | Retired: the syngeneic-model exception appears only in the deferred source. Legacy source onco-tumor-microenvironment.pdf (PMC13430506) is deferred: its acknowledgements credit BioRender, so complete-PDF reuse rights are unresolved. No selected case tests the same evidence type, so no replacement is linked. | — |
| q093 | retire_legacy_case | o025 | Retired: one of its two documents is the deferred source. Legacy source onco-tumor-microenvironment.pdf (PMC13430506) is deferred: its acknowledgements credit BioRender, so complete-PDF reuse rights are unresolved. | o025 keeps ctDNA in the liquid-biopsy review as a named-distractor task. |
| q094 | retire_legacy_case | o025 | Retired: one of its two documents is the deferred source. Legacy source onco-tumor-microenvironment.pdf (PMC13430506) is deferred: its acknowledgements credit BioRender, so complete-PDF reuse rights are unresolved. | o025 keeps ctDNA monitoring performance from the liquid-biopsy review. |
| q095 | revise_in_v1 | q095 | Revised on the retained study to the four mutually exclusive categories; task change recorded in revision_ledger.json. | Revised in place. |
| q096 | revise_in_v1 | q096 | Revised on the retained study: compare the mutually exclusive cervical-only and CRC-only categories. | Revised in place. |
| q097 | revise_in_v1 | q097 | Restored on 2026-10-02 at Juan's request after the original author confirmed no case-specific retirement reason; revised on the retained source with pinned evidence. | Revised in place. |
| q098 | revise_in_v1 | q098 | Restored on 2026-10-02 at Juan's request after the original author confirmed no case-specific retirement reason; revised on the retained source with pinned evidence. | Revised in place. |
| q099 | revise_in_v1 | q099 | Restored on 2026-10-02 at Juan's request after the original author confirmed no case-specific retirement reason; revised on the retained source with pinned evidence. | Revised in place. |
| q100 | revise_in_v1 | q100 | Revised on the retained study as a scoped absent fact. | Revised in place. |
| q101 | revise_in_v1 | q101 | Revised on the retained study into a false-premise correction of targets versus achieved rates. | Revised in place. |
| q102 | revise_in_v1 | q102 | Revised on the retained study: printed flow-diagram counts, with the diagram's inconsistencies kept explicit. | Revised in place. |
| q103 | retire_legacy_case | o022 | Retired; study-specific task moved to a new ID. Legacy source onco-breast-immunotherapy.pdf (PMC13438349) is a driver-positive NSCLC perioperative study under CC BY-NC 4.0, which fails the CC BY 4.0/CC0 policy. | o022 asks population and treatment-group sizes in an eligible perioperative NSCLC cohort. |
| q104 | retire_legacy_case | o029 | Retired; study-specific task moved to a new ID. Legacy source onco-breast-immunotherapy.pdf (PMC13438349) is a driver-positive NSCLC perioperative study under CC BY-NC 4.0, which fails the CC BY 4.0/CC0 policy. | o029 asks DFS and OS interpretation in an eligible perioperative NSCLC cohort. |
| q105 | retire_legacy_case | o028 | Retired; study-specific task moved to a new ID. Legacy source onco-breast-immunotherapy.pdf (PMC13438349) is a driver-positive NSCLC perioperative study under CC BY-NC 4.0, which fails the CC BY 4.0/CC0 policy. | o028 asks pathological response rates in an eligible perioperative NSCLC cohort. |
| q106 | retire_legacy_case | o001, o002 | Retired: the EGFR-mutant neoadjuvant-targeted subgroup appears only in the restricted source. Legacy source onco-breast-immunotherapy.pdf (PMC13438349) is a driver-positive NSCLC perioperative study under CC BY-NC 4.0, which fails the CC BY 4.0/CC0 policy. | o001 and o002 test pathological response versus DFS in another perioperative cohort. |
| q107 | retire_legacy_case | o029 | Retired: MPR-to-survival subgroup results appear only in the restricted source. Legacy source onco-breast-immunotherapy.pdf (PMC13438349) is a driver-positive NSCLC perioperative study under CC BY-NC 4.0, which fails the CC BY 4.0/CC0 policy. | o029 tests response versus survival interpretation in an eligible cohort. |
| q108 | revise_in_v1 | q108 | Revised onto the eligible driver review as an ADAURA attribution false premise. Legacy source onco-breast-immunotherapy.pdf (PMC13438349) is a driver-positive NSCLC perioperative study under CC BY-NC 4.0, which fails the CC BY 4.0/CC0 policy. | Revised in place. |
| q109 | retire_legacy_case | — | Retired: Legacy source onco-breast-immunotherapy.pdf (PMC13438349) is a driver-positive NSCLC perioperative study under CC BY-NC 4.0, which fails the CC BY 4.0/CC0 policy. The question is not recast onto another study, so no replacement case is linked. | — |
| q110 | retire_legacy_case | — | Retired: RADON EUROPE appears only in the restricted source. Legacy source onco-genomics-precision-medicine.pdf (PMC13434091) is CC BY-NC 4.0, which fails the CC BY 4.0/CC0 policy. No selected case tests the same evidence type, so no replacement is linked. | — |
| q111 | retire_legacy_case | o023 | Retired; study-specific task moved to a new ID. Legacy source onco-genomics-precision-medicine.pdf (PMC13434091) is CC BY-NC 4.0, which fails the CC BY 4.0/CC0 policy. | o023 tests real-world biomarker-testing workflow and delay in an eligible consensus. |
| q112 | retire_legacy_case | o026 | Retired; study-specific task moved to a new ID. Legacy source onco-genomics-precision-medicine.pdf (PMC13434091) is CC BY-NC 4.0, which fails the CC BY 4.0/CC0 policy. | o026 tests CVD-specific mortality in lung cancer in an eligible cohort. |
| q113 | retire_legacy_case | o027 | Retired; study-specific task moved to a new ID. Legacy source onco-genomics-precision-medicine.pdf (PMC13434091) is CC BY-NC 4.0, which fails the CC BY 4.0/CC0 policy. | o027 tests afatinib dose and outcomes in the eligible Vietnam cohort. |
| q114 | retire_legacy_case | — | Retired: the environmental-exposure synthesis appears only in the restricted source. Legacy source onco-genomics-precision-medicine.pdf (PMC13434091) is CC BY-NC 4.0, which fails the CC BY 4.0/CC0 policy. No selected case tests the same evidence type, so no replacement is linked. | — |
| q115 | retire_legacy_case | — | Retired: Legacy source onco-genomics-precision-medicine.pdf (PMC13434091) is CC BY-NC 4.0, which fails the CC BY 4.0/CC0 policy. The question is not recast onto another study, so no replacement case is linked. | — |
| q116 | retire_legacy_case | o011, o012 | Retired: the radon causation question appears only in the restricted source. Legacy source onco-genomics-precision-medicine.pdf (PMC13434091) is CC BY-NC 4.0, which fails the CC BY 4.0/CC0 policy. | o011 and o012 test the same reasoning task: association or a null estimate does not prove causation or absence of risk. |
| q117 | retire_legacy_case | o030 | Retired; study-specific task moved to a new ID. Legacy source onco-breast-immunotherapy.pdf (PMC13438349) is a driver-positive NSCLC perioperative study under CC BY-NC 4.0, which fails the CC BY 4.0/CC0 policy. Legacy source onco-genomics-precision-medicine.pdf (PMC13434091) is CC BY-NC 4.0, which fails the CC BY 4.0/CC0 policy. | o030 synthesises treatment outcomes with real-world testing readiness from eligible sources. |
| q118 | retire_legacy_case | o024 | Retired; study-specific task moved to a new ID. Legacy source onco-breast-immunotherapy.pdf (PMC13438349) is a driver-positive NSCLC perioperative study under CC BY-NC 4.0, which fails the CC BY 4.0/CC0 policy. Legacy source onco-genomics-precision-medicine.pdf (PMC13434091) is CC BY-NC 4.0, which fails the CC BY 4.0/CC0 policy. | o024 tests EGFR-directed treatment outcomes against a dosing-study distractor. |
| q119 | retire_legacy_case | o025 | Retired; study-specific task moved to a new ID. Legacy source onco-breast-immunotherapy.pdf (PMC13438349) is a driver-positive NSCLC perioperative study under CC BY-NC 4.0, which fails the CC BY 4.0/CC0 policy. | o025 tests longitudinal ctDNA monitoring performance against a distractor. |

## Retained IDs whose task changed

- **q081:** Legacy multi-hop modality comparison is now a false-premise check that MCED shares LDCT's demonstrated mortality benefit.
- **q095:** Legacy dual-screening percentage plus single-cancer comparison is now the four mutually exclusive screening categories.
- **q108:** Legacy question on an ineligible NSCLC paper is now the ADAURA attribution check in the eligible nonmetastatic driver review.
- **q098:** Legacy Hispanic-versus-Black framing is now each group compared with White women, matching the paper's regression reference.

## Revision history

1. From `8b1adbe`: Validated Claude review: complete OS and HR scope, reflex overlap, non-reused IDs, positive premise correction and legacy negative migration.
2. From `a226bba`: Claude re-review: Hunan OS label conflict and Limitations anchor, Helsinki five-year OS correction, duplicate withdrawal with one POL-MOL role, same-field MRD decoy, per-article search provenance.
3. From `fd4eadf`: Decision documentation: case-specific selection rationale and near-duplicate review, specific legacy reasons and replacement bases, lower-priority candidate coverage, and multi_hop categories for two cases needing separated passages.
4. From `fa0245a`: Restored legacy q078, q097, q098 and q099 on retained sources: no retirement reason existed and their evidence is pinned.
