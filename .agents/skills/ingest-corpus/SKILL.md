---
name: ingest-corpus
description: Ingest an acquired corpus manifest into a new isolated collection, in-process, with seeding disabled. Use after corpus acquisition and before retrieval evaluation; not for corpus acquisition, the Docker demo or appending to an existing collection.
---

Follow [the ingestion workflow](../../../tools/corpus/ingestion-workflow.md)
in the active ai-research-assistant checkout. Use the supplied manifest and
corpus directory, or the documented defaults; the collection is created beside
the corpus at `corpus/<corpus_name>/chroma`. Report failed safeguards; do not
reuse, reset or append to an existing collection to make a run pass.
