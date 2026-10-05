# Source-grounded gold corrections — 2026-10-05

This applies the clear benchmark mismatches recorded in [PR 45](https://github.com/juan-casimiro/ai-research-assistant/pull/45). It preserves the established evaluation strategy: articles and questions must meet the existing category and evidence rules. Juan does not need to adjudicate biomedical facts manually; the corrections use the recorded model reviews and pinned source text.

## Decisions

| Query | Correction |
| --- | --- |
| a001 | Relabel the continuous tissue/neuron Results passage as direct lookup; retain the factual contrast. |
| a007 | Relabel the short imaging/genetics/autopsy case account as direct lookup. |
| a009 | Require the diagnostic genetic result only; autopsy and decoy discussion are optional. |
| c003 | Explicitly request scattergram-level performance and correct the endpoint metadata. |
| c012 | Keep the original question. Accept either source-reported pair of adjusted estimates (abstract/Results text or Table 2), with Table 2 added as alternative evidence; use retrospective observational for HFpEF and accept attributed case-control/cohort labels. |
| c013 | Keep the original question and relabel direct lookup. Accept either source-stated price basis (abstract 2022 US prices or Methods NADAC July 2023), with the complete abstract passage and the Methods passages as alternative evidence. No mandatory current-price or head-to-head commentary. |
| c016 | Explicitly request the genetic limitation and comparison with advanced-CKD renal/infection evidence, preserving cross-document synthesis. Remove the unrequested sulfonylurea claim. |
| d015 | Explicitly request the environmental limitation as well as the inverse genetic association, preserving two necessary passages; each part is its own required fact. |
| d016 | Explicitly request the three reported HFpEF outcomes and indirect comparison design, preserving two necessary passages; each part is its own required fact. |
| d020 | Specify primary intention-to-treat analysis so the false premise is actually false in the requested scope. |
| q058 | Restrict diabetes-status interaction to the five reported marker changes, excluding GDF-15 and rehospitalization. |
| x004 | Require only the two treatment-count results; discussion of the competitor is optional. The competitor remains a decoy. |
| x005 | Keep the original question. Accept either source description of the ANN task (abstract risk prediction or detailed binary classification), with the detailed passages as alternative evidence; replace the copied ARG warning. |

The ten question/key/scope issues can affect answer or evidence grading. The three category-only issues (a001, a007, c013) are inexpensive label repairs, not evidence that the factual answers or retrieval system failed. Calling every item “blocking” follows the validation rule but can exaggerate their practical similarity. Minor authoring preferences do not warrant another full review cycle.

The article conflicts in c012, c013 and x005 are handled by accepting either source-supported reading, each with its own evidence set, rather than by naming a section in the question or inventing a reconciliation. Discussing the contradiction is not a mandatory answer claim.

## Revision and verification

[revision_ledger.json](revision_ledger.json) records the prior and corrected per-case and query-set fingerprints. Each of the 13 cases increments its revision. The parent commit preserves every previous question and key; existing run artifacts and PR 45 findings remain historical records. The 145 other cases are unchanged. This is targeted correction, not a fresh 158-case independent certification or a re-audit of all retained minor notes.

Current condition and review/dependency fingerprints track the corrected files. No corpus membership, source bytes, retrieval code, scorer or historical evaluation is changed. Existing results must not be presented as executions of these corrected revisions. Integration into later combined releases must use these corrected source sets and regenerate combined fingerprints.

All 206 offline tests passed. [verification.json](verification.json) records schema/revision checks and 170 pinned-text anchor checks across the four affected sets. No additional Codex CLI, Claude CLI, retrieval, answer-generation or paid judge run was launched. Page metadata is retained from source anchors; this check did not reacquire PDFs.

Future quality comparisons should execute the corrected revisions in affected conditions. They are not part of this correction task; any paid rewriting or generation run requires explicit approval. Category-only changes may permit clearly labelled rescoring of preserved results where the required evidence and retrieval inputs are identical; changed questions require new retrieval executions.
