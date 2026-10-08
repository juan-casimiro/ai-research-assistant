import copy
import contextlib
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tools.corpus.fetch_article_metadata import fetch_metadata, main, parse_record


class ArticleMetadataTests(unittest.TestCase):
    def setUp(self):
        self.cloud_metadata = {
            "pmcid": "PMC123456", "version": 2, "pmid": 987654,
            "pdf_url": "s3://pmc-oa-opendata/PMC123456.2/synthetic.pdf",
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
          <contrib contrib-type="author"><collab>Synthetic <italic>Cardiac</italic> Study Group<xref ref-type="aff">1</xref><contrib-group><contrib contrib-type="author"><name><given-names>Nested</given-names><surname>Member</surname></name><email>member@example.test</email></contrib></contrib-group></collab></contrib>
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
        return patch("tools.corpus.fetch_article_metadata.read_bytes", side_effect=responses)

    def test_latest_version_is_pinned_and_lookup_evidence_retained(self):
        identifiers = copy.deepcopy(self.identifiers)
        identifiers['records'][0]['versions'] = [
            {'pmcid': 'PMC123456.1', 'current': False},
            {'pmcid': 'PMC123456.2', 'current': True},
        ]
        cloud = dict(self.cloud_metadata, xml_url='s3://pmc-oa-opendata/PMC123456.2/synthetic.xml?md5=' + hashlib.md5(self.jats).hexdigest())
        raw = json.dumps(identifiers).encode()
        responses = [raw, json.dumps(cloud).encode(), self.pubmed, self.jats]
        with tempfile.TemporaryDirectory() as directory, patch('tools.corpus.fetch_article_metadata.read_bytes', side_effect=responses) as source_reader:
            result = fetch_metadata('PMC123456', archive_dir=Path(directory))
            self.assertEqual(result['pmc_version'], 2)
            self.assertIn('PMC123456.2.json', source_reader.call_args_list[1].args[0])
            self.assertEqual((Path(directory)/'PMC123456.2.id-converter.json').read_bytes(), raw)
            self.assertEqual(result['metadata_sources']['id-converter.json']['sha256'], hashlib.sha256(raw).hexdigest())
            self.assertEqual(result['filename'], 'PMC123456-a-synthetic-cardiac-study.pdf')
            self.assertEqual(result['cluster'], '')
            self.assertEqual(result['selection_rationale'], '')
            self.assertIn('User supplied PMCID', result['search_query'])

    def test_explicit_version_is_not_replaced_by_current_version(self):
        self.identifiers['records'][0]['versions'] = [{'pmcid': 'PMC123456.3', 'current': True}]
        with self.xml_service(hashlib.md5(self.jats).hexdigest()):
            result = fetch_metadata('PMC123456', 2, cluster='test-topic')
        self.assertEqual(result['pmc_version'], 2)
        self.assertIn('/PMC123456.2/', result['metadata_sources']['pdf']['url'])

    def test_selection_fetch_loops_and_prints_reviewed_filename(self):
        from tests.corpus.test_build_corpus_manifest import record
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            selection = root/'candidates.json'
            articles = [{'pmcid': 'PMC123456', 'cluster': 'test-topic',
                         'filename': 'PMC123456-reviewed-study.pdf'},
                        {'pmcid': 'PMC999', 'cluster': 'test-topic'}]
            selection.write_text(json.dumps({'articles': articles}))
            before = selection.read_bytes()
            with patch('tools.corpus.fetch_article_metadata.fetch_metadata', side_effect=[record(), OSError('synthetic failure')]) as fetcher, contextlib.redirect_stdout(io.StringIO()) as report:
                self.assertEqual(main(['--selection-file', str(selection), '--records-dir', str(root/'metadata'), '--archive-dir', str(root/'provenance')]), 1)
            self.assertEqual(fetcher.call_count, 2)
            self.assertEqual(fetcher.call_args_list[0].args[3:5], ('PMC123456-reviewed-study.pdf', 'test-topic'))
            self.assertIn('PMC123456-synthetic-study.pdf', report.getvalue())
            self.assertIn('PMC999', report.getvalue())
            self.assertEqual(selection.read_bytes(), before)

    def test_pmcid_filter_preserves_other_records_and_uses_selection_fields(self):
        from tests.corpus.test_build_corpus_manifest import record
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            records = root/'metadata'; records.mkdir()
            untouched = records/'PMC999.json'
            untouched.write_bytes(b'{"synthetic": "existing record"}\n')
            before = untouched.read_bytes()
            selection = root/'candidates.json'
            selection.write_text(json.dumps({'articles': [
                {'pmcid': 'PMC123456', 'pmc_version': 2, 'cluster': 'test-topic',
                 'filename': 'PMC123456-reviewed-study.pdf', 'search_query': 'some query'},
                {'pmcid': 'PMC999', 'cluster': 'another topic'}]}))
            with patch('tools.corpus.fetch_article_metadata.fetch_metadata', return_value=record()) as fetcher, contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(main(['--selection-file', str(selection), '--records-dir', str(records),
                                       '--archive-dir', str(root/'provenance'), '--pmcid', 'PMC123456']), 0)
            fetcher.assert_called_once_with('PMC123456', 2, 'some query',
                                           'PMC123456-reviewed-study.pdf', 'test-topic', root/'provenance')
            self.assertEqual(untouched.read_bytes(), before)
            self.assertTrue((records/'PMC123456.json').exists())
            selected = json.loads(selection.read_text())
            selected['articles'].append({'pmcid': 'PMC888', 'cluster': 'test-topic'})
            selection.write_text(json.dumps(selected))
            with patch('tools.corpus.fetch_article_metadata.fetch_metadata', side_effect=[record(), dict(record(), pmcid='PMC888')]) as fetcher, contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(main(['--selection-file', str(selection), '--records-dir', str(records),
                                       '--archive-dir', str(root/'provenance'), '--pmcid', 'PMC123456',
                                       '--pmcid', 'PMC888']), 0)
            self.assertEqual([call.args[0] for call in fetcher.call_args_list], ['PMC123456', 'PMC888'])
            self.assertEqual(untouched.read_bytes(), before)
            self.assertTrue((records/'PMC888.json').exists())

    def test_refetch_preserves_topic_rationale_and_uses_supplied_selection_rationale(self):
        from tests.corpus.test_build_corpus_manifest import record
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            records = root/'metadata'; records.mkdir()
            output = records/'PMC123456.json'
            output.write_text(json.dumps(dict(record(), selection_rationale='Some selection reason',
                                              topic_rationale='Some topic reason')))
            selection = root/'candidates.json'
            article = {'pmcid': 'PMC123456', 'cluster': '', 'search_query': ''}
            for replacement in [None, 'Some revised selection reason']:
                if replacement:
                    article['selection_rationale'] = replacement
                selection.write_text(json.dumps({'articles': [article]}))
                with patch('tools.corpus.fetch_article_metadata.fetch_metadata', return_value=record()), contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(main(['--selection-file', str(selection), '--records-dir', str(records),
                                           '--archive-dir', str(root/'provenance'), '--pmcid', 'PMC123456']), 0)
                fetched = json.loads(output.read_text())
                self.assertEqual(fetched['selection_rationale'], replacement or '')
                self.assertEqual(fetched['topic_rationale'], 'Some topic reason')

    def test_unknown_pmcid_filter_fails_before_network(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            selection = root/'candidates.json'
            selection.write_text(json.dumps({'articles': [{'pmcid': 'PMC123456'}]}))
            with patch('tools.corpus.fetch_article_metadata.read_bytes') as source_reader, contextlib.redirect_stdout(io.StringIO()) as report:
                self.assertEqual(main(['--selection-file', str(selection), '--records-dir', str(root/'metadata'),
                                       '--archive-dir', str(root/'provenance'), '--pmcid', 'PMC123456',
                                       '--pmcid', 'PMC999']), 1)
            source_reader.assert_not_called()
            self.assertIn('PMC999', report.getvalue())
            self.assertFalse((root/'metadata').exists())

    def test_latest_without_unique_current_deposit_fails_and_retains_response(self):
        raw = json.dumps(self.identifiers).encode()
        with tempfile.TemporaryDirectory() as directory, patch('tools.corpus.fetch_article_metadata.read_bytes', return_value=raw):
            with self.assertRaisesRegex(ValueError, 'current deposit'):
                fetch_metadata('PMC123456', cluster='test-topic', archive_dir=Path(directory))
            self.assertEqual((Path(directory)/'PMC123456.id-converter.json').read_bytes(), raw)
        # No fallback to version one or a guessed version.

    def test_fetch_rejects_missing_pubmed_abstract(self):
        self.pubmed = self.pubmed.replace(b"<Abstract>", b"<Other>").replace(b"</Abstract>", b"</Other>")
        with self.xml_service(hashlib.md5(self.jats).hexdigest()), self.assertRaisesRegex(ValueError, "abstract"):
            fetch_metadata("PMC123456", 2, "some discovery query", "PMC123456-synthetic-study.pdf", "test-topic")

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
            selection = Path(directory, 'candidates.json')
            selection.write_text(json.dumps({'articles': [{'pmcid': 'PMC123456', 'pmc_version': 2, 'cluster': 'test-topic'}]}))
            captured = io.StringIO()
            with contextlib.redirect_stdout(captured):
                result = main(['--selection-file', str(selection), '--records-dir', str(Path(directory)/'metadata'), '--archive-dir', str(archive)])
            self.assertEqual(result, 1)
            self.assertIn("FAILED PMC123456: PMC XML checksum mismatch", captured.getvalue())
            self.assertEqual(output.read_text(), "some existing record")
            self.assertFalse(archive.exists())

    @patch("tools.corpus.fetch_article_metadata.read_bytes")
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

    @patch("tools.corpus.fetch_article_metadata.read_bytes")
    def test_invalid_input_and_wrong_deposit_version_fail_before_join(self, source_reader):
        with self.assertRaises(ValueError):
            fetch_metadata("123456", 2, "a search", "PMC123456-synthetic-study.pdf", "cardiology")
        source_reader.assert_not_called()
        source_reader.return_value = b'{"pmcid":"PMC123456","version":1}'
        with self.assertRaisesRegex(ValueError, "PMCID/version"):
            fetch_metadata("PMC123456", 2, "a search", "PMC123456-synthetic-study.pdf", "cardiology")

class MetadataRequestTests(unittest.TestCase):
    @patch("tools.corpus.fetch_article_metadata.time.sleep")
    @patch("tools.corpus.fetch_article_metadata.open_url")
    def test_rate_limit_is_retried_but_permanent_failure_is_not(self, opener, sleep):
        from urllib.error import HTTPError
        from unittest.mock import MagicMock
        from tools.corpus.fetch_article_metadata import read_bytes
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
        from tools.corpus.fetch_article_metadata import licence_eligibility
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
