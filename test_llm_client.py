"""Adapter contracts and actual SDK payloads; all provider traffic stays in memory."""
import asyncio
import json
import os
import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
from anthropic import APITimeoutError
from langchain_ollama import ChatOllama

import llm_client
import main


MESSAGES = [{"role": "user", "content": "test question"}]


class ConfigurationTests(unittest.TestCase):
    def test_default_anthropic_settings_are_preserved(self):
        with patch.dict(os.environ, {"LLM_PROVIDER": "anthropic", "ANTHROPIC_API_KEY": "  test-dummy-key  "}, clear=True), patch(
            "llm_client.init_chat_model"
        ) as constructor:
            adapter = llm_client.create_llm_client()
        self.assertIsInstance(adapter, llm_client.AnthropicAdapter)
        constructor.assert_called_once_with(
            "claude-haiku-4-5-20251001", model_provider="anthropic", api_key="test-dummy-key",
            max_tokens=1024, temperature=0, timeout=35.0, max_retries=0,
        )

    def test_anthropic_requires_nonblank_key_before_constructing_client(self):
        for key in (None, "", "   "):
            environment = {"LLM_PROVIDER": "anthropic"}
            if key is not None:
                environment["ANTHROPIC_API_KEY"] = key
            with self.subTest(key=key), patch.dict(os.environ, environment, clear=True), patch(
                "llm_client.init_chat_model"
            ) as constructor:
                with self.assertRaisesRegex(
                    ValueError, "^ANTHROPIC_API_KEY is required when LLM_PROVIDER=anthropic$"
                ):
                    llm_client.create_llm_client()
                constructor.assert_not_called()

    def test_anthropic_ignores_invalid_ollama_configuration(self):
        with patch.dict(os.environ, {
            "LLM_PROVIDER": "anthropic", "ANTHROPIC_API_KEY": "test-dummy-key",
            "OLLAMA_BASE_URL": "test-invalid-url",
        }, clear=True), patch("llm_client.init_chat_model"):
            self.assertIsInstance(llm_client.create_llm_client(), llm_client.AnthropicAdapter)

    def test_selected_provider_resolves_model_from_mapping(self):
        for provider in ("anthropic", "ollama"):
            with self.subTest(provider=provider), patch.dict(
                os.environ, {"LLM_PROVIDER": provider, "ANTHROPIC_API_KEY": "test-dummy-key"}, clear=True
            ), patch.dict(llm_client.DEFAULT_MODELS_BY_PROVIDER, {provider: "test-mapped-model"}), patch(
                "llm_client.AnthropicAdapter"
            ) as anthropic, patch("llm_client.OllamaAdapter") as ollama:
                llm_client.create_llm_client()
                selected = anthropic if provider == "anthropic" else ollama
                self.assertEqual(selected.call_args.kwargs["model"], "test-mapped-model")
                unused = ollama if provider == "anthropic" else anthropic
                unused.assert_not_called()

    def test_local_configuration_never_constructs_anthropic(self):
        with patch.dict(os.environ, {
            "LLM_PROVIDER": "ollama",
            "OLLAMA_BASE_URL": "http://test-ollama:11434",
        }, clear=True), patch("llm_client.init_chat_model") as anthropic:
            adapter = llm_client.create_llm_client()
        self.assertIsInstance(adapter, llm_client.OllamaAdapter)
        self.assertEqual(adapter._model.model, "smollm2:1.7b-instruct-q4_K_M")
        self.assertEqual(adapter._model.base_url, "http://test-ollama:11434")
        self.assertEqual(adapter._model.num_ctx, 8192)
        self.assertEqual(adapter._model.num_predict, 1024)
        self.assertEqual(adapter._model.client_kwargs["timeout"], 35.0)
        anthropic.assert_not_called()

    def test_local_defaults(self):
        with patch.dict(os.environ, {}, clear=True):
            adapter = llm_client.create_llm_client()
        self.assertEqual(adapter._model.model, "smollm2:1.7b-instruct-q4_K_M")
        self.assertEqual(adapter._model.base_url, "http://localhost:11434")

    def test_invalid_configuration_fails_without_fallback_or_exposing_values(self):
        cases = [
            ({"LLM_PROVIDER": "test-unknown"}, "LLM_PROVIDER"),
            ({"LLM_PROVIDER": ""}, "LLM_PROVIDER"),
        ]
        cases += [({"OLLAMA_BASE_URL": url}, "OLLAMA_BASE_URL") for url in (
            "", "test-host", "ftp://test-host", "http://test-host:bad",
            "http://user:test-secret@test-host", "http://test-host?key=test-secret",
            "http://@test-host", "http://:@test-host",
        )]
        for environment, setting in cases:
            with self.subTest(environment=environment), patch.dict(
                os.environ, {"LLM_PROVIDER": "ollama", **environment}, clear=True
            ), patch("llm_client.init_chat_model") as anthropic, patch(
                "langchain_ollama.ChatOllama"
            ) as ollama:
                with self.assertRaisesRegex(ValueError, setting) as error:
                    llm_client.create_llm_client()
                self.assertNotIn("test-secret", str(error.exception))
                anthropic.assert_not_called()
                ollama.assert_not_called()


class AdapterTests(unittest.IsolatedAsyncioTestCase):
    def adapters(self):
        for provider, constructor in (
            ("anthropic", "llm_client.init_chat_model"),
            ("ollama", "langchain_ollama.ChatOllama"),
        ):
            model = MagicMock()
            model.with_structured_output.return_value.ainvoke = AsyncMock()
            model.bind.return_value.ainvoke = AsyncMock()
            with patch.dict(os.environ, {"LLM_PROVIDER": provider, "ANTHROPIC_API_KEY": "test-dummy-key"}, clear=True), patch(
                constructor, return_value=model
            ):
                yield provider, llm_client.create_llm_client(), model

    async def test_generation_uses_provider_structured_output_and_schema(self):
        for provider, adapter, model in self.adapters():
            with self.subTest(provider=provider):
                answer = main.GroundedAnswer(answer="some answer", context_sufficient=True)
                model.with_structured_output.return_value.ainvoke.return_value = answer
                self.assertIs(await adapter.generate(MESSAGES, main.GroundedAnswer), answer)
                options = {"method": "json_schema"} if provider == "ollama" else {}
                model.with_structured_output.assert_called_once_with(main.GroundedAnswer, **options)

    async def test_rewrite_options_and_non_text_fallback(self):
        for provider, adapter, model in self.adapters():
            with self.subTest(provider=provider):
                operation = model.bind.return_value.ainvoke
                operation.return_value = SimpleNamespace(content="some rewritten query")
                self.assertEqual(await adapter.rewrite(MESSAGES), "some rewritten query")
                options = ({"options": {"num_predict": 100, "num_ctx": 8192, "temperature": 0}}
                           if provider == "ollama" else {"max_tokens": 100, "timeout": 10.0})
                model.bind.assert_called_once_with(**options)
                operation.return_value = SimpleNamespace(content=[{"text": "some block"}])
                self.assertIsNone(await adapter.rewrite(MESSAGES))

    async def test_transport_timeouts_are_normalized_without_retry(self):
        for provider, adapter, model in self.adapters():
            for operation in ("generate", "rewrite"):
                with self.subTest(provider=provider, operation=operation):
                    invocation = (model.with_structured_output.return_value.ainvoke
                                  if operation == "generate" else model.bind.return_value.ainvoke)
                    invocation.side_effect = (
                        APITimeoutError(request=httpx.Request("POST", "https://test.invalid"))
                        if provider == "anthropic" else httpx.ReadTimeout("test timeout")
                    )
                    with self.assertRaises(llm_client.LlmTimeoutError):
                        if operation == "generate":
                            await adapter.generate(MESSAGES, main.GroundedAnswer)
                        else:
                            await adapter.rewrite(MESSAGES)
                    invocation.assert_awaited_once()

    async def test_overall_deadlines_cancel_stalled_operations(self):
        for provider, adapter, model in self.adapters():
            for operation, deadline in (("generate", "LLM_TIMEOUT_SECONDS"),
                                        ("rewrite", "REWRITE_TIMEOUT_SECONDS")):
                with self.subTest(provider=provider, operation=operation):
                    cancelled = asyncio.Event()

                    async def stall(*args):
                        try:
                            await asyncio.Event().wait()
                        finally:
                            cancelled.set()

                    invocation = (model.with_structured_output.return_value.ainvoke
                                  if operation == "generate" else model.bind.return_value.ainvoke)
                    invocation.side_effect = stall
                    with patch.object(llm_client, deadline, 0.01), self.assertRaises(
                        llm_client.LlmTimeoutError
                    ):
                        if operation == "generate":
                            await adapter.generate(MESSAGES, main.GroundedAnswer)
                        else:
                            await adapter.rewrite(MESSAGES)
                    self.assertTrue(cancelled.is_set())
                    invocation.assert_awaited_once()

    async def test_non_timeout_errors_are_not_translated_or_retried(self):
        for provider, adapter, model in self.adapters():
            with self.subTest(provider=provider):
                error = ValueError("test malformed answer")
                invocation = model.with_structured_output.return_value.ainvoke
                invocation.side_effect = error
                with self.assertRaises(ValueError) as raised:
                    await adapter.generate(MESSAGES, main.GroundedAnswer)
                self.assertIs(raised.exception, error)
                invocation.assert_awaited_once()


class WireTests(unittest.IsolatedAsyncioTestCase):
    async def make_adapter(self, provider, handler):
        transport = httpx.MockTransport(handler)
        if provider == "ollama":
            def construct(**kwargs):
                kwargs["client_kwargs"]["transport"] = transport
                return ChatOllama(**kwargs)
            with patch("langchain_ollama.ChatOllama", side_effect=construct):
                return llm_client.OllamaAdapter(model="test-model", base_url="http://test-ollama:11434")
        http_client = await self.enterAsyncContext(httpx.AsyncClient(transport=transport))
        self.enterContext(patch(
            "langchain_anthropic.chat_models._get_default_async_httpx_client",
            return_value=http_client,
        ))
        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-dummy-key"}, clear=True):
            return llm_client.AnthropicAdapter(
                model="claude-haiku-4-5-20251001", api_key="test-dummy-key",
            )

    async def test_sdk_payloads_and_parsed_answers(self):
        for provider in ("ollama", "anthropic"):
            requests = []
            answer = {"answer": "some answer", "context_sufficient": False,
                      "insufficiency_reason": "The requested detail is absent."}

            def respond(request):
                payload = json.loads(request.content)
                requests.append(payload)
                if provider == "ollama":
                    content = json.dumps(answer) if payload.get("format") else "some rewritten query"
                    return httpx.Response(200, json={
                        "model": "test-model", "message": {"role": "assistant", "content": content},
                        "done": True,
                    })
                content = ([{"type": "tool_use", "id": "test-tool-id",
                             "name": "GroundedAnswer", "input": answer}] if payload.get("tools")
                           else [{"type": "text", "text": "some rewritten query"}])
                return httpx.Response(200, json={
                    "id": "test-message", "type": "message", "role": "assistant",
                    "model": "claude-haiku-4-5-20251001", "content": content,
                    "stop_reason": "end_turn", "usage": {"input_tokens": 10, "output_tokens": 10},
                })

            with self.subTest(provider=provider):
                adapter = await self.make_adapter(provider, respond)
                self.assertEqual(await adapter.rewrite(MESSAGES), "some rewritten query")
                result = await adapter.generate(MESSAGES, main.GroundedAnswer)
                self.assertEqual(result.model_dump(), answer)
                self.assertEqual(len(requests), 2)
                if provider == "ollama":
                    self.assertEqual(requests[0]["options"]["num_predict"], 100)
                    self.assertEqual(requests[0]["options"]["num_ctx"], 8192)
                    self.assertEqual(requests[1]["options"]["num_predict"], 1024)
                    self.assertEqual(requests[1]["format"], main.GroundedAnswer.model_json_schema())
                else:
                    self.assertEqual(requests[0]["max_tokens"], 100)
                    self.assertEqual(requests[1]["max_tokens"], 1024)
                    self.assertEqual(requests[1]["tools"][0]["name"], "GroundedAnswer")

    async def test_real_adapter_timeout_reaches_http_contract(self):
        for provider in ("ollama", "anthropic"):
            requests = []

            def timeout(request):
                requests.append(request)
                raise httpx.ReadTimeout("test stalled provider", request=request)

            with self.subTest(provider=provider):
                adapter = await self.make_adapter(provider, timeout)
                with patch.object(main, "llm", adapter), patch.object(main, "_ready", True), patch.object(
                    main, "_startup_error", None
                ), patch.object(main, "retrieve", AsyncMock(return_value=(["some evidence"], ["test.txt"]))):
                    async with httpx.AsyncClient(
                        transport=httpx.ASGITransport(app=main.app), base_url="http://test"
                    ) as rag_client:
                        response = await rag_client.post("/query", json={"question": "test question"})
                self.assertEqual(response.status_code, 504)
                self.assertEqual(response.json(), {"detail": "upstream LLM request timed out"})
                self.assertEqual(len(requests), 1)
