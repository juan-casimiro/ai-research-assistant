# Benchmark gold validation report — JUA-106

**150 of 158 benchmark cases stand as written; 8 need a correction, 2 of them
blocking.** No article outside a case's declared sources answers, contradicts
or undermines any case, so the keys hold as the corpus grows from C1 to C3.

Run on 2026-10-03 and 2026-10-04 following [PLAN.md](PLAN.md). This is model
review of the extracted article text. It did not open the PDFs, run retrieval
or judge generated answers, and it is not clinical expert review. No gold,
anchor, source or run artifact was changed.

## Verdicts

| Set | Cases | Valid | Valid, minor note | Needs correction |
| --- | --- | --- | --- | --- |
| cardiology | 45 | 33 | 8 | 4 |
| diabetes | 49 | 33 | 14 | 2 |
| oncology | 44 | 33 | 11 | 0 |
| outliers | 10 | 6 | 4 | 0 |
| ALS/FTD (prepared) | 10 | 4 | 4 | 2 |
| **Total** | **158** | **109** | **41** | **8** |

| Category | Cases | Valid | Valid, minor note | Needs correction |
| --- | --- | --- | --- | --- |
| direct lookup | 64 | 52 | 11 | 1 |
| multi-hop | 32 | 18 | 9 | 5 |
| cross-document synthesis | 18 | 11 | 5 | 2 |
| cross-document distractor | 15 | 9 | 6 | 0 |
| false premise | 18 | 14 | 4 | 0 |
| unanswerable | 11 | 5 | 6 | 0 |

A minor note is an annotation or wording issue that does not change scoring.
All 41 are listed with their proposed clean-up in
[results/full_findings.json](results/full_findings.json).

## Cases needing correction

Each was adjudicated by Claude Opus against the article text. Quotes are
verbatim from the extracted text, including its spacing artefacts.

| Case | Category | Verdict | Blocking |
| --- | --- | --- | --- |
| cardiology q058 | direct lookup | `defect_gold` | yes |
| cardiology c016 | synthesis | `ambiguous_question` | yes |
| cardiology c012 | synthesis | `defect_gold` | no |
| cardiology c013 | multi-hop | `alternative_missing` | no |
| diabetes d015 | multi-hop | `defect_category` | no |
| diabetes d016 | multi-hop | `defect_category` | no |
| ALS/FTD a001 | multi-hop | `defect_category` | no |
| ALS/FTD a007 | multi-hop | `defect_category` | no |

**cardiology q058 — wrong outcome list.** The gold says diabetes-status
interaction P values exceeded 0.05 for GLS, "the three biomarkers" and HF
rehospitalization. Table 6 in `cardio-heartfailure-biomarkers.txt` has five
interaction rows and neither GDF-15 nor rehospitalization: "Intera ction ΔGLS
0.119 Intera ction ΔEe 0.554 Intera ction ΔLA VI 0.115 Intera ction ΔNTproBNP
0.554 Intera ction ΔPIIINP 0.594". A system listing the five reported outcomes
would be scored wrong. Correction: rewrite the fact and reference answer to
match Table 6.

**cardiology c016 — question does not require the second paper.** The
polygenic article alone answers the cardiometabolic question as asked; the
question never points to the SGLT2 advanced-CKD cohort the gold requires as a
second source. Correction: either name that cohort in the question, or recast
the case as a single-document case on the polygenic article.

**cardiology c012 — source conflict not exposed.** The gold uses the narrative
values (ESRD/dialysis aHR 0.35, CI 0.19–0.67; GUTI aHR 1.78, CI 1.12–2.84).
Table 2 of `cardio-ckd-sglt2-acei-arb.txt` prints 0.19–0.66 and 1.80
(1.13–2.86). The standards require conflicting source values to be shown, not
reconciled. Correction: state both sets and accept either.

**cardiology c013 — undeclared evidence set.** The abstract of
`cardio-hfpef-dapagliflozin-cost-analysis.txt` carries both required facts
("Costs were based on 2022 US prices" and "The corresponding CNTs were
$148,547.13"), so it is a complete alternative to the declared anchors.
Correction: add the abstract as an alternative evidence set; consider
relabelling, since one passage answers it.

**diabetes d015, d016; ALS/FTD a001, a007 — not multi-hop.** In each, the
content is accurate but one passage answers the question: adjacent sentences
(a001), one contiguous case-presentation passage (a007), the inverse-cluster
passage alone (d015), and a single results sentence (d016). d016 also requires
an indirect-evidence qualifier the question does not ask for, so a correct
plain answer could lose credit. Correction: relabel as direct lookup, or reword
the question so the second anchor is needed.

Adjudication also examined 13 other escalated cases and upheld the gold in all
of them, including every case escalated because the blind answer disagreed.

## Stability as the corpus grows

For every case, Codex searched the articles outside its declared sources,
across all 55 articles, for anything that would break it.

| Finding type | Count |
| --- | --- |
| Undeclared alternative in another article (H1) | 0 |
| Conflicting value for the same scope (H2) | 0 |
| Absent fact present somewhere (H3) | 0 |
| False premise true elsewhere (H4) | 0 |
| Named decoy actually answers (H6) | 0 |
| Possible undeclared competitor (H5, informational) | 67, of which 3 rated probable |

All 158 cases are recorded stable across C1, C2, C3 and the four ALS/FTD
articles. The three probable competitors are for diabetes d018 and oncology
o010 and o015. "Stable" means no counter-evidence was found with the recorded
search terms; absence cannot be proven.

## How far the reviewers can be trusted

| Check | Result |
| --- | --- |
| Stage 0 mechanical checks | 143 pass, 15 warn, 0 fail; all 247 anchors match the text and recorded hashes |
| Blind answers against gold, 196 required facts | 160 match, 31 partial, 2 not addressed, 3 contradicted |
| Blind answerability against gold | agrees in 154 of 158 cases |
| Second blind answer by Codex, 15 cases | same answerability as the first in 14 |
| Quoted passages found in the named article | 871 of 882 |
| Seeded defects in the pilot, auditor | 7 of 7 caught |
| Seeded defects in the pilot, hunter | 3 of 3 caught |
| Coverage gaps | none; every case has a result from every stage |

The seeded defects were obvious and five of eight were in cardiology, so the
detection rate shows the reviewers work, not that they would catch subtle
errors.

## What this says about the benchmark design

- **Multi-hop and synthesis labels are the weak point.** Seven of the eight
  corrections fall in these two categories, and five are cases one passage or
  one paper answers. Per-category scores for them are slightly inflated until
  the cases are relabelled.
- **The distractor category tests little.** There are 15 cases; the hunt rated
  three unnamed passages as probably more confusable than the named decoys, and
  one named decoy (ALS/FTD a009) was judged a weak competitor.
- **Some reference answers put caveats in required facts.** Adjudication noted
  this for o009, q037, d004, o011 and d016. Retrieval scoring is unaffected,
  but an answer judge would mark down a correct plain answer.
- **Absent fact and false premise blur in practice.** Blind answerers often
  called an absent fact a wrong premise. Refusal scoring should accept either
  for the 11 unanswerable cases.

## Roles, models and cost

| Stage | Runner | Batches | Use |
| --- | --- | --- | --- |
| Blind answer | Claude Sonnet 5.5 | 29 | $8.08 |
| Gold audit | Claude Sonnet 5.5 | 29 | $7.39 |
| Corpus-growth hunt | Codex `gpt-6.1-sol`, medium effort | 23 | 10.7M input tokens (9.1M cached), 101k output |
| Second blind answer | Codex `gpt-6.1-sol`, medium effort | 6 | 0.76M input tokens (0.56M cached), 18k output |
| Compare | Claude Sonnet 5.5 | 16 | $1.67 |
| Adjudication | Claude Opus 5.5 | 21 cases | $5.07 |

Claude figures are list-price equivalents reported by the CLI for accepted
batches. The pilot cost about $4.30 on Claude and 1.73M Codex input tokens.

## Deviations from the plan

- **Blind answerer.** Kimi K3 was planned but returned a 5-hour usage-limit
  error after two pilot batches (five questions). Claude Sonnet answered the
  rest of the pilot and the whole full run.
- **Escalation rules narrowed after the pilot.** The first rules sent 9 of 12
  pilot cases to adjudication and none was a defect. The full run escalates on
  a blind ambiguity only when it changes the answer, treats "premise wrong" and
  "not in the articles" as agreeing for unanswerable cases, and records
  `valid_minor` without adjudication.
- **Hunt brief changed mid-stage.** A line telling the hunter to use only the
  `.txt` files was added after 14 of 23 hunt batches had finished. The
  workspace held only text files throughout, and no Codex transcript shows PDF
  access.
- **Interrupted run.** The machine slept twice during the full run and Codex
  credit ran out once. Accepted batches were kept and only missing ones were
  rerun; no batch was rerun after it had succeeded.
- **Pilot cases rerun.** The 12 pilot cases were reviewed again inside their
  full-run batches so that every case has the same runners and briefs.

## Limits

- Model review, not clinical expert review.
- Text only. No case was left as `needs_pdf_check`, but table bindings were
  judged from flattened text.
- The auditor and adjudicator are Claude models; four oncology cases were
  authored by Claude and two sets had an earlier Claude review.
- Retrieval repeatability and generated-answer stability were out of scope.

## Files

| File | Content |
| --- | --- |
| [results/full_findings.json](results/full_findings.json) | One record per case: every stage's result, the final verdict and proposed correction |
| [results/pilot_findings.json](results/pilot_findings.json) | Pilot findings and seeded-defect detection |
| `results/<group>/` | Accepted reply for each batch, with runner, attempts, quote verification and token usage |
| [manifest.json](manifest.json) | Case-to-batch assignment, runners, hashes of query files, briefs and schemas |
| `briefs/`, `schemas/` | Prompts and output schemas for each stage |

Raw transcripts, the review workspaces and the seeded-defect records are kept
outside the repository and are not part of this record.

## Next step

Corrections are a separate task. Under the [standards](../../STANDARDS.md) each
is a recorded revision with matching reruns of the affected conditions, and the
original result is preserved.
