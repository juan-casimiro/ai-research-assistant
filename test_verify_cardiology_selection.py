"""Offline CLI regressions for corrupted PDFs and pinned article XML."""
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

from pypdf import PdfWriter
from pypdf.errors import PdfReadError
from pypdf.generic import DecodedStreamObject, DictionaryObject, NameObject

import verify_cardiology_selection as selection_verifier


def synthetic_pdf(text):
    writer = PdfWriter()
    page = writer.add_blank_page(width=200, height=100)
    font = DictionaryObject({NameObject("/Type"): NameObject("/Font"),
                             NameObject("/Subtype"): NameObject("/Type1"),
                             NameObject("/BaseFont"): NameObject("/Helvetica")})
    page[NameObject("/Resources")] = DictionaryObject({
        NameObject("/Font"): DictionaryObject({NameObject("/F1"): writer._add_object(font)})})
    content = DecodedStreamObject()
    content.set_data(f"BT /F1 10 Tf 10 50 Td ({text}) Tj ET".encode())
    page[NameObject("/Contents")] = writer._add_object(content)
    output = io.BytesIO()
    writer.write(output)
    return output.getvalue()


class VerifyCardiologySelectionTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.selection_dir = Path(directory.name, "selection")
        self.corpus_dir = Path(directory.name, "corpus")
        self.selection_dir.mkdir()
        self.corpus_dir.mkdir()
        self.article_id = "PMC123456"
        self.text = "Some synthetic cardiac evidence."
        self.pdf = self.corpus_dir / "test-cardiac-article.pdf"
        self.pdf.write_bytes(synthetic_pdf(self.text))
        self.pdf.with_suffix(".txt").write_text(self.text)
        self.xml = self.corpus_dir / "PMC123456.2.xml"
        self.xml.write_bytes(b"<article>Some synthetic article metadata.</article>")
        cloud = {"pmcid": self.article_id, "version": 2, "doi": "10.1234/synthetic", "pmid": 987654}
        cloud_bytes = json.dumps(cloud).encode()
        sources = {}
        for key, payload in [("pmc_cloud", cloud_bytes), ("pubmed", b"<SomeSyntheticPubMedRecord/>"),
                             ("pmcid_converter", b'{"records": []}')]:
            archive = f"test-{key}.txt"
            (self.selection_dir / archive).write_bytes(payload)
            sources[key] = {"archive": archive, "sha256": selection_verifier.digest(payload)}
        sources["pmc_article_xml"] = {"sha256": selection_verifier.digest(self.xml.read_bytes())}
        self.article = {
            "article_id": self.article_id, "filename": self.pdf.name, "cluster": "cardiology",
            "search_query": "some synthetic cardiac search", "pmcid": self.article_id, "pmc_version": 2,
            "pmid": "987654", "doi": "10.1234/synthetic", "title": "Some synthetic cardiac study",
            "authors": ["Some Researcher"], "journal": "Synthetic Journal", "year": 2024,
            "abstract": "Some synthetic study abstract.", "abstract_summary": "Some authored summary.",
            "license": "CC BY 4.0", "license_notes": "Some licence notice", "licence": {"id": "CC-BY-4.0"},
            "third_party_review": {"status": "clear"}, "eligibility": "eligible", "notes": "Some selection notes",
            "page_count": 1, "has_structured_sections": True,
            "download": {"route": "pmc_cloud", "pdf_sha256": selection_verifier.digest(self.pdf.read_bytes())},
            "validation": {"extracted_text_sha256": selection_verifier.digest(self.text.encode())},
            "metadata_sources": sources, "metadata_sha256": sources["pmc_cloud"]["sha256"],
        }
        self.write_selection()

    def write_json(self, name, value):
        (self.selection_dir / name).write_text(json.dumps(value))

    def write_selection(self):
        article = self.article
        manifest = {"articles": [article]}
        manifest["fingerprint_sha256"] = selection_verifier.digest(selection_verifier.canonical(manifest))
        self.write_json("manifest.json", manifest)
        self.write_json("evidence_map.json", {"articles": [{
            "article_id": self.article_id, "pdf_sha256": article["download"]["pdf_sha256"],
            "text_sha256": article["validation"]["extracted_text_sha256"],
            "selection_locations": [{"text_start": 0, "text_end": len(self.text), "excerpt": self.text,
                                     "excerpt_sha256": selection_verifier.digest(self.text.encode())}],
        }]})
        (self.selection_dir / "ATTRIBUTION.md").write_text(f"## {self.article_id}\n{article['download']['pdf_sha256']}\n")
        tuples = [{"article_id": self.article_id, "pmc_version": 2,
                   "pdf_sha256": article["download"]["pdf_sha256"],
                   "text_sha256": article["validation"]["extracted_text_sha256"]}]
        membership = {"article_ids": [self.article_id], "membership_sha256": selection_verifier.digest(selection_verifier.canonical(tuples))}
        self.write_json("conditions.json", {"article_tuples": tuples, "conditions": {key: membership for key in ["C1", "C2", "C3"]}})
        self.write_json("migration.json", {"baseline": {"files": {}}})

    def run_cli(self):
        captured = io.StringIO()
        with contextlib.redirect_stdout(captured):
            result = selection_verifier.main(["--selection-dir", str(self.selection_dir), "--corpus-dir", str(self.corpus_dir)])
        return result, captured.getvalue()

    def test_intact_selection_verifies_without_network_or_real_corpus(self):
        result, output = self.run_cli()
        self.assertEqual(result, 0)
        self.assertIn("Verified 1 articles", output)

    def test_corrupt_pdf_reports_article_error_without_traceback(self):
        self.pdf.write_bytes(b"%PDF-1.7\nSome corrupt synthetic PDF bytes")
        # Matching the manifest hash must not let invalid PDF structure through.
        self.article["download"]["pdf_sha256"] = selection_verifier.digest(self.pdf.read_bytes())
        self.write_selection()
        result, output = self.run_cli()
        self.assertEqual(result, 1)
        self.assertEqual(output, f"ERROR: {self.article_id}: unreadable PDF\n")

    def test_text_extraction_errors_report_article_error_without_traceback(self):
        for error in [PdfReadError("Some broken text stream"), KeyError("Some missing font resource")]:
            with self.subTest(error=type(error).__name__):
                page = Mock()
                page.extract_text.side_effect = error
                with patch.object(selection_verifier, "PdfReader", return_value=Mock(pages=[page])):
                    result, output = self.run_cli()
                self.assertEqual(result, 1)
                self.assertEqual(output, f"ERROR: {self.article_id}: unreadable PDF\n")

    def test_changed_article_xml_is_rejected(self):
        self.xml.write_bytes(b"<article>Some changed licence metadata.</article>")
        result, output = self.run_cli()
        self.assertEqual(result, 1)
        self.assertEqual(output, f"ERROR: {self.article_id}: article XML hash mismatch\n")

    def test_missing_article_xml_is_rejected(self):
        self.xml.unlink()
        result, output = self.run_cli()
        self.assertEqual(result, 1)
        self.assertEqual(output, f"ERROR: {self.article_id}: missing or unreadable article XML\n")


if __name__ == "__main__":
    unittest.main()
