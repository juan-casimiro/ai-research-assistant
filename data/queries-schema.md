# Q&A input fields

`queries.json` contains 158 cases adapted from the recorded epic commit to the
current corpus IDs. The source questions, answers, scientific qualifications,
accepted alternatives and evidence text are preserved. Topic anchor IDs are
prefixed to avoid collisions. This is a new input version, not the original
frozen release. Removed C1/C2/C3 metadata and historical workflow review blocks
are not current evaluation instructions. Original inputs remain in the source commit.

## Review status

This benchmark is **model-reviewed, not expert-certified**. Its expected answers,
scientific qualifications and evidence have not been certified by domain experts.
Some retained answer rubrics explicitly state that independent full-text and
cross-topic alternative review remains pending before freeze. Those reviews
remain outstanding; consolidation and successful validation or evaluation do
not constitute completion of scientific review. Local evaluation may proceed,
but results should be interpreted with this review status in mind.

## Envelope

| Field | Meaning |
| --- | --- |
| `schema_version` | Input format version, currently `1.0` |
| `query_version` | Version of this adapted question set |
| `schema_document` | Relative link to this field guide |
| `source_commit` | Original epic Git commit |
| `queries` | Unique evaluation cases |
| `anchors` | Unique supporting and distractor excerpts referenced by cases |
| `sources` | Map from current article ID to PMCID, pinned PMC version, PDF SHA-256 and production-extracted text SHA-256 |

`data/corpus_manifest.json` owns article filenames and scientific metadata.
`sources` retains only the identity/hash pins needed to validate evidence; it is
not a duplicate article catalogue. The manifest must have exactly the same source
membership. PDFs and adjacent UTF-8 text must match these hashes before retrieval.

## Query

| Field | Meaning and requirements |
| --- | --- |
| `id`, `revision` | Sequential `q001`–`q158`, sorted by the first topic alphabetically then original numeric ID; positive revision number |
| `question` | Nonempty text passed to retrieval; gold is never passed to retrieval |
| `topics` | Topic labels; no C1/C2/C3 membership logic |
| `category` | `direct_lookup`, `multi_hop`, `cross_doc_distractor`, `cross_doc_synthesis`, `unanswerable`, `false_premise`, or `source_conflict` |
| `answerability` | Object with `status`: `answerable`, `absent_fact` for unanswerable, or `false_premise` for false-premise cases |
| `answerability.search_scope` | Required for absent-fact cases: a preserved prose statement or an object with reviewed `article_ids`, `searched_terms`, `reviewed_sections`, and `rationale`. This documents the reviewed scope; it does not prove absence in additional sources |
| `reference_answer` | Expected scoped answer; reference only, no automated answer judging |
| `required_facts` | Fact objects; empty only for absent-fact cases |
| `evidence_sets` | Complete sufficient alternatives; empty only for absent-fact cases |
| `related_distractors` | Competitors with source ID/filename, `anchor_id`, `reason_inapplicable` and `plausible_confusion`; required for distractor cases |
| `answer_rubric` | `required_claims` references fact IDs; `acceptable_alternatives`, `forbidden_conflations`, and `judging_status` retain answer-review guidance |
| `dependencies` | Reviewed required, alternative and competing source relationships; article references use current IDs |
| `reasoning` | Required multi-hop reasoning rationale; absent for other cases when unnecessary |
| `selection_rationale` | Optional original scientific case-selection rationale |
| `supersedes_epic_coverage_of` | Optional original coverage lineage; not a scoring instruction |

Each fact has a query-local `id`, expected statement (`expected_text` or the
preserved `expected` field), `units`, `population`, `endpoint`, `timeframe`,
`qualifiers`, `tolerance`, and `contradiction_rule`. These preserve scientific
limits and interpretation; empty descriptive values add no constraint.

Each evidence set has `id`, `anchors` and `fact_anchors`. Every required fact maps
to one or more anchors in that set, and every listed anchor binds to a fact.
All anchors within one set are required; any complete alternative set suffices.
Partial pieces from different sets do not establish complete evidence coverage.

## Anchor

`id` is unique across the file. `article_id` and `filename` identify the source.
`pmc_version`, `pdf_sha256` and `text_sha256` bind the deposit and local bytes.
`text_start` and `text_end` are Python character offsets into production-extracted
text, with an exclusive end. The sliced text must equal `excerpt`, whose UTF-8
SHA-256 is `excerpt_sha256`.

`page`, optional `pages`, and `section` locate the evidence for human review.
`fact_ids` use current query IDs when query-qualified; references outside this
dataset carry an `epic:` prefix. Bare fact IDs remain query-local. Evidence-set mappings own
scoring. Optional `role` describes support/distractor use. These references do
not imply that every alternative is required simultaneously.

## Metrics

Document coverage requires all source documents from one sufficient evidence set.
Evidence coverage requires its pinned excerpts, bound to the right sources;
certified adjacent chunks can jointly cover an excerpt. Fact recall reports the
fraction of supported facts. Distractor ordering requires sufficient sources to
rank ahead of retrieved competitors.

Some complete evidence sets need more chunks than the retrieval depth allows;
a failure can reflect the chunk budget as well as retrieval quality.

For example, if complete supporting evidence needs 4 chunks but retrieval returns
only 3, evidence coverage fails even when the right documents are found.

Absent-fact cases are not positively scored. False-premise cases assess correction
evidence, not whether an answer corrected the premise. Source-conflict cases
preserve both attributed readings. These metrics do not judge generated answers,
clinical correctness or semantic support missed by literal excerpt matching.
