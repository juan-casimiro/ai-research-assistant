"""Metadata-only assembly: no PDF, download or extraction work."""
import contextlib
import copy
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from tools.corpus import build_corpus_manifest as builder


def record():
    return dict(pmcid='PMC123456', pmc_version=2, filename='PMC123456-synthetic-study.pdf',
                id='PMC123456-synthetic-study', article_id='PMC123456-synthetic-study',
                cluster='test-topic', search_query='some discovery query', pmid='987654',
                doi='10.1234/synthetic', title='Synthetic study', journal='Synthetic journal',
                publication_date='2024-07', year=2024, authors=['Ada Example'],
                abstract='Synthetic PubMed abstract.', pubmed_url='https://pubmed.ncbi.nlm.nih.gov/987654/',
                license='CC BY 4.0', licence_urls=['https://creativecommons.org/licenses/by/4.0/'])


class ManifestTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.records = self.root / 'metadata'
        self.records.mkdir()
        self.output = self.root / 'manifest.json'
        self.article = record()
        (self.records / 'article.json').write_text(json.dumps(self.article))

    def run_builder(self, finalize=False):
        args = ['--finalize', str(self.output)] if finalize else ['--records-dir', str(self.records), '--output', str(self.output)]
        with contextlib.redirect_stdout(io.StringIO()) as report:
            status = builder.main(args)
        return status, report.getvalue()

    def test_assembles_existing_records_without_modification(self):
        self.assertEqual(self.run_builder()[0], 0)
        self.assertEqual(json.loads(self.output.read_text()), {'articles': [self.article]})
        before = self.output.read_bytes()
        self.assertEqual(self.run_builder(finalize=True)[0], 0)
        self.assertEqual(self.output.read_bytes(), before)

    def test_mandatory_fields_and_licence_failure_preserve_existing(self):
        for field in ['pmid','doi','title','journal','authors','year','abstract','pubmed_url','id','article_id','licence_urls']:
            with self.subTest(field=field):
                article = copy.deepcopy(self.article)
                del article[field]
                self.output.write_text(json.dumps({'articles':[article]}))
                before = self.output.read_bytes()
                self.assertEqual(self.run_builder(finalize=True)[0], 1)
                self.assertEqual(self.output.read_bytes(), before)

    def test_incomplete_selection_never_publishes_reduced_manifest(self):
        invalid = dict(self.article, pmcid='PMC999', filename='PMC999-synthetic-study.pdf', id='PMC999-synthetic-study', article_id='PMC999-synthetic-study', abstract='')
        (self.records/'invalid.json').write_text(json.dumps(invalid))
        status, report = self.run_builder()
        self.assertEqual(status,1)
        self.assertIn('Selected: 2; included: 1; excluded: 1',report)
        self.assertFalse(self.output.exists())

    def test_existing_output_and_atomic_failure_preserve_original(self):
        self.output.write_text(json.dumps({'articles':[self.article]}))
        before = self.output.read_bytes()
        self.assertEqual(self.run_builder()[0],1)
        with patch.object(builder.os,'replace',side_effect=OSError('synthetic failure')):
            self.assertEqual(self.run_builder(finalize=True)[0],1)
        self.assertEqual(self.output.read_bytes(),before)

    def test_invalid_or_missing_filename_fails_before_output(self):
        for filename in [None, '../synthetic-study.pdf', 'PMC123456-Bad-name.pdf']:
            with self.subTest(filename=filename):
                invalid = dict(self.article)
                if filename is None: del invalid['filename']
                else: invalid['filename'] = filename
                (self.records/'article.json').write_text(json.dumps(invalid))
                self.assertEqual(self.run_builder()[0],1)
                self.assertFalse(self.output.exists())
