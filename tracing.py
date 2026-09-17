"""Application-owned tracing; OTLP/gRPC export is explicitly opt-in."""
import os

from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


def create_tracer_provider() -> TracerProvider:
    exporter = os.getenv("OTEL_TRACES_EXPORTER", "none").strip().lower()
    if exporter not in {"none", "otlp"}:
        raise ValueError("OTEL_TRACES_EXPORTER must be 'none' or 'otlp'")
    provider = TracerProvider(resource=Resource.create({
        "service.name": "ai-research-assistant",
    }))
    if exporter == "otlp":
        # The SDK reads standard OTEL_EXPORTER_OTLP[_TRACES]_* settings.
        provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))
    return provider
