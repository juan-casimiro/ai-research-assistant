# Codex-led final validation plan — 2026-10-05

This continues the findings-only validation in PR #45. Juan authorized final
Codex decisions, one query per session, text-only evidence, delivery as jcas-agent,
and a separate later task for gold corrections. Do not merge this PR.

## Scope and selection

Preserve the completed Stages 0–5, all 59 targeted Stage 6 second opinions, and
8 partial Kimi blind results. Stage 6 is a targeted second opinion with exposure
to an earlier review; it is not a fully independent or blind review.

31 cases need fresh final adjudication: a001, a004, a007, a008, a009, c002, c004,
c008, c009, c012, c013, c016, d001, d008, d015, d016, d020, d022, d023, o004,
o010, o024, q017, q030, q032, q055, q058, q083, x002, x004, x005.

Selection is reproducible in `build_final_review.py`: every Stage 6 verdict,
severity or correction disagreement, every proposed defect in either review,
and every Stage 6 result with an unverifiable quote. This includes optional-note
disagreements, not just the six highlighted cases. The remaining 28 agreeing
Stage 6 sessions are retained as accepted second opinions. The 99 cases outside
Stage 6 retain their original stage decisions; do not claim all 158 received
one-case Codex final review. Earlier batch reviews remain historical evidence.

## Single blocking rule

A defect is **blocking** if it can cause a correct answer to be scored incorrectly
(including acceptance of a wrong answer), makes the question materially ambiguous,
or violates the category admission criterion used for benchmark scoring.
Category defects block even if the legacy document-only scorer ignores them.
A `valid_minor` note is non-blocking only when none of these conditions applies;
`valid` has severity `none`. Unsettled text extraction is a blocking validation
gap, not a proven source defect. Judge the declared fact/evidence/category
contract, not hypothetical lenient scoring or a blind answerer's luck.

## Execution

1. Inspect current guidance, standards, source metadata, Stage 6 work and PR.
2. Freeze one packet/workspace per selected case under
   `<development-root>/.agent-tmp/jua-106-final-ws/<id>/`. Include only that
   question and its gold/evidence metadata, applicable standards, relevant prior
   review claims, full declared source text, named decoys, alternatives and
   competing candidates. For absent-fact reviews all 55 text articles are
   relevant to the corpus-wide criterion. No PDFs are copied or opened.
3. Launch a fresh ephemeral, read-only Codex CLI session for each case. Sessions
   have no shared conversation/history. User config is ignored. The packet/brief
   forbids other cases, out-of-workspace reads and outside sources. Run the main queue with three concurrent sessions, each deciding only its assigned case. This is
   authorized per-case review, not a full retrieval/answer-generation evaluation.
4. Save schema-checked JSON under `results/final_codex/`; preserve raw transcripts
   outside Git. Require exact .txt quote substrings after optional deterministic whitespace-only formatting recovery (original wording preserved), matching case ID, scoped
   article names, standards reasoning, severity basis and articles-read list.
   Record exact quote line locations during aggregation. Inspect tool transcripts
   for actual source access and isolation. Invalid replies are retried once;
   gaps remain explicit and prevent completion.
5. Aggregate precedence: fresh Codex final decision > accepted Stage 6 decision >
   historical Stages 0–5 decision. Never overwrite prior results. Emit a separate
   final findings file with provenance, correction text and unresolved issues.
6. Update REPORT.md and PR #45 with counts by set/category, final defect list,
   agreement/severity changes, limits, coverage and verified evidence. Keep the
   earlier report as an immutable historical snapshot. Retain Kimi's partial pass
   as experimental; do not continue it.
7. Verify input hashes, no gold/source/run changes, complete required review
   coverage and exact citations. Run required offline regressions, commit and
   push on the assigned branch as jcas-agent. Leave PR open for Juan.

## Runner and scale

The historical Stage 6 runner used `gpt-6.1-sol`, medium effort. The installed
Codex CLI 0.157.0 rejected that name for this ChatGPT account before reviewing
c012; both failed-launch attempts are preserved under `final_launch_failure`.
An initial `gpt-6-astra` high-effort attempt was stopped when Juan clarified
his Plus usage budget; its gap and transcript are preserved. Final reviews use
`gpt-6-luna` low effort for 21 routine note cases and `gpt-6-sol` low effort for
10 proposed defects. GPT-6.1 Sol remains unavailable in this CLI. No further
Astra or above-light reasoning is authorized. Record actual runner and usage per case. No model authentication or
shared configuration is changed. Juan's current request authorizes this Codex
run (31 case sessions plus at most one invalid-reply retry each). The staged
article files total about 14 MB, mostly three corpus-wide absence packets; actual
read/token use depends on each session. Uses Codex account credit, no Anthropic
or Kimi API runs and no new retrieval executions.

The manifest pins standards, query, prompt, schema, packet and article hashes.
Absence is a recorded search result, never proof; flattened text may leave table
bindings unresolved. This is model evidence review, not biomedical expert review.

Budget-preserving validation: a local `articles/` prefix and whitespace may be
normalized deterministically against the original text; original replies remain
in the transcript/adjustment log. A word/punctuation mismatch is never repaired.
c008 needed a fresh Sol low session after both Luna replies failed this check;
this additional failed-review recovery preserves both earlier attempts.

Supplemental evidence triage: c001’s horizon concern is already covered by the
scoped study question and accepted Stage 6 decision; c004’s citation concern is
covered by its fresh final review. c003/c006’s metric/population ambiguities were
appended as two fresh Sol low sessions. Final scope is 33 sessions, 27 accepted
Stage 6 agreements, and 98 historical-only cases. Supplemental/failure queues
may overlap the three-session main queue; sessions never share case context.
q032 also needed a Sol low recovery after failed Luna source quotes.

Luna found new material defects in x002/x004/x005 during routine-note review.
Those accepted Luna replies are preserved under `final_luna_preconfirmation`;
only these three cases receive Sol low substantive confirmation. Earlier
blocking category replies sometimes kept `gold_stands=true` to refer to factual
content; final findings preserve that raw signal and separately compute whether
the complete scoring contract stands under the declared blocking rule.
