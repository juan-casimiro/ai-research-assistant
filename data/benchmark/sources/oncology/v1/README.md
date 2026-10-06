# Oncology selection and query release — v1

Oncology selection and authoring record, 2026-10-02. **14 articles**, 187 physical PDF pages,
25,168,522 downloaded bytes; **44 cases** and 84 exact extraction anchors.
Selection and gold were authored without retrieval results. Review rounds
are recorded in the historical review files. The reviewed merge is held fixed for the local retrieval baseline in [EVALUATION.md](EVALUATION.md).

[DECISIONS.md](DECISIONS.md) explains every article, candidate, case and legacy-migration
decision, and lists open decisions. [render_decisions.py](../../../../../tools/evaluation/historical/benchmark/oncology/v1/render_decisions.py) generates it from the
release JSON files plus the article rationales and principles held in that script. The verifier
rejects undocumented decisions, shared boilerplate rationale and prose that differs
from a fresh in-memory render.

## Audit and selection

All five legacy oncology articles and all 42 cases (q078–q119) are accounted for
in [legacy_audit.json](legacy_audit.json). The two permissive liquid-biopsy and
US screening papers are retained after checking their pinned deposits. The
misnamed `onco-breast-immunotherapy.pdf` is actually driver-positive NSCLC and,
like the precision-treatment editorial, has a CC BY-NC licence. Both are replaced.
The legacy microenvironment review is deferred because its acknowledgement
credits BioRender; its complete-PDF reuse rights remain unresolved.

The replacement set adds resected NSCLC treatment cohorts, nonmetastatic driver
therapy, first-line advanced EGFR treatment, pathologist-initiated reflex testing,
actual TNBC evidence, cardiovascular event and cause-specific mortality evidence,
and immune-exclusion/ICD mechanisms. POL-MOL supplies additional biomarker-testing
competition. [candidate_log.json](candidate_log.json) records 28 candidates and
selected, restricted, deferred or lower-priority dispositions. A permissive
article-level notice does not override a specific incompatible figure credit.
Deferred BioRender papers were not ingested or counted as selected.

[manifest.json](manifest.json) contains full bibliographic metadata, complete
abstracts, separately authored selection summaries, explicit topic membership,
licence and figure/table credit inventories, version decisions and acquisition
receipts. Every selected version is pinned to PMC version 1, CC BY 4.0, matching
PMCID/PMID/DOI, provider MD5, local PDF/text SHA-256 and readable parsed pages.
Article XML notices and PDF licence links were checked. PDF identity pages and
representative evidence pages were rendered; exact gold evidence is separately
bound in [queries.json](queries.json). Standalone linked supplements are excluded.

[ATTRIBUTION.md](ATTRIBUTION.md) supplies ordered author citations, notices and
source/licence links. [metadata/](metadata) contains unchanged Cloud JSON,
PubMed XML and converter responses with manifest hashes. PDFs, complete article
XML, extracted text and renders remain local and ignored by Git. Original global
manifest, golden cases, prior evaluation results and shared collections are preserved.

## Cases and conditions

[queries.json](queries.json) contains 21 lookups, 8 same-article multi-hop cases,
3 cross-document synthesis cases, 2 named-distractor cases, 7 false-premise cases
and 3 absent-fact cases. Each answer fact names its population, endpoint, units,
timeframe, tolerance and contradiction rule. Evidence includes physical page,
section, exact raw extraction offsets and hashes. Required evidence is bound to
each fact; decoys identify the plausible confusion and why their scope differs.
The three absent cases ask for facts not reported by specifically named studies;
their scopes include the whole selected oncology corpus. Broader combined-corpus
negative claims require another scope review in the combined evaluation.

Of the legacy cases, 15 IDs have explicit revisions and 27 are retired. New
oncology-local IDs are o001–o030 except o019. Before freeze, q082 and o019 were withdrawn
as near-duplicates of o025 and o023. [revision_ledger.json](revision_ledger.json) records
the pre-freeze corrections, renamed coverage tasks, withdrawn cases and retained IDs whose task changed. These are coverage replacements, not equivalent
labels: historical scores must not be compared as if sources and gold were unchanged.
[case_dependencies.json](case_dependencies.json) and [evidence_map.json](evidence_map.json)
record required sources, decoys, overlap review and selected evidence relationships.
Shared evidence supports distinct tasks; no fixed query or article count was used.

All 41 evidence-bearing cases received a restatement review, recorded per case in
[case_review.json](case_review.json). Twenty cases have complete alternative sets,
including Results/table screening rates, Table 4 race contrasts and the Hunan MPR
Results. One complete alternative suffices; matching only part of an alternative
does not. q098 and o027 are direct lookups because a local table/Results passage
supplies their complete gold. Alternatives remain conservative pinned spans, not
exhaustive semantic matching; the review did not re-audit external cited studies.

Important source conflicts are explicit: Hunan unadjusted DFS significance
disappears after matching, and its p=0.038 OS comparison is a "weighted population"
in the Results but "after PSM" in the Figure 1D legend; the stage III cohort's MPR narrative and table disagree;
the Vietnam afatinib abstract reverses starting-dose shares relative to Table 2;
Helsinki postoperative discontinuation percentages use different denominators.
Screening flow-chart counts are requested as printed; the chart's age label and
subtraction arithmetic are inconsistent. Do not invent corrected cohort counts.
Table 4 labels N=42,701 although the analysis group is 40,511; q097/q098 accept
either optional count when attributed and do not require a denominator. o001's
response-versus-DFS correction no longer requires the separate count-conflict task
tested by o002. The q098 cervical-only-versus-dual contrast includes both Hispanic
women's higher odds and Black women's lower odds, each relative to White women.
Cardiac events, myocarditis, troponin elevation, cause-specific death, pathological
response and mature survival benefit remain distinct endpoints.

[conditions.json](conditions.json) binds article/version/PDF/text tuples and query
hashes: C1 is the exact 13-article answer-source union; C2 adds POL-MOL. C3 currently
equals C2 and is explicitly an oncology-only placeholder. Cross-topic membership
and interference evaluation belong to the later combined-corpus task; this release
does not incorporate the independently changing diabetes or outlier selections.

## Reproduce acquisition and offline checks

Run from the repository root with Python 3.12 and pypdf 6.16.1. PDFs are fetched
using supported PMC Cloud deposits; no browser exceptions apply to this set.

```sh
.venv/bin/python -m tools.corpus.download_corpus --manifest data/benchmark/sources/oncology/v1/manifest.json --corpus-dir corpus/oncology-v1
.venv/bin/python - <<'PY'
import hashlib, json
from pathlib import Path
from pypdf import PdfReader
from fetch_article_metadata import read_pmc_xml
release = Path('benchmark/oncology/v1')
corpus = Path('corpus/oncology-v1')
for article in json.loads((release / 'manifest.json').read_text())['articles']:
    pdf = corpus / article['filename']
    assert hashlib.sha256(pdf.read_bytes()).hexdigest() == article['download']['pdf_sha256']
    text = '\n'.join(page.extract_text() or '' for page in PdfReader(pdf, strict=True).pages)
    assert hashlib.sha256(text.encode()).hexdigest() == article['validation']['extracted_text_sha256']
    pdf.with_suffix('.txt').write_text(text)
    cloud = json.loads((release / article['metadata_sources']['cloud.json']['archive']).read_text())
    xml = read_pmc_xml(cloud['xml_url'])
    assert hashlib.sha256(xml).hexdigest() == article['metadata_sources']['article.xml']['sha256']
    (corpus / f"{article['article_id']}.{article['pmc_version']}.cloud.xml").write_bytes(xml)
PY
.venv/bin/python -m tools.corpus.verify_oncology_release
.venv/bin/python -m tools.corpus.verify_benchmark_reachability --benchmark data/benchmark/sources/oncology/v1 --corpus-dir corpus/oncology-v1 --condition C2
.venv/bin/python -m unittest discover -v
```

When using a worktree, invoke the existing repository virtual environment by its
absolute path if `.venv` is absent. Readability alone does not certify byte identity;
the separate verifier rejects changed PDFs, extraction, metadata and gold linkage.
It also checks oracle counts/rates/labels and the production chunker fingerprint,
recomputes both oracles, validates ledger hash/category history and migration links,
and checks anchor fact bindings and positive false-premise correction evidence.
Source/decoy roles remain question-specific, as required by STANDARDS.

## Retrieval evaluation

The reviewed PR #33 merge is held fixed in [runs/freeze.json](runs/freeze.json).
[EVALUATION.md](EVALUATION.md) records complete C1/C2 vector retrieval and a
focused cardiology/diabetes regression, with immutable raw contexts, matching
fingerprints and verification limits. Gold, source bytes, scorer and retrieval
implementation were unchanged during the comparison. No paid calls occurred.

The original [REPORT.md](REPORT.md) records the pre-retrieval offline checks;
its no-retrieval statements describe that earlier stage. Combined C3 and
cross-topic negative review are recorded in the current combined benchmark. Paid rewrite/generation/judge
runs require separate explicit approval.

Raw duplicate PDFs and deferred candidates remain archived under
`corpus/oncology-v1/acquisition/`, outside top-level selected membership.

The generated decision record retains its original command and bytes. Run its
archived generator through the [original-layout runner](../../../../../tools/README.md#preserved-historical-tools);
relative output belongs to the temporary historical view.
