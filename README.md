# NVIDIA GPU Monitoring Demo with OpenTelemetry

This demo showcases monitoring NVIDIA GPUs, AI analysis jobs, and geo seismic data processing using OpenTelemetry (metrics, traces, and logs) with export to a local Elastic instance.

## Features

- **GPU Monitoring**: Real-time metrics for NVIDIA GPU utilization, memory, temperature, and power
- **AI/Analysis Job Monitoring**: Traces and metrics for seismic analysis jobs
- **Geo Seismic Data Monitoring**: Logs and metrics for data processing pipelines
- **OpenTelemetry Integration**: Full observability with metrics, traces, and logs
- **Elastic Export**: All telemetry data exported to local Elastic instance

## Prerequisites

- Python 3.9+
- NVIDIA GPU with CUDA support
- Docker and Docker Compose (for Elastic stack)
- NVIDIA drivers and CUDA toolkit

## Quick Start

### Automated Setup

Run the setup script to install dependencies and check prerequisites:
```bash
chmod +x setup.sh
./setup.sh
```

### Manual Setup

1. **Start Elastic Stack**:
   ```bash
   docker-compose up -d
   ```
   Wait for Elasticsearch and Kibana to be healthy (check with `docker-compose ps`).

2. **Install Python dependencies**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Start OpenTelemetry Collector**:
   
   **Option A: Use Docker Compose (Recommended)**
   ```bash
   # The collector is already included in docker-compose.yml
   # Just start it with the Elastic stack:
   docker-compose up -d
   ```
   
   **Option B: Run Collector Binary Locally**
   - Install from: https://github.com/open-telemetry/opentelemetry-collector-releases/releases
   - Run: `./run-collector.sh` or `otelcol --config=otel-collector-config.local.yaml`
   
   **Option C: Run Collector in Docker Manually**
   ```bash
   docker run -d --name otel-collector \
     -p 4317:4317 -p 4318:4318 \
     -v $(pwd)/otel-collector-config.local.yaml:/etc/otelcol/config.yaml \
     otel/opentelemetry-collector-contrib:latest \
     --config=/etc/otelcol/config.yaml
   ```

5. **Run the demo application** (in a separate terminal):
   ```bash
   source venv/bin/activate
   python demo.py
   ```

## Architecture

```
┌─────────────┐
│  Demo App   │
│  (Python)   │
└──────┬──────┘
       │
       │ OTLP (gRPC/HTTP)
       │
┌──────▼──────────────┐
│  OTEL Collector     │
│  (otel-collector)   │
└──────┬──────────────┘
       │
       │ Elasticsearch
       │
┌──────▼──────────────┐
│  Elastic Stack      │
│  (Elasticsearch +   │
│   Kibana)           │
└─────────────────────┘
```

## Components

- `gpu_monitor.py`: GPU metrics collection using pynvml
- `job_monitor.py`: AI/analysis job monitoring with traces
- `seismic_monitor.py`: Geo seismic data processing monitoring
- `demo.py`: Main demo application
- `otel-collector-config.yaml`: OpenTelemetry Collector configuration
- `docker-compose.yml`: Elastic stack setup

## Viewing Data

Access Kibana at: http://localhost:5601

### Metrics

1. Navigate to **Stack Management** > **Index Patterns**
2. Create index pattern: `metrics-nvidia-gpu-monitoring-*`
3. View metrics in **Discover** or create custom dashboards

Key metrics to explore:
- `gpu.utilization.percent` - GPU utilization
- `gpu.memory.used.bytes` - GPU memory usage
- `gpu.temperature.celsius` - GPU temperature
- `seismic.job.duration.seconds` - Job execution time
- `seismic.data.ingestion.rate.bytes_per_second` - Data ingestion rate

### Traces

1. Navigate to **Stack Management** > **Index Patterns**
2. Create index pattern: `traces-nvidia-gpu-monitoring-*`
3. View traces in **Discover** or use **APM**

Key traces:
- `seismic.analysis.*` - Analysis job traces
- `seismic.data.ingestion` - Data ingestion traces
- `seismic.data.processing` - Data processing traces

### Logs

1. Navigate to **Stack Management** > **Index Patterns**
2. Create index pattern: `logs-nvidia-gpu-monitoring-*`
3. View logs in **Discover** or **Logs Explorer**

## Monitoring Components

### GPU Monitor (`gpu_monitor.py`)
- Collects real-time GPU metrics using NVIDIA Management Library (NVML)
- Monitors: utilization, memory, temperature, power, clock speeds
- Falls back to mock data if NVIDIA hardware is not available

### Job Monitor (`job_monitor.py`)
- Tracks AI/analysis jobs with distributed tracing
- Monitors: job duration, success/failure rates, data processing
- Supports job types: inference, training, preprocessing

### Seismic Data Monitor (`seismic_monitor.py`)
- Monitors geo seismic data pipelines
- Tracks: ingestion rates, processing latency, data quality, storage
- Provides end-to-end pipeline tracing

## Configuration

### OpenTelemetry Collector

Edit `otel-collector-config.yaml` to:
- Adjust export intervals and batch sizes
- Modify Elasticsearch endpoints
- Add additional processors or exporters
- Configure sampling rates

### Demo Application

The demo runs three concurrent simulations:
- **GPU Monitoring**: Collects metrics every 5 seconds
- **Job Processing**: Creates and processes analysis jobs every 2 seconds
- **Data Pipelines**: Runs seismic data processing every 10 seconds

Adjust timing in `demo.py` if needed.

## Troubleshooting

### OpenTelemetry Collector not receiving data
- Check that the collector is running: `curl http://localhost:4317`
- Verify endpoint in `otel_setup.py` matches collector configuration
- Check collector logs for errors

### Elasticsearch connection issues
- Ensure Elasticsearch is running: `docker-compose ps`
- Check Elasticsearch health: `curl http://localhost:9200/_cluster/health`
- Verify network connectivity between collector and Elasticsearch

### No GPU metrics
- Verify NVIDIA drivers are installed: `nvidia-smi`
- Check that `pynvml` is installed: `pip list | grep pynvml`
- The demo will use mock data if GPU is not available

## Stopping the Demo

1. Press `Ctrl+C` in the demo terminal
2. Stop OpenTelemetry Collector: `Ctrl+C` or `docker stop otel-collector`
3. Stop Elastic stack: `docker-compose down`
