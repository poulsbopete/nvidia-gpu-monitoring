# Architecture Overview

## System Components

### 1. Demo Application (`demo.py`)
The main application that orchestrates all monitoring components:
- **GPU Monitoring Loop**: Collects GPU metrics every 5 seconds
- **Job Simulation**: Creates and processes AI analysis jobs every 2 seconds
- **Data Pipeline Simulation**: Runs seismic data processing every 10 seconds

### 2. GPU Monitor (`gpu_monitor.py`)
Monitors NVIDIA GPU hardware using pynvml:
- **Metrics Collected**:
  - GPU utilization (compute and memory)
  - Memory usage (used, total, free)
  - Temperature
  - Power consumption and limits
  - Clock speeds (graphics and memory)
- **Fallback**: Uses mock data if NVIDIA hardware is not available

### 3. Job Monitor (`job_monitor.py`)
Tracks AI/analysis jobs with distributed tracing:
- **Job Types**:
  - Inference: Model loading, data loading, GPU computation, post-processing
  - Training: Epoch-based training with loss and accuracy tracking
  - Preprocessing: Data normalization, filtering, transformation
- **Metrics**: Job duration, success/failure rates, data processed
- **Traces**: End-to-end job execution with nested spans

### 4. Seismic Data Monitor (`seismic_monitor.py`)
Monitors geo seismic data processing pipelines:
- **Pipeline Stages**:
  - Data ingestion with rate monitoring
  - Chunk processing with quality scoring
  - Data storage with size tracking
- **Metrics**: Ingestion rate, processing latency, data quality, storage size
- **Traces**: Complete pipeline execution with validation, transformation, and analysis spans

### 5. OpenTelemetry Setup (`otel_setup.py`)
Configures OpenTelemetry SDK:
- **Metrics**: Periodic export every 5 seconds
- **Traces**: Batch span processing
- **Logs**: Integrated with Python logging
- **Resource Attributes**: Service identification and metadata

### 6. OpenTelemetry Collector
Receives telemetry data and exports to Elasticsearch:
- **Receivers**: OTLP (gRPC on 4317, HTTP on 4318)
- **Processors**: Memory limiter, resource attributes, batching
- **Exporters**: Elasticsearch (metrics, traces, logs), logging (debug)

### 7. Elastic Stack
Stores and visualizes telemetry data:
- **Elasticsearch**: Indexes metrics, traces, and logs
- **Kibana**: Provides visualization and exploration UI

## Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    Demo Application                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ GPU Monitor  │  │ Job Monitor   │  │ Data Monitor │     │
│  │ (Metrics)    │  │ (Traces)      │  │ (Logs)       │     │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘     │
│         │                  │                  │             │
│         └──────────────────┼──────────────────┘             │
│                            │                                 │
│                    ┌───────▼────────┐                        │
│                    │  OTEL Setup    │                        │
│                    │  (SDK)         │                        │
│                    └───────┬────────┘                        │
└────────────────────────────┼─────────────────────────────────┘
                             │
                             │ OTLP (gRPC/HTTP)
                             │
┌────────────────────────────▼─────────────────────────────────┐
│              OpenTelemetry Collector                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Receivers  │→ │  Processors   │→ │  Exporters   │      │
│  │   (OTLP)     │  │  (Batch, etc) │  │(Elasticsearch)│     │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└────────────────────────────┬─────────────────────────────────┘
                              │
                              │ Elasticsearch API
                              │
┌─────────────────────────────▼─────────────────────────────────┐
│                      Elastic Stack                            │
│  ┌──────────────────┐         ┌──────────────────┐          │
│  │  Elasticsearch   │────────→│     Kibana       │          │
│  │  (Storage)       │         │  (Visualization) │          │
│  └──────────────────┘         └──────────────────┘          │
└──────────────────────────────────────────────────────────────┘
```

## Telemetry Data

### Metrics
- **GPU Metrics**: `gpu.*` namespace
  - `gpu.utilization.percent`
  - `gpu.memory.used.bytes`
  - `gpu.temperature.celsius`
  - `gpu.power.usage.watts`
  - `gpu.clock.*.mhz`

- **Job Metrics**: `seismic.job.*` namespace
  - `seismic.job.duration.seconds`
  - `seismic.job.success.count`
  - `seismic.job.failure.count`
  - `seismic.job.data.processed.bytes`

- **Data Metrics**: `seismic.data.*` namespace
  - `seismic.data.ingestion.rate.bytes_per_second`
  - `seismic.data.processing.latency.seconds`
  - `seismic.data.storage.size.bytes`
  - `seismic.data.quality.score`

### Traces
- **Job Traces**: `seismic.analysis.*`
  - `seismic.analysis.inference`
  - `seismic.analysis.training`
  - `seismic.analysis.preprocessing`

- **Data Traces**: `seismic.data.*`
  - `seismic.data.ingestion`
  - `seismic.data.processing`
  - `seismic.data.pipeline`
  - `seismic.data.storage`

### Logs
- Application logs with structured attributes
- Log levels: INFO, WARNING, ERROR
- Includes context about GPU status, job execution, and data processing

## Elasticsearch Indices

- **Metrics**: `metrics-nvidia-gpu-monitoring-*`
- **Traces**: `traces-nvidia-gpu-monitoring-*`
- **Logs**: `logs-nvidia-gpu-monitoring-*`

## Resource Attributes

All telemetry data includes:
- `service.name`: "nvidia-gpu-monitoring"
- `service.version`: "1.0.0"
- `service.namespace`: "slb-seismic-analysis"
- `deployment.environment`: "demo"
- `hardware.type`: "nvidia-gpu"

## Deployment Options

1. **All-in-One Docker Compose**: Everything runs in containers
2. **Hybrid**: Elastic stack in Docker, collector and app locally
3. **Fully Local**: All components run natively (requires local Elasticsearch)
