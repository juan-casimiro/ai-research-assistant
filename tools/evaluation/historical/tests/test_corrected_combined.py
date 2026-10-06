"""Offline rejection tests for corrected benchmark evidence and vector reuse."""
from copy import deepcopy
import hashlib
from importlib.metadata import version
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from benchmark_scoring import SCORER_VERSION, FEASIBILITY_VERSION, canonical_hash
from benchmark.combined import verify_corrected_runs as verifier
from benchmark.combined.reuse_store import embedding_hash
from benchmark.combined.build_corrected_release import build
from eval_benchmark import summarize
import test_combined_baseline as fixture_library


class CorrectedRunVerificationTests(unittest.TestCase):
    def setUp(self):
        # Reuse the visibly synthetic source/anchor fixture, without models,
        # local corpus dependencies, or external calls.
        fixture = fixture_library.SavedEvidenceReuseTests()
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        self.directory = fixture.directory
        self.path = self.directory / "synthetic-run.json"
        self.release = deepcopy(fixture.release)
        benchmark, manifest, conditions, member, tuples, texts = self.release
        manifest["fingerprint_sha256"] = benchmark["selection_sha256"]
        data = deepcopy(fixture.parent)
        data["config"] = {"use_bm25": False, "use_query_rewriting": False, "n_values": [3, 8]}
        data["results"][0]["revision"] = 1
        data["summary"] = summarize(data["results"])
        p = data["provenance"]
        p.update(query_version=benchmark["query_version"], query_sha256=canonical_hash(benchmark),
            subset_sha256=canonical_hash(benchmark["queries"]), selection_sha256=benchmark["selection_sha256"],
            conditions_sha256=canonical_hash(conditions), condition="C3", depths=[3, 8],
            scorer_version=SCORER_VERSION, feasibility_version=FEASIBILITY_VERSION,
            dependencies={"chromadb": version("chromadb")}, loaded_models={"synthetic": "weights"},
            rewrite_identity={"provider": "synthetic", "model": "synthetic"})
        p["retrieval_sha256"] = canonical_hash({"source_sha256": hashlib.sha256((verifier.ROOT / "main.py").read_bytes()).hexdigest(),
            "llm_source_sha256": hashlib.sha256((verifier.ROOT / "llm_client.py").read_bytes()).hexdigest(),
            "dependencies": p["dependencies"], "loaded_models": p["loaded_models"], "rewrite_identity": p["rewrite_identity"]})
        receipt = {"status": "complete", "seed_on_empty": False, "membership_sha256": member["membership_sha256"],
            "article_tuples": tuples, "loaded_models": p["loaded_models"],
            "dependencies": p["dependencies"],
            "source_query_probes": {"synthetic.pdf": "synthetic-id"}, "chunk_count": 1,
            "per_source_chunks": {"synthetic.pdf": 1},
            "chunks_sha256": canonical_hash([("synthetic.pdf", fixture.text, 1)])}
        p["ingestion_verification"] = deepcopy(receipt)
        self.data, self.receipt = data, receipt

    def execute(self):
        self.path.write_text(json.dumps(self.data))
        with patch.object(verifier, "read_release", return_value=self.release):
            return verifier.verify_run(self.path, self.directory, self.directory, "C3", self.receipt)

    def test_complete_saved_evidence_verifies(self):
        self.assertEqual(self.execute(), self.data)

    def test_changed_question_is_rejected(self):
        self.data["results"][0]["question"] = "synthetic altered question"
        with self.assertRaisesRegex(ValueError, "query metadata"):
            self.execute()

    def test_fabricated_context_is_rejected(self):
        self.data["results"][0]["n8"]["retrieved_contexts"] = ["fabricated synthetic evidence"]
        with self.assertRaisesRegex(ValueError, "production contexts"):
            self.execute()

    def test_missing_id_is_rejected(self):
        self.data["provenance"]["executed_ids"] = []
        with self.assertRaisesRegex(ValueError, "coverage"):
            self.execute()

    def test_score_improvement_is_rejected(self):
        self.data["results"][0]["n3"]["metrics"]["fact_recall"] = 0.5
        with self.assertRaisesRegex(ValueError, "metrics/verdict"):
            self.execute()

    def test_extra_seed_chunk_is_rejected(self):
        self.receipt["per_source_chunks"]["synthetic-seed.txt"] = 1
        with self.assertRaisesRegex(ValueError, "production chunks"):
            self.execute()

    def test_model_receipt_drift_is_rejected(self):
        self.receipt["loaded_models"] = {"synthetic": "altered weights"}
        with self.assertRaisesRegex(ValueError, "linkage"):
            self.execute()

    def test_truncated_embeddings_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "lengths"):
            embedding_hash({"ids": ["synthetic-id"], "metadatas": [], "documents": ["synthetic"], "embeddings": [[1.0]]})

    def test_embedding_copy_hash_is_order_independent_and_detects_drift(self):
        stored = {"ids": ["synthetic-b", "synthetic-a"], "metadatas": [{"source": "synthetic.pdf"}] * 2,
                  "documents": ["synthetic passage b", "synthetic passage a"], "embeddings": [[1.0, 0.5], [0.5, 1.0]]}
        reordered = {k: deepcopy(list(reversed(v))) for k, v in stored.items()}
        self.assertEqual(embedding_hash(stored), embedding_hash(reordered))
        reordered["embeddings"][0][0] = 0.25
        self.assertNotEqual(embedding_hash(stored), embedding_hash(reordered))


class CorrectedEnvelopeTests(unittest.TestCase):
    def test_shared_manifest_links_and_identical_rebuild(self):
        with TemporaryDirectory() as temporary:
            destination = Path(temporary)
            build(destination)
            first = {str(p.relative_to(destination)): p.read_bytes()
                     for p in destination.rglob("*") if p.is_file()}
            build(destination)
            second = {str(p.relative_to(destination)): p.read_bytes()
                      for p in destination.rglob("*") if p.is_file()}
            self.assertEqual(first, second)
            self.assertEqual((destination / "als-ftd/manifest.json").readlink(), Path("../manifest.json"))

    def test_altered_topic_manifest_is_rejected(self):
        with TemporaryDirectory() as temporary:
            destination = Path(temporary)
            build(destination)
            path = destination / "cardiology/manifest.json"
            altered = json.loads(path.read_text())
            altered["articles"][0]["filename"] = "synthetic-changed-source.pdf"
            path.unlink()
            path.write_text(json.dumps(altered))
            with self.assertRaisesRegex(ValueError, "changed topic manifest"):
                build(destination)
