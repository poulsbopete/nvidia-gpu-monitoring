#!/bin/bash
# Script to run OpenTelemetry Collector

set -e

echo "Starting OpenTelemetry Collector..."

# Check if otelcol is installed
if ! command -v otelcol &> /dev/null; then
    echo "Error: otelcol not found"
    echo ""
    echo "Option 1: Install from https://opentelemetry.io/docs/collector/getting-started/"
    echo ""
    echo "Option 2: Use Docker:"
    echo "  docker run -p 4317:4317 -p 4318:4318 \\"
    echo "    -v \$(pwd)/otel-collector-config.yaml:/etc/otelcol/config.yaml \\"
    echo "    otel/opentelemetry-collector:latest"
    exit 1
fi

# Check if config file exists
if [ ! -f "otel-collector-config.local.yaml" ]; then
    echo "Error: otel-collector-config.local.yaml not found"
    exit 1
fi

# Run collector
echo "Running OpenTelemetry Collector with config: otel-collector-config.local.yaml"
otelcol --config=otel-collector-config.local.yaml
