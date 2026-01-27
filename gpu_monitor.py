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
    
    def __init__(self, force_mock: bool = False):
        """
        Initialize GPU monitor.
        
        Args:
            force_mock: If True, use mock data even if NVML is available (useful for testing)
        """
        self.meter = get_meter(__name__)
        self.initialized = False
        self.gpu_count = 0
        self.force_mock = force_mock
        
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
        
        if self.force_mock:
            logger.info("Mock mode forced - using fake GPU data")
            self.initialized = False
            self.gpu_count = 1
        elif NVML_AVAILABLE:
            try:
                pynvml.nvmlInit()
                self.gpu_count = pynvml.nvmlDeviceGetCount()
                self.initialized = True
                logger.info(f"Initialized GPU monitoring for {self.gpu_count} GPU(s)")
            except Exception as e:
                logger.error(f"Failed to initialize NVML: {e}")
                logger.warning("Falling back to mock data")
                self.initialized = False
                self.gpu_count = 1
        else:
            logger.warning("NVML not available - using mock data")
            self.gpu_count = 1  # Set to 1 for mock mode
    
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
        
        # Set gpu_count to 1 for mock mode
        if self.gpu_count == 0:
            self.gpu_count = 1
        
        # Generate realistic mock metrics
        utilization_gpu = random.randint(40, 95)
        utilization_memory = random.randint(50, 90)
        memory_total = 40 * 1024 * 1024 * 1024  # 40 GB
        memory_used = int(memory_total * (utilization_memory / 100))
        memory_free = memory_total - memory_used
        temperature = random.randint(45, 75)
        power_usage = random.randint(200, 300)
        power_limit = 400
        clock_graphics = random.randint(1000, 1400)
        clock_memory = random.randint(1200, 1600)
        
        gpu_metrics = {
            "gpu_index": 0,
            "gpu_name": "NVIDIA A100 (Mock)",
            "gpu_uuid": "mock-uuid-001",
            "utilization_gpu": utilization_gpu,
            "utilization_memory": utilization_memory,
            "memory_used": memory_used,
            "memory_total": memory_total,
            "memory_free": memory_free,
            "temperature": temperature,
            "power_usage": power_usage,
            "power_limit": power_limit,
            "clock_graphics": clock_graphics,
            "clock_memory": clock_memory,
        }
        
        # Send mock metrics to OpenTelemetry
        attributes = {
            "gpu.index": "0",
            "gpu.name": "NVIDIA A100 (Mock)",
            "gpu.uuid": "mock-uuid-001",
            "gpu.mock": "true",  # Flag to indicate this is mock data
        }
        
        self.gpu_utilization.add(utilization_gpu, attributes=attributes)
        self.gpu_memory_used.add(memory_used, attributes=attributes)
        self.gpu_memory_total.add(memory_total, attributes=attributes)
        self.gpu_temperature.add(temperature, attributes=attributes)
        self.gpu_power_usage.add(power_usage, attributes=attributes)
        self.gpu_power_limit.add(power_limit, attributes=attributes)
        self.gpu_clock_graphics.add(clock_graphics, attributes=attributes)
        self.gpu_clock_memory.add(clock_memory, attributes=attributes)
        
        return [gpu_metrics]
    
    def shutdown(self):
        """Cleanup NVML resources."""
        if self.initialized and NVML_AVAILABLE:
            try:
                pynvml.nvmlShutdown()
            except Exception as e:
                logger.error(f"Error shutting down NVML: {e}")
