# Combined-corpus scope and pre-run evidence review

The comparison is frozen before integrated retrieval. It contains the four
finalized topic releases: 51 unique articles, 148 cases (45 cardiology, 49 diabetes,
44 oncology, 10 outliers). The four prepared ALS/FTD articles and ten unfrozen
cases are excluded. Their independent review/freeze is a tracked extension, not
a completed part of this comparison. This is the original four-topic scope of
the combined evaluation; it is not the complete local 55-article inventory.

## Source and query boundaries

Every common source retains its article/version/PDF/text tuple. The union
contains 50 CC BY 4.0 articles and one CC0 article. Article eligibility,
third-party checks and acquisition receipts are inherited from the reviewed
manifests. Attribution remains in the four original inventories. No corpus PDF
or complete text is published. The envelopes retain all original query objects
and anchors. Diabetes uses the explicitly preserved final evaluated release,
before later descriptive annotations; this choice makes the original baseline
exactly reproducible. Its current questions, facts, anchors and evidence bindings
are unchanged. Source/distractor roles remain query-specific.

The current scorer and retrieval fingerprints match the saved baselines.
Re-envelope derivation checks complete coverage, identical per-query hashes,
pinned source tuples, feasibility, every returned production chunk, and
recomputed metrics before accepting a historical parent. Derived artifacts
retain the original run timestamp, commit and provenance and make zero retrieval
calls. A fresh combined store is required; no historical result is relabelled as
a fresh execution. Final nested comparisons must also match retrieval/model
fingerprints and use the existing compatibility validator.

## Integrated evidence validity checks

Codex reviewed all 148 questions against their scoped source/evidence dependency
maps and inspected candidate cross-topic full-text passages before retrieval.
The original topic authors' full-text/alternative reviews remain the foundation;
this is an integration review, not independent clinical certification or an
exhaustive semantic search of every possible paraphrase.

The dominant queries explicitly name an author, cohort, paper or review. Adding
a paper about the same treatment, prediction method or endpoint does not supply
another author's population-specific values. Important competition families are
HFpEF/SGLT2/CKD versus oncology cardiovascular adverse events; sleep/cardiometabolic
risk versus cardiac mortality; genetic susceptibility versus TB Mendelian
randomization; CGM counseling AI versus Alzheimer ANN/MRI; and zinc/HIF renal
mechanisms versus TB immune metabolism and environmental zinc resistance.
The frozen evidence sets are retained. No added cross-topic complete alternative
or newly answerable scoped fact was identified in this review; no gold is tuned
using combined retrieval outputs. Unlisted semantically sufficient passages
remain a limitation of literal-span scoring and require a separately versioned
source-based review rather than post-run anchor relaxation.

A case-specific complete-text term scan covered all 51 main-PDF extractions for
named original cohorts/authors and negative-outcome terms: Djoumessi/Cameroon,
TAILORED-AF, Gao/1884303, SIZE-DM, Berthoumieux, Lebedeva/zinc/HIF-1,
EarlyCDT/FDA, Basque/FIT, Hunan, GQD/Gegen Qinlian and wastewater/patient linkage.
Candidate passages and their scope were inspected. No-match scans are candidate
filters, not proof of absence. Existing source methods/results/limitations
reviews establish the named study scope.

| Cases | Integration decision |
| --- | --- |
| c020 | Buea's Cameroon metabolic-syndrome survey and the TB review's Cameroon adverse-event citation are different studies; neither supplies five-year mortality in the four-week spironolactone randomized cohort. |
| c021 | No addition reports five-year single-procedure freedom from AF in TAILORED-AF. The existing primary/review report 12-month endpoints. |
| c022 | Additional cardiac mortality/risk sources use different populations and endpoints; none externally validates Gao's original one-year nomogram at ten years for hard MACE. |
| q007 | The question explicitly asks what the selected GQD review main PDF reports; other papers' metformin brands do not fill missing per-trial brands there. |
| d022, d023 | Oncology five-year OS and other glycemic studies are not five-year SIZE-DM cardiovascular mortality or twelve-month outcomes of the original Berthoumieux cohort. |
| d024 | TB succinate/HIF-1 inflammatory metabolism, WWTP metal resistance and CT-FFR's zinc/AGE citation supply no Lebedeva stage-3 DKD clinical formulation/dose/duration recommendation. |
| o020 | GQD's Hunan journal citation is unrelated to the Hunan NSCLC surgical cohort's excluded patients. The cohort itself states missing excluded-patient data. |
| q083, q100 | EarlyCDT remains in the original liquid-biopsy source; no addition supplies FDA-validated sensitivity or a Basque-programme dual-screening rate. The question's selected oncology corpus remains its original frozen selection. |
| x009 | The question explicitly limits the evidence search to the five selected outliers. No downstream infection count is inferred from ARG measurements, clinical-risk prose or unrelated cardiac/oncology patients. It is not an assertion of universal absence in 51 articles. |
| false-premise cases | Source-supported corrections retain population/design/task/timeframe qualifications. TB probiotic trials do not turn Yuan's MR into an administered intervention; related AI studies do not independently validate the Alzheimer models or establish TB-care superiority. Other randomized or observational cohorts do not change the named papers' design. |

The salient accidental matches were inspected: Hunan in the GQD bibliography;
Cameroon in a TB adverse-event bibliography; HIF-1 in TB inflammatory metabolism;
zinc in WWTP resistance scaffolds and the CT-FFR bibliography; Oasis HLB
extraction cartridges versus OASIS-3 Alzheimer validation. These are scope
mismatches, not alternative complete evidence.

## Execution scope and limits

Complete final coverage justifies one vector-only integrated execution of all
148 frozen IDs at n=3 and n=8: 296 local retrieval calls. The affected set is the
entire release because the corpus expands across topics and the deliverable
makes whole-benchmark comparisons. There is no iterative global tuning or
configuration sweep. Every requested ID must execute; subset results may not be
reported as full coverage. The 18-case historical regression sample is retained
as a labelled slice of the complete results, not rerun separately.

BM25, rewriting, answer generation and judging are omitted from this corpus-only
baseline comparison. No paid provider calls occur. Answer/refusal correctness
has zero judged cases and no accuracy estimate; correction-evidence retrieval
is reported separately. The pending answer-judge work retains its sequencing.
The prepared ALS/FTD extension, independent domain review, configuration
comparisons and semantic evidence adjudication remain explicit limitations.
