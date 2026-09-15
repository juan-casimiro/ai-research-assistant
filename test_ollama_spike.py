"""Offline checks for the opt-in local provider; no model server is required."""
import unittest
import json
from unittest.mock import AsyncMock, patch

import httpx

import main


class OllamaConfigurationTests(unittest.TestCase):
    def test_constructs_local_client_without_anthropic_credentials(self):
        with patch.object(main, "LLM_PROVIDER", "ollama"), patch.dict(
            "os.environ", {"OLLAMA_MODEL": "test-model", "OLLAMA_BASE_URL": "http://test-ollama:11434"},
            clear=True,
        ):
            llm = main._create_llm()
        self.assertEqual(llm.model, "test-model")
        self.assertEqual(llm.base_url, "http://test-ollama:11434")
        self.assertEqual(llm.num_ctx, 8192)
        self.assertEqual(llm.num_predict, 1024)
        self.assertEqual(llm.client_kwargs["timeout"], main.LLM_TIMEOUT_SECONDS)

    def test_unknown_provider_fails_instead_of_falling_back_to_paid_api(self):
        with patch.object(main, "LLM_PROVIDER", "test-unknown-provider"):
            with self.assertRaisesRegex(ValueError, "LLM_PROVIDER"):
                main._create_llm()


class OllamaQueryTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.enterContext(patch.object(main, "LLM_PROVIDER", "ollama"))
        self.enterContext(patch.object(main, "_ready", True))
        self.enterContext(patch.object(main, "retrieve", AsyncMock(
            return_value=(["test evidence"], ["test-source.txt"]))))
        self.llm = self.enterContext(patch.object(main, "llm"))
        self.answer = self.llm.with_structured_output.return_value
        self.answer.ainvoke = AsyncMock(return_value=main.GroundedAnswer(
            answer="The detail is not in the evidence.", context_sufficient=False,
            insufficiency_reason="Missing evidence.",
        ))
        self.client = await self.enterAsyncContext(httpx.AsyncClient(
            transport=httpx.ASGITransport(app=main.app), base_url="http://test"))

    async def test_json_schema_preserves_public_response_contract(self):
        response = await self.client.post("/query", json={"question": "test question"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "answer": "The detail is not in the evidence.", "sources": ["test-source.txt"],
            "context_sufficient": False, "insufficiency_reason": "Missing evidence.",
        })
        self.llm.with_structured_output.assert_called_once_with(main.GroundedAnswer, method="json_schema")

    async def test_ollama_transport_timeout_maps_to_504_without_retry(self):
        self.answer.ainvoke.side_effect = httpx.ReadTimeout("test timeout")
        response = await self.client.post("/query", json={"question": "test question"})
        self.assertEqual(response.status_code, 504)
        self.answer.ainvoke.assert_awaited_once()

    async def test_generation_deadline_bounds_a_stalled_response(self):
        import asyncio

        async def stall(*args, **kwargs):
            await asyncio.sleep(60)

        self.answer.ainvoke.side_effect = stall
        with patch.object(main, "LLM_TIMEOUT_SECONDS", 0.01):
            response = await self.client.post("/query", json={"question": "test question"})
        self.assertEqual(response.status_code, 504)

    async def test_rewrite_uses_ollama_output_limit(self):
        bound = self.llm.bind.return_value
        bound.ainvoke = AsyncMock(return_value=type("Answer", (), {"content": "test rewritten question"})())
        self.assertEqual(await main.rewrite_query("test question"), "test rewritten question")
        self.llm.bind.assert_called_once_with(
            options={"num_predict": 100, "num_ctx": 8192, "temperature": 0})


class OllamaWireTests(unittest.IsolatedAsyncioTestCase):
    async def test_real_client_serializes_schema_and_rewrite_options(self):
        from langchain_ollama import ChatOllama

        requests = []

        def respond(request):
            payload = json.loads(request.content)
            requests.append(payload)
            content = (json.dumps({"answer": "test answer", "context_sufficient": True})
                       if payload.get("format") else "test rewritten question")
            return httpx.Response(200, json={
                "model": "test-model", "message": {"role": "assistant", "content": content},
                "done": True,
            })

        llm = ChatOllama(model="test-model", num_predict=1024,
                         client_kwargs={"transport": httpx.MockTransport(respond)})
        with patch.object(main, "LLM_PROVIDER", "ollama"), patch.object(main, "llm", llm):
            self.assertEqual(await main.rewrite_query("test question"), "test rewritten question")
            with patch.object(main, "_ready", True), patch.object(main, "retrieve", AsyncMock(
                return_value=(["test evidence"], ["test-source"])
            )):
                result = await main.query(main.QueryRequest(question="test question"))
        self.assertEqual(result.answer, "test answer")
        self.assertEqual(requests[0]["options"]["num_predict"], 100)
        self.assertEqual(requests[0]["options"]["num_ctx"], 8192)
        self.assertEqual(requests[1]["format"], main.GroundedAnswer.model_json_schema())
        self.assertEqual(requests[1]["options"]["num_predict"], 1024)
