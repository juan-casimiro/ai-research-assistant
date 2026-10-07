import copy
import contextlib
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from fetch_article_metadata import fetch_metadata, main, parse_record


class ArticleMetadataTests(unittest.TestCase):
    def setUp(self):
        self.cloud_metadata = {
            "pmcid": "PMC123456", "version": 2, "pmid": 987654,
            "doi": "10.1234/synthetic", "license_code": "CC BY", "is_retracted": False,
        }
        self.identifiers = {"records": [{"pmcid": "PMC123456", "pmid": 987654, "doi": "10.1234/synthetic"}]}
        self.jats = b'''<article article-type="research-article"><front>
          <journal-meta><journal-title-group><journal-title>Test Journal</journal-title></journal-title-group></journal-meta>
          <article-meta><article-id pub-id-type="doi">10.1234/synthetic</article-id>
            <title-group><article-title>A synthetic <italic>cardiac</italic> study</article-title></title-group>
            <contrib-group><contrib contrib-type="author"><name><surname>Example</surname><given-names>Ada</given-names></name></contrib></contrib-group>
            <pub-date pub-type="epub"><month>7</month><year>2024</year></pub-date>
            <permissions><license><license-p>CC BY: https://creativecommons.org/licenses/by/4.0/.
            Data: https://creativecommons.org/publicdomain/zero/1.0/.</license-p></license></permissions>
          </article-meta></front><body><sec><title>Results</title></sec></body></article>'''
        self.pubmed = b'''<PubmedArticleSet><PubmedArticle><MedlineCitation><PMID>987654</PMID><Article>
          <ArticleTitle>A synthetic <i>cardiac</i> study.</ArticleTitle>
          <Abstract><AbstractText Label="BACKGROUND">Some test population.</AbstractText>
            <AbstractText Label="RESULTS">A test <b>finding</b> with qualifiers.</AbstractText></Abstract>
        </Article></MedlineCitation><PubmedData><ArticleIdList>
          <ArticleId IdType="doi">10.1234/synthetic</ArticleId>
        </ArticleIdList></PubmedData></PubmedArticle></PubmedArticleSet>'''

    def test_join_preserves_abstract_and_date_precision_without_certifying_pdf(self):
        record = parse_record(self.cloud_metadata, self.jats, self.pubmed, self.identifiers)
        self.assertEqual(record["abstract"], "BACKGROUND: Some test population.\n\nRESULTS: A test finding with qualifiers.")
        self.assertEqual(record["authors"], ["Ada Example"])
        self.assertEqual(record["publication_date"], "2024-07")
        self.assertEqual(record["publication_date_precision"], "month")
        self.assertEqual(record["license"], "CC BY 4.0")
        self.assertEqual(record["pmc_version"], 2)
        self.assertEqual(record["eligibility"], "eligible")
        self.assertIsNone(record["page_count"])

    def test_mismatched_mapping_does_not_attach_wrong_pubmed_record(self):
        mapping = copy.deepcopy(self.identifiers)
        mapping["records"][0]["pmid"] = 999999
        with self.assertRaisesRegex(ValueError, "converter disagrees"):
            parse_record(self.cloud_metadata, self.jats, self.pubmed, mapping)

    def test_pubmed_doi_and_title_disagreements_require_review(self):
        for pubmed in [self.pubmed.replace(b"10.1234/synthetic", b"10.1234/other"), self.pubmed.replace(b"cardiac", b"renal")]:
            with self.subTest(pubmed=pubmed), self.assertRaises(ValueError):
                parse_record(self.cloud_metadata, self.jats, pubmed, self.identifiers)

    def test_missing_abstract_is_explicit_not_an_invented_summary(self):
        pubmed = self.pubmed.replace(b"<Abstract>", b"<Other>").replace(b"</Abstract>", b"</Other>")
        record = parse_record(self.cloud_metadata, self.jats, pubmed, self.identifiers)
        self.assertIsNone(record["abstract"])
        self.assertIsNone(record["abstract_summary"])
        self.assertTrue(record["abstract_absence_reason"])

    def test_old_cc_by_version_is_not_labelled_cc_by_4(self):
        jats = self.jats.replace(b"licenses/by/4.0", b"licenses/by/3.0")
        record = parse_record(self.cloud_metadata, jats, self.pubmed, self.identifiers)
        self.assertNotEqual(record["license"], "CC BY 4.0")
        self.assertEqual(record["eligibility"], "excluded")

    def test_mixed_jats_author_formats_preserve_order_and_complete_names(self):
        authors = b'''<contrib-group>
          <contrib contrib-type="author"><name><surname>Example</surname><given-names>Ada</given-names></name></contrib>
          <contrib contrib-type="editor"><string-name>Some Editor</string-name></contrib>
          <contrib contrib-type="author"><string-name><surname>Researcher</surname><given-names>Sam</given-names><suffix>Jr.</suffix></string-name></contrib>
          <contrib contrib-type="author"><string-name>Lee <italic>Sample</italic></string-name></contrib>
          <contrib contrib-type="author"><string-name><given-names>Pat</given-names> Synthetic</string-name></contrib>
          <contrib contrib-type="author"><collab>Synthetic Cardiac Study Group</collab></contrib>
        </contrib-group>'''
        start, end = self.jats.index(b"<contrib-group>"), self.jats.index(b"</contrib-group>") + len(b"</contrib-group>")
        jats = self.jats[:start] + authors + self.jats[end:]
        record = parse_record(self.cloud_metadata, jats, self.pubmed, self.identifiers)
        self.assertEqual(record["authors"], ["Ada Example", "Sam Researcher Jr.", "Lee Sample", "Pat Synthetic", "Synthetic Cardiac Study Group"])

    def test_unnamed_author_fails_instead_of_silently_writing_partial_list(self):
        jats = self.jats.replace(b"</contrib-group>", b'<contrib contrib-type="author"><xref>Some unsupported name</xref></contrib></contrib-group>')
        with self.assertRaisesRegex(ValueError, "author without a supported name"):
            parse_record(self.cloud_metadata, jats, self.pubmed, self.identifiers)

    def xml_service(self, checksum):
        metadata = dict(self.cloud_metadata, xml_url=f"s3://pmc-oa-opendata/PMC123456.2/test-article.xml?md5={checksum}")
        responses = [json.dumps(metadata).encode(), json.dumps(self.identifiers).encode(), self.pubmed, self.jats]
        return patch("fetch_article_metadata.read_bytes", side_effect=responses)

    def test_xml_checksum_match_allows_parsing_and_archival(self):
        with tempfile.TemporaryDirectory() as directory, self.xml_service(hashlib.md5(self.jats).hexdigest()):
            archive = Path(directory)
            record = fetch_metadata("PMC123456", 2, "some discovery query", "PMC123456-synthetic-cardiac-study.pdf", "cardiology", archive)
            self.assertEqual(record["authors"], ["Ada Example"])
            self.assertEqual(record["id"], "PMC123456-synthetic-cardiac-study")
            self.assertEqual(record["article_id"], record["id"])
            self.assertEqual(record["metadata_sources"]["article.xml"]["sha256"], hashlib.sha256(self.jats).hexdigest())
            self.assertEqual((archive / "PMC123456.2.article.xml").read_bytes(), self.jats)

    def test_xml_checksum_mismatch_does_not_write_record_or_archive(self):
        with tempfile.TemporaryDirectory() as directory, self.xml_service("0" * 32):
            output = Path(directory, "record.json")
            output.write_text("some existing record")
            archive = Path(directory, "archive")
            captured = io.StringIO()
            with contextlib.redirect_stdout(captured):
                result = main(["--pmcid", "PMC123456", "--pmc-version", "2", "--search-query", "some discovery query",
                               "--filename", "PMC123456-synthetic-cardiac-study.pdf", "--cluster", "cardiology", "--output", str(output), "--archive-dir", str(archive)])
            self.assertEqual(result, 1)
            self.assertIn("ERROR: PMC XML checksum mismatch", captured.getvalue())
            self.assertEqual(output.read_text(), "some existing record")
            self.assertFalse(archive.exists())

    @patch("fetch_article_metadata.read_bytes")
    def test_invalid_names_fail_before_network_or_archival(self, source_reader):
        names = ["synthetic-study.pdf", "PMC999999-synthetic-study.pdf",
                 "PMC123456.pdf", "PMC123456-Synthetic-study.pdf",
                 "PMC123456-synthetic_study.pdf", "../PMC123456-synthetic-study.pdf",
                 "PMC123456-one-two-three-four-five-six-seven-eight.pdf",
                 "PMC123456-synthetic--study.pdf"]
        with tempfile.TemporaryDirectory() as directory:
            archive = Path(directory, "archive")
            for name in names:
                with self.subTest(name=name), self.assertRaisesRegex(ValueError, "filename must"):
                    fetch_metadata("PMC123456", 2, "some discovery query", name, "cardiology", archive)
            source_reader.assert_not_called()
            self.assertFalse(archive.exists())

    def test_seven_word_summary_is_accepted(self):
        with self.xml_service(hashlib.md5(self.jats).hexdigest()):
            record = fetch_metadata("PMC123456", 2, "some discovery query",
                                    "PMC123456-one-two-three-four-five-six-seven.pdf", "cardiology")
        self.assertEqual(record["id"], "PMC123456-one-two-three-four-five-six-seven")

    def test_retraction_stops_candidate_metadata(self):
        metadata = dict(self.cloud_metadata, is_retracted=True)
        with self.assertRaisesRegex(ValueError, "retracted"):
            parse_record(metadata, self.jats, self.pubmed, self.identifiers)

    def test_pubmed_retraction_is_not_overridden_by_cloud_flag(self):
        pubmed = self.pubmed.replace(b"</MedlineCitation>", b'<CommentsCorrectionsList><CommentsCorrections RefType="RetractionIn"/></CommentsCorrectionsList></MedlineCitation>')
        with self.assertRaisesRegex(ValueError, "PubMed reports a retraction"):
            parse_record(self.cloud_metadata, self.jats, pubmed, self.identifiers)

    @patch("fetch_article_metadata.read_bytes")
    def test_invalid_input_and_wrong_deposit_version_fail_before_join(self, source_reader):
        with self.assertRaises(ValueError):
            fetch_metadata("123456", 2, "a search", "PMC123456-synthetic-study.pdf", "cardiology")
        source_reader.assert_not_called()
        source_reader.return_value = b'{"pmcid":"PMC123456","version":1}'
        with self.assertRaisesRegex(ValueError, "PMCID/version"):
            fetch_metadata("PMC123456", 2, "a search", "PMC123456-synthetic-study.pdf", "cardiology")

class MetadataRequestTests(unittest.TestCase):
    @patch("fetch_article_metadata.time.sleep")
    @patch("fetch_article_metadata.open_url")
    def test_rate_limit_is_retried_but_permanent_failure_is_not(self, opener, sleep):
        from urllib.error import HTTPError
        from unittest.mock import MagicMock
        from fetch_article_metadata import read_bytes
        response = MagicMock()
        response.__enter__.return_value.read.return_value = b"some metadata"
        opener.side_effect = [HTTPError("https://example.test", 429, "rate limit", {}, None), response]
        self.assertEqual(read_bytes("https://example.test"), b"some metadata")
        self.assertEqual(opener.call_count, 2)
        opener.reset_mock()
        opener.side_effect = HTTPError("https://example.test", 404, "missing", {}, None)
        with self.assertRaises(HTTPError):
            read_bytes("https://example.test")
        self.assertEqual(opener.call_count, 1)


class LicenceEligibilityTests(unittest.TestCase):
    def test_only_explicit_compatible_licence_evidence_passes(self):
        from fetch_article_metadata import licence_eligibility
        by = "https://creativecommons.org/licenses/by/4.0/"
        zero = "https://creativecommons.org/publicdomain/zero/1.0/"
        cases = [
            ("CC BY 4.0", [by], "eligible"),
            ("CC0 1.0", [zero], "eligible"),
            ("CC BY 4.0", [by, zero], "eligible"),
            ("CC BY 4.0", [], "excluded"),
            ("CC BY", [by], "excluded"),
            ("CC BY 4.0", [by, "https://creativecommons.org/licenses/by-nc/4.0/"], "excluded"),
            ("CC BY 4.0", ["https://example.test/licenses/by/4.0/"], "excluded"),
            ("CC BY 4.0", ["https://creativecommons.org/licenses/by/3.0/"], "excluded"),
        ]
        for name, urls, expected in cases:
            with self.subTest(name=name, urls=urls):
                self.assertEqual(licence_eligibility(name, urls), expected)


if __name__ == "__main__":
    unittest.main()
