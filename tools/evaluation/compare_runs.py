"""Offline comparisons of complete current retrieval evaluation results."""
import argparse
import csv
import io
import json
import math
import shutil
from pathlib import Path

from .scoring import CATEGORIES

METRICS = ('document_coverage', 'evidence_coverage', 'fact_recall', 'distractor_ordering')
DEPTHS = (3, 8)


def unique_ids(values, label):
    if not isinstance(values, list) or not values or any(not isinstance(v, str) or not v for v in values):
        raise ValueError(f'{label}: expected nonempty query IDs')
    if len(set(values)) != len(values):
        raise ValueError(f'{label}: duplicate IDs')
    return set(values)


def metric_value(metrics, name):
    value = metrics[name]
    if name == 'fact_recall':
        if value is None:
            return None
        if type(value) not in (int, float) or not math.isfinite(value) or not 0 <= value <= 1:
            raise ValueError('invalid fact_recall')
        return value
    if value not in ('pass', 'fail', 'not_scored'):
        raise ValueError(f'invalid {name}')
    return None if value == 'not_scored' else int(value == 'pass')


def validate_run(run):
    if run['run_status'] != 'complete' or not isinstance(run['summary'], dict):
        raise ValueError('run must be complete with a summary')
    requested = unique_ids(run['requested_ids'], 'requested_ids')
    executed = unique_ids(run['executed_ids'], 'executed_ids')
    rows = run['results']
    ids = unique_ids([row['id'] for row in rows], 'results')
    if requested != executed or requested != ids:
        raise ValueError('requested/executed/result query sets differ')
    depths = run['config']['depths']
    if len(depths) != 2 or any(type(d) is not int for d in depths) or set(depths) != set(DEPTHS):
        raise ValueError('expected depths 3 and 8')
    hashes = run['input_hashes']
    if not isinstance(hashes, dict) or any(
        not isinstance(hashes.get(k), str) or len(hashes[k]) != 64
        or any(c not in '0123456789abcdef' for c in hashes[k]) for k in ('queries', 'manifest')
    ):
        raise ValueError('missing or invalid input hashes')
    for row in rows:
        if row['category'] not in CATEGORIES:
            raise ValueError(f"{row['id']}: unknown category")
        if {k for k in row if k.startswith('n') and k[1:].isdigit()} != {'n3', 'n8'}:
            raise ValueError(f"{row['id']}: result depths differ")
        for depth in DEPTHS:
            metrics = row[f'n{depth}']['metrics']
            for name in METRICS:
                metric_value(metrics, name)
    return {row['id']: row for row in rows}


def compare_runs(runs):
    """Compare each named experiment to the first run; order of query IDs is immaterial."""
    if len(runs) < 2:
        raise ValueError('at least two runs required')
    indexed = {label: validate_run(run) for label, run in runs.items()}
    baseline = next(iter(runs))
    base = runs[baseline]
    for label, run in runs.items():
        if (run['input_hashes'] != base['input_hashes']
                or set(run['requested_ids']) != set(base['requested_ids'])):
            raise ValueError(f'{label}: incompatible input hashes or query sets')
        for qid, row in indexed[label].items():
            if row['category'] != indexed[baseline][qid]['category']:
                raise ValueError(f'{qid}: category differs')
    changes = []
    for label in list(runs)[1:]:
        for qid in sorted(indexed[baseline]):
            before_row, after_row = indexed[baseline][qid], indexed[label][qid]
            for depth in DEPTHS:
                for metric in METRICS:
                    before = metric_value(before_row[f'n{depth}']['metrics'], metric)
                    after = metric_value(after_row[f'n{depth}']['metrics'], metric)
                    scored = before is not None and after is not None
                    delta = after - before if scored else None
                    change = ('improved' if delta > 0 else 'regressed' if delta < 0 else 'unchanged') if scored else 'not_scored'
                    changes.append(dict(baseline=baseline, experiment=label, id=qid,
                                        category=before_row['category'], depth=depth, metric=metric,
                                        before=before, after=after, delta=delta, change=change))
    summary = []
    categories = sorted({row['category'] for row in indexed[baseline].values()})
    for label in list(runs)[1:]:
        for category in ['all'] + categories:
            for depth in DEPTHS:
                for metric in METRICS:
                    selected = [r for r in changes if r['experiment'] == label and r['depth'] == depth
                                and r['metric'] == metric and (category == 'all' or r['category'] == category)]
                    scored = [r for r in selected if r['change'] != 'not_scored']
                    means = {key: sum(r[key] for r in scored) / len(scored) if scored else None
                             for key in ('before', 'after', 'delta')}
                    summary.append(dict(experiment=label, category=category, depth=depth, metric=metric,
                                        scored=len(scored), excluded=len(selected)-len(scored), **means,
                                        **{key: sum(r['change'] == key for r in scored)
                                           for key in ('improved', 'regressed', 'unchanged')}))
    return dict(baseline=baseline, summary=summary, changes=changes)


def render_summary(report):
    lines = ['# Saved retrieval run comparison', '',
             f"Baseline: `{report['baseline']}`. Each experiment is compared to this baseline.", '',
             'One observed sweep; no statistical significance or generated-answer quality is established.',
             'Evidence coverage measures pinned excerpts; misses do not prove absent semantic support.',
             'Absent-fact cases are not positively scored; false-premise scores measure correction evidence.',
             'Source-conflict scores preserve attributed readings. Rewrites vary independently by depth and run.',
             'Means and deltas use only queries scored in both runs for that metric; excluded cases are counted separately.', '',
             '| Experiment | Category | Depth | Metric | Scored | Excluded | Before % | After % | Delta pp | Improved | Regressed | Unchanged |',
             '| --- | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |']
    for row in report['summary']:
        values = [row[k] for k in ('experiment', 'category', 'depth', 'metric', 'scored', 'excluded')]
        values += ['—' if row[k] is None else f'{100 * row[k]:.2f}' for k in ('before', 'after', 'delta')]
        values += [row[k] for k in ('improved', 'regressed', 'unchanged')]
        lines.append('| ' + ' | '.join(map(str, values)) + ' |')
    return '\n'.join(lines) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('results', nargs='+', type=Path, help='Baseline first, then experiment JSON files')
    parser.add_argument('--check', action='store_true', help='Validate compatibility without writing reports')
    parser.add_argument('--output-dir', type=Path, help='New directory for summary.md and per_query.csv')
    args = parser.parse_args()
    try:
        labels = [p.stem.removeprefix('eval_results_') for p in args.results]
        if len(set(labels)) != len(labels):
            raise ValueError('duplicate run labels (file stems)')
        runs = {label: json.loads(path.read_text(encoding='utf-8')) for label, path in zip(labels, args.results)}
        report = compare_runs(runs)
        if args.check:
            print(f'Compatible: {len(runs)} complete runs, {len(next(iter(runs.values()))["requested_ids"])} queries, depths 3 and 8')
        elif args.output_dir:
            args.output_dir.mkdir(parents=True, exist_ok=False)
            try:
                (args.output_dir / 'summary.md').write_text(render_summary(report), encoding='utf-8')
                output = io.StringIO()
                writer = csv.DictWriter(output, fieldnames=list(report['changes'][0]), lineterminator='\n')
                writer.writeheader()
                writer.writerows(report['changes'])
                (args.output_dir / 'per_query.csv').write_text(output.getvalue(), encoding='utf-8')
            except OSError:
                shutil.rmtree(args.output_dir)
                raise
            print(f'Reports saved to {args.output_dir}')
        else:
            print(render_summary(report), end='')
    except (ValueError, KeyError, TypeError, OSError) as exc:
        parser.exit(1, f'ERROR: {exc}\n')


if __name__ == '__main__':
    main()
