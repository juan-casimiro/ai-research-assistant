"""Offline corpus admission, provenance and safe finalization checks."""
import contextlib
import copy
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

from pypdf import PdfWriter, PdfReader
from pypdf.generic import DictionaryObject, NameObject, DecodedStreamObject
from tools.corpus import build_corpus_manifest as builder
from ingest_corpus import ingest_file


def pdf_bytes(texts=('Synthetic first page', 'Synthetic second page')):
    writer = PdfWriter()
    for text in texts:
        page = writer.add_blank_page(200, 200)
        font = DictionaryObject({NameObject('/Type'): NameObject('/Font'), NameObject('/Subtype'): NameObject('/Type1'), NameObject('/BaseFont'): NameObject('/Helvetica')})
        page[NameObject('/Resources')] = DictionaryObject({NameObject('/Font'): DictionaryObject({NameObject('/F1'): writer._add_object(font)})})
        stream = DecodedStreamObject()
        stream.set_data(f'BT /F1 12 Tf 10 100 Td ({text}) Tj ET'.encode())
        page[NameObject('/Contents')] = writer._add_object(stream)
    output = io.BytesIO()
    writer.write(output)
    return output.getvalue()


class ManifestTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.output = self.root / 'manifest.json'
        self.candidates = self.root / 'candidates.json'
        self.record = dict(pmcid='PMC123456', pmc_version=2, filename='PMC123456-synthetic-study.pdf',
                           id='PMC123456-synthetic-study', article_id='PMC123456-synthetic-study',
                           cluster='test-topic', search_query='some discovery query', pmid='987654',
                           doi='10.1234/synthetic', title='Synthetic study', journal='Synthetic journal',
                           publication_date='2024-07', year=2024, authors=['Ada Example'],
                           abstract='Synthetic complete PubMed abstract.', pubmed_url='https://pubmed.ncbi.nlm.nih.gov/987654/',
                           license='CC BY 4.0', licence_urls=['https://creativecommons.org/licenses/by/4.0/'],
                           metadata_sources={'pdf': {'url': builder.BUCKET + '/PMC123456.2/synthetic.pdf'}})
        self.pdf = self.root / self.record['filename']
        self.pdf.write_bytes(pdf_bytes())
        self.candidates.write_text(json.dumps({'articles': [self.record]}))

    def run_builder(self, finalize=False):
        args = ['--corpus-dir', str(self.root)]
        args += ['--finalize', str(self.output)] if finalize else ['--candidates', str(self.candidates), '--output', str(self.output)]
        with patch.object(builder, 'fetch_metadata', return_value=copy.deepcopy(self.record)) as fetch, contextlib.redirect_stdout(io.StringIO()) as report:
            status = builder.main(args)
        return status, fetch.call_count, report.getvalue()

    def test_creation_generates_exact_production_text_and_pdf_provenance(self):
        self.assertEqual(self.run_builder()[0], 0)
        article = json.loads(self.output.read_text())['articles'][0]
        expected = '\n'.join(page.extract_text() or '' for page in PdfReader(str(self.pdf)).pages)
        self.assertEqual(article['metadata_sources']['pdf']['sha256'], hashlib.sha256(self.pdf.read_bytes()).hexdigest())
        extraction = article['metadata_sources']['extracted_text']
        self.assertEqual(extraction['sha256'], hashlib.sha256(expected.encode('utf-8')).hexdigest())
        self.assertEqual(extraction['pages_without_text'], [])
        self.assertEqual(extraction['pypdf_version'], builder.pypdf.__version__)
        self.assertEqual(extraction['method'], builder.EXTRACTION_METHOD)
        self.assertEqual(article['page_count'], 2)
        rag_client = Mock()
        rag_client.post.return_value.json.return_value = {'chunks_ingested': 0}
        ingest_file(rag_client, self.pdf, self.record['filename'])
        production_text = rag_client.post.call_args.kwargs['json']['text']
        self.assertEqual(extraction['sha256'], hashlib.sha256(production_text.encode('utf-8')).hexdigest())

    def test_finalization_preserves_metadata_and_does_not_fetch(self):
        self.output.write_text(json.dumps({'articles': [self.record], 'candidate_source': {'synthetic': True}}))
        self.assertEqual(self.run_builder(finalize=True)[:2], (0, 0))
        final = json.loads(self.output.read_text())
        self.assertEqual(final['candidate_source'], {'synthetic': True})
        for key, value in self.record.items():
            if key != 'metadata_sources':
                self.assertEqual(final['articles'][0][key], value)
        before = self.output.read_bytes()
        self.assertEqual(self.run_builder(finalize=True)[:2], (0, 0))
        self.assertEqual(self.output.read_bytes(), before)

    def test_missing_pdf_url_is_completed_from_local_verified_cloud_source(self):
        cloud = dict(pmcid=self.record['pmcid'], version=2, pmid=self.record['pmid'], doi=self.record['doi'], pdf_url='s3://pmc-oa-opendata/PMC123456.2/synthetic.pdf')
        raw = json.dumps(cloud).encode()
        source = self.root / 'PMC123456.2.cloud.json'
        source.write_bytes(raw)
        record = copy.deepcopy(self.record)
        record['metadata_sources'] = {'cloud.json': {'sha256': hashlib.sha256(raw).hexdigest()}}
        self.output.write_text(json.dumps({'articles': [record]}))
        with patch.object(builder, 'fetch_metadata', side_effect=AssertionError('no refetch')), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(builder.main(['--finalize', str(self.output), '--corpus-dir', str(self.root), '--provenance-dir', str(self.root)]), 0)
        self.assertEqual(json.loads(self.output.read_text())['articles'][0]['metadata_sources']['pdf']['url'], self.record['metadata_sources']['pdf']['url'])
        self.output.write_text(json.dumps({'articles': [record]}))
        before = self.output.read_bytes()
        source.write_bytes(raw + b' ')
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(builder.main(['--finalize', str(self.output), '--corpus-dir', str(self.root), '--provenance-dir', str(self.root)]), 1)
        self.assertEqual(self.output.read_bytes(), before)

    def test_hash_mismatches_preserve_original(self):
        for source in ['pdf', 'extracted_text']:
            with self.subTest(source=source):
                record = copy.deepcopy(self.record)
                record['metadata_sources'].setdefault(source, {})['sha256'] = '0' * 64
                self.output.write_text(json.dumps({'articles': [record]}))
                before = self.output.read_bytes()
                status, calls, report = self.run_builder(finalize=True)
                self.assertEqual((status, calls), (1, 0))
                self.assertIn('mismatch', report)
                self.assertEqual(self.output.read_bytes(), before)

    def test_mandatory_fields_are_required(self):
        for field in ['pmid', 'doi', 'title', 'authors', 'journal', 'publication_date', 'year', 'abstract', 'pubmed_url', 'id', 'article_id']:
            with self.subTest(field=field):
                record = copy.deepcopy(self.record)
                del record[field]
                self.output.write_text(json.dumps({'articles': [record]}))
                before = self.output.read_bytes()
                self.assertEqual(self.run_builder(finalize=True)[0], 1)
                self.assertEqual(self.output.read_bytes(), before)

    def test_inconsistent_provenance_and_abstract_fail_without_writing(self):
        for field in ['url', 'md5', 'page_count', 'pubmed_url', 'abstract_absence_reason']:
            with self.subTest(field=field):
                record = copy.deepcopy(self.record)
                if field == 'url': record['metadata_sources']['pdf']['url'] = builder.BUCKET + '/PMC999.2/synthetic.pdf'
                elif field == 'md5': record['metadata_sources']['pdf']['md5'] = '0' * 32
                elif field == 'page_count': record['page_count'] = 99
                elif field == 'pubmed_url': record['pubmed_url'] = 'https://pubmed.ncbi.nlm.nih.gov/111/'
                else: record[field] = 'No abstract in the PubMed record'
                self.output.write_text(json.dumps({'articles': [record]}))
                before = self.output.read_bytes()
                self.assertEqual(self.run_builder(finalize=True)[0], 1)
                self.assertEqual(self.output.read_bytes(), before)

    def test_incomplete_selection_does_not_publish_reduced_corpus(self):
        other = dict(self.record, pmcid='PMC999', filename='PMC999-synthetic-study.pdf', id='PMC999-synthetic-study', article_id='PMC999-synthetic-study')
        self.output.write_text(json.dumps({'articles': [self.record, other]}))
        before = self.output.read_bytes()
        status, _, report = self.run_builder(finalize=True)
        self.assertEqual(status, 1)
        self.assertIn('Selected: 2; included: 1; excluded: 1', report)
        self.assertEqual(self.output.read_bytes(), before)
        self.output.unlink()
        self.candidates.write_text(json.dumps({'articles': [self.record, other]}))
        with patch.object(builder, 'fetch_metadata', side_effect=[copy.deepcopy(self.record), other]), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(builder.main(['--candidates', str(self.candidates), '--corpus-dir', str(self.root), '--output', str(self.output)]), 1)
        self.assertFalse(self.output.exists())

    def test_unsupported_licence_and_unreadable_pdf_are_excluded(self):
        for change in ['licence', 'blank', 'missing', 'corrupt']:
            with self.subTest(change=change):
                record = copy.deepcopy(self.record)
                self.pdf.write_bytes(pdf_bytes())
                if change == 'licence': record['licence_urls'] = []
                if change == 'blank': self.pdf.write_bytes(pdf_bytes(('',)))
                if change == 'missing': self.pdf.unlink()
                if change == 'corrupt': self.pdf.write_bytes(b'not a PDF')
                self.output.write_text(json.dumps({'articles': [record]}))
                before = self.output.read_bytes()
                self.assertEqual(self.run_builder(finalize=True)[0], 1)
                self.assertEqual(self.output.read_bytes(), before)

    def test_existing_output_and_invalid_selections_never_fetch(self):
        self.output.write_bytes(b'preserved bytes')
        self.assertEqual(self.run_builder()[:2], (1, 0))
        self.assertEqual(self.output.read_bytes(), b'preserved bytes')
        self.output.unlink()
        for articles in [[], [self.record, self.record], [dict(self.record, filename='../bad.pdf')]]:
            self.candidates.write_text(json.dumps({'articles': articles}))
            self.assertEqual(self.run_builder()[:2], (1, 0))

    def test_atomic_failure_preserves_original_and_removes_temporary(self):
        self.output.write_text(json.dumps({'articles': [self.record]}))
        before = self.output.read_bytes()
        with patch.object(builder.os, 'replace', side_effect=OSError('synthetic write failure')):
            self.assertEqual(self.run_builder(finalize=True)[0], 1)
        self.assertEqual(self.output.read_bytes(), before)
        self.assertEqual(set(p.name for p in self.root.iterdir()), {self.output.name, self.candidates.name, self.pdf.name})

    def test_exception_requires_exact_identity_hash_version_and_page_set(self):
        for version, checksum, blank_count, expected in [(1, None, 3, 0), (2, None, 3, 1), (1, 'wrong', 3, 1), (1, None, 4, 1)]:
            with self.subTest(version=version, checksum=checksum, blank_count=blank_count):
                record = dict(self.record, pmcid='PMC12003177', pmc_version=version, filename='PMC12003177-synthetic-study.pdf', id='PMC12003177-synthetic-study', article_id='PMC12003177-synthetic-study', metadata_sources={'pdf': {'url': f'{builder.BUCKET}/PMC12003177.{version}/synthetic.pdf'}})
                pdf = self.root / record['filename']
                pdf.write_bytes(pdf_bytes(('Synthetic page',) * 21 + ('',) * blank_count))
                self.output.write_text(json.dumps({'articles': [record]}))
                with patch.object(builder, 'READABILITY_EXCEPTION', ('PMC12003177', 1, checksum or hashlib.sha256(pdf.read_bytes()).hexdigest())):
                    self.assertEqual(self.run_builder(finalize=True)[0], expected)
