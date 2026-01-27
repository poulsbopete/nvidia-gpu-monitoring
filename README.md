# NVIDIA GPU Monitoring Demo with OpenTelemetry

This demo showcases monitoring NVIDIA GPUs, AI analysis jobs, and geo seismic data processing using OpenTelemetry (metrics, traces, and logs) with export to a local Elastic instance.

## Features

- **GPU Monitoring**: Real-time metrics for NVIDIA GPU utilization, memory, temperature, and power
  - Automatically falls back to mock data if NVIDIA hardware is not available
  - Mock mode can be forced with `--mock-gpu` flag for testing
  - See [MOCK_MODE.md](MOCK_MODE.md) for detailed mock mode documentation
- **AI/Analysis Job Monitoring**: Traces and metrics for seismic analysis jobs
- **Geo Seismic Data Monitoring**: Logs and metrics for data processing pipelines
- **OpenTelemetry Integration**: Full observability with metrics, traces, and logs
- **Elastic Export**: All telemetry data exported to local Elastic instance

## Prerequisites

- Python 3.9+
- Docker and Docker Compose (for Elastic stack)
- **Optional**: NVIDIA GPU with CUDA support
  - **No GPU? No problem!** The demo automatically uses realistic mock GPU metrics
  - If you have NVIDIA hardware, install: `pip install pynvml nvidia-ml-py`
  - Mock mode can be forced with `--mock-gpu` flag even if hardware is available

## Quick Start

### Automated Setup

Run the setup script to install dependencies and check prerequisites:
```bash
chmod +x setup.sh
./setup.sh
```

### Manual Setup

1. **Start Elastic Stack**:
   
   **Option A: Using start-local with Observability (Recommended)**
   ```bash
   curl -fsSL https://elastic.co/start-local | sh -s -- --edot
   ```
   Note the API key from the output and update `otel-collector-config.start-local.yaml` with it.
   
   **Option B: Using Docker Compose**
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
   - For start-local Elastic (with `--edot`): 
     - First update `otel-collector-config.start-local.yaml` with your API key from start-local output
     - Then run: `otelcol --config=otel-collector-config.start-local.yaml`
   - For local Elastic: `./run-collector.sh` or `otelcol --config=otel-collector-config.local.yaml`
   
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
   
   **Options:**
   - `--mock-gpu`: Force mock GPU mode (useful for testing without hardware)
   - `--otel-endpoint HOST:PORT`: Custom OpenTelemetry Collector endpoint

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

### Step 1: Create Index Patterns

Before exploring data, you need to create index patterns for each telemetry type:

1. Navigate to **Stack Management** > **Index Patterns** > **Create Index Pattern**
2. Create the following patterns (one at a time):

   **Metrics:**
   - Pattern: `metrics-nvidia-gpu-monitoring-*`
   - Time field: `@timestamp`
   - Click "Create index pattern"

   **Traces:**
   - Pattern: `traces-nvidia-gpu-monitoring-*`
   - Time field: `@timestamp`
   - Click "Create index pattern"

   **Logs:**
   - Pattern: `logs-nvidia-gpu-monitoring-*`
   - Time field: `@timestamp`
   - Click "Create index pattern"

### Step 2: Explore Metrics

1. Go to **Discover** in Kibana
2. Select the `metrics-nvidia-gpu-monitoring-*` index pattern from the dropdown
3. Explore key metrics:
   - `gpu.utilization.percent` - GPU utilization percentage
   - `gpu.memory.used.bytes` - GPU memory usage
   - `gpu.temperature.celsius` - GPU temperature
   - `gpu.power.usage.watts` - GPU power consumption
   - `seismic.job.duration.seconds` - Job execution time
   - `seismic.job.success.count` - Successful job count
   - `seismic.data.ingestion.rate.bytes_per_second` - Data ingestion rate
   - `seismic.data.quality.score` - Data quality scores

**Filtering Tips:**
- Filter by `gpu.index` to see metrics for specific GPUs
- Filter by `gpu.mock` to see if using mock data (`gpu.mock: "true"`)
- Filter by `job.type` to see metrics for specific job types (inference, training, preprocessing)

### Step 3: Explore Traces

1. In **Discover**, select the `traces-nvidia-gpu-monitoring-*` index pattern
2. View distributed traces for:
   - `seismic.analysis.inference` - AI inference job traces
   - `seismic.analysis.training` - Training job traces
   - `seismic.analysis.preprocessing` - Data preprocessing traces
   - `seismic.data.ingestion` - Data ingestion traces
   - `seismic.data.processing` - Data processing traces
   - `seismic.data.pipeline` - Complete pipeline traces

**Trace Details:**
- Click on any trace to see the full span hierarchy
- View timing information for each operation
- See attributes like `job.id`, `job.type`, `data.size`, etc.

### Step 4: Explore Logs

1. In **Discover**, select the `logs-nvidia-gpu-monitoring-*` index pattern
2. View application logs showing:
   - Job queue operations
   - Job completion status
   - Data pipeline progress
   - GPU monitoring status
   - Error messages (if any)

**Log Filtering:**
- Filter by `log.level` (INFO, WARN, ERROR)
- Search for specific job IDs: `job_0020`
- Filter by service: `resource.attributes.service.name: "nvidia-gpu-monitoring"`

### Step 5: Create Dashboards (Optional)

1. Navigate to **Dashboard** > **Create Dashboard**
2. Add visualizations for:
   - GPU utilization over time (line chart)
   - GPU memory usage (area chart)
   - Job success/failure rates (pie chart)
   - Data processing throughput (bar chart)
   - Average job duration (metric)
   - Data quality scores (histogram)

**Quick Visualization Tips:**
- Use Lens or Visualize to create charts
- Group by `gpu.index` for multi-GPU setups
- Group by `job.type` to compare job types
- Use time-based aggregations for trends

## Monitoring Components

### GPU Monitor (`gpu_monitor.py`)
- Collects real-time GPU metrics using NVIDIA Management Library (NVML)
- Monitors: utilization, memory, temperature, power, clock speeds
- **Automatic Mock Mode**: Falls back to realistic mock data if NVIDIA hardware is not available
- **Mock Data Features**:
  - Realistic GPU metrics (utilization, memory, temperature, power)
  - All metrics exported to OpenTelemetry/Elasticsearch
  - Marked with `gpu.mock: "true"` attribute for filtering
  - Can be forced with `--mock-gpu` flag for testing

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

The project includes multiple collector configurations:
- `otel-collector-config.start-local.yaml` - For start-local Elastic instance with API key
- `otel-collector-config.local.yaml` - For local Elastic without authentication
- `otel-collector-config.yaml` - For Docker Compose setup

**For start-local Elastic:**
The configuration file `otel-collector-config.start-local.yaml` is configured for:
- Endpoint: `http://localhost:9200`
- API key: **You must update this with the API key from start-local output**

After running `curl -fsSL https://elastic.co/start-local | sh -s -- --edot`, copy the API key from the terminal output and update the `api_key` field in the config file.

Edit the config files to:
- Adjust export intervals and batch sizes
- Modify Elasticsearch endpoints
- Update API keys or authentication
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
- The demo will automatically use mock data if GPU is not available
- Force mock mode for testing: `python demo.py --mock-gpu`

## Stopping the Demo

1. Press `Ctrl+C` in the demo terminal
2. Stop OpenTelemetry Collector: `Ctrl+C` or `docker stop otel-collector`
3. Stop Elastic stack: `docker-compose down`
