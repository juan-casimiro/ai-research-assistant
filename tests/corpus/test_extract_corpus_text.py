"""Production-equivalent extraction, verified cache reuse and admission failures."""
import contextlib
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch
from pypdf import PdfWriter
from pypdf.generic import DictionaryObject, NameObject, DecodedStreamObject
from ingest_corpus import ingest_file
from tools.corpus import extract_corpus_text as extractor
from tests.corpus.test_build_corpus_manifest import record


def pdf_bytes(texts=('Synthetic first page','Synthetic second page')):
    writer=PdfWriter()
    for text in texts:
        page=writer.add_blank_page(200,200)
        font=DictionaryObject({NameObject('/Type'):NameObject('/Font'),NameObject('/Subtype'):NameObject('/Type1'),NameObject('/BaseFont'):NameObject('/Helvetica')})
        page[NameObject('/Resources')]=DictionaryObject({NameObject('/Font'):DictionaryObject({NameObject('/F1'):writer._add_object(font)})})
        stream=DecodedStreamObject()
        stream.set_data(f'BT /F1 12 Tf 10 100 Td ({text}) Tj ET'.encode())
        page[NameObject('/Contents')]=writer._add_object(stream)
    result=io.BytesIO();writer.write(result);return result.getvalue()


class ExtractionTests(unittest.TestCase):
    def setUp(self):
        self.directory=tempfile.TemporaryDirectory();self.addCleanup(self.directory.cleanup)
        self.root=Path(self.directory.name);self.cache=self.root/'extracted_text';self.manifest=self.root/'manifest.json'
        self.article=record();self.pdf=self.root/self.article['filename'];self.pdf.write_bytes(pdf_bytes());self.write_manifest()

    def write_manifest(self):
        self.manifest.write_text(json.dumps({'articles':[self.article]}))

    def run_tool(self):
        with contextlib.redirect_stdout(io.StringIO()):
            return extractor.main(['--manifest',str(self.manifest),'--corpus-dir',str(self.root),'--cache-dir',str(self.cache)])

    def index(self):return json.loads((self.cache/'index.json').read_text())
    def report(self):return json.loads((self.cache/'extraction_report.json').read_text())

    def test_exact_production_output_and_hash_verified_reuse(self):
        self.assertEqual(self.run_tool(),0)
        rag_client=Mock();rag_client.post.return_value.json.return_value={'chunks_ingested':0}
        ingest_file(rag_client,self.pdf,self.article['filename'])
        production=rag_client.post.call_args.kwargs['json']['text'].encode('utf-8')
        entry=self.index()['articles'][0]
        self.assertEqual((self.cache/entry['text_file']).read_bytes(),production)
        self.assertEqual(entry['text_sha256'],hashlib.sha256(production).hexdigest())
        self.assertEqual(entry['pdf_sha256'],hashlib.sha256(self.pdf.read_bytes()).hexdigest())
        self.assertEqual(set(entry),{'source_id','pdf_sha256','text_file','text_sha256','extractor'})
        with patch.object(extractor,'extract_pdf',side_effect=AssertionError('should reuse')):
            self.assertEqual(self.run_tool(),0)
        self.assertTrue(self.report()['articles'][0]['reused'])

    def test_tampered_text_and_changed_pdf_are_not_reused(self):
        self.assertEqual(self.run_tool(),0)
        text=self.cache/self.index()['articles'][0]['text_file'];text.write_text('tampered text')
        self.assertEqual(self.run_tool(),0);self.assertNotEqual(text.read_text(),'tampered text')
        self.pdf.write_bytes(pdf_bytes(('Changed synthetic page',)))
        self.assertEqual(self.run_tool(),0);self.assertIn('Changed',text.read_text())
        self.assertFalse(self.report()['articles'][0]['reused'])

    def test_failures_invalidate_successful_cache(self):
        for failure in ['missing','corrupt','empty','blank-page','recorded-hash']:
            with self.subTest(failure=failure):
                self.article=record();self.write_manifest();self.pdf.write_bytes(pdf_bytes());self.assertEqual(self.run_tool(),0)
                if failure=='missing':self.pdf.unlink()
                elif failure=='corrupt':self.pdf.write_bytes(b'not a PDF')
                elif failure=='empty':self.pdf.write_bytes(pdf_bytes(('',)))
                elif failure=='blank-page':self.pdf.write_bytes(pdf_bytes(('Some text','')))
                else:self.article['metadata_sources']={'pdf':{'sha256':'0'*64}};self.write_manifest()
                self.assertEqual(self.run_tool(),1)
                self.assertEqual(self.index()['articles'],[])
                self.assertFalse((self.cache/(self.article['id']+'.txt')).exists())
                self.assertFalse(self.report()['complete'])
                self.assertEqual(self.report()['articles'][0]['status'],'requires_replacement')
                self.assertEqual(self.report()['articles'][0]['pmcid'],self.article['pmcid'])

    def test_pinned_exception_is_narrow_and_recorded_only_in_report(self):
        payload=pdf_bytes(('Synthetic article text',''))
        checksum=hashlib.sha256(payload).hexdigest()
        for pmcid,version,expected_hash,status in [('PMC12003177',1,checksum,0),('PMC12003177',2,checksum,1),('PMC999',1,checksum,1),('PMC12003177',1,'wrong',1)]:
            with self.subTest(pmcid=pmcid,version=version,hash=expected_hash):
                self.article=dict(record(),pmcid=pmcid,pmc_version=version,filename=pmcid+'-synthetic-study.pdf',id=pmcid+'-synthetic-study',article_id=pmcid+'-synthetic-study')
                self.pdf=self.root/self.article['filename'];self.pdf.write_bytes(payload);self.write_manifest()
                with patch.object(extractor,'EXCEPTION',('PMC12003177',1,expected_hash)):
                    self.assertEqual(self.run_tool(),status)
                if status==0:
                    report=self.report()['articles'][0]
                    self.assertTrue(report['accepted_exception']);self.assertEqual(report['pages_without_text'],[2]);self.assertIn('not searchable',report['limitation'])
                    self.assertNotIn('pages_without_text',self.index()['articles'][0])

    def test_extraction_error_invalidates_entry_even_for_same_pdf(self):
        self.assertEqual(self.run_tool(),0)
        # A new extractor version invalidates otherwise valid cached output.
        with patch.object(extractor.pypdf,'__version__','synthetic-new-version'),patch.object(extractor,'extract_pdf',side_effect=ValueError('synthetic extraction failure')):
            self.assertEqual(self.run_tool(),1)
        self.assertEqual(self.index()['articles'],[])
        self.assertIn('synthetic extraction failure',self.report()['articles'][0]['reason'])
