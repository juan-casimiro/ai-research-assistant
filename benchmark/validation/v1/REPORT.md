# Benchmark gold validation report — Codex-led final decisions

**145 of 158 cases require no material correction; 13 require correction, 13 blocking.**

Findings only: gold questions, anchors, source documents and evaluation runs remain unchanged. PR #45 stays open; corrections belong to a separate revision task.

Historical review ran on October 3–4; Codex-led final review completed on October 5, 2026. This is model review of extracted `.txt` files, not biomedical expert validation, retrieval evaluation or generated-answer evaluation. No PDFs were used.

## Scope and decision authority

Stages 0–5 covered all 158 cases. Stage 6 added 59 targeted, one-case Codex second opinions: all adjudications, minor audit notes, and Claude-authored gold. The reviewer saw an earlier review, so Stage 6 was neither blind nor fully independent. Codex then decided all 33 remaining disagreements/proposed defects and Kimi ambiguity signals in fresh one-case sessions. The other 27 agreeing Stage 6 decisions were accepted; 98 cases retain their historical decisions. This is not a fresh independent 158-case Codex review.

Some category-defect replies use gold_stands to refer to factual content. The findings preserve that returned flag separately from scoring_contract_stands, which is false for material defects under the stated rule.

Decision precedence: final Codex adjudication, then agreeing Stage 6 Codex result, then historical Stages 0–5. Earlier model results are preserved even when superseded.

## Blocking rule

Blocking means a defect can cause a correct answer to be scored incorrectly (including a wrong answer accepted), makes the question materially ambiguous, or violates the category admission criterion used for benchmark scoring. Category defects are blocking even when legacy document-only scoring ignores them. A valid_minor note is non_blocking only if none of those conditions applies; valid has severity none. Unsettled extraction is a blocking validation gap, not a proven source defect. Evaluate the declared fact/evidence/category contract, not hypothetical lenient scoring or whether a blind model happened to answer fully.

This replaces the historical rule that treated category defects as non-blocking when legacy document scoring was unaffected. Severity changes are explicit methodology changes, not new retrieval failures.

## Verdicts

| Set | Cases | Valid | Minor note | Needs correction | Blocking |
| --- | ---: | ---: | ---: | ---: | ---: |
| als-ftd | 10 | 4 | 3 | 3 | 3 |
| cardiology | 45 | 36 | 4 | 5 | 5 |
| diabetes | 49 | 35 | 11 | 3 | 3 |
| oncology | 44 | 35 | 9 | 0 | 0 |
| outliers | 10 | 6 | 2 | 2 | 2 |
| **Total** | **158** | **116** | **29** | **13** | **13** |

| Category | Cases | Valid | Minor note | Needs correction | Blocking |
| --- | ---: | ---: | ---: | ---: | ---: |
| cross_doc_distractor | 15 | 9 | 4 | 2 | 2 |
| cross_doc_synthesis | 18 | 12 | 4 | 2 | 2 |
| direct_lookup | 64 | 54 | 8 | 2 | 2 |
| false_premise | 18 | 14 | 3 | 1 | 1 |
| multi_hop | 32 | 22 | 4 | 6 | 6 |
| unanswerable | 11 | 5 | 6 | 0 | 0 |
| **Total** | **158** | **116** | **29** | **13** | **13** |

## Cases requiring correction

| Case | Verdict | Blocking |
| --- | --- | --- |
| als-ftd a001 | `defect_category` | yes |
| als-ftd a007 | `defect_category` | yes |
| als-ftd a009 | `ambiguous_question` | yes |
| cardiology c003 | `defect_gold` | yes |
| cardiology c012 | `defect_gold` | yes |
| cardiology c013 | `defect_category` | yes |
| cardiology c016 | `ambiguous_question` | yes |
| diabetes d015 | `defect_category` | yes |
| diabetes d016 | `defect_category` | yes |
| diabetes d020 | `premise_not_false` | yes |
| cardiology q058 | `defect_gold` | yes |
| outliers x004 | `defect_category` | yes |
| outliers x005 | `ambiguous_question` | yes |

Each decision below is Codex-led. Full standards checks, all citations, competing review claims and proposed correction text are in [final findings](results/final_findings.json) and the linked per-case results. Line numbers are one-based in the frozen `.txt` extraction.

### als-ftd a001

The required facts and cautious reference answer are supported. The category is defective: lines 318–331 form one continuous local Results passage containing the tissue finding, neuron finding, and tentative explanation. The supplied multi_hop criterion requires separated evidence anchors that must be connected; splitting consecutive sentences into two anchors does not satisfy it. No unresolved text-extraction issue affects this decision.

**Blocking basis:** Blocking under the packet’s express rule: violating a category admission criterion used for benchmark scoring is blocking even if document-only answer scoring would accept the correct answer. I therefore agree with the first review’s verdict and gold status, but disagree with its non_blocking severity.

**Proposed correction:** Relabel this as direct_lookup while retaining the facts and answer rubric. Merging the anchors alone would leave the category defect if multi_hop remained. The pending-review wording in acceptable_alternatives can be updated as housekeeping. Gold remains unchanged in this adjudication.

`als-ftd-pmc10188109.txt:316–319` — Lines 316–319: one Results subsection introduces both systems.

```text
Increased levels of phosphorylated PKR and eIF2α in C9FTD/ALS 
patients
To study disease relevance, we next determined the levels of phosphorylated PKR and eIF2α in 
C9FTD/ALS patient postmortem tissues and in patient- derived iPSCs motor neurons.
```

`als-ftd-pmc10188109.txt:320–322` — Lines 320–322: increased phosphorylated PKR in patient frontal cortex.

```text
tochemistry staining showed that the level of phosphorylated PKR is increased in the frontal cortex, 
especially in the large pyramidal neurons, of patients carrying C9ORF72 repeat expansions compared 
to age- matched non- disease controls
```

`als-ftd-pmc10188109.txt:324–325` — Lines 324–325: increased normalized phosphorylated eIF2α in patient tissue.

```text
2020). In addition, the level of phosphorylated eIF2α after normalizing to the total eIF2α level is also 
significantly increased, despite the heterogeneity of eIF2α protein levels in patients
```

### als-ftd a007

The source supports the gold answer for this one patient. SPECT favored Alzheimer disease over FTLD; genetic testing confirmed FTD-ALS; autopsy confirmed FTLD with TDP pathology type C. The category fails admission: all required findings are available in one short, continuous case account at lines 191–216, so answering does not require connecting separated evidence passages. No material source conflict or unresolved text-extraction issue remains.

**Blocking basis:** The supplied blocking rule expressly makes a violation of a category admission criterion blocking, even if document-only scoring would accept the answer. The first review identified the category defect but assigned non_blocking severity; that is the point of disagreement.

**Proposed correction:** Relabel the case as direct_lookup, or the benchmark’s equivalent single-passage category. Retain the facts, answer and source anchors; record a new query revision for the category change.

`als-ftd-pmc10802081.txt:90–90` — Line 90: identifies the single patient in the case report.

```text
A 42-year-old previously healthy male with a remote
```

`als-ftd-pmc10802081.txt:191–201` — Lines 191–201: the SPECT interpretation and genetic result appear consecutively in one local passage.

```text
A brain SPECT scan was ordered and demonstrated
moderate decreased perfusion to the parietal lobes bilat-
erally, left greater than right, with some involvement of the
posterior aspect of the left frontal lobe. The nuclear
medicine radiologist concluded the distribution was most
in keeping with Alzheimer ’s disease and it was not felt to
represent frontotemporal lobar degeneration (FTLD).
However, given ongoing clinical suspicion for a rapidly
progressive neurodegenerative cause, genetic testing was
performed and identi ﬁed a repeat expansion of GGGGCC
in C9orf72, thereby con ﬁrming a diagnosis of FTD-ALS.
```

`als-ftd-pmc10802081.txt:211–216` — Lines 211–216: the same case account supplies the subsequent autopsy finding.

```text
Ultimately, he died from complica-
tions of aspiration pneumonia. His family consented to
post-mortem autopsy and the ﬁnal report con ﬁrmed a
fronto-temporal lobar degeneration with transactive re-
sponse DNA binding protein (TDP) pathology, interna-
tional harmonized classi ﬁcation type C.
```

### als-ftd a009

The source supports both keyed findings, but the question asks what supported FTD-ALS after discordant imaging. The article answers that with genetic testing alone; autopsy was later postmortem confirmation. A genetics-only answer is therefore responsive yet would omit a mandatory keyed element. The decoy shares C9orf72 and patient language but supplies no diagnosis for LeBlanc’s patient. No unresolved text-extraction issue affects this decision.

**Blocking basis:** Blocking under the supplied rule: the mandatory autopsy element can cause a correct genetics-only answer to be scored incomplete. Proximity of the autopsy passage and an earlier answer that included it do not remove that risk.

**Proposed correction:** Require the C9orf72 expansion and make autopsy confirmation supplementary, or revise the question to explicitly ask for both the diagnostic finding and later autopsy result. Keep the gold unchanged pending revision.

`als-ftd-pmc10802081.txt:196–201` — Lines 196–201: after discordant SPECT imaging, genetic testing confirmed the diagnosis.

```text
in keeping with Alzheimer ’s disease and it was not felt to
represent frontotemporal lobar degeneration (FTLD).
However, given ongoing clinical suspicion for a rapidly
progressive neurodegenerative cause, genetic testing was
performed and identi ﬁed a repeat expansion of GGGGCC
in C9orf72, thereby con ﬁrming a diagnosis of FTD-ALS.
```

`als-ftd-pmc10802081.txt:211–216` — Lines 211–216: the keyed pathology finding is accurate, but occurred after death.

```text
Ultimately, he died from complica-
tions of aspiration pneumonia. His family consented to
post-mortem autopsy and the ﬁnal report con ﬁrmed a
fronto-temporal lobar degeneration with transactive re-
sponse DNA binding protein (TDP) pathology, interna-
tional harmonized classi ﬁcation type C.
```

`als-ftd-pmc10802081.txt:449–451` — Lines 449–451: the authors’ summary identifies genetic testing as the response to discordant imaging.

```text
although the neuroimagingﬁndings were not consistent with
FTD, the history led to further pursuance of genetic testing
which ultimately conﬁrmed the diagnosis.
```

### cardiology c003

The numerical gold answer and five-patient limitation are supported. But f1’s declared endpoint calls the 0.989/0.956/0.967 values record-level, while the article assigns them to Lorenz scattergrams. The same external MS-AF evaluation reports different ECG-record metrics. The question does not specify the evaluation level, so the declared contract can reject an appropriately scoped record-level response or accept scattergram figures as record-level. This is more than a minor annotation issue. No text-extraction gap remains.

**Blocking basis:** Blocking: the incorrect endpoint metadata and unspecified performance level create a material answer and scoring ambiguity under the supplied rule. The separate, conflicting record-level values make this consequential. The multi-hop category itself is satisfied.

**Proposed correction:** Revise the question to specify Lorenz-scattergram-level external AF detection, label f1’s endpoint accordingly, and state that scope in the reference answer. Keep the five-patient limitation. This is a recommended revision; the current gold remains unchanged.

`cardio-af-lorenz-detection.txt:254–259` — Lines 254–259: the study distinguishes scattergram-level from record-level performance.

```text
The performance evaluation of the model was divided 
into two levels. In the first level, based on the LS with 85 
R waves, the predicted classification of the model was 
compared with the real classification of the LS to evalu -
ate the model performance. The second level was based 
on long-range ECG records.
```

`cardio-af-lorenz-detection.txt:361–368` — Lines 361–368: the gold figures are external Lorenz-scattergram results.

```text
Performance evaluation in the lorenz scattergram
The confusion matrix for diagnostic model in the inter -
nal and external validation sets was shown in Table  2. In 
the internal validation set, the sensitivity of the model for 
diagnosing AF was 0.992, the specificity was 0.973, and 
the accuracy was 0.983. In the external validation set, the 
sensitivity of the model for diagnosing AF was 0.989, the 
specificity was 0.956, and the accuracy was 0.967.
```

`cardio-af-lorenz-detection.txt:373–379` — Lines 373–379: external ECG-record results have different values, creating a consequential scope conflict.

```text
Performance evaluation in ECG records
In the 113 ECG records from the MS-AF dataset. The 
sensitivity of the model diagnosis of paroxysmal AF was 
1.000, the specificity was 0.870, and the accuracy was 
0.876. The sensitivity of the model diagnosis of persistent 
AF was 0.927, the specificity was 1.000, and the accuracy 
was 0.973.
```

### cardiology c012

The reference answer's CKD figures are supported by the abstract and Results narrative, but Table 2 binds different adjusted figures to the same population and endpoints. These are source conflicts, not stated rounding. The HFpEF source likewise describes its design as case-control in Methods and retrospective cohort in its abstract and elsewhere. The reference answer selects one description without exposing the conflict. No text-extraction gap prevents binding the Table 2 rows. The competing HFpEF article is similar but has a different comparison design; it does not resolve the conflicts.

**Blocking basis:** Blocking under the supplied rule: the current exact-value tolerance and unqualified design claim can cause an answer accurately using Table 2 or the source's cohort label to be scored incorrectly. The small size of the numerical differences does not remove that scoring risk.

**Proposed correction:** Retain the narrative CKD figures with explicit attribution, disclose and accept Table 2's adjusted figures as source-supported alternatives, and add the table passage to the evidence set. Describe the HFpEF study as retrospective observational, noting its case-control and cohort self-descriptions; accept either attributed label. Preserve the non-causal interpretation. These are recommended revisions only.

`cardio-ckd-sglt2-acei-arb.txt:319–323` — Lines 318–322: the Results narrative supports the reference answer's renal estimate.

```text
SGLT2 inhibitor users had a lower incidence rate (3.78 
vs. 6.59 per 100 person -years) and a significantly 
lower risk of ESRD/dialysis (aHR = 0.35, 95% 
confidence interval [CI] = 0.19~0.67) than did 
nonusers.
```

`cardio-ckd-sglt2-acei-arb.txt:422–423` — Lines 422–423: the Results narrative supports the reference answer's infection estimate.

```text
significantly greater risk of developing GUTIs (aHR = 
1.78, 95% CI = 1.12~2.84).
```

`cardio-ckd-sglt2-acei-arb.txt:525–526` — Lines 525–526: Table 2 identifies the adjusted HR column.

```text
Group No. of events PY Incidence (95% CI) Crude HR (95% CI) p value Adjusted HR* (95% CI) p value 
Congestive heart failure
```

### cardiology c013

The numerical answer is supported, but the question fails the supplied multi_hop admission criterion. One contiguous abstract passage answers every requested part, so two separated anchors need not be connected. The same passage is missing as a complete alternative evidence set. The abstract’s 2022 price statement and Methods’ July 2023 NADAC extraction detail remain unreconciled in the supplied text; answers should attribute both when discussing that detail.

**Blocking basis:** The packet expressly makes a category admission violation blocking, even if legacy document-only scoring ignores it. The undeclared complete abstract alternative can also cause a correctly evidenced answer to fail the declared evidence contract. The first review’s non_blocking severity therefore does not follow the binding rule.

**Proposed correction:** Relabel the case as direct_lookup and add the complete abstract passage as an accepted evidence set. Keep the reported base-case CNTs. Clarify that “2022 US prices” is the abstract’s statement while Methods describes costs as 75% of NADAC extracted in July 2023; do not invent a reconciliation. Treat the unasked current-price and head-to-head caveats as optional context.

`cardio-hfpef-dapagliflozin-cost-analysis.txt:20–34` — Lines 20–34: one contiguous abstract passage supplies the trial sources, stated price year, endpoint, and both attributed CNTs. It is also an undeclared complete alternative to the two-anchor evidence set.

```text
Methods: We compared the annualized cost needed to treat (CNT) to prevent the
composite outcome of total HF hospitalizations and CVD with dapagli ﬂozin or
sacubitril– valsartan. The CNT was estimated by multiplying the annualized
number needed to treat (aNNT) by the annual cost of therapy. The aNNT was
calculated based on data collected from the DELIVER trial for dapagli ﬂozin and a
pooled analysis of the PARAGLIDE-HF and PARAGON-HF trials for
sacubitril– valsartan. Costs were based on 2022 US prices. Scenario analyses
were performed to attenuate the differences in the studies ’ populations.
Results: The aNNT with dapagliﬂozin in DELIVER was 30 (95% conﬁdence interval
[CI]: 21-62) versus 44 (95% CI: 25-311) with sacubitril – valsartan in a pooled
analysis of PARAGLIDE-HF and PARAGON-HF, with an annual cost of $4,951 and
$5,576, respectively. The corresponding CNTs were $148,547.13 (95% CI:
$103,982.99– $306,997.39) for dapagli ﬂozin and $245,346.77 (95% CI:
$139,401.58– 1,734,155.60) for sacubitril – valsartan for preventing the
composite outcome of CVD and HF hospitalizations.
```

`cardio-hfpef-dapagliflozin-cost-analysis.txt:168–171` — Lines 168–171: Methods gives a July 2023 extraction date for the pricing input. The text does not reconcile that detail with the abstract’s 2022 US price statement.

```text
The CNT was calculated by multiplying the aNNT by the annual
t r e a t m e n tc o s t(Mayne et al., 2006). Drug costs were calculated as 75%
of the US National Average Drug Acquisition Cost (NADAC),
extracted in July 2023 (Medicaid.gov, 2023).
```

`cardio-hfpef-dapagliflozin-cost-analysis.txt:210–214` — Lines 210–214: Results confirms the reference answer’s base-case values, drug assignments, and composite endpoint.

```text
The annual drug costs are $4,951.57 for dapagli ﬂozin and
$5,576.06 for sacubitril–valsartan. The CNT to prevent one event of total
worsening HF events and CVD (composite outcome) was $148,547.13
($103,982.99–306,997.39) for dapagli ﬂozin and $245,346.77
($139,401.58–1,734,155.60) for sacubitril–valsartan (Figure 1).
```

### cardiology c016

The genetic finding and the two studies' scoped results are supported. The question, however, asks only why the inverse cluster is not a drug-response result. A complete answer can explain that it is a genetic association without mentioning an SGLT2 advanced-CKD cohort or sulfonylureas. Requiring that unspecified comparison would penalize a correct answer. No source conflict changes the cluster finding; lack of validation is an inference from the articles' different analyses, not a reported test. The supplied text resolves the relevant claims without a PDF check.

**Blocking basis:** Blocking: the required f2 comparison is not elicited by the question, so a correct answer can be scored incorrectly. The question also fails the cross_doc_synthesis admission criterion as written because the polygenic article alone supplies an adequate answer. Both conditions independently meet the packet's blocking rule.

**Proposed correction:** Either name the SGLT2 advanced-CKD cohort in the question and ask for a comparison, or remove the CKD-specific requirement and recategorize the case. Remove the sulfonylurea-response requirement. If retaining the validation language, mark it as an inference.

`cardio-diabetes-hypertension-polygenic.txt:256–262` — Lines 256–262 support the cluster count and the scoped genetic associations in f1.

```text
In the Inverse T2D-BP riskcluster, we noted an inverse relationship
of associated SNVs effects on higher T2D risk related to lower SBP/
DBP/PP. Predominantly originating from associations with BP traits
(Supplementary Fig. 1), the 353 SNVs within this cluster, when aligned
to the T2D risk allele, are associated with a lower risk of cardiovascular
events, such as atrial ﬁbrillation (AF), coronary artery disease (CAD),
stroke and heart failure.
```

`cardio-diabetes-hypertension-polygenic.txt:497–500` — Lines 497–500 show the article's drug-related discussion concerns antihypertensive medications. It does not identify the CKD cohort requested by the key.

```text
These results support
previous research on the heterogeneous effects of hypertensive
medications on the risk of T2D, indicating that some biological pro-
cesses between T2D and high BP may reduce the risk of comorbidity
```

`cardio-diabetes-hypertension-polygenic.txt:685–688` — Lines 685–688 support the environmental caveat as a general limitation, not a drug-response finding.

```text
We acknowledge several caveats in this work. The pathophysio-
logical mechanisms involved in both T2D and high BP are not fully
explained by genetics alone, and are inﬂuenced by a variety of external
and environmental factors, such as salt consumption or western diet.
```

### diabetes d015

The inverse-cluster Results passage alone establishes the requested rejection of a uniformly positive BP-risk axis; the partitioned PGS result corroborates it. The environmental caveat is source-supported but is an additional, unrequested claim made mandatory by f1. Neither supplied anchor needs to be connected with the other to answer the question, so the multi_hop admission criterion fails. A correct answer focused on the inverse association could also lose credit for omitting the caveat. The text resolves the relevant bindings; no extraction gap remains.

**Blocking basis:** Blocking: the case violates the supplied multi_hop admission criterion, which independently triggers the packet's blocking rule. The mandatory environmental clause also permits a correct answer to be scored incorrectly. This conclusion does not depend on hypothetical lenient grading.

**Proposed correction:** Recategorize as direct_lookup and require the inverse association and non-uniform-axis implication. Make the environmental caveat optional, or revise the question to ask for limitations explicitly and score them as a separate fact. Retain the association-versus-causation guard without demanding an unasked-for treatment-effect discussion. Replace the placeholder population and endpoint metadata. Recommend these changes in a new revision; the present gold contract does not stand unchanged.

`cardio-diabetes-hypertension-polygenic.txt:256–258` — Lines 256–258. This local passage answers the question's central implication: the BP association is not uniformly positive.

```text
In the Inverse T2D-BP riskcluster, we noted an inverse relationship
of associated SNVs effects on higher T2D risk related to lower SBP/
DBP/PP.
```

`cardio-diabetes-hypertension-polygenic.txt:485–488` — Lines 485–488. The partitioned PGS result independently supports the inverse direction for the essential-hypertension endpoint.

```text
We detected a reciprocal
protective effect of the Inverse T2D-BP cluster PGS on essential
hypertension (OR[95% CI] = 0.91[0.90 –0.92], p <1 . 0 0×1 0
−40)
```

`cardio-diabetes-hypertension-polygenic.txt:685–688` — Lines 685–688. This supports the gold's environmental caveat, but the question does not request that separate limitation.

```text
We acknowledge several caveats in this work. The pathophysio-
logical mechanisms involved in both T2D and high BP are not fully
explained by genetics alone, and are inﬂuenced by a variety of external
and environmental factors, such as salt consumption or western diet.
```

### diabetes d016

The gold answer is factually supported, but the question asks only whether the HFpEF network meta-analysis found a significant drug-class difference in cardiovascular mortality. One results passage answers no. The required fact additionally demands other endpoints and an indirect-comparison explanation, so a correct answer to the question could be under-credited. The multi_hop label also fails its two-necessary-anchors criterion. The supplied text settles these points; no extraction gap remains.

**Blocking basis:** Blocking: the category violates its admission criterion, which the supplied rule makes blocking even if document-only scoring ignores it. The bundled required fact can also cause a correct, concise answer to be scored incorrectly.

**Proposed correction:** Reclassify as direct_lookup and require only the null HFpEF cardiovascular mortality finding. Treat the other endpoints and indirect design as optional context. Alternatively, ask explicitly about comparison design to retain a two-anchor question. Match the source wording “HF hospitalization/event” if that endpoint remains.

`cardio-cardiorenal-drug-network-meta-analysis.txt:519–521` — Lines 519–521. This single results passage fully answers the question about HFpEF cardiovascular mortality.

```text
In the HFpEF NMA, there were no significant differ -
ences between any of the drug classes for CV mortality, 
all-cause mortality, or HF hospitalization/event.
```

`cardio-cardiorenal-drug-network-meta-analysis.txt:194–197` — Lines 194–197. The design qualifier in the required fact is supported, but the question does not ask how the comparisons were made.

```text
Because all included trials were placebo-
controlled, comparisons between treatment classes were 
derived through indirect evidence using placebo as the 
common comparator.
```

`cardio-cardiorenal-drug-network-meta-analysis.txt:742–746` — Lines 742–746. The discussion confirms the results and limits their interpretation.

```text
In contrast, no significant differences were observed 
between drug classes in the HFpEF population across 
CV mortality, all-cause mortality, or HF outcomes. The 
NMA findings should be interpreted with caution and 
viewed as hypothesis generating rather than definitive.
```

### diabetes d020

The gold correctly describes the main intention-to-treat analysis, but the question does not specify that analysis. The same article explicitly reports statistically significant HbA1c differences at both follow-up visits in a sensitivity analysis. A response identifying that analysis and its six-month −0.8% difference therefore has a defensible reading of the premise. The unqualified required premise rejection cannot stand. No text-extraction issue remains unresolved for these passages.

**Blocking basis:** Blocking: the documented rule applies because a correct, explicitly scoped sensitivity-analysis answer could be scored wrong under the required premise rejection, and the omitted analysis scope makes the question materially ambiguous. This exceeds a non-blocking valid_minor note.

**Proposed correction:** Specify the primary intention-to-treat analysis in the question if premise rejection is intended, and retain the three-month P=.03 versus six-month P=.12 correction. If the question remains unqualified, accept a clearly scoped sensitivity-analysis answer without requiring premise rejection. The population and endpoint metadata should also be made specific.

`diabetes-digital-education-cgm-trial.txt:34–37` — Lines 34–37. The abstract supports the gold values for the intention-to-treat result: the six-month confidence interval crosses zero and P=.12.

```text
Results: HbA1c was lower among the intervention group versus the usual care group at 3 months (difference= −0.7%, 95% CI
−1.4% to −0.1% or difference=−8.1 mmol/mol, 95% CI −15.5 to −0.7 mmol/mol; P=.03) and at 6 months (difference= −0.6%,
95% CI −1.4% to 0.2% or difference= −6.9 mmol/mol, 95% CI −15.7 to 1.9 mmol/mol; P=.12) but only reached statistical
significance at 3 months.
```

`diabetes-digital-education-cgm-trial.txt:393–397` — Lines 393–397. The article explicitly distinguishes the restricted sensitivity analysis from the main analysis.

```text
In addition to the main analysis, we conducted sensitiv-
ity analyses for all primary and secondary outcomes where
we excluded participants (n=9) who were randomized to
the intervention condition but never enrolled in the digital
DSMES+CGM integrated solution (sample size n=42).
```

`diabetes-digital-education-cgm-trial.txt:517–524` — Lines 517–524. The complete alternative passage reports significant HbA1c differences at both visits, including a six-month difference of −0.8%.

```text
A sensitivity analysis excluding participants who never
participated in the intervention showed that participants in
the digital DSMES+CGM condition had significantly lower
HbA1c than those in usual care at both 3 months ( −1%, 95%
CI −1.6% to −0.3% or −10.5 mmol/mol, 95% CI −17.9 to
−3.1 mmol/mol; P=.01) and 6 months (−0.8%, 95% CI −1.6%
to −0.02% or −9.1 mmol/mol, 95% CI −18.0 to −0.2 mmol/
mol; P=.046).
```

### cardiology q058

The source reports diabetes-status interaction P values above 0.05 for ΔGLS, ΔE/e’, ΔLAVI, ΔNT-proBNP, and ΔPIIINP. The required fact instead extends that finding to all three serum biomarkers and HF rehospitalization. The text reports no diabetes-status interaction for GDF-15 or rehospitalization. The authors claim independence from glycemic control, but the reported subgroup tests do not establish independence from glycemic changes or causal mediation. No binding extraction gap remains; the interaction rows are legible.

**Blocking basis:** Blocking under the supplied rule: a correct answer limited to the five reported tests could be scored incomplete, while an incorrect claim of GDF-15 or rehospitalization interaction could satisfy the gold. The defect is in the required fact, not an unresolved table extraction.

**Proposed correction:** Revise the required fact and reference answer to name the five Table 6 outcomes and their interaction P values. Remove HF rehospitalization from the interaction claim and timeframe; say that GDF-15 has no reported interaction result. Attribute glycemic independence to the authors while retaining the evidentiary caveat. Extend the anchor to include the Table 6 interaction rows.

`cardio-heartfailure-biomarkers.txt:442–449` — Lines 442–449: Section 3.8 names five subgroup outcomes and ties its interaction claim to Table 6. The authors interpret the result as glycemic independence.

```text
The beneficial effects of SGL T2i on ΔGLS, ΔE/e‘, ΔLA VI, 
ΔNT-proBNP , and ΔPIIINP we re consis tently observe d in both 
diabetic and non-diabetic subgroups (all P < 0.001 for within- 
subgroup comparisons). No significant intera ction was found 
between SGL T2i trea tment and diabetes s tatus for any outcome 
(all P for intera ction >0.05; Table 6 ), indicat ing that the 
cardiopr otective effects of SGL T2i are independent of 
glycemic contr ol.
```

`cardio-heartfailure-biomarkers.txt:856–860` — Lines 856–860: These are all five reported diabetes-status interaction rows. Their outcome and P-value bindings are readable; neither GDF-15 nor HF rehospitalization appears.

```text
Intera ction ΔGLS 0.119
Intera ction ΔEe 0.554
Intera ction ΔLA VI 0.115
Intera ction ΔNTproBNP 0.554
Intera ction ΔPIIINP 0.594
```

`cardio-heartfailure-biomarkers.txt:317–320` — Lines 317–320: The study distinguishes two diastolic measures, three serum biomarkers, and rehospitalization. Thus the gold phrase “the three biomarkers” includes GDF-15, which has no reported interaction row.

```text
Changes in diastolic function parameters (ΔE/e’, ΔLA VI);
Per centage changes in serum biomarkers (ΔNT-proBNP%, 
ΔPIIINP%, ΔGDF-15%);
Incidence of heart failure re hospitalization.
```

### outliers x004

The requested numerical answer is supported: total ARG relative abundance decreased at 11 of 12 plants, and absolute abundance per millilitre decreased at all 12. But f1 is a required claim and adds that a separate four-setting qPCR-versus-metagenomic study is not the 12-plant result. The question does not request that comparison, and its evidence comes from the named decoy. Thus the complete fact/evidence/category contract requires decoy information and cannot stand unchanged. The supplied text resolves the issue; no extraction gap remains.

**Blocking basis:** Blocking under the supplied rule: cross_doc_distractor requires that the question not require the decoy, yet the rubric requires f1, which includes a claim about the decoy. A correct answer giving only the two requested counts could therefore be scored incomplete. A category admission violation blocks even if a legacy scorer ignores it.

**Proposed correction:** Remove the four-setting comparison clause from f1 and the reference answer, leaving it as distractor context. Then remove f1 from the decoy anchor’s fact_ids. Retain the treatment counts and primary anchor.

`outlier-amr-international-wwtp.txt:19–20` — Lines 19–20: identifies the primary study’s population and treatment comparison.

```text
sequencing to wastewater influent and effluent samples from 12
international WWTPs to classify the behavior of specific ARGs
```

`outlier-amr-international-wwtp.txt:418–424` — Lines 418–424: the detailed results confirm both counts for total ARGs and identify the relative-abundance exception.

```text
the overall relative abundance of the summed
total ARGs (total ARGs) decreased at 11 of 12 WWTPs (p =
0.01 across the data set). Only one WWTP, PHL-1, exhibited
an increase in relative total ARG during treatment. Absolute
abundance (per mL) of total ARGs exhibited a similar trend to
that observed for relative abundance, decreasing at all 12
WWTPs by ∼0.5−3.5 log (Figure 1B).
```

`outlier-amr-method-comparison.txt:48–51` — Lines 47–50: the decoy studies four samples and compares measurement methods.

```text
In this study, we compare metagenomic shotgun sequencing
(TruSeq DNA sequencin g) of wastewater samples with a state-of-the-art PCR-based
method (Resistomap HT-qPCR) on four wastewater samples that were taken from hospital,
industrial, urban and rural areas.
```

### outliers x005

The two accuracy figures are reported, and the MRI CNN’s four-category task is supported. The ANN endpoint is inconsistent across the article: the abstract calls it early-stage risk prediction, while the implementation and detailed results describe binary Alzheimer’s detection without an early-stage endpoint. The question asks for the tasks behind the figures, and the gold requires the abstract’s description. An answer accurately following the detailed results could therefore be marked wrong. The supplied text settles that the descriptions conflict; it does not reconcile them.

**Blocking basis:** The packet’s rule makes material ambiguity blocking when it can cause a correct answer to be scored incorrectly. The conflict concerns the task qualifier expressly requested and required by the gold, so it meets that rule. The unrelated ARG warning is an additional nonblocking rubric error.

**Proposed correction:** Revise the question and gold to acknowledge both descriptions of the ANN task, accepting a properly scoped binary-detection answer alongside the paper’s risk-prediction wording. Replace the unrelated ARG rubric warning with guidance about the distinct datasets and endpoints. Gold remains unchanged in this adjudication.

`outlier-alzheimer-dual-model.txt:22–24` — Lines 22–24: the abstract supplies both accuracies and calls the ANN task early-stage risk prediction.

```text
Results and Discussion:  The ANN achieved an accuracy of 87.08% in early-
stage risk prediction, while the CNN demonstrated a superior 97% accuracy in 
disease staging, supported by Grad-CAM visualizations that improved model 
```

`outlier-alzheimer-dual-model.txt:351–356` — Lines 351–356: the implemented ANN is described as a binary classifier.

```text
The Artificial Neural Network (ANN) model employed a feed-
forward structure with input, hidden, and output layers. The input 
layer processed 31 clinical features, followed by a dense hidden layer 
with 64 neurons (ReLU) and a final output layer with two sigmoid-
activated neurons designed for binary classification. The ANN was 
trained using the Adam optimizer and binary cross-entropy loss, and 
```

`outlier-alzheimer-dual-model.txt:532–537` — Lines 532–537: the detailed ANN results identify the endpoint as Alzheimer’s versus no Alzheimer’s.

```text
Confusion matrix summarizes ANN model performance of a 
binary classification model designed to detect Alzheimer’s disease in 
Figure 10. The matrix outlines the relationship between the true and 
predicted labels. The rows correspond to the actual labels, where “0” 
represents cases without Alzheimer’s and “1” represents cases with 
Alzheimer’s.
```

## Agreement and audit trail

All 33 final results are recorded individually, with verdict, severity, scoring impact, standards checks and source evidence. Note-only disagreements were reviewed too. The machine-readable findings retain each historical verdict/severity for comparison.

Every required final session has an accepted result. Source quotations were checked against the pinned `.txt` files. Whitespace-only formatting was recovered deterministically where needed; words and punctuation were never repaired. Raw replies/transcripts and adjustment records preserve what the model returned. Substantive quote mismatches were rejected.

The corpus-growth hunt remains the historical search across all 55 articles: zero H1/H2/H3/H4/H6 findings, 67 informational H5 candidates. This means no counter-evidence was found by that search; it does not prove corpus-wide absence. Final reviewers received declared sources, alternatives, named decoys and relevant candidates; absent-fact cases received the entire 55-article text corpus.

## Models, verification and limits

Accepted final sessions used GPT-6 Sol with low effort for 17 cases and GPT-6 Luna with low effort for 16 cases, honoring Juan’s Plus usage budget. The installed CLI rejected historical `gpt-6.1-sol`; the failed launch is preserved. An Astra high-effort attempt was stopped after the budget clarification and contributes no accepted verdict. Actual model, token usage and attempts are recorded per case; no API-price estimate is presented as subscription consumption.

- 206 repository offline tests passed; no retrieval or paid rewriting/generation runs were launched.
- Frozen query, standards, prompt, schema, packet and text hashes verified unchanged.
- Per-session tool commands, source scope, result/transcript hashes and citations are recorded in [final verification](results/final_verification.json).
- The eight completed Kimi results are preserved as a partial experimental blind pass, not whole-suite coverage. The Kimi pass was not continued.
- Model review is not clinical expert review. Flattened extraction may obscure table bindings; unresolved extraction would remain a gap, never be resolved by opening a PDF.
- Codex leads adjudication but also authored much of the gold; targeted second opinions do not eliminate correlated model-family errors.

## Files and next step

- [Final plan](FINAL_PLAN.md) and [frozen manifest](final_review_manifest.json).
- [Historical report](REPORT.pre-codex-final.md) and unchanged [historical findings](results/full_findings.json).
- [Final findings](results/final_findings.json), `results/review6/`, `results/final_codex/` and `results/stage1_kimi/`.
- Briefs, schemas, packet builder, runner, format-only acceptance helper and aggregation script make selection and evidence checks reviewable. Raw transcripts/workspaces remain outside Git.

After Juan reviews this findings-only PR, apply accepted corrections in a separate task: increase revisions, retain old results, update the affected gold/evidence/category metadata, and rerun only affected benchmark conditions when the changed scoring contract requires it. This PR is not merged by agents.
