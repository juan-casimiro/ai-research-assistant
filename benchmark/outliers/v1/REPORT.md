# Outlier benchmark and focused regression report

## Corpus and cases

The frozen outlier set contains five selected articles (423 chunks): two
environmental AMR/wastewater sources, two microbiome/TB sources, and one
cognitive AI source. All five are pinned to deposit version 1 and their PDF and
extracted text hashes. Article-level attribution, permission/credit review,
candidate gates, case dependencies, evidence anchors, and legacy migration are
in the adjacent release files. Full source PDFs/text are ignored local corpus
artifacts and are not part of this commit.

The ten authored queries include nine evidence-scored cases and one absent-fact
case. The absent case asks for downstream patient infections linked to sampled
wastewater plants; the negative search covered all five selected outlier
articles, not the integrated multi-topic corpus. The TB Mendelian-randomization
case preserves a material abstract/Results discrepancy: the abstract reports
11 potential UK Biobank associations and three taxa validated in FinnGen; the
UK Results say associations no longer meet Bonferroni significance, while a
later section calls three taxa significant in both databases. Gold wording
attributes these statements to their source locations and does not resolve the
conflict. The genetic design is not a clinical intervention. Likewise, the
Alzheimer ANN and MRI CNN percentages describe distinct tasks and datasets and
are not clinical-performance estimates.

## Retrieval observations

Eight of nine answerable cases were structurally reachable at n=3 and all nine
were reachable at n=8 by the chunk-feasibility check; x001 needs four chunks.
One absent-fact case is intentionally not scored by evidence excerpt reachability. In the saved outlier C1 vector-only run, exact
pinned evidence coverage passed for 3/9 cases at both n=3 and n=8. Document
coverage passed for 8/9 at n=3 and 9/9 at n=8; for the single named-decoy case,
the answer source ranked ahead of the decoy when the decoy was present at n=8.
These are local retrieval diagnostics only. The scorer checks literal pinned
excerpt overlap and does not judge generated answers, clinical interpretation,
false-premise correction, or absent-fact refusal.

The frozen topic regression copies 18 existing cases, six each from cardiology,
diabetes, and oncology. Both conditions have all 36 source anchors reachable.
Structural evidence feasibility is identical for C1 and C2: 15/17 evidence
cases fit n=3 and 17/17 fit n=8; q083 is the existing unanswerable case and is
not scored. The retrieval runs compare the same questions and settings over 46
core articles (C1) and those same articles plus five outliers (C2). Consult the
immutable run files for per-query contexts and values; this report intentionally
does not infer topic-wide quality from the focused sample.

## Exact run scope

`runs/outliers-C1-vector-reviewed.json` is the final complete 10/10 vector-only retrieval run on
the five-article outlier corpus. It evaluated all ten cases at n=3 and n=8 using
the production retrieval path and reranker. The local embedding and reranker
weights, collection receipt, query/corpus/scorer fingerprints, retrieved
contexts, source order, and ingestion verification are recorded in the artifact's
provenance; no separate outlier ingestion receipt was retained. No
rewrite, BM25, generation, or paid judge was run.

`runs/topic-regression/C1-vector-final-v2.json` and
`runs/topic-regression/C2-vector-final-v2.json` are the complete
18/18 vector-only comparison; their ingestion receipts are
`runs/topic-regression/C1-ingestion.json` and `C2-ingestion.json`. C1 uses the 46-article topic union; C2 adds the
five outliers. Each condition uses its own isolated, separately ingested collection with identical
retrieval flags and immutable output. After the query fingerprint correction and x001 evidence-anchor update, all
three final evaluations were rerun against those unchanged corpus memberships. Compatibility validation passed. Across
the 17 evidence-scored cases, document coverage remained 15/17 at
both depths and exact evidence coverage remained 4/17 at n=3 and 6/17 at n=8;
there were no per-case metric flips. No outlier-source chunk appeared in the top 3 or top 8 for any of the 18 cases.
The unchanged scores therefore do not test outlier competition or support a
no-interference conclusion; they show only the core cases remained unchanged
when the outliers ranked below the retrieval cutoff. Failed setup attempts and earlier pre-final query snapshots were excluded from the release; only the complete final runs and verified comparison ingestion receipts are included.

The release's outlier-only C1/C2/C3 lists have identical membership, so only one
outlier-only retrieval run was made. The integrated C3 comparison and
corpus-wide recheck of absent-information cases belong to JUA-114. Run
`compare_evals.py --nested-corpus` validates the focused C1-to-C2 comparison.

## Fingerprint note

Each `queries.json` stores a non-self-referential `query_sha256` that excludes
its own field. `conditions.json`, `case_dependencies.json`, `case_review.json`,
and run provenance use the hash of the complete serialized query document.

## Verification limits

Topic regression is a 6-case-per-topic sample, not a complete topic evaluation.
Source-family breadth is uneven: the cognition family has one primary paper.
The legacy preserved search strings do not prove the exact original search
syntax. Author case review and read-only Claude CLI review are complete; Juan PR review
is pending. No clinical or other domain expert has reviewed these cases. Strict evidence retrieval rates are not answer correctness, and no
generated answer/refusal behavior was evaluated. Full integrated corpus review
and final cross-topic claims require JUA-114.
