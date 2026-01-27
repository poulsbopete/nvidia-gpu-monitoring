# Mock GPU Mode

The NVIDIA GPU Monitoring Demo includes full support for mock GPU monitoring, allowing you to test and demonstrate the monitoring pipeline without requiring actual NVIDIA hardware.

## Automatic Mock Mode

The demo **automatically** uses mock GPU data when:
- NVIDIA drivers are not installed
- `pynvml` library is not available
- NVML initialization fails
- No NVIDIA GPUs are detected

**No configuration needed!** Just run the demo and it will work.

## Mock Data Features

The mock GPU monitor generates realistic GPU metrics:

- **GPU Utilization**: 40-95% (randomized)
- **Memory Usage**: 30GB used / 40GB total (simulated A100)
- **Temperature**: 45-75°C (realistic range)
- **Power Consumption**: 200-300W (within normal limits)
- **Clock Speeds**: Graphics 1000-1400 MHz, Memory 1200-1600 MHz

All mock metrics are:
- ✅ Sent to OpenTelemetry
- ✅ Exported to Elasticsearch
- ✅ Visible in Kibana dashboards
- ✅ Tagged with `gpu.mock: "true"` attribute

## Forcing Mock Mode

Even if you have NVIDIA hardware, you can force mock mode for testing:

```bash
python demo.py --mock-gpu
```

This is useful for:
- Testing the monitoring pipeline
- Demonstrations without hardware
- Development environments
- CI/CD pipelines

## Identifying Mock Data

In Kibana, you can filter mock data using the `gpu.mock` attribute:

```json
{
  "gpu.mock": "true"
}
```

Or search for mock GPU names:
- `gpu.name: "NVIDIA A100 (Mock)"`

## Real vs Mock Comparison

| Feature | Real GPU | Mock GPU |
|---------|----------|----------|
| Requires NVIDIA hardware | ✅ Yes | ❌ No |
| Requires pynvml | ✅ Yes | ❌ No |
| Metrics sent to OpenTelemetry | ✅ Yes | ✅ Yes |
| Visible in Elasticsearch | ✅ Yes | ✅ Yes |
| Real-time actual values | ✅ Yes | ⚠️ Simulated |
| Useful for testing | ✅ Yes | ✅ Yes |

## Installation Without GPU

The demo works perfectly without installing GPU libraries:

```bash
# Standard installation (no GPU libraries needed)
pip install -r requirements.txt

# The demo will automatically detect no GPU and use mock data
python demo.py
```

If you later get NVIDIA hardware, just install:
```bash
pip install pynvml nvidia-ml-py
```

The demo will automatically switch to real GPU monitoring!

## Example Output

When running in mock mode, you'll see:

```
WARNING - NVML not available - using mock data
INFO - Starting GPU monitoring loop...
DEBUG - GPU 0: Util=67%, Mem=30.0GB/40.0GB, Temp=58°C, Power=245W
```

All metrics are still exported to Elasticsearch and visible in Kibana!
