# Quick Start Guide

## Prerequisites Check

```bash
# Check Python
python3 --version  # Should be 3.9+

# Check Docker
docker --version
docker-compose --version

# Check NVIDIA GPU (optional - demo works without it!)
# The demo automatically uses mock GPU data if no hardware is available
# If you have NVIDIA hardware and want real metrics:
#   pip install pynvml nvidia-ml-py
nvidia-smi  # Optional - only if you have NVIDIA hardware
```

## Step-by-Step Setup

### 1. Start Elastic Stack and OpenTelemetry Collector

**Option A: Using start-local Elastic with Observability (Recommended)**
```bash
# Start Elastic with observability features
curl -fsSL https://elastic.co/start-local | sh -s -- --edot

# Note the API key from the output, then update otel-collector-config.start-local.yaml
# with the API key (replace the existing api_key value)

# Start OpenTelemetry Collector with start-local config
otelcol --config=otel-collector-config.start-local.yaml
```

**Option B: Using Docker Compose (local Elastic)**
```bash
docker-compose up -d
```

Wait for services to be healthy:
```bash
docker-compose ps
```

Check Elasticsearch:
```bash
# For Docker Compose (no auth):
curl http://localhost:9200/_cluster/health

# For start-local with API key (replace YOUR_API_KEY with actual key):
curl -H "Authorization: ApiKey YOUR_API_KEY" http://localhost:9200/_cluster/health
```

### 2. Setup Python Environment

```bash
# Run automated setup
./setup.sh

# Or manually:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Run the Demo

```bash
source venv/bin/activate
python demo.py
```

**Note**: If you don't have NVIDIA GPU hardware, the demo will automatically use mock GPU data. All metrics will still be sent to Elasticsearch!

**Options:**
- `--mock-gpu`: Force mock GPU mode (even if hardware is available)
- `--otel-endpoint HOST:PORT`: Custom OpenTelemetry endpoint

The demo will start generating:
- GPU metrics every 5 seconds (real or mock)
- AI analysis jobs every 2 seconds
- Seismic data processing every 10 seconds

### 4. View Data in Kibana

1. **Open Kibana**: http://localhost:5601

2. **Create Index Patterns** (required first step):
   - Go to **Stack Management** > **Index Patterns** > **Create Index Pattern**
   - Create these patterns one at a time:
     - `metrics-nvidia-gpu-monitoring-*` (Time field: `@timestamp`)
     - `traces-nvidia-gpu-monitoring-*` (Time field: `@timestamp`)
     - `logs-nvidia-gpu-monitoring-*` (Time field: `@timestamp`)

3. **Explore Data in Discover**:
   - Go to **Discover**
   - Select an index pattern from the dropdown
   - Use the time picker (top right) to adjust time range
   - Click on fields in the left sidebar to filter

4. **What to Look For**:
   - **Metrics**: GPU utilization, memory, temperature, job durations
   - **Traces**: Distributed traces showing job execution and data pipelines
   - **Logs**: Application logs showing job status, data storage, pipeline progress

5. **Create Visualizations** (optional):
   - Go to **Dashboard** > **Create Dashboard**
   - Add visualizations for GPU metrics, job performance, data throughput

## Stopping Everything

```bash
# Stop demo: Ctrl+C

# Stop all services
docker-compose down
```

## Troubleshooting

### Elasticsearch not starting
```bash
# Check logs
docker-compose logs elasticsearch

# Increase memory limit in docker-compose.yml if needed
```

### No data in Kibana
1. Wait 30-60 seconds for data to be indexed
2. Check OpenTelemetry Collector logs: `docker-compose logs otel-collector`
3. Verify demo is running and sending data
4. Check Elasticsearch indices: `curl http://localhost:9200/_cat/indices`

### Collector connection issues
- Verify collector is running: `docker-compose ps otel-collector`
- Check collector logs: `docker-compose logs otel-collector`
- Verify port 4317 is accessible: `curl http://localhost:4317`
