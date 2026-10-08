"""Publication gate: all validation first, conflicts abort, moves can be resumed."""
import contextlib
import hashlib
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
        self.run_dir = self.root / 'build/corpus/synthetic-run'
        (self.run_dir / 'pdfs').mkdir(parents=True)
        self.article = record()
        self.article['metadata_sources'] = {'pdf': {'url': publisher.BUCKET + '/PMC123456.2/synthetic.pdf', 'md5': hashlib.md5(pdf_bytes()).hexdigest()}}
        self.source = self.run_dir / 'corpus_manifest.json'
        self.source.write_text(json.dumps({'articles': [self.article]}))
        (self.run_dir / 'candidates.json').write_text(self.source.read_text())
        self.pdf = self.run_dir / 'pdfs' / self.article['filename']
        self.pdf.write_bytes(pdf_bytes())
        self.final_manifest = self.root / 'data/corpus_manifest.json'
        self.final_pdfs = self.root / 'corpus/mvp'

    def run_tool(self, check=False):
        args = ['--run-dir', str(self.run_dir), '--manifest-destination', str(self.final_manifest), '--pdf-destination', str(self.final_pdfs)]
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
        self.assertTrue(self.source.exists())
        self.assertTrue((self.final_pdfs / self.pdf.with_suffix('.txt').name).exists())
        self.assertEqual(self.run_tool(), 0)
        for value in [None, '']:
            article = json.loads(self.final_manifest.read_text())['articles'][0]
            for field in ['cluster', 'search_query', 'selection_rationale']:
                if value is None:
                    article.pop(field, None)
                else:
                    article[field] = value
            manifest = json.dumps({'articles': [article]})
            self.source.write_text(manifest)
            self.final_manifest.write_text(manifest)
            (self.run_dir/'candidates.json').write_text(manifest)
            self.assertEqual(self.run_tool(check=True), 0)

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
                report = json.loads((self.run_dir / 'publication_report.json').read_text())
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
                (self.run_dir / 'candidates.json').write_text(json.dumps({'articles': [selection]}))
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
        manifest = {'articles': [dict(self.article, metadata_sources={'pdf': {'url': self.article['metadata_sources']['pdf']['url'], 'md5': self.article['metadata_sources']['pdf']['md5'], 'sha256': publisher.digest(raw)}})]}
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
        self.assertIn('MD5 mismatch', json.loads((self.run_dir / 'publication_report.json').read_text())['failures'][0]['reason'])

    def test_failed_fetch_preserves_selection_and_reports_missing_pmcid(self):
        from tools.corpus.fetch_article_metadata import main as fetch
        selection = self.run_dir/'candidates.json'
        selection.write_text(json.dumps({'articles':[{'pmcid':'PMC123456'},{'pmcid':'PMC999'}]}))
        before = selection.read_bytes()
        with patch('tools.corpus.fetch_article_metadata.read_bytes',side_effect=OSError('synthetic fetch failure')),contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(fetch(['--selection-file',str(selection),'--archive-dir',str(self.run_dir/'provenance'),'--records-dir',str(self.run_dir/'metadata')]),1)
        self.assertEqual(selection.read_bytes(),before)
        self.assertEqual(self.run_tool(),1)
        failures=json.loads((self.run_dir/'publication_report.json').read_text())['failures']
        self.assertIn({'pmcid':'PMC999','reason':'selected PMCID missing from prepared manifest'},failures)
        self.assertFalse(self.final_manifest.exists())

    def test_extra_manifest_pmcid_is_named_and_versions_names_are_not_selection(self):
        selection=self.run_dir/'candidates.json'
        selection.write_text(json.dumps({'articles':[{'pmcid':'PMC999'}]}))
        self.assertEqual(self.run_tool(),1)
        failures=json.loads((self.run_dir/'publication_report.json').read_text())['failures']
        self.assertIn({'pmcid':'PMC123456','reason':'prepared PMCID not in supplied selection'},failures)
        selection.write_text(json.dumps({'articles':[{'pmcid':'PMC123456'}]}))
        self.assertEqual(self.run_tool(check=True),0)

    def test_partial_move_can_be_resumed(self):
        real_move = publisher.shutil.move
        moves = 0
        def move_then_fail(source, target):
            nonlocal moves
            moves += 1
            if moves == 2:
                raise OSError('synthetic move failure')
            return real_move(source, target)
        with patch.object(publisher.shutil, 'move', side_effect=move_then_fail):
            self.assertEqual(self.run_tool(), 1)
        self.assertTrue((self.final_pdfs / self.pdf.name).exists())
        self.assertFalse(self.pdf.exists())
        self.assertEqual(self.run_tool(), 0)
        self.assertEqual(self.run_tool(), 0)

    def test_unrelated_files_and_matching_ingested_text_do_not_conflict(self):
        from tools.corpus.pdf_text import extract_pdf
        self.final_pdfs.mkdir(parents=True)
        (self.final_pdfs/'.DS_Store').write_bytes(b'synthetic unrelated content')
        text = extract_pdf(self.pdf)[0]
        (self.final_pdfs/self.pdf.with_suffix('.txt').name).write_text(text)
        self.assertEqual(self.run_tool(), 0)
        self.assertEqual((self.final_pdfs/'.DS_Store').read_bytes(), b'synthetic unrelated content')

    def test_conflicting_text_is_named_and_preserved(self):
        self.final_pdfs.mkdir(parents=True)
        target = self.final_pdfs/self.pdf.with_suffix('.txt').name
        target.write_text('synthetic conflicting text')
        self.assertEqual(self.run_tool(), 1)
        self.assertEqual(target.read_text(), 'synthetic conflicting text')
        failures = json.loads((self.run_dir/'publication_report.json').read_text())['failures']
        self.assertIn(str(target), [f.get('file') for f in failures])

    def test_every_incomplete_metadata_field_blocks_publication(self):
        for field in ['pmcid', 'pmc_version', 'pmid', 'doi', 'title', 'authors', 'journal',
                      'publication_date', 'abstract', 'filename', 'id', 'article_id',
                      'pubmed_url', 'year', 'license', 'licence_urls']:
            with self.subTest(field=field):
                invalid = dict(self.article)
                del invalid[field]
                self.source.write_text(json.dumps({'articles': [invalid]}))
                self.assertEqual(self.run_tool(), 1)
                self.assertFalse(self.final_manifest.exists())
                self.assertFalse(self.final_pdfs.exists())

    def test_bad_pdf_or_pinned_hash_blocks_publication(self):
        for raw, checksum in [(b'not a PDF', None), (pdf_bytes(('',)), None),
                              (pdf_bytes(('Some synthetic text', '')), None),
                              (pdf_bytes(), '0'*64)]:
            with self.subTest(checksum=checksum, size=len(raw)):
                self.pdf.write_bytes(raw)
                self.article['metadata_sources']['pdf']['md5'] = hashlib.md5(raw).hexdigest()
                self.article['metadata_sources']['pdf'].pop('sha256', None)
                if checksum:
                    self.article['metadata_sources']['pdf']['sha256'] = checksum
                self.source.write_text(json.dumps({'articles': [self.article]}))
                self.assertEqual(self.run_tool(), 1)
                self.assertFalse(self.final_manifest.exists())
                self.assertFalse(self.final_pdfs.exists())

    def test_only_existing_licence_admission_rules_allow_publication(self):
        for licence, urls in [('CC BY 3.0', ['https://creativecommons.org/licenses/by/3.0/']),
                              ('CC BY 4.0', []),
                              ('CC BY 4.0', ['https://creativecommons.org/licenses/by-nc/4.0/'])]:
            with self.subTest(licence=licence, urls=urls):
                invalid = dict(self.article, license=licence, licence_urls=urls)
                self.source.write_text(json.dumps({'articles': [invalid]}))
                self.assertEqual(self.run_tool(), 1)
                self.assertFalse(self.final_manifest.exists())
                self.assertFalse(self.final_pdfs.exists())

    def test_one_failed_article_blocks_moves_for_entire_selection(self):
        invalid = dict(self.article, pmcid='PMC999', filename='PMC999-test-study.pdf',
                       id='PMC999-test-study', article_id='PMC999-test-study', abstract='')
        self.source.write_text(json.dumps({'articles': [self.article, invalid]}))
        (self.run_dir/'candidates.json').write_text(self.source.read_text())
        self.assertEqual(self.run_tool(), 1)
        self.assertTrue(self.pdf.exists())
        self.assertFalse(self.final_pdfs.exists())
        failures = json.loads((self.run_dir/'publication_report.json').read_text())['failures']
        self.assertEqual(failures[0]['pmcid'], 'PMC999')

    def test_all_conflicting_files_are_named(self):
        self.final_pdfs.mkdir(parents=True)
        targets = [self.final_pdfs/self.pdf.name, self.final_pdfs/self.pdf.with_suffix('.txt').name]
        for target in targets:
            target.write_bytes(b'synthetic conflicting content')
        self.final_manifest.parent.mkdir(parents=True)
        self.final_manifest.write_text('synthetic invalid manifest')
        self.assertEqual(self.run_tool(), 1)
        failures = json.loads((self.run_dir/'publication_report.json').read_text())['failures']
        self.assertEqual({f['file'] for f in failures}, {str(p) for p in targets + [self.final_manifest]})
        for target in targets:
            self.assertEqual(target.read_bytes(), b'synthetic conflicting content')

    def test_publication_keeps_exact_pdf_exception(self):
        raw = pdf_bytes(('Some synthetic article text', ''))
        self.pdf.write_bytes(raw)
        self.article['metadata_sources']['pdf']['md5'] = hashlib.md5(raw).hexdigest()
        for version, checksum, status in [(1, hashlib.sha256(raw).hexdigest(), 0),
                                          (2, hashlib.sha256(raw).hexdigest(), 1),
                                          (1, 'wrong', 1)]:
            with self.subTest(version=version, checksum=checksum):
                self.article['pmc_version'] = version
                self.article['metadata_sources']['pdf']['url'] = publisher.BUCKET + f'/PMC123456.{version}/synthetic.pdf'
                self.source.write_text(json.dumps({'articles': [self.article]}))
                with patch('tools.corpus.extract_corpus_text.EXCEPTION', ('PMC123456', 1, checksum)):
                    self.assertEqual(self.run_tool(check=True), status)
                self.assertFalse(self.final_pdfs.exists())

    def test_missing_provider_md5_blocks_publication(self):
        del self.article['metadata_sources']['pdf']['md5']
        self.source.write_text(json.dumps({'articles': [self.article]}))
        self.assertEqual(self.run_tool(), 1)
        failures = json.loads((self.run_dir/'publication_report.json').read_text())['failures']
        self.assertEqual(failures, [{'pmcid': self.article['pmcid'], 'reason': 'missing PDF provider MD5 checksum'}])
        self.assertFalse(self.final_pdfs.exists())
        self.assertFalse(self.final_manifest.exists())

    def test_url_provider_md5_is_sufficient(self):
        pdf_source = self.article['metadata_sources']['pdf']
        pdf_source['url'] += '?md5=' + pdf_source.pop('md5')
        self.source.write_text(json.dumps({'articles': [self.article]}))
        self.assertEqual(self.run_tool(), 0)

    def test_missing_pdf_names_prepared_path(self):
        self.pdf.unlink()
        self.assertEqual(self.run_tool(), 1)
        failures = json.loads((self.run_dir/'publication_report.json').read_text())['failures']
        self.assertIn(str(self.pdf), failures[0]['reason'])
        self.assertNotIn(str(self.final_pdfs), failures[0]['reason'])

    def test_nonexistent_run_directory_creates_nothing(self):
        self.run_dir = self.root/'mistyped-parent'/'mistyped-run'
        with contextlib.redirect_stdout(io.StringIO()) as report:
            self.assertEqual(publisher.main(['--run-dir', str(self.run_dir)]), 1)
        self.assertIn(str(self.run_dir), report.getvalue())
        self.assertFalse(self.run_dir.parent.exists())
