# Repository evidence and release scope

This release presents a working RAG service, controlled retrieval experiments
and inspectable findings. The main reading path is [the project overview](../README.md),
[current methodology](../adr/002-evaluation-methodology.md), [benchmark guide](../data/benchmark/README.md)
and [findings](../data/findings/retrieval.md). Raw scientific evidence is retained
so an engineer can trace a claim without depending on a temporary workspace.

## Concrete file selection

[release-inventory.csv](release-inventory.csv) lists every net change from main
at `b621ad16974e895790696938e127410383d840a8` to this release, using rename detection.
Each row records Git status, destination and prior path, decision, role,
rationale and dependency basis. It includes this scope document and inventory.
Unchanged service files are outside that net diff; the service's production
retrieval behavior is unchanged by the release consolidation.

The selection retains current scientific inputs/results and necessary historical
dependencies. Presentation is consolidated without changing those records:
V2 is the default host path; original V1 reproduction is in the
[historical benchmark guide](../data/archive/v1/README.md), with its [original methodology](../data/archive/v1/methodology.md).
[Later methodology history](../data/archive/development/methodology-history.md)
sits beside the archived development experiments.
The deleted root comparator is replaced by the maintained utility under tools/.

| Retained group | Why it belongs | Dependency consequence |
| --- | --- | --- |
| `data/manifest.json` and current topic envelopes | Authoritative article inventory, gold, condition membership and evidence contracts | Evaluation and case generation must use these exact inputs |
| `data/benchmark/sources/` | Selection/attribution, metadata, migration decisions and topic evidence | Metadata joins, source identities, topic integrity checks and historical parents need these records; authoring `v1` is not the original corpus archive |
| `data/evaluations/` | Ranked contexts, receipts, analysis and original seal/overlay | Findings and saved-evidence replay depend on them |
| `data/findings/` | Readable results, exact conflict cases and compact provenance | Preserve README links and every measured claim's source/query/run identity |
| `data/archive/v1/` | Original manifest, gold and five evaluations | Preserve original bytes and schemas, legacy tooling defaults and migration baseline checks |
| `data/archive/development/` | Earlier combined inputs/results and final model-review evidence | Historical derived baselines, seals and correction history require them |
| `tools/corpus/` and `tools/evaluation/` | Reusable acquisition, integrity and production-path evaluation | Updated imports, module entry points and tests remain consistent with the data layout |
| `tools/evaluation/historical/`, `tools/historical.py`, `data/layout.json` | Hash-bound original helpers/tests, original-layout replay and relocation records | Do not directly execute relocated historical helpers or rewrite frozen provenance paths |
| Generated case pages and generator | Human-readable question → sources → evidence → expected-response relationships | JSON stays authoritative; `--check` detects stale pages |
| Tests, ADRs, standards and build support | Protect behavior and explain decisions | Keep offline historical CI prerequisites and current module paths |

The prior data/tools layout was reviewed at epic commit
`632aec977445648c587d860e576c05f02da45a95`. Historical execution is pinned separately
at `c8caa0cf1327b73f358ad4c2e3c16c9736d079d9`, as recorded in the layout map.
Duplicated manifests, earlier runs and date-specific helpers are not removed
merely because their names look historical: seals, parent-result joins and
helper fingerprints make them part of the retained evidence chain.

Intermediate model-review orchestration, prompts, replies and superseded
findings were already excluded from the release. Their immutable
[pre-cleanup archive](https://github.com/juan-casimiro/ai-research-assistant/tree/benchmark-epic-before-cleanup-2026-10-06)
at `e3eada3363ad7eb7b1f56d5a5053496a24498a8a` preserves the historical record;
it excludes ignored local PDFs and does not replace current evidence.
No new scientific artifact removals are selected here. Downloaded PDFs/text,
collections, credentials, logs and temporary workspaces remain outside Git.

## Claim and verification boundaries

The original V1, earlier combined run, Docker demo and current V2 have separate
scopes. Retain current question/source/evidence contracts, accepted alternatives,
public article identities and legitimate failures. In particular c012/c013/x005
require both attributed readings; no narrower question or relaxed grading is
part of this selection. Gold is LLM-authored/model-reviewed, not expert-certified.
Retrieval coverage is not generated-answer correctness.

[Offline verification](../data/README.md#verify-the-retained-experiment) checks
369 immutable relocated artifacts against the pinned original source. Full
saved-evidence replay additionally requires local pinned PDF/text inputs and
recomputes the sealed experiment's 266-path evidence, 55 article joins and 158
case analysis without model/provider calls. Historical regression tests exercise
the original runtime, while the current test suite exercises maintained code.
Topic integrity checks and generated-case/local-link checks cover the adapted
presentation and source metadata. A byte-identical saved replay does not promise
byte-identical fresh approximate-index inference.

This file inventory is a reviewable selection, not proof that integration has
merged. Refresh the diff and inventory if main or the selected release changes;
check synchronization, applicable CI and the complete evidence before integration.
Temporary epic CI filters remain through integration and post-merge verification.
Generated-answer judging and repository-owned agent skills remain later work.
