# Corpus and benchmark standards — v1

Status: shared corpus selection, query authoring and evaluation contract.
The selected corpora and versioned scorer implement this design. This contract
does not certify the legacy benchmark or biomedical correctness.

## Evaluation objective and fair authoring

The objective is to understand system performance across meaningful case types
and a larger corpus. Historical scores are context, not targets to reproduce.
Before authoring, read the selected cardiology full texts and the related or
competing articles relevant to each proposed query. Understand their populations,
methods, endpoints, estimates and limitations; abstracts alone are insufficient.
Design self-contained questions and expected answers from that evidence,
including plausible competing evidence and acceptable alternative answers.
Select cases for coverage and realistic difficulty, not desired flag outcomes.

Freeze reviewed questions, expected answers, evidence and scoring rules before
running experiments. Then compare BM25 and query rewriting on/off under the
same benchmark and declared nested corpus conditions, with explicit approval
for paid runs. Focused subsets support iteration; a final four-configuration
comparison needs complete declared coverage, not automatic repeated sweeps.
Report improvements, regressions and unchanged results equally. Never rewrite
questions or expectations to favour a configuration after seeing its scores.
A genuine source or benchmark defect may be corrected with a recorded revision
and matching reruns; preserve the original result and explain the correction.

## Scope and selection rubric

| Topic membership | Evidence relationships to seek | Planned scope |
| --- | --- | --- |
| cardiology | AF detection/stroke, CCTA/MACE, HFpEF/SGLT2, resistant hypertension, STEMI/no-reflow; same score with different endpoints, primary/secondary endpoints, overall/subgroup estimates | Approximately 20 closely related articles, selected in the article selection audit |
| diabetes | Glycaemic treatment, drug response, genetic risk and cardiovascular outcomes | Size decided after the diabetes audit audit |
| oncology | Detection, biomarkers, precision treatment and clinical outcomes | Size decided after the oncology audit audit; actual topic overrides misleading filenames |
| other topics | AMR/environment, microbiome/TB, cognition/AI diagnosis if retained; expand distinct topics after audit | Size decided in the outlier audit |

Topic membership is an article-level, possibly multi-valued classification with
an explicit rationale. Filenames and legacy `cluster` values are hints only.
Diabetes/cardiovascular outcomes can belong to both diabetes and cardiology.
Cognition/vascular comorbidity can overlap cardiology even in an `outlier-*` file.
An outlier designation is relative to an experiment's target topic, recorded
separately from article topics. A substantially different topic can still offer
valid alternative evidence for a particular question and must be checked.

Select around evidence relationships and readable, dense full text, not counts
alone. Prefer plausible confusions: same intervention/different population,
same model/different prediction horizon, adjusted/unadjusted results and similar
numeric estimates. Record why each candidate adds coverage or competition.
Most selected cardiology papers receive grounded queries; a small additional
competition set can have none. No fixed quota or total corpus target applies.
Do not select papers or gold answers because they raise observed scores.

| Query-relative role | Rule | Example (design illustration, not eligibility certification) |
| --- | --- | --- |
| answer source | Contains required evidence or an explicitly accepted alternative | No-reflow paper for a STEMI PCI score estimate |
| related distractor | Plausible competing passage, but wrong endpoint/population/timeframe/task for this question | AF stroke-risk review for that STEMI-only question |
| additional related competition | Topic-related article with no authored query or named decoy role | Another cardiology score-validation paper |
| topic outlier | Substantially different subject relative to target topic | Microbiome/TB paper in a cardiology experiment |

The same article can answer one query and distract another. If a question asks
for AF and STEMI evidence together, both papers are sources: q044/q050's audited
comparison intent must not be scored as distractor rejection. Lack of authored
queries never makes a cardiology paper a topic outlier.

## Eligibility gates and provenance

Every included article, including competition and outliers, must pass all gates:

1. Resolve a syntactically valid `PMC[0-9]+` identifier to the actual article.
   Match DOI, title, authors and publication identity; validate PMID where
   available. Pin the PMC deposit version explicitly; never silently default
   to latest or assume version 1 is the correct paper.
2. Verify exactly CC BY 4.0 or CC0 1.0 for the selected version in authoritative
   metadata and article/PDF notices. Store the exact licence URL and evidence.
   Unversioned CC BY, earlier versions, NC/ND/SA, custom/ambiguous notices and
   unresolved conflicts do not pass this project's new-selection policy.
3. Inspect captions, credit lines, supplements and notices for third-party
   exclusions. A full PDF containing unresolved incompatible material fails;
   do not silently strip material and call it the original verified PDF.
4. Retrieve the actual PDF automatically through a currently supported PMC
   route. The repository's supported route is PMC Cloud's
   `pmc-oa-opendata` metadata/PDF service, used by `download_corpus.py`.
   Resolve the pinned metadata record and its PDF object, retaining both URLs
   and provider checksum. No browser-only/publisher/manual exception qualifies.
   Missing PDF, HTML masquerading as PDF or XML-only availability fails.
5. Parse the PDF, verify nonzero pages, readable text and first-page identity,
   inspect extraction of intended evidence (especially tables), and compute
   SHA-256 of the retrieved bytes. Record acquisition time, checks and provenance.
   A file header or HTTP success alone is insufficient. Retain the original bytes;
   extracted text has its own checksum and extraction-tool version.
6. Produce an attribution inventory entry, review metadata completeness and
   record inclusion rationale and reviewer. Only `eligible` records may enter
   a frozen selected corpus. Unknown/unverified status is never a pass.

These are project selection gates, not a claim that every excluded licence
forbids all redistribution. [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
allows commercial reuse with attribution and its other conditions;
[CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/) provides a public-domain
waiver/dedication. Preserve supplied notices, credits, source/licence links and
modification history; retain attribution for CC0 as a project provenance rule.
Code licensing does not replace article terms.

[PMC dataset documentation](https://pmc.ncbi.nlm.nih.gov/tools/textmining/) identifies
Cloud as the PDF delivery service and requires article-specific rights checks.
The [legacy OA web service](https://pmc.ncbi.nlm.nih.gov/tools/oa-service/) was retired
in August 2026; it is not an approved fallback. Recheck service documentation
when acquiring articles. Extending download tooling to another route requires
explicit support and the same identity, licence and readability gates.

### Article record schema

This is a documented schema, not an enforced JSON Schema or a claim that the
legacy manifest already supplies these fields. Use a versioned selected manifest
with `schema_version`, `corpus_version`, `articles` and `selection_log`.
All fields below are required for eligible entries unless explicitly nullable.
No placeholder values qualify as verified metadata.

Every topic selection must also preserve the applicable fields already present
in `corpus_manifest.json`, including `cluster`, `search_query`, `year`, `license`,
`page_count`, `has_structured_sections`, `notes` and `license_notes`; richer fields
extend these records rather than replacing their metadata. Preserve the complete
source abstract separately from an authored summary. Starting from a PMCID,
resolve its PMID through the official PMC ID Converter and retrieve the PubMed
record for the abstract and bibliographic cross-check; obtain exact version and
licence evidence from the pinned PMC deposit. Record source URLs and hashes.
The original `search_query` must be recorded at discovery and preserved verbatim:
PubMed cannot reconstruct it, and a later PMCID lookup must not overwrite it.
Missing metadata needs an explicit absence reason, not an inferred value.

| Field | Type and rule |
| --- | --- |
| `article_id`, `filename` | Unique stable string ID and unique PDF basename; keep legacy filename aliases in migration records |
| `topics`, `topic_rationale` | Nonempty array of topic strings and membership explanation |
| `doi`, `pmcid`, `pmc_version`, `pmid` | DOI string; resolved PMCID; positive integer deposit version; PMID string or null with absence reason |
| `title`, `authors`, `journal`, `publication_date` | Exact title, ordered author names, journal and ISO date with recorded precision (day/month/year); no invented date components |
| `abstract`, `abstract_summary` | Source abstract text or null with absence reason; separately labelled optional authored summary |
| `article_url`, `metadata_url`, `metadata_sha256` | Authoritative version/source links and checksum of archived metadata response |
| `licence` | Object: `id` (CC-BY-4.0 or CC0-1.0), `version`, `url`, `notice`, `evidence_locations`, `checked_at`, `reviewer` |
| `third_party_review` | Object: `status` (clear/unresolved/excluded), inspected locations, exclusions and resolution; only clear passes |
| `download` | Object: `route` (pmc_cloud), resolved PDF URL/object/version, UTC timestamp, provider checksum (nullable), byte count, PDF SHA-256, tool/version |
| `validation` | Object: identity match evidence, page count, parser/version, readability and table checks, extracted-text SHA-256 and extraction version |
| `provenance` | Discovery query/source, acquisition/review dates, reviewer, notices/corrections/retraction check and any discrepancy resolutions |
| `attribution_id`, `selection_rationale`, `eligibility` | Inventory reference, evidence/competition purpose, and eligible/pending/excluded with gate reasons |

Keep selection failures in `selection_log` with candidate ID, failed gates,
review date, owner issue and decision. The attribution inventory records each
article's full citation, DOI/PMCID/version, source URL, exact licence link,
copyright/credit/disclaimer notices, third-party review and modifications
(including derived text). Verify inventory-to-manifest completeness before
publication. PDFs remain untracked; public PDF publication is a separate decision.

### Mandatory legacy exclusions and ownership

The article selection audit owns replacement of `cardio-hypertension-guidelines.pdf` (DOI
10.4103/singaporemedj.SMJ-2025-248) and removal/replacement of
`outlier-gpt5-tau217-diagnosis.pdf` (DOI 10.4103/singaporemedj.SMJ-2025-289)
from the selected cardiology experiment, including its full-corpus condition.
Both lack recorded PMCIDs and already have restrictive licences in the legacy licence audit.
They cannot pass by retaining a manual Ovid route. If cognition/AI diagnosis is
retained, choose an eligible replacement; the outlier audit reuses the article selection audit's decision
rather than replacing it independently. Together they are two of the existing
seven restrictive candidates, not two extra papers. Other legacy papers still
need exact-version rights and download verification; no grandfathering.

Maintain a migration ledger with old article/query ID, action (replace, retire,
rebuild or retain after verification), new ID/version, rationale, owner and all
source/distractor/synthesis/overlap dependencies. Retired cases remain traceable.
Current direct dependencies in `golden_qa.json` are hypertension: q059,q060,
q061,q062,q122,q125,q127,q129; GPT-5: q130,q131,q132,q133. Recompute from the
active query revision rather than treating this list as permanent. Extend the
dependency map beyond filename references to indirect topic/evidence overlap.

## Query and evidence schema

A versioned query set has `schema_version`, `query_version`, `queries` and a
revision ledger. Preserve stable query IDs, increase `revision` for any semantic
change and retire rather than silently reuse IDs for unrelated tasks.

| Field | Required contents |
| --- | --- |
| `id`, `revision`, `question`, `category`, `topics` | Stable ID, positive revision, self-contained question, category below and topic membership |
| `required_facts` | Fact IDs with expected values/text, units, population, endpoint, timeframe, qualifiers, tolerances and contradiction rules |
| `evidence_sets` | Nonempty OR-list of accepted complete evidence sets for answerable cases; each set is an AND-list of anchor IDs covering all required facts |
| `anchors` | Each anchor: ID, article ID/version/PDF SHA-256, page (physical PDF page, one-based), section/table/row, exact short evidence excerpt, extracted-text offsets/hash and fact IDs |
| `related_distractors` | Article/anchor IDs plus plausible confusion and why evidence fails the question's scope; empty allowed outside distractor category |
| `reference_answer`, `answer_rubric` | Grounded answer and required claims, acceptable alternatives, forbidden conflations and source conflicts |
| `answerability` | answerable/absent_fact/false_premise; for absent facts: missing fact, search scope and review; for false premises: offending premise and correction anchors |
| `dependencies`, `review` | Required/alternative/decoy/overlap articles and negative-evidence corpus dependencies; author, independent full-text review, duplicate/leakage checks |

For genuine corpus absence `evidence_sets` may be empty: specify which claim is
missing and the frozen corpus searched. A false-premise case needs positive
correction evidence, not merely absence. During migration, every legacy
`unanswerable` case maps to either
`answerability=absent_fact` (retaining category `unanswerable`) or
`answerability=false_premise` (new category `false_premise`), after evidence
review. Do not expect `context_sufficient=false` for a
well-supported premise correction. Freeze alternative sets before evaluation.
Alternative evidence must answer the same population, endpoint and timeframe,
not simply mention similar terms. One complete alternative suffices; do not
require every interchangeable source. Cross-document synthesis alternatives
must still combine evidence across documents.

Anchors identify source evidence independently of transient chunk IDs. A
retrieved chunk supports an anchor only when its content contains the required
fact and scope qualifiers; article presence or page overlap alone is insufficient.
Record chunk-to-anchor matches and extraction discrepancies. Any table whose
values cannot be bound to their rows/columns needs extraction repair or exclusion
from that evidence case. Gold facts must expose conflicting source values rather
than inventing a reconciliation (as audited in q051/q062).

### Category criteria and authoring checks

| Category | Admission criterion |
| --- | --- |
| `direct_lookup` | One local passage/table supports the fact, even if it contains multiple closely bound values |
| `multi_hop` | At least two separated evidence anchors in one article must be connected; explain why neither alone answers |
| `cross_doc_distractor` | One valid evidence set plus a plausible wrong-answer competitor; question does not require the decoy |
| `cross_doc_synthesis` | Required claims span at least two articles; each contributes evidence needed for the synthesis |
| `unanswerable` / absent_fact subtype | Requested fact absent across the entire frozen condition corpus; related text may exist |
| `false_premise` | Corpus supports explicit rejection/correction of the presupposition; implemented category |
| `source_conflict` | One article gives two unreconciled readings of the requested fact (for example abstract versus table); every evidence set contains both passages and each reading is its own required fact. A valid answer reports both with attribution; reporting one as uncontested, or merging them, fails |

Do not supply the requested answer in the question (q067), rely on undefined
“this study”, or call a single-paragraph answer multi-hop (q043). Identification
cues can disambiguate the task but must not reveal the target value. Author from
full text, verify abstracts against detailed results, bind numbers to groups,
separate association from causation and primary from secondary endpoints.
Record near-duplicates and retain them only with distinct failure-mode rationale.

Keep development/tuning IDs separate from frozen evaluation IDs. Split related
question variants and evidence families together to avoid paraphrase leakage.
Do not put gold answers, reference text or anchors into retrieval/rewrite inputs,
indexed documents or generation prompts. Freeze held-out cases before tuning;
log tuning exposure and revise the benchmark if held-out failures drive changes.
Evidence judgments may be manual initially; record method and reviewer, and
never call unimplemented checks automated results. Paid judges coordinate with
the separate generated-answer evaluation follow-up and require explicit run approval.

## Metrics: three distinct layers

Report each depth and category with numerator, denominator and unscored count.
`n=3`/`n=8` are requested chunk depths, not numbers of unique documents. Retain
production reranking order through source deduplication. Missing executions or
judgments are coverage gaps, never passes or silently dropped failures.

| Metric | Definition and limits |
| --- | --- |
| Legacy document pass rate | Existing `score_query()` pass / executed scored queries; lookup/multi-hop require document presence, distractors require expected strictly before named decoy if present, synthesis requires all expected documents; unanswerable excluded |
| Accepted document-set coverage | Fraction of answerable queries retrieving all source documents of at least one complete accepted evidence set; alternatives use OR, members use AND |
| Distractor ordering success | Fraction of distractor cases with an accepted answer source present and ranked strictly before each present named decoy; absent decoys do not fail; report decoy-present counts separately |
| Fact evidence recall | Supported required fact IDs / required fact IDs for each query, then macro-average over executed answerable queries; alternatives do not duplicate facts |
| Complete evidence sufficiency | Queries whose retrieved context supports every required fact via one complete accepted set / executed answerable queries |
| Answer correctness | Judged answers meeting every required fact, qualifier, tolerance and attribution rule without material unsupported claims / judged answerable queries |
| Absent-fact refusal accuracy | Correctly scoped non-answers without invented facts / judged absent-fact cases; do not require empty retrieval |
| False-premise correction accuracy | Answers explicitly rejecting the premise with grounded correction / judged false-premise cases |

Document coverage cannot establish evidence sufficiency or faithful generation.
Do not blend these metrics into one “accuracy”. A null result must retain its
population/statistical scope. `context_sufficient` is a model signal, assessed
against answerability subtype, not a gold answer-correctness metric.
Historical 96.4%/98.2% is the original full-host-corpus document pass rate on 111
scored of 133 queries; it describes neither Docker seed nor this new benchmark.
Versioned strengthened scoring is implemented; historical results use legacy
metrics and labelled manual evidence checks.

## Versioning, fingerprints and controlled comparisons

Every frozen release records schema, corpus, queries and scorer versions plus
content hashes; a version label alone does not prove compatibility. Use SHA-256
of UTF-8 canonical JSON (`sort_keys=True`, compact separators, `ensure_ascii=False`,
no NaN); sort set-valued ID lists while preserving author, evidence/ranking and
other meaningful array order. Exclude only each fingerprint's own hash field.
Hash raw PDF/text/source bytes separately. Document the canonicalization version.

- Corpus fingerprint: exact selected article IDs, deposit versions, PDF/text
  hashes and eligibility/attribution metadata. Each condition has its own hash.
- Query fingerprint: exact IDs/revisions, questions, categories, facts, anchors,
  alternatives, negative-evidence scope and rubrics; also record subset hash.
- Scorer fingerprint: scorer source bytes, rules/thresholds and relevant dependency
  versions; record commit and schema. Any scoring-rule change creates a new version.
- Retrieval configuration fingerprint: embedding/reranker revisions, chunker and
  extraction settings, fusion parameters, rewrite flag/model/prompt if used and
  dependency versions. For generation/judges include models, prompts and settings.

For the frozen cardiology query set define explicit membership lists:

1. **C1 answer sources:** union of all required and accepted alternative articles.
2. **C2 related competition:** C1 plus selected related cardiology competition.
3. **C3 full corpus:** C2 plus eligible other-topic articles and topic outliers.

Enforce C1 subset-of C2 subset-of C3 on exact ID/version/hash tuples; record
additions and each article's experiment-relative role. Named decoys belong in
C2/C3; C1 tests coverage without that competition. If roles overlap, source
membership takes precedence for the corpus union, while per-query roles remain.
Use the same queries, anchors, alternatives, scorer and retrieval settings in
all three conditions. Review all three for alternative evidence and newly
answerable absent-fact cases *before* freezing. A later discovery invalidates
the affected comparison: record the conflict, revise the query benchmark and
rerun matching affected conditions. Never edit expectations mid-comparison.

For configuration comparisons require identical corpus/query/scorer fingerprints
and exact requested/executed IDs and depths. For nested-corpus comparisons only
the declared corpus membership may vary; common article versions/extraction and
all other fingerprints must match. Reject incompatible comparisons; explicitly
label legacy artifacts without fingerprints as historical, unverifiable pairs.
`compare_evals.py` enforces these guards for versioned benchmark runs. Legacy
artifacts remain explicitly unverifiable and require the legacy opt-in. No cross-version percentage delta is evidence of
retrieval improvement.

### Run record and targeted iteration

Save `run_id`, UTC timestamp, code commit, benchmark/component fingerprints,
condition membership/hash, config, collection identity/path, ingestion receipt
(article hashes, extraction settings and per-document/total chunk counts),
requested/executed/missing IDs, depths, raw ranked chunk/context/source outputs,
verdicts, metric counts, review method, cost approval if relevant and limitations.
Follow [repository constraints](../AGENTS.md#constraints) for production retrieval,
reranker threading/order and host seeding, and the
[host setup](../README.md#develop-and-evaluate-host) for ingestion. Verify
extraction, article identity, chunk counts and queryability before any run.
`--ids` neither ingests nor isolates a collection. Never reset another task's
collection.

Use `.venv/bin/python eval_golden.py --ids <comma-separated-IDs>` from repository
root; add `--bm25` only for a justified configuration comparison. Confirm every
requested ID exists first: partial matches can return success today. Choose IDs
from direct source, alternative, decoy, synthesis and overlap dependencies.
Article replacements also need a justified small regression sample because
rankings may change outside direct references. Reference-only edits need evidence
review, not retrieval reruns when the scorer does not consume those edits.

The current output names are `eval_results_subset_vector-only-baseline.json`,
`eval_results_subset_vector-bm25.json`, `eval_results_subset_vector-rewrite.json`
and `eval_results_subset_vector-bm25-rewrite.json`; full runs use
`eval_results.json`. Copy each relevant artifact and run record to an immutable
run-ID location before another same-config run overwrites it. Never present a
subset percentage as whole-suite coverage. Record omitted IDs/configurations
and the reason. No automatic four-configuration sweep.

Broaden for global retrieval/scorer changes, broad expansion, unexplained
regressions or complete benchmark claims. Final baseline/comparison reporting
requires complete declared query coverage in all compared conditions; focused
iteration is not a waiver of that requirement or repository offline regressions.
Paid rewriting/generation/judging requires explicit run approval with provider
and estimated scale/cost; local retrieval without rewriting does not.

## Release acceptance

Retain eligible article records, selection/exclusion rationale, attribution and
explicit nested membership. Restrictive no-PMCID legacy papers and manual
exceptions do not enter the selected permissive corpus. Reviewed queries,
anchors, alternatives, category migration and versioned scorers define the gold.
Compatible ingestion/run receipts and complete declared coverage support the
reported comparisons. Alternative evidence and negative claims must be checked
against the actual selected corpus, rather than inferred from source recall.

Temporary epic CI filters remain until final integration and post-merge
verification. Remove those filters in a separate follow-up while retaining main
validation and publication. Active delivery routing is documented in AGENTS.md.
