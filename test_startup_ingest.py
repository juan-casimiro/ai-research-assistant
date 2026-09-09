"""Startup and ingestion without model downloads or a persistent user store."""
import asyncio
import os
from pathlib import Path
import runpy
import tempfile
import threading
import unittest
from unittest.mock import MagicMock, patch

import httpx
import numpy as np

import main


class ChunkingTests(unittest.TestCase):
    def test_whitespace_and_short_paragraphs(self):
        self.assertEqual(main.chunk_text(" \n\t\n "), [])
        self.assertEqual(main.chunk_text("  first paragraph \n\n second paragraph  "),
                         ["first paragraph\n\nsecond paragraph"])

    def test_long_paragraph_preserves_preceding_and_trailing_text_once(self):
        # ADR-001 records a previous missing-continue bug in this branch.
        self.assertEqual(main.chunk_text("head\n\nabcdefghijk\n\ntail", chunk_size=5, overlap=2),
                         ["head", "abcde", "fghij", "k", "tail"])

    def test_overflow_keeps_previous_tail_as_overlap(self):
        self.assertEqual(main.chunk_text("abcdef\n\nghijkl", chunk_size=10, overlap=2),
                         ["abcdef", "ef\n\nghijkl"])


class StartupTests(unittest.TestCase):
    def setUp(self):
        self.enterContext(patch.object(main, "_ready", False))
        self.enterContext(patch.object(main, "_startup_error", None))
        self.enterContext(patch.object(main, "_log"))
        self.store = self.enterContext(patch.object(main, "collection"))
        self.store.count.return_value = 3

    def test_startup_marks_ready_only_after_loading_seeding_and_index_refresh(self):
        events = []
        def step(name, result=None):
            def run():
                self.assertFalse(main._ready)
                events.append(name)
                return result
            return run
        with patch.object(main, "SEED_ON_EMPTY", True), patch.object(
            main, "_load_models_and_index", side_effect=step("load")
        ), patch.object(main, "_seed_if_empty", side_effect=step("seed", 1)), patch.object(
            main, "_rebuild_bm25_index", side_effect=step("refresh")
        ):
            main._startup()
        self.assertEqual(events, ["load", "seed", "refresh"])
        self.assertTrue(main._ready)
        self.assertIsNone(main._startup_error)

    def test_disabled_seeding_never_touches_seed_path(self):
        with patch.object(main, "SEED_ON_EMPTY", False), patch.object(
            main, "_load_models_and_index"
        ) as load, patch.object(main, "_seed_if_empty") as seed, patch.object(main, "_rebuild_bm25_index") as rebuild:
            main._startup()
        load.assert_called_once()
        seed.assert_not_called()
        rebuild.assert_not_called()
        self.assertTrue(main._ready)

    def test_existing_store_does_not_trigger_second_index_build(self):
        with patch.object(main, "SEED_ON_EMPTY", True), patch.object(
            main, "_load_models_and_index"
        ), patch.object(main, "_seed_if_empty", return_value=0), patch.object(main, "_rebuild_bm25_index") as rebuild:
            main._startup()
        rebuild.assert_not_called()
        self.assertTrue(main._ready)

    def test_failure_in_any_startup_phase_keeps_service_unready(self):
        for failing in ("_load_models_and_index", "_seed_if_empty", "_rebuild_bm25_index"):
            with self.subTest(failing=failing), patch.object(main, "_startup_error", None), patch.object(main, "SEED_ON_EMPTY", True), patch.object(
                main, "_load_models_and_index"
            ), patch.object(main, "_seed_if_empty", return_value=1), patch.object(main, "_rebuild_bm25_index"):
                with patch.object(main, failing, side_effect=RuntimeError("test failure")):
                    main._startup()
                self.assertFalse(main._ready)
                self.assertEqual(main._startup_error, "RuntimeError: test failure")

    def test_evaluation_loader_builds_index_without_demo_seeding(self):
        events = []
        with patch.object(main, "_load_models", side_effect=lambda: events.append("load")), patch.object(
            main, "_rebuild_bm25_index", side_effect=lambda: events.append("index")
        ), patch.object(main, "_seed_if_empty") as seed:
            main._load_models_and_index()
        self.assertEqual(events, ["load", "index"])
        seed.assert_not_called()
        self.assertFalse(main._ready)


class LifespanTests(unittest.IsolatedAsyncioTestCase):
    async def test_health_can_observe_loading_while_loader_runs_off_loop(self):
        started = threading.Event()
        release = threading.Event()
        finished = threading.Event()
        loop_thread = threading.get_ident()
        worker_threads = []
        startup_finished = asyncio.Event()
        loop = asyncio.get_running_loop()
        original_startup = main._startup
        def startup():
            try:
                original_startup()
            finally:
                loop.call_soon_threadsafe(startup_finished.set)
        def load():
            worker_threads.append(threading.get_ident())
            started.set()
            try:
                if not release.wait(3):
                    raise TimeoutError("test did not release loader")
            finally:
                finished.set()
        with patch.object(main, "_startup", side_effect=startup), patch.object(main, "_ready", False), patch.object(main, "_startup_error", None), patch.object(
            main, "_load_models_and_index", side_effect=load
        ), patch.object(main, "SEED_ON_EMPTY", False), patch.object(main, "collection") as store:
            store.count.return_value = 2
            try:
                async with main.lifespan(main.app):
                    self.assertTrue(await asyncio.to_thread(started.wait, 1))
                    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=main.app),
                                                 base_url="http://test") as client:
                        response = await client.get("/health")
                        self.assertEqual(response.status_code, 503)
                        self.assertEqual(response.json(), {"status": "loading"})
                        self.assertNotEqual(worker_threads, [loop_thread])
                        release.set()
                        self.assertTrue(await asyncio.to_thread(finished.wait, 1))
                        await asyncio.wait_for(startup_finished.wait(), 2)
                        response = await client.get("/health")
                        self.assertEqual(response.json(), {"status": "ready", "chunks": 2})
            finally:
                release.set()
                await asyncio.to_thread(finished.wait, 3)
                await asyncio.wait_for(startup_finished.wait(), 2)


class SeedAndIngestTests(unittest.TestCase):
    def setUp(self):
        self.directory = self.enterContext(tempfile.TemporaryDirectory())
        self.enterContext(patch.object(main, "_log"))
        self.store = self.enterContext(patch.object(main, "collection"))
        self.store.count.return_value = 0
        self.enterContext(patch.object(main, "SEED_CORPUS_DIR", Path(self.directory)))
        self.enterContext(patch.object(main, "embed", return_value=[0.2, 0.8]))

    def test_seed_reads_only_nonempty_text_and_does_not_reingest_populated_store(self):
        for name, content in {"test.txt": "some seed text", "empty.txt": " \n", "ATTRIBUTION.md": "some attribution"}.items():
            Path(self.directory, name).write_text(content)
        self.assertEqual(main._seed_if_empty(), 1)
        self.store.add.assert_called_once_with(ids=["test.txt_0"], embeddings=[[0.2, 0.8]],
                                                documents=["some seed text"], metadatas=[{"source": "test.txt"}])
        self.store.count.return_value = 1
        self.assertEqual(main._seed_if_empty(), 0)
        self.assertEqual(self.store.add.call_count, 1)

    def test_ingest_stores_aligned_chunks_then_refreshes_sparse_search(self):
        text = "x" * 1001
        with patch.object(main, "_ready", True), patch.object(main, "_startup_error", None), patch.object(
            main, "_rebuild_bm25_index"
        ) as rebuild:
            order = MagicMock()
            order.attach_mock(self.store.add, "add")
            order.attach_mock(rebuild, "rebuild")
            result = main.ingest(main.IngestRequest(text=text, source="test.txt"))
        self.assertEqual(result, {"chunks_ingested": 2})
        self.store.add.assert_called_once_with(ids=["test.txt_0", "test.txt_1"],
                                                embeddings=[[0.2, 0.8], [0.2, 0.8]],
                                                documents=["x" * 1000, "x"],
                                                metadatas=[{"source": "test.txt"}] * 2)
        self.assertEqual([c[0] for c in order.mock_calls], ["add", "rebuild"])

    def test_failed_store_write_does_not_report_ingestion_or_refresh_index(self):
        self.store.add.side_effect = RuntimeError("test storage failure")
        with patch.object(main, "_ready", True), patch.object(main, "_startup_error", None), patch.object(
            main, "_rebuild_bm25_index"
        ) as rebuild:
            with self.assertRaisesRegex(RuntimeError, "test storage failure"):
                main.ingest(main.IngestRequest(text="some text", source="test.txt"))
        rebuild.assert_not_called()

    def test_embed_returns_plain_vector_from_lazy_model_output(self):
        model = MagicMock()
        model.embed.return_value = iter([np.array([0.25, 0.75])])
        # setUp patches embed for seed/ingest tests; exercise its original implementation here.
        with patch.object(main, "embed_model", model):
            self.assertEqual(self.original_embed("some text"), [0.25, 0.75])
        model.embed.assert_called_once_with(["some text"])

    original_embed = staticmethod(main.embed)


class ImportConfigurationTests(unittest.TestCase):
    def test_import_constructs_no_models_and_environment_overrides_do_not_depend_on_local_dotenv(self):
        for environment, expected in [({}, ("./chroma_db", Path("./seed_corpus"), True)),
            ({"CHROMA_PATH": "test-store", "SEED_CORPUS_DIR": "test-seeds", "SEED_ON_EMPTY": "FaLsE"},
             ("test-store", Path("test-seeds"), False))]:
            with self.subTest(environment=environment), patch.dict(os.environ, environment, clear=True), patch(
                "dotenv.load_dotenv"
            ), patch("fastembed.TextEmbedding") as embedding, patch(
                "fastembed.rerank.cross_encoder.TextCrossEncoder"
            ) as reranker, patch("chromadb.PersistentClient") as store, patch("langchain.chat_models.init_chat_model") as llm:
                module = runpy.run_path(str(Path(main.__file__)))
                self.assertEqual((module["CHROMA_PATH"], module["SEED_CORPUS_DIR"], module["SEED_ON_EMPTY"]), expected)
                self.assertFalse(module["_ready"])
                for constructor in (embedding, reranker, store, llm):
                    constructor.assert_not_called()
