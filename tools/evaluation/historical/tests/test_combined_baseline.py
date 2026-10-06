"""Offline corruption checks for reuse of saved retrieval evidence."""
from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from benchmark_scoring import canonical_hash, compile_anchor_spans, compile_query_feasibility, score_evidence
from main import chunk_text

ROOT = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("combined_baseline", ROOT / "benchmark/combined/derive_baseline.py")
helper = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(helper)


class SavedEvidenceReuseTests(unittest.TestCase):
    def setUp(self):
        temporary = TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.directory = Path(temporary.name)
        self.text = "The synthetic trial had 17 participants at six months."
        self.anchor = {"id": "synthetic-anchor", "article_id": "synthetic-article",
            "filename": "synthetic.pdf", "text_start": 0, "text_end": len(self.text), "excerpt": self.text}
        self.query = {"id": "synthetic-case", "revision": 1, "question": "What was the synthetic count?",
            "category": "direct_lookup", "answerability": {"status": "answerable"},
            "required_facts": [{"id": "count"}], "related_distractors": [],
            "evidence_sets": [{"id": "primary", "anchors": [self.anchor["id"]],
                               "fact_anchors": {"count": [self.anchor["id"]]}}]}
        texts = {"synthetic.pdf": self.text}
        anchors = {self.anchor["id"]: self.anchor}
        plans = compile_anchor_spans(anchors, texts, chunk_text)
        feasibility = compile_query_feasibility([self.query], anchors, plans,
            {source: chunk_text(text) for source, text in texts.items()})
        metrics = score_evidence([self.text], ["synthetic.pdf"], self.query, anchors, plans)
        tuples = [{"article_id": "synthetic-article", "pmc_version": 1,
                   "pdf_sha256": "synthetic-pdf-hash", "text_sha256": "synthetic-text-hash"}]
        scorer = canonical_hash({"scoring": hashlib.sha256((ROOT / "benchmark_scoring.py").read_bytes()).hexdigest(),
                                 "adapter": hashlib.sha256((ROOT / "eval_benchmark.py").read_bytes()).hexdigest()})
        provenance = {"requested_ids": [self.query["id"]], "executed_ids": [self.query["id"]],
            "missing_ids": [], "query_sha256": "synthetic-parent-hash", "article_tuples": deepcopy(tuples),
            "membership_sha256": canonical_hash(tuples), "scorer_sha256": scorer,
            "feasibility_sha256": canonical_hash(feasibility)}
        entry = {"id": self.query["id"], "question": self.query["question"],
            "query_sha256": canonical_hash(self.query), "category": "direct_lookup",
            "answerability": "answerable", "evidence_feasibility": feasibility[self.query["id"]]}
        for depth in [3, 8]:
            entry[f"n{depth}"] = {"retrieved_contexts": [self.text],
                "retrieved_sources": ["synthetic.pdf"], "metrics": deepcopy(metrics), "verdict": "pass"}
        self.parent = {"run_id": "synthetic-original-run", "run_status": "complete",
                       "provenance": provenance, "results": [entry]}
        benchmark = {"queries": [self.query], "anchors": [self.anchor],
            "parent": {"query_sha256": provenance["query_sha256"]},
            "query_version": "synthetic-v1", "selection_sha256": "synthetic-selection"}
        self.release = (benchmark, {}, {}, {"membership_sha256": canonical_hash(tuples)}, tuples, texts)

    def execute(self):
        parent_path = self.directory / "parent.json"
        parent_path.write_text(json.dumps(self.parent))
        output_path = self.directory / "derived.json"
        with patch.object(helper, "read_release", return_value=self.release):
            helper.derive(parent_path, self.directory, self.directory, "C1", output_path)
        return json.loads(output_path.read_text())

    def test_verified_reuse_keeps_parent_and_original_contexts(self):
        result = self.execute()
        self.assertEqual(result["results"], self.parent["results"])
        self.assertEqual(result["derivation"]["parent_provenance"], self.parent["provenance"])
        self.assertEqual(result["derivation"]["retrieval_calls"], 0)
        self.assertNotEqual(result["provenance"]["query_sha256"], self.parent["provenance"]["query_sha256"])

    def test_partial_or_duplicate_coverage_is_rejected(self):
        self.parent["results"].append(deepcopy(self.parent["results"][0]))
        with self.assertRaisesRegex(ValueError, "coverage"):
            self.execute()

    def test_different_document_version_is_rejected(self):
        self.parent["provenance"]["article_tuples"][0]["pmc_version"] = 2
        with self.assertRaisesRegex(ValueError, "corpus differs"):
            self.execute()

    def test_revised_gold_is_rejected(self):
        self.parent["results"][0]["query_sha256"] = "synthetic-revised-gold"
        with self.assertRaisesRegex(ValueError, "changed query/gold"):
            self.execute()

    def test_fabricated_context_is_rejected_even_with_matching_source(self):
        self.parent["results"][0]["n8"]["retrieved_contexts"] = ["A fabricated complete answer."]
        with self.assertRaisesRegex(ValueError, "pinned production chunk"):
            self.execute()

    def test_inflated_saved_metric_is_rejected(self):
        self.parent["results"][0]["n8"]["metrics"]["evidence_coverage"] = "fail"
        with self.assertRaisesRegex(ValueError, "metrics differ"):
            self.execute()

    def test_scorer_change_requires_reviewed_rescoring(self):
        self.parent["provenance"]["scorer_sha256"] = "synthetic-other-scorer"
        with self.assertRaisesRegex(ValueError, "scorer differs"):
            self.execute()


if __name__ == "__main__":
    unittest.main()
