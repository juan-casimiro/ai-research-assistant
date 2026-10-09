---
name: ingest-corpus
description: Ingest an acquired corpus manifest into a new isolated collection, in-process, with seeding disabled. Use after corpus acquisition and before retrieval evaluation; not for corpus acquisition, the Docker demo or appending to an existing collection.
---

Follow [the ingestion workflow](../../../tools/corpus/ingestion-workflow.md)
in the active ai-research-assistant checkout. Use the supplied manifest, corpus
directory and collection path, or the documented defaults. Report failed
safeguards; do not reuse, reset or append to an existing collection to make a
run pass.
