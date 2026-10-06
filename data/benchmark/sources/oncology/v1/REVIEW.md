# Claude review assessment and pre-freeze corrections

Claude independently reviewed initial PR commit `8b1adbe` and recommended against
freezing. The author checked its findings against the pinned papers and standards.
The initial draft remains recoverable from Git; corrections are recorded in
[revision_ledger.json](revision_ledger.json). No retrieval output informed them.

| Concern | Assessment and action |
| --- | --- |
| F1: Hunan OS | Confirmed omission, with a qualification: the paper itself calls OS immature in its discussion of further prognostic analysis. Gold now includes significant unweighted and weighted two-year OS comparisons as well as that limitation. Neither “no reported benefit” nor a mature causal survival claim is acceptable. Corrected o029 and o030 replace the old study-specific tasks. |
| F2: observational HR scope | Confirmed. o009/o017 now distinguish twelve studies overall from four contributing to the HR. Added an exact limitations anchor and retained the difference between event prevalence and comparator-relative hazard; attributed comparative Results wording is accepted. |
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
| D1: Hunan OS label | Confirmed. The Results call the p=0.038 OS comparison a "weighted population", but the Figure 1D legend labels it "after PSM", and the Methods describe PSM only. o029 requires the attributed conflict and anchors the Figure 1D legend. The Limitations statement replaces the Discussion caveat as the OS-maturity anchor. o030 accepts either attributed label. Its primary set needed seven chunks; adding the legend needed nine, exceeding n=8. o029 tests the conflict. |
| D2: Helsinki five-year OS | Confirmed. o021 adds the follow-up anchor and corrects both halves of the premise. The study is retrospective and nonmatched, and its survival endpoint is EFS by pCR within each cohort, with median follow-up of 22 and 35 months. A full-text search found no OS result for either cohort. |
| D3: near-duplicates and POL-MOL role | Confirmed. q082 (same anchor and facts as o025) and o019 (a strict subset of o023) are withdrawn. POL-MOL is partial support in o023/o030 and a named decoy nowhere in this release. It mentions faster time to optimal treatment, but not MDT agreement or deterioration/suboptimal therapy before complete biomarker status. Roles are question-specific; an article may answer another question and distract this one. |
| D4: weak MRD decoy | Confirmed. o025's decoy is now the ctDNA-MRD-guided adjuvant trial row in the driver review's Table 2. It is in the same field but reports no assay performance. Stale overlap records are rebuilt from dependencies. The o024 afatinib decoy is kept as weak but valid. |
| D5: search provenance | Each article records `search_query_type`: legacy manifest, topical search or targeted lookup. The third-review pass corrects misattributed terms: Marjanski, 4.602 and 21.5/37.9 came from legacy reference gold, not the selected articles. Unpreserved discovery queries remain explicitly unpreserved; the -BioRender filter is disclosed. |
| D6 and ID semantics | REPORT counts and the stale o025 sentence are corrected; the offline suite result is recorded there. The ledger notes the retained IDs whose task changed: q081, q095 and q108. Retired negatives q091, q109 and q115 no longer link unrelated replacement cases. |
| V1–V3: verifier gaps | Attribution, query-role, migration and ledger checks are now separate functions with tests. New checks cover overlap and negative-context anchor resolution, decoy/partial-support conflicts, overlap-review completeness, correction anchors, revised-question and answerability drift, renamed/withdrawn ledger consistency, and oracle case coverage. Run against a226bba, the new checks reject o019 and o025. |

## Decision record and restored legacy cases

Writing [DECISIONS.md](DECISIONS.md) showed that o009 and o023 needed two separated passages, so they are now multi-hop. It also showed that four legacy cases on retained sources had been retired without a reason. The original author confirmed that no reason was recorded, so q078, q097, q098 and q099 are restored as revised cases with pinned evidence. q098 is reframed to the paper's design: Black and Hispanic women are each compared with White women.

At b626fbb the draft had 44 cases, 49 anchors and 14 selected articles. Offline reachability
and release checks have been refreshed. These remain structural checks, not measured
retrieval quality. This records the pre-freeze review stage. Subsequent model review and corrected
gold are preserved in the current combined benchmark; historical topic evaluation
and regressions are recorded in [EVALUATION.md](EVALUATION.md).

## Third review of b626fbb and Codex correction pass

Codex independently checked the supplied third-review findings against the pinned
texts and verifier. The corrections below are author verification; the changed
gold and alternatives still require independent re-review before freeze.

| Finding | Correction |
| --- | --- |
| H1: q098 | Results 2a and Table 4 give Black versus White women aOR 0.77 (0.64–0.92), significantly lower cervical-only versus dual odds, alongside Hispanic aOR 1.39 (1.10–1.77), higher odds. Removed the false no-estimate qualifier and cross-contrast ordering inference. Extended the 2a anchor and pinned Table 4 as the complete primary evidence. |
| M1: o001/o002 | o001 requires the response-versus-nonsignificant-DFS correction. The narrative/table count conflict is optional there and required only in o002. Their complete gold answers are no longer subsets. |
| M2: alternatives | Reviewed all 41 evidence cases for same-source restatements and question-scoped competition. Twenty cases have complete alternatives, recorded per case. q096 accepts the explicitly stated fivefold ratio without requiring its supporting percentages. q098 and o027 become direct lookups because one local table/Results paragraph supplies their complete gold. |
| M3: integrity | Verifier checks oracle minimums, labels, lists, counts, rates and chunker hash, then recomputes both oracles; compares DECISIONS with its renderer; checks migration categories/self-links, ledger hash/category history and restoration/link events; validates anchor roles/fact bindings and positive false-premise correction anchors. Thirteen additional regression tests cover these failures and permit legitimate roles across different questions. |
| L1/L2: stale descriptions | o029 rubric reflects OS-label conflict and maturity. Seven chunks for o030, nine if the legend were required, replaces the eight-chunk claim. |
| L3: migration | Removed topic-only q089/q093/q094/q106/q118/q119 links and q116→o012. q086/q087 link to o007 only for review-attributed trial-result reasoning, explicitly without equivalent clinical coverage. Removed the corresponding q118/q119 renamed-coverage claims. |
| L4/L5: provenance/denominators | Lookup notes identify legacy-gold terms and the exclusion filter. q097/q098 permit either source-attributed 40,511 or Table 4 N=42,701 as an optional count; q097 identifies the binary income contrast. |
| L6/L7: wording/bookkeeping | Backfilled q099's restoration category transition, recorded q078's added NCCN task, accepted clinician/woman synonyms, and described o024's 12-point difference as derived from reported rates. |
| L8–L11: clarity | POL-MOL's time-to-treatment statement is acknowledged; truncated spans were re-pinned; generic contradiction rules were simplified; candidate covered_by fields explicitly identify post-hoc title-only hypotheses and unassessed competition. No new candidate was selected on that basis. |

The corrected release retains 14 articles and 44 cases, with 84 anchors. All 206
offline tests pass (55 verifier tests); release verification passes. All 41
evidence cases are feasible at n=8 and 33 at n=3. No retrieval, ingestion or paid
evaluation occurred. Alternative evidence remains conservative pinned coverage,
not exhaustive semantic equivalence or clinical peer review.
