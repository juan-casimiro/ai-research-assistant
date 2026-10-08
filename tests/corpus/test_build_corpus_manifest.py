"""Metadata-only assembly: no PDF, download or extraction work."""
import contextlib
import copy
import io
import json
from pathlib import Path
import tempfile
import unittest
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

    def run_builder(self):
        with contextlib.redirect_stdout(io.StringIO()) as report:
            status = builder.main(['--records-dir', str(self.records), '--output', str(self.output)])
        return status, report.getvalue()

    def test_assembles_complete_records_and_reruns(self):
        self.assertEqual(self.run_builder()[0], 0)
        self.assertEqual(json.loads(self.output.read_text()), {'articles': [self.article]})
        self.assertEqual(self.run_builder()[0], 0)
        for value in [None, '']:
            article = dict(self.article)
            for field in ['cluster', 'search_query', 'selection_rationale']:
                if value is None:
                    article.pop(field, None)
                else:
                    article[field] = value
            (self.records/'article.json').write_text(json.dumps(article))
            self.assertEqual(self.run_builder()[0], 0)

    def test_incomplete_records_never_write_manifest(self):
        for field in ['pmcid', 'pmc_version', 'filename', 'pmid', 'doi', 'title', 'journal',
                      'publication_date', 'authors', 'year', 'abstract', 'pubmed_url',
                      'id', 'article_id', 'licence_urls']:
            with self.subTest(field=field):
                article = copy.deepcopy(self.article)
                del article[field]
                (self.records / 'article.json').write_text(json.dumps(article))
                self.assertEqual(self.run_builder()[0], 1)
                self.assertFalse(self.output.exists())

    def test_differing_prepared_manifest_is_rebuilt(self):
        self.output.write_text('{"articles": []}')
        self.assertEqual(self.run_builder()[0], 0)
        self.assertEqual(json.loads(self.output.read_text()), {'articles': [self.article]})
