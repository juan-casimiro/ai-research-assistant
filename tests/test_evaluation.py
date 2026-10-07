"""Protect evaluation verdicts and denominators without live retrieval or LLM calls."""
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import AsyncMock, patch

import eval_golden as golden
import eval_context_sufficient as sufficiency


class ScoringTests(unittest.TestCase):
    def test_category_scoring_including_missing_metadata_and_distractor_order(self):
        cases = [
            ("unanswerable", {}, [], "not_scored"),
            ("direct_lookup", {"expected_doc": "a.pdf"}, ["a.pdf"], "pass"),
            ("direct_lookup", {"expected_doc": "a.pdf"}, ["b.pdf"], "fail"),
            ("multi_hop", {"expected_doc": "a.pdf"}, ["a.pdf"], "pass"),
            ("multi_hop", {}, ["a.pdf"], "fail"),
            ("cross_doc_distractor", {"expected_doc": "a.pdf", "distractor_doc": "b.pdf"}, ["a.pdf", "b.pdf"], "pass"),
            ("cross_doc_distractor", {"expected_doc": "a.pdf", "distractor_doc": "b.pdf"}, ["b.pdf", "a.pdf"], "fail"),
            ("cross_doc_distractor", {"expected_doc": "a.pdf", "distractor_doc": "b.pdf"}, ["a.pdf"], "pass"),
            ("cross_doc_distractor", {"expected_doc": "a.pdf"}, ["a.pdf"], "pass"),
            ("cross_doc_distractor", {"expected_doc": "a.pdf"}, ["b.pdf"], "fail"),
            ("cross_doc_distractor", {}, [], "fail"),
            ("cross_doc_synthesis", {"expected_docs": ["a.pdf", "b.pdf"]}, ["b.pdf", "a.pdf"], "pass"),
            ("cross_doc_synthesis", {"expected_docs": ["a.pdf", "b.pdf"]}, ["a.pdf", "a.pdf"], "fail"),
            ("cross_doc_synthesis", {}, [], "fail"),
            ("unknown", {"expected_doc": "a.pdf"}, ["a.pdf"], "fail"),
        ]
        for category, metadata, sources, verdict in cases:
            with self.subTest(category=category, metadata=metadata, sources=sources):
                self.assertEqual(golden.score_query(sources, {"category": category, **metadata}), verdict)

    def test_config_labels_distinguish_all_four_experiments(self):
        for bm25, rewrite, label in [(False, False, "vector-only-baseline"), (True, False, "vector-bm25"),
                                     (False, True, "vector-rewrite"), (True, True, "vector-bm25-rewrite")]:
            with self.subTest(label=label):
                self.assertEqual(golden.build_config_label(bm25, rewrite), label)


class GoldenHarnessTests(unittest.IsolatedAsyncioTestCase):
    async def test_harness_records_both_depths_and_excludes_unanswerable_from_denominator(self):
        with tempfile.TemporaryDirectory() as directory:
            input_path, output_path = Path(directory, "qa.json"), Path(directory, "results.json")
            input_path.write_text(json.dumps({"queries": [
                {"id": "test-a", "category": "direct_lookup", "question": "some question", "expected_doc": "a.pdf"},
                {"id": "test-b", "category": "unanswerable", "question": "some other question"},
            ]}))
            async def retrieve(question, n_results, **options):
                return [], ["a.pdf"] if n_results == 8 else ["b.pdf"]
            output = io.StringIO()
            with patch.object(golden, "GOLDEN_QA_PATH", input_path), patch.object(golden, "RESULTS_PATH", output_path), patch.object(
                golden, "_load_models_and_index"
            ) as load, patch.object(golden, "retrieve", AsyncMock(side_effect=retrieve)) as lookup, patch(
                "sys.argv", ["eval_golden.py", "--bm25", "--rewrite"]
            ), contextlib.redirect_stdout(output):
                self.assertEqual(await golden.main(), 0)
            load.assert_called_once()
            self.assertEqual(lookup.await_count, 4)
            lookup.assert_any_await("some question", n_results=8, use_query_rewriting=True, use_bm25=True)
            result = json.loads(output_path.read_text())
            self.assertEqual(result["config"]["n_values"], [3, 8])
            self.assertEqual(result["config_label"], "vector-bm25-rewrite")
            self.assertEqual(result["results"][0]["n3"]["verdict"], "fail")
            self.assertEqual(result["results"][0]["n8"]["verdict"], "pass")
            self.assertEqual(result["results"][1]["n8"]["verdict"], "not_scored")
            overall = next(line for line in output.getvalue().splitlines() if line.startswith("OVERALL"))
            self.assertIn("0/1", overall)
            self.assertIn("1/1", overall)

    async def test_missing_file_and_unknown_id_do_not_load_models(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory, "qa.json")
            for exists in (False, True):
                with self.subTest(exists=exists):
                    if exists:
                        path.write_text('{"queries": []}')
                    with patch.object(golden, "GOLDEN_QA_PATH", path), patch.object(
                        golden, "_load_models_and_index"
                    ) as load, patch("sys.argv", ["eval_golden.py", "--ids", "test-unknown"]), contextlib.redirect_stdout(io.StringIO()):
                        self.assertEqual(await golden.main(), 1)
                    load.assert_not_called()


class SufficiencyEvaluationTests(unittest.TestCase):
    def test_buckets_exclude_false_premise_and_sample_only_n8_passes_reproducibly(self):
        with tempfile.TemporaryDirectory() as directory:
            qa, baseline = Path(directory, "qa.json"), Path(directory, "baseline.json")
            qa.write_text(json.dumps({"queries": [
                {"id": "q083", "category": "unanswerable", "question": "false premise"},
                {"id": "test-false", "category": "unanswerable", "question": "some absent detail"},
                {"id": "test-other", "category": "direct_lookup", "question": "some known detail"},
            ]}))
            baseline.write_text(json.dumps({"results": [
                {"id": f"test-{i}", "question": f"some question {i}", "n8": {"verdict": "pass"}}
                for i in range(35)
            ] + [{"id": "test-fail", "question": "some missing detail", "n8": {"verdict": "fail"}}]}))
            with patch.object(sufficiency, "GOLDEN_QA_PATH", qa), patch.object(sufficiency, "BASELINE_RESULTS_PATH", baseline):
                self.assertEqual(sufficiency.build_false_bucket(), [
                    {"id": "test-false", "question": "some absent detail", "expected_sufficient": False}])
                first = sufficiency.build_true_bucket()
                self.assertEqual(first, sufficiency.build_true_bucket())
                self.assertEqual(len(first), 29)
                self.assertTrue(all(r["expected_sufficient"] for r in first))
                self.assertNotIn("test-fail", [r["id"] for r in first])

    def test_error_rates_use_separate_denominators_and_id_filter(self):
        false = [{"id": "test-f1", "question": "some false question", "expected_sufficient": False},
                 {"id": "test-f2", "question": "another false question", "expected_sufficient": False}]
        true = [{"id": "test-t1", "question": "some true question", "expected_sufficient": True}]
        for ids, expected_size, fp, fn in [(None, 3, 0.5, 1.0), (" test-f1 ", 1, 1.0, 0.0)]:
            with self.subTest(ids=ids), tempfile.TemporaryDirectory() as directory:
                path = Path(directory, "output.json")
                with patch.object(sufficiency, "build_false_bucket", return_value=false), patch.object(
                    sufficiency, "build_true_bucket", return_value=true
                ), patch.object(sufficiency, "query_service", side_effect=lambda q: q == "some false question"), patch.object(
                    sufficiency, "OUTPUT_PATH", path
                ), contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(sufficiency.main([] if ids is None else ["--ids", ids]), 0)
                result = json.loads(path.read_text())
                self.assertEqual(result["sample_size"], expected_size)
                self.assertEqual(result["false_positive_rate"], fp)
                self.assertEqual(result["false_negative_rate"], fn)

    def test_unknown_id_fails_before_service_call(self):
        with patch.object(sufficiency, "build_false_bucket", return_value=[]), patch.object(
            sufficiency, "build_true_bucket", return_value=[]
        ), patch.object(sufficiency, "query_service") as query, contextlib.redirect_stderr(io.StringIO()), contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaises(SystemExit) as raised:
                sufficiency.main(["--ids", "test-unknown"])
        self.assertEqual(raised.exception.code, 2)
        query.assert_not_called()
