import copy
import unittest
from unittest.mock import patch

from fetch_article_metadata import fetch_metadata, parse_record


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
        self.assertEqual(record["eligibility"], "pending")
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
            fetch_metadata("123456", 2, "a search", "test.pdf", "cardiology")
        source_reader.assert_not_called()
        source_reader.return_value = b'{"pmcid":"PMC123456","version":1}'
        with self.assertRaisesRegex(ValueError, "PMCID/version"):
            fetch_metadata("PMC123456", 2, "a search", "test.pdf", "cardiology")


if __name__ == "__main__":
    unittest.main()
