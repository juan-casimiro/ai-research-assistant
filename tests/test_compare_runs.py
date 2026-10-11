"""Offline compatibility and paired-metric regression tests."""
import copy
import io
import json
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path

from tools.evaluation.compare_runs import compare_runs, main


def test_run():
    metrics = dict(document_coverage='fail', evidence_coverage='fail', fact_recall=0.5,
                   distractor_ordering='not_scored')
    return dict(run_status='complete', requested_ids=['test-q1', 'test-q2'],
                executed_ids=['test-q1', 'test-q2'], input_hashes=dict(queries='a'*64, manifest='b'*64),
                config=dict(depths=[3, 8], bm25=False, rewrite=False), summary={}, results=[
                    dict(id='test-q1', category='direct_lookup', n3=dict(metrics=copy.deepcopy(metrics)),
                         n8=dict(metrics=copy.deepcopy(metrics))),
                    dict(id='test-q2', category='unanswerable', **{f'n{d}': dict(metrics=dict(
                        document_coverage='not_scored', evidence_coverage='not_scored',
                        fact_recall=None, distractor_ordering='not_scored')) for d in (3, 8)})])


class CompareRunsTests(unittest.TestCase):
    def test_changes_denominators_and_config_differences(self):
        base = test_run()
        experiment = copy.deepcopy(base)
        experiment['config'].update(bm25=True, rewrite=True)
        experiment['models'] = {'rewrite': 'some test provider'}
        experiment['results'].reverse()
        experiment['requested_ids'].reverse()
        experiment['executed_ids'].reverse()
        experiment['results'][1]['n3']['metrics'].update(document_coverage='pass', fact_recall=0.25)
        report = compare_runs(dict(baseline=base, experiment=experiment))
        rows = {r['metric']: r for r in report['summary'] if r['category'] == 'all' and r['depth'] == 3}
        self.assertEqual((rows['document_coverage']['scored'], rows['document_coverage']['excluded'],
                          rows['document_coverage']['improved']), (1, 1, 1))
        self.assertEqual(rows['fact_recall']['regressed'], 1)
        self.assertEqual(rows['fact_recall']['delta'], -0.25)
        self.assertEqual(rows['evidence_coverage']['unchanged'], 1)
        self.assertEqual(rows['distractor_ordering']['scored'], 0)
        self.assertIsNone(rows['distractor_ordering']['after'])
        self.assertEqual(len(report['changes']), 16)

    def test_reject_incompatible_or_incomplete_runs(self):
        mutations = [
            lambda r: r.update(run_status='incomplete'),
            lambda r: r.update(summary=None),
            lambda r: r['requested_ids'].append('test-q1'),
            lambda r: r['executed_ids'].append('test-q1'),
            lambda r: r['results'].append(copy.deepcopy(r['results'][0])),
            lambda r: r['executed_ids'].pop(),
            lambda r: r['requested_ids'].append('test-q3'),
            lambda r: r['input_hashes'].update(queries='c'*64),
            lambda r: r['input_hashes'].pop('manifest'),
            lambda r: r['config'].update(depths=[3]),
            lambda r: r['config'].update(depths=[3, 3, 8]),
            lambda r: r['results'][0].pop('n8'),
            lambda r: r['results'][0].update(n10=r['results'][0]['n8']),
            lambda r: r['results'][0].update(category='multi_hop'),
            lambda r: r['results'][0]['n3']['metrics'].pop('fact_recall'),
            lambda r: r['results'][0]['n3']['metrics'].update(fact_recall=float('nan')),
            lambda r: r['results'][0]['n3']['metrics'].update(fact_recall=True),
            lambda r: r['results'][0]['n3']['metrics'].update(document_coverage='unknown'),
        ]
        for index, mutate in enumerate(mutations):
            with self.subTest(index=index):
                experiment = test_run()
                mutate(experiment)
                with self.assertRaises((ValueError, KeyError)):
                    compare_runs(dict(baseline=test_run(), experiment=experiment))

    def test_mismatched_scoring_is_excluded_per_metric(self):
        experiment = test_run()
        experiment['results'][0]['n3']['metrics']['fact_recall'] = None
        report = compare_runs(dict(baseline=test_run(), experiment=experiment))
        recall = next(r for r in report['summary'] if r['category'] == 'all'
                      and r['depth'] == 3 and r['metric'] == 'fact_recall')
        self.assertEqual((recall['scored'], recall['excluded']), (0, 2))
        self.assertIsNone(recall['delta'])

    def test_cli_reports_and_refuses_existing_destination(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            paths = [root / name for name in ('baseline.json', 'experiment.json')]
            for path in paths:
                path.write_text(json.dumps(test_run()))
            output = root / 'reports'
            command = [sys.executable, '-m', 'tools.evaluation.compare_runs', *map(str, paths)]
            checked = subprocess.run(command + ['--check'], capture_output=True, text=True)
            self.assertEqual(checked.returncode, 0, checked.stderr)
            self.assertFalse(output.exists())
            completed = subprocess.run(command + ['--output-dir', str(output)], capture_output=True, text=True)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertEqual({p.name for p in output.iterdir()}, {'summary.md', 'per_query.csv'})
            self.assertNotIn(b'\r', (output / 'per_query.csv').read_bytes())
            original = (output / 'per_query.csv').read_bytes()
            repeated = subprocess.run(command + ['--output-dir', str(output)], capture_output=True, text=True)
            self.assertEqual(repeated.returncode, 1)
            self.assertEqual((output / 'per_query.csv').read_bytes(), original)

    def test_failed_report_write_removes_own_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            paths = [root / name for name in ('baseline.json', 'experiment.json')]
            for path in paths:
                path.write_text(json.dumps(test_run()))
            output = root / 'reports'
            with patch.object(sys, 'argv', ['compare_runs', *map(str, paths), '--output-dir', str(output)]), \
                    patch.object(Path, 'write_text', side_effect=OSError('synthetic write failure')), \
                    patch('sys.stderr', new_callable=io.StringIO):
                with self.assertRaises(SystemExit) as raised:
                    main()
            self.assertEqual(raised.exception.code, 1)
            self.assertFalse(output.exists())
            self.assertTrue(all(path.exists() for path in paths))

    def test_saved_mvp_runs(self):
        folder = Path(__file__).resolve().parents[1] / 'data/evaluations/mvp/2026-10-09-anthropic'
        runs = {name: json.loads((folder / f'eval_results_{name}.json').read_text())
                for name in ('baseline', 'bm25', 'rewrite', 'bm25_rewrite')}
        report = compare_runs(runs)
        self.assertEqual(len(report['changes']), 3 * 158 * 2 * 4)
        coverage = next(r for r in report['summary'] if r['experiment'] == 'bm25_rewrite'
                        and r['category'] == 'all' and r['depth'] == 8 and r['metric'] == 'evidence_coverage')
        self.assertEqual(coverage['scored'], 147)
        self.assertAlmostEqual(coverage['before'], 43/147)
        self.assertAlmostEqual(coverage['after'], 50/147)
