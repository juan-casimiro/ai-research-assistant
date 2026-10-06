"""Render benchmark/oncology/v1/DECISIONS.md from the release data; run from the repository root. Offline only."""
import json
import re
from pathlib import Path

R = Path('benchmark/oncology/v1')


ARTICLE_WHY = {
    'PMC13429855': 'Retained legacy article after re-verifying CC BY 4.0, version and PDF. A dense review of cited liquid-biopsy evidence (CSF ctDNA, NILE, LDCT versus MCED, MRD assays, EarlyCDT), so it supports attribution-to-cited-study cases and a scoped absent fact.',
    'PMC9239676': 'Retained legacy article after re-verification. The only screening source: mutually exclusive screening categories, printed flow-diagram counts with internal inconsistencies, and cited targets versus observed rates.',
    'PMC9844597': 'Replaces the restricted perioperative NSCLC study. A resected real-world cohort with unadjusted versus PSM DFS, MPR, OS comparisons with conflicting labels, and a resected-only selection restriction. Treatment partner for the q117 synthesis replacement (o030).',
    'PMC10770829': 'Second neoadjuvant chemoimmunotherapy cohort (stage III, EGFR/ALK-negative). Same intervention as Hunan in a different population, so the two compete realistically; it adds a response gain with nonsignificant DFS and a narrative/table MPR conflict.',
    'PMC12931073': 'Actual breast immunotherapy evidence, replacing the mislabelled legacy breast file. Nonmatched historical cohorts, myocarditis surveillance and discontinuation denominators; also a cardio-oncology source.',
    'PMC10840225': 'Advanced EGFR-mutant first-line afatinib cohort. Separates ORR from time to treatment failure by starting dose and contains an abstract/Table 2 dose-share reversal. Replaces the restricted source\'s afatinib-dosing coverage and serves as the o024 decoy.',
    'PMC11891047': 'Observational meta-analysis of cardiovascular events with ICIs in NSCLC: prevalence distinct from a pooled HR from only four studies; attributed comparative Results wording is accepted. Needed for cardio-oncology endpoint distinctions.',
    'PMC11181582': 'RCT meta-analysis of ICI cardiotoxicity in lung cancer: comparator-relative cardiac adverse-event RRs and a null, imprecise heart-failure subgroup.',
    'PMC11431721': 'Review of nonmetastatic driver-altered NSCLC that attributes ADAURA results by stage population. Supports attribution and stage-scope cases and supplies the ctDNA-MRD trial row used as the o025 decoy.',
    'PMC11547071': 'Additional competition only (C2): POL-MOL describes pathologist-ordered testing of agreed biomarkers, which overlaps the Gosney consensus. No case uses it as an answer; it is recorded as partial support so that attribution to the consensus is tested.',
    'PMC10485396': 'Gosney expert consensus on pathologist-initiated reflex testing: workflow, delays and early-stage EGFR testing. Real-world readiness partner for the q117 synthesis replacement (o030).',
    'PMC13190586': 'ICD mini-review on cold phenotypes and danger signals. Replaces the deferred microenvironment coverage with mechanistic content; cited trial claims were deliberately not used as efficacy gold. Its notice, captions and credits show no BioRender credit.',
    'PMC10073666': 'Consensus-definition review of immune exclusion: spatial phenotypes, arbitrary cutoffs and heterogeneity. Competes with the ICD review\'s phenotype definitions.',
    'PMC12495207': 'Older advanced-NSCLC PD-1 cohort with competing-risk cause-specific mortality. Replaces the restricted source\'s CVD-mortality coverage and keeps mortality distinct from cardiac events.',
}

PRINCIPLES = [
    ('Eligibility', 'Only exactly CC BY 4.0 or CC0 1.0 articles with a pinned PMC version, verified PDF and clear third-party review are selected (STANDARDS gates 1–6). NC/ND licences are rejected. Articles crediting BioRender figures are deferred, because complete-PDF reuse rights are unresolved. Resemblance to BioRender artwork without a credit is not treated as a blocker.'),
    ('Coverage, not counts', 'No fixed article or case count. Articles were chosen for evidence relationships: same intervention in different populations, response versus survival, adjusted versus unadjusted results, cited-trial attribution, and competing cardio-oncology endpoints. Cases were authored from full text before any retrieval run.'),
    ('Legacy migration', 'All five legacy articles and 42 legacy cases are accounted for. Two articles are retained after re-verification; three are replaced or deferred. A legacy ID is kept only when its task stays on the same source family and the ledger notes any task change. Changed study-specific tasks get new oncology-local o-IDs. Replacement links are kept only when the new case tests the same evidence type or reasoning task; topic similarity alone is not enough.'),
    ('Source conflicts', 'Internal source conflicts are made explicit in gold and accepted when attributed: Hunan weighted/PSM label, Zhongshan narrative/table MPR, Vietnam abstract/Table 2 dose shares, Helsinki discontinuation denominators and the screening flow diagram. Gold never invents a reconciliation.'),
    ('Answerability', 'Absent facts are scoped to the whole selected oncology corpus and record near-miss context. False premises need positive correction anchors. Combined-corpus negative claims are rechecked in the current combined evaluation.'),
    ('Near-duplicates', 'A strict subset or duplicate of another case is withdrawn (q082, o019; legacy q084). Overlapping cases are retained only with a distinct failure mode, recorded per case below.'),
    ('Categories', 'Categories follow STANDARDS: a direct lookup uses one local passage, and separated passages in one article make a case multi-hop. o009 and o023 were recategorised for this reason.'),
    ('Evidence budget', 'Every evidence case must be completely retrievable at n=8. Where a required span would exceed that, the fact is tested in a companion case instead (o030 accepts either attributed Hunan OS label; o029 requires the Results/legend conflict. The pre-correction primary o030 set needed 7 chunks, and adding its legend needed 9).'),
    ('Conditions', 'C1 is the exact answer-source union; C2 adds POL-MOL as competition; source-v1 C3 is an oncology-only placeholder; use combined-v2 C3 for all 55 articles.'),
    ('Provenance honesty', 'Each article\'s search string is labelled legacy, topical or targeted lookup. Unpreserved discovery queries are stated as unpreserved, not reconstructed.'),
    ('No tuning exposure', 'No retrieval output, generated answer or paid call informed selection or gold. Three Claude reviews (8b1adbe, a226bba, b626fbb) and the Codex correction pass drove the recorded corrections.'),
]


def bullet(label, value):
    return f'- **{label}:** {value}'


def render_decisions(manifest, queries, audit, candidates, ledger, conditions):
    """Render in memory so release verification can detect stale or edited prose."""
    articles = {a['article_id']: a for a in manifest['articles']}
    short = {a['article_id']: a['filename'].removesuffix('.pdf') for a in manifest['articles']}
    if set(ARTICLE_WHY) != set(articles):
        raise ValueError('Selected articles lack decision rationales')
    lines = ['# Oncology v1 decision record', '',
             'This record explains every article, case and migration decision in this release. It is generated from',
             '[manifest.json](manifest.json), [candidate_log.json](candidate_log.json), [queries.json](queries.json),',
             '[legacy_audit.json](legacy_audit.json) and [revision_ledger.json](revision_ledger.json), which remain the',
             'sources of truth. Regenerate it from the repository root with `.venv/bin/python benchmark/oncology/v1/render_decisions.py`.',
             '[REVIEW.md](REVIEW.md) records the independent review rounds.', '',
             '## Open decisions', '']
    open_cases = [c for c in audit['cases'] if c['open_decision']]
    if open_cases:
        lines += ['These legacy cases were retired on retained sources even though the pinned text contains their evidence.',
                  'The original author recorded no case-specific reason, so the choice to restore them or confirm retirement is open:', '']
        for c in open_cases:
            lines += [f'- **{c["id"]}** ({c["legacy_category"]}): {c["question"]}',
                      f'  - Original author\'s rationale: {c.get("original_author_rationale", "not recorded")}']
        lines += ['', 'To resolve one, replace its `original_author_rationale` placeholder in legacy_audit.json, set',
                  '`open_decision` to false once Juan decides, update `reason`, then re-render this file and run the verifier.']
    else:
        lines.append('None.')
    resolved = [c for c in audit['cases'] if c.get('original_author_rationale') and not c['open_decision']]
    if resolved:
        lines += ['', '### Resolved', '']
        for c in resolved:
            lines += [f'- **{c["id"]}**: {c["reason"]}',
                      f'  - Original author\'s rationale: {c["original_author_rationale"]}']
    lines += ['', '## Decision principles', '']
    lines += [bullet(label, text) for label, text in PRINCIPLES]

    lines += ['', '## Legacy articles', '', '| Legacy file | PMCID | Licence | Disposition |', '| --- | --- | --- | --- |']
    for article in audit['articles']:
        licence = ', '.join(u.split('/licenses/')[1].strip('/').replace('/', ' ') for u in article['licence_urls'])
        lines.append(f'| {article["legacy_filename"]} | {article["pmcid"]} | CC {licence.upper()} | {article["disposition"]} |')

    lines += ['', '## Selected articles', '']
    for aid, article in articles.items():
        answer = [q['id'] for q in queries['queries'] if aid in q['dependencies']['required'] + q['dependencies']['alternatives']]
        decoy = [q['id'] for q in queries['queries'] if aid in q['dependencies']['decoys']]
        overlap = [q['id'] for q in queries['queries'] if aid in {f['article_id'] for f in q['dependencies'].get('overlap_findings', [])}]
        member = [name for name, cond in conditions['conditions'].items() if aid in cond['article_ids']]
        lines += [f'### {aid} — {short[aid]}', '', f'*{article["title"]}*', '',
                  bullet('Why selected', ARTICLE_WHY[aid]),
                  bullet('Answer source for', ', '.join(answer) or 'none (competition only)'),
                  bullet('Named decoy for', ', '.join(decoy) or 'none'),
                  bullet('Partial-support overlap for', ', '.join(overlap) or 'none'),
                  bullet('Conditions', ', '.join(member)),
                  bullet('Search provenance', f'{article["search_query_type"]} — {article["search_provenance_note"]}'), '']

    lines += ['## Candidates not selected', '', '| PMCID | Title | Disposition | Reason |', '| --- | --- | --- | --- |']
    for candidate in candidates['candidates']:
        if candidate['disposition'] != 'selected':
            lines.append(f'| {candidate["pmcid"]} | {candidate["title"]} | {candidate["disposition"]} | {candidate["reason"]} |')

    order = ['direct_lookup', 'multi_hop', 'cross_doc_synthesis', 'cross_doc_distractor', 'false_premise', 'unanswerable']
    lines += ['', '## Active cases', '']
    for category in order:
        cases = [q for q in queries['queries'] if q['category'] == category]
        lines += [f'### {category} ({len(cases)})', '']
        for q in cases:
            evidence = '; OR '.join(s['id'] + ': ' + ' + '.join(s['anchors']) for s in q['evidence_sets']) if q['evidence_sets'] else 'none (absent fact)'
            lines += [f'#### {q["id"]} (revision {q["revision"]})', '', f'> {q["question"]}', '',
                      bullet('Why this case', q['selection_rationale']),
                      bullet('Evidence', evidence)]
            if q.get('reasoning'):
                lines.append(bullet('Multi-hop link', q['reasoning']))
            for d in q['related_distractors']:
                lines.append(bullet('Named decoy', f'{d["article_id"]} `{d["anchor_id"]}`. {d["plausible_confusion"]} {d["reason_inapplicable"]}'))
            for f in q['dependencies'].get('overlap_findings', []):
                lines.append(bullet('Overlap', f'{f["article_id"]} `{f["anchor_id"]}` ({f["role"]}). {f["assessment"]}'))
            for n in q['dependencies'].get('negative_context', []):
                lines.append(bullet('Near-miss context', f'`{n["anchor_id"]}`. {n["assessment"]}'))
            lines.append(bullet('Alternative-evidence review', q['review'].get('alternative_evidence_check', 'Not yet recorded.')))
            lines.append(bullet('Near-duplicate review', q['review']['duplicate_leakage_check']))
            if q.get('supersedes_coverage_of'):
                lines.append(bullet('Replaces coverage of', f'legacy {q["supersedes_coverage_of"]}'))
            lines.append('')

    lines += ['## Withdrawn before freeze', '']
    for qid, record in ledger['withdrawn_cases'].items():
        lines.append(bullet(qid, f'{record["reason"]} Coverage retained by {record["coverage_retained_by"]}.'))

    lines += ['', '## Legacy case migration', '', '| Legacy ID | Action | Linked cases | Reason | Link basis |', '| --- | --- | --- | --- | --- |']
    for c in audit['cases']:
        linked = ', '.join(c['replacement_cases']) or '—'
        basis = c.get('replacement_basis') or ('Revised in place.' if c['action'] == 'revise_in_v1' else '—')
        lines.append(f'| {c["id"]} | {c["action"]} | {linked} | {c["reason"]} | {basis} |')

    lines += ['', '## Retained IDs whose task changed', '']
    lines += [bullet(qid, note) for qid, note in ledger['retained_id_task_changes'].items()]

    lines += ['', '## Revision history', '']
    for n, rev in enumerate(ledger['revisions'], 1):
        lines.append(f'{n}. From `{rev["previous_commit"][:7]}`: {rev["reason"]}')
    lines.append('')
    return re.sub(r'JUA-112', 'the oncology audit', '\n'.join(lines))


def main():
    values = [json.loads((R / name).read_text()) for name in
              ['manifest.json', 'queries.json', 'legacy_audit.json', 'candidate_log.json',
               'revision_ledger.json', 'conditions.json']]
    rendered = render_decisions(*values)
    (R / 'DECISIONS.md').write_text(rendered)
    print(len(rendered.splitlines()), 'lines')


if __name__ == '__main__':
    main()
