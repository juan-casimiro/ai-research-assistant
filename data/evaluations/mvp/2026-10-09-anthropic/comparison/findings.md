# Strategy findings — one observed MVP sweep

The four saved 9 October 2026 runs pass the offline compatibility checks:
158 unique requested/executed queries, matching query and manifest hashes,
complete metrics at depths 3 and 8. Each strategy below is paired with baseline.
The [category summary](summary.md), [per-query changes](per_query.csv) retain the full accounting; the four source
result files retain configuration and model provenance.

At depth 3, BM25 and BM25 plus rewriting each add three excerpt successes
(21 to 24 of 147), with no excerpt regressions. Rewriting alone leaves all
147 excerpt verdicts unchanged and lowers mean fact recall by 0.23 percentage
points. Document coverage rises by two queries for BM25 and rewriting alone,
and by three for the combined run, but every experiment loses one synthesis
source-coverage success. Source presence and complete evidence remain distinct.

At depth 8, the observed overall changes are:

| Strategy | Document coverage delta | Excerpt coverage delta | Mean fact recall delta | Excerpt improved / regressed / unchanged |
| --- | ---: | ---: | ---: | ---: |
| BM25 | +2.04 pp | +3.40 pp | +3.85 pp | 8 / 3 / 136 |
| Rewriting | −2.72 pp | +2.04 pp | +2.15 pp | 5 / 2 / 140 |
| BM25 + rewriting | +2.04 pp | +4.76 pp | +4.08 pp | 8 / 1 / 138 |

All three positive metrics above use 147 paired scored queries; 11 absent-fact
queries are excluded. Distractor ordering is unchanged for all 15 scored
queries at both depths (14 pass); the other 143 queries are excluded from that
metric, not counted as unchanged.

The category findings explain the modest overall gains:

- **Direct lookup (65 queries):** at depth 8, both BM25 configurations raise
  excerpt coverage from 27/65 to 34/65, seven gains with no regressions.
  Rewriting alone reaches 31/65, with five gains and one loss. This category
  accounts for seven of eight excerpt gains in each BM25 configuration.
- **Multi-hop (29):** complete excerpt coverage stays 0/29 at depth 3 and
  3/29 at depth 8 in every run. BM25 reaches 29/29 document coverage at depth
  8 without improving complete evidence; its q042 partial-fact gain is offset
  by q080's loss. Rewriting alone loses partial fact support for q012.
- **Cross-document synthesis (17):** no complete excerpt success at either
  depth in any run. At depth 8 the combined run retrieves the required sources
  for 10/17 versus baseline's 9/17, yet mean fact recall falls from 14.71% to
  8.82%, with q014 and q025 losing partial support. Rewriting alone reduces
  document coverage to 7/17. Source gains do not resolve this evidence gap.
- **False premise (18):** at depth 8, BM25 swaps one excerpt gain (q057) for
  one loss (q115), preserving 6/18. The combined run keeps q115 and adds q057,
  reaching 7/18. Rewriting alone leaves the excerpt verdicts unchanged.
  These scores concern correction evidence, not successful premise correction.
- **Cross-document distractor (15):** source coverage and distractor ordering
  are unchanged. Both BM25 runs lose excerpt support for q138 at depth 8
  (6/15 to 5/15); rewriting alone preserves baseline excerpt coverage.
- **Source conflict (3):** BM25 and rewriting alone lose complete excerpt
  support for q023 at depth 8 (1/3 to 0/3), retaining two of its three facts.
  The combined run preserves baseline's 1/3. These very small denominators
  make percentage changes look large; they do not establish a general effect.
- **Unanswerable (11):** every positive metric is unscored; no refusal-quality
  conclusion follows from this comparison.

The combined run has the highest observed depth-8 excerpt coverage (50/147)
and mean fact recall (39.46%), but the advantage over BM25 alone is small and
category-dependent. This is one sweep per configuration, with independent
rewrites by depth and configuration, so it cannot establish a stable ranking,
statistical significance or attribute the combined differences solely to BM25.
Pinned-excerpt misses can retain semantic support. No generated answers were
judged, no provider logs were read, and no new evaluations were run. These current scores
are not directly comparable to the historical V1 benchmark.
