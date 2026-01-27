#!/bin/bash
# Setup script for NVIDIA GPU Monitoring Demo

set -e

echo "=========================================="
echo "NVIDIA GPU Monitoring Demo - Setup"
echo "=========================================="

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found Python $python_version"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created"
else
    echo "Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Try to install GPU monitoring libraries (optional)
echo ""
echo "Checking for NVIDIA GPU support..."
if command -v nvidia-smi &> /dev/null; then
    echo "NVIDIA GPU detected:"
    nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader
    echo ""
    echo "Installing GPU monitoring libraries..."
    pip install pynvml nvidia-ml-py || echo "Warning: Could not install GPU libraries. Mock data will be used."
else
    echo "No NVIDIA GPU detected. GPU monitoring will use mock data."
    echo "To enable real GPU monitoring, install: pip install pynvml nvidia-ml-py"
fi

# Check for OpenTelemetry Collector
echo ""
echo "Checking for OpenTelemetry Collector..."
if command -v otelcol &> /dev/null; then
    echo "OpenTelemetry Collector found: $(otelcol --version 2>&1 | head -n 1)"
else
    echo "Warning: OpenTelemetry Collector (otelcol) not found."
    echo "Install it from: https://opentelemetry.io/docs/collector/getting-started/"
    echo "Or use the Docker image: otel/opentelemetry-collector:latest"
fi

echo ""
echo "=========================================="
echo "Setup complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Start Elastic stack: docker-compose up -d"
echo "2. Start OpenTelemetry Collector: otelcol --config=otel-collector-config.yaml"
echo "3. Run the demo: python demo.py"
echo ""
echo "Access Kibana at: http://localhost:5601"
echo ""
