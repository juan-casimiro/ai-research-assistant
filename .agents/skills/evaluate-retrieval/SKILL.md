---
name: evaluate-retrieval
description: Evaluate production retrieval against the current corpus and Q&A dataset with separate document and evidence metrics, checking acquisition and ingestion prerequisites first. Use for retrieval experiments or the evaluation stage of a corpus workflow, not generated-answer judging.
---

Follow [the evaluation workflow](../../../tools/evaluation/evaluation-workflow.md)
in the active ai-research-assistant checkout. Use the supplied corpus, manifest
and Q&A paths, or the documented current defaults; the collection is read from
`corpus/<corpus_name>/chroma` beside the corpus. Report prerequisite failures
and conflicts; do not repair benchmark evidence to make a run pass.

Check readiness before running retrieval. If inputs and the collection are ready,
run the requested evaluation without a prerequisite warning or confirmation.
If preparation is missing, explain the missing steps in dependency order:
[generate-corpus-metadata](../generate-corpus-metadata/SKILL.md) for acquiring
and verifying PDFs and adjacent text, then
[ingest-corpus](../ingest-corpus/SKILL.md) for creating the collection, then
evaluation. Load those skills only when their steps are needed. For an
evaluation-only request, report missing preparation rather than silently expanding
scope; for an explicitly requested whole flow, perform the missing steps within
the user's authorization. Preserve deletion, benchmark-conflict and paid-call
approval requirements in the linked workflows.
