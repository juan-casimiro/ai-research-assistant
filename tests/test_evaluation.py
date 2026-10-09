"""Protect evaluation verdicts and denominators without live retrieval or LLM calls."""
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import AsyncMock, Mock, patch

from tools.evaluation import evaluate, scoring
import eval_context_sufficient as sufficiency


class ScoringTests(unittest.TestCase):
    def fixture(self):
        anchors = {"a": {"filename": "some-source.pdf", "excerpt": "Some measured finding."},
                   "b": {"filename": "other-source.pdf", "excerpt": "Another scoped finding."}}
        query = {"category": "cross_doc_synthesis", "answerability": {"status": "answerable"},
                 "required_facts": [{"id": "f1"}, {"id": "f2"}], "related_distractors": [],
                 "evidence_sets": [{"anchors": ["a", "b"], "fact_anchors": {"f1": ["a"], "f2": ["b"]}}]}
        return query, anchors

    def test_document_coverage_and_distractor_order(self):
        query, anchors = self.fixture()
        self.assertEqual(scoring.score_evidence(["Unrelated text"], ["some-source.pdf"], query, anchors)["document_coverage"], "fail")
        query["category"] = "cross_doc_distractor"
        query["required_facts"] = [{"id": "f1"}]
        query["evidence_sets"] = [{"anchors": ["a"], "fact_anchors": {"f1": ["a"]}}]
        query["related_distractors"] = [{"filename": "other-source.pdf"}]
        for sources, expected in [(["some-source.pdf", "other-source.pdf"], "pass"),
                                  (["other-source.pdf", "some-source.pdf"], "fail")]:
            with self.subTest(sources=sources):
                self.assertEqual(scoring.score_evidence(["irrelevant", "irrelevant"], sources, query, anchors)["distractor_ordering"], expected)

    def test_documents_without_evidence_and_partial_facts_are_separate(self):
        query, anchors = self.fixture()
        result = scoring.score_evidence(["Some measured finding.", "Unrelated text"],
                                        ["some-source.pdf", "other-source.pdf"], query, anchors)
        self.assertEqual(result["document_coverage"], "pass")
        self.assertEqual(result["evidence_coverage"], "fail")
        self.assertEqual(result["fact_recall"], 0.5)

    def test_complete_alternative_passes_without_mixing_partial_sets(self):
        query, anchors = self.fixture()
        anchors["c"] = {"filename": "alternative.pdf", "excerpt": "Both scoped findings."}
        query["evidence_sets"].append({"anchors": ["c"], "fact_anchors": {"f1": ["c"], "f2": ["c"]}})
        result = scoring.score_evidence(["Both scoped findings."], ["alternative.pdf"], query, anchors)
        self.assertEqual(result["evidence_coverage"], "pass")
        self.assertEqual(result["fact_recall"], 1.0)

    def test_absent_fact_is_not_scored_and_wrong_source_cannot_support_evidence(self):
        query, anchors = self.fixture()
        result = scoring.score_evidence(["Some measured finding."], ["other-source.pdf"], query, anchors)
        self.assertEqual(result["fact_recall"], 0.0)
        query["answerability"]["status"] = "absent_fact"
        self.assertEqual(scoring.score_evidence([], [], query, anchors)["evidence_coverage"], "not_scored")


class AdjacentSpanTests(unittest.TestCase):
    """Ported from epic 6bfed40:test_benchmark.py; no feasibility oracle required."""
    def case(self, text, start, end, chunker=None):
        from main import chunk_text
        excerpt = "At six months, adjusted HR was 0.35."
        anchors = {"a": {"id": "a", "filename": "A.pdf", "excerpt": excerpt,
                         "text_start": 0, "text_end": len(excerpt)}}
        q = {"category": "direct_lookup", "answerability": {"status": "answerable"},
             "related_distractors": []}
        q["required_facts"] = [{"id": "f1"}]
        q["evidence_sets"] = [{"id": "only", "anchors": ["a"], "fact_anchors": {"f1": ["a"]}}]
        anchor = {**anchors["a"], "text_start": start, "text_end": end, "excerpt": text[start:end]}
        anchors = {"a": anchor}
        chunker = chunker or chunk_text
        chunks = chunker(text)
        plans = scoring.compile_anchor_spans(anchors, {"A.pdf": text}, chunker)
        return q, anchors, chunks, plans

    def test_boundary_inside_number_matches_verified_chunks_in_reverse_retrieval_order(self):
        excerpt = "At six months, adjusted HR was 0.35."
        start = 1000 - excerpt.index("0.35") - 2
        q, anchors, chunks, plans = self.case("x" * start + excerpt + "y" * 1100, start, start + len(excerpt))
        self.assertEqual(scoring.score_evidence(chunks, ["A.pdf"] * len(chunks), q, anchors)["evidence_coverage"], "fail")
        result = scoring.score_evidence([chunks[1], chunks[0]], ["A.pdf"] * 2, q, anchors, plans)
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
                result = scoring.score_evidence(contexts, sources, q, anchors, plans)
                self.assertEqual(result["fact_recall"], 0)
                self.assertEqual(result["anchor_matches"]["a"], [])

    def test_long_span_requires_every_intermediate_chunk(self):
        text = " ".join(f"finding-{i:04d}" for i in range(400))
        q, anchors, chunks, plans = self.case(text, 900, 3100)
        self.assertEqual(plans["a"][0]["chunk_indices"], [0, 1, 2, 3])
        for missing in range(4):
            selected = [chunk for i, chunk in enumerate(chunks[:4]) if i != missing]
            self.assertEqual(scoring.score_evidence(selected, ["A.pdf"] * 3, q, anchors, plans)["evidence_coverage"], "fail")
        self.assertEqual(scoring.score_evidence(chunks[:4], ["A.pdf"] * 4, q, anchors, plans)["evidence_coverage"], "pass")

    def test_overlapping_paragraph_chunks_and_trimmed_whitespace_boundaries(self):
        from main import chunk_text
        text = " ".join(f"first-{i}" for i in range(95)) + "\n\n" + " ".join(f"second-{i}" for i in range(70))
        start, end = 600, len(text) - 30
        for chunker in [chunk_text, lambda value: [p.strip() for p in value.split("\n\n")]]:
            with self.subTest(chunker=chunker):
                q, anchors, chunks, plans = self.case(text, start, end, chunker)
                self.assertEqual(scoring.score_evidence(chunks[::-1], ["A.pdf"] * len(chunks), q, anchors, plans)["evidence_coverage"], "pass")

    def test_one_retrieved_chunk_cannot_satisfy_two_identical_required_positions(self):
        repeated = "".join(f"{i:04d}" for i in range(250))
        text = "x" * 999 + "a" + repeated * 2 + "c" + "y" * 999
        q, anchors, chunks, plans = self.case(text, 999, 3001)
        self.assertEqual(scoring.score_evidence([chunks[0], chunks[1], chunks[3]], ["A.pdf"] * 3, q, anchors, plans)["evidence_coverage"], "fail")
        self.assertEqual(scoring.score_evidence(chunks, ["A.pdf"] * 4, q, anchors, plans)["evidence_coverage"], "pass")

    def test_planner_rejects_wrong_offsets_and_gaps_with_missing_source_text(self):
        excerpt = "At six months, adjusted HR was 0.35."
        anchors = {"a": {"id": "a", "filename": "A.pdf", "excerpt": excerpt,
                         "text_start": 0, "text_end": len(excerpt)}}
        q = {"category": "direct_lookup", "answerability": {"status": "answerable"},
             "related_distractors": []}
        anchors = {"a": anchors["a"]}
        text = anchors["a"]["excerpt"]
        with self.assertRaisesRegex(ValueError, "offset/excerpt mismatch"):
            scoring.compile_anchor_spans(anchors, {"A.pdf": "x" + text}, lambda t: [t])
        with self.assertRaisesRegex(ValueError, "unreachable"):
            scoring.compile_anchor_spans(anchors, {"A.pdf": text}, lambda t: [t[:10], t[20:]])
        with self.assertRaisesRegex(ValueError, "not a source substring"):
            scoring.compile_anchor_spans(anchors, {"A.pdf": text}, lambda t: ["invented"])


class BenchmarkValidationTests(unittest.TestCase):
    def fixture(self):
        return {"queries": [{"id": "q001", "revision": 1, "question": "What was found?",
            "category": "direct_lookup", "answerability": {"status": "answerable"},
            "required_facts": [{"id": "f1"}], "related_distractors": [],
            "evidence_sets": [{"anchors": ["a"], "fact_anchors": {"f1": ["a"]}}]}],
            "anchors": [{"id": "a", "article_id": "A", "filename": "A.pdf",
                         "excerpt": "A finding."}]}

    def test_rejects_duplicate_ids(self):
        import copy
        scoring.validate_benchmark(self.fixture())
        for field, message in [("queries", "duplicate query IDs"),
                               ("anchors", "duplicate anchor IDs")]:
            data = self.fixture()
            data[field].append(copy.deepcopy(data[field][0]))
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, message):
                scoring.validate_benchmark(data)

    def test_rejects_unknown_anchor_and_incomplete_fact_mapping(self):
        for mapping, members, message in [
            ({"f1": ["missing"]}, ["missing"], "unknown evidence anchor"),
            ({}, ["a"], "does not cover each required fact"),
            ({"f2": ["a"]}, ["a"], "does not cover each required fact"),
            ({"f1": []}, ["a"], "does not cover each required fact"),
        ]:
            data = self.fixture()
            data["queries"][0]["evidence_sets"][0] = {"anchors": members, "fact_anchors": mapping}
            with self.subTest(mapping=mapping), self.assertRaisesRegex(ValueError, message):
                scoring.validate_benchmark(data)

    def test_rejects_inconsistent_answerability_and_unscoped_absence(self):
        data = self.fixture()
        data["queries"][0]["answerability"]["status"] = "absent_fact"
        with self.assertRaisesRegex(ValueError, "inconsistent answerability"):
            scoring.validate_benchmark(data)
        query = data["queries"][0]
        query.update(category="unanswerable", required_facts=[], evidence_sets=[])
        with self.assertRaisesRegex(ValueError, "explicit search scope"):
            scoring.validate_benchmark(data)
        query["answerability"]["search_scope"] = "Reviewed the complete article."
        scoring.validate_benchmark(data)


class InputTests(unittest.TestCase):
    def test_combined_dataset_has_valid_unique_cases_and_current_references(self):
        root = Path(__file__).resolve().parents[1]
        data = json.loads((root / "data/queries.json").read_text())
        scoring.validate_benchmark(data)
        self.assertEqual(len(data["queries"]), 158)
        self.assertEqual(len({q["id"] for q in data["queries"]}), 158)
        articles = {a["article_id"]: a for a in json.loads((root / "data/corpus_manifest.json").read_text())["articles"]}
        self.assertEqual(set(data["sources"]), set(articles))
        for anchor in data["anchors"]:
            self.assertEqual(anchor["filename"], articles[anchor["article_id"]]["filename"])
        self.assertEqual([q["id"] for q in data["queries"]], [f"q{i:03d}" for i in range(1, 159)])
        qualified_facts = {
            fact["id"] if fact["id"].startswith(query["id"] + ":")
            else query["id"] + ":" + fact["id"]
            for query in data["queries"] for fact in query["required_facts"]
        }
        for anchor in data["anchors"]:
            for fact_id in anchor.get("fact_ids", []):
                if fact_id.startswith("q") and ":" in fact_id:
                    self.assertIn(fact_id, qualified_facts, anchor["id"])
            if anchor["id"].startswith("outliers-"):
                self.assertFalse(any(f.startswith("epic:") for f in anchor["fact_ids"]))
        topics = [q["topics"][0] for q in data["queries"]]
        self.assertEqual(topics, sorted(topics))

    def test_collection_rejects_extra_and_missing_chunks(self):
        from types import SimpleNamespace
        texts = {"A.pdf": "first|second"}
        def collection(rows):
            return SimpleNamespace(get=lambda **kw: {
                "documents": [text for source, text in rows],
                "metadatas": [{"source": source} for source, text in rows]})
        expected = [("A.pdf", "first"), ("A.pdf", "second")]
        self.assertEqual(evaluate.verify_collection(collection(expected), texts,
                                                   lambda text: text.split("|")), 2)
        cases = {
            "missing": expected[:1],
            "empty": [],
            "extra": expected + [("A.pdf", "third")],
            "extra source": expected + [("B.pdf", "first")],
            "duplicate": expected + expected[:1],
            "changed text": [("A.pdf", "first"), ("A.pdf", "changed")],
            "wrong source": [("A.pdf", "first"), ("B.pdf", "second")],
        }
        for name, rows in cases.items():
            with self.subTest(case=name), self.assertRaisesRegex(ValueError, "collection differs"):
                evaluate.verify_collection(collection(rows), texts, lambda text: text.split("|"))

    def test_missing_inputs_and_check_do_not_load_models(self):
        with tempfile.TemporaryDirectory() as directory:
            with patch("sys.argv", ["evaluate", "--check", "--queries", str(Path(directory) / "missing.json")]), patch("main._load_models_and_index") as load:
                self.assertEqual(__import__("asyncio").run(evaluate.main()), 1)
                load.assert_not_called()

    def test_check_validates_span_reachability_without_loading_models(self):
        import asyncio
        anchor = {"id": "a", "filename": "A.pdf", "excerpt": "finding",
                  "text_start": 0, "text_end": 7}
        benchmark = {"queries": [{}], "anchors": [anchor]}
        with patch.object(evaluate, "read_inputs", return_value=(benchmark, {"articles": [{}]}, {"A.pdf": "finding"})), patch("main._load_models_and_index") as load:
            self.assertEqual(asyncio.run(evaluate.main(["--check"])), 0)
            anchor["text_start"], anchor["text_end"] = 1, 8
            with contextlib.redirect_stdout(io.StringIO()) as output:
                self.assertEqual(asyncio.run(evaluate.main(["--check"])), 1)
            self.assertIn("offset/excerpt mismatch", output.getvalue())
            load.assert_not_called()

    def test_check_reports_missing_required_key(self):
        import asyncio
        with patch.object(evaluate, "read_inputs", side_effect=KeyError("queries")), contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(asyncio.run(evaluate.main(["--check"])), 1)
        self.assertIn("missing required key 'queries'", output.getvalue())

    def test_checkpoint_preserves_prior_file_on_serialization_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "run.json"
            evaluate.write_checkpoint(path, {"results": ["some result"]})
            original = path.read_bytes()
            with self.assertRaises(ValueError):
                evaluate.write_checkpoint(path, {"value": float("nan")})
            self.assertEqual(path.read_bytes(), original)


class EvaluationRunTests(unittest.IsolatedAsyncioTestCase):
    def inputs(self, directory):
        import copy
        import hashlib
        from types import SimpleNamespace
        root = Path(__file__).resolve().parents[1]
        article = copy.deepcopy(json.loads((root / "data/corpus_manifest.json").read_text())["articles"][0])
        pdf_bytes = b"synthetic test PDF bytes"
        text = "Some measured finding."
        pin = {"pmcid": article["pmcid"], "pmc_version": article["pmc_version"],
               "pdf_sha256": hashlib.sha256(pdf_bytes).hexdigest(), "text_sha256": hashlib.sha256(text.encode()).hexdigest()}
        article["metadata_sources"]["pdf"]["sha256"] = pin["pdf_sha256"]
        path = Path(directory)
        pdf = path / article["filename"]
        pdf.write_bytes(pdf_bytes)
        pdf.with_suffix(".txt").write_text(text)
        anchor = {"id": "some-anchor", "article_id": article["id"], "filename": article["filename"],
                  "excerpt": text, "text_start": 0, "text_end": len(text), "excerpt_sha256": pin["text_sha256"],
                  "pmc_version": pin["pmc_version"], "pdf_sha256": pin["pdf_sha256"], "text_sha256": pin["text_sha256"]}
        query = {"id": "some-case", "revision": 1, "category": "direct_lookup", "question": "Some test question?",
                 "answerability": {"status": "answerable"}, "required_facts": [{"id": "f1"}],
                 "related_distractors": [], "evidence_sets": [{"anchors": [anchor["id"]], "fact_anchors": {"f1": [anchor["id"]]}}]}
        (path / "queries.json").write_text(json.dumps({"query_version": "test-v1", "sources": {article["id"]: pin}, "queries": [query], "anchors": [anchor]}))
        (path / "manifest.json").write_text(json.dumps({"articles": [article]}))
        return SimpleNamespace(queries=path / "queries.json", manifest=path / "manifest.json", corpus_dir=path,
                               output=path / "result.json", ids=None, bm25=False, rewrite=False), article, text

    async def test_complete_run_records_both_depths_and_refuses_output_overwrite(self):
        from types import SimpleNamespace
        with tempfile.TemporaryDirectory() as directory:
            args, article, text = self.inputs(directory)
            collection = SimpleNamespace(name="test collection", get=lambda **kw: {"documents": [text], "metadatas": [{"source": article["filename"]}]})
            lookup = AsyncMock(return_value=([text], [article["filename"]]))
            with patch("main.collection", collection), patch("main.CHROMA_PATH", "some-test-store"), patch("main.chunk_text", side_effect=lambda s: [s]):
                loader = Mock()
                self.assertEqual(await evaluate.run_evaluation(args, lookup, loader), 0)
                result = json.loads(args.output.read_text())
                self.assertEqual(result["run_status"], "complete")
                self.assertEqual(result["results"][0]["n3"]["metrics"]["evidence_coverage"], "pass")
                self.assertEqual(result["executed_ids"], ["some-case"])
                original = args.output.read_bytes()
                self.assertEqual(await evaluate.run_evaluation(args, lookup, loader), 1)
                self.assertEqual(args.output.read_bytes(), original)
                self.assertEqual(lookup.await_count, 2)
                self.assertEqual(loader.call_count, 1)

    async def test_provider_failure_retains_incomplete_results(self):
        from types import SimpleNamespace
        from llm_client import LlmTimeoutError
        with tempfile.TemporaryDirectory() as directory:
            args, article, text = self.inputs(directory)
            collection = SimpleNamespace(name="test collection", get=lambda **kw: {"documents": [text], "metadatas": [{"source": article["filename"]}]})
            lookup = AsyncMock(side_effect=[([text], [article["filename"]]), LlmTimeoutError("synthetic timeout")])
            with patch("main.collection", collection), patch("main.CHROMA_PATH", "some-test-store"), patch("main.chunk_text", side_effect=lambda s: [s]):
                self.assertEqual(await evaluate.run_evaluation(args, lookup, lambda: None), 1)
                result = json.loads(args.output.read_text())
                self.assertEqual(result["run_status"], "incomplete")
                self.assertEqual(result["results"][0]["n3"]["metrics"]["evidence_coverage"], "pass")
                self.assertNotIn("n8", result["results"][0])
                self.assertEqual(sorted(set(result["requested_ids"]) - set(result["executed_ids"])), ["some-case"])

    async def test_collection_failure_marks_reserved_output_incomplete(self):
        from types import SimpleNamespace
        with tempfile.TemporaryDirectory() as directory:
            args, article, text = self.inputs(directory)
            collection = SimpleNamespace(name="test collection", get=lambda **kw: {"documents": [], "metadatas": []})
            lookup = AsyncMock()
            with patch("main.collection", collection):
                self.assertEqual(await evaluate.run_evaluation(args, lookup, lambda: None), 1)
            self.assertEqual(json.loads(args.output.read_text())["run_status"], "incomplete")
            lookup.assert_not_awaited()

    async def test_tampered_text_stops_before_loading_or_retrieval(self):
        with tempfile.TemporaryDirectory() as directory:
            args, article, text = self.inputs(directory)
            (Path(directory) / article["filename"]).with_suffix(".txt").write_text("corrupted text")
            lookup = AsyncMock()
            loader = Mock()
            self.assertEqual(await evaluate.run_evaluation(args, lookup, loader), 1)
            loader.assert_not_called()
            lookup.assert_not_awaited()
            self.assertFalse(args.output.exists())


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
