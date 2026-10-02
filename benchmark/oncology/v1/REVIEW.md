# Claude review assessment and pre-freeze corrections

Claude independently reviewed initial PR commit `8b1adbe` and recommended against
freezing. The author checked its findings against the pinned papers and standards.
The initial draft remains recoverable from Git; corrections are recorded in
[revision_ledger.json](revision_ledger.json). No retrieval output informed them.

| Concern | Assessment and action |
| --- | --- |
| F1: Hunan OS | Confirmed omission, with a qualification: the paper itself calls OS immature in its discussion of further prognostic analysis. Gold now includes significant unweighted and weighted two-year OS comparisons as well as that limitation. Neither “no reported benefit” nor a mature causal survival claim is acceptable. Corrected o029 and o030 replace the old study-specific tasks. |
| F2: observational HR scope | Confirmed. o009/o017 now distinguish twelve studies overall from four contributing to the HR. Added an exact limitations anchor and retained the difference between noncomparative event prevalence and comparator-relative hazard. |
| F3: POL-MOL overlap | Confirmed. Its Discussion defines pathologist-led reflex testing and potential implementation benefits. The new anchor and case-specific overlap assessments record that partial support. o023/o019/o030 (o019 since withdrawn) explicitly require the Gosney consensus details, including MDT agreement and no formal oncologist request; POL-MOL does not complete those details. Its decoy rationale no longer claims it lacks a reflex definition. |
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

## Re-review of a226bba

Claude re-reviewed the corrected draft and still recommended against freezing. All
confirmed findings are addressed below; [revision_ledger.json](revision_ledger.json)
records the revision. No retrieval output informed these changes.

| Finding | Action |
| --- | --- |
| D1: Hunan OS label | Confirmed. The Results call the p=0.038 OS comparison a "weighted population", but the Figure 1D legend labels it "after PSM", and the Methods describe PSM only. o029 now requires the attributed conflict and anchors the Figure 1D legend. The Limitations statement (follow-up too short for OS as primary endpoint) replaces the Discussion caveat as the OS-maturity anchor. o030 states the same OS facts and accepts either attributed label. It does not require the legend span, because o030 was already at the eight-chunk ceiling and o029 tests the conflict. |
| D2: Helsinki five-year OS | Confirmed. o021 adds the follow-up anchor and corrects both halves of the premise. The study is retrospective and nonmatched, and its survival endpoint is EFS by pCR within each cohort, with median follow-up of 22 and 35 months. A full-text search found no OS result for either cohort. |
| D3: near-duplicates and POL-MOL role | Confirmed. q082 (same anchor and facts as o025) and o019 (a strict subset of o023) are withdrawn. POL-MOL is now partial support in every case and is never a decoy. Its assessment notes that it implies no oncologist request but omits the MDT agreement and the delay mechanism. o023 forbids attributing those details to POL-MOL. |
| D4: weak MRD decoy | Confirmed. o025's decoy is now the ctDNA-MRD-guided adjuvant trial row in the driver review's Table 2. It is in the same field but reports no assay performance. Stale overlap records are rebuilt from dependencies. The o024 afatinib decoy is kept as weak but valid. |
| D5: search provenance | Confirmed. Each article now records `search_query_type`: legacy manifest, topical search or targeted lookup. Its note names any publication-specific terms and shared results. Original topical queries that were not preserved are stated as such and not reconstructed. |
| D6 and ID semantics | REPORT counts and the stale o025 sentence are corrected; the offline suite result is recorded there. The ledger notes the retained IDs whose task changed: q081, q095 and q108. Retired negatives q091, q109 and q115 no longer link unrelated replacement cases. |
| V1–V3: verifier gaps | Attribution, query-role, migration and ledger checks are now separate functions with tests. New checks cover overlap and negative-context anchor resolution, decoy/partial-support conflicts, overlap-review completeness, correction anchors, revised-question and answerability drift, renamed/withdrawn ledger consistency, and oracle case coverage. Run against a226bba, the new checks reject o019 and o025. |

## Decision record and restored legacy cases

Writing [DECISIONS.md](DECISIONS.md) showed that o009 and o023 needed two separated passages, so they are now multi-hop. It also showed that four legacy cases on retained sources had been retired without a reason. The original author confirmed that no reason was recorded, so q078, q097, q098 and q099 are restored as revised cases with pinned evidence. q098 is reframed to the paper's design: Black and Hispanic women are each compared with White women.

The draft now has 44 cases, 49 anchors and 14 selected articles. Offline reachability
and release checks have been refreshed. These remain structural checks, not measured
retrieval quality. Changed gold still needs independent re-review before freeze;
oncology evaluation and topic regressions remain outstanding.
