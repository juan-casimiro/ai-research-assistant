"""Production-equivalent extraction, fresh extraction and admission failures."""
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
        self.root=Path(self.directory.name);self.manifest=self.root/'manifest.json'
        self.article=record();self.pdf=self.root/self.article['filename'];self.pdf.write_bytes(pdf_bytes());self.write_manifest()

    def write_manifest(self):
        self.manifest.write_text(json.dumps({'articles':[self.article]}))

    def run_tool(self):
        with contextlib.redirect_stdout(io.StringIO()):
            return extractor.main(['--manifest',str(self.manifest),'--corpus-dir',str(self.root)])

    def report(self):return json.loads((self.root/'extraction_report.json').read_text())

    def test_exact_production_output_and_extraction_on_every_run(self):
        self.assertEqual(self.run_tool(),0)
        rag_client=Mock();rag_client.post.return_value.json.return_value={'chunks_ingested':0}
        ingest_file(rag_client,self.pdf,self.article['filename'])
        production=rag_client.post.call_args.kwargs['json']['text'].encode('utf-8')
        self.assertEqual(self.pdf.with_suffix('.txt').read_bytes(),production)
        with patch.object(extractor,'extract_pdf',side_effect=ValueError('synthetic extraction failure')):
            self.assertEqual(self.run_tool(),1)
        self.assertFalse(self.pdf.with_suffix('.txt').exists())
        self.assertIn('synthetic extraction failure',self.report()['failures'][0]['reason'])

    def test_invalid_pdfs_and_pinned_hash_fail(self):
        for failure in ['missing','corrupt','empty','blank-page','recorded-hash']:
            with self.subTest(failure=failure):
                self.article=record();self.write_manifest();self.pdf.write_bytes(pdf_bytes());self.assertEqual(self.run_tool(),0)
                if failure=='missing':self.pdf.unlink()
                elif failure=='corrupt':self.pdf.write_bytes(b'not a PDF')
                elif failure=='empty':self.pdf.write_bytes(pdf_bytes(('',)))
                elif failure=='blank-page':self.pdf.write_bytes(pdf_bytes(('Some text','')))
                else:self.article['metadata_sources']={'pdf':{'sha256':'0'*64}};self.write_manifest()
                self.assertEqual(self.run_tool(),1)
                self.assertFalse(self.pdf.with_suffix('.txt').exists())
                self.assertFalse(self.report()['complete'])
                self.assertEqual(self.report()['failures'][0]['pmcid'],self.article['pmcid'])

    def test_pinned_exception_is_narrow(self):
        payload=pdf_bytes(('Synthetic article text',''))
        checksum=hashlib.sha256(payload).hexdigest()
        for pmcid,version,expected_hash,status in [('PMC12003177',1,checksum,0),('PMC12003177',2,checksum,1),('PMC999',1,checksum,1),('PMC12003177',1,'wrong',1)]:
            with self.subTest(pmcid=pmcid,version=version,hash=expected_hash):
                self.article=dict(record(),pmcid=pmcid,pmc_version=version,filename=pmcid+'-synthetic-study.pdf',id=pmcid+'-synthetic-study',article_id=pmcid+'-synthetic-study')
                self.pdf=self.root/self.article['filename'];self.pdf.write_bytes(payload);self.write_manifest()
                with patch.object(extractor,'EXCEPTION',('PMC12003177',1,expected_hash)):
                    self.assertEqual(self.run_tool(),status)
                self.assertEqual(self.report()['complete'],status==0)
