# JUA-80: test-strength audit

Audited 2026-09-08 against `5fb8028` in `ai-research-assistant`. Production source,
model configuration, prompts, corpus, and deployment files are unchanged.

## Requirements and behaviour map

Read the current Linear **Repo Guide — ai-research-assistant**, **Working Agreement —
Development Process**, JUA-80 and relevant issue comments before implementation.
The current Repo Guide supersedes historical seeding counts and old pairing prompts.

| Behaviour / source of requirement | Baseline regression protection | Protection after audit |
| --- | --- | --- |
| JUA-75: normalized question, length 1–1000, result count 1–20 | Six Pydantic unit tests; no HTTP rejection tests | Retained unit boundaries; `test_api` checks 422 field locations, malformed JSON/non-object bodies, wrong types, flags, and rejection before retrieval/LLM work |
| JUA-24: ranked, deduplicated sources | HTTP query through real fusion/reranking | Retained; prompt assertions now check content and relative order rather than separator formatting |
| JUA-16: structured sufficiency independent of non-empty sources | Only sufficient=True response | `test_api` verifies insufficient=False with sources/reason, empty retrieval response, schema selection and role separation |
| JUA-73: 35s answer budget, 10s rewrite budget, no SDK retries, timeout → 504 | Constructor/bind mocks; direct endpoint calls; rewrite timeout injected at retrieval boundary | Literal budget assertions, HTTP 504/body/no-retry checks, actual retrieve → rewrite → bound LLM timeout; connection and malformed structured-output errors remain 500 |
| JUA-58: eager and lazy reranking off the event loop | Thread identity plus exact `to_thread` call count | Preserved thread-identity and stable-score-tie ordering assertions; removed dispatch-count coupling |
| JUA-30: lazy import, background startup, loading/error/ready health, readiness gates | None | `test_startup_ingest` and `test_api`: constructor-free import, environment/default boundaries, event-coordinated lifespan, failure at each startup phase, no work before readiness, readiness independent of LLM probe |
| JUA-30 / Repo Guide: host seed opt-out, empty-store seeding, BM25 refresh | None | Disabled seeding never checks seed files; populated store skips; nonempty `.txt` only; source/ID/embedding alignment; index refresh after seed; evaluation loader never seeds |
| ADR-001: paragraph chunking, oversized paragraph split, overlap | None; ADR records an earlier missing-continue defect | Whitespace/short text, preceding and trailing content around a long paragraph without duplication, overflow overlap |
| ADR-001: dense/BM25/rewrite/RRF composition and capped rerank | Only dense path with candidate lookup stubbed | `test_retrieval`: all four combinations, original question reranking, source alignment/first provenance, consensus fusion, empty corpus, pool cap, non-text rewrite fallback, real BM25 tokenization/ranking and stale-index replacement |
| `/ingest`: aligned persisted chunks, index refresh, storage errors | None | HTTP success/validation, real chunking with vector/store boundaries mocked, no success/index refresh after failed write |
| ADR-002: category scoring and comparable experiments | Saved live evaluation artifacts, no deterministic tests | `test_evaluation`: every category, distractor order, all-source synthesis, missing metadata, unanswerable exclusion, both depths and flags, missing file/unknown ID; `test_corpus_tools`: both flip directions and no-change comparisons |
| JUA-19: sufficiency evaluation sample/exclusion and error rates | Saved live evaluation artifacts only | False-premise q083 excluded, deterministic n8-pass sample, distinct FP/FN denominators, filtered sample and empty denominator, unknown-ID rejection |
| JUA-30 comments: full-corpus ingestion duplication guard | Manual workflow | `test_corpus_tools`: unavailable/loading server stops, populated store requires affirmative response, manifest filename preserved, unreadable/textless PDF does not POST |
| JUA-32/JUA-33/JUA-76: image, offline weights, seed attribution/count documentation | Historical manual evidence | Inspected Docker/Compose and current documentation; no image rebuild, real model-cache or corpus-count test added |

## Test weaknesses addressed

- The model-loading test left constructed mock objects in module globals, allowing
  later tests to inherit fake state. It now restores all loader-owned globals.
- Expectations referencing the timeout constants under test would accept a changed
  budget. They now protect the measured 35s/10s values explicitly.
- Requiring exactly two calls to `asyncio.to_thread` coupled a useful thread-safety
  test to scheduling structure. The test still checks both eager invocation and
  lazy score consumption happen outside the event-loop thread.
- Exact whole-prompt formatting was unnecessarily brittle; retained ordering,
  selected context, question, and message-role checks instead.
- Replaced two narrower direct-call timeout tests with HTTP tests. The previous
  rewrite test could pass even if the actual rewrite path never ran.
- No wholesale test deduplication: schema boundary tests and HTTP tests protect
  different failure surfaces. No production refactor or model/prompt snapshot was
  needed to improve the tests.

## Verification results

Baseline: **12 tests pass**. Final: **55 tests pass** with `unittest discover`,
including the coverage run. Focused runs passed before the final suite. Tests use
fake model/LLM/store boundaries and temporary fixtures; no real Chroma store,
model download, live LLM request, or paid evaluation was used.

The existing toolchain had `unittest` but no configured coverage, complexity,
mutation, lint, or CI gate. Added optional pinned `coverage==7.16.0` and
`radon==6.0.1` in `requirements-quality.txt`; runtime requirements and Docker image
are untouched. `pip check` and `git diff --check` pass. No arbitrary numerical gate
was introduced as part of a one-time audit.

### Coverage

Same eight production/service/CLI Python files in both reports, including uncovered
utility scripts. Tests, `.venv`, and audit tooling are excluded, explicitly in
`.coveragerc`. Combined means (executed statements + executed branch exits) /
(all statements + all branch exits), not statement coverage alone.

| Scope | Baseline statements | Final statements | Baseline branches | Final branches | Combined before → after |
| --- | --- | --- | --- | --- | --- |
| `main.py` | 133/222 (59.91%) | 221/222 (99.55%) | 15/52 (28.85%) | 51/52 (98.08%) | 54.01% → 99.27% |
| All eight files | 133/576 (23.09%) | 526/576 (91.32%) | 15/158 (9.49%) | 134/158 (84.81%) | 20.16% → 89.92% |

Final combined coverage: `eval_golden.py` 97%, `eval_context_sufficient.py` 94%,
`compare_evals.py` 96%, `ingest_corpus.py` 80%. `reset_collection.py`,
`show_failures.py`, and `debug_bm25.py` remain 0%, visibly included in the denominator.

The sole uncovered service statement is the second empty-fusion return. With the
current RRF implementation, nonempty ranked lists necessarily produce nonempty
fusion. Forcing an impossible fusion result through a mock merely to cover that
line would not add useful protection.

### Complexity and coverage hotspots

`scripts/quality_hotspots.py` joins Radon cyclomatic complexity (CC) to coverage.py
executed/missing statement lines in each function body, excluding its `def` line.
It calculates **CC² × (1 − covered fraction)³ + CC**. This is a reproducible,
line-coverage CRAP-style prioritization calculation, not a correctness score.
Nested functions are reported separately; parent spans include nested source and
must not be summed. Radon's outer `retrieve` CC excludes its closure (CC 6).

No cognitive-complexity tool was installed. The closest lightweight structural
complement reported here is maximum decision nesting from Python's AST (`if`,
loops, `try`, conditional expressions, `match`). This is **not** Sonar cognitive
complexity; it does not count comprehensions or boolean operators as nesting.
Radon accounts for those decisions in CC. Neither metric changed: no production
code was rewritten for a score.

| Function | CC | Decision nesting | Body line coverage before → after | CRAP-style before → after |
| --- | --- | --- | --- | --- |
| `eval_golden.main` | 26 | 4 | 0% → 100% | 702 → 26 |
| `eval_context_sufficient.main` | 24 | 3 | 0% → 100% | 600 → 24 |
| `eval_golden.score_query` | 15 | 3 | 0% → 100% | 240 → 15 |
| `compare_evals.main` | 14 | 3 | 0% → 100% | 210 → 14 |
| `main.chunk_text` | 10 | 3 | 0% → 100% | 110 → 10 |
| `main._seed_if_empty` | 7 | 2 | 0% → 100% | 56 → 7 |
| `ingest_corpus.main` | 7 | 2 | 0% → 82.93% | 56 → 7.24 |

The highest original complexity/coverage overlap was in evaluation, then chunking
and seeding. Those received behavioural tests first. The evaluation entry points
remain the most complex functions and still have untested branches despite 100%
body line coverage. Splitting reporting/CLI logic solely to lower CC is deferred.

### Deliberate break/restore and targeted mutation analysis

`scripts/verify_test_strength.py` copies the actual production `.py` source and tests
into isolated temporary directories. For **each** mutation it runs the selected
test successfully, edits production behaviour, requires an assertion failure with
the expected diagnostic, restores identical bytes, and reruns successfully. A
`finally` block restores the copy even after an error. Source in the checkout is
never intentionally broken. Logs and restored SHA-256 hashes are written to the
chosen output directory.

**20 curated mutations detected; all 20 restored runs passed.** Source-order,
LLM-retry and startup-error checks were repeated after final test cleanup and also passed the full
cycle. These are manually selected, meaningful mutants: no exhaustive automated
mutation population or global mutation percentage is claimed.

| Temporary production change | Observed failure |
| --- | --- |
| Permit 1001-character question | HTTP 200 instead of 422 |
| Remove endpoint readiness calls | HTTP 200 instead of 503 |
| Return 500 for answer timeout | HTTP 500 instead of 504 |
| Return 500 for actual rewrite timeout | HTTP 500 instead of 504; answer stage never reached |
| Force `context_sufficient=True` | Response True instead of False with nonempty sources |
| Reverse-sort unique sources | `test-d.pdf` before `test-b.pdf`, contrary to relevance order |
| Remove pre-rerank pool cap | Reranker received 25 candidates instead of 20 |
| Disable rewriting | Missing rewritten candidate/source |
| Disable sparse retrieval | Missing sparse candidate/source |
| Replace accumulated RRF scores | Shared document no longer promoted above single-list leaders |
| Ignore `SEED_ON_EMPTY=false` | Seed function unexpectedly called |
| Remove populated-store guard | Seed count 1 instead of 0 on second call |
| Suppress startup error state | None instead of captured RuntimeError |
| Remove oversized-paragraph `continue` | Duplicated long-paragraph content |
| Consume reranker scores on the event loop | Worker-thread assertion false |
| Enable SDK retries | Constructor got retries=2 instead of 0 |
| Invert distractor ranking rule | Expected pass/fail verdicts reversed |
| Require any rather than all synthesis sources | Incomplete synthesis passed instead of failed |
| Remove q083 false-premise exclusion | Excluded query appeared in false bucket |
| Divide false positives by total sample | 0.3333 instead of 0.5 |

## Remaining risks and deliberate deferrals

- Mocks cannot establish real retrieval quality, embedding shape/model-cache
  compatibility, Chroma persistence semantics, or SDK timeout passthrough. Historical
  live evidence in JUA-73 remains relevant; no new live claim is made here.
- Grounding tests protect propagation and provenance, not truthfulness of the LLM's
  sufficiency judgement. JUA-19's measured limitations and existing prompt remain
  unchanged. No prompt-injection mitigation or authentication added.
- `/ingest` still accepts empty text/source strings; empty chunks, duplicate IDs,
  partial writes, and concurrent BM25 rebuilds need a separate contract/design
  decision. Tests do not freeze accidental backend behaviour as a desired API.
- Startup task cancellation, repeated lifespans, and partial model-load cleanup are
  not established lifecycle contracts. Tests cover ordinary one-start loading and
  failures without redesigning module globals.
- Corpus CLI readiness checks explicitly handle connect failure and 503, but do
  not validate other HTTP error statuses before reading `chunks`. Response hardening,
  PDF extraction success, and retry semantics remain follow-up candidates.
- Evaluation subset-success/output naming, some malformed artifact cases, and
  CLI branches are not fully protected. Saved live golden results were not regenerated.
- Docker's offline cache and genuine zero-config empty-store demo remain unverified
  here. Synthetic seeding tests do not close the Repo Guide's real-demo verification
  gap. No corpus counts were duplicated in tests.
- Destructive reset and ad hoc display/debug utilities remain uncovered. No live
  reset was executed. A full mutation engine, new CI gate, and formatting overhaul
  are deferred; the curated checks provide bounded evidence with little tooling.

## Reproduce

From the repository root, with Python 3.12 and runtime dependencies installed:

```sh
.venv/bin/python -m pip install -r requirements-quality.txt
mkdir -p "$HOME/development/.agent-tmp/jua80"
export TMPDIR="$HOME/development/.agent-tmp"
AUDIT_DIR="$HOME/development/.agent-tmp/jua80"
.venv/bin/python -m unittest discover -v
.venv/bin/python -m coverage run --data-file="$AUDIT_DIR/final.coverage" -m unittest discover
.venv/bin/python -m coverage report --data-file="$AUDIT_DIR/final.coverage"
.venv/bin/python -m coverage json --data-file="$AUDIT_DIR/final.coverage" -o "$AUDIT_DIR/final.json"
.venv/bin/python scripts/quality_hotspots.py "$AUDIT_DIR/final.json" > "$AUDIT_DIR/final-hotspots.json"
.venv/bin/python -m radon cc main.py eval_golden.py eval_context_sufficient.py ingest_corpus.py compare_evals.py -s -a
.venv/bin/python scripts/verify_test_strength.py --output-dir "$AUDIT_DIR/mutations"
.venv/bin/python -m pip check
git diff --check
```

The original baseline used the same coverage source/omit options and 12 tests at
`5fb8028`, before adding tests. For a fresh baseline reproduction, use an isolated
checkout of that commit and the same optional tool versions; do not reset a working
checkout. The hotspot script can join that baseline JSON because production source
is unchanged in this PR. Local raw evidence is retained under
`~/development/.agent-tmp/jua80/`; this document records the portable review results.
