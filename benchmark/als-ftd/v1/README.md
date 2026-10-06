# ALS/FTD selection and prepared evidence cases

This focused C9ORF72 strand adds four primary articles (2023–2024), 58 physical
PDF pages and ten prepared cases. It covers a human clinical case, human
postmortem tissue, patient-derived isogenic neurons, engineered cells, zebrafish
and BAC mice. It is an author-verified selection and a source authoring record.
Model review and corrected-gold integration are recorded in the current combined
benchmark; biomedical expert review remains absent. It is
not a comprehensive ALS/FTD review or a clinical treatment recommendation.

## Selection decisions

| Article | Evidence and corpus role | Reason to include |
| --- | --- | --- |
| [Liu et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC11527445.1/) | RNA-targeting intervention in cells and BAC mice | DPR reduction with variable transcript response; molecular target engagement differs from motor/survival benefit. |
| [Sachdev et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC11047104.1/) | DNA editing in patient-derived isogenic motor neurons | Exon 1A silencing, repeat excision and mutant-allele excision differ across DPR and functional endpoints. Most insight comes from one donor line. |
| [Parameswaran et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC10188109.1/) | Mechanistic/cell and zebrafish experiments plus human postmortem observations | Strand, model and time distinctions; postmortem phosphorylation increase differs from 38-day motor-neuron findings. |
| [LeBlanc et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC10802081.1/) | Single human clinical case | Imaging/genetic/pathological discordance; diagnostic evidence must remain distinct from laboratory intervention findings. |

No count target drove the selection. These papers give closely related terminology
with different evidence scopes. Each is an answer source for some cases and can
compete with others. Human-derived cells are not a treated human cohort. The
postmortem series is not a randomized clinical intervention. No clinical efficacy
estimate is inferred from the clinical case or from DPR lowering.

The summit review (PMC10630271) was excluded for CC BY-NC. The genetic ALS review
(PMC12010636) has only a text-mining/fair-use notice in the inspected deposit and
an unresolved PMC/PubMed title difference, so it was excluded too. See
[manifest.json](manifest.json) and [candidate_log.json](candidate_log.json).
No eligible standalone review was added; review statements and cited studies
within selected papers remain explicitly secondary evidence.

All selected articles have a current sole PMC deposit version 1, publisher-article
Cloud identity, matching PMCID/PMID/DOI/title, CC BY 4.0 notices, and verified
supported PMC Cloud downloads. Provider MD5, PDF/text SHA-256, readable pages and
metadata-source hashes are recorded. First pages and case evidence pages were
rendered and inspected; all main-PDF captions/notices and pinned JATS credit
inventories were checked for separately restrictive material. No such credit was
located. Standalone supplements and cited articles are not selected.

The recorded corrections have now received explicit author impact review in
the manifest. Liu's [disclosure correction](https://pmc.ncbi.nlm.nih.gov/articles/PMC11645136/)
adds a patent conflict of interest; its [figure-label correction](https://pmc.ncbi.nlm.nih.gov/articles/PMC13132388/)
affects Supplemental Figure 3C, whereas a003 uses main-PDF prose referring to
Figures 2B/C. Sachdev's [probe correction](https://pmc.ncbi.nlm.nih.gov/articles/PMC12704798/)
changes a supplementary antisense ddPCR probe sequence; the authors state that
the published data are unaffected. None changes an accepted anchor. The original
deposit/PDF/text bytes remain pinned; notices are assessed separately and are
not added as corpus answer sources.

[ATTRIBUTION.md](ATTRIBUTION.md) preserves ordered citations, notices and licence
links. [metadata/](metadata/) contains unchanged Cloud JSON, PubMed XML and
converter responses. PDFs, complete JATS, extracted text, restricted candidates
and rendered pages remain ignored under `corpus/als-ftd-v1/`. No PDFs are committed
or publicly uploaded. Full PubMed abstracts remain separate from authored summaries.
The actual discovery queries are retained; later PMCID lookups are not discoveries.

## Prepared cases and review

[queries.json](queries.json) contains a001–a010: two same-article multi-hop cases,
four direct lookups, two cross-document synthesis cases, one false-premise case,
and one named-distractor case. Nineteen physical-page anchors bind exact extraction
spans and hashes to facts and evidence sets. [case_dependencies.json](case_dependencies.json)
records source/overlap/decoy dependencies. There are no absent-fact cases, so this
release makes no whole-corpus negative claim. No legacy IDs or gold are replaced.

The central evidence contrasts are:

- a001: postmortem tissue versus 38-day motor neurons; later activation is a hypothesis.
- a002: BAC mouse DPR lowering versus unsupported survival/motor rescue.
- a003: same-donor iPSCs versus differentiated neurons; cell state matters.
- a004: residual poly-GP versus network bursting after different DNA edits.
- a005: RNA-targeting molecular endpoints versus DNA-editing functional endpoints.
- a006: antisense versus sense RNA axonopathy rescue in zebrafish.
- a007: SPECT interpretation versus genetic diagnosis and autopsy in one patient.
- a008: human tissue molecular association versus clinical diagnostic evidence.
- a009: patient diagnosis versus patient-derived laboratory cells as a named decoy.
- a010: cited Drosophila model differences versus the performed vertebrate PKR experiment.

Related cases intentionally test different tasks: a006 is strand-specific lookup,
a010 connects that result to a model explanation; a007 reconstructs diagnostic
discordance, while a009 tests exclusion of laboratory evidence from the patient's
clinical diagnosis. a005 and a008 require distinct contributions from two papers.
The Drosophila and PKR-distribution claims in a010 are attributed to the selected
paper's Discussion and cited work, not independently verified primary findings.

The reference answers preserve models, populations, endpoints and timeframes.
Revision 2 records the Claude review fixes before any evaluation: network bursting
is an edited-versus-unedited observation, without a wild-type normalization claim;
the poly-GP anchor includes both editing outcomes; the BAC phenotype limitation
is attributed to cited prior work; and a002 records its premise and correction
anchors. a008's phosphorylation fact is separated from an authored methodological
caution in its rubric. Case-specific forbidden claims replace generic boilerplate.
Seventeen complete evidence sets include main-PDF figure-legend alternatives for
a004, a005, a006 and a010, plus the alternate Results passage for a003. The figure legend's "minimal to no" network bursting
is accepted alongside the Results wording "no". Other passages and cross-topic
alternatives still require independent completeness review before freeze.
Revision 3 records acceptance of a003’s Results passage without requiring the
Discussion-only adjective "mild", and explains why broad tissue/electrophysiology
summaries alone do not supply all pinned fact qualifiers. Author review covers
identified candidate passages; exhaustive expert completeness review is not established.
The per-alternative receipt is reproducible with `verify_als_ftd_alternatives.py`.
No retrieval output, paid rewriting or judge result was used to choose them.
Before freeze, an independent reviewer should read the four full texts, verify
fact/anchor sufficiency and alternatives, check overlap/duplicates and assess
whether the clinical case is suitable for the intended expert review. Review must
not silently turn hypotheses into causal claims. Correct defects through a traced
revision before evaluation; do not tune gold to preferred retrieval results.

## Conditions and verification

[conditions.json](conditions.json) pins article/version/PDF/text tuples and query
hashes. C1 is the union of all accepted sources; C2 equals C1 because all selected
papers answer a case. The named decoy is already an answer source for other cases.
C3 equals C2 as an **ALS/FTD-only placeholder**, not the combined corpus. Combined
integration needs alternative-evidence and formerly absent-fact review across
cardiology, diabetes, oncology and outliers. Metformin references do not establish
diabetes clinical efficacy; cognitive/diagnostic themes warrant overlap review.

[verification.json](verification.json) records mechanical provenance checks and
[reachability.json](reachability.json) records the offline production chunker oracle.
All 19 anchors and all 10 cases are reachable with unlimited chunks; 10/10 are
structurally feasible at n=8. At n=3, 8/10 are feasible: a005 and a008 need more
chunks for their complete pinned evidence. 7 anchors require adjacent chunks.
The oracle generated 288 chunks and loaded no retrieval models or collection.
These are feasibility ceilings, not retrieval scores or answer correctness.

No collection ingestion or retrieval evaluation runs for this preparation task.
Existing cardiology and other topic queries, collections and results remain
unchanged. After independent review/freeze and isolated combined ingestion, run
cardiology regression and ALS/FTD retrieval on declared membership with
`SEED_ON_EMPTY=false`; record collection identity, extraction and per-source chunks.
Paid rewrite/generation/judge runs need explicit approval. Later combined evaluation
must not treat C3 here as a complete cross-topic condition.

## Reproduce

Use Python 3.12 and the repository environment (pypdf 6.16.1), from the repo root.
In a worktree without `.venv`, use the main checkout's environment by absolute path.

```sh
.venv/bin/python download_corpus.py --manifest benchmark/als-ftd/v1/manifest.json --corpus-dir corpus/als-ftd-v1
.venv/bin/python - <<'PY'
import json
from pathlib import Path
from pypdf import PdfReader
from fetch_article_metadata import read_pmc_xml
release = Path('benchmark/als-ftd/v1')
corpus = Path('corpus/als-ftd-v1')
for article in json.loads((release / 'manifest.json').read_text())['articles']:
    pdf = corpus / article['filename']
    pdf.with_suffix('.txt').write_text('\n'.join(p.extract_text() or '' for p in PdfReader(pdf, strict=True).pages))
    cloud = json.loads((release / article['metadata_sources']['cloud.json']['archive']).read_text())
    (corpus / f"{article['article_id']}.{article['pmc_version']}.article.xml").write_bytes(read_pmc_xml(cloud['xml_url']))
PY
.venv/bin/python verify_als_ftd_release.py
.venv/bin/python verify_als_ftd_alternatives.py
.venv/bin/python verify_benchmark_reachability.py --benchmark benchmark/als-ftd/v1 --corpus-dir corpus/als-ftd-v1 --condition C2
.venv/bin/python -m unittest discover -v
```

The release verifier rejects changed source bytes, metadata joins, PDF provider
receipts, extraction/page boundaries, parser version and incorrect anchor/fact
bindings, missing correction impact records and missing false-premise records.
Four corruption checks reject a re-signed incorrect title, incorrect evidence
offset, omitted correction review and omitted offending premise.
All 206 offline regression tests passed. Mechanical
success does not certify independent scientific review.

## Gold correction revision — 2026-10-05

The active query set incorporates the [source-grounded correction ledger](../../corrections/2026-10-05/README.md). Prior runs retain their original questions and fingerprints; they are not runs of this corrected revision. The corpus and evaluation strategy are unchanged.

## Corrected combined evaluation

The preparation/review status and receipts above describe the original snapshot.
The merged gold-validation findings and accepted corrections now supply the
model-review basis for the [five-topic evaluation freeze](../../combined/v2/README.md).
Its [current verification and reachability](../../combined/v2/reachability.json)
regenerate this strand's query fingerprints, metadata checks and all accepted
alternative witnesses. The old receipts are preserved as historical evidence.
The [combined report](../../combined/v2/REPORT.md) verifies all ten cases in both
the four-article baseline and 55-article corpus. It does not certify independent
biomedical expert review or generated-answer correctness.
