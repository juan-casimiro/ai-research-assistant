# Benchmark gold validation plan — JUA-106

Status: executed on 2026-10-03 and 2026-10-04; results are in
[REPORT.md](REPORT.md). The plan produces findings only: no gold, anchor,
source or run artifact is edited.

## Goal

Check, case by case, that every question, reference answer, anchor, distractor,
alternative and absence claim in the JUA-106 benchmark is supported by the
article text in `corpus/JUA-106/**/*.txt`, and that it stays true as the corpus
grows from C1 to C2 to the combined C3. Retrieval repeatability and
generated-answer stability are out of scope (Juan's decision, 2026-10-03).

Every case so far has author review only (`review.independent_review` is
pending in all five sets), and 144 of 158 cases were authored by Codex. This
plan supplies the independent review the [standards](../../STANDARDS.md)
require before freeze.

## Scope: 158 cases, 55 articles

| Set | Queries file | Cases | lookup | multi-hop | synthesis | distractor | false premise | unanswerable |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| cardiology | `benchmark/cardiology/v1/queries.json` | 45 | 14 | 9 | 8 | 7 | 4 | 3 |
| diabetes | `benchmark/diabetes/v1/queries.json` | 49 | 23 | 10 | 5 | 4 | 3 | 4 |
| oncology | `benchmark/oncology/v1/queries.json` | 44 | 21 | 8 | 3 | 2 | 7 | 3 |
| outliers | `benchmark/outliers/v1/queries.json` | 10 | 4 | 1 | 0 | 1 | 3 | 1 |
| ALS/FTD (prepared) | `benchmark/als-ftd/v1/queries.json` | 10 | 2 | 4 | 2 | 1 | 1 | 0 |
| **Total** | | **158** | 64 | 32 | 18 | 15 | 18 | 11 |

The first four sets are the parents of the combined release being assembled in
JUA-114; Stage 0 confirms the current diabetes questions and anchors are
identical to the evaluated snapshot the combined release scores against. The
regression envelopes (`diabetes/v1/cardio-regression`, `outliers/v1/regression`)
repeat the same questions and are not reviewed again.

Article text only. PDFs are not opened. Where a verdict depends on table layout
that pypdf text cannot settle, the case is flagged `needs_pdf_check` instead of
being decided.

## Roles and models

| Role | Runner and model | Why |
| --- | --- | --- |
| Orchestrator | Claude Code session (this one or a fresh one), Opus 5.5 | Can drive the other two CLIs headless through the shell, validates outputs, builds batches. Does no judging itself. |
| Blind answerer | Claude CLI, `claude-sonnet-5-5` | Not the gold author. Kimi K3 was the first choice but reached its 5-hour usage limit after five pilot questions, so it cannot carry 158. |
| Gold auditor | Claude CLI, `claude-sonnet-5-5` | Different family from the Codex author. Close reading against a checklist does not need Opus. |
| Corpus-growth hunter | Codex CLI, `gpt-6.1-sol` (configured), reasoning effort `medium` | Codex wrote most of the gold, so it is not given a confirming role. Here it is asked to find counter-evidence, which works against author bias. |
| Adjudicator | Claude CLI, `claude-opus-5-5` | Only for cases where stages disagree; expected to be a minority. |

Model choice caveats: I confirmed the configured model names and headless flags
for all three CLIs, but not the relative credit cost of Kimi K3 versus the other
Kimi aliases, nor whether a cheaper Codex model than `gpt-6.1-sol` is available
on this account. The pilot measures actual consumption before the full run.

Four oncology cases were authored by Claude and the oncology and outlier sets
had an earlier Claude review. For those, the Claude audit is a second look by
the same family; Kimi's blind answer and Codex's growth hunt are the independent
signals.

## Workspace and isolation

`build_workspace.py` writes two disposable workspaces outside the repository,
under `<development-root>/.agent-tmp/`:

- `jua-106-blind-ws/<set>/` holds that set's C2 article text and batch files
  containing only question IDs and questions. Blind answerers run with this as
  their working directory.
- `jua-106-gold-ws/` holds the gold-aware batches: `audit/<set>/` with the same
  articles plus full gold records, and `hunt/` with all 55 articles.

The two are separate roots so that a blind run never has gold beneath its
working directory. [manifest.json](manifest.json) records the case-to-batch
assignment, runners, pilot and double-coverage cases, and hashes of the query
files, briefs and schemas. It contains no gold. Rebuild with:

```sh
cd benchmark/validation/v1
python3 build_workspace.py --corpus-dir <main checkout>/corpus/JUA-106 \
  --workspace-root <development-root>/.agent-tmp
```

- The blind workspace has no `benchmark/`, `golden_qa.json`, run artifacts or PDFs.
- Each blind run's tool transcript is scanned for any path outside the
  workspace. A hit voids that batch and it is rerun.
- Codex runs with `--sandbox read-only`; Claude runs with `--allowed-tools Read
  Grep Glob`; Kimi runs in the throwaway workspace only.
- Each stage's output is checked against a JSON schema. Invalid output is
  retried once, then recorded as a coverage gap, never as a pass.

The extracted text has pypdf spacing artefacts (for example `show ed`,
`cor onary`). Every brief tells agents to search on numbers and short tokens,
not long phrases, and not to treat a failed phrase search as absence.

## Stages

### Stage 0 — mechanical checks (no model)

Script run by the orchestrator over all five query files:

1. Every anchor's `text[text_start:text_end]` equals its `excerpt`, and hashes
   match the inventory. Already checked while preparing this plan: 247 of 247
   anchors match.
2. Every required fact maps to at least one anchor in every evidence set; every
   anchor referenced exists; anchor articles equal `dependencies.required` plus
   `alternatives`.
3. Category shape: synthesis has two or more required articles; multi-hop has
   two or more anchors in one article; distractor has a named decoy that is in
   C2 and not in the required set; unanswerable has empty evidence sets and a
   recorded search scope; false premise has correction anchors.
4. Leakage: numbers and distinctive terms from `expected_text` that also appear
   in the `question`.
5. Near-duplicate questions within and across sets.

Run from the repository root; the corpus is untracked, so point at the checkout
that holds it:

```sh
python3 benchmark/validation/v1/stage0.py --corpus-dir <main checkout>/corpus/JUA-106
```

Output: [results/stage0.json](results/stage0.json), one row per case with
`pass`, `warn` or `fail`. Failures go straight to adjudication; warnings are
passed to the Stage 2 auditor as things to look at.

Result on 2026-10-03: 143 pass, 15 warn, 0 fail. All 247 anchors match the text
at their offsets and their recorded hashes; no near-duplicate questions.

### Stage 1 — blind answer (Kimi)

Input per case: the question text and nothing else. Batches of about six cases
from one topic, shuffled so categories are mixed. The agent searches its
topic's folder (the case's C2 article set; for ALS/FTD the four ALS/FTD files).

The agent is not told the category, the expected source or that some questions
are unanswerable or built on a false premise. For each case it returns:

- `answerability`: answerable, not in these articles, or premise is wrong.
- `answer`: its own answer with values, units, population, endpoint, timeframe.
- `evidence`: for each claim, filename and a verbatim quote of 40–400
  characters.
- `other_candidates`: other passages or articles that looked like they could
  answer, and why it rejected them.
- `ambiguity`: any second reading of the question that gives a different answer.
- `confidence`: high, medium or low.

The orchestrator verifies each quote is a substring of the named file
(whitespace-normalised). Unverifiable quotes are marked and count against the
blind answer, not against the gold.

### Stage 2 — gold audit (Claude Sonnet)

Input per case: the full gold record, its anchors, and read access to the
article text. Batches of about six cases from one topic. The auditor does not
see the blind answers. It reads at least 2,000 characters either side of each
anchor and the relevant methods and results sections, not only the excerpt.

Checklist for every case:

| ID | Check |
| --- | --- |
| G1 | Question is self-contained, has one reading, and does not give away the answer. |
| G2 | Every value in each required fact (number, unit, group, CI, P value) is in the anchored text and bound to the right group, arm or row. |
| G3 | Stated population, endpoint, timeframe and adjusted/unadjusted status match the source context. |
| G4 | Each anchor supports the fact it is mapped to; no fact rests on an anchor that only mentions the topic. |
| G5 | The reference answer says nothing beyond the required facts that the text does not support. |
| G6 | Conflicting values inside the source (abstract versus table) are exposed, not silently reconciled. |
| G7 | The category matches the admission criterion in the standards. |

Extra checks by category:

| Category | Extra checks |
| --- | --- |
| direct lookup | One local passage is enough to answer. |
| multi-hop | Neither anchor alone answers; the two are really separated; both are needed. |
| cross-doc synthesis | Each article contributes a fact the other lacks; one article alone cannot answer; the comparison in the reference is legitimate and its caveats are stated. |
| cross-doc distractor | The decoy shares enough surface terms to be tempting; the stated reason it does not apply is correct; the decoy does not in fact answer the question; the question does not need the decoy. |
| false premise | The premise is false according to the text; the correction anchors are positive evidence, not mere silence; the premise is not partly true. |
| unanswerable | The fact is absent from the named article; it cannot be derived by simple arithmetic from reported values; the recorded search terms were adequate. |
| alternative evidence sets | Each alternative set answers the same population, endpoint and timeframe in full (20 oncology cases, 5 ALS/FTD, 1 each in cardiology and diabetes). |

Output per case: each check as pass, fail or cannot-tell with a quoted reason,
plus a verdict from the taxonomy below.

### Stage 3 — corpus-growth hunt (Codex)

Input per case: the question, required facts and declared dependencies. Search
space: all 55 articles, with the case's own required and alternative articles
excluded from the hunt. Batches of about eight cases from one topic.

The brief is adversarial: find evidence that breaks the case. For each case the
agent reports, with filename and verbatim quote:

- H1 undeclared alternative: another article that fully answers the same scoped
  question.
- H2 conflict: another article reporting a different value for the same
  population, endpoint and timeframe.
- H3 absence broken: for unanswerable cases, any passage that supplies the fact.
- H4 premise true elsewhere: for false-premise cases, an article where the
  premise holds.
- H5 undeclared competitor: a passage more confusable than the named decoy
  (informational; not a defect).
- H6 hidden answer in the decoy: the named decoy does answer the question.

The agent reports the filename only. The orchestrator tags each finding with
the smallest condition that file first appears in, using the membership lists
in each topic's `conditions.json`: C1, C2, C3 (51 articles), or ALS/FTD-only
(the four articles outside the combined release).
A case with no findings is recorded as stable across C1, C2 and C3. "Nothing
found" must list the search terms used.

### Stage 4 — compare (Claude Sonnet, no article access)

Per case, match the blind answer to the gold: each required fact as match,
partial, mismatch or not addressed; answerability agree or disagree; same or
different source article. This is a text comparison only, so it is cheap.

A case goes to adjudication if any of these hold:

- Stage 0 failure.
- Blind answerability differs from gold, or any fact is a mismatch. For an
  unanswerable case, "premise wrong" and "not in the articles" both agree.
- Blind answer rests a fact on a different article and the quote verifies.
- Blind answerer reported a second reading that gives a different answer from
  the gold.
- Auditor verdict is a defect. `valid_minor` is recorded as the final verdict
  without adjudication.
- Any H1, H2, H3, H4 or H6 finding.

Everything else is closed as `valid` or `valid_minor` with the stage records
attached. These triggers were narrowed after the pilot, where the first version
sent 9 of 12 cases to adjudication and none was a defect.

### Stage 5 — adjudication (Claude Opus)

One case per run, with all stage records and article access. The adjudicator
reads the disputed passages and decides. It may conclude that the blind answer
or the hunter was wrong and the gold stands. It writes the final verdict,
severity, the evidence, and a proposed correction in words. It does not edit
gold.

## Verdicts

| Verdict | Meaning |
| --- | --- |
| `valid` | Gold is supported as written and stable across conditions. |
| `valid_minor` | Annotation or wording issue that does not change scoring. |
| `defect_gold` | A required value, scope or reference claim is wrong. |
| `defect_anchor` | The anchor does not support its fact, though the fact may be true elsewhere. |
| `defect_category` | Case does not meet its category's criterion. |
| `ambiguous_question` | More than one defensible answer, or the answer is leaked. |
| `alternative_missing` | A complete undeclared evidence set exists (states the condition). |
| `absence_violated` | An unanswerable fact is present in the corpus (states the condition). |
| `premise_not_false` | The premise is true or partly true in the corpus. |
| `decoy_invalid` | The decoy answers the question or is not a plausible competitor. |
| `needs_pdf_check` | Text extraction cannot settle a table binding. |
| `unreviewed` | A stage failed twice; coverage gap. |

Severity is `blocking` when the scorer would mark a correct system wrong or a
wrong system right, otherwise `non_blocking`.

## Running a stage

`run_stage.py` sends each batch of a group to its runner headless, with the
stage brief as the prompt and the batch's workspace folder as the working
directory. Without `--execute` it only prints the commands.

```sh
cd benchmark/validation/v1
python3 run_stage.py --group pilot_stage1_blind --workspace-root <development-root>/.agent-tmp --execute
```

For each batch it:

- accepts a reply only if it matches the stage schema and covers exactly the
  batch's case IDs; otherwise it retries once, then writes a `.gap.json`
  recording the cases as unreviewed;
- for blind stages, rejects any run whose transcript names a gold location
  (`benchmark/`, `queries.json`, the gold workspace, the main checkout);
- marks every quoted passage with `quote_verified`, by whitespace-normalised
  match against the named article;
- writes the accepted reply with runner, attempts, duration and any token usage
  the CLI reported to `results/<group>/<batch_id>.json`, and keeps the raw
  transcript outside the repository under `.agent-tmp/jua-106-runs/`;
- skips batches that already have a result, so a rerun only fills gaps.

Runner commands: Kimi `kimi -m <model> --output-format stream-json -p`; Codex
`codex exec -s read-only --ephemeral --json --output-schema`; Claude
`claude -p --restricted --tools Read Grep Glob --strict-mcp-config --json-schema`.
The plumbing is tested against a stub CLI. The real flags are taken from each
CLI's help text and are first exercised in the pilot.

## Checking the checkers

Two controls run inside the pilot:

- **Seeded defects.** Eight real cases altered to be wrong in one known way
  each: a changed number, swapped arms, a fact bound to the wrong anchor, a
  reported fact labelled absent, a needed source named as an inapplicable
  decoy, a true premise labelled false, a removed alternative source, and a
  changed endpoint. They are mixed into the pilot's Stage 2 and Stage 3
  batches under plausible IDs; the reviewers are not told. Seven target the
  auditor and three the hunter. Detection is reported next to the findings.
  The generator, the altered records and the answer key live outside the
  repository in `.agent-tmp/jua-106-seeds/` and are never committed. The
  seeded batches replace the plain pilot batches for Stages 2 and 3:

  ```sh
  python3 run_stage.py --group pilot_seeded_stage2 --stage stage2_audit \
    --batch-list <development-root>/.agent-tmp/jua-106-seeds/seed_batches.json \
    --workspace-root <development-root>/.agent-tmp --execute
  ```

- **Double coverage sample.** Fifteen cases, five each from synthesis,
  distractor and false premise, get a second blind answer from Codex (group
  `stage1_double`). Agreement between the two blind answers is reported as the
  measure of how far a single blind answer can be trusted.

## Execution order and approval gates

1. Juan approves this plan.
2. Orchestrator builds the workspace, the batch manifest (case to batch to
   runner), the briefs and the output schemas under
   `benchmark/validation/v1/`, and runs Stage 0. No model calls.
3. **Pilot:** 12 cases, two per category spread across the five sets, through
   Stages 1–5, plus the eight seeded defects. Report token and credit use per
   runner, schema failure rate, isolation violations and seeded-defect
   detection.
4. **Gate:** Juan reviews the pilot and approves the full run with the measured
   cost. Briefs may be tightened here; after this point they are frozen.
5. Full run: Stages 1, 2 and 3 are independent and run in parallel, by topic.
   Then Stage 4, then Stage 5.
6. Report.

Rough scale before the pilot measures it: about 27 batches each for Stages 1
and 2, about 20 for Stage 3, and adjudication for an expected 30 to 50 cases.
Stage 1 and Stage 3 dominate because they read article text widely; expect
several million input tokens each on Kimi and Codex, and less on Claude. These
are estimates, not measurements.

Agent CLI usage consumes account credit on three providers. Under the Working
Agreement this needs Juan's explicit approval of the run; the pilot and the
full run are approved separately.

## Deliverables

All under `benchmark/validation/v1/`:

| File | Content |
| --- | --- |
| `PLAN.md` | This plan. |
| `briefs/`, `schemas/` | Frozen prompts and output schemas for each stage. |
| `manifest.json` | Case to batch to runner assignment, model and CLI versions, query file hashes. |
| `results/stage{0..5}/` | Raw per-batch outputs as returned. |
| `findings.json` | One record per case: stage verdicts, final verdict, severity, evidence quotes, condition stability, proposed correction. |
| `REPORT.md` | Counts by set, category and verdict; every non-valid case with its evidence; seeded-defect detection and blind agreement rates; coverage gaps. |

Corrections to gold are a separate, approved task. Per the standards, each one
is a recorded revision with matching reruns of the affected conditions, and the
original result is preserved.

## Limits

- This is model review, not clinical expert review. It can show that gold
  disagrees with the text; it cannot certify clinical interpretation.
- Text-only review cannot confirm table row and column bindings where
  extraction interleaves cells. Those cases are flagged, not resolved.
- A blind answerer that fails to find an answer is evidence about difficulty,
  not about validity. Only the adjudicator can call a defect.
- Absence can be shown false by one quote but never proven true; "stable" means
  no counter-evidence was found with the recorded search terms.
