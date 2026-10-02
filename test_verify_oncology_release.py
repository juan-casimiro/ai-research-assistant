"""Integrity checks against archived evidence, independent of corpus downloads."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from benchmark_scoring import canonical_hash
from fetch_article_metadata import parse_record
from verify_oncology_release import (ROOT, digest, verify, verify_attribution, verify_decision_record, verify_ledger, verify_linkage,
                                     verify_metadata, verify_migration, verify_production_oracle, verify_query_roles)


class ProductionOracleTests(unittest.TestCase):
    def test_self_consistent_false_ceiling_is_rejected_by_recomputation(self):
        from main import chunk_text
        from verify_benchmark_reachability import verify_reachability
        text = "A synthetic source reports a measured value of 7."
        benchmark = {"anchors": [{"id": "some_span", "article_id": "PMC123", "filename": "some-source.pdf",
                                   "text_start": 0, "text_end": len(text), "excerpt": text}],
                     "queries": [{"id": "o001", "category": "direct_lookup", "answerability": {"status": "answerable"},
                                  "required_facts": [{"id": "f1"}], "related_distractors": [],
                                  "evidence_sets": [{"anchors": ["some_span"], "fact_anchors": {"f1": ["some_span"]}}]}]}
        source_text = {"some-source.pdf": text}
        actual = verify_reachability(benchmark, source_text, chunk_text)
        verify_production_oracle(benchmark, source_text, actual)
        actual["query_feasibility"]["o001"] = {"minimum_chunks": 99, "by_depth": {"n3": "infeasible", "n8": "infeasible"}}
        for depth in actual["by_depth"].values():
            depth.update(feasible_ids=[], infeasible_ids=["o001"], feasible_queries=0, ceiling_rate=0.0)
        with self.assertRaisesRegex(ValueError, "production-chunker recomputation"):
            verify_production_oracle(benchmark, source_text, actual)


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
            "production_chunker_source_sha256": digest((ROOT / "main.py").read_bytes()),
            "result": {"evidence_queries": len(feasible_ids),
                       "query_feasibility": {qid: {"minimum_chunks": 1, "by_depth": {"n3": "feasible", "n8": "feasible"}} for qid in feasible_ids},
                       "by_depth": {depth: {"feasible_ids": feasible_ids, "infeasible_ids": [],
                                            "feasible_queries": len(feasible_ids), "total_queries": len(feasible_ids),
                                            "ceiling_rate": 1.0 if feasible_ids else None} for depth in ["n3", "n8"]}}})

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

    def test_oracle_tampering_is_rejected_with_current_linkage(self):
        changes = [
            lambda r: r["result"]["query_feasibility"]["o001"].update(minimum_chunks=99),
            lambda r: r["result"]["by_depth"]["n3"]["infeasible_ids"].append("o001"),
            lambda r: r["result"]["by_depth"]["n3"]["feasible_ids"].append("o001"),
            lambda r: r["result"]["by_depth"]["n3"].update(ceiling_rate=0.5),
            lambda r: r["result"]["by_depth"]["n8"].update(feasible_queries=99),
            lambda r: r.update(production_chunker_source_sha256="0" * 64),
            lambda r: r["result"]["query_feasibility"]["o001"]["by_depth"].update(n3="infeasible"),
        ]
        for change in changes:
            with self.subTest(change=changes.index(change)):
                self.write_oracle("C2", ["o001"])
                result = json.loads((self.release / "results/offline-C2.json").read_text())
                change(result)
                self.write("results/offline-C2.json", result)
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
        anchors = [{"id": "source_span", "article_id": "PMC1", "role": "support", "fact_ids": ["o001:f1"]},
                   {"id": "decoy_span", "article_id": "PMC2", "role": "support", "fact_ids": []},
                   {"id": "overlap_span", "article_id": "PMC3", "role": "support", "fact_ids": []}]
        query = {"id": "o001", "evidence_sets": [{"anchors": ["source_span"], "fact_anchors": {"f1": ["source_span"]}}],
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

    def test_false_premise_requires_positive_evidence(self):
        self.query["answerability"]["status"] = "false_premise"
        self.assert_rejected("positive correction")

    def test_anchor_fact_binding_and_role_tampering_is_rejected(self):
        for field, value in [("fact_ids", ["o001:unknown"]), ("fact_ids", []), ("role", "unknown")]:
            with self.subTest(field=field, value=value):
                self.setUp()
                self.benchmark["anchors"][0][field] = value
                self.assert_rejected("anchor role/fact_ids")

    def test_article_can_answer_one_query_and_distract_another(self):
        other = copy.deepcopy(self.query)
        other.update(id="o002", evidence_sets=[{"anchors": ["decoy_span"], "fact_anchors": {"f1": ["decoy_span"]}}],
                     related_distractors=[])
        other["dependencies"].update(required=["PMC2"], decoys=[])
        self.benchmark["queries"].append(other)
        self.benchmark["anchors"][1]["fact_ids"] = ["o002:f1"]
        verify_query_roles(self.benchmark)


class MigrationTests(unittest.TestCase):
    def setUp(self):
        ids = [f"q{n:03d}" for n in range(78, 120)]
        self.legacy = {qid: {"question": f"legacy question {qid}", "category": "direct_lookup"} for qid in ids}
        self.audit = {"cases": [{"id": qid, "question": f"legacy question {qid}", "legacy_category": "direct_lookup",
                                 "action": "retire_legacy_case", "replacement_cases": [], "negative_scope_review": "not_applicable"}
                                for qid in ids]}
        self.revised = self.audit["cases"][5]
        self.revised.update(action="revise_in_v1", legacy_category="unanswerable", negative_scope_review="absent_fact",
                            revised_question="revised test question", replacement_cases=[self.revised["id"]])
        self.legacy[self.revised["id"]]["category"] = "unanswerable"
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

    def test_legacy_category_drift_is_rejected(self):
        self.audit["cases"][0]["legacy_category"] = "multi_hop"
        self.assert_rejected("legacy category")

    def test_revised_case_cannot_link_to_unrelated_active_case(self):
        self.revised["replacement_cases"] = ["o001"]
        self.assert_rejected("link to itself")


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

    def test_broken_revision_hash_chain_is_rejected(self):
        self.ledger["revisions"].insert(0, {"query_sha256": "previous-query-hash"})
        self.ledger["revisions"][-1]["previous_query_sha256"] = "broken"
        self.assert_rejected("broken query revision chain")

    def test_category_history_must_agree_with_current_case(self):
        self.active["o001"]["category"] = "multi_hop"
        self.ledger["revisions"][-1]["recategorised_cases"] = {"o001": "direct_lookup -> false_premise"}
        self.assert_rejected("recategorised cases")

    def test_restored_case_must_be_revised_in_migration(self):
        self.ledger["revisions"][-1]["restored_cases"] = ["q100"]
        self.assert_rejected("restored cases")

    def test_dropped_link_cannot_remain_in_migration(self):
        self.ledger["revisions"][-1]["dropped_replacement_links"] = {"q100": ["o002"]}
        self.assert_rejected("dropped replacement links")

    def test_explicit_reintroduction_of_a_dropped_link_passes(self):
        self.ledger["revisions"][-1].update(dropped_replacement_links={"q100": ["o002"]},
                                            added_replacement_links={"q100": ["o002"]})
        verify_ledger(self.ledger, self.active, self.audit)


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

    def test_body_edit_is_rejected_even_when_every_heading_is_present(self):
        with self.assertRaisesRegex(ValueError, "generated decision record"):
            verify_decision_record(self.record + "Changed rationale.\n", self.benchmark, self.audit,
                                   self.candidates, self.ledger, expected_record=self.record)

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
