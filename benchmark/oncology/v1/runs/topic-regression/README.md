# Focused topic regression

C1 is the 32-article merged cardiology/diabetes corpus; C2 adds all 14 reviewed oncology articles. These condition names belong to these regression envelopes, not the original topic releases. `parents.json` records exact original query/manifest hashes. Only the query envelope's selection linkage changes; full questions, categories, facts, anchors, revisions and evidence sets are identical to the parents. Common article versions/PDF/extraction hashes were checked against both topic manifests.

Raw baseline/expanded files contain results at both depths. Four original cardiology IDs and two additional controls are disjoint; four diabetes IDs include one unscored absent-fact control. Comparisons are valid only for matching subsets and the declared nested conditions. These artifacts do not claim complete-topic coverage, new gold review, clinical accuracy or refusal correctness.

The shared `baseline-ingestion.json` and `expanded-ingestion.json` receipts apply to both topic adapters: collection membership is the same, while each adapter uses its own preserved questions. All evaluation model fingerprints match their ingestion receipts. Fresh stores were ingested using the production handler and `../ingest_isolated.py`; no HTTP server or paid provider call was started.

The temporary combined corpus directory links pinned files from the existing diabetes and oncology corpora; bytes are checked by `read_release()`. To reproduce on another host, populate a directory with all 46 manifest-listed PDF/text pairs, choose unused collection paths and pass explicit benchmark, corpus, condition, IDs and output paths to the existing scripts. Do not overwrite the saved outputs or use another task's store.
