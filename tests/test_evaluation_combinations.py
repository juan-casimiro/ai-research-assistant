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

    async def test_four_outputs_and_existing_directory_refusal(self):
        with tempfile.TemporaryDirectory() as directory:
            root, benchmark, manifest = self.inputs(directory)
            output = root / 'results'
            async def save_run(args):
                args.output.write_text(json.dumps({'bm25': args.bm25, 'rewrite': args.rewrite}))
                return 0
            runner = AsyncMock(side_effect=save_run)
            with patch.object(combinations.evaluate, 'read_inputs', return_value=(benchmark, manifest, {})), patch.object(combinations, 'run_combination', runner):
                argv = ['--corpus-dir', str(root), '--output-dir', str(output)]
                self.assertEqual(await combinations.main(argv), 0)
                self.assertEqual([json.loads((output / f'eval_results_{name}.json').read_text()) for name, _, _ in combinations.COMBINATIONS],
                                 [{'bm25': b, 'rewrite': r} for _, b, r in combinations.COMBINATIONS])
                original = {p.name: p.read_bytes() for p in output.iterdir()}
                self.assertEqual(await combinations.main(argv), 1)
                self.assertEqual(runner.await_count, 4)
                self.assertEqual({p.name: p.read_bytes() for p in output.iterdir()}, original)

    async def test_failure_stops_before_later_paid_runs(self):
        with tempfile.TemporaryDirectory() as directory:
            root, benchmark, manifest = self.inputs(directory)
            runner = AsyncMock(side_effect=[0, 1])
            with patch.object(combinations.evaluate, 'read_inputs', return_value=(benchmark, manifest, {})), patch.object(combinations, 'run_combination', runner):
                self.assertEqual(await combinations.main(['--corpus-dir', str(root), '--output-dir', str(root / 'results')]), 1)
                self.assertEqual(runner.await_count, 2)
                self.assertFalse(any(call.args[0].rewrite for call in runner.await_args_list))

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
            async def evaluation(args, retrieve, loader):
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
            async def evaluation(args, retrieve, loader):
                return await retrieve('Some test question?', n_results=3)
            with patch.object(llm_client, '_invoke', original_invoke), patch.object(main, 'retrieve', side_effect=lookup), patch.object(combinations.evaluate, 'read_inputs', return_value=(benchmark, manifest, {})), patch.object(combinations.evaluate, 'run_evaluation', side_effect=evaluation):
                with self.assertRaises(RuntimeError): await combinations.run_combination(args)
                self.assertIs(llm_client._invoke, original_invoke)
            row=json.loads((root/'eval_results_rewrite.responses/q001.jsonl').read_text())
            self.assertEqual(row['error_type'], 'RuntimeError')
            self.assertNotIn('response', row)
