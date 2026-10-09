---
name: evaluate-retrieval
description: Evaluate production retrieval against the current corpus and Q&A dataset, with separate document and evidence metrics. Use for retrieval experiments, not corpus acquisition or generated-answer judging.
---

Follow [the evaluation workflow](../../../tools/evaluation/evaluation-workflow.md)
in the active ai-research-assistant checkout. Use the supplied corpus, manifest
and Q&A paths, or the documented current defaults; the collection is read from
`corpus/<corpus_name>/chroma` beside the corpus. Report prerequisite failures
and conflicts; do not repair benchmark evidence to make a run pass.
