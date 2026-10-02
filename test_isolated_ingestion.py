"""Offline failure-path regressions for isolated benchmark ingestion."""
import json
from pathlib import Path
import runpy
import sys
from tempfile import TemporaryDirectory
from types import ModuleType
import unittest
from unittest.mock import Mock, patch

import eval_benchmark

HELPER = Path(__file__).parent / 'benchmark/cardiology/v1/runs/ingest_isolated.py'


class IsolatedIngestionTests(unittest.TestCase):
    def setUp(self):
        self.temporary = TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)
        self.receipt = self.directory / 'receipt.json'
        self.production = ModuleType('main')
        self.production.collection = Mock()
        self.production.collection.count.return_value = 0
        self.production._load_models_and_index = Mock()
        self.production.embed_model = Mock()
        self.production.reranker = Mock()
        self.production.bm25_documents = ['some chunk']
        self.production.chunk_text = Mock()
        self.production.IngestRequest = Mock()
        self.production.ingest = Mock()

    def execute(self):
        with patch.dict(sys.modules, {'main': self.production}), \
             patch.dict('os.environ', {'SEED_ON_EMPTY': 'false',
                                      'CHROMA_PATH': str(self.directory / 'fresh')}), \
             patch.object(sys, 'argv', [str(HELPER), '--condition', 'C1',
                                       '--receipt', str(self.receipt)]), \
             patch.object(eval_benchmark, 'read_release', return_value=(
                 {}, {}, {}, {'membership_sha256': 'synthetic hash'}, [],
                 {'some source.pdf': 'some text'})), \
             patch.object(eval_benchmark, 'model_fingerprint', return_value={}), \
             patch.object(eval_benchmark, 'verify_collection', return_value={'chunk_count': 1}), \
             patch('subprocess.check_output', return_value='synthetic commit\n'):
            runpy.run_path(str(HELPER), run_name='__main__')

    def test_nonempty_store_stops_before_ingestion(self):
        self.production.collection.count.return_value = 1
        with self.assertRaisesRegex(ValueError, 'must be empty'):
            self.execute()
        self.production.ingest.assert_not_called()
        self.assertEqual(json.loads(self.receipt.read_text())['status'], 'setup')

    def test_bm25_mismatch_retains_setup_receipt(self):
        self.production.bm25_documents = []
        with self.assertRaisesRegex(ValueError, 'BM25 index count'):
            self.execute()
        self.assertEqual(json.loads(self.receipt.read_text())['status'], 'setup')

    def test_failed_atomic_replace_preserves_receipt_and_cleans_temporary(self):
        with patch.object(eval_benchmark.os, 'replace', side_effect=OSError('synthetic disk failure')):
            with self.assertRaisesRegex(OSError, 'synthetic disk failure'):
                self.execute()
        self.assertEqual(json.loads(self.receipt.read_text())['status'], 'setup')
        self.assertEqual(list(self.directory.iterdir()), [self.receipt])

    def test_success_finalizes_complete_receipt(self):
        self.execute()
        self.assertEqual(json.loads(self.receipt.read_text())['status'], 'complete')
        self.production.ingest.assert_called_once()
        self.assertEqual(list(self.directory.iterdir()), [self.receipt])
