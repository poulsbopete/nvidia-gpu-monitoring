# Docker Setup Guide

## Docker File Sharing (macOS)

**Note:** The project has been moved to `~/nvidia-gpu-monitoring` (home directory) to avoid Docker file sharing issues. Docker Desktop on macOS typically has access to the home directory by default.

If you encounter errors like:
```
Error response from daemon: mounts denied: 
The path is not shared from the host
```

### Solution 1: Add Path to Docker File Sharing (Recommended)

1. Open **Docker Desktop**
2. Go to **Settings** (gear icon) > **Resources** > **File Sharing**
3. Click **+** to add a new path
4. Add the directory containing the project:
   - The project is now in `~/nvidia-gpu-monitoring` (home directory)
   - Docker Desktop typically has access to the home directory by default
   - If needed, add `~` or `/Users/your-username` to file sharing
5. Click **Apply & Restart**

### Solution 2: Use Relative Paths (Already Configured)

The `docker-compose.yml` uses `${PWD}` which should work if you run docker-compose from the project directory:

```bash
cd ~/nvidia-gpu-monitoring
docker-compose up -d
```

### Solution 3: Copy Config into Container

If file sharing is not possible, you can copy the config into the container:

1. Create a Dockerfile for the collector:
```dockerfile
FROM otel/opentelemetry-collector-contrib:latest
COPY otel-collector-config.yaml /etc/otelcol/config.yaml
```

2. Update docker-compose.yml to build the image instead of mounting

### Solution 4: Use Environment Variable

Set the path explicitly:

```bash
export PWD=$(pwd)
docker-compose up -d
```

## Verifying Setup

After fixing file sharing, verify the setup:

```bash
# Check containers are running
docker-compose ps

# Check collector logs
docker-compose logs otel-collector

# Verify config is mounted
docker exec otel-collector cat /etc/otelcol/config.yaml
```

## Alternative: Run Collector Outside Docker

If Docker file sharing continues to be an issue, you can run the collector outside Docker:

```bash
# Install collector binary
# Then run:
otelcol --config=otel-collector-config.start-local.yaml
```

This avoids Docker file sharing issues entirely.
