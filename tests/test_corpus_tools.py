"""Offline protection for corpus duplication guards and evaluation comparisons."""
import contextlib
import io
import json
import os
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import compare_evals
from tests.corpus.test_extract_corpus_text import pdf_bytes
from tools.corpus import ingest_corpus


class FakeProduction:
    """Stands in for main.py: ten-character chunks stored in memory."""
    def __init__(self, drop_last_chunk=False):
        self.collection, self.stored, self.drop_last_chunk = self, [], drop_last_chunk

    IngestRequest = staticmethod(lambda text, source: SimpleNamespace(text=text, source=source))
    chunk_text = staticmethod(lambda text: [text[i:i + 10] for i in range(0, len(text), 10)])

    def ingest(self, request):
        chunks = self.chunk_text(request.text)
        self.stored += [(request.source, chunk) for chunk in (chunks[:-1] if self.drop_last_chunk else chunks)]
        return {"chunks_ingested": len(chunks)}

    def get(self, include):
        return {"documents": [chunk for _, chunk in self.stored], "metadatas": [{"source": source} for source, _ in self.stored]}


class CorpusIngestionTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.manifest = self.root / "manifest.json"
        self.manifest.write_text(json.dumps({"articles": [{"filename": "first-test.pdf"}, {"filename": "second-test.pdf"}]}))
        for name in ("first-test.pdf", "second-test.pdf"):
            (self.root / name).write_bytes(pdf_bytes((f"Some text in {name}", "Some more text")))
        self.environment = {"SEED_ON_EMPTY": "false", "CHROMA_PATH": str(self.root / "new-collection")}

    def run_tool(self, rag_production):
        with patch.dict(os.environ, self.environment, clear=True), patch.object(
                ingest_corpus, "load_production", return_value=rag_production) as load, contextlib.redirect_stdout(io.StringIO()):
            return ingest_corpus.main(["--manifest", str(self.manifest), "--corpus-dir", str(self.root)]), load

    def test_unsafe_environment_or_missing_pdf_stops_before_models_load(self):
        for unsafe in ("seed unset", "seed enabled", "path unset", "path exists", "pdf missing"):
            with self.subTest(unsafe=unsafe):
                self.setUp()
                if unsafe == "seed unset":
                    del self.environment["SEED_ON_EMPTY"]
                elif unsafe == "seed enabled":
                    self.environment["SEED_ON_EMPTY"] = "true"
                elif unsafe == "path unset":
                    del self.environment["CHROMA_PATH"]
                elif unsafe == "path exists":
                    Path(self.environment["CHROMA_PATH"]).mkdir()
                else:
                    (self.root / "second-test.pdf").unlink()
                status, load = self.run_tool(FakeProduction())
                self.assertEqual(status, 1)
                load.assert_not_called()

    def test_production_loads_for_ingestion_without_an_llm_client(self):
        import main
        with patch("main.TextEmbedding"), patch("main.TextCrossEncoder"), patch("main.chromadb.PersistentClient") as store, patch(
                "main.create_llm_client") as create_llm_client, patch.multiple(
                main, embed_model=None, reranker=None, chroma_client=None, collection=None, llm=None, _ready=False), \
                contextlib.redirect_stdout(io.StringIO()):
            rag_production = ingest_corpus.load_production()
            self.assertIs(rag_production.collection, store.return_value.get_or_create_collection.return_value)
            self.assertTrue(rag_production._ready)
            self.assertIsNone(rag_production.llm)
        create_llm_client.assert_not_called()

    def test_corpus_folder_defaults_to_the_manifest_corpus_name(self):
        named = self.root / "corpus/test-corpus"
        named.mkdir(parents=True)
        for name in ("first-test.pdf", "second-test.pdf"):
            (self.root / name).rename(named / name)
        for corpus, status in [(None, 1), ("test-corpus", 0)]:
            with self.subTest(corpus=corpus):
                articles = [{"filename": "first-test.pdf"}, {"filename": "second-test.pdf"}]
                self.manifest.write_text(json.dumps({"articles": articles} if corpus is None else {"corpus": corpus, "articles": articles}))
                rag_production = FakeProduction()
                with patch.dict(os.environ, self.environment, clear=True), patch.object(ingest_corpus, "ROOT", self.root), patch.object(
                        ingest_corpus, "load_production", return_value=rag_production), contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(ingest_corpus.main(["--manifest", str(self.manifest)]), status)
                self.assertEqual((named / "first-test.txt").exists(), corpus is not None)

    def test_every_article_is_ingested_by_filename_and_verified(self):
        rag_production = FakeProduction()
        status, _ = self.run_tool(rag_production)
        self.assertEqual(status, 0)
        self.assertEqual({source for source, _ in rag_production.stored}, {"first-test.pdf", "second-test.pdf"})
        self.assertIn("Some text in first-test.pdf", (self.root / "first-test.txt").read_text())

    def test_textless_pdf_or_incomplete_collection_is_reported_as_failure(self):
        self.assertEqual(self.run_tool(FakeProduction(drop_last_chunk=True))[0], 1)
        (self.root / "second-test.pdf").write_bytes(pdf_bytes(("",)))
        rag_production = FakeProduction()
        self.assertEqual(self.run_tool(rag_production)[0], 1)
        self.assertNotIn("second-test.pdf", {source for source, _ in rag_production.stored})


class ComparisonTests(unittest.TestCase):
    def test_comparison_reports_both_flip_directions_and_ignores_unanswerable(self):
        with tempfile.TemporaryDirectory() as directory:
            baseline, experiment = Path(directory, "before.json"), Path(directory, "after.json")
            before = [
                {"id": "test-a", "category": "direct_lookup", "n3": {"verdict": "fail"}, "n8": {"verdict": "pass"}},
                {"id": "test-b", "category": "unanswerable", "n3": {"verdict": "not_scored"}, "n8": {"verdict": "not_scored"}},
            ]
            after = [
                {"id": "test-a", "category": "direct_lookup", "n3": {"verdict": "pass"}, "n8": {"verdict": "fail"}},
                {"id": "test-b", "category": "unanswerable", "n3": {"verdict": "pass"}, "n8": {"verdict": "pass"}},
            ]
            baseline.write_text(json.dumps({"results": before}))
            experiment.write_text(json.dumps({"results": after}))
            for path, changed in [(experiment, True), (baseline, False)]:
                output = io.StringIO()
                with self.subTest(changed=changed), patch("sys.argv", ["compare_evals.py", str(baseline), str(path)]), contextlib.redirect_stdout(output):
                    compare_evals.main()
                text = output.getvalue()
                self.assertNotIn("test-b", text)
                if changed:
                    self.assertIn("n=3: 0/1 → 1/1", text)
                    self.assertIn("n=8: 1/1 → 0/1", text)
                    self.assertIn("IMPROVED  test-a", text)
                    self.assertIn("REGRESSED  test-a", text)
                else:
                    self.assertIn("No changes between runs.", text)
