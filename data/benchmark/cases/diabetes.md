# Diabetes evaluation cases

Generated from the current combined v2 inputs. Regenerate with
`python -m tools.evaluation.render_case_index`; do not edit this page by hand.

[All topics](README.md) · [Article catalogue](articles.md) ·
[Authoritative questions](../diabetes/queries.json) ·
[Dependency map](../case_dependencies.json)

Expected responses are model-reviewed references, not biomedical expert
certification or observed RAG responses. No new scoring is performed here.

## Find a question

| ID | Category | Question |
| --- | --- | --- |
| [q001](#q001) | direct_lookup | In He et al.’s GQD plus metformin meta-analysis, which glycemic outcomes were primary and secondary? |
| [q002](#q002) | direct_lookup | How many trials and participants were included in He et al.’s systematic review of GQD plus metformin? |
| [q003](#q003) | direct_lookup | In He et al.’s primary change-score analysis, what was the HbA1c estimate and did it demonstrate a reliable additional benefit of GQD? |
| [q004](#q004) | multi_hop | Why should the all-eight post-treatment HbA1c sensitivity result in He et al. not override its primary change-score result? |
| [q005](#q005) | direct_lookup | What certainty and downgrade reasons did He et al. assign to HbA1c, FPG and 2hPG evidence for GQD plus metformin? |
| [q006](#q006) | direct_lookup | Did reporting random-number tables make any included GQD trials low risk of bias in He et al.’s review? |
| [q007](#q007) | unanswerable | Which commercial metformin brand was given in each of the eight GQD trials, according to the selected main PDF of He et al.’s review? |
| [q015](#q015) | direct_lookup | What proportion of people with T2DM does Lebedeva et al.’s zinc/hypoxia review cite as developing DKD? |
| [q016](#q016) | direct_lookup | Which pathogenic mechanism does Lebedeva et al.’s zinc/T2DM/DKD review emphasize for DKD onset and progression? |
| [q017](#q017) | direct_lookup | In the pancreatic-islet transporter section of Lebedeva et al.’s review, what role and expression profile are attributed to ZnT8? |
| [q018](#q018) | direct_lookup | What zinc/HIF mechanisms and experimental fibrosis evidence are reported by Lebedeva et al., and are they a clinical dosing recommendation? |
| [q019](#q019) | direct_lookup | How do the renal ZnT7 and ZnT8 experimental pathways differ in Lebedeva et al.’s DKD review? |
| [q021](#q021) | direct_lookup | How does Lebedeva et al.’s review distinguish acute adaptive HIF-1α activation from chronic overactivation in DKD? |
| [q029](#q029) | direct_lookup | How many studies did Ghanem et al.’s sleep-loss narrative review synthesize, and was that count from a prospective PRISMA screening protocol? |
| [q030](#q030) | direct_lookup | What heart-disease and stroke risks does Ghanem et al.’s sleep-loss review attribute to Cappuccio’s short-sleep synthesis? |
| [q031](#q031) | direct_lookup | In the Leproult study described by Ghanem et al., how should unchanged overall fasting glucose/insulin and correlations with sleep extension be distinguished? |
| [q032](#q032) | multi_hop | Which appetite-hormone changes and separate glucose/insulin findings does Ghanem et al.’s sleep review link to sleep restriction? |
| [q034](#q034) | cross_doc_distractor | What CAD, MI and stroke risk ratios does Ghanem et al.’s sleep-loss review attribute to the Isomaa metabolic-syndrome cohort? |
| [q035](#q035) | direct_lookup | How does Ghanem et al.’s review distinguish the day-specific DST/MI associations from the weekly PCI-for-MI result? |
| [q036](#q036) | multi_hop | What vector index, embedding/chunk configuration and retrieval depth did Guo et al.’s CGM counseling system use? |
| [q037](#q037) | cross_doc_distractor | In Guo et al.’s source-masked CGM counseling evaluation, what was the overall CA-versus-clinician response-quality difference? |
| [q038](#q038) | direct_lookup | Which quality dimensions had the largest CA-versus-clinician differences in Guo et al.’s CGM counseling study? |
| [q039](#q039) | multi_hop | How do source-identification denominators and the limitations section qualify practical blinding in Guo et al.’s CGM counseling study? |
| [d001](#d001) | multi_hop | How did the two metabolic-syndrome definitions affect prevalence in Mbota et al.’s Buea T2DM cohort? |
| [d002](#d002) | cross_doc_distractor | What female PRS-by-SHBG interaction estimate and population are reported in Dabbs-Brown et al.’s T2DM study? |
| [d003](#d003) | multi_hop | Are the male genome-wide interaction counts consistent between the abstract and Results of Dabbs-Brown et al.’s gene/sex-hormone study? |
| [d004](#d004) | direct_lookup | What CYP2C9*2 carriage frequencies were reported for Pashtun sulfonylurea hypoglycaemia cases and controls by Jan et al.? |
| [d005](#d005) | direct_lookup | Which OR, CI and crude/adjusted P values does Jan et al.’s Table 4 print for CYP2C9*2, and can that line be treated as an internally coherent risk estimate? |
| [d006](#d006) | multi_hop | How did the SIZE-DM trial’s predefined rule and adjusted HbA1c result support generic semaglutide non-inferiority? |
| [d007](#d007) | cross_doc_distractor | How did the HbA1c comparison at three versus six months differ in Berthoumieux et al.’s digital DSMES+CGM randomized trial? |
| [d008](#d008) | direct_lookup | What happened to the exploratory sleep-duration mediation findings after adjustment in Wang et al.’s three-cohort cardiometabolic study? |
| [d009](#d009) | cross_doc_synthesis | How do the GQD meta-analysis and SIZE-DM primary trial differ in comparator and interpretation of their HbA1c findings? |
| [d010](#d010) | cross_doc_synthesis | Why are Guo’s CGM counseling quality advantage and Berthoumieux’s six-month glycemic results not interchangeable management evidence? |
| [d011](#d011) | cross_doc_synthesis | How do Jan’s sulfonylurea pharmacogenetic study and Dabbs-Brown’s sex-hormone interaction GWAS differ in phenotype and population? |
| [d012](#d012) | cross_doc_synthesis | How should Lebedeva’s zinc/HIF renal mechanisms and the Taiwan SGLT2-plus-ACEI/ARB cohort’s renal association be distinguished? |
| [d013](#d013) | cross_doc_synthesis | How do the sleep narrative review’s Isomaa risks and Mbota’s Buea estimates represent different metabolic-syndrome evidence? |
| [d014](#d014) | multi_hop | What did the Cameroon fourth-line spironolactone trial report for office BP reductions relative to control, and over what follow-up? |
| [d015](#d015) | multi_hop | What do partitioned T2DM/BP polygenic associations imply about treating diabetes-risk mechanisms as a uniformly positive BP-risk axis, and what environmental limitation do the authors identify for explaining T2D/high-BP comorbidity? |
| [d016](#d016) | multi_hop | In the cardiorenal network meta-analysis, what did HFpEF comparisons report for drug-class differences in cardiovascular mortality, all-cause mortality and HF hospitalization/event, and how were the between-class comparisons derived? |
| [d017](#d017) | direct_lookup | What oxidative-stress and platelet-marker changes were reported at follow-up in elderly diabetic HFpEF patients in the geriatric SGLT2 study? |
| [d018](#d018) | direct_lookup | What pathogenic HIF-1α roles does Qin et al.’s HIF/zinc DKD review summarize? |
| [d019](#d019) | false_premise | Since He et al.’s primary GQD change-score analysis included all reviewed trials, how robust was its significant HbA1c benefit? |
| [d020](#d020) | false_premise | Since the primary intention-to-treat analysis of Berthoumieux’s DSMES+CGM trial showed statistically significant HbA1c improvement at both follow-up visits, what was the later benefit? |
| [d021](#d021) | false_premise | Since Guo’s CGM counseling evaluation was a randomized clinical trial proving patient glycemic improvement, what supports that clinical benefit? |
| [d022](#d022) | unanswerable | What was five-year cardiovascular mortality in the randomized SIZE-DM cohort after generic versus innovator semaglutide? |
| [d023](#d023) | unanswerable | What was the twelve-month HbA1c difference in the original Berthoumieux digital DSMES+CGM randomized cohort? |
| [d024](#d024) | unanswerable | What exact zinc formulation, dose and duration did Lebedeva et al. recommend for adults with stage-3 DKD? |
| [d025](#d025) | direct_lookup | Which two damaging DKD processes can HIF-1α promote, according to the selected zinc/HIF reviews? |
| [d026](#d026) | direct_lookup | Why should Wang et al.’s three-cohort sleep-quality estimates not be treated as directly interchangeable effect sizes? |

## q001

**direct_lookup · revision 2 · answerable**

In He et al.’s GQD plus metformin meta-analysis, which glycemic outcomes were primary and secondary?

**Expected response**

HbA1c was primary; fasting plasma glucose and 2-hour postprandial glucose were secondary.

**Required claims**

- `f1`: HbA1c was primary; fasting plasma glucose and 2-hour postprandial glucose were secondary.

**Article roles declared by the question**

- Required: [PMC13423648](https://pmc.ncbi.nlm.nih.gov/articles/PMC13423648.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC13423648](https://pmc.ncbi.nlm.nih.gov/articles/PMC13423648.1/) | Abstract; outcomes; p. 1 | `gqd_outcomes` |

**Response distinctions to preserve**

- Do not substitute another study/cohort/endpoint/timepoint
- Do not imply source consistency or clinical superiority from reported observational/vignette findings

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## q002

**direct_lookup · revision 2 · answerable**

How many trials and participants were included in He et al.’s systematic review of GQD plus metformin?

**Expected response**

Eight trials enrolled 725 participants; this is the review total, not the primary-analysis denominator.

**Required claims**

- `f1`: Eight trials enrolled 725 participants; this is the review total, not the primary-analysis denominator.

**Article roles declared by the question**

- Required: [PMC13423648](https://pmc.ncbi.nlm.nih.gov/articles/PMC13423648.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC13423648](https://pmc.ncbi.nlm.nih.gov/articles/PMC13423648.1/) | Results; study characteristics; p. 4 | `gqd_count` |

**Response distinctions to preserve**

- Do not substitute another study/cohort/endpoint/timepoint
- Do not imply source consistency or clinical superiority from reported observational/vignette findings

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## q003

**direct_lookup · revision 2 · answerable**

In He et al.’s primary change-score analysis, what was the HbA1c estimate and did it demonstrate a reliable additional benefit of GQD?

**Expected response**

Two trials/196 participants: MD -1.92 percentage points, 95% CI -4.43 to 0.59, P=.13; no statistically significant or reliable additional HbA1c benefit.

**Required claims**

- `f1`: Two trials/196 participants: MD -1.92 percentage points, 95% CI -4.43 to 0.59, P=.13; no statistically significant or reliable additional HbA1c benefit.

**Article roles declared by the question**

- Required: [PMC13423648](https://pmc.ncbi.nlm.nih.gov/articles/PMC13423648.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC13423648](https://pmc.ncbi.nlm.nih.gov/articles/PMC13423648.1/) | Results; primary change-score analysis; p. 6 | `gqd_primary` |

**Response distinctions to preserve**

- Do not substitute another study/cohort/endpoint/timepoint
- Do not imply source consistency or clinical superiority from reported observational/vignette findings

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## q004

**multi_hop · revision 2 · answerable**

Why should the all-eight post-treatment HbA1c sensitivity result in He et al. not override its primary change-score result?

**Expected response**

The two-trial primary change-score MD was -1.92, CI -4.43 to .59, P=.13, with extreme heterogeneity. The all-eight post-treatment MD was -1.21, CI -1.99 to -.43, P=.002, but heterogeneity and trial bias meant it did not override the conservative primary result.

**Required claims**

- `f1`: The two-trial primary change-score MD was -1.92, CI -4.43 to .59, P=.13, with extreme heterogeneity.
- `f2`: The all-eight post-treatment MD was -1.21, CI -1.99 to -.43, P=.002, but heterogeneity and trial bias meant it did not override the conservative primary result.

**Article roles declared by the question**

- Required: [PMC13423648](https://pmc.ncbi.nlm.nih.gov/articles/PMC13423648.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC13423648](https://pmc.ncbi.nlm.nih.gov/articles/PMC13423648.1/) | Results; primary change-score analysis; p. 6 | `gqd_primary` |
| primary | f2 | [PMC13423648](https://pmc.ncbi.nlm.nih.gov/articles/PMC13423648.1/) | Results; all-eight post-treatment sensitivity; p. 7 | `gqd_sensitivity` |

**Response distinctions to preserve**

- Do not substitute another study/cohort/endpoint/timepoint
- Do not imply source consistency or clinical superiority from reported observational/vignette findings

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## q005

**direct_lookup · revision 4 · answerable**

What certainty and downgrade reasons did He et al. assign to HbA1c, FPG and 2hPG evidence for GQD plus metformin?

**Expected response**

All three outcomes were very-low certainty. HbA1c was downgraded for high bias, extreme inconsistency and imprecision; FPG/2hPG for only two trials, substantial heterogeneity and methodological limitations.

**Required claims**

- `f1`: All three outcomes were very-low certainty. HbA1c was downgraded for high bias, extreme inconsistency and imprecision; FPG/2hPG for only two trials, substantial heterogeneity and methodological limitations.

**Article roles declared by the question**

- Required: [PMC13423648](https://pmc.ncbi.nlm.nih.gov/articles/PMC13423648.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC13423648](https://pmc.ncbi.nlm.nih.gov/articles/PMC13423648.1/) | Results; certainty of evidence; p. 6 | `gqd_grade` |

**Response distinctions to preserve**

- Do not substitute another study/cohort/endpoint/timepoint
- Do not imply source consistency or clinical superiority from reported observational/vignette findings

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## q006

**direct_lookup · revision 2 · answerable**

Did reporting random-number tables make any included GQD trials low risk of bias in He et al.’s review?

**Expected response**

No. All trials were judged high risk of bias; S1-S3 reported random-number tables but allocation concealment was not described.

**Required claims**

- `f1`: No. All trials were judged high risk of bias; S1-S3 reported random-number tables but allocation concealment was not described.

**Article roles declared by the question**

- Required: [PMC13423648](https://pmc.ncbi.nlm.nih.gov/articles/PMC13423648.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC13423648](https://pmc.ncbi.nlm.nih.gov/articles/PMC13423648.1/) | Results; risk of bias; p. 5 | `gqd_bias` |

**Response distinctions to preserve**

- Do not substitute another study/cohort/endpoint/timepoint
- Do not imply source consistency or clinical superiority from reported observational/vignette findings

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## q007

**unanswerable · revision 2 · absent_fact**

Which commercial metformin brand was given in each of the eight GQD trials, according to the selected main PDF of He et al.’s review?

**Expected response**

Not reported for the named cohort/timepoint in the selected main PDFs. State the evidence limit rather than inventing the requested result.

**Article roles declared by the question**

- Required: None recorded.
- Alternatives: None recorded.
- Decoys: None recorded.

**Evidence:** No positive answer-evidence set is defined. See the
expected refusal and the recorded search scope below.

**Response distinctions to preserve**

- Do not substitute another study/cohort/endpoint/timepoint
- Do not imply source consistency or clinical superiority from reported observational/vignette findings

**Missing-fact search scope**

Reviewed named original cohort/report follow-up; no selected article supplies the requested cohort/timepoint outcome. Supplements not included.

[PMC10363301](https://pmc.ncbi.nlm.nih.gov/articles/PMC10363301.1/), [PMC10452755](https://pmc.ncbi.nlm.nih.gov/articles/PMC10452755.1/), [PMC10607686](https://pmc.ncbi.nlm.nih.gov/articles/PMC10607686.1/), [PMC10619268](https://pmc.ncbi.nlm.nih.gov/articles/PMC10619268.1/), [PMC10985250](https://pmc.ncbi.nlm.nih.gov/articles/PMC10985250.1/), [PMC11265054](https://pmc.ncbi.nlm.nih.gov/articles/PMC11265054.1/), [PMC11354916](https://pmc.ncbi.nlm.nih.gov/articles/PMC11354916.1/), [PMC11373557](https://pmc.ncbi.nlm.nih.gov/articles/PMC11373557.1/), [PMC11374717](https://pmc.ncbi.nlm.nih.gov/articles/PMC11374717.1/), [PMC11514186](https://pmc.ncbi.nlm.nih.gov/articles/PMC11514186.1/), [PMC11549774](https://pmc.ncbi.nlm.nih.gov/articles/PMC11549774.1/), [PMC11847805](https://pmc.ncbi.nlm.nih.gov/articles/PMC11847805.1/), [PMC11973566](https://pmc.ncbi.nlm.nih.gov/articles/PMC11973566.1/), [PMC12003177](https://pmc.ncbi.nlm.nih.gov/articles/PMC12003177.1/), [PMC12419643](https://pmc.ncbi.nlm.nih.gov/articles/PMC12419643.1/), [PMC12436478](https://pmc.ncbi.nlm.nih.gov/articles/PMC12436478.1/), [PMC12683810](https://pmc.ncbi.nlm.nih.gov/articles/PMC12683810.1/), [PMC12880197](https://pmc.ncbi.nlm.nih.gov/articles/PMC12880197.1/), [PMC12886974](https://pmc.ncbi.nlm.nih.gov/articles/PMC12886974.1/), [PMC13107781](https://pmc.ncbi.nlm.nih.gov/articles/PMC13107781.1/), [PMC13175446](https://pmc.ncbi.nlm.nih.gov/articles/PMC13175446.1/), [PMC13311226](https://pmc.ncbi.nlm.nih.gov/articles/PMC13311226.1/), [PMC13423648](https://pmc.ncbi.nlm.nih.gov/articles/PMC13423648.1/), [PMC13430954](https://pmc.ncbi.nlm.nih.gov/articles/PMC13430954.1/), [PMC13433181](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433181.1/), [PMC13433218](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433218.1/), [PMC13433680](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433680.1/), [PMC13433862](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433862.1/), [PMC13439631](https://pmc.ncbi.nlm.nih.gov/articles/PMC13439631.1/), [PMC13472562](https://pmc.ncbi.nlm.nih.gov/articles/PMC13472562.1/), [PMC4804513](https://pmc.ncbi.nlm.nih.gov/articles/PMC4804513.1/), [PMC8866621](https://pmc.ncbi.nlm.nih.gov/articles/PMC8866621.1/)

**Overlap review:** 55 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## q015

**direct_lookup · revision 2 · answerable**

What proportion of people with T2DM does Lebedeva et al.’s zinc/hypoxia review cite as developing DKD?

**Expected response**

Approximately 30-40%, a cited review estimate rather than a newly measured study incidence.

**Required claims**

- `f1`: Approximately 30-40%, a cited review estimate rather than a newly measured study incidence.

**Article roles declared by the question**

- Required: [PMC13433218](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433218.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC13433218](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433218.1/) | Introduction; cited DKD estimate and renal hypoxia; p. 2 | `zinc_intro` |

**Response distinctions to preserve**

- Do not substitute another study/cohort/endpoint/timepoint
- Do not imply source consistency or clinical superiority from reported observational/vignette findings

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## q016

**direct_lookup · revision 2 · answerable**

Which pathogenic mechanism does Lebedeva et al.’s zinc/T2DM/DKD review emphasize for DKD onset and progression?

**Expected response**

Renal hypoxia is emphasized as a fundamental pathogenic mechanism; this review framing does not prove a treatment effect.

**Required claims**

- `f1`: Renal hypoxia is emphasized as a fundamental pathogenic mechanism; this review framing does not prove a treatment effect.

**Article roles declared by the question**

- Required: [PMC13433218](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433218.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC13433218](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433218.1/) | Introduction; cited DKD estimate and renal hypoxia; p. 2 | `zinc_intro` |

**Response distinctions to preserve**

- Do not substitute another study/cohort/endpoint/timepoint
- Do not imply source consistency or clinical superiority from reported observational/vignette findings

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## q017

**direct_lookup · revision 2 · answerable**

In the pancreatic-islet transporter section of Lebedeva et al.’s review, what role and expression profile are attributed to ZnT8?

**Expected response**

ZnT8 in dense insulin-granule membranes mediates zinc accumulation/storage/preparation of insulin for secretion; this section describes expression as largely restricted to pancreatic islets. It does not establish zero renal expression.

**Required claims**

- `f1`: ZnT8 in dense insulin-granule membranes mediates zinc accumulation/storage/preparation of insulin for secretion; this section describes expression as largely restricted to pancreatic islets. It does not establish zero renal expression.

**Article roles declared by the question**

- Required: [PMC13433218](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433218.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC13433218](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433218.1/) | SLC30A/ZnT transporters; pancreatic-islet role; p. 4 | `zinc_granule` |

**Response distinctions to preserve**

- Do not substitute another study/cohort/endpoint/timepoint
- Do not imply source consistency or clinical superiority from reported observational/vignette findings

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## q018

**direct_lookup · revision 2 · answerable**

What zinc/HIF mechanisms and experimental fibrosis evidence are reported by Lebedeva et al., and are they a clinical dosing recommendation?

**Expected response**

Zinc promotes proteasomal HIF-1α degradation and inhibits nuclear translocation; animal DKD studies report reduced fibrotic markers/EMT via PI3K/AKT/GSK-3β with decreased HIF-1α. These are mechanistic/preclinical findings, not a clinical dosing recommendation.

**Required claims**

- `f1`: Zinc promotes proteasomal HIF-1α degradation and inhibits nuclear translocation; animal DKD studies report reduced fibrotic markers/EMT via PI3K/AKT/GSK-3β with decreased HIF-1α. These are mechanistic/preclinical findings, not a clinical dosing recommendation.

**Article roles declared by the question**

- Required: [PMC13433218](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433218.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC13433218](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433218.1/) | Renal hypoxia; zinc/HIF and animal fibrosis; p. 12 | `zinc_hif` |

**Response distinctions to preserve**

- Do not substitute another study/cohort/endpoint/timepoint
- Do not imply source consistency or clinical superiority from reported observational/vignette findings

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## q019

**direct_lookup · revision 2 · answerable**

How do the renal ZnT7 and ZnT8 experimental pathways differ in Lebedeva et al.’s DKD review?

**Expected response**

ZnT7 knockdown increases high-glucose EMT with MAPK/ERK and TGF-β/Smad activation in rat tubular cells. ZnT8 restrains TGF-β1/Smads and supports TNFAIP3-mediated NF-κB suppression; these are distinct experimental pathways.

**Required claims**

- `f1`: ZnT7 knockdown increases high-glucose EMT with MAPK/ERK and TGF-β/Smad activation in rat tubular cells. ZnT8 restrains TGF-β1/Smads and supports TNFAIP3-mediated NF-κB suppression; these are distinct experimental pathways.

**Article roles declared by the question**

- Required: [PMC13433218](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433218.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC13433218](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433218.1/) | DKD; renal ZnT7/ZnT8 experimental pathways; p. 11 | `zinc_transporters` |

**Response distinctions to preserve**

- Do not substitute another study/cohort/endpoint/timepoint
- Do not imply source consistency or clinical superiority from reported observational/vignette findings

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## q021

**direct_lookup · revision 2 · answerable**

How does Lebedeva et al.’s review distinguish acute adaptive HIF-1α activation from chronic overactivation in DKD?

**Expected response**

Acute activation is adaptive/reversible; chronic overactivation persistently drives pathological signalling, inflammation and fibrosis. HIF-1α is not uniformly harmful.

**Required claims**

- `f1`: Acute activation is adaptive/reversible; chronic overactivation persistently drives pathological signalling, inflammation and fibrosis. HIF-1α is not uniformly harmful.

**Article roles declared by the question**

- Required: [PMC13433218](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433218.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC13433218](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433218.1/) | DKD; acute adaptive versus chronic HIF overactivation; p. 10 | `zinc_acute_chronic` |

**Response distinctions to preserve**

- Do not substitute another study/cohort/endpoint/timepoint
- Do not imply source consistency or clinical superiority from reported observational/vignette findings

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## q029

**direct_lookup · revision 2 · answerable**

How many studies did Ghanem et al.’s sleep-loss narrative review synthesize, and was that count from a prospective PRISMA screening protocol?

**Expected response**

The review included 102 studies in qualitative synthesis; it is a narrative review, with no prospective PRISMA protocol or recorded intermediate screening flow.

**Required claims**

- `f1`: The review included 102 studies in qualitative synthesis; it is a narrative review, with no prospective PRISMA protocol or recorded intermediate screening flow.

**Article roles declared by the question**

- Required: [PMC13433680](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433680.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC13433680](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433680.1/) | Methods; narrative synthesis count; p. 2 | `sleep_method` |

**Response distinctions to preserve**

- Do not substitute another study/cohort/endpoint/timepoint
- Do not imply source consistency or clinical superiority from reported observational/vignette findings

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## q030

**direct_lookup · revision 2 · answerable**

What heart-disease and stroke risks does Ghanem et al.’s sleep-loss review attribute to Cappuccio’s short-sleep synthesis?

**Expected response**

The review reports 48% higher developing/dying heart-disease risk and 15% higher stroke risk, from over 474,000 participants in eight countries; this is pooled reviewed evidence, not a single MI trial.

**Required claims**

- `f1`: The review reports 48% higher developing/dying heart-disease risk and 15% higher stroke risk, from over 474,000 participants in eight countries; this is pooled reviewed evidence, not a single MI trial.

**Article roles declared by the question**

- Required: [PMC13433680](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433680.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC13433680](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433680.1/) | Results; review-attributed short-sleep heart/stroke evidence; p. 3 | `sleep_cappuccio` |

**Response distinctions to preserve**

- Do not substitute another study/cohort/endpoint/timepoint
- Do not imply source consistency or clinical superiority from reported observational/vignette findings

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## q031

**direct_lookup · revision 2 · answerable**

In the Leproult study described by Ghanem et al., how should unchanged overall fasting glucose/insulin and correlations with sleep extension be distinguished?

**Expected response**

Sixteen healthy non-obese adults showed no significant overall glucose/insulin change; reported correlations were glucose r=.53 (P=.041), insulin r=-.60 (P=.025), insulin sensitivity r=.76 (P=.002). Correlations are not mean treatment effects.

**Required claims**

- `f1`: Sixteen healthy non-obese adults showed no significant overall glucose/insulin change; reported correlations were glucose r=.53 (P=.041), insulin r=-.60 (P=.025), insulin sensitivity r=.76 (P=.002). Correlations are not mean treatment effects.

**Article roles declared by the question**

- Required: [PMC13433680](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433680.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC13433680](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433680.1/) | Results; Leproult sleep extension and correlations; p. 9 | `sleep_leproult` |

**Response distinctions to preserve**

- Do not substitute another study/cohort/endpoint/timepoint
- Do not imply source consistency or clinical superiority from reported observational/vignette findings

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## q032

**multi_hop · revision 2 · answerable**

Which appetite-hormone changes and separate glucose/insulin findings does Ghanem et al.’s sleep review link to sleep restriction?

**Expected response**

Sleep restriction is discussed with increased ghrelin and reduced leptin, promoting appetite. The cited restriction experiment reports a 40% decrease in glucose clearance and 30% lower insulin response; separate evidence does not prove one hormonal change caused all outcomes.

**Required claims**

- `f1`: Sleep restriction is discussed with increased ghrelin and reduced leptin, promoting appetite.
- `f2`: The cited restriction experiment reports a 40% decrease in glucose clearance and 30% lower insulin response; separate evidence does not prove one hormonal change caused all outcomes.

**Article roles declared by the question**

- Required: [PMC13433680](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433680.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC13433680](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433680.1/) | Sleep/metabolic syndrome; appetite hormones; p. 6 | `sleep_hormones` |
| primary | f2 | [PMC13433680](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433680.1/) | Sleep/metabolic syndrome; glucose and insulin experiment; p. 6 | `sleep_glucose` |

**Response distinctions to preserve**

- Do not substitute another study/cohort/endpoint/timepoint
- Do not imply source consistency or clinical superiority from reported observational/vignette findings

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## q034

**cross_doc_distractor · revision 2 · answerable**

What CAD, MI and stroke risk ratios does Ghanem et al.’s sleep-loss review attribute to the Isomaa metabolic-syndrome cohort?

**Expected response**

The review attributes CAD RR 2.96, MI RR 2.63 and stroke RR 2.27 to the cited 4,483-person Isomaa cohort; these are macrovascular risk ratios.

**Required claims**

- `f1`: The review attributes CAD RR 2.96, MI RR 2.63 and stroke RR 2.27 to the cited 4,483-person Isomaa cohort; these are macrovascular risk ratios.

**Article roles declared by the question**

- Required: [PMC13433680](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433680.1/)
- Alternatives: None recorded.
- Decoys: [PMC13311226](https://pmc.ncbi.nlm.nih.gov/articles/PMC13311226.1/)

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC13433680](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433680.1/) | Results; Isomaa review-attributed macrovascular risks; p. 9 | `sleep_macrovascular` |

**Why the distractors matter**

- [PMC13311226](https://pmc.ncbi.nlm.nih.gov/articles/PMC13311226.1/) — Metabolic syndrome, hypertension and cardiometabolic risk vocabulary
  Cameroon hospital T2DM syndrome prevalence under diagnostic criteria is not Isomaa macrovascular risk ratios.
  Passage: Results; criteria-specific prevalence; PDF p. 5; anchor `epi_prevalence`.

**Response distinctions to preserve**

- Do not substitute another study/cohort/endpoint/timepoint
- Do not imply source consistency or clinical superiority from reported observational/vignette findings

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## q035

**direct_lookup · revision 2 · answerable**

How does Ghanem et al.’s review distinguish the day-specific DST/MI associations from the weekly PCI-for-MI result?

**Expected response**

Spring day-specific MI RR 1.24 (CI 1.05-1.46, P=.011) and fall RR .79 (CI .62-.99, P=.044) are contrasted with no weekly PCI-for-MI change. These are reviewed observational associations.

**Required claims**

- `f1`: Spring day-specific MI RR 1.24 (CI 1.05-1.46, P=.011) and fall RR .79 (CI .62-.99, P=.044) are contrasted with no weekly PCI-for-MI change. These are reviewed observational associations.

**Article roles declared by the question**

- Required: [PMC13433680](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433680.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC13433680](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433680.1/) | Results; day-specific MI effects versus weekly PCI null; p. 5 | `sleep_dst` |

**Response distinctions to preserve**

- Do not substitute another study/cohort/endpoint/timepoint
- Do not imply source consistency or clinical superiority from reported observational/vignette findings

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## q036

**multi_hop · revision 4 · answerable**

What vector index, embedding/chunk configuration and retrieval depth did Guo et al.’s CGM counseling system use?

**Expected response**

FAISS with text-embedding-3-small, about 500-character segments and 100-character overlap, top_k=2 using Euclidean/L2 distance.

**Required claims**

- `f1`: FAISS with text-embedding-3-small, about 500-character segments and 100-character overlap, top_k=2 using Euclidean/L2 distance.

**Article roles declared by the question**

- Required: [PMC13430954](https://pmc.ncbi.nlm.nih.gov/articles/PMC13430954.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC13430954](https://pmc.ncbi.nlm.nih.gov/articles/PMC13430954.1/) | Methods; CA retrieval design; p. 5 | `ca_architecture` |
| primary | f1 | [PMC13430954](https://pmc.ncbi.nlm.nih.gov/articles/PMC13430954.1/) | Methods; named embedding model and top_k; p. 5, 6 | `ca_embedding` |

**Response distinctions to preserve**

- Do not substitute another study/cohort/endpoint/timepoint
- Do not imply source consistency or clinical superiority from reported observational/vignette findings

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## q037

**cross_doc_distractor · revision 2 · answerable**

In Guo et al.’s source-masked CGM counseling evaluation, what was the overall CA-versus-clinician response-quality difference?

**Expected response**

The estimated difference was .782 points, 95% CI .692-.872, P<.001, on the response-rating scale; it is not a patient HbA1c effect.

**Required claims**

- `f1`: The estimated difference was .782 points, 95% CI .692-.872, P<.001, on the response-rating scale; it is not a patient HbA1c effect.

**Article roles declared by the question**

- Required: [PMC13430954](https://pmc.ncbi.nlm.nih.gov/articles/PMC13430954.1/)
- Alternatives: None recorded.
- Decoys: [PMC13175446](https://pmc.ncbi.nlm.nih.gov/articles/PMC13175446.1/)

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC13430954](https://pmc.ncbi.nlm.nih.gov/articles/PMC13430954.1/) | Results; overall response-quality estimate; p. 10 | `ca_quality` |

**Why the distractors matter**

- [PMC13175446](https://pmc.ncbi.nlm.nih.gov/articles/PMC13175446.1/) — CGM intervention and quality/control improvement
  Berthoumieux’s randomized patient trial measures HbA1c, not vignette response quality.
  Passage: Abstract Results; ITT HbA1c timepoints; PDF p. 1; anchor `cgm_timepoints`.

**Response distinctions to preserve**

- Do not substitute another study/cohort/endpoint/timepoint
- Do not imply source consistency or clinical superiority from reported observational/vignette findings

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## q038

**direct_lookup · revision 2 · answerable**

Which quality dimensions had the largest CA-versus-clinician differences in Guo et al.’s CGM counseling study?

**Expected response**

Empathy and actionability had the largest differences (1.062 and .992 points, respectively); these are perceived written-response ratings.

**Required claims**

- `f1`: Empathy and actionability had the largest differences (1.062 and .992 points, respectively); these are perceived written-response ratings.

**Article roles declared by the question**

- Required: [PMC13430954](https://pmc.ncbi.nlm.nih.gov/articles/PMC13430954.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC13430954](https://pmc.ncbi.nlm.nih.gov/articles/PMC13430954.1/) | Results; quality dimensions; p. 11 | `ca_dimensions` |

**Response distinctions to preserve**

- Do not substitute another study/cohort/endpoint/timepoint
- Do not imply source consistency or clinical superiority from reported observational/vignette findings

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## q039

**multi_hop · revision 2 · answerable**

How do source-identification denominators and the limitations section qualify practical blinding in Guo et al.’s CGM counseling study?

**Expected response**

697/864 ratings correctly identified source (80.7%); after excluding 67 unsure judgments, 697/797 definitive judgments were correct (87.5%). The design was source-masked but responses were often recognizable, so practical blinding was imperfect; this does not quantify causal source-label bias.

**Required claims**

- `f1`: 697/864 ratings correctly identified source (80.7%); after excluding 67 unsure judgments, 697/797 definitive judgments were correct (87.5%).
- `f2`: The design was source-masked but responses were often recognizable, so practical blinding was imperfect; this does not quantify causal source-label bias.

**Article roles declared by the question**

- Required: [PMC13430954](https://pmc.ncbi.nlm.nih.gov/articles/PMC13430954.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC13430954](https://pmc.ncbi.nlm.nih.gov/articles/PMC13430954.1/) | Results; source identification denominators; p. 13 | `ca_identification` |
| primary | f2 | [PMC13430954](https://pmc.ncbi.nlm.nih.gov/articles/PMC13430954.1/) | Discussion; imperfect practical blinding; p. 15 | `ca_limitations` |

**Response distinctions to preserve**

- Do not substitute another study/cohort/endpoint/timepoint
- Do not imply source consistency or clinical superiority from reported observational/vignette findings

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## d001

**multi_hop · revision 1 · answerable**

How did the two metabolic-syndrome definitions affect prevalence in Mbota et al.’s Buea T2DM cohort?

**Expected response**

IDF requires central obesity plus two risk factors. Reported IDF prevalence was 64.0%, versus NCEP-ATP III 56.8%; these describe this hospital-based cohort, not global T2DM prevalence.

**Required claims**

- `f1`: IDF requires central obesity plus two risk factors.
- `f2`: Reported IDF prevalence was 64.0%, versus NCEP-ATP III 56.8%; these describe this hospital-based cohort, not global T2DM prevalence.

**Article roles declared by the question**

- Required: [PMC13311226](https://pmc.ncbi.nlm.nih.gov/articles/PMC13311226.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC13311226](https://pmc.ncbi.nlm.nih.gov/articles/PMC13311226.1/) | Methods; IDF operational definition; p. 4 | `epi_definitions` |
| primary | f2 | [PMC13311226](https://pmc.ncbi.nlm.nih.gov/articles/PMC13311226.1/) | Results; criteria-specific prevalence; p. 5 | `epi_prevalence` |

**Response distinctions to preserve**

- Do not substitute another study/cohort/endpoint/timepoint
- Do not imply source consistency or clinical superiority from reported observational/vignette findings

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## d002

**cross_doc_distractor · revision 1 · answerable**

What female PRS-by-SHBG interaction estimate and population are reported in Dabbs-Brown et al.’s T2DM study?

**Expected response**

White European UK Biobank participants; female interaction OR .88, CI .85-.90, significant. This is disease-risk interaction, not sulfonylurea response.

**Required claims**

- `f1`: White European UK Biobank participants; female interaction OR .88, CI .85-.90, significant. This is disease-risk interaction, not sulfonylurea response.

**Article roles declared by the question**

- Required: [PMC12419643](https://pmc.ncbi.nlm.nih.gov/articles/PMC12419643.1/)
- Alternatives: None recorded.
- Decoys: [PMC10452755](https://pmc.ncbi.nlm.nih.gov/articles/PMC10452755.1/)

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC12419643](https://pmc.ncbi.nlm.nih.gov/articles/PMC12419643.1/) | Abstract Methods; population and adjustment; p. 1 | `gene_population` |
| primary | f1 | [PMC12419643](https://pmc.ncbi.nlm.nih.gov/articles/PMC12419643.1/) | Results; female PRS/SHBG interaction; p. 5 | `gene_shbg` |

**Why the distractors matter**

- [PMC10452755](https://pmc.ncbi.nlm.nih.gov/articles/PMC10452755.1/) — Genetic allele effects in T2DM
  Pashtun sulfonylurea-associated hypoglycaemia phenotype differs from hormone-interaction disease risk.
  Passage: Results; allele-frequency comparison; PDF p. 6; anchor `drug_frequency`.

**Response distinctions to preserve**

- Do not substitute another study/cohort/endpoint/timepoint
- Do not imply source consistency or clinical superiority from reported observational/vignette findings

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## d003

**multi_hop · revision 1 · answerable**

Are the male genome-wide interaction counts consistent between the abstract and Results of Dabbs-Brown et al.’s gene/sex-hormone study?

**Expected response**

The abstract reports three male and fourteen female SNP-by-hormone interactions. The Results paragraph reports two male and fourteen female relevant interaction loci. Preserve the discrepancy without inventing a resolution.

**Required claims**

- `f1`: The abstract reports three male and fourteen female SNP-by-hormone interactions.
- `f2`: The Results paragraph reports two male and fourteen female relevant interaction loci. Preserve the discrepancy without inventing a resolution.

**Article roles declared by the question**

- Required: [PMC12419643](https://pmc.ncbi.nlm.nih.gov/articles/PMC12419643.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC12419643](https://pmc.ncbi.nlm.nih.gov/articles/PMC12419643.1/) | Abstract; reported male/female interaction counts; p. 1 | `gene_abstract_count` |
| primary | f2 | [PMC12419643](https://pmc.ncbi.nlm.nih.gov/articles/PMC12419643.1/) | Results; two male interaction loci; p. 5 | `gene_result_count` |

**Response distinctions to preserve**

- Do not substitute another study/cohort/endpoint/timepoint
- Do not imply source consistency or clinical superiority from reported observational/vignette findings

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## d004

**direct_lookup · revision 1 · answerable**

What CYP2C9*2 carriage frequencies were reported for Pashtun sulfonylurea hypoglycaemia cases and controls by Jan et al.?

**Expected response**

The Results report 17.5% in cases and 6.0% in controls; do not silently replace the article’s reported frequency denominator or infer a causal dose rule.

**Required claims**

- `f1`: The Results report 17.5% in cases and 6.0% in controls; do not silently replace the article’s reported frequency denominator or infer a causal dose rule.

**Article roles declared by the question**

- Required: [PMC10452755](https://pmc.ncbi.nlm.nih.gov/articles/PMC10452755.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC10452755](https://pmc.ncbi.nlm.nih.gov/articles/PMC10452755.1/) | Results; allele-frequency comparison; p. 6 | `drug_frequency` |

**Response distinctions to preserve**

- Do not substitute another study/cohort/endpoint/timepoint
- Do not imply source consistency or clinical superiority from reported observational/vignette findings

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## d005

**direct_lookup · revision 1 · answerable**

Which OR, CI and crude/adjusted P values does Jan et al.’s Table 4 print for CYP2C9*2, and can that line be treated as an internally coherent risk estimate?

**Expected response**

Table 4 prints OR .102, CI .08-3.08, crude P=.021 and adjusted P=.031. The interval crosses one and the reported direction/P values are anomalous; report the inconsistency rather than repair the estimate.

**Required claims**

- `f1`: Table 4 prints OR .102, CI .08-3.08, crude P=.021 and adjusted P=.031. The interval crosses one and the reported direction/P values are anomalous; report the inconsistency rather than repair the estimate.

**Article roles declared by the question**

- Required: [PMC10452755](https://pmc.ncbi.nlm.nih.gov/articles/PMC10452755.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC10452755](https://pmc.ncbi.nlm.nih.gov/articles/PMC10452755.1/) | Table 4; reported anomalous OR/CI/p-value; p. 6 | `drug_table_conflict` |

**Response distinctions to preserve**

- Do not substitute another study/cohort/endpoint/timepoint
- Do not imply source consistency or clinical superiority from reported observational/vignette findings

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## d006

**multi_hop · revision 1 · answerable**

How did the SIZE-DM trial’s predefined rule and adjusted HbA1c result support generic semaglutide non-inferiority?

**Expected response**

The upper 95% CI bound for generic-reference HbA1c difference had to be below .4 percentage points. LSM changes -2.22% versus -2.17%; difference -.05 percentage points, CI -.19 to .09. Upper bound .09 is below .4; this establishes non-inferiority, not superiority.

**Required claims**

- `f1`: The upper 95% CI bound for generic-reference HbA1c difference had to be below .4 percentage points.
- `f2`: LSM changes -2.22% versus -2.17%; difference -.05 percentage points, CI -.19 to .09. Upper bound .09 is below .4; this establishes non-inferiority, not superiority.

**Article roles declared by the question**

- Required: [PMC13107781](https://pmc.ncbi.nlm.nih.gov/articles/PMC13107781.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC13107781](https://pmc.ncbi.nlm.nih.gov/articles/PMC13107781.1/) | Methods; predefined non-inferiority rule; p. 3 | `trial_margin` |
| primary | f2 | [PMC13107781](https://pmc.ncbi.nlm.nih.gov/articles/PMC13107781.1/) | Results; adjusted generic/reference HbA1c difference; p. 3 | `trial_effect` |

**Response distinctions to preserve**

- Do not substitute another study/cohort/endpoint/timepoint
- Do not imply source consistency or clinical superiority from reported observational/vignette findings

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## d007

**cross_doc_distractor · revision 1 · answerable**

How did the HbA1c comparison at three versus six months differ in Berthoumieux et al.’s digital DSMES+CGM randomized trial?

**Expected response**

ITT difference -.7 percentage points at three months (CI -1.4 to -.1, P=.03) versus -.6 at six months (CI -1.4 to .2, P=.12); only three months reached statistical significance.

**Required claims**

- `f1`: ITT difference -.7 percentage points at three months (CI -1.4 to -.1, P=.03) versus -.6 at six months (CI -1.4 to .2, P=.12); only three months reached statistical significance.

**Article roles declared by the question**

- Required: [PMC13175446](https://pmc.ncbi.nlm.nih.gov/articles/PMC13175446.1/)
- Alternatives: None recorded.
- Decoys: [PMC13430954](https://pmc.ncbi.nlm.nih.gov/articles/PMC13430954.1/)

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC13175446](https://pmc.ncbi.nlm.nih.gov/articles/PMC13175446.1/) | Abstract Results; ITT HbA1c timepoints; p. 1 | `cgm_timepoints` |

**Why the distractors matter**

- [PMC13430954](https://pmc.ncbi.nlm.nih.gov/articles/PMC13430954.1/) — Digital CGM improvement and quality comparisons
  Guo’s vignette response ratings do not measure trial participants’ HbA1c at follow-up.
  Passage: Results; overall response-quality estimate; PDF p. 10; anchor `ca_quality`.

**Response distinctions to preserve**

- Do not substitute another study/cohort/endpoint/timepoint
- Do not imply source consistency or clinical superiority from reported observational/vignette findings

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## d008

**direct_lookup · revision 1 · answerable**

What happened to the exploratory sleep-duration mediation findings after adjustment in Wang et al.’s three-cohort cardiometabolic study?

**Expected response**

Small indirect effects were seen in unadjusted models; none remained evident after covariate adjustment. This is not proof of no biological mediation.

**Required claims**

- `f1`: Small indirect effects were seen in unadjusted models; none remained evident after covariate adjustment. This is not proof of no biological mediation.

**Article roles declared by the question**

- Required: [PMC13472562](https://pmc.ncbi.nlm.nih.gov/articles/PMC13472562.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC13472562](https://pmc.ncbi.nlm.nih.gov/articles/PMC13472562.1/) | Abstract Results; adjusted versus unadjusted mediation; p. 1 | `sleep_mediation` |

**Response distinctions to preserve**

- Do not substitute another study/cohort/endpoint/timepoint
- Do not imply source consistency or clinical superiority from reported observational/vignette findings

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## d009

**cross_doc_synthesis · revision 1 · answerable**

How do the GQD meta-analysis and SIZE-DM primary trial differ in comparator and interpretation of their HbA1c findings?

**Expected response**

GQD plus metformin versus metformin alone: two-trial change-score MD -1.92, CI -4.43 to .59, P=.13, not reliable additional HbA1c benefit. SIZE-DM is a 24-week generic-versus-innovator semaglutide active-control trial; adjusted difference -.05, CI -.19 to .09 supports non-inferiority, not a GQD effect.

**Required claims**

- `f1`: GQD plus metformin versus metformin alone: two-trial change-score MD -1.92, CI -4.43 to .59, P=.13, not reliable additional HbA1c benefit.
- `f2`: SIZE-DM is a 24-week generic-versus-innovator semaglutide active-control trial; adjusted difference -.05, CI -.19 to .09 supports non-inferiority, not a GQD effect.

**Article roles declared by the question**

- Required: [PMC13107781](https://pmc.ncbi.nlm.nih.gov/articles/PMC13107781.1/), [PMC13423648](https://pmc.ncbi.nlm.nih.gov/articles/PMC13423648.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC13423648](https://pmc.ncbi.nlm.nih.gov/articles/PMC13423648.1/) | Results; primary change-score analysis; p. 6 | `gqd_primary` |
| primary | f2 | [PMC13107781](https://pmc.ncbi.nlm.nih.gov/articles/PMC13107781.1/) | Abstract Methods; active-control primary trial; p. 1 | `trial_design` |
| primary | f2 | [PMC13107781](https://pmc.ncbi.nlm.nih.gov/articles/PMC13107781.1/) | Results; adjusted generic/reference HbA1c difference; p. 3 | `trial_effect` |

**Response distinctions to preserve**

- Do not substitute another study/cohort/endpoint/timepoint
- Do not imply source consistency or clinical superiority from reported observational/vignette findings

**Overlap review:** 53 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## d010

**cross_doc_synthesis · revision 1 · answerable**

Why are Guo’s CGM counseling quality advantage and Berthoumieux’s six-month glycemic results not interchangeable management evidence?

**Expected response**

Guo compares simulated written vignette responses, with .782-point quality advantage rather than patient glycemic follow-up. Berthoumieux randomizes patient DSMES+CGM versus usual care; six-month HbA1c P=.12 but time-in-range difference 14.6 percentage points (CI 1.0-28.2, P=.04).

**Required claims**

- `f1`: Guo compares simulated written vignette responses, with .782-point quality advantage rather than patient glycemic follow-up.
- `f2`: Berthoumieux randomizes patient DSMES+CGM versus usual care; six-month HbA1c P=.12 but time-in-range difference 14.6 percentage points (CI 1.0-28.2, P=.04).

**Article roles declared by the question**

- Required: [PMC13175446](https://pmc.ncbi.nlm.nih.gov/articles/PMC13175446.1/), [PMC13430954](https://pmc.ncbi.nlm.nih.gov/articles/PMC13430954.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC13430954](https://pmc.ncbi.nlm.nih.gov/articles/PMC13430954.1/) | Results; overall response-quality estimate; p. 10 | `ca_quality` |
| primary | f1 | [PMC13430954](https://pmc.ncbi.nlm.nih.gov/articles/PMC13430954.1/) | Methods; reporting framework and nonclinical evaluation; p. 9 | `ca_vignette` |
| primary | f2 | [PMC13175446](https://pmc.ncbi.nlm.nih.gov/articles/PMC13175446.1/) | Abstract Results; ITT HbA1c timepoints; p. 1 | `cgm_timepoints` |
| primary | f2 | [PMC13175446](https://pmc.ncbi.nlm.nih.gov/articles/PMC13175446.1/) | Abstract Results; CGM glycemic secondary endpoints; p. 1 | `cgm_tir` |

**Response distinctions to preserve**

- Do not substitute another study/cohort/endpoint/timepoint
- Do not imply source consistency or clinical superiority from reported observational/vignette findings

**Overlap review:** 53 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## d011

**cross_doc_synthesis · revision 1 · answerable**

How do Jan’s sulfonylurea pharmacogenetic study and Dabbs-Brown’s sex-hormone interaction GWAS differ in phenotype and population?

**Expected response**

Jan studies 200 hypoglycaemia cases and 200 controls of Pashtun ethnicity receiving sulfonylureas. Dabbs-Brown studies white European UK Biobank T2DM risk with sex-hormone/genetic interactions, excluding type 1 diabetes; not drug response.

**Required claims**

- `f1`: Jan studies 200 hypoglycaemia cases and 200 controls of Pashtun ethnicity receiving sulfonylureas.
- `f2`: Dabbs-Brown studies white European UK Biobank T2DM risk with sex-hormone/genetic interactions, excluding type 1 diabetes; not drug response.

**Article roles declared by the question**

- Required: [PMC10452755](https://pmc.ncbi.nlm.nih.gov/articles/PMC10452755.1/), [PMC12419643](https://pmc.ncbi.nlm.nih.gov/articles/PMC12419643.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC10452755](https://pmc.ncbi.nlm.nih.gov/articles/PMC10452755.1/) | Abstract; Pashtun case-control drug adverse-response phenotype; p. 1 | `drug_design` |
| primary | f2 | [PMC12419643](https://pmc.ncbi.nlm.nih.gov/articles/PMC12419643.1/) | Abstract Methods; population and adjustment; p. 1 | `gene_population` |

**Response distinctions to preserve**

- Do not substitute another study/cohort/endpoint/timepoint
- Do not imply source consistency or clinical superiority from reported observational/vignette findings

**Overlap review:** 53 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## d012

**cross_doc_synthesis · revision 1 · answerable**

How should Lebedeva’s zinc/HIF renal mechanisms and the Taiwan SGLT2-plus-ACEI/ARB cohort’s renal association be distinguished?

**Expected response**

Lebedeva describes mechanistic zinc/HIF regulation and animal fibrosis findings, not a human SGLT2 randomized efficacy estimate. The Taiwan CKD cohort reports lower ESRD/dialysis risk among SGLT2 users, but retrospective matching cannot exclude residual confounding; clinical association does not prove the zinc/HIF mechanism.

**Required claims**

- `f1`: Lebedeva describes mechanistic zinc/HIF regulation and animal fibrosis findings, not a human SGLT2 randomized efficacy estimate.
- `f2`: The Taiwan CKD cohort reports lower ESRD/dialysis risk among SGLT2 users, but retrospective matching cannot exclude residual confounding; clinical association does not prove the zinc/HIF mechanism.

**Article roles declared by the question**

- Required: [PMC11373557](https://pmc.ncbi.nlm.nih.gov/articles/PMC11373557.1/), [PMC13433218](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433218.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC13433218](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433218.1/) | Renal hypoxia; zinc/HIF and animal fibrosis; p. 12 | `zinc_hif` |
| primary | f2 | [PMC11373557](https://pmc.ncbi.nlm.nih.gov/articles/PMC11373557.1/) | Results; ESRD/dialysis incidence and adjusted HR; p. 1 | `shared_ckd_renal` |
| primary | f2 | [PMC11373557](https://pmc.ncbi.nlm.nih.gov/articles/PMC11373557.1/) | Discussion; residual confounding; p. 8 | `shared_ckd_confounding` |

**Response distinctions to preserve**

- Do not substitute another study/cohort/endpoint/timepoint
- Do not imply source consistency or clinical superiority from reported observational/vignette findings

**Overlap review:** 53 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## d013

**cross_doc_synthesis · revision 1 · answerable**

How do the sleep narrative review’s Isomaa risks and Mbota’s Buea estimates represent different metabolic-syndrome evidence?

**Expected response**

Ghanem attributes macrovascular CAD/MI/stroke RRs 2.96/2.63/2.27 to Isomaa’s cohort. Mbota reports hospital T2DM syndrome prevalence 64.0% IDF versus 56.8% NCEP-ATP III; diagnostic prevalence is not a macrovascular risk ratio.

**Required claims**

- `f1`: Ghanem attributes macrovascular CAD/MI/stroke RRs 2.96/2.63/2.27 to Isomaa’s cohort.
- `f2`: Mbota reports hospital T2DM syndrome prevalence 64.0% IDF versus 56.8% NCEP-ATP III; diagnostic prevalence is not a macrovascular risk ratio.

**Article roles declared by the question**

- Required: [PMC13311226](https://pmc.ncbi.nlm.nih.gov/articles/PMC13311226.1/), [PMC13433680](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433680.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC13433680](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433680.1/) | Results; Isomaa review-attributed macrovascular risks; p. 9 | `sleep_macrovascular` |
| primary | f2 | [PMC13311226](https://pmc.ncbi.nlm.nih.gov/articles/PMC13311226.1/) | Results; criteria-specific prevalence; p. 5 | `epi_prevalence` |

**Response distinctions to preserve**

- Do not substitute another study/cohort/endpoint/timepoint
- Do not imply source consistency or clinical superiority from reported observational/vignette findings

**Overlap review:** 53 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## d014

**multi_hop · revision 3 · answerable**

What did the Cameroon fourth-line spironolactone trial report for office BP reductions relative to control, and over what follow-up?

**Expected response**

Daily spironolactone 25 mg over four weeks; office systolic/diastolic reductions were 33 versus 14 and 14 versus 5 mmHg. This is BP response in T2DM resistant hypertension, not glycemic drug response.

**Required claims**

- `f1`: Daily spironolactone 25 mg over four weeks; office systolic/diastolic reductions were 33 versus 14 and 14 versus 5 mmHg. This is BP response in T2DM resistant hypertension, not glycemic drug response.

**Article roles declared by the question**

- Required: [PMC4804513](https://pmc.ncbi.nlm.nih.gov/articles/PMC4804513.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC4804513](https://pmc.ncbi.nlm.nih.gov/articles/PMC4804513.1/) | Methods; trial dose and four-week follow-up; p. 2, 3 | `shared_spirono_design` |
| primary | f1 | [PMC4804513](https://pmc.ncbi.nlm.nih.gov/articles/PMC4804513.1/) | Results; four-week office BP reductions; p. 4 | `shared_spirono_results` |

**Response distinctions to preserve**

- Do not substitute another study/cohort/endpoint/timepoint
- Do not imply source consistency or clinical superiority from reported observational/vignette findings

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## d015

**multi_hop · revision 4 · answerable**

What do partitioned T2DM/BP polygenic associations imply about treating diabetes-risk mechanisms as a uniformly positive BP-risk axis, and what environmental limitation do the authors identify for explaining T2D/high-BP comorbidity?

**Expected response**

The inverse cluster associates higher T2D risk with lower BP, contradicting a uniformly positive risk axis. The authors state that genetics alone does not fully explain T2D/high-BP comorbidity and identify environmental influences such as salt consumption or western diet.

**Required claims**

- `f1`: The inverse cluster associates higher T2D risk with lower BP, contradicting a uniformly positive risk axis.
- `f2`: The authors state that genetics alone does not fully explain T2D/high-BP comorbidity and identify environmental influences such as salt consumption or western diet.

**Article roles declared by the question**

- Required: [PMC12886974](https://pmc.ncbi.nlm.nih.gov/articles/PMC12886974.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC12886974](https://pmc.ncbi.nlm.nih.gov/articles/PMC12886974.1/) | Results; inverse T2D-BP cluster; p. 3 | `shared_pgs_inverse` |
| primary | f2 | [PMC12886974](https://pmc.ncbi.nlm.nih.gov/articles/PMC12886974.1/) | Discussion; environmental and external factors; p. 8 | `shared_pgs_caveat` |

**Response distinctions to preserve**

- Do not substitute another study/cohort/endpoint/timepoint
- Do not imply source consistency or clinical superiority from reported observational/vignette findings
- Do not turn the inverse genetic association into a causal treatment effect.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## d016

**multi_hop · revision 4 · answerable**

In the cardiorenal network meta-analysis, what did HFpEF comparisons report for drug-class differences in cardiovascular mortality, all-cause mortality and HF hospitalization/event, and how were the between-class comparisons derived?

**Expected response**

No significant drug-class differences in HFpEF CV mortality, all-cause mortality or HF hospitalization/event were reported. Between-class comparisons used indirect evidence with placebo as the common comparator, rather than randomized head-to-head comparisons.

**Required claims**

- `f1`: No significant drug-class differences in HFpEF CV mortality, all-cause mortality or HF hospitalization/event were reported.
- `f2`: Between-class comparisons used indirect evidence with placebo as the common comparator, rather than randomized head-to-head comparisons.

**Article roles declared by the question**

- Required: [PMC12683810](https://pmc.ncbi.nlm.nih.gov/articles/PMC12683810.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC12683810](https://pmc.ncbi.nlm.nih.gov/articles/PMC12683810.1/) | Results; indirect HFpEF class comparisons; p. 9 | `shared_nma_hfpef` |
| primary | f2 | [PMC12683810](https://pmc.ncbi.nlm.nih.gov/articles/PMC12683810.1/) | Methods; placebo-anchored indirect comparisons; p. 3 | `shared_nma_indirect` |

**Response distinctions to preserve**

- Do not substitute another study/cohort/endpoint/timepoint
- Do not imply source consistency or clinical superiority from reported observational/vignette findings

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## d017

**direct_lookup · revision 1 · answerable**

What oxidative-stress and platelet-marker changes were reported at follow-up in elderly diabetic HFpEF patients in the geriatric SGLT2 study?

**Expected response**

Nox-2 decreased from 1.24±.71 to 1.01±.04 nmol/L, 8-isoprostane from 70.41±5.67 to 65.67±4.16 pg/mL, Sp-Selectin from 125.92±12.84 to 101.84±4.42 ng/mL, and Gp-VI from 60.99±6.36 to 49.51±5.89 (unit unstated in this paragraph); all P<.0001; these biomarkers are not an HbA1c efficacy estimate or proof of a unique renal mechanism.

**Required claims**

- `f1`: Nox-2 decreased from 1.24±.71 to 1.01±.04 nmol/L, 8-isoprostane from 70.41±5.67 to 65.67±4.16 pg/mL, Sp-Selectin from 125.92±12.84 to 101.84±4.42 ng/mL, and Gp-VI from 60.99±6.36 to 49.51±5.89 (unit unstated in this paragraph); all P<.0001; these biomarkers are not an HbA1c efficacy estimate or proof of a unique renal mechanism.

**Article roles declared by the question**

- Required: [PMC11354916](https://pmc.ncbi.nlm.nih.gov/articles/PMC11354916.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC11354916](https://pmc.ncbi.nlm.nih.gov/articles/PMC11354916.1/) | Results; six-month oxidative/platelet markers; p. 4 | `shared_geriatric_markers` |

**Response distinctions to preserve**

- Do not substitute another study/cohort/endpoint/timepoint
- Do not imply source consistency or clinical superiority from reported observational/vignette findings

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## d018

**direct_lookup · revision 3 · answerable**

What pathogenic HIF-1α roles does Qin et al.’s HIF/zinc DKD review summarize?

**Expected response**

The review describes oxidative-stress pathways, inflammation, EMT/pathological angiogenesis and renal fibrosis. Its broader HIF roles also include EPO/angiogenesis; do not portray every HIF role as harmful or infer a clinical zinc regimen.

**Required claims**

- `f1`: The review describes oxidative-stress pathways, inflammation, EMT/pathological angiogenesis and renal fibrosis. Its broader HIF roles also include EPO/angiogenesis; do not portray every HIF role as harmful or infer a clinical zinc regimen.

**Article roles declared by the question**

- Required: [PMC11847805](https://pmc.ncbi.nlm.nih.gov/articles/PMC11847805.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC11847805](https://pmc.ncbi.nlm.nih.gov/articles/PMC11847805.1/) | Abstract; HIF pathogenic pathways; p. 1 | `hif_alternative` |

**Response distinctions to preserve**

- Do not substitute another study/cohort/endpoint/timepoint
- Do not imply source consistency or clinical superiority from reported observational/vignette findings

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## d019

**false_premise · revision 1 · false_premise**

Since He et al.’s primary GQD change-score analysis included all reviewed trials, how robust was its significant HbA1c benefit?

**Expected response**

Reject both premises: primary change-score analysis used only two trials/196 participants and HbA1c MD -1.92, CI -4.43 to .59, P=.13 was nonsignificant.

**Required claims**

- `f1`: Reject both premises: primary change-score analysis used only two trials/196 participants and HbA1c MD -1.92, CI -4.43 to .59, P=.13 was nonsignificant.

**Article roles declared by the question**

- Required: [PMC13423648](https://pmc.ncbi.nlm.nih.gov/articles/PMC13423648.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC13423648](https://pmc.ncbi.nlm.nih.gov/articles/PMC13423648.1/) | Results; primary change-score analysis; p. 6 | `gqd_primary` |

**Response distinctions to preserve**

- Do not substitute another study/cohort/endpoint/timepoint
- Do not imply source consistency or clinical superiority from reported observational/vignette findings

**Premise to correct:** Since He et al.’s primary GQD change-score analysis included all reviewed trials, how robust was its significant HbA1c benefit?

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## d020

**false_premise · revision 2 · false_premise**

Since the primary intention-to-treat analysis of Berthoumieux’s DSMES+CGM trial showed statistically significant HbA1c improvement at both follow-up visits, what was the later benefit?

**Expected response**

Reject the premise for the primary intention-to-treat analysis: the three-month difference was −0.7 percentage points (P=.03), while the six-month difference was −0.6 percentage points (95% CI −1.4 to 0.2; P=.12), not statistically significant.

**Required claims**

- `f1`: Reject the premise for the primary intention-to-treat analysis: the three-month difference was −0.7 percentage points (P=.03), while the six-month difference was −0.6 percentage points (95% CI −1.4 to 0.2; P=.12), not statistically significant.

**Article roles declared by the question**

- Required: [PMC13175446](https://pmc.ncbi.nlm.nih.gov/articles/PMC13175446.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC13175446](https://pmc.ncbi.nlm.nih.gov/articles/PMC13175446.1/) | Abstract Results; ITT HbA1c timepoints; p. 1 | `cgm_timepoints` |

**Response distinctions to preserve**

- Do not substitute another study/cohort/endpoint/timepoint
- Do not imply source consistency or clinical superiority from reported observational/vignette findings
- Do not substitute the sensitivity analysis excluding intervention nonparticipants for the primary intention-to-treat analysis.

**Premise to correct:** The primary intention-to-treat analysis found statistically significant HbA1c improvement at both three and six months.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## d021

**false_premise · revision 1 · false_premise**

Since Guo’s CGM counseling evaluation was a randomized clinical trial proving patient glycemic improvement, what supports that clinical benefit?

**Expected response**

Reject the premise: this was simulated vignette-based early-stage system evaluation, not a prospective interventional or randomized clinical trial.

**Required claims**

- `f1`: Reject the premise: this was simulated vignette-based early-stage system evaluation, not a prospective interventional or randomized clinical trial.

**Article roles declared by the question**

- Required: [PMC13430954](https://pmc.ncbi.nlm.nih.gov/articles/PMC13430954.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC13430954](https://pmc.ncbi.nlm.nih.gov/articles/PMC13430954.1/) | Methods; reporting framework and nonclinical evaluation; p. 9 | `ca_vignette` |

**Response distinctions to preserve**

- Do not substitute another study/cohort/endpoint/timepoint
- Do not imply source consistency or clinical superiority from reported observational/vignette findings

**Premise to correct:** Since Guo’s CGM counseling evaluation was a randomized clinical trial proving patient glycemic improvement, what supports that clinical benefit?

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## d022

**unanswerable · revision 1 · absent_fact**

What was five-year cardiovascular mortality in the randomized SIZE-DM cohort after generic versus innovator semaglutide?

**Expected response**

Not reported for the named cohort/timepoint in the selected main PDFs. State the evidence limit rather than inventing the requested result.

**Article roles declared by the question**

- Required: None recorded.
- Alternatives: None recorded.
- Decoys: None recorded.

**Evidence:** No positive answer-evidence set is defined. See the
expected refusal and the recorded search scope below.

**Response distinctions to preserve**

- Do not substitute another study/cohort/endpoint/timepoint
- Do not imply source consistency or clinical superiority from reported observational/vignette findings

**Missing-fact search scope**

Reviewed named original cohort/report follow-up; no selected article supplies the requested cohort/timepoint outcome. Supplements not included.

[PMC10363301](https://pmc.ncbi.nlm.nih.gov/articles/PMC10363301.1/), [PMC10452755](https://pmc.ncbi.nlm.nih.gov/articles/PMC10452755.1/), [PMC10607686](https://pmc.ncbi.nlm.nih.gov/articles/PMC10607686.1/), [PMC10619268](https://pmc.ncbi.nlm.nih.gov/articles/PMC10619268.1/), [PMC10985250](https://pmc.ncbi.nlm.nih.gov/articles/PMC10985250.1/), [PMC11265054](https://pmc.ncbi.nlm.nih.gov/articles/PMC11265054.1/), [PMC11354916](https://pmc.ncbi.nlm.nih.gov/articles/PMC11354916.1/), [PMC11373557](https://pmc.ncbi.nlm.nih.gov/articles/PMC11373557.1/), [PMC11374717](https://pmc.ncbi.nlm.nih.gov/articles/PMC11374717.1/), [PMC11514186](https://pmc.ncbi.nlm.nih.gov/articles/PMC11514186.1/), [PMC11549774](https://pmc.ncbi.nlm.nih.gov/articles/PMC11549774.1/), [PMC11847805](https://pmc.ncbi.nlm.nih.gov/articles/PMC11847805.1/), [PMC11973566](https://pmc.ncbi.nlm.nih.gov/articles/PMC11973566.1/), [PMC12003177](https://pmc.ncbi.nlm.nih.gov/articles/PMC12003177.1/), [PMC12419643](https://pmc.ncbi.nlm.nih.gov/articles/PMC12419643.1/), [PMC12436478](https://pmc.ncbi.nlm.nih.gov/articles/PMC12436478.1/), [PMC12683810](https://pmc.ncbi.nlm.nih.gov/articles/PMC12683810.1/), [PMC12880197](https://pmc.ncbi.nlm.nih.gov/articles/PMC12880197.1/), [PMC12886974](https://pmc.ncbi.nlm.nih.gov/articles/PMC12886974.1/), [PMC13107781](https://pmc.ncbi.nlm.nih.gov/articles/PMC13107781.1/), [PMC13175446](https://pmc.ncbi.nlm.nih.gov/articles/PMC13175446.1/), [PMC13311226](https://pmc.ncbi.nlm.nih.gov/articles/PMC13311226.1/), [PMC13423648](https://pmc.ncbi.nlm.nih.gov/articles/PMC13423648.1/), [PMC13430954](https://pmc.ncbi.nlm.nih.gov/articles/PMC13430954.1/), [PMC13433181](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433181.1/), [PMC13433218](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433218.1/), [PMC13433680](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433680.1/), [PMC13433862](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433862.1/), [PMC13439631](https://pmc.ncbi.nlm.nih.gov/articles/PMC13439631.1/), [PMC13472562](https://pmc.ncbi.nlm.nih.gov/articles/PMC13472562.1/), [PMC4804513](https://pmc.ncbi.nlm.nih.gov/articles/PMC4804513.1/), [PMC8866621](https://pmc.ncbi.nlm.nih.gov/articles/PMC8866621.1/)

**Overlap review:** 55 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## d023

**unanswerable · revision 1 · absent_fact**

What was the twelve-month HbA1c difference in the original Berthoumieux digital DSMES+CGM randomized cohort?

**Expected response**

Not reported for the named cohort/timepoint in the selected main PDFs. State the evidence limit rather than inventing the requested result.

**Article roles declared by the question**

- Required: None recorded.
- Alternatives: None recorded.
- Decoys: None recorded.

**Evidence:** No positive answer-evidence set is defined. See the
expected refusal and the recorded search scope below.

**Response distinctions to preserve**

- Do not substitute another study/cohort/endpoint/timepoint
- Do not imply source consistency or clinical superiority from reported observational/vignette findings

**Missing-fact search scope**

Reviewed named original cohort/report follow-up; no selected article supplies the requested cohort/timepoint outcome. Supplements not included.

[PMC10363301](https://pmc.ncbi.nlm.nih.gov/articles/PMC10363301.1/), [PMC10452755](https://pmc.ncbi.nlm.nih.gov/articles/PMC10452755.1/), [PMC10607686](https://pmc.ncbi.nlm.nih.gov/articles/PMC10607686.1/), [PMC10619268](https://pmc.ncbi.nlm.nih.gov/articles/PMC10619268.1/), [PMC10985250](https://pmc.ncbi.nlm.nih.gov/articles/PMC10985250.1/), [PMC11265054](https://pmc.ncbi.nlm.nih.gov/articles/PMC11265054.1/), [PMC11354916](https://pmc.ncbi.nlm.nih.gov/articles/PMC11354916.1/), [PMC11373557](https://pmc.ncbi.nlm.nih.gov/articles/PMC11373557.1/), [PMC11374717](https://pmc.ncbi.nlm.nih.gov/articles/PMC11374717.1/), [PMC11514186](https://pmc.ncbi.nlm.nih.gov/articles/PMC11514186.1/), [PMC11549774](https://pmc.ncbi.nlm.nih.gov/articles/PMC11549774.1/), [PMC11847805](https://pmc.ncbi.nlm.nih.gov/articles/PMC11847805.1/), [PMC11973566](https://pmc.ncbi.nlm.nih.gov/articles/PMC11973566.1/), [PMC12003177](https://pmc.ncbi.nlm.nih.gov/articles/PMC12003177.1/), [PMC12419643](https://pmc.ncbi.nlm.nih.gov/articles/PMC12419643.1/), [PMC12436478](https://pmc.ncbi.nlm.nih.gov/articles/PMC12436478.1/), [PMC12683810](https://pmc.ncbi.nlm.nih.gov/articles/PMC12683810.1/), [PMC12880197](https://pmc.ncbi.nlm.nih.gov/articles/PMC12880197.1/), [PMC12886974](https://pmc.ncbi.nlm.nih.gov/articles/PMC12886974.1/), [PMC13107781](https://pmc.ncbi.nlm.nih.gov/articles/PMC13107781.1/), [PMC13175446](https://pmc.ncbi.nlm.nih.gov/articles/PMC13175446.1/), [PMC13311226](https://pmc.ncbi.nlm.nih.gov/articles/PMC13311226.1/), [PMC13423648](https://pmc.ncbi.nlm.nih.gov/articles/PMC13423648.1/), [PMC13430954](https://pmc.ncbi.nlm.nih.gov/articles/PMC13430954.1/), [PMC13433181](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433181.1/), [PMC13433218](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433218.1/), [PMC13433680](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433680.1/), [PMC13433862](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433862.1/), [PMC13439631](https://pmc.ncbi.nlm.nih.gov/articles/PMC13439631.1/), [PMC13472562](https://pmc.ncbi.nlm.nih.gov/articles/PMC13472562.1/), [PMC4804513](https://pmc.ncbi.nlm.nih.gov/articles/PMC4804513.1/), [PMC8866621](https://pmc.ncbi.nlm.nih.gov/articles/PMC8866621.1/)

**Overlap review:** 55 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## d024

**unanswerable · revision 1 · absent_fact**

What exact zinc formulation, dose and duration did Lebedeva et al. recommend for adults with stage-3 DKD?

**Expected response**

Not reported for the named cohort/timepoint in the selected main PDFs. State the evidence limit rather than inventing the requested result.

**Article roles declared by the question**

- Required: None recorded.
- Alternatives: None recorded.
- Decoys: None recorded.

**Evidence:** No positive answer-evidence set is defined. See the
expected refusal and the recorded search scope below.

**Response distinctions to preserve**

- Do not substitute another study/cohort/endpoint/timepoint
- Do not imply source consistency or clinical superiority from reported observational/vignette findings

**Missing-fact search scope**

Reviewed named original cohort/report follow-up; no selected article supplies the requested cohort/timepoint outcome. Supplements not included.

[PMC10363301](https://pmc.ncbi.nlm.nih.gov/articles/PMC10363301.1/), [PMC10452755](https://pmc.ncbi.nlm.nih.gov/articles/PMC10452755.1/), [PMC10607686](https://pmc.ncbi.nlm.nih.gov/articles/PMC10607686.1/), [PMC10619268](https://pmc.ncbi.nlm.nih.gov/articles/PMC10619268.1/), [PMC10985250](https://pmc.ncbi.nlm.nih.gov/articles/PMC10985250.1/), [PMC11265054](https://pmc.ncbi.nlm.nih.gov/articles/PMC11265054.1/), [PMC11354916](https://pmc.ncbi.nlm.nih.gov/articles/PMC11354916.1/), [PMC11373557](https://pmc.ncbi.nlm.nih.gov/articles/PMC11373557.1/), [PMC11374717](https://pmc.ncbi.nlm.nih.gov/articles/PMC11374717.1/), [PMC11514186](https://pmc.ncbi.nlm.nih.gov/articles/PMC11514186.1/), [PMC11549774](https://pmc.ncbi.nlm.nih.gov/articles/PMC11549774.1/), [PMC11847805](https://pmc.ncbi.nlm.nih.gov/articles/PMC11847805.1/), [PMC11973566](https://pmc.ncbi.nlm.nih.gov/articles/PMC11973566.1/), [PMC12003177](https://pmc.ncbi.nlm.nih.gov/articles/PMC12003177.1/), [PMC12419643](https://pmc.ncbi.nlm.nih.gov/articles/PMC12419643.1/), [PMC12436478](https://pmc.ncbi.nlm.nih.gov/articles/PMC12436478.1/), [PMC12683810](https://pmc.ncbi.nlm.nih.gov/articles/PMC12683810.1/), [PMC12880197](https://pmc.ncbi.nlm.nih.gov/articles/PMC12880197.1/), [PMC12886974](https://pmc.ncbi.nlm.nih.gov/articles/PMC12886974.1/), [PMC13107781](https://pmc.ncbi.nlm.nih.gov/articles/PMC13107781.1/), [PMC13175446](https://pmc.ncbi.nlm.nih.gov/articles/PMC13175446.1/), [PMC13311226](https://pmc.ncbi.nlm.nih.gov/articles/PMC13311226.1/), [PMC13423648](https://pmc.ncbi.nlm.nih.gov/articles/PMC13423648.1/), [PMC13430954](https://pmc.ncbi.nlm.nih.gov/articles/PMC13430954.1/), [PMC13433181](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433181.1/), [PMC13433218](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433218.1/), [PMC13433680](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433680.1/), [PMC13433862](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433862.1/), [PMC13439631](https://pmc.ncbi.nlm.nih.gov/articles/PMC13439631.1/), [PMC13472562](https://pmc.ncbi.nlm.nih.gov/articles/PMC13472562.1/), [PMC4804513](https://pmc.ncbi.nlm.nih.gov/articles/PMC4804513.1/), [PMC8866621](https://pmc.ncbi.nlm.nih.gov/articles/PMC8866621.1/)

**Overlap review:** 55 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## d025

**direct_lookup · revision 1 · answerable**

Which two damaging DKD processes can HIF-1α promote, according to the selected zinc/HIF reviews?

**Expected response**

HIF-1α can promote inflammation and renal fibrosis; describe pathogenic processes rather than a clinical zinc dosing effect.

**Required claims**

- `f1`: HIF-1α can promote inflammation and renal fibrosis; describe pathogenic processes rather than a clinical zinc dosing effect.

**Article roles declared by the question**

- Required: [PMC13433218](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433218.1/)
- Alternatives: [PMC11847805](https://pmc.ncbi.nlm.nih.gov/articles/PMC11847805.1/)
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC13433218](https://pmc.ncbi.nlm.nih.gov/articles/PMC13433218.1/) | DKD; acute adaptive versus chronic HIF overactivation; p. 10 | `zinc_acute_chronic` |
| accepted_qin_alternative | f1 | [PMC11847805](https://pmc.ncbi.nlm.nih.gov/articles/PMC11847805.1/) | Abstract; HIF pathogenic pathways; p. 1 | `hif_alternative` |

**Response distinctions to preserve**

- Do not substitute another study/cohort/endpoint/timepoint
- Do not imply source consistency or clinical superiority from reported observational/vignette findings

**Overlap review:** 53 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## d026

**direct_lookup · revision 1 · answerable**

Why should Wang et al.’s three-cohort sleep-quality estimates not be treated as directly interchangeable effect sizes?

**Expected response**

Sleep measures differed across cohorts and harmonization occurred at the construct/score level; cross-cohort effect-size comparisons require caution.

**Required claims**

- `f1`: Sleep measures differed across cohorts and harmonization occurred at the construct/score level; cross-cohort effect-size comparisons require caution.

**Article roles declared by the question**

- Required: [PMC13472562](https://pmc.ncbi.nlm.nih.gov/articles/PMC13472562.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC13472562](https://pmc.ncbi.nlm.nih.gov/articles/PMC13472562.1/) | Abstract Methods; harmonization limit; p. 1 | `sleep_caution` |

**Response distinctions to preserve**

- Do not substitute another study/cohort/endpoint/timepoint
- Do not imply source consistency or clinical superiority from reported observational/vignette findings

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)
