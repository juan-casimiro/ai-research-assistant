"""Accept an existing reply after format-only repair; never rerun or adjudicate."""
from __future__ import annotations
import argparse
import json
import shutil
from pathlib import Path
from run_stage import check_quotes, schema_errors, source_quote, usage_records
from stage0 import HERE, load


def canonical_reply(reply, articles):
    schema = load(HERE / 'schemas/stage7_final.schema.json')
    errors = schema_errors(reply, schema)
    if errors:
        raise ValueError('; '.join(errors))
    changes = []
    for item in reply['evidence']:
        original_name, original_quote = item['file'], item['quote']
        parts = Path(original_name).parts
        if len(parts) == 2 and parts[0] == 'articles':
            item['file'] = parts[1]
        name = item['file']
        if Path(name).name != name or not name.endswith('.txt') or not (articles / name).is_file():
            raise ValueError(f'out-of-scope source: {original_name}')
        exact = source_quote(original_quote, (articles / name).read_text())
        if exact is None:
            raise ValueError(f'source words/punctuation differ: {name}')
        item['quote'] = exact
        if original_name != name or original_quote != exact:
            changes.append({'file_as_returned': original_name, 'quote_as_returned': original_quote,
                            'file': name, 'source_quote': exact, 'reason': 'source_path_or_whitespace_only'})
    for i, name in enumerate(reply['articles_read']):
        parts = Path(name).parts
        if len(parts) == 2 and parts[0] == 'articles':
            name = parts[1]
        if Path(name).name != name or not (articles / name).is_file():
            raise ValueError(f'out-of-scope article read: {name}')
        reply['articles_read'][i] = name
    if not reply['evidence']:
        raise ValueError('no evidence')
    if reply['own_verdict'] == 'defect_category' and reply['own_severity'] != 'blocking':
        raise ValueError('category defect violates documented blocking rule')
    if reply['own_verdict'] == 'valid' and reply['own_severity'] != 'none':
        raise ValueError('valid result has non-none severity')
    return reply, changes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workspace-root', type=Path, required=True)
    parser.add_argument('--case', required=True)
    args = parser.parse_args()
    manifest = load(HERE / 'final_review_manifest.json')
    batch = next(b for b in manifest['stage7_final'] if b['cases'] == [args.case])
    out = HERE / 'results/final_codex' / (batch['batch_id'] + '.json')
    if out.exists():
        raise SystemExit('accepted result already exists; preserve it')
    run = args.workspace_root / 'jua-106-runs/final_codex'
    articles = args.workspace_root / 'jua-106-final-ws' / args.case / 'articles'
    for attempt in (2, 1):
        path = run / f"{batch['batch_id']}.attempt{attempt}.reply.json"
        if not path.exists():
            continue
        try:
            reply, changes = canonical_reply(load(path), articles)
            if reply['id'] != args.case:
                raise ValueError('different case')
        except ValueError as error:
            print(f'{path.name}: {error}')
            continue
        trace = run / f"{batch['batch_id']}.attempt{attempt}.transcript"
        gap = out.with_suffix('.gap.json')
        record = {'batch_id': batch['batch_id'], 'stage': 'stage7_final', 'group': 'final_codex',
                  'runner': batch['runner'], 'attempts': attempt, 'duration_s': None,
                  'acceptance': 'revalidated existing reply; no model call, no semantic repair',
                  'prior_gap': load(gap) if gap.exists() else None,
                  'quote_adjustments': changes, 'quotes': check_quotes(reply, articles),
                  'usage': usage_records(trace.read_text()),
                  'transcript': str(trace.relative_to(args.workspace_root)), 'output': reply}
        out.write_text(json.dumps(record, indent=2, ensure_ascii=False) + '\n')
        if gap.exists():
            target = HERE / 'results/final_format_rejections'
            target.mkdir(exist_ok=True)
            shutil.move(str(gap), str(target / gap.name))
        print(json.dumps({'case': args.case, 'accepted_attempt': attempt, 'format_adjustments': len(changes)}))
        return
    raise SystemExit('No acceptable existing reply; substantive or coverage gap remains')


if __name__ == '__main__':
    main()
