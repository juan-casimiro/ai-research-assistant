# JUA-112 verification and pending evaluation

Review candidate, 2026-10-02. The legacy five-paper/42-case oncology set has been
audited into a 14-paper/42-case release. Article and query fingerprints are bound
in the manifest, conditions and dependency files. Historical document-only scores
are not comparable to this revised evidence benchmark.

## Completed verification

- All 14 PDFs: provider MD5 and byte count, local SHA-256, matching identifiers,
  CC BY 4.0 notice, caption/credit inventory, page extraction and representative visuals.
- Offline release verification: complete selected metadata, archived receipts,
  pinned article XML, PDF/text identity, exact anchors, C1 answer-source union,
  nested C1/C2 membership and unchanged original global files.
- Fault checks: a changed metadata archive was rejected; altered questions without
  matching reviewed condition linkage were rejected. Checks used temporary copies.
- Required offline regressions: **161 tests passed**.
- Production-chunker reachability: all **39 evidence-bearing cases** are reachable
  with their exact fact-bound gold. The three absent-fact cases deliberately have no
  invented evidence sets. [C1](results/offline-C1.json) and
  [C2](results/offline-C2.json) preserve complete oracle output and provenance.

At n=3, 31/39 evidence cases can fit all required evidence; eight cannot:
o004, o013, o016, o017, o018, q081, o029 and o030. At n=8 all 39 can fit.
These are evidence-budget feasibility ceilings, **not retrieval success rates**.
Twenty-one pinned spans require adjacent production chunks in C2. The scorer accounts
for that adjacency; changing gold merely to improve a score would invalidate the
comparison. Fact recall and complete evidence coverage must be reported separately.

No retrieval, collection ingestion or paid evaluation call was performed.
Claude reviewer inference was separately requested by Juan. Source review
is author verification, not independent clinical peer review. Independent PR review
and benchmark freeze are pending under the shared authoring standards.

## Interpretation and source defects

The selection preserves different disease stages, genomic drivers, treatment
strategies and endpoint definitions. It includes actual TNBC treatment evidence,
instead of relying on the old breast-labelled NSCLC filename. o030 joins treatment
outcomes to reflex-testing barriers without claiming the consensus measured the
cohort's testing implementation. o024 separates adjuvant osimertinib OS from advanced
afatinib mTTF; o025 separates MRD assay performance from ICD danger-signal mechanisms.

Cardio-oncology evidence supplies observational CV events, RCT cardiac adverse
events, TNBC myocarditis with intensive surveillance, and older-PD-1-cohort
cause-specific death. None is interchangeable with general cardiac treatment
effects. A null comparative CVD-mortality estimate between two PD-1 drugs does not
show no ICI cardiovascular risk. The observational meta-analysis uses only four
studies in its HR analysis despite including 12 overall, and has substantial
heterogeneity; its estimate is not a causal treatment-effect claim.

[case_review.json](case_review.json) records the stage III MPR conflict, reversed
afatinib dose shares, differing TNBC discontinuation denominators, screening flow
chart discrepancies. Explicitly
attributed source conflicts are valid responses; silently correcting them is not.
Clinical-trial citation claims in the ICD mini-review were not adopted as clinical
efficacy gold. Its authored cases are scoped to reported mechanistic pathways.

## Planned targeted runs after review/freeze

The initial focused IDs are **o029,o023,o026,o027,o030,o024,o025,o002,o003,o004,
o005,o006,o011,o012,o017,o018,o019,o020,o021**. They exercise changed treatment
sources, response-versus-survival, implementation synthesis, conflicts and
denominators, named competitors, mortality overlap and scoped absence. Check every
requested ID exists; a partial CLI match is not complete requested coverage.

Run local vector-only and vector-plus-BM25 retrieval at n=3/n=8, with fixed gold
and isolated collections for C1 and C2. Use explicit immutable result paths, record
source/model/chunker/scorer hashes and collection identities, and inspect retrieved
evidence failures manually. Focused outputs support iteration; a complete baseline
claim requires all 42 declared cases. Preserve every relevant result before reruns.
Report regressions and unchanged results as well as improvements. For the absence
cases distinguish retrieval behaviour from manually validated correct refusal;
source recall alone cannot establish answer correctness.

A small cardiology regression sample is q044,q050,q058,q065: score/endpoint
disambiguation, same-model competing documents, diabetes interaction and subgroup
scope. The reviewed JUA-111 release is now merged into the epic at 2dcbfcc; use its
versioned diabetes dependency map for the planned regression sample. Those sources
are not silently imported into the oncology-only conditions here. Cross-topic
condition membership and whole-corpus negative checks belong to JUA-114. Do not
reuse or mutate another task's active collection to run these samples.

Paid rewrite/generation/judge runs require a separately approved run specification;
general task authorization does not approve them. The four configurations are not
run automatically. Retrieval results, interference/failure analysis and topic
regressions remain outstanding, so JUA-112 is not complete.

## Independent review corrections

[REVIEW.md](REVIEW.md) records confirmed Claude findings, corrections and qualified
responses. The initial draft is preserved at commit 8b1adbe. No retrieval results
were used to change gold; selection and queries remain unfrozen for re-review.
