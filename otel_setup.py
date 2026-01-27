"""
OpenTelemetry setup and configuration for metrics, traces, and logs.
"""
import logging
from opentelemetry import metrics, trace
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter

# Resource attributes
resource = Resource.create({
    "service.name": "nvidia-gpu-monitoring",
    "service.version": "1.0.0",
    "service.namespace": "slb-seismic-analysis",
    "deployment.environment": "demo",
    "hardware.type": "nvidia-gpu",
})

def setup_metrics(endpoint: str = "localhost:4317"):
    """Setup OpenTelemetry metrics with OTLP exporter."""
    # Remove http:// prefix if present for gRPC
    endpoint = endpoint.replace("http://", "").replace("https://", "")
    metric_exporter = OTLPMetricExporter(
        endpoint=endpoint,
        insecure=True,
    )
    
    metric_reader = PeriodicExportingMetricReader(
        exporter=metric_exporter,
        export_interval_millis=5000,  # Export every 5 seconds
    )
    
    provider = MeterProvider(
        resource=resource,
        metric_readers=[metric_reader],
    )
    
    metrics.set_meter_provider(provider)
    return provider

def setup_traces(endpoint: str = "localhost:4317"):
    """Setup OpenTelemetry traces with OTLP exporter."""
    # Remove http:// prefix if present for gRPC
    endpoint = endpoint.replace("http://", "").replace("https://", "")
    trace_exporter = OTLPSpanExporter(
        endpoint=endpoint,
        insecure=True,
    )
    
    provider = TracerProvider(resource=resource)
    processor = BatchSpanProcessor(trace_exporter)
    provider.add_span_processor(processor)
    
    trace.set_tracer_provider(provider)
    return provider

def setup_logs(endpoint: str = "localhost:4317"):
    """Setup OpenTelemetry logs with OTLP exporter."""
    # Remove http:// prefix if present for gRPC
    endpoint = endpoint.replace("http://", "").replace("https://", "")
    log_exporter = OTLPLogExporter(
        endpoint=endpoint,
        insecure=True,
    )
    
    provider = LoggerProvider(resource=resource)
    processor = BatchLogRecordProcessor(log_exporter)
    provider.add_log_record_processor(processor)
    
    # Setup logging handler
    handler = LoggingHandler(level=logging.NOTSET, logger_provider=provider)
    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(logging.INFO)
    
    return provider

def initialize_otel(endpoint: str = "localhost:4317"):
    """Initialize all OpenTelemetry components."""
    metrics_provider = setup_metrics(endpoint)
    traces_provider = setup_traces(endpoint)
    logs_provider = setup_logs(endpoint)
    
    return {
        "metrics": metrics_provider,
        "traces": traces_provider,
        "logs": logs_provider,
    }
