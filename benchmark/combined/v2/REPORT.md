# Combined corrected-gold retrieval benchmark

**All 55 articles / 158 queries are verified at n=3 and n=8.** At n=8,
complete source sets are retrieved for 115/129 answerable cases and complete
pinned evidence for 37/129. Failures remain in the denominator. No generated
answers, refusals or conflict explanations were evaluated.

## Scope, configuration and historical boundary

The corpus contains 55 unique version-pinned articles, 3,638 production chunks,
54 CC BY 4.0 sources and one CC0 source. Five topic envelopes preserve the current
corrected gold: 45 cardiology, 49 diabetes, 44 oncology, ten outlier and ten ALS/FTD
cases. There are 129 answerable, 18 false-premise and 11 absent-fact cases.
All 158 requested IDs executed at both depths, with no missing or duplicate ID.
No query, answer, category or evidence set was changed to improve retrieval.

Production `retrieve()` uses local vector retrieval and the existing reranker;
BM25 and query rewriting are off. `main.py`, `llm_client.py`, the production
scorer and evaluation adapter are unchanged by this task. Inference and reranker
score consumption remain inside `asyncio.to_thread()`; deduplication retains
reranked source order. This is one snapshot, not a repeat-run stability estimate.

The [51-article / 148-query baseline](../v1/REPORT.md) and its raw/derived runs
remain historical evidence, unchanged. That baseline excluded ALS/FTD and used
older gold/category/scorer fingerprints (and a preserved diabetes snapshot).
Direct performance comparability with it is rejected; the different denominators
and the added source-conflict requirements cannot be treated as a retrieval gain
or loss. The table below compares only complete current-gold nested runs whose
compatibility is checked. The historical 19-article / 133-query headline and the
Docker seed demo are also separate.

[Pre-run review](PRE_RUN_REVIEW.md) records the scope decision, source/negative
boundaries, existing model-review basis and integration inspection. The merged
validation/correction records now cover ALS/FTD; freezing the current corrected
objects for this experiment does not imply fresh independent biomedical review.
Earlier preparation receipts remain historical. Current source verification,
all 17 ALS/FTD alternatives, and five reachability oracles are recorded in
[reachability.json](reachability.json), with current fingerprints.

## Compatible topic and nested-corpus results

Each cell shows complete answerable documents / complete pinned evidence.
Every topic baseline uses the same current queries, scorer, retrieval/model
fingerprints and flags as its 55-article run. Shared article tuples are identical.

| Topic / condition | Articles | Answerable | n3 documents / evidence | n8 documents / evidence |
| --- | ---: | ---: | ---: | ---: |
| cardiology / C1 | 19 | 38 | 25 / 2 | 31 / 5 |
| cardiology / C2 | 21 | 38 | 24 / 2 | 31 / 4 |
| cardiology / C3 | 55 | 38 | 24 / 2 | 30 / 4 |
| diabetes / C2 | 16 | 42 | 40 / 8 | 41 / 14 |
| diabetes / C3 | 55 | 42 | 40 / 8 | 41 / 13 |
| oncology / C2 | 14 | 34 | 31 / 7 | 32 / 15 |
| oncology / C3 | 55 | 34 | 30 / 7 | 31 / 14 |
| outliers / C1 | 5 | 6 | 6 / 2 | 6 / 2 |
| outliers / C3 | 55 | 6 | 6 / 2 | 6 / 2 |
| als-ftd / C1 | 4 | 9 | 7 / 1 | 8 / 4 |
| als-ftd / C3 | 55 | 9 | 7 / 1 | 7 / 4 |

Combined answerable results are 107/129 document sets and 20/129 evidence sets at
n3; 115/129 and 37/129 at n8. Full-set and feasible-only denominators are distinct:
at n3 28/129 answerable cases exceed the budget, so feasible-only evidence is
20/101. All 129 are structurally feasible at n8. False-premise correction evidence
is 1/18 at n3 (1/15 feasible-only) and 6/18 at n8. These are source-supported
correction passages, not judged premise corrections. The 11 absent-fact cases
remain unscored; original named-source/topic search scopes are preserved.

## Categories and evidence breadth

The category table includes correction-evidence cases but does not score absence
or answer correctness. Full-set denominators retain infeasible cases.

| Category | Cases | n3 document / evidence passes | n8 document / evidence passes |
| --- | ---: | ---: | ---: |
| cross_doc_distractor | 15 | 15 / 2 | 15 / 6 |
| cross_doc_synthesis | 17 | 6 / 0 | 9 / 0 |
| direct_lookup | 65 | 59 / 18 | 62 / 27 |
| false_premise | 18 | 15 / 1 | 17 / 6 |
| multi_hop | 29 | 25 / 0 | 27 / 3 |
| source_conflict | 3 | 2 / 0 | 2 / 1 |
| unanswerable | 11 | 0 / 0 | 0 / 0 |

No cross-document synthesis case has complete pinned evidence at either depth
(0/17); source retrieval alone is insufficient. The three accepted source-conflict
cases have 0/3 evidence at n3 and 1/3 at n8. The report does not narrow their
questions or remove a source reading to manufacture a pass.

| Topic | Accepted-source union n3 / n8 | Accepted-anchor union n3 / n8 | Mean fact recall n3 / n8 |
| --- | --- | --- | --- |
| cardiology | 18/19 / 18/19 | 16/77 / 21/77 | 12.28% / 18.42% |
| diabetes | 16/16 / 16/16 | 10/51 / 19/51 | 20.24% / 36.90% |
| oncology | 13/13 / 13/13 | 14/80 / 30/80 | 23.53% / 44.12% |
| outliers | 5/5 / 5/5 | 4/14 / 5/14 | 33.33% / 33.33% |
| als-ftd | 4/4 / 4/4 | 6/19 / 10/19 | 27.78% / 55.56% |

Unions count a source/anchor only in a case that accepts it. They include optional
alternatives and are breadth diagnostics, not per-case completeness. Full
per-topic/category/answerability summaries, minimum-chunk groups, missed-source/
anchor lists, context changes, named-decoy ordering and new-source exposures are
in [analysis.json](analysis.json). Named-decoy ordering passes 14/15 cases at both
depths; absent decoy exposure is not proof of rejection.

## Failures and representative saved-context inspection

These findings compare the new compatible topic baselines with the new combined
runs, not the historical 51/148 run. Every metric-changing case is reviewed;
a005 and the three accepted conflicts are additional failure controls.

| Case | Verified finding and limit |
| --- | --- |
| q051 | The Gao CCTA source disappears at both depths. Combined contexts include AF trial/calibration and Buea diabetes sample-size material. The topic baseline already lacked complete pinned evidence; unchanged evidence failure must not conceal the new required-source loss. |
| c004 | Both TAILORED-AF/review sources now fit n3, improving document coverage, but the review numerical passage is still absent. Evidence remains incomplete at n3/n8. |
| q006 | n8 loses the complete GQD bias span while retaining the right paper and generic bias/concealment prose. Exact evidence and fact recall fall; the upstream candidate mechanism is unmeasured. |
| o029 | Hunan disappears at both depths, displaced in the returned set by CKD, GQD and HFpEF methodology material. These cannot supply Hunan's DFS/OS and analysis-label facts. |
| o004 | n8 loses complete primary/table evidence. Table 6 still shows 23 new troponin rises / 11 myocarditis, monitoring criteria remain, and Discussion retains 14.7% myocarditis / no grade-3 cardiac events. This is a conservative whole-span loss with substantive evidence retained, not proof of a wrong generated answer. |
| x006 | The explicit independent-validation-limit anchor disappears at both depths. Rank 0 still calls ADNI/OASIS-3 validation a next step and identifies OASIS-derived training data. The pinned correction fails; useful premise-rejection prose is not relabelled as a judged correct answer. |
| a008 | Its four-article n8 baseline returns both required papers but incomplete evidence. In the 55-article run both required sources disappear; TB MR/review, lung liquid-biopsy and diabetes bibliography/methods passages appear instead. Document coverage falls and evidence remains fail. This is substantive cross-topic intrusion, not an answer-quality judgment. |
| a005 | Both baseline and combined runs lack the required DNA-editing source. The combined n8 set contains only Liu Cas13d passages, including mechanisms/therapeutic prose, without the complete requested RNA-versus-DNA endpoint/limit synthesis. This is an existing source/evidence failure, not a newly attributed corpus regression. |
| c012 | Both depths fail the accepted two-reading/design contract: the renal abstract anchor matches but Table 2, complete infection/confounding passages and the HFpEF evidence are missing. The original question and attributed-reading requirements remain intact. |
| c013 | n3 covers the abstract reading but not Methods. At n8 the NADAC Methods passage at rank 7 completes both readings, so evidence passes. No generated explanation of the price discrepancy is judged. |
| x005 | The right Alzheimer paper is returned, but neither complete required conflict reading matches at either depth. Both failures remain valid; the ANN/MRI question is unchanged. |

Outlier exposure now occurs for c003 at n8 (Alzheimer ANN/MRI source) and a008 at
both depths (TB MR, plus TB review at n8). c003's metric verdicts do not change;
a008 loses required-source coverage at n8. No added ALS/FTD source appears in the
other four topics' returned contexts. Low/no exposure does not establish
resistance to interference. No pre-rerank candidate trace was recorded, so
candidate displacement is a hypothesis, not a demonstrated mechanism.

The [durable source-conflict report](../../../docs/evaluation/source-conflicts.md)
contains exact questions, article roles, source locations, current gold contracts,
historical/current retrieval tables and unmeasured answer limits for 21 cases.
A [retained summary](../../../docs/evaluation/combined-benchmark-v2.json) embeds
source identities, case/run/query/configuration fingerprints and measured results
so the report can survive release selection without bulk experiment artifacts.

## Verification, resources, cost and remaining work

All 224 offline regressions pass, including nine new corruption/copy-hash checks and two frozen-envelope checks.
All 55 PDF/text pairs and accepted anchor offsets match pinned source bytes;
ALS/FTD XML metadata was reacquired and hash-checked because those ignored local
files were missing. Attribution/eligibility joins cover all 55 articles.
Unlimited-chunk reachability passes for all 147 evidence-bearing cases; n3 has
116 feasible and 31 infeasible cases, while all 147 fit n8. Reachability is a
structural ceiling, not a quality score.

There are 722 local production retrieval calls: 316 combined, 406 across six
complete nested baselines. No successful case was iteratively rerun or tuned.
The 55-article store reuses 3,350 historical production embeddings and adds 288
ALS/FTD embeddings. Baseline stores copy only their verified condition membership;
the ALS/FTD-only store embeds its 288 chunks. There are 576 newly embedded chunks
in total and 134 per-article filtered vector probes across seven stores. Existing
source files, caches and the original store are preserved. `SEED_ON_EMPTY=false`
is recorded in every receipt; exact stored chunk multiplicities exclude extra,
duplicate or stale seed sources. Copied vectors are float-hash checked against
the parent and every retained store has a full embedding digest. Original vectors
inherit the original ingestion/model provenance and were not recomputed.

Model-file fingerprints and actual dependency versions are recorded in each run;
current receipt/query/condition/selection/scorer/retrieval/feasibility fingerprints
are rechecked. Every saved context is an exact production chunk, all metrics and
summaries are recomputed, complete nested comparisons pass, and rebuilding the
frozen envelopes/dependency metadata plus saved-context analysis is byte-identical.
Fresh ingestion/inference can produce new IDs/timestamps and approximate-index
variation; this deterministic verification reproduces the saved experiment,
not a claim of identical results from every fresh run.

Provider calls: **0**. Paid evaluation cost incurred: **$0**. There was no
rewriting, generation, judge call, extra model-review session or HTTP service.
No corpus PDFs/full texts, secrets or disposable execution transcripts are
committed. Downloaded source metadata checks do not incur model-provider charges.

At initial delivery, required CI was pending during an active GitHub Actions
incident. The status check showed the earlier major outage had become degraded
performance, with the incident still investigating; no affected job was retried.
Current hosted-check and review readiness is recorded on the delivery PR.
Required hosted checks and the normal review/merge procedure remain gates. The
release-retention review must retain the source-conflict report, its README link,
and minimal provenance, and decide which bulk envelopes/runs/helpers enter main.
This task does not prune the epic or open its final integration PR. No PR is merged.

Retrieval failures remain findings for later diagnostics. Semantic sufficiency,
answer/refusal/correction accuracy, generated conflict handling, other retrieval
flags and independent clinical review remain unmeasured. A paid follow-up requires
explicit run approval with purpose/provider/scale/cost; none is needed for this
completed local retrieval evidence.
