"""Build isolated, one-case Codex final-review packets without changing gold."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path

from assemble import gold_records
from build_review import first_review
from stage0 import HERE, ROOT, SETS, load

RULE = ('Blocking means a defect can cause a correct answer to be scored incorrectly '
        '(including a wrong answer accepted), makes the question materially ambiguous, '
        'or violates the category admission criterion used for benchmark scoring. '
        'Category defects are blocking even when legacy document-only scoring ignores them. '
        'A valid_minor note is non_blocking only if none of those conditions applies; '
        'valid has severity none. Unsettled extraction is a blocking validation gap, '
        'not a proven source defect. Evaluate the declared fact/evidence/category contract, '
        'not hypothetical lenient scoring or whether a blind model happened to answer fully.')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--corpus-dir', type=Path, required=True)
    parser.add_argument('--workspace-root', type=Path, required=True)
    parser.add_argument('--supplemental-kimi', action='store_true', help='Append c003/c006 ambiguity signals from the retained experimental pass')
    args = parser.parse_args()
    corpus, ws = args.corpus_dir.resolve(), args.workspace_root.resolve()
    if not args.supplemental_kimi and (HERE / 'final_review_manifest.json').exists():
        raise SystemExit('Frozen manifest already exists; use it for replay rather than overwriting it.')
    records = gold_records(corpus)
    previous = {c['id']: c for c in load(HERE / 'results/full_findings.json')['cases']}
    second = {p.stem.removeprefix('review6-'): load(p) for p in (HERE / 'results/review6').glob('*.json')}
    kimi = {c['id']: c for f in (HERE / 'results/stage1_kimi').glob('*.json') for c in load(f)['output']['cases']}
    if args.supplemental_kimi:
        second = {cid: second.get(cid) for cid in ('c003', 'c006')}
    inventory = load(corpus / 'inventory.json')['articles']
    articles = {Path(a['txt']['path']).name: corpus / a['txt']['path'] for a in inventory}
    standards = (ROOT / 'benchmark/STANDARDS.md').read_text()
    criteria = standards[standards.index('## Query and evidence schema'):standards.index('## Metrics:')]
    criteria += '\n' + standards[standards.index('## Versioning,'):standards.index('### Run record')]
    selected, accepted = [], []
    for case_id, record in sorted(second.items()):
        case, result = previous[case_id], record['output'] if record else None
        reasons = ['experimental_kimi_ambiguity'] if args.supplemental_kimi else []
        if result and result['agreement'] != 'agree':
            reasons.append('verdict_severity_or_correction_disagreement')
        if case['verdict'] not in ('valid', 'valid_minor') or (result and result['own_verdict'] not in ('valid', 'valid_minor')):
            reasons.append('defect_requires_consistent_blocking_rule')
        if record and record['quotes']['verified'] != record['quotes']['total']:
            reasons.append('unverified_prior_quote')
        if not reasons:
            accepted.append(case_id)
            continue
        gold = records[case_id]['gold']
        review, why = first_review(case)
        files = {f for names in gold['dependencies'].values() for f in names}
        files |= {a['file'] for a in gold['anchors']}
        for evidence in review['evidence'] + (result['evidence'] if result else []):
            files.add(evidence['file'])
        # A named competing candidate is relevant even if the prior hunt called it informational.
        files |= {Path(f['file']).name for f in (case['hunt'] or {}).get('findings', [])}
        files = {Path(f).name for f in files}
        declared = sorted(files)
        if gold['category'] == 'unanswerable':
            files = set(articles)  # absence is corpus-wide, never source-only
        folder = ws / 'jua-106-final-ws' / case_id
        (folder / 'cases').mkdir(parents=True, exist_ok=True)
        (folder / 'articles').mkdir(exist_ok=True)
        for name in sorted(files):
            if Path(name).name != name or not name.endswith('.txt'):
                raise ValueError(f'unsafe article name: {name}')
            target = folder / 'articles' / name
            if target.exists() and digest(target) != digest(articles[name]):
                raise SystemExit(f'frozen article differs: {target}')
            if not target.exists():
                shutil.copyfile(articles[name], target)
        packet = {**gold, 'set': records[case_id]['set'], 'first_review': {**review, 'why_reviewed': why},
                  'codex_second_opinion': result, 'selection_reasons': reasons,
                  'declared_and_candidate_articles': declared,
                  'available_articles': sorted(files),
                  'prior_corpus_hunt': case['hunt'],
                  'standards_criteria': criteria, 'blocking_rule': RULE}
        if args.supplemental_kimi:
            packet['experimental_kimi_signal'] = kimi[case_id]
        path = folder / 'cases' / f'final-{case_id}.json'
        contents = json.dumps(packet, indent=2, ensure_ascii=False) + '\n'
        if path.exists() and path.read_text() != contents:
            raise SystemExit(f'frozen packet differs: {path}')
        path.write_text(contents)
        selected.append({'batch_id': f'final-{case_id}', 'cases': [case_id], 'selected_for': reasons,
                         'batch_file': str(path.relative_to(ws)), 'input_sha256': digest(path),
                         'article_sha256': {n: digest(folder / 'articles' / n) for n in sorted(files)}})
    plan = {'created_date': '2026-10-05', 'blocking_rule': RULE,
            'selection': 'All Stage 6 disagreements (including notes and corrections), all proposed defects, and unverifiable quotes.',
            'accepted_stage6_cases': accepted, 'stage7_final': selected,
            'runner': {'cli': 'codex', 'model': 'gpt-6-luna', 'reasoning_effort': 'low',
                       'extra_args': ['--ignore-user-config'], 'workspace': 'jua-106-final-ws'},
            'standards_sha256': digest(ROOT / 'benchmark/STANDARDS.md'),
            'query_sha256': {s: digest(ROOT / p) for s, p in SETS.items()},
            'brief_sha256': digest(HERE / 'briefs/stage7_final.md'),
            'schema_sha256': digest(HERE / 'schemas/stage7_final.schema.json')}
    substantive = {'a001', 'a007', 'a009', 'c012', 'c013', 'c016', 'd015', 'd016', 'd020', 'q058'}
    for batch in selected:
        batch['runner'] = {**plan['runner'], 'model': 'gpt-6-sol' if batch['cases'][0] in substantive else 'gpt-6-luna'}
    plan['model_policy'] = 'Plus budget: Luna low for notes; Sol low for proposed defects. No Astra or above-light effort.'
    if args.supplemental_kimi:
        existing = load(HERE / 'final_review_manifest.json')
        have = {b['cases'][0] for b in existing['stage7_final']}
        for batch in selected:
            if batch['cases'][0] not in have:
                batch['runner']['model'] = 'gpt-6-sol'
                existing['stage7_final'].append(batch)
        existing['accepted_stage6_cases'] = [cid for cid in existing['accepted_stage6_cases'] if cid not in {b['cases'][0] for b in selected}]
        existing['supplemental_scope'] = 'c003/c006: unresolved scope ambiguity signals in retained partial Kimi pass; Codex makes final decision in separate sessions.'
        plan = existing
    (HERE / 'final_review_manifest.json').write_text(json.dumps(plan, indent=2) + '\n')
    print(json.dumps({'new_final_sessions': len(selected), 'accepted_existing_sessions': len(accepted),
                      'ids': [b['cases'][0] for b in selected]}))


if __name__ == '__main__':
    main()
