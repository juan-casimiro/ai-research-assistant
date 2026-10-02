# Claude review assessment and pre-freeze corrections

Claude independently reviewed initial PR commit `8b1adbe` and recommended against
freezing. The author checked its findings against the pinned papers and standards.
The initial draft remains recoverable from Git; corrections are recorded in
[revision_ledger.json](revision_ledger.json). No retrieval output informed them.

| Concern | Assessment and action |
| --- | --- |
| F1: Hunan OS | Confirmed omission, with a qualification: the paper itself calls OS immature in its discussion of further prognostic analysis. Gold now includes significant unweighted and weighted two-year OS comparisons as well as that limitation. Neither “no reported benefit” nor a mature causal survival claim is acceptable. Corrected o029 and o030 replace the old study-specific tasks. |
| F2: observational HR scope | Confirmed. o009/o017 now distinguish twelve studies overall from four contributing to the HR. Added an exact limitations anchor and retained the difference between noncomparative event prevalence and comparator-relative hazard. |
| F3: POL-MOL overlap | Confirmed. Its Discussion defines pathologist-led reflex testing and potential implementation benefits. The new anchor and case-specific overlap assessments record that partial support. o023/o019/o030 explicitly require the Gosney consensus details, including MDT agreement and no formal oncologist request; POL-MOL does not complete those details. Its decoy rationale no longer claims it lacks a reflex definition. |
| F4: legacy IDs and negatives | Confirmed. Nine changed study-specific tasks receive o022–o030 instead of reusing their old IDs. Coverage links preserve traceability without claiming equivalent gold. q083/q100 are restored as scoped absent regulatory/geographic facts; q101 positively corrects target-versus-achieved-rate attribution. Retired negatives on ineligible sources record the old answerability distinction and why they are not recast onto another study. |
| F5: stage III ambiguity | Confirmed. o001/o002 name Zhongshan; o001 explicitly preserves the narrative/table MPR conflict instead of presenting one value as uncontested. The existing narrative anchor also captures its reported RR for review. |
| F6: false premise versus absence | Confirmed. o021 now positively corrects the randomized-design premise using the retrospective, nonmatched-cohort anchor. o020 records the explicit missing-data passage and why other-study failure percentages or unresectability after receiving surgery do not supply the excluded-patient denominator. |
| F7: decoy wording and relevance | Confirmed. Questions no longer name competing documents merely to pull them into retrieval. The MRD case o025 uses early-stage treatment-selection biomarker evidence as its competing purpose, replacing the weak ICD decoy. |
| F8: metadata schema and rubric specificity | Added licence ID/version and attribution IDs; contradiction and rubric rules now name the fact’s population and endpoint. Added private insurance as the Medicaid comparison. Recorded discovery-search context: exploratory queries can contain legacy numbers/names and return multiple candidates; this is not a post-retrieval selection strategy. |

The proposed downgrade of o016 solely because its spans are on the same page is
not supported by the production chunker: complete evidence requires **four**
chunks. Its reasoning joins distinct cellular-stress and extracellular-DAMP
mechanisms. It remains a multi-hop case with that rationale and declared budget.

Likewise, resemblance to BioRender artwork without a credit is not evidence of an
incompatible licence. The pinned ICD article's notice/caption/credit inventory
contains no identified specific exclusion. The earlier deferrals were based on
actual BioRender credits. This review question does not establish a new blocker.

## Verifier improvements

Ten committed tests exercise archived bibliographic/rights changes, removed
figure credits, converter mismatch, altered dependency content and stale auxiliary
or oracle linkage. The verifier now reconstructs metadata from archived XML,
PubMed and converter responses, checks figure/table inventories and per-article
attribution entries, validates migration actions/targets/revisions/legacy wording,
and includes alternative evidence in the C1 union. Preserved evaluation-result
hashes supplement the original manifest/golden hashes. PDF parser failures are
reported as controlled verification errors.

Raw duplicate PDFs and deferred candidates have been moved into the ignored
`acquisition/` subdirectory. Top-level corpus PDF membership must match the selected
manifest. This is an ingestion boundary; archives are not additional corpus sources.

The draft now has 42 cases, 42 anchors and 14 selected articles. Offline reachability
and release checks have been refreshed. These remain structural checks, not measured
retrieval quality. Changed gold still needs independent re-review before freeze;
oncology evaluation and topic regressions remain outstanding.
