# Historical model review of benchmark gold

Model reviews of all 158 cases ran on 3–5 October 2026. The final review identified
13 material corrections and retained 145 cases without material correction.
These were judgments against pinned extracted article text, not biomedical expert
certification, retrieval evaluation or generated-answer evaluation.

Stages 0–5 covered the full benchmark. Stage 6 added 59 targeted second opinions;
reviewers saw prior findings, so those opinions were not blind or fully independent.
Fresh one-case sessions resolved 33 remaining disagreements. This was not a fresh
independent 158-case final review. Category defects were considered material when
they could invalidate the declared grading contract, even where legacy
article-only scores were unaffected.

## Decisions and subsequent corrections

The byte-preserved [final findings](results/final_findings.json) and
[verification record](results/final_verification.json) describe the historical
review. Their relative packet, reply and transcript references resolve in the
[immutable review archive](https://github.com/juan-casimiro/ai-research-assistant/tree/benchmark-epic-before-cleanup-2026-10-06/benchmark/validation/v1).
Intermediate orchestration, prompts, replies, execution gaps and superseded
findings are archived there rather than shipped with the release.

The [correction ledger](../../corrections/2026-10-05/README.md) explains what was
accepted and changed afterward. Historical proposals are not the current grading
contract. In particular, c012, c013 and x005 retain their original questions and
require both attributed readings; their retrieval failures remain valid findings.
The [current case index](../../cases/README.md) reflects authoritative current gold.

Gold is LLM-authored and model-reviewed, not expert-certified. Minor notes retained
by the historical review and later explicit corrections remain legitimate limits.
The review did not measure answer accuracy or clinically correct refusal.
