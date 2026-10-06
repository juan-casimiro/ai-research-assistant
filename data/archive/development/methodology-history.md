# Methodology history after the original V1 benchmark

These records describe the versioned topic rebuilds and later combined
experiments. The original 19-article / 133-question [V1 methodology](../v1/methodology.md)
is archived separately. Use [ADR-002](../../../adr/002-evaluation-methodology.md),
the [current benchmark guide](../../benchmark/README.md) and [findings](../../findings/retrieval.md)
for the current strategy, inputs and measured results. Historical statements
retain the scope and limitations of the experiment they describe.

## Versioned cardiology benchmark rebuild

[Corpus and benchmark standards v1](../../../docs/benchmark-standards.md) governs the corpus and benchmark expansion.
The versioned scorer supports the separate [45-case cardiology query release](../../benchmark/sources/cardiology/v1/BENCHMARK.md),
with reviewed and frozen inputs for recorded experiments. The historical
[V1 schema/scoring](../v1/methodology.md) remains unchanged for `data/archive/v1/golden_qa.json`; it is not a measure
of passage sufficiency or answer correctness.

In versioned mode, `tools/evaluation/eval_golden.py` still calls production `retrieve()` and records
reranked chunks/sources at depths 3 and 8. Document coverage, conservative pinned
excerpt coverage, fact recall and competitor ordering are distinct. Complete
alternatives use OR; each set requires all its anchors. An excerpt spanning chunks
requires every whole chunk in a contiguous production window certified against
its pinned source offsets, regardless of retrieval rank. The offline oracle
checks unlimited coverage and minimum complete-evidence chunk budgets. V3
reports full-set and feasible-only coverage at each depth, with structural
ceilings and infeasible IDs; document coverage and partial fact recall retain
all scored cases. All 42 evidence-bearing cases fit at n=8, but only 30 fit at
n=3 (27/38 answerable and 3/4 false-premise correction cases). These are
structural assertions, not retrieval-quality results. Absent facts are unscored;
false-premise correction evidence is reported separately from judging generated
corrections. Exact matching cannot exclude valid paraphrases, so failures require
context inspection. The separate generated-answer evaluation follow-up retains separately sequenced answer-judge work.

`tools/evaluation/compare_evals.py` now rejects changed queries/revisions, scorer/retrieval/corpus
fingerprints, depths, changed/missing feasibility and incomplete executed-ID sets.
Explicit nested comparisons
hold retrieval flags fixed and preserve common article tuples. Historical pairs
require `--allow-legacy`, are labelled unverifiable and cannot be mixed with the
new release. This prevents a repaired reference or changed corpus from appearing
as an improvement to the old benchmark. No new quality results are claimed.

## Diabetes expansion and frozen cardiology interference

The diabetes audit adds the [versioned diabetes release](../../benchmark/sources/diabetes/v1/README.md):
16 topic/overlap sources, 49 cases and 55 pinned anchors, with the original
21-article cardiology selection extended by 11 verified permissive articles.
Legacy sources/cases are audited and migrated explicitly; new cohorts cannot
inherit retired numerical gold. Four absent-fact cases are scoped to selected
main PDFs; three false-premise cases require affirmative correction evidence.
A generic HIF question accepts either complete review evidence set.

The diabetes pair compares 16 with 32 articles. The frozen cardiology pair
compares 21 with 32 using the exact original questions and anchors inside a
common extended selection envelope. A fresh 21-article baseline is required
because historical results have incompatible selection/envelope fingerprints.
No historical output is relabelled. Only local vector retrieval and production
reranking are run; complete final coverage is justified by corpus expansion,
with no four-configuration sweep or paid calls. See the release report for
source-aware context review, feasibility ceilings and evidence limitations.

## Combined-corpus evaluation

We evaluate whether adding articles from other topics changes retrieval quality.
Comparisons use the same questions, scoring rules, system settings and versions
of shared articles so that differences can be attributed to the corpus change.

We report finding the right articles separately from finding the evidence needed
to answer. Answer correctness requires a separate evaluation.

The [combined report](combined-v1/REPORT.md) records the historical
four-topic experiment's corpus, results and limitations. Its results remain
separate from the original benchmark and Docker demo.

## Corrected five-topic snapshot

The [corrected combined report](../../findings/retrieval.md) freezes the
current model-reviewed gold and accepted correction ledger for all 158 cases in
a 55-article / 3,638-chunk corpus, including ALS/FTD. Its canonical source query
objects and anchors are preserved; the comparison envelope, conditions and
dependency map receive new fingerprints. The original 51/148 runs remain
historical. Changed questions, categories, scorer fingerprint and corpus prevent
a direct historical performance comparison, despite an unchanged scorer version
label. New complete nested runs pass the existing compatibility guard.

One local vector-only configuration with production reranking evaluates every
case at n3/n8 and six complete topic baselines (722 retrieval calls, zero paid
provider calls). Existing production embeddings are reused only after checking
the original model/dependency/code/source/chunk provenance; new source chunks
use production ingestion. Fresh stores disable seeding, verify exact source/chunk
multiplicities, hash copied and final vectors, and record per-source filtered
query probes. Those probes prove queryability, not unfiltered QA success.

Saved contexts, metrics, summaries, gold and all provenance joins are independently
recomputed. Offline replay reproduces envelopes/dependency metadata and analysis;
fresh approximate-index inference is not promised to be byte-identical. At n8,
answerable document coverage is 115/129 and pinned evidence 37/129; correction
evidence is 6/18 and eleven absent-fact cases are unscored. c012/c013/x005 retain
both attributed readings, with valid failures preserved. No answer/refusal or
conflict-handling accuracy is inferred from retrieval. The durable
[source-conflict report](../../findings/source-conflicts.md) and
[minimal provenance summary](../../findings/combined-benchmark-v2.json) are
intended for retention independently of bulk experiment files. Biomedical expert
review, semantic adjudication and answer judging remain separate limitations.
