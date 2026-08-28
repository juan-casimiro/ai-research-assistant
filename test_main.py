import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
from anthropic import APITimeoutError
from fastapi import HTTPException
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
        main._load_models()

        init_chat_model.assert_called_once_with(
            main.LLM_MODEL,
            max_tokens=1024,
            temperature=0,
            timeout=main.LLM_TIMEOUT_SECONDS,
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
            timeout=main.REWRITE_TIMEOUT_SECONDS,
        )

    async def test_query_maps_grounded_answer_timeout_to_504(self):
        structured_llm = MagicMock()
        structured_llm.ainvoke = AsyncMock(side_effect=api_timeout())
        base_llm = MagicMock()
        base_llm.with_structured_output.return_value = structured_llm

        with (
            patch.object(main, "_ready", True),
            patch.object(
                main,
                "retrieve",
                AsyncMock(return_value=(["test retrieved context"], ["test-source.pdf"])),
            ),
            patch.object(main, "llm", base_llm),
        ):
            with self.assertRaises(HTTPException) as raised:
                await main.query(main.QueryRequest(question="test question"))

        self.assertEqual(raised.exception.status_code, 504)
        self.assertEqual(raised.exception.detail, "upstream LLM request timed out")

    async def test_query_maps_rewrite_timeout_to_504(self):
        with (
            patch.object(main, "_ready", True),
            patch.object(main, "retrieve", AsyncMock(side_effect=api_timeout())),
        ):
            with self.assertRaises(HTTPException) as raised:
                await main.query(main.QueryRequest(question="test question"))

        self.assertEqual(raised.exception.status_code, 504)


if __name__ == "__main__":
    unittest.main()
