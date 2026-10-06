# Corrected-gold five-topic evaluation scope

The evaluation freezes the current gold from the merged correction ledger into
five comparison envelopes: 55 unique articles, 158 cases (45 cardiology,
49 diabetes, 44 oncology, ten outliers, ten ALS/FTD). The envelopes preserve
complete query objects and anchors byte-for-byte as canonical objects. No
question, expected answer, category, alternative or conflict contract is changed
by this evaluation. In particular c012/c013/x005 retain their original questions
and require both attributed source readings.

The historical 51/148 release remains immutable. Its diabetes evaluated snapshot
and earlier category/scorer fingerprints differ from the current release. Its
results are historical evidence, not corrected-gold executions. New nested
conditions use identical current per-query hashes and scoring code. The
cardiology C1/C2 pair remains 19/21 articles; other topic baselines contain
16 diabetes, 14 oncology, five outlier and four ALS/FTD articles.

## Review basis and boundaries

The retained gold-validation findings cover all 158 cases and the correction
ledger records the 13 accepted revisions. Those merged records supersede the
old ALS/FTD preparation handoff; the new envelopes freeze those corrected inputs
for this evaluation. The review is source-grounded model review with correlated
author/reviewer risk, not biomedical expert certification or a new independent
158-case review. No additional model-review session was launched.

The earlier four-topic integration review and outlier/ALS-FTD relationship audit
remain historical source-review evidence. Current dependency metadata is rebuilt
from actual query/evidence bindings and all 55 article identities. Broad overlap
dependencies are deliberately conservative. Negative search scopes retain their
original meaning rather than becoming unsupported assertions about all 55 papers.

Before evaluating, the integration inspection rechecked every ALS/FTD question,
all absent/false-premise question scopes, and candidate passages selected by
C9ORF72/FTD/ALS, metformin, diabetes, Alzheimer, cancer, HIF/zinc, tuberculosis,
and wastewater terms in the added and prior texts. The four added studies have
specific tissue, cell, zebrafish, mouse and individual-case endpoints. The
metformin discussion in Parameswaran (Discussion, extracted lines 596–602) cites
preclinical BAC-mouse work; LeBlanc's treatment discussion (lines 383–399)
describes therapies in development. Neither supplies SIZE-DM follow-up, clinical
DKD zinc dosing, GQD trial brands, or outcomes in the named diabetes trials.
LeBlanc's SPECT/genetics account (lines 190–208) contrasts an Alzheimer-pattern
interpretation with C9ORF72-confirmed FTD-ALS; it does not independently validate
the outlier ANN's ADNI/OASIS-3 claims. No C9ORF72/Cas13d/poly-GA candidate was
located in the prior 51 texts by that scan. These scans filter candidates and
are not proofs of semantic absence. No new complete cross-topic alternative or
formerly absent scoped outcome was identified; no post-run evidence relaxation
is authorized. Unlisted paraphrases remain a conservative-scoring limitation.

## Execution and resource selection

All 158 combined IDs are selected because four added articles can affect global
rankings and this deliverable makes complete benchmark claims. Existing saved
runs cannot be treated as compatible current-gold baselines: changed questions
require fresh retrieval, and the scorer fingerprint changed. Complete current
nested runs establish compatibility without editing or relabelling historical
results. This is one vector-only configuration with production reranking,
BM25 off, rewriting off, and n=3/n=8. There is no iterative tuning or flag sweep.
The complete combined and six baseline runs require 722 local retrieval calls
(316 combined; 406 baseline). No separate regression-sample rerun is needed.

The original 51-article isolated store is verified against its historical receipt,
source tuples, exact chunk multiplicities, loaded model files, dependency versions
and unchanged production embedding code. Fresh stores copy the selected original
vectors with byte-equivalent float hashes. Only missing articles are ingested
through production `main.ingest` / `embed` / `chunk_text`; the 55-article union
adds 288 chunks to the 3,350 retained chunks. `SEED_ON_EMPTY=false` is mandatory.
Each new store records a filtered vector query for every source, proving index
queryability without claiming unfiltered QA success. Copied-vector provenance is
inherited; original embeddings are not recomputed. Original stores/runs are not
reset or replaced. No downloaded PDF/full text is committed.

Paid rewriting, generation and judging are omitted. No external evaluation run
needs approval in this local-only scope. There are zero generated answers,
refusal judgments or conflict-resolution judgments. Retrieval evidence coverage
must not be reported as answer accuracy or clinical conflict adjudication.
