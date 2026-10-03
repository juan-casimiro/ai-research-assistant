# Topic outliers v1

This release selects five CC BY 4.0 articles with verified PMC version 1
identities, supported PMC Cloud PDF retrieval, readable PDFs, and pinned PDF/text
hashes. It restores three deliberately different evidence families: two
environmental AMR/wastewater papers, two microbiome/tuberculosis papers, and
one cognitive AI paper. The cognition family has only one primary paper, so
topic breadth is not evidence of a deep source cluster. Selection and
exclusions are recorded in `manifest.json`, `candidate_log.json`, and
`ATTRIBUTION.md`; source metadata responses are archived under `metadata/`.
PDFs and extracted full text are local ignored corpus files and must not be
committed.

The former Galápagos AMR article is excluded because its CC BY-NC-ND licence is
outside the new-corpus policy. The GPT-5/tau217 paper's no-PMCID and restrictive
licence exclusion is owned by JUA-108. The Alzheimer replacement is a different
study and does not reproduce its plasma-tau or physician-comparison evidence.
Other rejected and deferred candidates include their failed eligibility gates
in `candidate_log.json`.

`queries.json` contains ten authored cases: a source-conflict multi-hop case,
four direct lookups, one cross-document distractor, three false-premise cases, and one absent-fact case. The
questions distinguish association from intervention, prediction from clinical
performance, and environmental ARG measurements from patient infections.
`topic_relationships.json` maps adjacent vocabulary to frozen cardiology,
diabetes, and oncology cases. `migration.json` records legacy IDs and avoids
claiming score equivalence. `case_review.json` describes focused full-text and
cross-topic checks. Search strings in the old candidate record were not
independently preserved as exact database syntax and are labelled accordingly.

[The supplementary ALS/FTD audit](als-ftd-audit-v1/README.md) reviews all five
outliers and ten cases against the four later ALS/FTD sources. The relationship,
dependency and review records link its evidence-grounded decisions. Queries,
evidence and frozen experiment membership remain unchanged; integrated review
and retrieval verification are handed off explicitly to JUA-114.

The outlier-only condition has five articles. C1, C2, and C3 therefore share
membership here and should be evaluated once; the broader cross-topic C3
condition is deferred to JUA-114. This release's absent-fact check covers all
five outlier articles only. It does not establish absence across the integrated
cardiology, diabetes, and oncology corpus.

## Focused topic regression

`regression/` copies 18 frozen existing-topic cases (six per topic) and their
anchors unchanged. Its C1 corpus is the 46-article cardiology/diabetes/oncology
union; C2 adds these five outliers (51 total). This is a focused interference
sample, not a complete topic benchmark. Unanswerable oncology case q083 is
reported but not scored by evidence reachability.

## Reproduction and verification

From the repository root, after the five ignored PDFs/texts and existing topic
corpora are available:

```sh
.venv/bin/python verify_benchmark_reachability.py --benchmark benchmark/outliers/v1 --corpus-dir corpus/outliers-v1 --condition C1
.venv/bin/python benchmark/outliers/v1/runs/build_topic_regression.py
.venv/bin/python benchmark/outliers/v1/runs/prepare_regression_corpus.py
.venv/bin/python verify_benchmark_reachability.py --benchmark benchmark/outliers/v1/regression --corpus-dir corpus/outliers-v1/topic-regression --condition C1
.venv/bin/python verify_benchmark_reachability.py --benchmark benchmark/outliers/v1/regression --corpus-dir corpus/outliers-v1/topic-regression --condition C2
.venv/bin/python -m unittest discover -v
```

The saved vector-only retrieval artifacts are under `runs/`. They call the
production `retrieve()` path with reranking, but do not run answer generation,
query rewriting, BM25, or an answer judge. Read `REPORT.md` for observed scores,
limits, and exact run records. Document/evidence retrieval metrics are not
answer correctness or refusal accuracy. Complete combined-corpus absence review
and full topic evaluation remain JUA-114 work.
