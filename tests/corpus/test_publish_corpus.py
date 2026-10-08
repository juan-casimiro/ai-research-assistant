"""Publication gate: all validation first, conflicts abort, promotion rolls back."""
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from tools.corpus import publish_corpus as publisher
from tests.corpus.test_build_corpus_manifest import record
from tests.corpus.test_extract_corpus_text import pdf_bytes


class PublicationTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.run = self.root / 'build/corpus/synthetic-run'
        (self.run / 'pdfs').mkdir(parents=True)
        self.article = record()
        self.article['metadata_sources'] = {'pdf': {'url': publisher.BUCKET + '/PMC123456.2/synthetic.pdf'}}
        self.source = self.run / 'corpus_manifest.json'
        self.source.write_text(json.dumps({'articles': [self.article]}))
        (self.run / 'candidates.json').write_text(self.source.read_text())
        self.pdf = self.run / 'pdfs' / self.article['filename']
        self.pdf.write_bytes(pdf_bytes())
        self.final_manifest = self.root / 'data/corpus_manifest.json'
        self.final_pdfs = self.root / 'corpus/mvp'

    def run_tool(self, check=False):
        args = ['--run-dir', str(self.run), '--manifest-destination', str(self.final_manifest), '--pdf-destination', str(self.final_pdfs)]
        if check:
            args.append('--check')
        with contextlib.redirect_stdout(io.StringIO()):
            return publisher.main(args)

    def test_success_moves_only_final_artifacts_after_validation(self):
        raw = self.pdf.read_bytes()
        self.assertEqual(self.run_tool(check=True), 0)
        self.assertFalse(self.final_manifest.exists())
        self.assertTrue(self.pdf.exists())
        self.assertEqual(self.run_tool(), 0)
        self.assertEqual((self.final_pdfs / self.pdf.name).read_bytes(), raw)
        article = json.loads(self.final_manifest.read_text())['articles'][0]
        self.assertEqual(article['metadata_sources']['pdf']['sha256'], publisher.digest(raw))
        self.assertFalse(self.pdf.exists())
        self.assertFalse(self.source.exists())
        self.assertTrue((self.run / 'extracted_text/index.json').exists())

    def test_conflicting_manifest_or_pdf_leaves_everything_intact(self):
        for kind in ['manifest', 'pdf']:
            with self.subTest(kind=kind):
                if kind == 'manifest':
                    self.final_manifest.parent.mkdir(parents=True)
                    self.final_manifest.write_text(json.dumps({'articles': []}))
                    before = self.final_manifest.read_bytes()
                else:
                    self.final_manifest.unlink()
                    self.final_pdfs.mkdir(parents=True)
                    (self.final_pdfs / self.pdf.name).write_bytes(b'conflicting existing bytes')
                self.assertEqual(self.run_tool(), 1)
                self.assertTrue(self.pdf.exists())
                self.assertTrue(self.source.exists())
                report = json.loads((self.run / 'publication_report.json').read_text())
                self.assertFalse(report['published'])
                self.assertTrue(report['failures'])
                if kind == 'manifest':
                    self.assertEqual(self.final_manifest.read_bytes(), before)
                    self.assertFalse(self.final_pdfs.exists())
                else:
                    self.assertEqual((self.final_pdfs / self.pdf.name).read_bytes(), b'conflicting existing bytes')
                    self.assertFalse(self.final_manifest.exists())

    def test_invalid_selection_metadata_or_extraction_never_publishes(self):
        for kind in ['selection', 'metadata', 'extraction']:
            with self.subTest(kind=kind):
                self.source.write_text(json.dumps({'articles': [self.article]}))
                selection = dict(self.article, pmcid='PMC999', filename='PMC999-synthetic-study.pdf') if kind == 'selection' else self.article
                (self.run / 'candidates.json').write_text(json.dumps({'articles': [selection]}))
                self.pdf.write_bytes(pdf_bytes(('',)) if kind == 'extraction' else pdf_bytes())
                if kind == 'metadata':
                    invalid = dict(self.article, abstract='')
                    self.source.write_text(json.dumps({'articles': [invalid]}))
                self.assertEqual(self.run_tool(), 1)
                self.assertFalse(self.final_manifest.exists())
                self.assertFalse(self.final_pdfs.exists())
                self.assertTrue(self.source.exists())
                self.assertTrue(self.pdf.exists())

    def test_matching_destinations_are_preserved(self):
        raw = self.pdf.read_bytes()
        manifest = {'articles': [dict(self.article, metadata_sources={'pdf': {'url': self.article['metadata_sources']['pdf']['url'], 'sha256': publisher.digest(raw)}})]}
        self.final_manifest.parent.mkdir(parents=True)
        self.final_manifest.write_text(json.dumps(manifest))
        before = self.final_manifest.read_bytes()
        self.final_pdfs.mkdir(parents=True)
        (self.final_pdfs / self.pdf.name).write_bytes(raw)
        self.assertEqual(self.run_tool(), 0)
        self.assertEqual(self.final_manifest.read_bytes(), before)
        self.assertEqual((self.final_pdfs / self.pdf.name).read_bytes(), raw)

    def test_provider_checksum_mismatch_aborts_before_publication(self):
        self.article['metadata_sources']['pdf']['md5'] = '0' * 32
        self.source.write_text(json.dumps({'articles': [self.article]}))
        self.assertEqual(self.run_tool(), 1)
        self.assertFalse(self.final_pdfs.exists())
        self.assertFalse(self.final_manifest.exists())
        self.assertIn('MD5 mismatch', json.loads((self.run / 'publication_report.json').read_text())['failures'][0]['reason'])

    def test_manifest_write_failure_rolls_back_new_pdf_directory(self):
        with patch.object(publisher, 'atomic_write', side_effect=OSError('synthetic manifest-write failure')):
            self.assertEqual(self.run_tool(), 1)
        self.assertFalse(self.final_pdfs.exists())
        self.assertFalse(self.final_manifest.exists())
        self.assertTrue(self.pdf.exists())
        self.assertTrue(self.source.exists())
