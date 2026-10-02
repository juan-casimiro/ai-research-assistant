# Verified cardiology selection and query release — v1

Selection finalized on 2026-10-01: **21 unique articles**, 263 physical PDF pages,
35,964,584 downloaded bytes (about 34.3 MiB). Every selected deposit is a final
journal version (PMC version 1, after enumerating available versions), carries
CC BY 4.0, resolves through the PMC ID Converter to a matching PubMed PMID/DOI,
and has a checksum-verified, parsed, readable PDF from the supported PMC Cloud
route. These checks apply to the two additional competitors as well as sources.
All 21 have a complete PubMed abstract and an independently labelled selection
summary. Selection is finalized before gold question authoring.

## Files and boundaries

- [manifest.json](manifest.json): full legacy-compatible article metadata plus
  exact rights/version/provenance, metadata/PDF/text hashes and validation receipts.
- [ATTRIBUTION.md](ATTRIBUTION.md): full ordered author citations, source and licence
  links, notices, third-party review and modification history for all 21 records.
- [evidence_map.json](evidence_map.json): full-text relationships, source limitations,
  physical PDF selection locations and byte-bound extraction excerpts. These are
  selection notes, not frozen gold anchors or expected answers.
- [conditions.json](conditions.json): authored source-union membership and tuple
  fingerprints. C1 has 19 actual answer sources; C2 adds Korean hypertension
  consensus and echocardiographic AHRE competition. C3 currently equals C2 because
  this cycle certifies no other-topic sources. Required/alternative source union
  is verified against the authored release. Later topic tasks extend C3 only with
  verified articles; none of the legacy corpus is automatically added.
- [migration.json](migration.json): original file fingerprints, 19 legacy article
  dispositions, all 34 direct cardiology cases plus 10 GWAS/GPT-5 dependencies,
  and additional topic/evidence overlap review flags. It preserves retired IDs.
- [metadata/](metadata/): byte-identical Cloud JSON, batched PubMed XML and PMCID
  converter response. Exact original URLs and SHA-256 receipts are in the manifest.
  The much larger raw article XML, PDFs, text and page renders remain local.

The original `corpus_manifest.json`, `golden_qa.json`, evaluation results and
local corpus are preserved. No server, collection, ingestion or golden run was
started. Historical retrieval percentages describe the original benchmark only.
The [45-case query release and scorer](BENCHMARK.md) are authored under the
[shared standards](../../STANDARDS.md), pending independent PR review/freeze.
The [first C1/C2 retrieval baseline](REPORT.md) records JUA-110 results and
manual evidence review; C3 adds no articles yet. Most selected papers are sources;
roles remain query specific and the two competitors are not topic outliers.

The query files are `queries.json`, `case_dependencies.json` and `case_review.json`.
See [BENCHMARK.md](BENCHMARK.md) for migration, metrics, provenance and focused run
instructions. Selection anchors in `evidence_map.json` remain acquisition notes.

## Retrieve metadata by PMCID

PMC and PubMed are distinct services. Resolve PMCID to PMID with the official
[PMC ID Converter](https://pmc.ncbi.nlm.nih.gov/tools/id-converter-api/), then fetch
that PubMed record through E-Utilities. PubMed supplies the complete abstract and
bibliographic cross-check. The pinned PMC Cloud/JATS deposit supplies the exact
licence, ordered article authors, publication date, article type and PDF object.
`search_query` is acquisition provenance supplied by the researcher; neither
PubMed nor PMC can recover the query used in an earlier search.

[fetch_article_metadata.py](../../../fetch_article_metadata.py) does this join,
checks PMCID/PMID/DOI/title identity, preserves structured abstract labels and
publication-date precision, and writes a **pending** draft record. It preserves
`filename`, `cluster`, `search_query`, `doi`, `pmcid`, `pmc_version`, `title`,
`authors`, `journal`, `abstract_summary`, `year`, `license`, `page_count`,
`has_structured_sections`, `notes` and `license_notes`, plus the full `abstract`,
`pmid`, precise date and source URLs/hashes. Authored summaries, PDF page count,
third-party review and eligibility cannot be invented from metadata; fill those
through the article/PDF selection workflow. Legacy-only manual-download fields
have no place in the new selection.

Run from the repository root, supplying the actual discovery query and a deposit
version chosen after inspecting the
[PMC version listing](https://pmc-oa-opendata.s3.amazonaws.com/?list-type=2&prefix=metadata%2FPMC10363301.):

```sh
.venv/bin/python fetch_article_metadata.py \
  --pmcid PMC10363301 --pmc-version 1 \
  --filename cardio-af-incident-ecg-calibration.pdf --cluster cardiology \
  --search-query '<exact query used for discovery>' \
  --output corpus/cardiology-v1/draft-record.json \
  --archive-dir corpus/cardiology-v1/metadata-refresh
```

For an already-selected article, retain its manifest `search_query` verbatim;
record a new search separately rather than rewriting historical provenance.
A direct PMCID lookup is not itself evidence of a new topical discovery query.
The fetcher requires the explicit deposit version and fails on identity conflicts
or retraction. A metadata refresh is a review input: do not silently replace the
frozen source hashes or certify a PDF from metadata alone.

## Acquire and verify local PDFs/text

[PMC Cloud documentation](https://pmc.ncbi.nlm.nih.gov/tools/pmcaws/) and its current
[dataset README](https://pmc-oa-opendata.s3.amazonaws.com/README.txt) document the
supported metadata/PDF route. Legacy OA/FTP and browser-only publisher routes
are not used. PDFs remain untracked and public PDF publication is separate.

```sh
.venv/bin/python download_corpus.py \
  --manifest benchmark/cardiology/v1/manifest.json \
  --corpus-dir corpus/cardiology-v1
```

For a fresh checkout, also acquire the pinned article XML. Keep it locally as
`corpus/cardiology-v1/<PMCID>.<version>.xml`; the verifier requires this file and
compares it with the manifest's `pmc_article_xml.sha256`. This recipe checks the
provider MD5 before writing and rejects drift from the frozen SHA-256:

```sh
.venv/bin/python - <<'PYTHON'
import hashlib
import json
from pathlib import Path
from fetch_article_metadata import read_pmc_xml
selection = json.loads(Path('benchmark/cardiology/v1/manifest.json').read_text())
for article in selection['articles']:
    metadata = json.loads(Path('benchmark/cardiology/v1',
        article['metadata_sources']['pmc_cloud']['archive']).read_text())
    data = read_pmc_xml(metadata['xml_url'])
    if hashlib.sha256(data).hexdigest() != article['metadata_sources']['pmc_article_xml']['sha256']:
        raise ValueError(f"{article['article_id']}: article XML hash mismatch")
    Path('corpus/cardiology-v1',
        f"{article['pmcid']}.{article['pmc_version']}.xml").write_bytes(data)
PYTHON
```

Extract the text using the recorded pypdf version (6.16.1)
and the same page-joining behaviour as production ingestion, without starting a
server or indexing documents:

```sh
.venv/bin/python - <<'PYTHON'
import json
from pathlib import Path
from pypdf import PdfReader
selection = json.loads(Path('benchmark/cardiology/v1/manifest.json').read_text())
for article in selection['articles']:
    pdf = Path('corpus/cardiology-v1') / article['filename']
    reader = PdfReader(pdf, strict=True)
    pdf.with_suffix('.txt').write_text(
        '\n'.join(page.extract_text() or '' for page in reader.pages), encoding='utf-8')
PYTHON
.venv/bin/python verify_cardiology_selection.py
```

The verifier checks exact selected bytes, deterministic extraction, source
snapshots (including local article XML), evidence offsets, attribution coverage,
nested membership and original baseline hashes. The downloader alone skips an
existing readable file; the verifier is required to catch a different readable
version or extraction drift.
Cloud objects can change within a deposit version; a checksum mismatch needs a
reviewed corpus revision, not silently accepting the new bytes.

Representative pages from every PDF were rendered and inspected. All actual
PDF notice locations and extracted captions/credits were checked against the
pinned article XML. No incompatible specific third-party credit was identified
in the selected PDFs. Standalone linked supplements are excluded. The TAILORED-AF
PDF includes readable image-only reporting-summary pages 22–24; those were
visually checked but are absent from extracted text and must not supply text
anchors. The AF management review PDF contains no licence notice itself; the
matching pinned article XML explicitly grants CC BY 4.0 and its notice is retained
in the attribution inventory. Frontiers/Wiley unversioned PDF notice text is
resolved by explicit CC BY 4.0 PDF hyperlink annotations and article XML.

Before authoring gold values, review every intended passage/table, bind rows and
columns, and resolve acceptable alternatives. The present extraction check is
representative selection QA; it does not certify all future gold table cells.
No independent question review, new retrieval metric or answer-quality claim is
made by article selection.

## Selected articles

| PMCID / PubMed | Article | Published | Planned role |
| --- | --- | --- | --- |
| [PMC10363301](https://pubmed.ncbi.nlm.nih.gov/37481514/) | Comparison of discrimination and calibration performance of ECG-based machine learning models for prediction of new-onset atrial fibrillation | 2023-07-22 | source pool |
| [PMC10607686](https://pubmed.ncbi.nlm.nih.gov/37892626/) | Mechanisms and Prediction of Ischemic Stroke in Atrial Fibrillation Patients | 2023-10-12 | source pool |
| [PMC10619268](https://pubmed.ncbi.nlm.nih.gov/37908019/) | Resistant hypertension: consensus document from the Korean society of hypertension | 2023-11-01 | competition |
| [PMC10985250](https://pubmed.ncbi.nlm.nih.gov/38567348/) | Dapagliflozin versus sacubitril–valsartan for heart failure with mildly reduced or preserved ejection fraction | 2024-03-19 | source pool |
| [PMC11265054](https://pubmed.ncbi.nlm.nih.gov/39033295/) | Detection of atrial fibrillation using a nonlinear Lorenz Scattergram and deep learning in primary care | 2024-07-20 | source pool |
| [PMC11354916](https://pubmed.ncbi.nlm.nih.gov/39201499/) | Effects of SGLT2-Inhibitors on Comprehensive Geriatric Assessment, Biomarkers of Oxidative Stress, and Platelet Activation in Elderly Diabetic Patients with Heart Failure with Preserved Ejection Fraction | 2024-08-13 | source pool |
| [PMC11373557](https://pubmed.ncbi.nlm.nih.gov/39239537/) | Investigation of cardiorenal outcomes and incidence of genitourinary tract infection after combined SGLT2 inhibitor and ACEI/ARB use in patients with chronic kidney disease stages 3-5: A real-world retrospective cohort study in Taiwan | 2024-08-12 | source pool |
| [PMC11374717](https://pubmed.ncbi.nlm.nih.gov/39014113/) | Resistant hypertension: diagnosis, evaluation, and treatment a clinical consensus statement from the Thai hypertension society | 2024-07-16 | source pool |
| [PMC11514186](https://pubmed.ncbi.nlm.nih.gov/39465316/) | Lack of incremental prognostic value of triglyceride glucose index beyond coronary computed tomography angiography features for major events | 2024-10-27 | source pool |
| [PMC11549774](https://pubmed.ncbi.nlm.nih.gov/39516772/) | Prognostic value of computed tomography-derived fractional flow reserve in patients with diabetes mellitus and unstable angina | 2024-11-08 | source pool |
| [PMC11973566](https://pubmed.ncbi.nlm.nih.gov/40037646/) | Empagliflozin in resistant hypertension and heart failure with preserved ejection fraction: the EMPEROR-Preserved trial | 2025-03-04 | source pool |
| [PMC12003177](https://pubmed.ncbi.nlm.nih.gov/39953289/) | Artificial intelligence for individualized treatment of persistent atrial fibrillation: a randomized controlled trial | 2025-02-14 | source pool |
| [PMC12436478](https://pubmed.ncbi.nlm.nih.gov/40450156/) | Subclinical atrial fibrillation prediction based on deep learning and strain analysis using echocardiography | 2025-05-31 | competition |
| [PMC12683810](https://pubmed.ncbi.nlm.nih.gov/41354946/) | Effectiveness of SGLT2 inhibitors, incretin-based therapies, and finerenone on cardiorenal outcomes: a meta-analysis and network meta-analysis | 2025-12-08 | source pool |
| [PMC12880197](https://pubmed.ncbi.nlm.nih.gov/41657709/) | Artificial Intelligence–driven Detection, Mapping, and Personalized Therapy for Atrial Fibrillation | 2026-01-15 | source pool |
| [PMC12886974](https://pubmed.ncbi.nlm.nih.gov/41663376/) | Partitioned polygenic scores show mechanistic heterogeneity in type 2 diabetes and hypertension comorbidity | 2026-02-09 | source pool |
| [PMC13433181](https://pubmed.ncbi.nlm.nih.gov/42553073/) | Development of a MACE risk prediction model based on CCTA-derived quantitative parameters: a proof-of-concept study | 2026-07-21 | source pool |
| [PMC13433862](https://pubmed.ncbi.nlm.nih.gov/42553332/) | Long-term SGLT2 inhibitor therapy improves myocardial strain and diastolic function in HFpEF: a retrospective study linking functional recovery to reduced myocardial fibrosis | 2026-07-21 | source pool |
| [PMC13439631](https://pubmed.ncbi.nlm.nih.gov/42554205/) | Predictive Ability of the CHA2DS2‐VA Score for No‐Reflow Phenomenon in ST‐Elevation Myocardial Infarction Patients Undergoing Primary PCI | 2026-08-05 | source pool |
| [PMC4804513](https://pubmed.ncbi.nlm.nih.gov/27007793/) | Effect of low-dose spironolactone on resistant hypertension in type 2 diabetes mellitus: a randomized controlled trial in a sub-Saharan African population | 2016-03-23 | source pool |
| [PMC8866621](https://pubmed.ncbi.nlm.nih.gov/35195795/) | CHA2DS2 VASc score and brachial artery flow-mediated dilation as predictors for no-reflow phenomenon in patients with ST-segment elevation myocardial infarction undergoing primary percutaneous coronary intervention | 2022-02-23 | source pool |

## Evidence relationships and deliberate exclusions

- **AF:** primary-care episode detection versus five-year incident-AF prediction;
  CNN discrimination versus calibration; AHRE duration/classification versus
  prospective prediction; primary/secondary ablation outcomes and mITT/PP groups;
  stroke-risk score applications versus no-reflow.
- **Coronary/STEMI:** CHA2DS2-VA versus CHA2DS2-VASc in distinct STEMI cohorts;
  CT-FFR diagnostic versus prognostic AUC; one-year soft-endpoint MACE versus
  three-year MACCE and longer-term MI/death/stroke; association versus incremental
  discrimination and unadjusted versus adjusted estimates.
- **HFpEF/BP/cardiorenal:** myocardial fibrosis versus geriatric oxidative/platelet
  markers; BP versus HF/renal endpoints; consensus recommendations versus a small
  intervention trial; renal benefit versus infection harm; direct trial evidence
  versus indirect drug-class/network or economic comparisons.
- **Genetic overlap:** partitioned T2D/BP comorbidity mechanisms, not sulfonylurea
  response. The transferred PGS candidate was freshly verified; the rest of the
  related transferred candidates remain unselected and unapproved.

The restricted AF review and no-PMCID hypertension survey are replaced around
these relationships. The no-PMCID GPT-5/tau217 paper and q130–q133 are retired from
this selected experiment: AI/plasma-tau diagnosis is not retained. Vascular/
geriatric cognition in the HFpEF source is a different topic and does not supply
those old facts. The later outlier task reuses this exclusion, avoiding duplicate
replacement work. Restricted GWAS and cardio-oncology overlap are excluded;
new T2D/BP genetics supplies a distinct eligible overlap, while drug-response and
oncology questions remain later topic work. Every legacy article disposition and
direct query dependency is explicit in the migration ledger.

PATHWAY-2 was rejected for **CC BY 3.0**. The AI-QCT ischaemia candidate was rejected
pending resolution of its **BioRender** graphical-abstract credit, not because
such a credit universally prohibits reuse. A further HFpEF review was redundant
for this cycle and was not PDF-certified. Rejected/deferred rationale is preserved
in `selection_log`; exclusions are project-policy decisions, not blanket legal
claims.

Source conflicts are useful evidence-review targets, not defects to harmonize
silently: AHRE accuracy 0.809 versus conclusion 0.805; spironolactone abstract
claim versus detailed BP thresholds/one uncontrolled patient; TAILORED-AF stage-
specific cohort counts and rounded HR; malformed CT-FFR abstract sensitivity;
TyG figure-caption label; and retained CCTA sample-count ambiguity. Reviews and
indirect studies must not be presented as primary head-to-head evidence.
