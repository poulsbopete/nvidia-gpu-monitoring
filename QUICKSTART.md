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

**Option A: Using start-local Elastic (with API key)**
```bash
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
curl http://localhost:9200/_cluster/health
# For start-local with API key:
curl -H "Authorization: ApiKey cS1LS0Fad0IweERGVE5FUFl6UFk6b3FDcm8zSExPMnhiMUh3YVlvZW42QQ==" http://localhost:9200/_cluster/health
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

1. Open browser: http://localhost:5601
2. Go to **Stack Management** > **Index Patterns**
3. Create index patterns:
   - `metrics-nvidia-gpu-monitoring-*`
   - `traces-nvidia-gpu-monitoring-*`
   - `logs-nvidia-gpu-monitoring-*`
4. Explore data in **Discover**

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
