"""Offline contract tests for pinned evidence, release dependencies and run guards."""
import contextlib
from copy import deepcopy
import io
import json
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest
from unittest.mock import AsyncMock, Mock, patch
from chromadb.errors import InternalError
import compare_evals

from benchmark_scoring import (CATEGORIES, FEASIBILITY_VERSION, canonical_hash, compile_anchor_spans,
                               compile_query_feasibility, evidence_coverage_report, feasibility_from_minimum,
                               minimum_evidence_witness, score_evidence, validate_answerability, validate_benchmark)
from compare_evals import check_compatible
import eval_benchmark as runner
from verify_benchmark_reachability import verify_reachability

ROOT = Path(__file__).resolve().parent


def fixture():
    anchors = {key: {"id": key, "article_id": doc, "filename": doc + ".pdf",
                     "excerpt": text, "text_start": offset, "text_end": offset + len(text)}
               for key, doc, text, offset in [
                   ("a", "A", "At six months, adjusted HR was 0.35.", 0),
                   ("b", "A", "The population excluded dialysis patients.", 100),
                   ("c", "B", "The complete alternative reports both scoped facts.", 0),
                   ("d", "D", "A different cohort had adjusted HR 0.35.", 0)]}
    query = {"id": "test", "revision": 1, "question": "What were the scoped findings?",
             "category": "direct_lookup", "answerability": {"status": "answerable"},
             "required_facts": [{"id": "f1"}, {"id": "f2"}], "related_distractors": [],
             "evidence_sets": [
                 {"id": "primary", "anchors": ["a", "b"], "fact_anchors": {"f1": ["a"], "f2": ["b"]}},
                 {"id": "alternative", "anchors": ["c"], "fact_anchors": {"f1": ["c"], "f2": ["c"]}}]}
    return query, anchors


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.q, self.a = fixture()

    def score(self, ids, sources=None):
        return score_evidence([self.a[i]["excerpt"] for i in ids],
                              sources or [self.a[i]["filename"] for i in ids], self.q, self.a)

    def test_document_presence_is_not_complete_evidence(self):
        result = self.score(["a"])
        self.assertEqual(result["document_coverage"], "pass")
        self.assertEqual(result["evidence_coverage"], "fail")
        self.assertEqual(result["fact_recall"], 0.5)
        self.assertEqual(result["anchor_matches"]["a"], [0])

    def test_every_primary_fact_or_a_complete_alternative_is_required(self):
        self.assertEqual(self.score(["a", "b"])["evidence_coverage"], "pass")
        self.assertEqual(self.score(["c"])["evidence_coverage"], "pass")
        # Mixing partial alternative sets must not pass complete coverage.
        self.q["evidence_sets"][1] = {"id": "alternative", "anchors": ["c", "d"],
                                     "fact_anchors": {"f1": ["c"], "f2": ["d"]}}
        result = self.score(["a", "d"])
        self.assertEqual(result["fact_recall"], 1)
        self.assertEqual(result["evidence_coverage"], "fail")

    def test_wrong_source_naked_number_and_chunk_concatenation_do_not_match(self):
        self.assertEqual(self.score(["a", "b"], ["D.pdf", "D.pdf"])["evidence_coverage"], "fail")
        result = score_evidence(["HR 0.35", "dialysis patients"], ["A.pdf"] * 2, self.q, self.a)
        self.assertEqual(result["fact_recall"], 0)
        text = self.a["a"]["excerpt"]
        result = score_evidence([text[:20], text[20:]], ["A.pdf"] * 2, self.q, self.a)
        self.assertEqual(result["fact_recall"], 0)
        with self.assertRaises(ValueError):
            score_evidence([text], [], self.q, self.a)

    def test_typographic_whitespace_preserves_signs_and_scope(self):
        text = self.a["a"]["excerpt"].replace(" ", "\n  ")
        result = score_evidence([text], ["A.pdf"], self.q, self.a)
        self.assertEqual(result["fact_recall"], 0.5)
        result = score_evidence([text.replace("0.35", "−0.35")], ["A.pdf"], self.q, self.a)
        self.assertEqual(result["fact_recall"], 0)

    def test_synthesis_requires_both_articles_and_decoys_use_first_reranked_rank(self):
        self.q["evidence_sets"] = [{"id": "two", "anchors": ["a", "c"],
                                   "fact_anchors": {"f1": ["a"], "f2": ["c"]}}]
        self.assertEqual(self.score(["a"])["document_coverage"], "fail")
        self.assertEqual(self.score(["a", "c"])["evidence_coverage"], "pass")
        self.q["category"] = "cross_doc_distractor"
        self.q["related_distractors"] = [{"filename": "D.pdf"}]
        self.assertEqual(self.score(["a", "c", "d"])["distractor_ordering"], "pass")
        self.assertEqual(self.score(["a", "d", "c"])["distractor_ordering"], "fail")
        self.assertEqual(self.score(["a", "a", "c"])["distractor_ordering"], "pass")

    def test_absent_facts_are_unscored_and_false_premise_correction_evidence_is_scored(self):
        self.q["answerability"]["status"] = "absent_fact"
        self.assertEqual(self.score(["a"])["evidence_coverage"], "not_scored")
        self.q["answerability"]["status"] = "false_premise"
        self.assertEqual(self.score(["a", "b"])["evidence_coverage"], "pass")


class AdjacentSpanTests(unittest.TestCase):
    def case(self, text, start, end, chunker=None):
        from main import chunk_text
        q, anchors = fixture()
        q["required_facts"] = [{"id": "f1"}]
        q["evidence_sets"] = [{"id": "only", "anchors": ["a"], "fact_anchors": {"f1": ["a"]}}]
        anchor = {**anchors["a"], "text_start": start, "text_end": end, "excerpt": text[start:end]}
        anchors = {"a": anchor}
        chunker = chunker or chunk_text
        chunks = chunker(text)
        plans = compile_anchor_spans(anchors, {"A.pdf": text}, chunker)
        return q, anchors, chunks, plans

    def test_boundary_inside_number_matches_verified_chunks_in_reverse_retrieval_order(self):
        excerpt = "At six months, adjusted HR was 0.35."
        start = 1000 - excerpt.index("0.35") - 2
        q, anchors, chunks, plans = self.case("x" * start + excerpt + "y" * 1100, start, start + len(excerpt))
        self.assertEqual(score_evidence(chunks, ["A.pdf"] * len(chunks), q, anchors)["evidence_coverage"], "fail")
        result = score_evidence([chunks[1], chunks[0]], ["A.pdf"] * 2, q, anchors, plans)
        self.assertEqual(result["evidence_coverage"], "pass")
        self.assertEqual(result["fact_recall"], 1)
        self.assertEqual(result["anchor_match_groups"]["a"], [[1, 0]])
        self.assertEqual(result["anchor_matches"]["a"], [0, 1])

    def test_missing_wrong_source_changed_or_arbitrary_fragment_cannot_complete_span(self):
        excerpt = "At six months, adjusted HR was 0.35."
        q, anchors, chunks, plans = self.case("x" * 990 + excerpt + "y" * 1100, 990, 990 + len(excerpt))
        for contexts, sources in [([chunks[0]], ["A.pdf"]),
                                  ([chunks[0], chunks[1]], ["A.pdf", "B.pdf"]),
                                  ([chunks[0], chunks[1].replace("0.35", "−0.35")], ["A.pdf"] * 2),
                                  ([chunks[0], chunks[2]], ["A.pdf"] * 2),
                                  ([excerpt[:10], excerpt[10:]], ["A.pdf"] * 2)]:
            with self.subTest(contexts=contexts, sources=sources):
                result = score_evidence(contexts, sources, q, anchors, plans)
                self.assertEqual(result["fact_recall"], 0)
                self.assertEqual(result["anchor_matches"]["a"], [])

    def test_long_span_requires_every_intermediate_chunk(self):
        text = " ".join(f"finding-{i:04d}" for i in range(400))
        q, anchors, chunks, plans = self.case(text, 900, 3100)
        self.assertEqual(plans["a"][0]["chunk_indices"], [0, 1, 2, 3])
        for missing in range(4):
            selected = [chunk for i, chunk in enumerate(chunks[:4]) if i != missing]
            self.assertEqual(score_evidence(selected, ["A.pdf"] * 3, q, anchors, plans)["evidence_coverage"], "fail")
        self.assertEqual(score_evidence(chunks[:4], ["A.pdf"] * 4, q, anchors, plans)["evidence_coverage"], "pass")

    def test_overlapping_paragraph_chunks_and_trimmed_whitespace_boundaries(self):
        from main import chunk_text
        text = " ".join(f"first-{i}" for i in range(95)) + "\n\n" + " ".join(f"second-{i}" for i in range(70))
        start, end = 600, len(text) - 30
        for chunker in [chunk_text, lambda value: [p.strip() for p in value.split("\n\n")]]:
            with self.subTest(chunker=chunker):
                q, anchors, chunks, plans = self.case(text, start, end, chunker)
                self.assertEqual(score_evidence(chunks[::-1], ["A.pdf"] * len(chunks), q, anchors, plans)["evidence_coverage"], "pass")

    def test_one_retrieved_chunk_cannot_satisfy_two_identical_required_positions(self):
        repeated = "".join(f"{i:04d}" for i in range(250))
        text = "x" * 999 + "a" + repeated * 2 + "c" + "y" * 999
        q, anchors, chunks, plans = self.case(text, 999, 3001)
        self.assertEqual(score_evidence([chunks[0], chunks[1], chunks[3]], ["A.pdf"] * 3, q, anchors, plans)["evidence_coverage"], "fail")
        self.assertEqual(score_evidence(chunks, ["A.pdf"] * 4, q, anchors, plans)["evidence_coverage"], "pass")
        self.assertEqual(minimum_evidence_witness(q, anchors, plans, {"A.pdf": chunks}).total(), 4)

    def test_planner_rejects_wrong_offsets_and_gaps_with_missing_source_text(self):
        q, anchors = fixture()
        anchors = {"a": anchors["a"]}
        text = anchors["a"]["excerpt"]
        with self.assertRaisesRegex(ValueError, "offset/excerpt mismatch"):
            compile_anchor_spans(anchors, {"A.pdf": "x" + text}, lambda t: [t])
        with self.assertRaisesRegex(ValueError, "unreachable"):
            compile_anchor_spans(anchors, {"A.pdf": text}, lambda t: [t[:10], t[20:]])
        with self.assertRaisesRegex(ValueError, "not a source substring"):
            compile_anchor_spans(anchors, {"A.pdf": text}, lambda t: ["invented"])

    def test_offline_oracle_uses_production_chunker_and_fails_for_unreachable_gold(self):
        from main import chunk_text
        text = " ".join(f"finding-{i:04d}" for i in range(400))
        q, anchors, _, _ = self.case(text, 900, 3100)
        benchmark = {"queries": [q], "anchors": list(anchors.values())}
        report = verify_reachability(benchmark, {"A.pdf": text}, chunk_text)
        self.assertEqual(report["unlimited_reachable_evidence_queries"], 1)
        self.assertEqual(report["anchors_requiring_adjacent_chunks"], 1)
        self.assertEqual(report["query_feasibility"]["test"], feasibility_from_minimum(4))
        self.assertEqual(report["by_depth"]["n3"]["feasible_queries"], 0)
        self.assertEqual(report["by_depth"]["n3"]["infeasible_ids"], ["test"])
        self.assertEqual(report["by_depth"]["n8"]["feasible_queries"], 1)
        self.assertFalse(report["retrieval_quality_measured"])
        with self.assertRaisesRegex(ValueError, "unreachable"):
            verify_reachability(benchmark, {"A.pdf": text}, lambda t: [t[:1000], t[3000:]])


class DepthFeasibilityTests(unittest.TestCase):
    def test_shared_single_chunk_and_cheapest_complete_alternative(self):
        q, anchors = fixture()
        chunks = {"A.pdf": [anchors["a"]["excerpt"], anchors["b"]["excerpt"]],
                  "B.pdf": [anchors["c"]["excerpt"]]}
        witness = minimum_evidence_witness(q, anchors, {}, chunks)
        self.assertEqual(witness.total(), 1)
        self.assertEqual({source for source, chunk in witness}, {"B.pdf"})
        q["evidence_sets"] = q["evidence_sets"][:1]
        self.assertEqual(minimum_evidence_witness(q, anchors, {}, chunks).total(), 2)
        chunks["A.pdf"] = [anchors["a"]["excerpt"] + " " + anchors["b"]["excerpt"]]
        self.assertEqual(minimum_evidence_witness(q, anchors, {}, chunks).total(), 1)
        self.assertEqual(compile_query_feasibility([q], anchors, {}, chunks)["test"], feasibility_from_minimum(1))

    def test_two_boundary_anchors_share_the_intermediate_production_chunk(self):
        from main import chunk_text
        q, anchors = fixture()
        q["evidence_sets"] = q["evidence_sets"][:1]
        text = ("x" * 990 + anchors["a"]["excerpt"]).ljust(1990, "y") + anchors["b"]["excerpt"] + "z" * 1000
        anchors = {aid: anchors[aid] for aid in ["a", "b"]}
        for anchor in anchors.values():
            anchor["text_start"] = text.index(anchor["excerpt"])
            anchor["text_end"] = anchor["text_start"] + len(anchor["excerpt"])
        plans = compile_anchor_spans(anchors, {"A.pdf": text}, chunk_text)
        self.assertEqual([p["chunk_indices"] for p in plans["a"]], [[0, 1]])
        self.assertEqual([p["chunk_indices"] for p in plans["b"]], [[1, 2]])
        witness = minimum_evidence_witness(q, anchors, plans, {"A.pdf": chunk_text(text)})
        self.assertEqual(witness.total(), 3)

    def test_minimum_optimizes_shared_windows_instead_of_greedy_anchor_sizes(self):
        q, anchors = fixture()
        q["evidence_sets"] = q["evidence_sets"][:1]
        # Pre-certified options: the larger choice for a shares all of b's chunks.
        plans = {"a": [{"chunks": ["short-left", "short-right"]},
                       {"chunks": ["shared-left", "shared-middle", "shared-right"]}],
                 "b": [{"chunks": ["shared-left", "shared-middle", "shared-right"]}]}
        chunks = {"A.pdf": ["short-left", "short-right", "shared-left", "shared-middle", "shared-right"]}
        self.assertEqual(minimum_evidence_witness(q, anchors, plans, chunks).total(), 3)

    def test_source_binding_absent_cases_and_unreachable_alternatives(self):
        q, anchors = fixture()
        chunks = {"D.pdf": [a["excerpt"] for a in anchors.values()]}
        with self.assertRaisesRegex(ValueError, "no complete evidence alternative"):
            minimum_evidence_witness(q, anchors, {}, chunks)
        q["answerability"]["status"] = "absent_fact"
        self.assertIsNone(minimum_evidence_witness(q, anchors, {}, chunks))
        self.assertEqual(compile_query_feasibility([q], anchors, {}, chunks)["test"], feasibility_from_minimum(None))

    def test_summary_retains_infeasible_fact_recall_and_explicit_zero_denominator(self):
        data = run_artifact()
        result = data["results"][0]
        result["evidence_feasibility"] = feasibility_from_minimum(4)
        result["n3"]["metrics"] = {**result["n3"]["metrics"], "evidence_coverage": "fail", "fact_recall": 0.5}
        summary = runner.summarize([result])
        report = summary["n3"]["answerable"]["evidence_coverage"]
        self.assertEqual(report["full_set"], {"pass": 0, "total": 1, "rate": 0})
        self.assertEqual(report["feasible_only"], {"pass": 0, "total": 0, "rate": None})
        self.assertEqual(report["infeasible_ids"], ["test"])
        self.assertEqual(summary["n3"]["answerable"]["macro_fact_recall"], 0.5)
        self.assertEqual(summary["n8"]["evidence_coverage"]["feasible_only"], {"pass": 1, "total": 1, "rate": 1})

    def test_reports_split_false_premise_and_exclude_absent_facts(self):
        answerable = run_artifact()["results"][0]
        correction = deepcopy(answerable)
        correction.update(id="correction", category="false_premise", answerability="false_premise",
                          evidence_feasibility=feasibility_from_minimum(4))
        correction["n3"]["metrics"]["evidence_coverage"] = "fail"
        absent = deepcopy(answerable)
        absent.update(id="absent", category="unanswerable", answerability="absent_fact",
                      evidence_feasibility=feasibility_from_minimum(None))
        for depth in ["n3", "n8"]:
            absent[depth]["metrics"]["evidence_coverage"] = "not_scored"
            absent[depth]["metrics"]["fact_recall"] = None
        summary = runner.summarize([answerable, correction, absent])
        report = summary["n3"]["evidence_coverage"]
        self.assertEqual(report["full_set"]["total"], 2)
        self.assertEqual(report["feasible_only"]["total"], 1)
        self.assertEqual(summary["n3"]["false_premise"]["evidence_coverage"]["infeasible_ids"], ["correction"])
        self.assertEqual(summary["n3"]["absent_fact"]["executed"], 1)
        self.assertEqual(summary["n3"]["absent_fact"]["evidence_coverage"]["full_set"]["total"], 0)


class ReleaseTests(unittest.TestCase):
    def test_category_status_pairing_is_bidirectional_and_gold_rejects_the_reported_gap(self):
        for category in CATEGORIES:
            expected = {"unanswerable": "absent_fact", "false_premise": "false_premise"}.get(category, "answerable")
            for status in ["answerable", "absent_fact", "false_premise", "test-unknown"]:
                with self.subTest(category=category, status=status):
                    if status == expected:
                        validate_answerability(category, status)
                    else:
                        with self.assertRaises(ValueError):
                            validate_answerability(category, status)
        q, anchors = fixture()
        q["category"] = "unanswerable"
        with self.assertRaisesRegex(ValueError, "inconsistent answerability"):
            validate_benchmark({"queries": [q], "anchors": list(anchors.values())})

    def test_checked_in_release_covers_migration_and_exact_source_union(self):
        directory = ROOT / "benchmark/cardiology/v1"
        b = json.loads((directory / "queries.json").read_text())
        validate_benchmark(b)
        queries = {q["id"]: q for q in b["queries"]}
        anchors = {a["id"]: a for a in b["anchors"]}
        conditions = json.loads((directory / "conditions.json").read_text())
        union = {anchors[a]["article_id"] for q in queries.values() for s in q["evidence_sets"] for a in s["anchors"]}
        self.assertEqual(union, set(conditions["conditions"]["C1"]["article_ids"]))
        self.assertEqual(canonical_hash(b), conditions["query_sha256"])
        ledger = json.loads((directory / "migration.json").read_text())
        reviewed = [q for q in ledger["queries"] if q["owner"] == "JUA-109"]
        self.assertEqual(len(reviewed), 34)
        for old in reviewed:
            self.assertTrue(set(old["new_query_ids"]) <= queries.keys())
            if old["action"] == "revise_as_versioned_case":
                self.assertGreater(queries[old["legacy_query_id"]]["revision"], 1)
        for name in ["case_dependencies.json", "case_review.json"]:
            self.assertEqual(json.loads((directory / name).read_text())["query_sha256"], canonical_hash(b))
        all_ids = set(conditions["conditions"]["C2"]["article_ids"])
        for q in queries.values():
            self.assertEqual(set(q["dependencies"]["overlap_review"]), all_ids)
            if q["category"] == "unanswerable":
                self.assertEqual(set(q["answerability"]["search_scope"]["article_ids"]), all_ids)

    def test_schema_rejects_incomplete_synthesis_and_fake_multihop(self):
        q, anchors = fixture()
        q["category"] = "cross_doc_synthesis"
        with self.assertRaises(ValueError):
            validate_benchmark({"queries": [q], "anchors": list(anchors.values())})
        q["category"] = "multi_hop"; q["reasoning"] = "two passages"
        q["evidence_sets"] = q["evidence_sets"][:1]
        anchors["b"]["text_start"] = 0; anchors["b"]["text_end"] = 40
        with self.assertRaises(ValueError):
            validate_benchmark({"queries": [q], "anchors": list(anchors.values())})

    def test_collection_rejects_extra_missing_stale_and_duplicate_chunks(self):
        collection = Mock(name="documents")
        collection.name = "documents"
        collection.get.return_value = {"documents": ["one"], "metadatas": [{"source": "a.pdf"}]}
        self.assertEqual(runner.verify_collection(collection, {"a.pdf": "one"}, lambda t: [t])["chunk_count"], 1)
        for docs in [[], ["stale"], ["one", "one"]]:
            collection.get.return_value = {"documents": docs, "metadatas": [{"source": "a.pdf"}] * len(docs)}
            with self.assertRaises(ValueError):
                runner.verify_collection(collection, {"a.pdf": "one"}, lambda t: [t])
        collection.get.return_value = {"documents": ["one"], "metadatas": [{"source": "a.txt"}]}
        with self.assertRaises(ValueError):
            runner.verify_collection(collection, {"a.pdf": "one"}, lambda t: [t])

    def test_failed_atomic_checkpoint_preserves_previous_file_and_cleans_temporary(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory, "run.json")
            original = '{"run_status": "running", "results": ["test completed depth"]}'
            path.write_text(original)
            with patch.object(runner.os, "replace", side_effect=OSError("test storage failure")):
                with self.assertRaises(OSError):
                    runner.write_checkpoint(path, {"run_status": "complete"})
            self.assertEqual(path.read_text(), original)
            self.assertEqual(list(Path(directory).iterdir()), [path])


def run_artifact():
    q, anchors = fixture()
    metrics = score_evidence([anchors["a"]["excerpt"], anchors["b"]["excerpt"]], ["A.pdf"] * 2, q, anchors)
    tuples = [{"article_id": "A", "pmc_version": 1, "pdf_sha256": "pdf", "text_sha256": "text"}]
    feasibility = feasibility_from_minimum(1)
    return {"config": {"n_values": [3, 8], "use_bm25": False, "use_query_rewriting": False},
            "provenance": {**{k: "fingerprint" for k in ["query_version", "query_sha256", "subset_sha256", "scorer_version", "scorer_sha256", "retrieval_sha256", "selection_sha256", "conditions_sha256"]},
                           "depths": [3, 8], "requested_ids": ["test"], "executed_ids": ["test"], "missing_ids": [],
                           "feasibility_version": FEASIBILITY_VERSION, "feasibility_sha256": canonical_hash({"test": feasibility}),
                           "article_tuples": tuples, "membership_sha256": canonical_hash(tuples)},
            "results": [{"id": "test", "revision": 1, "query_sha256": canonical_hash(q), "question": q["question"],
                         "category": q["category"], "answerability": "answerable", "evidence_feasibility": feasibility,
                         **{n: {"verdict": "pass", "metrics": metrics} for n in ["n3", "n8"]}}]}


class CompatibilityTests(unittest.TestCase):
    def test_missing_inconsistent_or_unbound_feasibility_is_rejected(self):
        for mutation in [lambda d: d["provenance"].pop("feasibility_version"),
                         lambda d: d["provenance"].update(feasibility_sha256="unbound"),
                         lambda d: d["results"][0].pop("evidence_feasibility"),
                         lambda d: d["results"][0].update(evidence_feasibility=None),
                         lambda d: d["results"][0]["evidence_feasibility"].update(minimum_chunks=True),
                         lambda d: d["results"][0]["evidence_feasibility"].update(minimum_chunks=-1),
                         lambda d: d["results"][0]["evidence_feasibility"]["by_depth"].update(n3="infeasible")]:
            data = run_artifact(); mutation(data)
            with self.subTest(data=data), self.assertRaises(ValueError):
                check_compatible(data, deepcopy(data))

    def test_changed_eligibility_is_rejected_even_in_nested_comparisons(self):
        base = run_artifact(); exp = deepcopy(base)
        exp["results"][0]["evidence_feasibility"] = feasibility_from_minimum(4)
        exp["provenance"]["feasibility_sha256"] = canonical_hash({"test": feasibility_from_minimum(4)})
        for nested in [False, True]:
            with self.subTest(nested=nested), self.assertRaisesRegex(ValueError, "evidence_feasibility"):
                check_compatible(base, exp, nested_corpus=nested)

    def test_infeasible_pass_is_invalid_but_partial_fact_recall_is_comparable(self):
        data = run_artifact()
        data["results"][0]["evidence_feasibility"] = feasibility_from_minimum(4)
        data["provenance"]["feasibility_sha256"] = canonical_hash({"test": feasibility_from_minimum(4)})
        with self.assertRaisesRegex(ValueError, "exceeds the depth budget"):
            check_compatible(data, deepcopy(data))
        data["results"][0]["n3"]["metrics"] = {**data["results"][0]["n3"]["metrics"], "evidence_coverage": "fail", "fact_recall": 0.5}
        check_compatible(data, deepcopy(data))

    def test_cli_reports_full_and_feasible_denominators_and_partial_fact_changes(self):
        base = run_artifact()
        base["results"][0]["evidence_feasibility"] = feasibility_from_minimum(4)
        base["provenance"]["feasibility_sha256"] = canonical_hash({"test": feasibility_from_minimum(4)})
        base["results"][0]["n3"]["metrics"] = {**base["results"][0]["n3"]["metrics"], "evidence_coverage": "fail", "fact_recall": 0.5}
        exp = deepcopy(base); exp["results"][0]["n3"]["metrics"]["fact_recall"] = 0.75
        with tempfile.TemporaryDirectory() as directory:
            before, after = Path(directory, "before.json"), Path(directory, "after.json")
            before.write_text(json.dumps(base)); after.write_text(json.dumps(exp))
            output = io.StringIO()
            with patch("sys.argv", ["compare_evals.py", str(before), str(after)]), contextlib.redirect_stdout(output):
                compare_evals.main()
            text = output.getvalue()
            self.assertIn("evidence_coverage (full_set): 0/1 → 0/1", text)
            self.assertIn("evidence_coverage (feasible_only): 0/0 → 0/0", text)
            self.assertIn("evidence ceiling: 0/1; infeasible IDs: ['test']", text)
            self.assertIn("fact_recall: 0.5 → 0.75", text)

    def test_cli_keeps_false_premise_evidence_denominator_separate(self):
        base = run_artifact()
        base["results"][0].update(category="false_premise", answerability="false_premise")
        for depth in ["n3", "n8"]:
            base["results"][0][depth]["verdict"] = "not_scored"
        with tempfile.TemporaryDirectory() as directory:
            before, after = Path(directory, "before.json"), Path(directory, "after.json")
            before.write_text(json.dumps(base)); after.write_text(json.dumps(base))
            output = io.StringIO()
            with patch("sys.argv", ["compare_evals.py", str(before), str(after)]), contextlib.redirect_stdout(output):
                compare_evals.main()
            self.assertIn("false-premise evidence (full_set): 1/1 → 1/1", output.getvalue())
            self.assertIn("false-premise evidence (feasible_only): 1/1 → 1/1", output.getvalue())

    def test_incomplete_run_or_inconsistent_status_cannot_affect_denominators(self):
        for status in ["setup", "running", "incomplete"]:
            data = run_artifact(); data["run_status"] = status
            with self.subTest(status=status), self.assertRaisesRegex(ValueError, "incomplete run"):
                check_compatible(data, deepcopy(data))
        data = run_artifact(); data["results"][0]["category"] = "unanswerable"
        with self.assertRaisesRegex(ValueError, "inconsistent answerability"):
            check_compatible(data, deepcopy(data))

    def test_config_ablation_requires_same_gold_and_corpus(self):
        base = run_artifact(); exp = deepcopy(base); exp["config"]["use_bm25"] = True
        check_compatible(base, exp)
        for field in ["query_sha256", "scorer_version", "scorer_sha256", "retrieval_sha256", "selection_sha256", "membership_sha256"]:
            bad = deepcopy(exp); bad["provenance"][field] = "changed"
            with self.subTest(field=field), self.assertRaises(ValueError):
                check_compatible(base, bad)
        bad = deepcopy(exp); bad["results"][0]["revision"] = 2
        with self.assertRaises(ValueError):check_compatible(base, bad)

    def test_partial_missing_duplicate_and_metricless_runs_are_rejected(self):
        base = run_artifact()
        for mutation in [lambda d: d["results"].clear(),
                         lambda d: d["results"].append(deepcopy(d["results"][0])),
                         lambda d: d["provenance"]["requested_ids"].append("missing"),
                         lambda d: d["provenance"].pop("missing_ids"),
                         lambda d: d["results"][0]["n8"].pop("metrics"),
                         lambda d: d["results"][0].pop("query_sha256")]:
            bad = deepcopy(base); mutation(bad)
            with self.assertRaises(ValueError):check_compatible(base, bad)

    def test_nested_corpus_holds_config_and_common_versions_fixed(self):
        base = run_artifact(); exp = deepcopy(base)
        exp["provenance"]["article_tuples"].append({"article_id": "B", "pmc_version": 1, "pdf_sha256": "b", "text_sha256": "bt"})
        exp["provenance"]["membership_sha256"] = canonical_hash(exp["provenance"]["article_tuples"])
        check_compatible(base, exp, nested_corpus=True)
        with self.assertRaises(ValueError):check_compatible(exp, base, nested_corpus=True)
        exp["config"]["use_bm25"] = True
        with self.assertRaises(ValueError):check_compatible(base, exp, nested_corpus=True)

    def test_historical_pair_is_explicit_and_cannot_mix_with_versioned(self):
        base = run_artifact(); legacy = deepcopy(base); legacy.pop("provenance")
        with self.assertRaises(ValueError):check_compatible(legacy, legacy)
        check_compatible(legacy, legacy, allow_legacy=True)
        with self.assertRaises(ValueError):check_compatible(legacy, base, allow_legacy=True)

    def test_cli_shows_passage_regression_when_document_verdict_is_unchanged(self):
        base = run_artifact(); exp = deepcopy(base)
        exp["results"][0]["n8"]["metrics"]["evidence_coverage"] = "fail"
        with tempfile.TemporaryDirectory() as directory:
            before, after = Path(directory, "before.json"), Path(directory, "after.json")
            before.write_text(json.dumps(base)); after.write_text(json.dumps(exp))
            output = io.StringIO()
            with patch("sys.argv", ["compare_evals.py", str(before), str(after)]), contextlib.redirect_stdout(output):
                compare_evals.main()
            self.assertIn("evidence_coverage: pass → fail", output.getvalue())
            self.assertNotIn("No changes between runs.", output.getvalue())


class RunnerTests(unittest.IsolatedAsyncioTestCase):
    async def test_runner_retains_depth_infeasible_case_and_rejects_over_budget_retrieval(self):
        from main import chunk_text
        with tempfile.TemporaryDirectory() as directory:
            q, anchors = fixture()
            q["evidence_sets"] = q["evidence_sets"][:1]
            text = " ".join(f"finding-{i:04d}" for i in range(400))
            anchors = {aid: anchors[aid] for aid in ["a", "b"]}
            for aid, start, end in [("a", 900, 3100), ("b", 0, 20)]:
                anchors[aid].update(text_start=start, text_end=end, excerpt=text[start:end])
            release = ({"queries": [q], "anchors": list(anchors.values()), "query_version": "test-v1"},
                       {"fingerprint_sha256": "manifest"}, {}, {"membership_sha256": "members"}, [], {"A.pdf": text})
            args = SimpleNamespace(benchmark=Path(directory), corpus_dir=Path(directory), condition="C2", ids="test", output=Path(directory, "run.json"), bm25=False, rewrite=False)
            chunks = chunk_text(text)
            retrieve = AsyncMock(side_effect=lambda *args, **kw: (chunks[:kw["n_results"]], ["A.pdf"] * len(chunks[:kw["n_results"]])))
            with patch.object(runner, "read_release", return_value=release), patch.object(runner, "verify_collection", return_value={}), patch.object(runner, "model_fingerprint", return_value={"sha256": "weights"}), patch.object(runner, "version", return_value="test"), patch.object(runner.subprocess, "run", return_value=SimpleNamespace(stdout="commit\n")), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(await runner.run_benchmark(args, retrieve, Mock()), 0)
                data = json.loads(args.output.read_text())
                result = data["results"][0]
                self.assertEqual(result["evidence_feasibility"], feasibility_from_minimum(4))
                self.assertEqual(result["n3"]["metrics"]["evidence_coverage"], "fail")
                self.assertEqual(result["n3"]["metrics"]["fact_recall"], 0.5)
                self.assertEqual(result["n8"]["metrics"]["evidence_coverage"], "pass")
                self.assertEqual(data["summary"]["n3"]["evidence_coverage"]["feasible_only"]["total"], 0)
                self.assertEqual(data["provenance"]["feasibility_sha256"], canonical_hash({"test": result["evidence_feasibility"]}))
                args.output = Path(directory, "overflow.json")
                retrieve = AsyncMock(return_value=(chunks[:4], ["A.pdf"] * 4))
                self.assertEqual(await runner.run_benchmark(args, retrieve, Mock()), 1)
                self.assertEqual(json.loads(args.output.read_text())["run_status"], "incomplete")

    def release(self):
        q, anchors = fixture()
        return ({"queries": [q], "anchors": list(anchors.values()), "query_version": "test-v1"},
                {"fingerprint_sha256": "manifest"}, {}, {"membership_sha256": "members"}, [],
                {"A.pdf": anchors["a"]["excerpt"].ljust(100) + anchors["b"]["excerpt"],
                 "B.pdf": anchors["c"]["excerpt"]})

    async def test_unreachable_source_span_is_rejected_before_models_or_retrieval(self):
        with tempfile.TemporaryDirectory() as directory:
            args = SimpleNamespace(benchmark=Path(directory), corpus_dir=Path(directory), condition="C2", ids="test", output=Path(directory, "run.json"))
            release = self.release()
            release[-1]["A.pdf"] = "incorrect source text"
            load, retrieve = Mock(), AsyncMock()
            with patch.object(runner, "read_release", return_value=release), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(await runner.run_benchmark(args, retrieve, load), 1)
            load.assert_not_called(); retrieve.assert_not_awaited()
            self.assertFalse(args.output.exists())

    async def test_runner_scores_boundary_span_and_checkpoints_complete_support_groups(self):
        from main import chunk_text
        with tempfile.TemporaryDirectory() as directory:
            args = SimpleNamespace(benchmark=Path(directory), corpus_dir=Path(directory), condition="C2", ids="test", output=Path(directory, "run.json"), bm25=False, rewrite=False)
            q, anchors = fixture()
            q["evidence_sets"] = q["evidence_sets"][:1]
            text = "x" * 990 + anchors["a"]["excerpt"] + "padding " * 60 + anchors["b"]["excerpt"] + "y" * 1000
            for aid in ["a", "b"]:
                anchors[aid]["text_start"] = text.index(anchors[aid]["excerpt"])
                anchors[aid]["text_end"] = anchors[aid]["text_start"] + len(anchors[aid]["excerpt"])
            release = ({"queries": [q], "anchors": list(anchors.values()), "query_version": "test-v1"},
                       {"fingerprint_sha256": "manifest"}, {}, {"membership_sha256": "members"}, [], {"A.pdf": text})
            chunks = chunk_text(text)[:2][::-1]
            retrieve = AsyncMock(return_value=(chunks, ["A.pdf"] * 2))
            with patch.object(runner, "read_release", return_value=release), patch.object(runner, "verify_collection", return_value={}), patch.object(runner, "model_fingerprint", return_value={"sha256": "weights"}), patch.object(runner, "version", return_value="test"), patch.object(runner.subprocess, "run", return_value=SimpleNamespace(stdout="commit\n")), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(await runner.run_benchmark(args, retrieve, Mock()), 0)
            data = json.loads(args.output.read_text())
            self.assertEqual(data["provenance"]["scorer_version"], "pinned-span-coverage-v3")
            self.assertEqual(data["results"][0]["evidence_feasibility"], feasibility_from_minimum(2))
            for depth in ["n3", "n8"]:
                metrics = data["results"][0][depth]["metrics"]
                self.assertEqual(metrics["evidence_coverage"], "pass")
                self.assertEqual(metrics["anchor_match_groups"]["a"], [[1, 0]])

    async def test_requested_id_and_overwrite_guards_precede_models_and_retrieval(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory, "result.json")
            args = SimpleNamespace(benchmark=Path(directory), corpus_dir=Path(directory), condition="C2", ids="test,missing", output=path)
            load, retrieve = Mock(), AsyncMock()
            with patch.object(runner, "read_release", return_value=self.release()), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(await runner.run_benchmark(args, retrieve, load), 1)
                path.write_text("original")
                args.ids = "test"
                self.assertEqual(await runner.run_benchmark(args, retrieve, load), 1)
            load.assert_not_called(); retrieve.assert_not_awaited()
            self.assertEqual(path.read_text(), "original")

    async def test_invalid_parent_and_unwritable_output_fail_before_models_or_calls(self):
        with tempfile.TemporaryDirectory() as directory:
            blocked = Path(directory, "test-parent-file"); blocked.write_text("original")
            args = SimpleNamespace(benchmark=Path(directory), corpus_dir=Path(directory), condition="C2", ids="test", output=blocked / "run.json")
            load, retrieve = Mock(), AsyncMock()
            with patch.object(runner, "read_release", return_value=self.release()), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(await runner.run_benchmark(args, retrieve, load), 1)
                args.output = Path(directory, "denied.json")
                with patch.object(Path, "open", side_effect=PermissionError("test permission denied")):
                    self.assertEqual(await runner.run_benchmark(args, retrieve, load), 1)
            load.assert_not_called(); retrieve.assert_not_awaited()
            self.assertEqual(blocked.read_text(), "original")

    async def test_chroma_collection_error_is_reported_without_retrieval(self):
        import main as production
        with tempfile.TemporaryDirectory() as directory:
            args = SimpleNamespace(benchmark=Path(directory), corpus_dir=Path(directory), condition="C2", ids="test", output=Path(directory, "run.json"))
            collection = Mock(); collection.get.side_effect = InternalError("test collection unavailable")
            retrieve = AsyncMock(); output = io.StringIO()
            with patch.object(runner, "read_release", return_value=self.release()), patch.object(production, "collection", collection), contextlib.redirect_stdout(output):
                self.assertEqual(await runner.run_benchmark(args, retrieve, Mock()), 1)
            retrieve.assert_not_awaited()
            self.assertIn("InternalError: test collection unavailable", output.getvalue())
            self.assertNotIn("Traceback", output.getvalue())

    async def test_later_failure_preserves_completed_depth_in_incomplete_checkpoint(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory, "run.json")
            args = SimpleNamespace(benchmark=Path(directory), corpus_dir=Path(directory), condition="C2", ids="test", output=path, bm25=False, rewrite=True)
            q, anchors = fixture()
            def result_then_failure(*args, **kwargs):
                if kwargs["n_results"] == 3:
                    checkpoint = json.loads(path.read_text())
                    self.assertEqual(checkpoint["run_status"], "running")
                    self.assertTrue(checkpoint["provenance"]["scorer_sha256"])
                    return [anchors["a"]["excerpt"]], ["A.pdf"]
                checkpoint = json.loads(path.read_text())
                self.assertIn("n3", checkpoint["results"][0])
                raise InternalError("test second-depth failure")
            retrieve = AsyncMock(side_effect=result_then_failure)
            with patch.object(runner, "read_release", return_value=self.release()), patch.object(runner, "verify_collection", return_value={}), patch.object(runner, "model_fingerprint", return_value={"sha256": "weights"}), patch.object(runner, "version", return_value="test"), patch.object(runner.subprocess, "run", return_value=SimpleNamespace(stdout="commit\n")), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(await runner.run_benchmark(args, retrieve, Mock()), 1)
            data = json.loads(path.read_text())
            self.assertEqual(data["run_status"], "incomplete")
            self.assertIsNone(data["summary"])
            self.assertEqual(data["provenance"]["executed_ids"], [])
            self.assertEqual(data["provenance"]["missing_ids"], ["test"])
            self.assertEqual(data["results"][0]["n3"]["retrieved_contexts"], [anchors["a"]["excerpt"]])
            self.assertNotIn("n8", data["results"][0])

    async def test_run_passes_only_question_to_production_and_records_immutable_provenance(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory, "result.json")
            args = SimpleNamespace(benchmark=Path(directory), corpus_dir=Path(directory), condition="C2", ids="test", output=path, bm25=True, rewrite=False)
            q, anchors = fixture()
            retrieve = AsyncMock(return_value=([anchors["a"]["excerpt"]], ["A.pdf"]))
            with patch.object(runner, "read_release", return_value=self.release()), patch.object(runner, "verify_collection", return_value={"chunks_sha256": "verified"}), patch.object(runner, "model_fingerprint", return_value={"sha256": "weights"}), patch.object(runner, "version", return_value="test"), patch.object(runner.subprocess, "run", return_value=SimpleNamespace(stdout="commit\n")), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(await runner.run_benchmark(args, retrieve, Mock()), 0)
            retrieve.assert_any_await(q["question"], n_results=3, use_query_rewriting=False, use_bm25=True)
            retrieve.assert_any_await(q["question"], n_results=8, use_query_rewriting=False, use_bm25=True)
            data = json.loads(path.read_text()); prov = data["provenance"]
            self.assertEqual(data["run_status"], "complete")
            self.assertEqual(prov["requested_ids"], prov["executed_ids"])
            self.assertEqual(prov["missing_ids"], [])
            self.assertEqual(data["results"][0]["n8"]["metrics"]["evidence_coverage"], "fail")
            self.assertEqual(data["summary"]["n8"]["answerable"]["answer_judged"], 0)
            self.assertEqual(data["results"][0]["n8"]["retrieved_contexts"], [anchors["a"]["excerpt"]])
