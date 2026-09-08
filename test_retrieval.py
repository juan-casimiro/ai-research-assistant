"""Deterministic retrieval tests: real fusion/BM25, fake model and store I/O."""
import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import main


class FusionTests(unittest.TestCase):
    def test_consensus_promotes_lower_ranked_document_and_deduplicates(self):
        self.assertEqual(main.reciprocal_rank_fusion([
            ["test a", "test shared"], ["test b", "test shared"],
        ]), ["test shared", "test a", "test b"])

    def test_empty_lists_and_single_ranking(self):
        self.assertEqual(main.reciprocal_rank_fusion([[], []]), [])
        self.assertEqual(main.reciprocal_rank_fusion([["test b", "test a"], []]),
                         ["test b", "test a"])


class RetrievalPipelineTests(unittest.IsolatedAsyncioTestCase):
    async def test_optional_retrievers_fuse_variants_and_keep_original_rerank_question(self):
        for bm25 in (False, True):
            for rewrite in (False, True):
                with self.subTest(bm25=bm25, rewrite=rewrite):
                    dense = MagicMock(side_effect=lambda q: (
                        (["test dense", "test shared"], ["dense.pdf", "first.pdf"])
                        if q == "test question" else (["test rewritten"], ["rewritten.pdf"])
                    ))
                    sparse = MagicMock(return_value=(["test shared", "test sparse"],
                                                      ["later.pdf", "sparse.pdf"]))
                    rewriter = AsyncMock(return_value="test expanded question")
                    ranker = MagicMock(side_effect=lambda q, docs: iter([1.0] * len(docs)))
                    with patch.object(main, "_retrieve_candidates", dense), patch.object(
                        main, "_retrieve_bm25_candidates", sparse
                    ), patch.object(main, "bm25_index", object()), patch.object(
                        main, "rewrite_query", rewriter
                    ), patch.object(main, "reranker", SimpleNamespace(rerank=ranker)):
                        docs, sources = await main.retrieve("test question", n_results=10,
                                                           use_bm25=bm25, use_query_rewriting=rewrite)
                    expected = {"test dense": "dense.pdf", "test shared": "first.pdf"}
                    if bm25:
                        expected["test sparse"] = "sparse.pdf"
                    if rewrite:
                        expected["test rewritten"] = "rewritten.pdf"
                    self.assertEqual(dict(zip(docs, sources)), expected)
                    self.assertEqual(len(docs), len(expected))
                    self.assertEqual(dense.call_count, 2 if rewrite else 1)
                    if rewrite:
                        dense.assert_any_call("test expanded question")
                        rewriter.assert_awaited_once_with("test question")
                    else:
                        rewriter.assert_not_awaited()
                    self.assertEqual(sparse.call_count, (2 if rewrite else 1) if bm25 else 0)
                    if bm25:
                        sparse.assert_any_call("test question")
                        if rewrite:
                            sparse.assert_any_call("test expanded question")
                    ranker.assert_called_once_with("test question", docs)
                    if bm25:
                        self.assertEqual(docs[0], "test shared")

    async def test_candidate_pool_is_capped_before_reranking(self):
        docs = [f"test chunk {i}" for i in range(25)]
        sources = [f"test-{i}.pdf" for i in range(25)]
        ranker = MagicMock(side_effect=lambda q, candidates: iter(range(len(candidates))))
        with patch.object(main, "_retrieve_candidates", return_value=(docs, sources)), patch.object(
            main, "reranker", SimpleNamespace(rerank=ranker)
        ):
            result = await main.retrieve("test question", n_results=3)
        ranker.assert_called_once_with("test question", docs[:20])
        self.assertEqual(result, (docs[17:20][::-1], sources[17:20][::-1]))

    async def test_empty_corpus_skips_reranker_even_with_bm25_enabled(self):
        with patch.object(main, "_retrieve_candidates", return_value=([], [])), patch.object(
            main, "bm25_index", None
        ), patch.object(main, "_retrieve_bm25_candidates") as sparse, patch.object(main, "reranker") as ranker:
            self.assertEqual(await main.retrieve("test question", use_bm25=True), ([], []))
        sparse.assert_not_called()
        ranker.rerank.assert_not_called()

    async def test_rewrite_non_text_content_falls_back_to_original(self):
        llm = MagicMock()
        llm.bind.return_value.ainvoke = AsyncMock(return_value=SimpleNamespace(content=[{"text": "some block"}]))
        with patch.object(main, "llm", llm):
            self.assertEqual(await main.rewrite_query("test question"), "test question")


class RetrievalStorageTests(unittest.TestCase):
    def setUp(self):
        for name, value in [("bm25_index", None), ("bm25_documents", []), ("bm25_sources", [])]:
            self.enterContext(patch.object(main, name, value))

    def test_bm25_rebuild_ranks_matching_terms_and_replaces_stale_index(self):
        store = MagicMock()
        store.get.return_value = {"documents": ["aspirin platelet", "insulin glucose", "tumour oncology"],
                                  "metadatas": [{"source": name} for name in ("cardio.pdf", "diabetes.pdf", "onco.pdf")]}
        with patch.object(main, "collection", store):
            main._rebuild_bm25_index()
            self.assertEqual(main._retrieve_bm25_candidates("INSULIN, glucose!", n=1),
                             (["insulin glucose"], ["diabetes.pdf"]))
            store.get.return_value = {"documents": [], "metadatas": []}
            main._rebuild_bm25_index()
            self.assertEqual(main._retrieve_bm25_candidates("insulin"), ([], []))
            self.assertEqual(main.bm25_documents, [])
            self.assertEqual(main.bm25_sources, [])

    def test_dense_lookup_preserves_document_source_alignment_and_limit(self):
        store = MagicMock()
        store.query.return_value = {"documents": [["test b", "test a"]],
                                    "metadatas": [[{"source": "b.pdf"}, {"source": "a.pdf"}]]}
        with patch.object(main, "collection", store), patch.object(main, "embed", return_value=[0.2, 0.8]) as embed:
            self.assertEqual(main._retrieve_candidates("test question", n=2),
                             (["test b", "test a"], ["b.pdf", "a.pdf"]))
        embed.assert_called_once_with("test question")
        store.query.assert_called_once_with(query_embeddings=[[0.2, 0.8]], n_results=2)
