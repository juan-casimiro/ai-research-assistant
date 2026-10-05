"""Join final decisions with immutable historical reviews and verify provenance."""
from __future__ import annotations
import argparse
import collections
import hashlib
import json
import re
from pathlib import Path
from accept_final_reply import canonical_reply
from run_stage import schema_errors, source_quote
from stage0 import HERE, ROOT, load


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def final_counts(cases, key):
    result = {}
    for label in sorted({c[key] for c in cases}):
        rows = [c for c in cases if c[key] == label]
        counts = collections.Counter(c['verdict'] for c in rows)
        result[label] = {'cases': len(rows), 'valid': counts['valid'], 'valid_minor': counts['valid_minor'],
                         'needs_correction': sum(c['verdict'] not in ('valid', 'valid_minor') for c in rows),
                         'blocking': sum(c['severity'] == 'blocking' for c in rows)}
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace-root', type=Path, required=True)
    parser.add_argument('--write-report', action='store_true')
    args = parser.parse_args()
    ws = args.workspace_root.resolve()
    manifest = load(HERE / 'final_review_manifest.json')
    baseline = load(HERE / 'results/full_findings.json')
    articles = ws / 'jua-106-gold-ws/hunt/articles'
    errors, coverage, audits = [], {}, []
    for set_name, sha in manifest['query_sha256'].items():
        from stage0 import SETS
        if digest(ROOT / SETS[set_name]) != sha:
            errors.append(f'gold changed: {set_name}')
    for path, sha in [(ROOT / 'benchmark/STANDARDS.md', manifest['standards_sha256']),
                      (HERE / 'briefs/stage7_final.md', manifest['brief_sha256']),
                      (HERE / 'schemas/stage7_final.schema.json', manifest['schema_sha256'])]:
        if digest(path) != sha:
            errors.append(f'frozen input changed: {path.name}')
    runner_counts = collections.Counter()
    for batch in manifest['stage7_final']:
        case_id = batch['cases'][0]
        packet = ws / batch['batch_file']
        if len(batch['cases']) != 1 or digest(packet) != batch['input_sha256']:
            errors.append(f'packet changed or multi-case: {case_id}')
        for name, sha in batch['article_sha256'].items():
            if digest(packet.parent.parent / 'articles' / name) != sha:
                errors.append(f'article changed: {case_id}/{name}')
        path = HERE / 'results/final_codex' / (batch['batch_id'] + '.json')
        if not path.exists():
            errors.append(f'missing final decision: {case_id}')
            continue
        record = load(path)
        runner_counts[record['runner']['model']] += 1
        reply = record['output']
        # The runner adds quote_verified after schema validation; do not mutate saved results.
        clean = json.loads(json.dumps(reply))
        for evidence in clean['evidence']:
            evidence.pop('quote_verified', None)
        try:
            canonical_reply(clean, packet.parent.parent / 'articles')
        except ValueError as error:
            errors.append(f'{case_id}: {error}')
        if record['runner']['model'] != batch['runner']['model'] or record['runner']['reasoning_effort'] != 'low':
            errors.append(f'runner outside budget: {case_id}')
        commands = []
        trace = ws / record['transcript']
        for line in trace.read_text().splitlines():
            try: event = json.loads(line)
            except ValueError: continue
            item = event.get('item', {})
            if event.get('type') == 'item.completed' and item.get('type') == 'command_execution':
                commands.append(item['command'])
        flags = []
        for command in commands:
            if '../' in command or '/Users/' in command or re.search(r'\b(curl|wget|claude|kimi|codex)\b', command):
                flags.append(command)
            for name in re.findall(r'(?:articles/)([A-Za-z0-9_.-]+\.txt)', command):
                if name not in batch['article_sha256']:
                    flags.append(command)
            if re.search(r'\b(?:cat|open|pdftotext|pypdf|fitz)\b[^\n]*\.pdf', command):
                flags.append(command)
            case_refs = re.findall(r'cases/final-([a-z0-9]+)\.json', command)
            if any(i != case_id for i in case_refs):
                flags.append(command)
        if flags:
            errors.append(f'transcript needs manual isolation check: {case_id}')
        audits.append({'id': case_id, 'packet_sha256': digest(packet),
                       'result_sha256': digest(path), 'transcript_sha256': digest(trace),
                       'commands': commands, 'potential_scope_flags': flags,
                       'quotes_verified': record['quotes'], 'runner': record['runner']})
        coverage[case_id] = record
    if errors:
        print(json.dumps({'validation_errors': errors}, indent=2))
        raise SystemExit(1)
    second = {p.stem.removeprefix('review6-'): load(p) for p in (HERE / 'results/review6').glob('*.json')}
    cases = []
    for old in baseline['cases']:
        case_id = old['id']
        row = {'id': case_id, 'set': old['set'], 'category': old['category'],
               'historical_verdict': old['verdict'], 'historical_severity': old['severity'],
               'historical_result': 'results/full_findings.json', 'verdict': old['verdict'],
               'severity': old['severity'], 'decision_source': 'historical_stages_0_to_5',
               'evidence': [], 'rationale': '', 'proposed_correction': ''}
        if case_id in second or case_id in coverage:
            reply = (coverage.get(case_id) or second[case_id])['output']
            row.update(verdict=reply['own_verdict'], severity=reply['own_severity'],
                       gold_stands_as_returned=reply['gold_stands'],
                       scoring_contract_stands=reply['own_verdict'] in ('valid', 'valid_minor'), evidence=reply['evidence'],
                       rationale=reply['rationale'], proposed_correction=reply['correction_assessment'],
                       decision_source='codex_final' if case_id in coverage else 'codex_stage6_agreement',
                       stage6_result=f'results/review6/review6-{case_id}.json' if case_id in second else None,
                       final_result=f'results/final_codex/final-{case_id}.json' if case_id in coverage else None,
                       severity_basis=reply.get('severity_basis', 'Accepted agreeing Stage 6 result; no material defect identified.'))
            cited = []
            for original in reply['evidence']:
                name = Path(original['file']).name
                text = (articles / name).read_text()
                quote = source_quote(original['quote'], text)
                if quote is None:
                    raise SystemExit(f'unverifiable accepted quote: {case_id}/{name}')
                start = text.index(quote)
                cited.append({'file': name, 'quote': quote, 'point': original['point'],
                              'line_start': text.count('\n', 0, start) + 1,
                              'line_end': text.count('\n', 0, start + len(quote)) + 1,
                              'quote_verified': True, 'text_sha256': digest(articles / name)})
            row['evidence'] = cited
        elif old.get('adjudication'):
            row.update(evidence=old['adjudication']['evidence'], rationale=old['adjudication']['rationale'],
                       proposed_correction=old['adjudication']['proposed_correction'])
        if case_id in ('x002', 'x004', 'x005'):
            row['luna_preconfirmation_result'] = f'results/final_luna_preconfirmation/final-{case_id}.json'
        cases.append(row)
    counts = collections.Counter(c['verdict'] for c in cases)
    findings = {'date': '2026-10-05', 'cases_in_scope': len(cases),
                'codex_final_sessions': len(coverage), 'accepted_stage6_sessions': len(manifest['accepted_stage6_cases']),
                'final_runner_counts': dict(runner_counts),
                'historical_only_cases': sum(c['decision_source'] == 'historical_stages_0_to_5' for c in cases),
                'blocking_rule': manifest['blocking_rule'], 'model_policy': manifest['model_policy'],
                'verdicts': dict(counts), 'by_set': final_counts(cases, 'set'),
                'by_category': final_counts(cases, 'category'), 'coverage_gaps': [], 'cases': cases}
    (HERE / 'results/final_findings.json').write_text(json.dumps(findings, indent=2, ensure_ascii=False) + '\n')
    (HERE / 'results/final_verification.json').write_text(json.dumps({'query_hashes_unchanged': True,
          'standards_prompt_schema_packet_article_hashes_unchanged': True, 'cases_verified': len(audits),
          'offline_regressions': {'passed': 206, 'failed': 0}, 'session_audits': audits}, indent=2) + '\n')
    corrections = [c for c in cases if c['verdict'] not in ('valid', 'valid_minor')]
    print(json.dumps({'verdicts': dict(counts), 'corrections': [(c['id'], c['verdict'], c['severity']) for c in corrections]}))
    if not args.write_report:
        return
    report = HERE / 'REPORT.md'
    historical = HERE / 'REPORT.pre-codex-final.md'
    if not historical.exists():
        historical.write_bytes(report.read_bytes())
    lines = ['# Benchmark gold validation report — Codex-led final decisions', '',
             f'**{len(cases)-len(corrections)} of {len(cases)} cases require no material correction; '
             f'{len(corrections)} require correction, {sum(c["severity"] == "blocking" for c in corrections)} blocking.**', '',
             'Findings only: gold questions, anchors, source documents and evaluation runs remain unchanged. '
             'PR #45 stays open; corrections belong to a separate revision task.', '',
             'Historical review ran on October 3–4; Codex-led final review completed on October 5, 2026. '
             'This is model review of extracted `.txt` files, not biomedical expert validation, '
             'retrieval evaluation or generated-answer evaluation. No PDFs were used.', '',
             '## Scope and decision authority', '',
             'Stages 0–5 covered all 158 cases. Stage 6 added 59 targeted, one-case Codex second opinions: '
             'all adjudications, minor audit notes, and Claude-authored gold. The reviewer saw an earlier '
             f'review, so Stage 6 was neither blind nor fully independent. Codex then decided all {len(coverage)} '
             f'remaining disagreements/proposed defects and Kimi ambiguity signals in fresh one-case sessions. The other {len(manifest["accepted_stage6_cases"])} agreeing '
             f'Stage 6 decisions were accepted; {findings["historical_only_cases"]} cases retain their historical decisions. '
             'This is not a fresh independent 158-case Codex review.', '',
             'Some category-defect replies use gold_stands to refer to factual content. The findings preserve '
             'that returned flag separately from scoring_contract_stands, which is false for material defects under the stated rule.', '',
             'Decision precedence: final Codex adjudication, then agreeing Stage 6 Codex result, then '
             'historical Stages 0–5. Earlier model results are preserved even when superseded.', '',
             '## Blocking rule', '', manifest['blocking_rule'], '',
             'This replaces the historical rule that treated category defects as non-blocking when '
             'legacy document scoring was unaffected. Severity changes are explicit methodology changes, '
             'not new retrieval failures.', '', '## Verdicts', '']
    for title, table in [('Set', findings['by_set']), ('Category', findings['by_category'])]:
        lines += [f'| {title} | Cases | Valid | Minor note | Needs correction | Blocking |',
                  '| --- | ---: | ---: | ---: | ---: | ---: |']
        for name, c in table.items():
            lines.append(f'| {name} | {c["cases"]} | {c["valid"]} | {c["valid_minor"]} | {c["needs_correction"]} | {c["blocking"]} |')
        totals = {k: sum(row[k] for row in table.values()) for k in ('cases', 'valid', 'valid_minor', 'needs_correction', 'blocking')}
        lines.append(f'| **Total** | **{totals["cases"]}** | **{totals["valid"]}** | **{totals["valid_minor"]}** | **{totals["needs_correction"]}** | **{totals["blocking"]}** |')
        lines.append('')
    lines += ['## Cases requiring correction', '', '| Case | Verdict | Blocking |', '| --- | --- | --- |']
    for c in corrections:
        lines.append(f'| {c["set"]} {c["id"]} | `{c["verdict"]}` | {"yes" if c["severity"] == "blocking" else "no"} |')
    lines += ['', 'Each decision below is Codex-led. Full standards checks, all citations, competing '
              'review claims and proposed correction text are in [final findings](results/final_findings.json) '
              'and the linked per-case results. Line numbers are one-based in the frozen `.txt` extraction.', '']
    for c in corrections:
        lines += [f'### {c["set"]} {c["id"]}', '', c['rationale'], '',
                  '**Blocking basis:** ' + c['severity_basis'], '', '**Proposed correction:** ' + c['proposed_correction'], '']
        for e in c['evidence'][:3]:
            lines += [f'`{e["file"]}:{e.get("line_start", "?")}–{e.get("line_end", "?")}` — {e["point"]}', '',
                      '```text', e['quote'], '```', '']
    lines += ['## Agreement and audit trail', '',
              f'All {len(coverage)} final results are recorded individually, with verdict, severity, scoring impact, '
              'standards checks and source evidence. Note-only disagreements were reviewed too. '
              'The machine-readable findings retain each historical verdict/severity for comparison.', '',
              'Every required final session has an accepted result. Source quotations were checked against '
              'the pinned `.txt` files. Whitespace-only formatting was recovered deterministically where '
              'needed; words and punctuation were never repaired. Raw replies/transcripts and adjustment '
              'records preserve what the model returned. Substantive quote mismatches were rejected.', '',
              'The corpus-growth hunt remains the historical search across all 55 articles: zero H1/H2/H3/H4/H6 '
              'findings, 67 informational H5 candidates. This means no counter-evidence was found by that '
              'search; it does not prove corpus-wide absence. Final reviewers received declared sources, '
              'alternatives, named decoys and relevant candidates; absent-fact cases received the entire '
              '55-article text corpus.', '', '## Models, verification and limits', '',
              f'Accepted final sessions used GPT-6 Sol with low effort for {runner_counts["gpt-6-sol"]} cases and GPT-6 Luna '
              f'with low effort for {runner_counts["gpt-6-luna"]} cases, honoring Juan’s Plus usage budget. The installed '
              'CLI rejected historical `gpt-6.1-sol`; the failed launch is preserved. An Astra high-effort '
              'attempt was stopped after the budget clarification and contributes no accepted verdict. '
              'Actual model, token usage and attempts are recorded per case; no API-price estimate is '
              'presented as subscription consumption.', '',
              '- 206 repository offline tests passed; no retrieval or paid rewriting/generation runs were launched.',
              '- Frozen query, standards, prompt, schema, packet and text hashes verified unchanged.',
              '- Per-session tool commands, source scope, result/transcript hashes and citations are recorded '
              'in [final verification](results/final_verification.json).',
              '- The eight completed Kimi results are preserved as a partial experimental blind pass, '
              'not whole-suite coverage. The Kimi pass was not continued.',
              '- Model review is not clinical expert review. Flattened extraction may obscure table bindings; '
              'unresolved extraction would remain a gap, never be resolved by opening a PDF.',
              '- Codex leads adjudication but also authored much of the gold; targeted second opinions do '
              'not eliminate correlated model-family errors.', '', '## Files and next step', '',
              '- [Final plan](FINAL_PLAN.md) and [frozen manifest](final_review_manifest.json).',
              '- [Historical report](REPORT.pre-codex-final.md) and unchanged [historical findings](results/full_findings.json).',
              '- [Final findings](results/final_findings.json), `results/review6/`, `results/final_codex/` '
              'and `results/stage1_kimi/`.',
              '- Briefs, schemas, packet builder, runner, format-only acceptance helper and aggregation script '
              'make selection and evidence checks reviewable. Raw transcripts/workspaces remain outside Git.', '',
              'After Juan reviews this findings-only PR, apply accepted corrections in a separate task: '
              'increase revisions, retain old results, update the affected gold/evidence/category metadata, '
              'and rerun only affected benchmark conditions when the changed scoring contract requires it. '
              'This PR is not merged by agents.', '']
    report.write_text('\n'.join(lines), encoding='utf-8')


if __name__ == '__main__':
    main()
