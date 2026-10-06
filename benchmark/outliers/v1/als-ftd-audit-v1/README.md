# ALS/FTD overlap and absence audit

This supplementary author review compares all five frozen outlier articles and
all ten cases against the four selected ALS/FTD articles. `audit.json` records
all 20 article pairs, source-bound extracted spans, case decisions and the
integrated evaluation handoff. The exact PDF/text bytes and six frozen
manifest/query/condition inputs are pinned. It is an audit revision, not a new
query or corpus release; no accepted anchors, alternatives, named decoys,
questions, rubrics or experiment membership changed.

The strongest substantive bridge is the Alzheimer ANN/MRI paper versus the
clinical FTD-ALS case: SPECT suggested Alzheimer disease, whereas genetic testing
and subsequent pathology supported FTD-ALS. This motivates related competition
for x005/x006/x010 and a007/a008/a009, without making either study alternative
evidence for the other. Parameswaran's Alzheimer Research Center is tissue-bank
provenance; Sachdev's Alzheimer funding acknowledgment is incidental. Neither is
Alzheimer AI validation. Genetics and translational vocabulary bridge the TB
papers to C9orf72 studies, but MR instruments, patient-derived neurons, mouse
interventions and clinical diagnosis have different endpoints and evidence roles.
Metformin discussion is secondary mouse evidence or future therapeutic
development, not an established human treatment or a TB microbiome trial.
Environmental ARG papers remain distant, with generic PCR/sequencing overlap.
These are plausible confusions, not observed retrieval interference.

All ten existing cases are retained. In particular:

- x002 still rejects an administered probiotic dose in the named MR study.
- x006 still rejects independent ADNI/OASIS-3 validation of the Alzheimer models.
- x008 still rejects established AI-assisted TB-care superiority.
- x009 still lacks a wastewater-linked antibiotic-resistant patient infection
  count. Aspiration pneumonia in the FTD-ALS case is a different outcome with no
  sampled-plant linkage. Its frozen question explicitly asks about five outlier
  articles, so that scope remains unchanged. Reviewing four additional papers
  does not establish absence across the complete integrated corpus.

The relationship map now includes ALS/FTD roles and case links. Pair-level
ALS/FTD links list answer-source cases; existing named-decoy roles, including
PMC11527445 for a009, are recorded separately in `external_article_roles`. The dependency
and case-review files point to this supplementary record; their original frozen
dependencies remain available for reproducing historical runs. No material gap
required a new case or a semantic query revision. Existing ALS/FTD cases already
exercise diagnostic discordance and human/cell/animal distinctions.

## Verification

Acquire and extract the pinned ignored ALS/FTD sources using the durable
[ALS/FTD release reproduction instructions](../../../als-ftd/v1/README.md#reproduce);
the manifest records download routes and source hashes. Reuse verified local
bytes when available. Outlier acquisition is documented in the parent release.
With those PDFs/texts available, run from the repository root:

```sh
.venv/bin/python benchmark/outliers/v1/als-ftd-audit-v1/verify.py --als-ftd-corpus <local-als-ftd-source-directory> --corruption-checks
.venv/bin/python -m unittest discover -v
```

`verification.json` preserves the mechanical audit receipt and offline regression
result. Verification checks all nine PDF/text pairs, span offsets/hashes, the six
unchanged inputs and complete pair/case coverage. It also cross-checks source/decoy
roles, case dependencies and relationship links.
The six corruption probes run reproducibly with `--corruption-checks` in temporary
fixtures. Neither source-offset checks nor pair coverage certify that an excerpt
scientifically supports a rationale; that remains a manual review responsibility.
No models, collection ingestion, retrieval, rewriting, generation or paid judge
were run for this audit: the executable benchmark did
not change. Historical outlier and 18-case regression results remain historical
conditions that did not contain ALS/FTD.

## Integrated evaluation handoff

The current combined evaluation records model review, corrected-gold freeze and
full 158-case results. The historical scope-selection rationale was to recheck alternatives
and negative scope against actual integrated membership, and run isolated nested
comparisons with compatible fingerprints. `audit.json` selects 20 affected IDs
and explains their roles. Retain the original 18-topic sample for comparison;
supplement it with justified ALS/FTD-sensitive cases after the combined review.
The 20-case set covers both small audited strands, including x009’s negative
dependencies on all five outliers and the ALS/FTD model/assay controls. Complete
final claims require full declared coverage. Record whether competing sources actually
enter retrieved contexts; unchanged scores without competitor exposure cannot
establish resistance to interference. Refusal correctness requires separate
answer review, and paid calls require explicit approval.

## Review revisions

Revision 2 addresses Claude’s software/records review: assay-specific and
clinical outcome spans replace weak supporting excerpts; duplicate span links
are removed; x009 is linked to every article pair; MR/clinical/mechanistic role
wording is made source-specific; a009’s existing named decoy is carried into
external roles; and the integrated handoff covers all 20 audited cases. The
verifier now checks these links and includes reproducible corruption probes.
Claude’s initial review found no material scientific or gold-evidence error,
but it is not domain-expert certification.

Claude’s focused follow-up confirmed all five review findings resolved and no
blocking defect. Its two minor residuals were addressed by replacing an irrelevant
metformin span in the cognition/PKR pair and documenting answer-source versus
named-decoy link scope. Mechanical checks were repeated after those edits.
