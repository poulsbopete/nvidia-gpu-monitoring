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

# Check for start-local config first, then fall back to local config
if [ -f "otel-collector-config.start-local.yaml" ]; then
    CONFIG_FILE="otel-collector-config.start-local.yaml"
    echo "Using start-local Elastic configuration"
elif [ -f "otel-collector-config.local.yaml" ]; then
    CONFIG_FILE="otel-collector-config.local.yaml"
    echo "Using local Elastic configuration"
else
    echo "Error: No collector config file found"
    echo "Expected: otel-collector-config.start-local.yaml or otel-collector-config.local.yaml"
    exit 1
fi

# Run collector
echo "Running OpenTelemetry Collector with config: $CONFIG_FILE"
otelcol --config=$CONFIG_FILE
