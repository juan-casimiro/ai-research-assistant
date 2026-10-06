# Current benchmark case index

Browse all **158 questions across 55 articles** in the combined v2 benchmark.
Each case links the question and expected response to its required/alternative
articles, accepted passage sets and recorded distractors. Article links open
the pinned public PMC version; passage locations refer to physical PDF pages.

| Topic | Questions |
| --- | ---: |
| [Cardiology](cardiology.md) | 45 |
| [Diabetes](diabetes.md) | 49 |
| [Oncology](oncology.md) | 44 |
| [Outliers](outliers.md) | 10 |
| [Als-Ftd](als-ftd.md) | 10 |

## Case categories

| Category | Questions |
| --- | ---: |
| cross_doc_distractor | 15 |
| cross_doc_synthesis | 17 |
| direct_lookup | 65 |
| false_premise | 18 |
| multi_hop | 29 |
| source_conflict | 3 |
| unanswerable | 11 |

## How to review a case

1. Read the question, category and expected response.
2. Follow the article links and inspect the named PDF sections/pages.
3. Check required claims against each complete accepted evidence set.
4. For distractors, read the recorded similarity and why the source is inapplicable.
5. Preserve attributed conflicts and scope distinctions; do not invent a reconciliation.

Expected answers are LLM-authored and reviewed against the articles. They can
be imperfect; corrections belong in the authoritative benchmark inputs.
This index does not generate responses, judge answers or change gold.

[Article catalogue](articles.md) · [Benchmark guide](../README.md) ·
[Source-conflict examples](../../docs/evaluation/source-conflicts.md)

## Regenerate

From the repository root:

```sh
python render_case_index.py
python render_case_index.py --check
```

These pages are generated from `benchmark/combined/v2/manifest.json`, the five
topic query files and `case_dependencies.json`. The check fails if the pages
are stale or question/article/evidence joins are broken. It uses no models,
network access or downloaded corpus files. Detailed qualifiers, rubric rules
and exact excerpts remain in the linked authoritative query files.
