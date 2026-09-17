"""Deterministic trace propagation and local OTLP contract checks."""
import os
import unittest
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import patch

import grpc
import httpx
from opentelemetry.proto.collector.trace.v1 import trace_service_pb2, trace_service_pb2_grpc
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter
from opentelemetry.trace import SpanKind

import main
from tracing import create_tracer_provider


class PropagationTests(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        cls.span_exporter = InMemorySpanExporter()
        main.tracer_provider.add_span_processor(SimpleSpanProcessor(cls.span_exporter))

    async def test_incoming_context_is_parent_of_production_server_span(self):
        self.span_exporter.clear()
        trace_id = "1234567890abcdef1234567890abcdef"
        parent_id = "1234567890abcdef"
        # Exercise the production app without loading models or contacting an LLM.
        with patch.object(main, "_ready", False), patch.object(main, "_startup_error", None):
            async with httpx.AsyncClient(
                transport=httpx.ASGITransport(app=main.app), base_url="http://test",
            ) as rag_client:
                response = await rag_client.get("/health", headers={
                    "traceparent": f"00-{trace_id}-{parent_id}-01",
                })
        self.assertEqual(response.status_code, 503)
        server_spans = [span for span in self.span_exporter.get_finished_spans()
                        if span.kind == SpanKind.SERVER]
        self.assertEqual(len(server_spans), 1)
        span = server_spans[0]
        self.assertEqual(span.context.trace_id, int(trace_id, 16))
        self.assertEqual(span.parent.span_id, int(parent_id, 16))
        self.assertTrue(span.parent.is_remote)
        self.assertNotEqual(span.context.span_id, int(parent_id, 16))
        self.assertEqual(span.resource.attributes["service.name"], "ai-research-assistant")


class TestCollector(trace_service_pb2_grpc.TraceServiceServicer):
    def __init__(self):
        self.requests = []

    def Export(self, request, context):
        self.requests.append(request)
        return trace_service_pb2.ExportTraceServiceResponse()


class ConfigurationTests(unittest.TestCase):
    def test_default_and_explicit_none_never_construct_network_exporter(self):
        for config in ({}, {"OTEL_TRACES_EXPORTER": "none"}):
            with self.subTest(config=config), patch.dict(os.environ, config, clear=True), patch(
                "tracing.OTLPSpanExporter"
            ) as otlp_exporter:
                provider = create_tracer_provider()
                with provider.get_tracer("test tracing").start_as_current_span("test request"):
                    pass
                provider.shutdown()
                otlp_exporter.assert_not_called()

    def test_invalid_exporter_fails_clearly(self):
        with patch.dict(os.environ, {"OTEL_TRACES_EXPORTER": "test unsupported exporter"}):
            with self.assertRaisesRegex(ValueError, "OTEL_TRACES_EXPORTER"):
                create_tracer_provider()

    def test_configured_otlp_exports_to_environment_endpoint(self):
        collector = TestCollector()
        with ThreadPoolExecutor(max_workers=1) as executor:
            server = grpc.server(executor)
            trace_service_pb2_grpc.add_TraceServiceServicer_to_server(collector, server)
            port = server.add_insecure_port("127.0.0.1:0")
            server.start()
            try:
                with patch.dict(os.environ, {
                    "OTEL_TRACES_EXPORTER": "otlp",
                    "OTEL_EXPORTER_OTLP_TRACES_ENDPOINT": f"http://127.0.0.1:{port}",
                    "OTEL_EXPORTER_OTLP_TRACES_TIMEOUT": "2",
                }, clear=True):
                    provider = create_tracer_provider()
                    try:
                        with provider.get_tracer("test tracing").start_as_current_span("test request"):
                            pass
                        self.assertTrue(provider.force_flush(timeout_millis=5000))
                    finally:
                        provider.shutdown()
                self.assertEqual(len(collector.requests), 1)
                resource_spans = collector.requests[0].resource_spans[0]
                attributes = {item.key: item.value.string_value
                              for item in resource_spans.resource.attributes}
                self.assertEqual(attributes["service.name"], "ai-research-assistant")
                self.assertEqual(resource_spans.scope_spans[0].spans[0].name, "test request")
            finally:
                server.stop(0).wait()
