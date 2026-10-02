"""Integrity checks against archived evidence, independent of corpus downloads."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from benchmark_scoring import canonical_hash
from fetch_article_metadata import parse_record
from verify_oncology_release import (verify, verify_attribution, verify_decision_record, verify_ledger, verify_linkage,
                                     verify_metadata, verify_migration, verify_query_roles)


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
        self.benchmark = {"queries": [{"id": "o001", "revision": 1, "category": "direct_lookup", "evidence_sets": [{"anchors": ["a1"]}],
                                       "dependencies": {"required": ["PMC123"]}}]}
        self.manifest = {"fingerprint_sha256": "selection-hash", "articles": [{"article_id": "PMC123"}]}
        self.conditions = {"conditions": {"C1": {"membership_sha256": "c1-members"}, "C2": {"membership_sha256": "c2-members"}}}
        query_hash = canonical_hash(self.benchmark)
        for name in ["case_review.json", "revision_ledger.json", "evidence_map.json"]:
            self.write(name, {"query_sha256": query_hash, "articles": [{"article_id": "PMC123"}]})
        self.write("case_dependencies.json", {"query_sha256": query_hash, "cases": [{"id": "o001", "revision": 1, "category": "direct_lookup", "required": ["PMC123"]}]})
        for condition in ["C1", "C2"]:
            self.write_oracle(condition, ["o001"])

    def write_oracle(self, condition, feasible_ids):
        self.write(f"results/offline-{condition}.json", {
            "query_sha256": canonical_hash(self.benchmark), "selection_sha256": "selection-hash",
            "conditions_sha256": canonical_hash(self.conditions), "condition": condition,
            "membership_sha256": self.conditions["conditions"][condition]["membership_sha256"],
            "result": {"evidence_queries": len(feasible_ids),
                       "query_feasibility": {qid: {"minimum_chunks": 1} for qid in feasible_ids},
                       "by_depth": {"n3": {"feasible_ids": feasible_ids, "infeasible_ids": []}}}})

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

    def test_oracle_missing_an_evidence_case_is_rejected_even_with_current_hashes(self):
        self.write_oracle("C2", [])
        with self.assertRaisesRegex(ValueError, "oracle content"):
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


class AttributionTests(unittest.TestCase):
    def setUp(self):
        self.articles = [{"article_id": "PMC123", "attribution_id": "PMC123", "title": "Some title", "doi": "10.123/test",
                          "article_url": "https://example.org/PMC123", "licence": {"url": "https://example.org/licence"},
                          "authors": ["A Researcher"]}]
        self.attribution = ('<a id="PMC123"></a>\n\n- [Some title](https://example.org/PMC123). A Researcher. '
                            'doi:10.123/test. https://example.org/licence\n')

    def test_complete_attribution_passes(self):
        verify_attribution(self.articles, self.attribution)

    def test_missing_attribution_entry_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "membership"):
            verify_attribution(self.articles, self.attribution.replace("PMC123\"></a>", "PMC456\"></a>"))

    def test_missing_author_credit_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "citation component"):
            verify_attribution(self.articles, self.attribution.replace("A Researcher", "Someone else"))


class QueryRoleTests(unittest.TestCase):
    def setUp(self):
        anchors = [{"id": "source_span", "article_id": "PMC1"}, {"id": "decoy_span", "article_id": "PMC2"},
                   {"id": "overlap_span", "article_id": "PMC3"}]
        query = {"id": "o001", "evidence_sets": [{"anchors": ["source_span"]}],
                 "related_distractors": [{"article_id": "PMC2", "anchor_id": "decoy_span"}],
                 "answerability": {"status": "answerable"},
                 "dependencies": {"required": ["PMC1"], "alternatives": [], "decoys": ["PMC2"],
                                  "overlap_review": ["PMC1", "PMC2", "PMC3"],
                                  "overlap_findings": [{"article_id": "PMC3", "anchor_id": "overlap_span", "role": "partial_support"}]}}
        self.benchmark = {"anchors": anchors, "queries": [query]}
        self.query = query

    def assert_rejected(self, message):
        with self.assertRaisesRegex(ValueError, message):
            verify_query_roles(self.benchmark)

    def test_consistent_roles_pass(self):
        verify_query_roles(self.benchmark)

    def test_named_decoy_recorded_as_supporting_overlap_is_rejected(self):
        self.query["dependencies"]["overlap_findings"][0].update(article_id="PMC2", anchor_id="decoy_span")
        self.assert_rejected("both a named decoy and supporting overlap")

    def test_unknown_overlap_or_negative_context_anchor_is_rejected(self):
        for field in ["overlap_findings", "negative_context"]:
            with self.subTest(field=field):
                self.setUp()
                self.query["dependencies"][field] = [{"article_id": "PMC3", "anchor_id": "missing_span", "role": "partial_support"}]
                self.assert_rejected("does not resolve")

    def test_overlap_anchor_from_another_article_is_rejected(self):
        self.query["dependencies"]["overlap_findings"][0]["anchor_id"] = "source_span"
        self.assert_rejected("does not resolve")

    def test_overlap_review_without_named_decoy_is_rejected(self):
        self.query["dependencies"]["overlap_review"] = ["PMC1", "PMC3", "PMC9"]
        self.assert_rejected("overlap review omits")

    def test_decoy_dependency_mismatch_is_rejected(self):
        self.query["dependencies"]["decoys"] = []
        self.assert_rejected("decoy dependencies")

    def test_correction_anchor_outside_gold_evidence_is_rejected(self):
        self.query["answerability"]["correction_anchors"] = ["decoy_span"]
        self.assert_rejected("correction anchor")


class MigrationTests(unittest.TestCase):
    def setUp(self):
        ids = [f"q{n:03d}" for n in range(78, 120)]
        self.legacy = {qid: {"question": f"legacy question {qid}"} for qid in ids}
        self.audit = {"cases": [{"id": qid, "question": f"legacy question {qid}", "legacy_category": "direct_lookup",
                                 "action": "retire_legacy_case", "replacement_cases": [], "negative_scope_review": "not_applicable"}
                                for qid in ids]}
        self.revised = self.audit["cases"][5]
        self.revised.update(action="revise_in_v1", legacy_category="unanswerable", negative_scope_review="absent_fact",
                            revised_question="revised test question", replacement_cases=[self.revised["id"]])
        self.active = {self.revised["id"]: {"revision": 2, "question": "revised test question",
                                            "answerability": {"status": "absent_fact"}},
                       "o001": {"revision": 1, "question": "test question", "answerability": {"status": "answerable"}}}

    def assert_rejected(self, message):
        with self.assertRaisesRegex(ValueError, message):
            verify_migration(self.audit, self.active, self.legacy)

    def test_consistent_migration_passes(self):
        verify_migration(self.audit, self.active, self.legacy)

    def test_missing_legacy_case_is_rejected(self):
        self.audit["cases"].pop()
        self.assert_rejected("fully accounted")

    def test_changed_legacy_question_is_rejected(self):
        self.audit["cases"][0]["question"] = "different question"
        self.assert_rejected("preserve legacy question")

    def test_retired_case_still_active_is_rejected(self):
        self.active[self.audit["cases"][0]["id"]] = self.active["o001"]
        self.assert_rejected("retired ID remains active")

    def test_unknown_replacement_is_rejected(self):
        self.audit["cases"][0]["replacement_cases"] = ["o999"]
        self.assert_rejected("unknown replacement")

    def test_revised_question_drift_is_rejected(self):
        self.active[self.revised["id"]]["question"] = "edited test question"
        self.assert_rejected("revised question differs")

    def test_revised_negative_answerability_drift_is_rejected(self):
        self.active[self.revised["id"]]["answerability"]["status"] = "false_premise"
        self.assert_rejected("answerability differs")

    def test_unrevised_active_case_is_rejected(self):
        self.active[self.revised["id"]]["revision"] = 1
        self.assert_rejected("missing revised case")


class LedgerTests(unittest.TestCase):
    def setUp(self):
        self.audit = {"cases": [{"id": "q100", "action": "retire_legacy_case", "replacement_cases": ["o002"]},
                                {"id": "q101", "action": "retire_legacy_case", "replacement_cases": ["o001"]},
                                {"id": "q102", "action": "revise_in_v1", "replacement_cases": ["q102"]}]}
        self.active = {"o001": {"supersedes_coverage_of": "q101"}, "o002": {}, "q102": {}}
        self.ledger = {"query_sha256": "query-hash", "renamed_coverage_cases": {"q101": "o001"},
                       "withdrawn_cases": {"q100": {"coverage_retained_by": "o002"}, "o003": {"coverage_retained_by": "o002"}},
                       "retained_id_task_changes": {"q102": "test note"},
                       "revisions": [{"query_sha256": "query-hash", "changed_cases": ["o001"]}]}

    def assert_rejected(self, message):
        with self.assertRaisesRegex(ValueError, message):
            verify_ledger(self.ledger, self.active, self.audit)

    def test_consistent_ledger_passes(self):
        verify_ledger(self.ledger, self.active, self.audit)

    def test_rename_without_active_supersedes_link_is_rejected(self):
        del self.active["o001"]["supersedes_coverage_of"]
        self.assert_rejected("renamed coverage differs")

    def test_rename_not_retired_in_audit_is_rejected(self):
        self.audit["cases"][1]["replacement_cases"] = []
        self.assert_rejected("not retired in favour")

    def test_withdrawn_case_still_active_is_rejected(self):
        self.active["o003"] = {}
        self.assert_rejected("withdrawn o003")

    def test_withdrawn_case_without_active_coverage_is_rejected(self):
        self.ledger["withdrawn_cases"]["o003"]["coverage_retained_by"] = "o999"
        self.assert_rejected("withdrawn o003")

    def test_withdrawn_legacy_case_not_retired_is_rejected(self):
        self.audit["cases"][0]["action"] = "revise_in_v1"
        self.assert_rejected("withdrawn legacy q100")

    def test_retained_id_note_for_unrevised_case_is_rejected(self):
        self.ledger["retained_id_task_changes"] = {"q101": "test note"}
        self.assert_rejected("retained-ID note")

    def test_stale_latest_revision_is_rejected(self):
        self.ledger["revisions"][-1]["query_sha256"] = "stale"
        self.assert_rejected("latest revision")


class DecisionRecordTests(unittest.TestCase):
    def setUp(self):
        self.benchmark = {"queries": [
            {"id": "o001", "selection_rationale": "test rationale one", "review": {"duplicate_leakage_check": "test overlap"}},
            {"id": "o002", "selection_rationale": "test rationale two", "review": {"duplicate_leakage_check": "test overlap"}}]}
        self.audit = {"cases": [{"id": "q100", "action": "retire_legacy_case", "replacement_cases": ["o001"], "replacement_basis": "test basis"}]}
        self.candidates = {"candidates": [{"pmcid": "PMC1", "disposition": "selected"}, {"pmcid": "PMC2", "disposition": "rejected"}]}
        self.ledger = {"withdrawn_cases": {"o003": {}}}
        self.record = "#### o001 (revision 1)\n#### o002 (revision 1)\n- **o003:** test\n| q100 | x |\n| PMC2 | x |\n### PMC1 — test\n"

    def verify(self):
        verify_decision_record(self.record, self.benchmark, self.audit, self.candidates, self.ledger)

    def test_complete_record_passes(self):
        self.verify()

    def test_shared_boilerplate_rationale_is_rejected(self):
        self.benchmark["queries"][1]["selection_rationale"] = "test rationale one"
        with self.assertRaisesRegex(ValueError, "boilerplate"):
            self.verify()

    def test_missing_near_duplicate_review_is_rejected(self):
        del self.benchmark["queries"][0]["review"]["duplicate_leakage_check"]
        with self.assertRaisesRegex(ValueError, "near-duplicate review"):
            self.verify()

    def test_replacement_link_without_basis_is_rejected(self):
        self.audit["cases"][0]["replacement_basis"] = None
        with self.assertRaisesRegex(ValueError, "no recorded basis"):
            self.verify()

    def test_undocumented_case_or_candidate_is_rejected(self):
        for removed in ["#### o002 (revision 1)\n", "| PMC2 | x |\n", "- **o003:** test\n"]:
            with self.subTest(removed=removed):
                self.record = self.record.replace(removed, "")
                with self.assertRaisesRegex(ValueError, "DECISIONS.md does not record"):
                    self.verify()
                self.setUp()


if __name__ == "__main__":
    unittest.main()
