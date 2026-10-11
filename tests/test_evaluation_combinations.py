"""Verify batch failure handling and complete response capture without paid calls."""
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import AsyncMock, patch

from langchain_core.messages import AIMessage
from tools.evaluation import evaluate_combinations as combinations
import llm_client


class CombinationTests(unittest.IsolatedAsyncioTestCase):
    def inputs(self, directory):
        root = Path(directory)
        (root / 'chroma').mkdir()
        return root, {'queries': [{'id': 'q001', 'question': 'Some test question?'}]}, {'corpus_name': 'some-test-corpus'}

    def result(self, args, inputs):
        return {'run_status': 'complete', 'summary': {}, 'requested_ids': ['q001'],
                'executed_ids': ['q001'], 'results': [{'id': 'q001', 'n3': {}, 'n8': {}}],
                'config': {'bm25': args.bm25, 'rewrite': args.rewrite, 'depths': [3, 8]},
                'input_hashes': {'queries': combinations.evaluate.canonical_hash(inputs[0]),
                                 'manifest': combinations.evaluate.canonical_hash(inputs[1])}}

    async def test_default_layout_and_unique_runs(self):
        with tempfile.TemporaryDirectory() as directory:
            root, benchmark, manifest = self.inputs(directory)
            async def save_run(args, *, inputs=None):
                args.output.write_text(json.dumps(self.result(args, inputs)))
                return 0
            with patch.object(combinations.evaluate, 'ROOT', root), patch.object(combinations.evaluate, 'read_inputs', return_value=(benchmark, manifest, {})), patch.object(combinations, 'run_combination', side_effect=save_run):
                for _ in range(2):
                    self.assertEqual(await combinations.main(['--corpus-dir', str(root)]), 0)
            staged=list((root/'build/corpus/evaluation-runs/some-test-corpus').iterdir())
            final=list((root/'data/evaluations/some-test-corpus').iterdir())
            self.assertEqual(len(staged), 2)
            self.assertEqual({p.name for p in staged}, {p.name for p in final})
            self.assertTrue(all(p.name.endswith('Z') for p in staged))
            self.assertTrue(all(len(list(p.iterdir())) == 4 for p in final))

    async def test_incomplete_results_are_not_published(self):
        with tempfile.TemporaryDirectory() as directory:
            root, benchmark, manifest = self.inputs(directory)
            async def save_run(args, *, inputs=None):
                result=self.result(args, inputs)
                result['run_status']='incomplete'
                args.output.write_text(json.dumps(result))
                return 0
            with patch.object(combinations.evaluate, 'ROOT', root), patch.object(combinations.evaluate, 'read_inputs', return_value=(benchmark, manifest, {})), patch.object(combinations, 'run_combination', side_effect=save_run):
                self.assertEqual(await combinations.main(['--corpus-dir', str(root), '--output-dir', str(root/'final')]), 1)
            self.assertFalse((root/'final').exists())
            self.assertEqual(len(list((root/'build').rglob('eval_results_*.json'))), 4)

    def test_copy_failure_retains_staged_results(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            stage=root/'stage'
            stage.mkdir()
            inputs=({'queries': []}, {'corpus_name': 'some-test-corpus'}, {})
            for name, bm25, rewrite in combinations.COMBINATIONS:
                (stage/f'eval_results_{name}.json').write_text(json.dumps(self.result(SimpleNamespace(bm25=bm25, rewrite=rewrite), inputs)))
            with patch.object(combinations.shutil, 'copy2', side_effect=OSError('some copy failure')):
                with self.assertRaises(OSError): combinations.publish_results(stage, root/'final', {'q001'}, inputs)
            self.assertFalse((root/'final').exists())
            self.assertEqual(len(list(stage.iterdir())), 4)

    async def test_four_outputs_and_existing_directory_refusal(self):
        with tempfile.TemporaryDirectory() as directory:
            root, benchmark, manifest = self.inputs(directory)
            output = root / 'results'
            async def save_run(args, *, inputs=None):
                args.output.write_text(json.dumps(self.result(args, inputs)))
                args.output.with_suffix('.responses').mkdir()
                (args.output.with_suffix('.responses')/'q001.jsonl').write_text('local log')
                return 0
            runner = AsyncMock(side_effect=save_run)
            with patch.object(combinations.evaluate, 'ROOT', root), patch.object(combinations.evaluate, 'read_inputs', return_value=(benchmark, manifest, {})), patch.object(combinations, 'run_combination', runner):
                argv = ['--corpus-dir', str(root), '--output-dir', str(output)]
                self.assertEqual(await combinations.main(argv), 0)
                self.assertEqual([json.loads((output / f'eval_results_{name}.json').read_text()) for name, _, _ in combinations.COMBINATIONS],
                                 [self.result(SimpleNamespace(bm25=b, rewrite=r), (benchmark, manifest, {})) for _, b, r in combinations.COMBINATIONS])
                original = {p.name: p.read_bytes() for p in output.iterdir()}
                self.assertEqual(await combinations.main(argv), 1)
                self.assertEqual(runner.await_count, 4)
                self.assertEqual({p.name: p.read_bytes() for p in output.iterdir()}, original)

    async def test_failure_stops_before_later_paid_runs(self):
        with tempfile.TemporaryDirectory() as directory:
            root, benchmark, manifest = self.inputs(directory)
            runner = AsyncMock(side_effect=[0, 1])
            with patch.object(combinations.evaluate, 'ROOT', root), patch.object(combinations.evaluate, 'read_inputs', return_value=(benchmark, manifest, {})), patch.object(combinations, 'run_combination', runner):
                self.assertEqual(await combinations.main(['--corpus-dir', str(root), '--output-dir', str(root / 'results')]), 1)
                self.assertEqual(runner.await_count, 2)
                self.assertFalse(any(call.args[0].rewrite for call in runner.await_args_list))
                self.assertFalse((root/'results').exists())
                self.assertEqual(len(list((root/'build/corpus/evaluation-runs/some-test-corpus').iterdir())), 1)

    async def test_capture_preserves_messages_usage_and_restores_hook(self):
        import main
        with tempfile.TemporaryDirectory() as directory:
            root, benchmark, manifest = self.inputs(directory)
            args = SimpleNamespace(queries=root/'queries.json', manifest=root/'manifest.json', corpus_dir=root,
                                   ids='q001', rewrite=True, output=root/'eval_results_rewrite.json')
            message = AIMessage(content='Some full rewritten query.\nSecond line.',
                                response_metadata={'stop_reason': 'end_turn'},
                                usage_metadata={'input_tokens': 10, 'output_tokens': 5, 'total_tokens': 15})
            original_invoke = AsyncMock(return_value=message)
            prompts = [{'role': 'user', 'content': 'Some test question?'}]
            async def lookup(question, **kwargs):
                await llm_client._invoke(None, prompts, 10)
                return ['Some test context'], ['some-source.pdf']
            async def evaluation(args, retrieve, loader, *, inputs=None):
                for depth in (3, 8): await retrieve('Some test question?', n_results=depth)
                return 0
            with patch.object(llm_client, '_invoke', original_invoke), patch.object(main, 'retrieve', side_effect=lookup), patch.object(combinations.evaluate, 'read_inputs', return_value=(benchmark, manifest, {})), patch.object(combinations.evaluate, 'run_evaluation', side_effect=evaluation):
                self.assertEqual(await combinations.run_combination(args), 0)
                self.assertIs(llm_client._invoke, original_invoke)
                self.assertEqual(original_invoke.await_count, 2)
            rows = [json.loads(line) for line in (root/'eval_results_rewrite.responses/q001.jsonl').read_text().splitlines()]
            self.assertEqual([r['depth'] for r in rows], [3, 8])
            for record in rows:
                self.assertEqual(record['request_messages'], prompts)
                self.assertEqual(record['response']['content'], message.content)
                self.assertEqual(record['response']['usage_metadata'], message.usage_metadata)

    async def test_capture_restores_hook_and_preserves_error_record(self):
        import main
        with tempfile.TemporaryDirectory() as directory:
            root, benchmark, manifest = self.inputs(directory)
            args = SimpleNamespace(queries=root/'queries.json', manifest=root/'manifest.json', corpus_dir=root,
                                   ids='q001', rewrite=True, output=root/'eval_results_rewrite.json')
            original_invoke = AsyncMock(side_effect=RuntimeError('some synthetic failure'))
            async def lookup(question, **kwargs):
                return await llm_client._invoke(None, [], 10)
            async def evaluation(args, retrieve, loader, *, inputs=None):
                return await retrieve('Some test question?', n_results=3)
            with patch.object(llm_client, '_invoke', original_invoke), patch.object(main, 'retrieve', side_effect=lookup), patch.object(combinations.evaluate, 'read_inputs', return_value=(benchmark, manifest, {})), patch.object(combinations.evaluate, 'run_evaluation', side_effect=evaluation):
                with self.assertRaises(RuntimeError): await combinations.run_combination(args)
                self.assertIs(llm_client._invoke, original_invoke)
            row=json.loads((root/'eval_results_rewrite.responses/q001.jsonl').read_text())
            self.assertEqual(row['error_type'], 'RuntimeError')
            self.assertNotIn('response', row)

    async def test_missing_or_duplicate_response_stops_at_first_depth(self):
        import main
        for duplicate in (False, True):
            with self.subTest(duplicate=duplicate), tempfile.TemporaryDirectory() as directory:
                root, benchmark, manifest = self.inputs(directory)
                args = SimpleNamespace(queries=root/'queries.json', manifest=root/'manifest.json', corpus_dir=root,
                                       ids='q001', rewrite=True, output=root/'eval_results_rewrite.json')
                original = AsyncMock(return_value=AIMessage(content='Some rewritten query'))
                depths=[]
                async def lookup(question, **kwargs):
                    depths.append(kwargs['n_results'])
                    if duplicate:
                        await llm_client._invoke(None, [], 10)
                        await llm_client._invoke(None, [], 10)
                    return [], []
                async def evaluation(args, retrieve, loader, *, inputs=None):
                    for depth in (3, 8): await retrieve('Some test question?', n_results=depth)
                    return 0
                with patch.object(llm_client, '_invoke', original), patch.object(main, 'retrieve', side_effect=lookup), patch.object(combinations.evaluate, 'read_inputs', return_value=(benchmark, manifest, {})), patch.object(combinations.evaluate, 'run_evaluation', side_effect=evaluation):
                    with self.assertRaises(ValueError): await combinations.run_combination(args)
                    self.assertIs(llm_client._invoke, original)
                self.assertEqual(depths, [3])
                self.assertEqual(original.await_count, 1 if duplicate else 0)

    async def test_real_evaluator_reuses_inputs_and_records_actual_default(self):
        import main
        from tests.test_evaluation import EvaluationRunTests
        from llm_client import DEFAULT_MODELS_BY_PROVIDER
        with tempfile.TemporaryDirectory() as directory:
            args, article, text = EvaluationRunTests().inputs(directory)
            output=Path(directory)/'batch'
            manifest=json.loads(args.manifest.read_text())
            manifest['corpus_name']='some-test-corpus'
            args.manifest.write_text(json.dumps(manifest))
            collection=SimpleNamespace(get=lambda **kw: {'documents': [text], 'metadatas': [{'source': article['filename']}]})
            original=AsyncMock(return_value=AIMessage(content='Some rewritten query'))
            async def lookup(question, **kwargs):
                if kwargs['use_query_rewriting']: await llm_client._invoke(None, [{'role': 'user', 'content': question}], 10)
                return [text], [article['filename']]
            with patch.object(combinations.evaluate, 'ROOT', Path(directory)), patch.dict('os.environ', {'LLM_PROVIDER': ' ANTHROPIC ', 'LLM_MODEL': 'some-not-used-model'}), patch.object(main, 'collection', collection), patch.object(main, '_load_models_and_index'), patch.object(main, 'chunk_text', side_effect=lambda s: [s]), patch.object(main, 'retrieve', side_effect=lookup), patch.object(llm_client, '_invoke', original), patch.object(combinations.evaluate, 'read_inputs', wraps=combinations.evaluate.read_inputs) as read_inputs:
                self.assertEqual(await combinations.main(['--queries', str(args.queries), '--manifest', str(args.manifest), '--corpus-dir', str(args.corpus_dir), '--output-dir', str(output)]), 0)
                self.assertEqual(read_inputs.call_count, 1)
                self.assertEqual(original.await_count, 4)
            for name in ('rewrite', 'bm25_rewrite'):
                result=json.loads((output/f'eval_results_{name}.json').read_text())
                self.assertEqual(result['run_status'], 'complete')
                self.assertEqual(result['models']['rewrite']['model'], DEFAULT_MODELS_BY_PROVIDER['anthropic'])
                run_dir=next((Path(directory)/'build/corpus/evaluation-runs/some-test-corpus').iterdir())
                rows=[json.loads(line) for line in (run_dir/f'eval_results_{name}.responses/some-case.jsonl').read_text().splitlines()]
                self.assertEqual(len(list(output.iterdir())), 4)
                self.assertTrue(all(row['model']==DEFAULT_MODELS_BY_PROVIDER['anthropic'] for row in rows))
