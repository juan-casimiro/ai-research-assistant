"""Integrity checks against archived evidence, independent of corpus downloads."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from benchmark_scoring import canonical_hash
from fetch_article_metadata import parse_record
from verify_oncology_release import verify, verify_linkage, verify_metadata


class ArchivedMetadataTests(unittest.TestCase):
    def setUp(self):
        self.cloud = {"pmcid": "PMC123", "version": 1, "doi": "10.123/test", "pmid": 123}
        self.identifiers = {"records": [{"pmcid": "PMC123", "doi": "10.123/test", "pmid": 123}]}
        self.xml = b'''<article article-type="research-article"><front>
        <journal-meta><journal-title-group><journal-title>Test Journal</journal-title></journal-title-group></journal-meta>
        <article-meta><article-id pub-id-type="doi">10.123/test</article-id>
        <title-group><article-title>Source title</article-title></title-group>
        <contrib-group><contrib contrib-type="author"><name><given-names>A</given-names><surname>Researcher</surname></name></contrib></contrib-group>
        <pub-date pub-type="epub"><year>2026</year><month>10</month><day>2</day></pub-date>
        <permissions><license xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="https://creativecommons.org/licenses/by/4.0/">Source licence</license></permissions>
        </article-meta></front><body><fig id="f1"><label>Figure 1</label><caption>Source caption</caption><attrib>Original artwork</attrib></fig></body></article>'''
        self.pubmed = b'''<PubmedArticleSet><PubmedArticle><MedlineCitation><PMID>123</PMID><Article>
        <ArticleTitle>Source title.</ArticleTitle><Abstract><AbstractText>Source abstract.</AbstractText></Abstract>
        </Article></MedlineCitation><PubmedData><ArticleIdList><ArticleId IdType="doi">10.123/test</ArticleId></ArticleIdList></PubmedData></PubmedArticle></PubmedArticleSet>'''
        self.article = parse_record(self.cloud, self.xml, self.pubmed, self.identifiers)
        self.article.update(article_id="PMC123", licence={"notice": self.article["license_notes"], "url": self.article["licence_urls"][0]},
                            third_party_review={"inventory": [{"type": "fig", "id": "f1", "label": "Figure 1", "caption": "Source caption", "credits": ["Original artwork"]}]})

    def test_matching_archived_metadata_passes(self):
        verify_metadata(self.article, self.cloud, self.xml, self.pubmed, self.identifiers)

    def test_changed_manifest_metadata_cannot_be_recertified_by_its_own_hash(self):
        for field, value in [("title", "Different title"), ("authors", ["Someone else"]),
                             ("abstract", "Different abstract"), ("license", "CC BY-NC 4.0")]:
            with self.subTest(field=field):
                changed = copy.deepcopy(self.article)
                changed[field] = value
                with self.assertRaisesRegex(ValueError, f"archived {field}"):
                    verify_metadata(changed, self.cloud, self.xml, self.pubmed, self.identifiers)

    def test_removed_third_party_credit_is_rejected(self):
        changed = copy.deepcopy(self.article)
        changed["third_party_review"]["inventory"][0]["credits"] = []
        with self.assertRaisesRegex(ValueError, "credit inventory"):
            verify_metadata(changed, self.cloud, self.xml, self.pubmed, self.identifiers)

    def test_converter_identity_mismatch_is_rejected(self):
        identifiers = copy.deepcopy(self.identifiers)
        identifiers["records"][0]["doi"] = "10.123/other"
        with self.assertRaisesRegex(ValueError, "converter disagrees"):
            verify_metadata(self.article, self.cloud, self.xml, self.pubmed, identifiers)


class AuxiliaryLinkageTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.release = Path(directory.name)
        (self.release / "results").mkdir()
        self.benchmark = {"queries": [{"id": "o001", "revision": 1, "category": "direct_lookup", "dependencies": {"required": ["PMC123"]}}]}
        self.manifest = {"fingerprint_sha256": "selection-hash", "articles": [{"article_id": "PMC123"}]}
        self.conditions = {"conditions": {"C1": {}, "C2": {}}}
        query_hash = canonical_hash(self.benchmark)
        for name in ["case_review.json", "revision_ledger.json", "evidence_map.json"]:
            self.write(name, {"query_sha256": query_hash, "articles": [{"article_id": "PMC123"}]})
        self.write("case_dependencies.json", {"query_sha256": query_hash, "cases": [{"id": "o001", "revision": 1, "category": "direct_lookup", "required": ["PMC123"]}]})
        for condition in ["C1", "C2"]:
            self.write(f"results/offline-{condition}.json", {"query_sha256": query_hash,
                       "selection_sha256": "selection-hash", "conditions_sha256": canonical_hash(self.conditions)})

    def write(self, name, value):
        (self.release / name).write_text(json.dumps(value))

    def verify(self):
        verify_linkage(self.release, self.benchmark, self.manifest, self.conditions)

    def test_matching_linked_files_pass(self):
        self.verify()

    def test_stale_auxiliary_query_hash_is_rejected(self):
        self.write("case_review.json", {"query_sha256": "stale"})
        with self.assertRaisesRegex(ValueError, "stale query linkage"):
            self.verify()

    def test_changed_dependency_content_is_rejected_even_with_current_hash(self):
        self.write("case_dependencies.json", {"query_sha256": canonical_hash(self.benchmark), "cases": []})
        with self.assertRaisesRegex(ValueError, "dependency content"):
            self.verify()

    def test_old_oracle_results_are_rejected_after_condition_change(self):
        self.conditions["conditions"]["C2"]["new_member"] = "PMC456"
        with self.assertRaisesRegex(ValueError, "stale oracle linkage"):
            self.verify()


class CorpusMembershipTests(unittest.TestCase):
    def test_unselected_pdf_is_rejected_before_parsing(self):
        with tempfile.TemporaryDirectory() as directory:
            corpus = Path(directory)
            (corpus / "selected.pdf").write_bytes(b"selected")
            (corpus / "deferred.pdf").write_bytes(b"deferred")
            manifest = {"articles": [{"article_id": "PMC123", "filename": "selected.pdf"}]}
            with patch("verify_oncology_release.read_release", return_value=({}, manifest, {}, None, None, None)):
                with self.assertRaisesRegex(ValueError, "unselected PDFs"):
                    verify(corpus / "release", corpus)

    def test_missing_selected_pdf_is_rejected_before_parsing(self):
        with tempfile.TemporaryDirectory() as directory:
            corpus = Path(directory)
            manifest = {"articles": [{"article_id": "PMC123", "filename": "selected.pdf"}]}
            with patch("verify_oncology_release.read_release", return_value=({}, manifest, {}, None, None, None)):
                with self.assertRaisesRegex(ValueError, "missing or unselected"):
                    verify(corpus / "release", corpus)


if __name__ == "__main__":
    unittest.main()
