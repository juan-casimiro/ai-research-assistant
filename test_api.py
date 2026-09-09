"""HTTP contracts, with external work replaced at the service boundary."""
import unittest
from unittest.mock import AsyncMock, patch

import httpx
from anthropic import APIConnectionError
from pydantic import ValidationError

import main
from test_main import api_timeout


class ApiTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.enterContext(patch.object(main, "_ready", True))
        self.enterContext(patch.object(main, "_startup_error", None))
        self.retrieve = self.enterContext(patch.object(
            main, "retrieve", AsyncMock(return_value=(["some context"], ["test.pdf"]))
        ))
        self.llm = self.enterContext(patch.object(main, "llm"))
        self.answer = self.llm.with_structured_output.return_value
        self.answer.ainvoke = AsyncMock(return_value=main.GroundedAnswer(
            answer="some answer", context_sufficient=True,
        ))
        self.collection = self.enterContext(patch.object(main, "collection"))
        self.client = await self.enterAsyncContext(httpx.AsyncClient(
            transport=httpx.ASGITransport(app=main.app, raise_app_exceptions=False),
            base_url="http://test",
        ))

    async def test_invalid_query_is_422_before_retrieval(self):
        cases = [({}, "question"), ({"question": None}, "question"),
                 ({"question": []}, "question"), ({"question": " \t\n"}, "question"),
                 ({"question": "q" * 1001}, "question")]
        cases += [({"question": "test question", "n_results": n}, "n_results")
                  for n in (0, -1, 21, None, [], "many", 1.5)]
        cases += [({"question": "test question", flag: "perhaps"}, flag)
                  for flag in ("use_bm25", "use_query_rewriting")]
        for body, field in cases:
            with self.subTest(body=body):
                response = await self.client.post("/query", json=body)
                self.assertEqual(response.status_code, 422)
                self.assertIn(["body", field], [e["loc"] for e in response.json()["detail"]])
        self.retrieve.assert_not_awaited()
        self.llm.with_structured_output.assert_not_called()

    async def test_malformed_json_and_non_object_bodies_are_422(self):
        for body in ('{"question":', '[]', 'null', '"some text"'):
            with self.subTest(body=body):
                response = await self.client.post("/query", content=body,
                                                  headers={"Content-Type": "application/json"})
                self.assertEqual(response.status_code, 422)
        self.retrieve.assert_not_awaited()

    async def test_normalized_question_defaults_and_opt_ins_reach_retrieval(self):
        for options, expected in [({}, (3, False, False)),
                                  ({"n_results": 20, "use_bm25": True,
                                    "use_query_rewriting": True}, (20, True, True))]:
            with self.subTest(options=options):
                response = await self.client.post("/query", json={
                    "question": "  test question \n", **options,
                })
                self.assertEqual(response.status_code, 200)
                self.retrieve.assert_awaited_with(question="test question", n_results=expected[0],
                                                 use_query_rewriting=expected[1], use_bm25=expected[2])

    async def test_insufficient_context_keeps_retrieved_sources_and_reason(self):
        self.answer.ainvoke.return_value = main.GroundedAnswer(
            answer="The requested detail is absent.", context_sufficient=False,
            insufficiency_reason="The context covers another topic.",
        )
        response = await self.client.post("/query", json={"question": "test question"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "answer": "The requested detail is absent.", "sources": ["test.pdf"],
            "context_sufficient": False, "insufficiency_reason": "The context covers another topic.",
        })
        self.llm.with_structured_output.assert_called_once_with(main.GroundedAnswer)
        messages = self.answer.ainvoke.call_args.args[0]
        self.assertEqual([m["role"] for m in messages], ["system", "user"])
        self.assertNotIn("test question", messages[0]["content"])
        self.assertIn("some context", messages[1]["content"])
        self.assertIn("test question", messages[1]["content"])

    async def test_empty_retrieval_preserves_insufficiency_response(self):
        self.retrieve.return_value = ([], [])
        self.answer.ainvoke.return_value = main.GroundedAnswer(
            answer="No context is available.", context_sufficient=False,
        )
        response = await self.client.post("/query", json={"question": "test question"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"answer": "No context is available.", "sources": [],
                                          "context_sufficient": False, "insufficiency_reason": None})

    async def test_grounded_timeout_is_504_without_retry(self):
        self.answer.ainvoke.side_effect = api_timeout()
        response = await self.client.post("/query", json={"question": "test question"})
        self.assertEqual(response.status_code, 504)
        self.assertEqual(response.json(), {"detail": "upstream LLM request timed out"})
        self.answer.ainvoke.assert_awaited_once()

    async def test_real_rewrite_path_timeout_stops_before_answer_generation(self):
        # Exercise retrieve -> rewrite_query -> bound LLM, not a timeout-shaped retrieval mock.
        with patch.object(main, "retrieve", self.original_retrieve), patch.object(
            main, "_retrieve_candidates", return_value=(["some context"], ["test.pdf"])
        ), patch.object(main, "reranker") as reranker:
            bound = self.llm.bind.return_value
            bound.ainvoke = AsyncMock(side_effect=api_timeout())
            response = await self.client.post("/query", json={
                "question": "test question", "use_query_rewriting": True,
            })
        self.assertEqual(response.status_code, 504)
        self.assertEqual(response.json(), {"detail": "upstream LLM request timed out"})
        bound.ainvoke.assert_awaited_once()
        self.answer.ainvoke.assert_not_awaited()
        reranker.rerank.assert_not_called()

    original_retrieve = staticmethod(main.retrieve)

    async def test_non_timeout_failures_remain_500_without_false_success_or_retry(self):
        with self.assertRaises(ValidationError) as invalid:
            main.GroundedAnswer.model_validate({"answer": "some truncated answer"})
        errors = [APIConnectionError(request=httpx.Request("POST", "https://test.invalid")),
                  invalid.exception]
        for error in errors:
            with self.subTest(error=type(error).__name__):
                self.answer.ainvoke.reset_mock()
                self.answer.ainvoke.side_effect = error
                response = await self.client.post("/query", json={"question": "test question"})
                self.assertEqual(response.status_code, 500)
                self.assertEqual(response.text, "Internal Server Error")
                self.answer.ainvoke.assert_awaited_once()

    async def test_health_and_endpoints_report_loading_and_startup_error(self):
        for ready, error, health, detail in [
            (False, None, {"status": "loading"}, "models still loading"),
            (False, "RuntimeError: test failure", {"status": "error", "detail": "RuntimeError: test failure"},
             "startup failed: RuntimeError: test failure"),
            (True, "RuntimeError: test failure", {"status": "error", "detail": "RuntimeError: test failure"},
             "startup failed: RuntimeError: test failure"),
        ]:
            with self.subTest(ready=ready, error=error), patch.object(main, "_ready", ready), patch.object(main, "_startup_error", error):
                response = await self.client.get("/health")
                self.assertEqual(response.status_code, 503)
                self.assertEqual(response.json(), health)
                for path, body in [("/query", {"question": "test question"}),
                                   ("/ingest", {"text": "some text", "source": "test.txt"})]:
                    response = await self.client.post(path, json=body)
                    self.assertEqual(response.status_code, 503)
                    self.assertEqual(response.json(), {"detail": detail})
        self.retrieve.assert_not_awaited()
        self.collection.add.assert_not_called()
        self.llm.with_structured_output.assert_not_called()

    async def test_ready_health_reports_collection_count_without_llm_probe(self):
        self.collection.count.return_value = 7
        response = await self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ready", "chunks": 7})
        self.assertEqual(self.llm.mock_calls, [])

    async def test_ingest_http_success_reports_stored_chunk_count(self):
        with patch.object(main, "embed", return_value=[0.2, 0.8]), patch.object(main, "_rebuild_bm25_index"):
            response = await self.client.post("/ingest", json={"text": "some text", "source": "test.txt"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"chunks_ingested": 1})
        self.collection.add.assert_called_once_with(
            ids=["test.txt_0"], documents=["some text"], embeddings=[[0.2, 0.8]],
            metadatas=[{"source": "test.txt"}],
        )

    async def test_ingest_rejects_missing_or_wrong_typed_fields(self):
        for body in ({}, {"text": "some text"}, {"source": "test.txt"},
                     {"text": [], "source": "test.txt"}, {"text": "some text", "source": None}):
            with self.subTest(body=body):
                response = await self.client.post("/ingest", json=body)
                self.assertEqual(response.status_code, 422)
        self.collection.add.assert_not_called()
