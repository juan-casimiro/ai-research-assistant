import threading
import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
from anthropic import APITimeoutError
from pydantic import ValidationError

import main


def api_timeout() -> APITimeoutError:
    return APITimeoutError(request=httpx.Request("POST", "https://api.anthropic.com"))


class QueryRequestValidationTests(unittest.TestCase):
    def test_question_strips_surrounding_whitespace(self):
        request = main.QueryRequest(question="  test question  ")

        self.assertEqual(request.question, "test question")

    def test_question_accepts_maximum_length(self):
        question = "q" * 1000

        request = main.QueryRequest(question=question)

        self.assertEqual(request.question, question)

    def test_question_rejects_empty_or_whitespace_only_values(self):
        for question in ("", "   "):
            with self.subTest(question=repr(question)):
                with self.assertRaises(ValidationError):
                    main.QueryRequest(question=question)

    def test_question_rejects_value_above_maximum_length(self):
        with self.assertRaises(ValidationError):
            main.QueryRequest(question="q" * 1001)

    def test_n_results_accepts_range_boundaries(self):
        for n_results in (1, main.FUSED_CANDIDATE_POOL):
            with self.subTest(n_results=n_results):
                request = main.QueryRequest(
                    question="test question",
                    n_results=n_results,
                )

                self.assertEqual(request.n_results, n_results)

    def test_n_results_rejects_values_outside_range(self):
        for n_results in (-1, 0, main.FUSED_CANDIDATE_POOL + 1):
            with self.subTest(n_results=n_results):
                with self.assertRaises(ValidationError):
                    main.QueryRequest(
                        question="test question",
                        n_results=n_results,
                    )


class RetrievalTests(unittest.IsolatedAsyncioTestCase):
    async def test_rerank_runs_off_loop_and_preserves_top_n_order(self):
        loop_thread = threading.get_ident()
        execution_threads = []
        chunks = ["test chunk A", "test chunk B", "test chunk C", "test chunk D"]
        sources = ["test-a.pdf", "test-b.pdf", "test-c.pdf", "test-d.pdf"]

        def rerank(question, candidates):
            execution_threads.append(threading.get_ident())

            def scores():
                execution_threads.append(threading.get_ident())
                yield from [0.1, 0.9, 0.9, 0.5]

            return scores()

        reranker_mock = SimpleNamespace(rerank=MagicMock(side_effect=rerank))
        with (
            patch.object(main, "_retrieve_candidates", return_value=(chunks, sources)),
            patch.object(main, "reranker", reranker_mock),
        ):
            result = await main.retrieve("test question", n_results=3)

        self.assertEqual(len(execution_threads), 2)
        self.assertTrue(all(thread != loop_thread for thread in execution_threads))
        reranker_mock.rerank.assert_called_once_with("test question", chunks)
        self.assertEqual(result, (chunks[1:], sources[1:]))


class QueryContractTests(unittest.IsolatedAsyncioTestCase):
    async def test_query_preserves_ranked_context_and_deduplicated_sources(self):
        chunks = ["test chunk A", "test chunk B", "test chunk C", "test chunk D"]
        sources = ["test-a.pdf", "test-b.pdf", "test-b.pdf", "test-d.pdf"]
        structured_llm_mock = MagicMock()
        structured_llm_mock.ainvoke = AsyncMock(return_value=main.GroundedAnswer(
            answer="test answer", context_sufficient=True, insufficiency_reason=None,
        ))
        llm_mock = MagicMock()
        llm_mock.with_structured_output.return_value = structured_llm_mock
        reranker_mock = SimpleNamespace(rerank=MagicMock(return_value=iter([0.1, 0.8, 0.9, 0.7])))

        with (
            patch.object(main, "_ready", True),
            patch.object(main, "_retrieve_candidates", return_value=(chunks, sources)),
            patch.object(main, "reranker", reranker_mock),
            patch.object(main, "llm", llm_mock),
        ):
            async with httpx.AsyncClient(
                transport=httpx.ASGITransport(app=main.app), base_url="http://test",
            ) as client:
                response = await client.post("/query", json={
                    "question": "test question", "n_results": 3,
                })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "answer": "test answer", "sources": ["test-b.pdf", "test-d.pdf"],
            "context_sufficient": True, "insufficiency_reason": None,
        })
        messages = structured_llm_mock.ainvoke.call_args.args[0]
        self.assertEqual([message["role"] for message in messages], ["system", "user"])
        user_prompt = messages[1]["content"]
        self.assertLess(user_prompt.index("test chunk C"), user_prompt.index("test chunk B"))
        self.assertLess(user_prompt.index("test chunk B"), user_prompt.index("test chunk D"))
        self.assertNotIn("test chunk A", user_prompt)
        self.assertIn("test question", user_prompt)
        reranker_mock.rerank.assert_called_once_with("test question", chunks)


class LlmConfigurationTests(unittest.TestCase):
    @patch("main.chromadb.PersistentClient")
    @patch("main.TextCrossEncoder")
    @patch("main.TextEmbedding")
    @patch("main.init_chat_model")
    def test_load_models_bounds_llm_client(
        self,
        init_chat_model,
        _text_embedding,
        _text_cross_encoder,
        _persistent_client,
    ):
        with patch.multiple(main, embed_model=None, reranker=None, chroma_client=None,
                            collection=None, llm=None, CHROMA_PATH="test-store"):
            main._load_models()

        _persistent_client.assert_called_once_with(path="test-store")
        init_chat_model.assert_called_once_with(
            main.LLM_MODEL,
            max_tokens=1024,
            temperature=0,
            timeout=35.0,
            max_retries=0,
        )


class LlmTimeoutTests(unittest.IsolatedAsyncioTestCase):
    async def test_rewrite_uses_its_own_token_and_timeout_bounds(self):
        bound_llm = MagicMock()
        bound_llm.ainvoke = AsyncMock(
            return_value=SimpleNamespace(content="test rewritten query")
        )
        base_llm = MagicMock()
        base_llm.bind.return_value = bound_llm

        with patch.object(main, "llm", base_llm):
            result = await main.rewrite_query("test question")

        self.assertEqual(result, "test rewritten query")
        base_llm.bind.assert_called_once_with(
            max_tokens=100,
            timeout=10.0,
        )

if __name__ == "__main__":
    unittest.main()
