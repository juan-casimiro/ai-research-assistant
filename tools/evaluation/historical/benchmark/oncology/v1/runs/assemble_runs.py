"""Assemble disjoint saved subsets; no models or retrieval. Run from repo root."""
import copy
import hashlib
import json
from pathlib import Path

from benchmark_scoring import canonical_hash
from eval_benchmark import summarize

R = Path('benchmark/oncology/v1/runs')
benchmark = json.loads((R.parent / 'queries.json').read_text())
order = {q['id']: i for i, q in enumerate(benchmark['queries'])}
for condition in ['C1', 'C2']:
    paths = [R / f'{condition}-{part}.json' for part in ['focused', 'remaining']]
    parents = [json.loads(p.read_text()) for p in paths]
    assert all(p['run_status'] == 'complete' and not p['provenance']['missing_ids'] for p in parents)
    for field in ['query_sha256', 'scorer_sha256', 'retrieval_sha256', 'selection_sha256',
                  'conditions_sha256', 'membership_sha256', 'loaded_models', 'ingestion_verification']:
        assert parents[0]['provenance'][field] == parents[1]['provenance'][field], field
    results = [v for p in parents for v in p['results']]
    assert len(results) == len(order) and {v['id'] for v in results} == set(order)
    results.sort(key=lambda v: order[v['id']])
    out = copy.deepcopy(parents[0])
    out.update(results=results, run_id=f'20261003-{condition}-assembled',
               artifact_kind='assembled disjoint retrieval subsets; no new retrieval',
               parents=[{'path': str(p), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest(),
                         'run_id': v['run_id']} for p, v in zip(paths, parents)],
               summary=summarize(results))
    provenance = out['provenance']
    provenance['requested_ids'] = provenance['executed_ids'] = sorted(order)
    provenance['subset_sha256'] = canonical_hash(benchmark['queries'])
    provenance['feasibility_sha256'] = canonical_hash({v['id']: v['evidence_feasibility'] for v in results})
    path = R / f'{condition}-complete.json'
    if path.exists():
        assert json.loads(path.read_text()) == out, f'{path}: assembled content differs'
    else:
        path.write_text(json.dumps(out, indent=2, ensure_ascii=False) + '\n')
    print(f'{condition}: {len(results)} disjoint saved cases verified')
