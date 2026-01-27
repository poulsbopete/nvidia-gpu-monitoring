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

start-local with `--edot` includes a built-in OpenTelemetry Collector, so setup is simple:

```bash
# Start Elastic with observability features (includes built-in collector)
curl -fsSL https://elastic.co/start-local | sh -s -- --edot

# Save the API key from the output (you'll need it if you want to use your own collector)
# The built-in collector is already running on ports 4317-4318 - ready to use!
```

**That's it!** The built-in collector is ready. Skip to step 3 to run the demo.

**Optional: Use Your Own Collector**

If you prefer to use your own collector with custom configuration:

```bash
# 1. Update otel-collector-config.start-local.yaml with the API key from start-local output
# 2. Start your collector:
otelcol --config=otel-collector-config.start-local.yaml
```

**Verify Elasticsearch is running:**

```bash
# For start-local with API key (replace YOUR_API_KEY with actual key from start-local output):
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

**Note**: 
- If you don't have NVIDIA GPU hardware, the demo will automatically use mock GPU data. All metrics will still be sent to Elasticsearch!
- If using start-local's built-in collector, the demo will automatically connect to `localhost:4317`
- If using your own collector, make sure it's running first

**Options:**
- `--mock-gpu`: Force mock GPU mode (even if hardware is available)
- `--otel-endpoint HOST:PORT`: Custom OpenTelemetry endpoint (default: `localhost:4317`)

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

### Port Already Allocated (9200)

If you see "port is already allocated" when running docker-compose:
- start-local is already running on port 9200
- This is fine! Use start-local instead of docker-compose
- Check running containers: `docker ps | grep -E "(es-local|kibana)"`
- If you want to use docker-compose, stop start-local first

### Elasticsearch not starting (Docker Compose)
```bash
# Check logs
docker-compose logs elasticsearch

# Increase memory limit in docker-compose.yml if needed
```

### No data in Kibana
1. Wait 30-60 seconds for data to be indexed
2. Check OpenTelemetry Collector:
   - For start-local built-in: `docker logs edot-collector`
   - For docker-compose: `docker-compose logs otel-collector`
   - For local collector: Check the terminal where you ran `otelcol`
3. Verify demo is running and sending data
4. Check Elasticsearch indices:
   - For start-local: `curl -H "Authorization: ApiKey YOUR_API_KEY" http://localhost:9200/_cat/indices`
   - For docker-compose: `curl http://localhost:9200/_cat/indices`

### Collector connection issues
- Verify collector is running:
  - Built-in (start-local): `docker ps | grep edot-collector`
  - Docker Compose: `docker-compose ps otel-collector`
  - Local: Check the terminal where you ran `otelcol`
- Check collector logs (see above)
- Verify port 4317 is accessible: `curl http://localhost:4317` (should return empty response if collector is running)

### Can't find API key from start-local
- Check the terminal where you ran `curl -fsSL https://elastic.co/start-local | sh -s -- --edot`
- Look for a line with `elastic:` followed by a long string
- If you can't find it, you can restart start-local (but this will stop your current instance)
- If using the built-in collector, you don't need the API key - it's already configured!
