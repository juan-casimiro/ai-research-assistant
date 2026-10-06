# Outliers evaluation cases

Generated from the current combined v2 inputs. Regenerate with
`python render_case_index.py`; do not edit this page by hand.

[All topics](README.md) · [Article catalogue](articles.md) ·
[Authoritative questions](../combined/v2/outliers/queries.json) ·
[Dependency map](../combined/v2/case_dependencies.json)

Expected responses are model-reviewed references, not biomedical expert
certification or observed RAG responses. No new scoring is performed here.

## Find a question

| ID | Category | Question |
| --- | --- | --- |
| [x001](#x001) | multi_hop | Yuan et al.’s abstract reports results for 195 taxa, 11 UK Biobank associations and three taxa validated in FinnGen. How does the UK-results section qualify those associations after multiple-comparison correction, and what does the later common-taxa section claim? |
| [x002](#x002) | false_premise | What probiotic treatment and dose did Yuan et al. administer to demonstrate reduced TB incidence in patients? |
| [x003](#x003) | direct_lookup | In Daw Elbait et al.’s qPCR-versus-metagenomic comparison, what kinds of wastewater sites supplied the four samples, and what did the authors identify as the main source of false negatives for each method? |
| [x004](#x004) | cross_doc_distractor | Across Garner et al.’s internationally sampled wastewater-treatment plants, how often did total ARG abundance decline after treatment when abundance was expressed per 16S rRNA gene and per millilitre? |
| [x005](#x005) | source_conflict | In Ciftci et al.’s dual-model Alzheimer paper, what accuracies are reported for the clinical ANN and MRI CNN, and what distinct tasks do those figures describe? |
| [x006](#x006) | false_premise | Which independent ADNI or OASIS-3 validation cohort confirmed the Alzheimer models’ reported performance? |
| [x007](#x007) | direct_lookup | In the TB review’s summary of a small PTB probiotic group, what happened to alpha diversity and beta diversity compared with patients who did not receive probiotics? |
| [x008](#x008) | false_premise | Which randomized clinical trial in the TB review established that AI-assisted precision-care strategies outperform standard care? |
| [x009](#x009) | unanswerable | Across the five selected outlier articles, how many downstream patients developed antibiotic-resistant infections linked to the sampled wastewater plants? |
| [x010](#x010) | direct_lookup | Across the Alzheimer ANN’s five training runs, which clinical features were most influential, and how did the authors describe diabetes and cardiovascular disease? |

## x001

**multi_hop · revision 1 · answerable**

Yuan et al.’s abstract reports results for 195 taxa, 11 UK Biobank associations and three taxa validated in FinnGen. How does the UK-results section qualify those associations after multiple-comparison correction, and what does the later common-taxa section claim?

**Expected response**

The abstract reports 195 taxa analyzed, 11 potential UK Biobank associations and three taxa (genus Akkermansia, family Verrucomicrobiacea and order Verrucomicrobiales) validated in FinnGen. The UK-results text labels the listed associations suggestive and says they were no longer significant after Bonferroni correction. A later section nevertheless describes three of those taxa as having significant causal associations in both databases. Preserve this internal inconsistency as the paper’s attributed wording; do not treat the reported genetic associations as an intervention effect.

**Required claims**

- `f1`: The abstract reports 195 taxa analyzed, 11 potential UK Biobank associations and three taxa (genus Akkermansia, family Verrucomicrobiacea and order Verrucomicrobiales) validated in FinnGen. The UK-results text labels the listed associations suggestive and says they were no longer significant after Bonferroni correction. A later section nevertheless describes three of those taxa as having significant causal associations in both databases. Preserve this internal inconsistency as the paper’s attributed wording; do not treat the reported genetic associations as an intervention effect.

**Article roles declared by the question**

- Required: [PMC10765819](https://pmc.ncbi.nlm.nih.gov/articles/PMC10765819.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC10765819](https://pmc.ncbi.nlm.nih.gov/articles/PMC10765819.1/) | Abstract: Methods and Results; p. 1 | `mr-summary` |
| primary | f1 | [PMC10765819](https://pmc.ncbi.nlm.nih.gov/articles/PMC10765819.1/) | Results: UK Biobank; p. 4 | `mr-uk-correction` |
| primary | f1 | [PMC10765819](https://pmc.ncbi.nlm.nih.gov/articles/PMC10765819.1/) | Results: UK Biobank; p. 4 | `mr-uk-bonferroni` |
| primary | f1 | [PMC10765819](https://pmc.ncbi.nlm.nih.gov/articles/PMC10765819.1/) | Results: Common taxa across databases; p. 8 | `mr-common-taxa` |

**Response distinctions to preserve**

- Do not equate environmental ARG abundance with patient infection incidence or clinical treatment outcomes.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../combined/v2/case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## x002

**false_premise · revision 1 · false_premise**

What probiotic treatment and dose did Yuan et al. administer to demonstrate reduced TB incidence in patients?

**Expected response**

None. Yuan et al. performed a bidirectional two-sample Mendelian-randomization analysis using genetic instruments and GWAS summary statistics; the study did not administer a probiotic or measure a treatment effect in patients.

**Required claims**

- `f1`: None. Yuan et al. performed a bidirectional two-sample Mendelian-randomization analysis using genetic instruments and GWAS summary statistics; the study did not administer a probiotic or measure a treatment effect in patients.

**Article roles declared by the question**

- Required: [PMC10765819](https://pmc.ncbi.nlm.nih.gov/articles/PMC10765819.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC10765819](https://pmc.ncbi.nlm.nih.gov/articles/PMC10765819.1/) | Abstract: Methods; p. 1 | `mr-design` |

**Response distinctions to preserve**

- Do not equate environmental ARG abundance with patient infection incidence or clinical treatment outcomes.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../combined/v2/case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## x003

**direct_lookup · revision 1 · answerable**

In Daw Elbait et al.’s qPCR-versus-metagenomic comparison, what kinds of wastewater sites supplied the four samples, and what did the authors identify as the main source of false negatives for each method?

**Expected response**

The four samples came from hospital, industrial, urban and rural areas. False negatives were more likely in qPCR when primer target sites were mutated; metagenomic sequencing missed ARGs with incomplete or low coverage under the bioinformatics-pipeline thresholds.

**Required claims**

- `f1`: The four samples came from hospital, industrial, urban and rural areas. False negatives were more likely in qPCR when primer target sites were mutated; metagenomic sequencing missed ARGs with incomplete or low coverage under the bioinformatics-pipeline thresholds.

**Article roles declared by the question**

- Required: [PMC10997137](https://pmc.ncbi.nlm.nih.gov/articles/PMC10997137.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC10997137](https://pmc.ncbi.nlm.nih.gov/articles/PMC10997137.1/) | Abstract; p. 1 | `qPCR-summary` |

**Response distinctions to preserve**

- Do not equate environmental ARG abundance with patient infection incidence or clinical treatment outcomes.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../combined/v2/case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## x004

**cross_doc_distractor · revision 2 · answerable**

Across Garner et al.’s internationally sampled wastewater-treatment plants, how often did total ARG abundance decline after treatment when abundance was expressed per 16S rRNA gene and per millilitre?

**Expected response**

Total ARG relative abundance (per 16S rRNA gene) decreased at 11 of 12 WWTPs, while absolute abundance (per mL) decreased at all 12.

**Required claims**

- `f1`: Total ARG relative abundance (per 16S rRNA gene) decreased at 11 of 12 WWTPs, while absolute abundance (per mL) decreased at all 12.

**Article roles declared by the question**

- Required: [PMC11411718](https://pmc.ncbi.nlm.nih.gov/articles/PMC11411718.1/)
- Alternatives: None recorded.
- Decoys: [PMC10997137](https://pmc.ncbi.nlm.nih.gov/articles/PMC10997137.1/)

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC11411718](https://pmc.ncbi.nlm.nih.gov/articles/PMC11411718.1/) | Abstract; p. 1 | `wwtp-summary` |

**Why the distractors matter**

- [PMC10997137](https://pmc.ncbi.nlm.nih.gov/articles/PMC10997137.1/) — Both papers report metagenomic wastewater measurements and ARG abundance.
  The four-site qPCR comparison does not report treatment outcomes across Garner et al.’s 12 internationally sourced WWTPs.
  Passage: Abstract; PDF p. 1; anchor `qPCR-summary`.

**Response distinctions to preserve**

- Do not equate environmental ARG abundance with patient infection incidence or clinical treatment outcomes.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../combined/v2/case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## x005

**source_conflict · revision 2 · answerable**

In Ciftci et al.’s dual-model Alzheimer paper, what accuracies are reported for the clinical ANN and MRI CNN, and what distinct tasks do those figures describe?

**Expected response**

The abstract reports ANN accuracy of 87.08% for early-stage risk prediction from clinical data and CNN accuracy of 97% for disease staging from MRI images. The detailed results instead describe the ANN as a binary classifier that detects Alzheimer’s versus no Alzheimer’s, with the same 87.08% accuracy. The article does not reconcile this with the early-stage risk-prediction label, so both descriptions are reported with their source location.

**Required claims**

- `f1`: The abstract reports ANN accuracy of 87.08% for early-stage risk prediction from clinical data and CNN accuracy of 97% for disease staging from MRI images.
- `f2`: The detailed results instead describe the ANN as a binary classifier that detects Alzheimer’s versus no Alzheimer’s, with the same 87.08% accuracy. The article does not reconcile this with the early-stage risk-prediction label, so both descriptions are reported with their source location.

**Article roles declared by the question**

- Required: [PMC12823827](https://pmc.ncbi.nlm.nih.gov/articles/PMC12823827.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC12823827](https://pmc.ncbi.nlm.nih.gov/articles/PMC12823827.1/) | Abstract; p. 1 | `alzheimer-summary` |
| primary | f2 | [PMC12823827](https://pmc.ncbi.nlm.nih.gov/articles/PMC12823827.1/) | Results: ANN binary classification; p. 7 | `alzheimer-ann-binary` |
| primary | f2 | [PMC12823827](https://pmc.ncbi.nlm.nih.gov/articles/PMC12823827.1/) | Results: ANN overall accuracy; p. 8 | `alzheimer-ann-accuracy` |

**Response distinctions to preserve**

- Do not treat the two models’ different datasets and tasks as a head-to-head clinical performance comparison.
- Do not treat the abstract’s early-stage risk label as proof of a prospective prediction endpoint.
- Do not report one reading as uncontested, and do not average or merge the two readings.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../combined/v2/case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## x006

**false_premise · revision 1 · false_premise**

Which independent ADNI or OASIS-3 validation cohort confirmed the Alzheimer models’ reported performance?

**Expected response**

None is reported. The authors list the absence of external validation using independent repositories such as ADNI or OASIS-3 as a limitation, which restricts generalizability.

**Required claims**

- `f1`: None is reported. The authors list the absence of external validation using independent repositories such as ADNI or OASIS-3 as a limitation, which restricts generalizability.

**Article roles declared by the question**

- Required: [PMC12823827](https://pmc.ncbi.nlm.nih.gov/articles/PMC12823827.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC12823827](https://pmc.ncbi.nlm.nih.gov/articles/PMC12823827.1/) | Discussion: Limitations; p. 11 | `alzheimer-validation-limit` |

**Response distinctions to preserve**

- Do not equate environmental ARG abundance with patient infection incidence or clinical treatment outcomes.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../combined/v2/case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## x007

**direct_lookup · revision 1 · answerable**

In the TB review’s summary of a small PTB probiotic group, what happened to alpha diversity and beta diversity compared with patients who did not receive probiotics?

**Expected response**

For the cited PTB group receiving probiotics (n=5), gut-microbiota alpha diversity increased significantly compared with those not receiving probiotics; no notable change in beta diversity was reported.

**Required claims**

- `f1`: For the cited PTB group receiving probiotics (n=5), gut-microbiota alpha diversity increased significantly compared with those not receiving probiotics; no notable change in beta diversity was reported.

**Article roles declared by the question**

- Required: [PMC13328407](https://pmc.ncbi.nlm.nih.gov/articles/PMC13328407.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC13328407](https://pmc.ncbi.nlm.nih.gov/articles/PMC13328407.1/) | 6.2 Clinical evidence for FMT and probiotics; p. 17 | `ptb-probiotic-summary` |

**Response distinctions to preserve**

- Do not equate environmental ARG abundance with patient infection incidence or clinical treatment outcomes.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../combined/v2/case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## x008

**false_premise · revision 1 · false_premise**

Which randomized clinical trial in the TB review established that AI-assisted precision-care strategies outperform standard care?

**Expected response**

The review identifies no such established superiority result. It says randomized controlled trials are essential to assess whether AI-assisted TB strategies are superior, equivalent or non-inferior to standard care.

**Required claims**

- `f1`: The review identifies no such established superiority result. It says randomized controlled trials are essential to assess whether AI-assisted TB strategies are superior, equivalent or non-inferior to standard care.

**Article roles declared by the question**

- Required: [PMC13328407](https://pmc.ncbi.nlm.nih.gov/articles/PMC13328407.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC13328407](https://pmc.ncbi.nlm.nih.gov/articles/PMC13328407.1/) | AI-assisted TB care limitations; p. 14 | `tb-ai-rct-gap` |

**Response distinctions to preserve**

- Do not equate environmental ARG abundance with patient infection incidence or clinical treatment outcomes.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../combined/v2/case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## x009

**unanswerable · revision 1 · absent_fact**

Across the five selected outlier articles, how many downstream patients developed antibiotic-resistant infections linked to the sampled wastewater plants?

**Expected response**

The selected corpus does not report a prospective patient infection count linked to the sampled wastewater plants. The wastewater papers measure environmental ARGs; neither follows exposed residents for clinical infection outcomes.

**Article roles declared by the question**

- Required: None recorded.
- Alternatives: None recorded.
- Decoys: None recorded.

**Evidence:** No positive answer-evidence set is defined. See the
expected refusal and the recorded search scope below.

**Response distinctions to preserve**

- Do not equate environmental ARG abundance with patient infection incidence or clinical treatment outcomes.

**Missing-fact search scope**

All five selected outlier articles in outliers-v1; both wastewater papers were checked in full for patient-linked infection outcomes, then the other three selected articles were reviewed for the same relation.

**Overlap review:** 55 other articles were considered; see the
[recorded dependency map](../combined/v2/case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## x010

**direct_lookup · revision 1 · answerable**

Across the Alzheimer ANN’s five training runs, which clinical features were most influential, and how did the authors describe diabetes and cardiovascular disease?

**Expected response**

MMSE score, age, systolic blood pressure, total cholesterol and family history were the most influential features across the five runs. Diabetes and cardiovascular disease were additional contributing comorbidities; the feature analysis was post-hoc and does not establish that those conditions cause Alzheimer disease.

**Required claims**

- `f1`: MMSE score, age, systolic blood pressure, total cholesterol and family history were the most influential features across the five runs. Diabetes and cardiovascular disease were additional contributing comorbidities; the feature analysis was post-hoc and does not establish that those conditions cause Alzheimer disease.

**Article roles declared by the question**

- Required: [PMC12823827](https://pmc.ncbi.nlm.nih.gov/articles/PMC12823827.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| primary | f1 | [PMC12823827](https://pmc.ncbi.nlm.nih.gov/articles/PMC12823827.1/) | Discussion: Feature importance; p. 11 | `alzheimer-feature-importance` |

**Response distinctions to preserve**

- Do not equate environmental ARG abundance with patient infection incidence or clinical treatment outcomes.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../combined/v2/case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)
