"""
GPU monitoring module for NVIDIA GPUs using pynvml.
Collects metrics and sends them via OpenTelemetry.
"""
import time
import logging
from typing import Dict, List, Optional
from opentelemetry import metrics
from opentelemetry.metrics import get_meter

logger = logging.getLogger(__name__)

try:
    import pynvml
    NVML_AVAILABLE = True
except ImportError:
    NVML_AVAILABLE = False
    logger.warning("pynvml not available. GPU monitoring will be disabled.")

class GPUMonitor:
    """Monitor NVIDIA GPU metrics using pynvml."""
    
    def __init__(self):
        self.meter = get_meter(__name__)
        self.initialized = False
        self.gpu_count = 0
        
        # Create OpenTelemetry metrics
        self.gpu_utilization = self.meter.create_up_down_counter(
            name="gpu.utilization.percent",
            description="GPU utilization percentage",
            unit="%",
        )
        
        self.gpu_memory_used = self.meter.create_up_down_counter(
            name="gpu.memory.used.bytes",
            description="GPU memory used in bytes",
            unit="By",
        )
        
        self.gpu_memory_total = self.meter.create_up_down_counter(
            name="gpu.memory.total.bytes",
            description="GPU memory total in bytes",
            unit="By",
        )
        
        self.gpu_temperature = self.meter.create_up_down_counter(
            name="gpu.temperature.celsius",
            description="GPU temperature in Celsius",
            unit="°C",
        )
        
        self.gpu_power_usage = self.meter.create_up_down_counter(
            name="gpu.power.usage.watts",
            description="GPU power usage in watts",
            unit="W",
        )
        
        self.gpu_power_limit = self.meter.create_up_down_counter(
            name="gpu.power.limit.watts",
            description="GPU power limit in watts",
            unit="W",
        )
        
        self.gpu_clock_graphics = self.meter.create_up_down_counter(
            name="gpu.clock.graphics.mhz",
            description="GPU graphics clock in MHz",
            unit="MHz",
        )
        
        self.gpu_clock_memory = self.meter.create_up_down_counter(
            name="gpu.clock.memory.mhz",
            description="GPU memory clock in MHz",
            unit="MHz",
        )
        
        if NVML_AVAILABLE:
            try:
                pynvml.nvmlInit()
                self.gpu_count = pynvml.nvmlDeviceGetCount()
                self.initialized = True
                logger.info(f"Initialized GPU monitoring for {self.gpu_count} GPU(s)")
            except Exception as e:
                logger.error(f"Failed to initialize NVML: {e}")
                self.initialized = False
        else:
            logger.warning("NVML not available - using mock data")
    
    def get_gpu_info(self, handle) -> Dict:
        """Get GPU information."""
        try:
            name = pynvml.nvmlDeviceGetName(handle).decode('utf-8')
            uuid = pynvml.nvmlDeviceGetUUID(handle).decode('utf-8')
            return {"name": name, "uuid": uuid}
        except Exception as e:
            logger.error(f"Error getting GPU info: {e}")
            return {"name": "Unknown", "uuid": "unknown"}
    
    def collect_metrics(self) -> List[Dict]:
        """Collect metrics from all GPUs."""
        metrics_data = []
        
        if not self.initialized:
            # Return mock data for demo purposes
            return self._get_mock_metrics()
        
        for i in range(self.gpu_count):
            try:
                handle = pynvml.nvmlDeviceGetHandleByIndex(i)
                gpu_info = self.get_gpu_info(handle)
                
                # Utilization
                util = pynvml.nvmlDeviceGetUtilizationRates(handle)
                
                # Memory
                mem_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
                
                # Temperature
                temp = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)
                
                # Power
                power = pynvml.nvmlDeviceGetPowerUsage(handle) / 1000.0  # Convert mW to W
                power_limit = pynvml.nvmlDeviceGetPowerManagementLimitConstraints(handle)[1] / 1000.0
                
                # Clocks
                clock_graphics = pynvml.nvmlDeviceGetClockInfo(handle, pynvml.NVML_CLOCK_GRAPHICS)
                clock_memory = pynvml.nvmlDeviceGetClockInfo(handle, pynvml.NVML_CLOCK_MEM)
                
                gpu_metrics = {
                    "gpu_index": i,
                    "gpu_name": gpu_info["name"],
                    "gpu_uuid": gpu_info["uuid"],
                    "utilization_gpu": util.gpu,
                    "utilization_memory": util.memory,
                    "memory_used": mem_info.used,
                    "memory_total": mem_info.total,
                    "memory_free": mem_info.free,
                    "temperature": temp,
                    "power_usage": power,
                    "power_limit": power_limit,
                    "clock_graphics": clock_graphics,
                    "clock_memory": clock_memory,
                }
                
                metrics_data.append(gpu_metrics)
                
                # Record metrics with attributes
                attributes = {
                    "gpu.index": str(i),
                    "gpu.name": gpu_info["name"],
                    "gpu.uuid": gpu_info["uuid"],
                }
                
                self.gpu_utilization.add(util.gpu, attributes=attributes)
                self.gpu_memory_used.add(mem_info.used, attributes=attributes)
                self.gpu_memory_total.add(mem_info.total, attributes=attributes)
                self.gpu_temperature.add(temp, attributes=attributes)
                self.gpu_power_usage.add(power, attributes=attributes)
                self.gpu_power_limit.add(power_limit, attributes=attributes)
                self.gpu_clock_graphics.add(clock_graphics, attributes=attributes)
                self.gpu_clock_memory.add(clock_memory, attributes=attributes)
                
            except Exception as e:
                logger.error(f"Error collecting metrics for GPU {i}: {e}")
        
        return metrics_data
    
    def _get_mock_metrics(self) -> List[Dict]:
        """Generate mock GPU metrics for demo when NVML is not available."""
        import random
        return [{
            "gpu_index": 0,
            "gpu_name": "NVIDIA A100 (Mock)",
            "gpu_uuid": "mock-uuid-001",
            "utilization_gpu": random.randint(40, 95),
            "utilization_memory": random.randint(50, 90),
            "memory_used": 30 * 1024 * 1024 * 1024,  # 30 GB
            "memory_total": 40 * 1024 * 1024 * 1024,  # 40 GB
            "memory_free": 10 * 1024 * 1024 * 1024,  # 10 GB
            "temperature": random.randint(45, 75),
            "power_usage": random.randint(200, 300),
            "power_limit": 400,
            "clock_graphics": random.randint(1000, 1400),
            "clock_memory": random.randint(1200, 1600),
        }]
    
    def shutdown(self):
        """Cleanup NVML resources."""
        if self.initialized and NVML_AVAILABLE:
            try:
                pynvml.nvmlShutdown()
            except Exception as e:
                logger.error(f"Error shutting down NVML: {e}")
