# Als-Ftd evaluation cases

Generated from the current combined v2 inputs. Regenerate with
`python render_case_index.py`; do not edit this page by hand.

[All topics](README.md) · [Article catalogue](articles.md) ·
[Authoritative questions](../combined/v2/als-ftd/queries.json) ·
[Dependency map](../combined/v2/case_dependencies.json)

Expected responses are model-reviewed references, not biomedical expert
certification or observed RAG responses. No new scoring is performed here.

## Find a question

| ID | Category | Question |
| --- | --- | --- |
| [a001](#a001) | direct_lookup | In Parameswaran et al. (2023), how did the PKR/eIF2α findings differ between human frontal-cortex samples and patient-derived motor neurons, and how cautiously should the authors’ explanation be interpreted? |
| [a002](#a002) | false_premise | Liu et al. (2024) proved that Cas13d improved survival and motor function in C9-500 BAC mice. Is that conclusion supported? |
| [a003](#a003) | direct_lookup | How did C9-V1/V3 responses to Cas13d differ between the same-donor iPSC line 2 and motor-neuron line 2 in Liu et al. (2024)? |
| [a004](#a004) | multi_hop | In Sachdev et al. (2024), did deleting exon 1A reproduce repeat-excision effects on both poly-GP elimination and network bursting? |
| [a005](#a005) | cross_doc_synthesis | Compare the endpoints and limits of Cas13d RNA targeting in Liu et al. (2024) with DNA editing in Sachdev et al. (2024). Why should neither be described as an established human treatment? |
| [a006](#a006) | direct_lookup | In Parameswaran et al. (2023), how did eif2ak2 knockdown affect antisense versus sense repeat-RNA motor axonopathy in zebrafish? |
| [a007](#a007) | direct_lookup | In the LeBlanc et al. case report, how did SPECT interpretation compare with genetic testing and subsequent pathology? |
| [a008](#a008) | cross_doc_synthesis | How do the human observations in Parameswaran et al. (2023) and LeBlanc et al. distinguish molecular association from diagnosis? |
| [a009](#a009) | cross_doc_distractor | What did the human case report by LeBlanc et al. use to support FTD-ALS after discordant brain imaging? |
| [a010](#a010) | multi_hop | What model-related explanation did Parameswaran et al. give for differences between Drosophila reports and their vertebrate repeat-RNA toxicity findings, and what experiment supported their PKR interpretation? |

## a001

**direct_lookup · revision 3 · answerable**

In Parameswaran et al. (2023), how did the PKR/eIF2α findings differ between human frontal-cortex samples and patient-derived motor neurons, and how cautiously should the authors’ explanation be interpreted?

**Expected response**

The human postmortem tissue showed increased pathway phosphorylation, whereas 38-day cultured motor neurons did not. Later activation is the authors’ possible explanation; different systems and times prevent a proved temporal or causal conclusion.

**Required claims**

- `a001:f1`: Frontal-cortex phosphorylated PKR and normalized phosphorylated eIF2α increased in C9FTD/ALS tissue.
- `a001:f2`: No phosphorylation difference was observed in two patient-derived lines versus isogenic controls at 38 days; later disease-stage activation was suggested, not demonstrated longitudinally.

**Article roles declared by the question**

- Required: [PMC10188109](https://pmc.ncbi.nlm.nih.gov/articles/PMC10188109.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| a001:set1 | a001:f1 | [PMC10188109](https://pmc.ncbi.nlm.nih.gov/articles/PMC10188109.1/) | Results: human tissue PKR/eIF2α; p. 9 | `isr-tissue` |
| a001:set1 | a001:f2 | [PMC10188109](https://pmc.ncbi.nlm.nih.gov/articles/PMC10188109.1/) | Results: 38-day induced motor neurons; p. 9 | `isr-young` |

**Response distinctions to preserve**

- Do not turn the later-stage explanation into a demonstrated longitudinal human result.
- Do not equate tissue immunohistochemistry and cultured-neuron protein extracts as identical assays.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../combined/v2/case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## a002

**false_premise · revision 2 · false_premise**

Liu et al. (2024) proved that Cas13d improved survival and motor function in C9-500 BAC mice. Is that conclusion supported?

**Expected response**

No. Liu cites prior work reporting no survival/motor deficits in this BAC model and reports reduced DPR levels after Cas13d treatment. DPR lowering does not demonstrate survival or motor rescue. The authors leave patient protection for future evaluation.

**Required claims**

- `a002:f1`: No: Liu cites prior work reporting no survival or motor deficits in this BAC model; the reported Cas13d result was reduced poly-GP/poly-GA, rather than demonstrated survival or motor rescue.
- `a002:f2`: Clinical protective effects still require evaluation.

**Article roles declared by the question**

- Required: [PMC11527445](https://pmc.ncbi.nlm.nih.gov/articles/PMC11527445.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| a002:set1 | a002:f1 | [PMC11527445](https://pmc.ncbi.nlm.nih.gov/articles/PMC11527445.1/) | Results: BAC mouse model limitations; p. 7 | `cas13-mice` |
| a002:set1 | a002:f2 | [PMC11527445](https://pmc.ncbi.nlm.nih.gov/articles/PMC11527445.1/) | Discussion: clinical protection remains untested; p. 10 | `cas13-clinical` |
| a002:set1 | a002:f1 | [PMC11527445](https://pmc.ncbi.nlm.nih.gov/articles/PMC11527445.1/) | Results: BAC mouse model limitations; p. 8 | `cas13-dpr` |

**Response distinctions to preserve**

- Do not equate DPR lowering with demonstrated survival or motor rescue.
- Do not attribute the cited BAC phenotype report to a new Liu survival experiment.
- Do not infer demonstrated patient protection.

**Premise to correct:** Liu et al. proved Cas13d improved survival and motor function in C9-500 BAC mice.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../combined/v2/case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## a003

**direct_lookup · revision 3 · answerable**

How did C9-V1/V3 responses to Cas13d differ between the same-donor iPSC line 2 and motor-neuron line 2 in Liu et al. (2024)?

**Expected response**

A mild C9-V1/V3 decrease was seen only in the induced motor neurons. A shared donor does not make cell states interchangeable; the authors suggest a cellular-environment effect.

**Required claims**

- `a003:f1`: A C9-V1/V3 decrease was observed only in iMNs, not in same-donor iPSCs; the authors suggest that cellular environment may influence targeting.

**Article roles declared by the question**

- Required: [PMC11527445](https://pmc.ncbi.nlm.nih.gov/articles/PMC11527445.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| a003:set1 | a003:f1 | [PMC11527445](https://pmc.ncbi.nlm.nih.gov/articles/PMC11527445.1/) | Results: same-donor iPSC versus iMN; p. 7 | `cas13-cell` |
| a003:set2 | a003:f1 | [PMC11527445](https://pmc.ncbi.nlm.nih.gov/articles/PMC11527445.1/) | Results: same-donor line-2 transcript response; p. 6 | `cas13-cell-results` |

**Response distinctions to preserve**

- Do not generalize the same-donor line-2 response to every patient line or cell state.
- Do not report the proposed cellular-environment explanation as a demonstrated mechanism or a mild decrease as necessarily statistically significant.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../combined/v2/case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## a004

**multi_hop · revision 2 · answerable**

In Sachdev et al. (2024), did deleting exon 1A reproduce repeat-excision effects on both poly-GP elimination and network bursting?

**Expected response**

No. Repeat or mutant-allele removal eliminated poly-GP; exon 1A excision left some poly-GP. At 3 weeks, REx and HET(Mut)x neurons showed network bursting, whereas C9-unedited and 1Ax showed no or minimal bursting. This establishes an edited-versus-unedited contrast, without a wild-type electrophysiology comparison.

**Required claims**

- `a004:f1`: No: repeat-expansion or mutant-allele removal eliminated poly-GP, whereas some poly-GP remained after exon 1A excision.
- `a004:f2`: At 3 weeks, REx and HET(Mut)x neurons showed network bursting; C9-unedited and 1Ax neurons showed no or minimal network bursting.

**Article roles declared by the question**

- Required: [PMC11047104](https://pmc.ncbi.nlm.nih.gov/articles/PMC11047104.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| a004:set1 | a004:f1 | [PMC11047104](https://pmc.ncbi.nlm.nih.gov/articles/PMC11047104.1/) | Results: repeat excision versus exon 1A poly-GP; p. 5 | `excision-dpr` |
| a004:set1 | a004:f2 | [PMC11047104](https://pmc.ncbi.nlm.nih.gov/articles/PMC11047104.1/) | Results: network burst activity; p. 7 | `excision-network` |
| a004:set2 | a004:f1 | [PMC11047104](https://pmc.ncbi.nlm.nih.gov/articles/PMC11047104.1/) | Figure 3 legend: repeat removal versus sense silencing; p. 6 | `excision-dpr-caption` |
| a004:set2 | a004:f2 | [PMC11047104](https://pmc.ncbi.nlm.nih.gov/articles/PMC11047104.1/) | Results: network burst activity; p. 7 | `excision-network` |
| a004:set3 | a004:f1 | [PMC11047104](https://pmc.ncbi.nlm.nih.gov/articles/PMC11047104.1/) | Results: repeat excision versus exon 1A poly-GP; p. 5 | `excision-dpr` |
| a004:set3 | a004:f2 | [PMC11047104](https://pmc.ncbi.nlm.nih.gov/articles/PMC11047104.1/) | Figure 5A legend: network bursting; p. 9 | `excision-network-caption` |
| a004:set4 | a004:f1 | [PMC11047104](https://pmc.ncbi.nlm.nih.gov/articles/PMC11047104.1/) | Figure 3 legend: repeat removal versus sense silencing; p. 6 | `excision-dpr-caption` |
| a004:set4 | a004:f2 | [PMC11047104](https://pmc.ncbi.nlm.nih.gov/articles/PMC11047104.1/) | Figure 5A legend: network bursting; p. 9 | `excision-network-caption` |

**Response distinctions to preserve**

- Do not claim exon 1A excision eliminated poly-GP.
- Do not claim network bursting was normalized to wild type: no WT electrophysiology comparison was performed.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../combined/v2/case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## a005

**cross_doc_synthesis · revision 2 · answerable**

Compare the endpoints and limits of Cas13d RNA targeting in Liu et al. (2024) with DNA editing in Sachdev et al. (2024). Why should neither be described as an established human treatment?

**Expected response**

Cas13d supports molecular target engagement in cells/mice; DNA excision supports cultured-neuron functional improvement. These are distinct preclinical endpoints, with model and donor limitations; neither demonstrates clinical efficacy.

**Required claims**

- `a005:f1`: Liu reported reduced poly-GP/poly-GA in BAC mice, cited prior work reporting no survival/motor deficits in this model, and left clinical protection for future evaluation.
- `a005:f2`: At 3 weeks, REx and HET(Mut)x cultured neurons showed network bursting while C9-unedited and 1Ax neurons showed no or minimal bursting; the biological insight came primarily from one donor line.

**Article roles declared by the question**

- Required: [PMC11047104](https://pmc.ncbi.nlm.nih.gov/articles/PMC11047104.1/), [PMC11527445](https://pmc.ncbi.nlm.nih.gov/articles/PMC11527445.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| a005:set1 | a005:f1 | [PMC11527445](https://pmc.ncbi.nlm.nih.gov/articles/PMC11527445.1/) | Results: BAC mouse model limitations; p. 7 | `cas13-mice` |
| a005:set1 | a005:f1 | [PMC11527445](https://pmc.ncbi.nlm.nih.gov/articles/PMC11527445.1/) | Discussion: clinical protection remains untested; p. 10 | `cas13-clinical` |
| a005:set1 | a005:f1 | [PMC11527445](https://pmc.ncbi.nlm.nih.gov/articles/PMC11527445.1/) | Results: BAC mouse model limitations; p. 8 | `cas13-dpr` |
| a005:set1 | a005:f2 | [PMC11047104](https://pmc.ncbi.nlm.nih.gov/articles/PMC11047104.1/) | Results: network burst activity; p. 7 | `excision-network` |
| a005:set1 | a005:f2 | [PMC11047104](https://pmc.ncbi.nlm.nih.gov/articles/PMC11047104.1/) | Discussion: donor scope; p. 9 | `excision-limit` |
| a005:set2 | a005:f1 | [PMC11527445](https://pmc.ncbi.nlm.nih.gov/articles/PMC11527445.1/) | Results: BAC mouse model limitations; p. 7 | `cas13-mice` |
| a005:set2 | a005:f1 | [PMC11527445](https://pmc.ncbi.nlm.nih.gov/articles/PMC11527445.1/) | Discussion: clinical protection remains untested; p. 10 | `cas13-clinical` |
| a005:set2 | a005:f1 | [PMC11527445](https://pmc.ncbi.nlm.nih.gov/articles/PMC11527445.1/) | Results: BAC mouse model limitations; p. 8 | `cas13-dpr` |
| a005:set2 | a005:f2 | [PMC11047104](https://pmc.ncbi.nlm.nih.gov/articles/PMC11047104.1/) | Figure 5A legend: network bursting; p. 9 | `excision-network-caption` |
| a005:set2 | a005:f2 | [PMC11047104](https://pmc.ncbi.nlm.nih.gov/articles/PMC11047104.1/) | Discussion: donor scope; p. 9 | `excision-limit` |

**Response distinctions to preserve**

- Do not equate mouse DPR lowering with motor or survival benefit.
- Do not turn cultured-neuron bursting into demonstrated clinical efficacy or normalization to wild type.
- Do not generalize primarily single-donor findings to all patients.

**Overlap review:** 53 other articles were considered; see the
[recorded dependency map](../combined/v2/case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## a006

**direct_lookup · revision 2 · answerable**

In Parameswaran et al. (2023), how did eif2ak2 knockdown affect antisense versus sense repeat-RNA motor axonopathy in zebrafish?

**Expected response**

PKR-ortholog reduction protected the antisense condition, whereas sense-induced abnormalities were not protected. This is an embryonic zebrafish result, not a clinical trial.

**Required claims**

- `a006:f1`: It mitigated antisense-induced axonal-length/branching abnormalities; no protective effect was observed for the sense-RNA condition.

**Article roles declared by the question**

- Required: [PMC10188109](https://pmc.ncbi.nlm.nih.gov/articles/PMC10188109.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| a006:set1 | a006:f1 | [PMC10188109](https://pmc.ncbi.nlm.nih.gov/articles/PMC10188109.1/) | Results: eif2ak2 knockdown; p. 11 | `zebrafish` |
| a006:set2 | a006:f1 | [PMC10188109](https://pmc.ncbi.nlm.nih.gov/articles/PMC10188109.1/) | Figure 7 legend: strand-specific toxicity result; p. 16 | `zebrafish-caption-result` |
| a006:set2 | a006:f1 | [PMC10188109](https://pmc.ncbi.nlm.nih.gov/articles/PMC10188109.1/) | Figure 7C-F legend: motor axon endpoints; p. 17 | `zebrafish-caption-endpoints` |

**Response distinctions to preserve**

- Do not swap the sense and antisense rescue results.
- Do not infer clinical efficacy from embryonic zebrafish axon endpoints.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../combined/v2/case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## a007

**direct_lookup · revision 3 · answerable**

In the LeBlanc et al. case report, how did SPECT interpretation compare with genetic testing and subsequent pathology?

**Expected response**

SPECT suggested Alzheimer disease, but genetic testing identified the C9orf72 expansion and the autopsy confirmed FTLD-TDP type C. The single case supports diagnostic discordance, not a population accuracy estimate.

**Required claims**

- `a007:f1`: SPECT was interpreted as most consistent with Alzheimer disease rather than FTLD.
- `a007:f2`: Testing found a C9orf72 GGGGCC expansion supporting FTD-ALS; autopsy confirmed FTLD with TDP pathology type C.

**Article roles declared by the question**

- Required: [PMC10802081](https://pmc.ncbi.nlm.nih.gov/articles/PMC10802081.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| a007:set1 | a007:f1 | [PMC10802081](https://pmc.ncbi.nlm.nih.gov/articles/PMC10802081.1/) | Case report: imaging interpretation; p. 3 | `case-imaging` |
| a007:set1 | a007:f2 | [PMC10802081](https://pmc.ncbi.nlm.nih.gov/articles/PMC10802081.1/) | Case report: genetic diagnosis; p. 3 | `case-genetics` |
| a007:set1 | a007:f2 | [PMC10802081](https://pmc.ncbi.nlm.nih.gov/articles/PMC10802081.1/) | Case report: autopsy; p. 3 | `case-autopsy` |

**Response distinctions to preserve**

- Do not treat the SPECT interpretation as the final pathological diagnosis.
- Do not infer population diagnostic accuracy from one patient.
- Do not substitute another TDP subtype for reported type C.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../combined/v2/case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## a008

**cross_doc_synthesis · revision 2 · answerable**

How do the human observations in Parameswaran et al. (2023) and LeBlanc et al. distinguish molecular association from diagnosis?

**Expected response**

The postmortem series offers a pathway association; the case offers a diagnostic history grounded in genetics and pathology. Neither establishes PKR testing as a validated diagnostic test or a therapy.

**Required claims**

- `a008:f1`: In human postmortem frontal cortex, phosphorylated PKR and normalized phosphorylated eIF2α were increased in C9FTD/ALS samples versus controls.
- `a008:f2`: The individual case was diagnosed through genetic evidence despite discordant SPECT, with pathology confirmation.

**Article roles declared by the question**

- Required: [PMC10188109](https://pmc.ncbi.nlm.nih.gov/articles/PMC10188109.1/), [PMC10802081](https://pmc.ncbi.nlm.nih.gov/articles/PMC10802081.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| a008:set1 | a008:f1 | [PMC10188109](https://pmc.ncbi.nlm.nih.gov/articles/PMC10188109.1/) | Results: human tissue PKR/eIF2α; p. 9 | `isr-tissue` |
| a008:set1 | a008:f2 | [PMC10802081](https://pmc.ncbi.nlm.nih.gov/articles/PMC10802081.1/) | Case report: imaging interpretation; p. 3 | `case-imaging` |
| a008:set1 | a008:f2 | [PMC10802081](https://pmc.ncbi.nlm.nih.gov/articles/PMC10802081.1/) | Case report: genetic diagnosis; p. 3 | `case-genetics` |
| a008:set1 | a008:f2 | [PMC10802081](https://pmc.ncbi.nlm.nih.gov/articles/PMC10802081.1/) | Case report: autopsy; p. 3 | `case-autopsy` |

**Response distinctions to preserve**

- Do not equate postmortem pathway association with diagnostic validation or a causal treatment effect.
- Do not conflate the tissue series with the single case or attribute PKR diagnostic testing to the case.

**Overlap review:** 53 other articles were considered; see the
[recorded dependency map](../combined/v2/case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## a009

**cross_doc_distractor · revision 3 · answerable**

What did the human case report by LeBlanc et al. use to support FTD-ALS after discordant brain imaging?

**Expected response**

Genetic testing identified a C9orf72 GGGGCC repeat expansion, confirming FTD-ALS after discordant SPECT imaging.

**Required claims**

- `a009:f1`: Genetic testing identified a C9orf72 GGGGCC repeat expansion, confirming FTD-ALS after discordant SPECT imaging.

**Article roles declared by the question**

- Required: [PMC10802081](https://pmc.ncbi.nlm.nih.gov/articles/PMC10802081.1/)
- Alternatives: None recorded.
- Decoys: [PMC11527445](https://pmc.ncbi.nlm.nih.gov/articles/PMC11527445.1/)

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| a009:set1 | a009:f1 | [PMC10802081](https://pmc.ncbi.nlm.nih.gov/articles/PMC10802081.1/) | Case report: genetic diagnosis; p. 3 | `case-genetics` |

**Why the distractors matter**

- [PMC11527445](https://pmc.ncbi.nlm.nih.gov/articles/PMC11527445.1/) — Human/patient language and C9orf72 genetics resemble clinical evidence.
  These are cultured iPSC/iMN line responses to Cas13d, not diagnostic observations in the case-report patient.
  Passage: Results: same-donor iPSC versus iMN; PDF p. 7; anchor `cas13-cell`.

**Response distinctions to preserve**

- Do not use Cas13d-treated cultured patient-derived cells as this patient’s diagnostic evidence.
- Do not equate SPECT interpretation with genetic/pathological findings.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../combined/v2/case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)

## a010

**multi_hop · revision 2 · answerable**

What model-related explanation did Parameswaran et al. give for differences between Drosophila reports and their vertebrate repeat-RNA toxicity findings, and what experiment supported their PKR interpretation?

**Expected response**

The authors propose vertebrate PKR availability as a partial model explanation and show strand-specific rescue by PKR-ortholog knockdown in zebrafish. The Drosophila observations are cited secondary evidence, not newly performed experiments here.

**Required claims**

- `a010:f1`: PKR is present in vertebrates and absent in Drosophila; the authors offer this as a partial explanation, not proof that every model discrepancy is resolved.
- `a010:f2`: Reducing eif2ak2 mitigated antisense but not sense axonopathy in zebrafish.

**Article roles declared by the question**

- Required: [PMC10188109](https://pmc.ncbi.nlm.nih.gov/articles/PMC10188109.1/)
- Alternatives: None recorded.
- Decoys: None recorded.

**Accepted evidence sets**

Each set is a complete accepted route to the answer. Alternatives are not
additional mandatory sources. Page numbers refer to the pinned PDF.

| Set | Claim | Article | Passage / PDF page | Anchor |
| --- | --- | --- | --- | --- |
| a010:set1 | a010:f1 | [PMC10188109](https://pmc.ncbi.nlm.nih.gov/articles/PMC10188109.1/) | Discussion: model-specific PKR expression; p. 13 | `model-pkr` |
| a010:set1 | a010:f2 | [PMC10188109](https://pmc.ncbi.nlm.nih.gov/articles/PMC10188109.1/) | Results: eif2ak2 knockdown; p. 11 | `zebrafish` |
| a010:set2 | a010:f1 | [PMC10188109](https://pmc.ncbi.nlm.nih.gov/articles/PMC10188109.1/) | Discussion: model-specific PKR expression; p. 13 | `model-pkr` |
| a010:set2 | a010:f2 | [PMC10188109](https://pmc.ncbi.nlm.nih.gov/articles/PMC10188109.1/) | Figure 7 legend: strand-specific toxicity result; p. 16 | `zebrafish-caption-result` |
| a010:set2 | a010:f2 | [PMC10188109](https://pmc.ncbi.nlm.nih.gov/articles/PMC10188109.1/) | Figure 7C-F legend: motor axon endpoints; p. 17 | `zebrafish-caption-endpoints` |

**Response distinctions to preserve**

- Do not present cited Drosophila observations as experiments performed in this paper.
- Do not treat PKR distribution as a proven complete explanation of model differences.
- Do not claim sense axonopathy was rescued by eif2ak2 knockdown.

**Overlap review:** 54 other articles were considered; see the
[recorded dependency map](../combined/v2/case_dependencies.json).
Review scope does not make every article a distractor or accepted source.

[Back to questions](#find-a-question)
