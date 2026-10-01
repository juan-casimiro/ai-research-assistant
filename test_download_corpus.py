"""Offline regression coverage for safe corpus downloads."""
import contextlib
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from pypdf import PdfWriter

import download_corpus


def pdf_bytes():
    writer = PdfWriter()
    page = writer.add_blank_page(width=100, height=100)
    # A real content stream allows validation to distinguish empty page objects.
    from pypdf.generic import DecodedStreamObject, NameObject
    content = DecodedStreamObject()
    content.set_data(b"q Q")
    page[NameObject("/Contents")] = writer._add_object(content)
    output = io.BytesIO()
    writer.write(output)
    return output.getvalue()


class DownloadCorpusTests(unittest.TestCase):
    def test_valid_download_checksum_and_atomic_replacement(self):
        payload = pdf_bytes()
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory, "test-paper.pdf")
            destination.write_bytes(b"previous invalid file")
            with patch.object(download_corpus, "open_url", return_value=io.BytesIO(payload)):
                download_corpus.download("https://example.test/paper", destination, hashlib.md5(payload).hexdigest())
            self.assertEqual(destination.read_bytes(), payload)
            self.assertTrue(download_corpus.valid_pdf(destination))
            self.assertEqual(list(Path(directory).glob("*.part")), [])

    def test_invalid_download_preserves_destination_and_removes_partial(self):
        for payload, checksum in [(b"<html>test challenge</html>", None), (b"%PDF-truncated", None), (pdf_bytes(), "bad checksum")]:
            with self.subTest(checksum=checksum), tempfile.TemporaryDirectory() as directory:
                destination = Path(directory, "test-paper.pdf")
                destination.write_bytes(b"previous file")
                with patch.object(download_corpus, "open_url", return_value=io.BytesIO(payload)), self.assertRaises(ValueError):
                    download_corpus.download("https://example.test/paper", destination, checksum)
                self.assertEqual(destination.read_bytes(), b"previous file")
                self.assertEqual(list(Path(directory).glob("*.part")), [])

    def test_metadata_identity_and_url_validation(self):
        article = {"pmcid": "PMC123", "doi": "10.123/test-paper", "pmc_version": 4}
        metadata = {"pmcid": "PMC123", "doi": "10.123/TEST-PAPER", "pdf_url": "s3://pmc-oa-opendata/PMC123.4/paper.pdf?md5=test-digest"}
        with patch.object(download_corpus, "open_url", return_value=io.BytesIO(json.dumps(metadata).encode())) as metadata_service:
            url, checksum = download_corpus.resolve_pdf(article)
            self.assertEqual(url, download_corpus.BUCKET + "/PMC123.4/paper.pdf?md5=test-digest")
            self.assertEqual(checksum, "test-digest")
            self.assertIn("PMC123.4.json", metadata_service.call_args.args[0])
        for field, value in [("doi", "10.123/wrong-paper"), ("pmcid", "PMC999"), ("pdf_url", "https://example.test/wrong.pdf")]:
            with self.subTest(field=field), patch.object(download_corpus, "open_url", return_value=io.BytesIO(json.dumps(dict(metadata, **{field: value})).encode())), self.assertRaises(ValueError):
                download_corpus.resolve_pdf(article)

    def test_missing_manual_is_incomplete_and_browser_is_opt_in(self):
        with tempfile.TemporaryDirectory() as directory:
            manifest = Path(directory, "manifest.json")
            manifest.write_text(json.dumps({"articles": [{"filename": "test-manual.pdf", "doi": "10.123/manual", "manual_url": "https://example.test/manual"}]}))
            args = ["--manifest", str(manifest), "--corpus-dir", directory]
            with patch.object(download_corpus.webbrowser, "open") as publisher_browser, contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(download_corpus.main(args), 1)
                publisher_browser.assert_not_called()
                self.assertEqual(download_corpus.main(args + ["--open-manual"]), 1)
                publisher_browser.assert_called_once_with("https://example.test/manual")
                Path(directory, "test-manual.pdf").write_bytes(pdf_bytes())
                publisher_browser.reset_mock()
                self.assertEqual(download_corpus.main(args + ["--open-manual"]), 0)
                publisher_browser.assert_not_called()

    def test_failure_continues_to_other_articles_and_unknown_selection_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            manifest = Path(directory, "manifest.json")
            manifest.write_text(json.dumps({"articles": [{"filename": name, "pmcid": "PMC123", "doi": "10.123/test"} for name in ["test-first.pdf", "test-second.pdf"]]}))
            args = ["--manifest", str(manifest), "--corpus-dir", directory]
            with patch.object(download_corpus, "resolve_pdf", side_effect=[ValueError("test unavailable"), ("https://example.test/pdf", None)]), patch.object(download_corpus, "download") as pdf_service, contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(download_corpus.main(args), 1)
                self.assertEqual(pdf_service.call_count, 1)
                self.assertEqual(download_corpus.main(args + ["--filename", "unknown.pdf"]), 1)


if __name__ == "__main__":
    unittest.main()
