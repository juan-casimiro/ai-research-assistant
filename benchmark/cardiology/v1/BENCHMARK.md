# Cardiology query release v1 — JUA-109

The authored release contains **45 cases** and **77 pinned evidence anchors**:
14 direct lookups, 9 same-article multi-hop cases, 7 related-document distractor
cases, 8 cross-document syntheses, 3 absent-fact cases and 4 false-premise cases.
It is ready for independent PR review by Juan. Approval of the release commit
freezes the questions, facts, alternatives and rubrics before any retrieval
configuration comparison. Author verification is not independent clinical review.
No retrieval scores, generated answers, paid calls or configuration tuning were
used to construct it. It makes no new retrieval-quality or BM25-benefit claim.

`queries.json` defines `cardiology-queries-v1`, per-case revisions, required facts,
units/population/endpoint/timeframe qualifiers, complete accepted evidence sets,
related competitors and answer rubrics. Anchors bind excerpts to the selected
article, physical PDF page(s), section/table, PMC version, PDF/text hashes and
exact extraction offsets. `case_dependencies.json` maps case → fact → anchor →
article/location and retains required, alternative, decoy, overlap-review and
negative-evidence dependencies. `case_review.json` records all selected-article
scope decisions, all 34 legacy dispositions, independent-review status and the
visual table checks. The pinned selected articles and their attribution are in
[ATTRIBUTION.md](ATTRIBUTION.md).

Validation enforces category/status agreement in both queries and versioned run
results: `unanswerable` requires `absent_fact`, `false_premise` requires the same
status, and the four retrieval categories require `answerable`. This keeps
summary and comparison denominators consistent.

## Migration and ambiguity

All 34 legacy cardiology cases were reviewed, including the 17 directly dependent
on the removed AF review or hypertension survey. **21 are revised at revision 2;
13 are retired**, with successor tasks and rationale in `migration.json`.
`golden_qa.json`, its 133 cases, original article manifest and historical results
remain byte-identical. Similar IDs do not mean comparable questions or scores.

Examples of resolved authoring problems:

- q044 and q050 require both attributed articles, so they are syntheses. q050
  removes the erroneous shared high-AUC premise.
- q055 and q066 use co-located findings, so they are direct lookups. q043’s removed
  explainability claim is retired; c001/c002 ask supported prediction/calibration
  questions. Multi-hop cases retain separate required locations and a reasoning
  step, rather than counting any two numbers as two hops.
- q051 preserves the unresolved CCTA sample-count inconsistency. It does not
  invent a subset definition. Table values and malformed source statements are
  attributed as reported, rather than silently repaired.
- q067 removes its leaked target and remains an intentional simple retrieval
  floor alongside q065’s incidence plus subgroup task. q068/q121/q123 are retired
  duplicates. Reused anchors elsewhere ask distinct scope/design comparisons.
- q058 distinguishes lack of diabetes-status interaction from proof of glycemic
  independence, despite the paper’s broader conclusion. Observational clinical
  and genetic associations do not become causal treatment claims.
- The removed physician-survey percentages, including q062’s conflicting referral
  ranges, cannot be transferred to replacement consensus papers. New cases use
  diagnostic requirements, population-specific estimates and primary BP evidence.

C1 is now the **actual 19-article union of required and accepted alternative
sources**. C2 adds the Korean RH consensus and echo/AHRE paper as real related
competitors. C3 still equals C2: later-topic verified additions are separate work.
Decoy roles are case relative: e.g. the two STEMI papers legitimately answer their
own scoped questions and compete only when their populations/score variants are
inapplicable. q047 accepts a genuinely equivalent complete abstract/result set;
c004 instead preserves the AF review/primary-trial percentage disagreement.

The three absent-fact labels were reviewed against all 21 selected articles and
are stable across current C1/C2/C3. They ask missing follow-up for specific study
cohorts, not universally unknown medical facts. False-premise cases carry positive
correction evidence and explicit offending premises. Neither category is scored
as a generated-answer success by this retrieval harness.

## Metrics and provenance

`eval_golden.py --benchmark benchmark/cardiology/v1` calls production `retrieve()`
at depths 3 and 8. Only the question enters retrieval. Gold facts/excerpts are
used afterwards. Reranked chunk/source order is retained; no retrieval or reranker
implementation changes are part of this task.

The new outputs distinguish:

- **Document coverage:** all articles of at least one complete accepted evidence
  set appear. This remains possible when the right paper’s wrong passage appears.
- **Pinned-excerpt coverage:** every required anchor of one complete set appears
  inside a source-bound chunk or is covered by verified adjacent production
  chunks from that source. Before model loading, `pinned-span-coverage-v3`
  maps each raw pinned excerpt offset to contiguous chunk windows in the
  authoritative text. A spanning match requires every whole normalized chunk
  in a certified window, with distinct retrieved indices; retrieval rank does
  not establish adjacency. Arbitrary fragments, missing intermediate chunks and
  mixed sources cannot complete a span. Alternative complete sets use OR;
  anchors within a set use AND. A query's minimum chunk budget is the cheapest
  complete alternative, allowing anchors to share chunks and retaining any
  required duplicate multiplicity. NFKC/whitespace normalization preserves
  values, signs and qualifiers; a naked number or the same excerpt attributed to
  another paper cannot match.
- **Fact recall:** share of required facts whose anchor requirements are covered.
  A fact may use any accepted alternative. Mixed partial alternatives can yield
  fact recall 1 while complete-set coverage still fails; both are reported.
- **Distractor ordering:** the first occurrence of every accepted source in a
  complete document set precedes each retrieved competitor. An absent competitor
  is reported separately, so ranking passes without competition are visible.

Exact excerpts are a conservative reproducible proxy, **not semantic evidence
sufficiency or answer correctness**. An unlisted valid paraphrase or retrieval
of only part of a pinned span can cause a miss. Preflight certifies that pinned
spans can be covered with enough production chunks; this does not guarantee
coverage within a particular retrieval depth. Saved query records include
`evidence_feasibility.minimum_chunks` and `by_depth` statuses (`feasible`,
`infeasible` or `not_scored` for absent facts), calculated before model loading.
Manually inspect recorded contexts before interpreting failures. Broad
answers, partial answers, refusals and premise
corrections require separate review against the rubrics. Results split answerable,
false-premise correction evidence and absent-fact executions, and report zero
answer judgments. JUA-40 owns any later answer judge, subject to its separately
agreed Spring Boot/Java-AI sequencing gate; this task does not start that work.

Summary evidence reports preserve **full-set** passes/total and additionally
show **feasible-only** passes/total, the structural ceiling and infeasible IDs
at each depth. Empty denominators have JSON rate `null`; they are not a zero
percent score. Every case still runs at both depths: document coverage, ranking
and partial fact recall remain meaningful even when complete evidence cannot
fit. Macro fact recall retains the full scored set. Reports split answerable
and false-premise correction evidence, include category groups and provide a
combined evidence-bearing total; absent facts do not enter either denominator.

In the pinned release, n=3 can cover 30/42 evidence-bearing cases; the other 12
need 4–7 chunks. The answerable-only ceiling is 27/38, and false-premise
correction evidence has a separate ceiling of 3/4. At n=8, all 42 fit. These
ceilings describe gold/chunk budget feasibility, not measured retrieval success.

Runs record exact requested/executed IDs, full and subset query hashes, scorer
version/source hashes, manifest/condition/membership hashes, pinned article tuples,
retrieval source/dependency hashes, loaded embedding/reranker file hashes,
rewrite provider/model, code commit, UTC time, flags, depths, retrieved contexts
and per-anchor chunk indices plus complete support groups (`anchor_match_groups`).
Feasibility has its own version (`minimum-evidence-chunks-v1`) and a fingerprint
of the requested queries' minimum budgets and depth statuses.
Group indices are zero-based retrieval positions listed in source-span order,
so a spanning group can have decreasing ranks. The runner compares actual stored
source/text chunks with the condition’s production chunking and rejects missing, extra,
duplicate or stale chunks. It verifies every selected local PDF/text and anchor,
including competitor pins when running C1. This does **not** rederive stored
embedding vectors to certify their original model; JUA-110 must retain isolated
ingestion/model provenance before making quality claims. Remote rewrite aliases
also cannot prove immutable provider weights. Keep these limits with results.

The source identifier is the manifest's `.pdf` filename. Host ingestion through
`ingest_corpus.py` saves a `.txt` extraction sidecar but posts the `.pdf` name to
`/ingest`, which preserves it. Demo seeding stores `.txt` names and is deliberately
incompatible with these conditions; disable it for isolated benchmark ingestion.
Chroma errors are reported as named errors with a nonzero exit status.

## Later focused execution

Offline validation is available now:

```bash
.venv/bin/python -m unittest discover -v
.venv/bin/python verify_cardiology_selection.py
.venv/bin/python verify_benchmark_reachability.py --condition C2
```

The reachability check needs the pinned local PDFs/text but loads no models,
opens no collection and makes no API calls. It supplies every production chunk
to the scorer, then requires coverage of every available anchor and every
evidence-bearing query with fact recall 1. It separately reports unlimited
coverage, per-depth feasible/infeasible IDs and every query's minimum chunk
count. It also verifies that each minimum-sized witness passes the scorer.
C2 has 77 anchors reachable with all chunks; 36 require adjacent chunks.
C1 and C3 can be checked with the same command; all conditions have the same
30/42 n=3 and 42/42 n=8 ceilings. These are structural assertions, not
retrieval-quality results. Synthetic boundary/budget regressions run in offline
CI without downloaded corpus files. V3 comparisons require matching feasibility
metadata and hashes; v1/v2 runs cannot be mixed with v3 or compared using this
contract. Historical baseline artifacts remain unchanged.

After PR review/freeze and JUA-110’s isolated condition ingestion, use the configured
collection for that exact condition. The benchmark runner never seeds or ingests.
For example, **only after C2 is ingested**:

```bash
SEED_ON_EMPTY=false CHROMA_PATH=./chroma_db/cardio-C2 \
  .venv/bin/python eval_golden.py --benchmark benchmark/cardiology/v1 \
  --condition C2 --ids q047,q050 --output eval_results/runs/example-vector.json
```

Do not use that command on an unprepared collection. The named output must not
already exist. The default output is a unique `eval_results/runs/<UTC>-<id>.json`.
After release/ID validation, the destination is created and reserved exclusively
before model loading or any external calls. The runner atomically checkpoints
each completed depth with provenance and contexts. Only a run finishing both
depths for every requested ID receives `run_status: complete` and a summary.
An interrupted/failed run retains an incomplete checkpoint; comparison refuses
`setup`, `running` or `incomplete` snapshots, even if every result is present.
Completed IDs mean both depths finished. Use a new output path for a subsequent
run; checkpoints do not implement automatic resumption. A later filesystem
failure can still prevent saving the newest response, but failed atomic writes
preserve the last successful snapshot.
`--bm25` and `--rewrite` retain production flag semantics. Rewriting makes external
calls and needs the Working Agreement’s paid-run approval; no such run is included
here. No full 133-query historical run is required for authoring or metadata edits.

For flag ablations, hold the reviewed query/scorer/model/corpus fingerprints,
IDs and depths fixed. For a source change, first re-review the dependency union
(required, alternatives, decoys, overlap and negative evidence), revise affected
cases, then use `--ids` for only that union and relevant configurations. Current
all-selection overlap review intentionally makes source changes conservative.
The dependency map is query-hash bound; regenerate it when gold changes.

```bash
.venv/bin/python compare_evals.py <vector-run.json> <bm25-run.json>
.venv/bin/python compare_evals.py <C1-run.json> <C2-run.json> --nested-corpus
.venv/bin/python compare_evals.py <historical-baseline.json> <historical-bm25.json> --allow-legacy
```

Normal comparisons reject changed gold/scorer/retrieval pins, changed corpus,
incomplete/duplicate IDs and missing provenance or metrics. They also reject
missing, inconsistent or changed per-query feasibility, including in nested
comparisons; infeasible cases cannot be saved as complete-evidence passes.
Both full-set and feasible-only evidence coverage are printed with their
denominators and ceiling/IDs, while fact-recall changes remain visible for all
scored cases. False-premise correction evidence has a separate report.
Explicit nested-corpus
comparisons require identical flags and a superset with identical common article
versions/hashes. Historical pairs require `--allow-legacy`, are labelled
unverifiable, and cannot be mixed with this versioned benchmark. An authoring
revision requires a new comparable baseline, not a before/after quality claim.
