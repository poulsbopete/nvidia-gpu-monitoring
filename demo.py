"""
Main demo application for NVIDIA GPU monitoring with OpenTelemetry.
Demonstrates GPU monitoring, AI job monitoring, and seismic data processing.
"""
import time
import logging
import signal
import sys
from typing import List
from otel_setup import initialize_otel
from gpu_monitor import GPUMonitor
from job_monitor import SeismicAnalysisJob, JobQueue
from seismic_monitor import SeismicDataProcessor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MonitoringDemo:
    """Main demo application."""
    
    def __init__(self, otel_endpoint: str = "localhost:4317"):
        logger.info("Initializing monitoring demo...")
        
        # Initialize OpenTelemetry
        logger.info(f"Initializing OpenTelemetry (endpoint: {otel_endpoint})...")
        self.otel_providers = initialize_otel(otel_endpoint)
        
        # Initialize monitors
        logger.info("Initializing GPU monitor...")
        self.gpu_monitor = GPUMonitor()
        
        logger.info("Initializing job queue...")
        self.job_queue = JobQueue()
        
        logger.info("Initializing seismic data processor...")
        self.data_processor = SeismicDataProcessor()
        
        self.running = False
    
    def run_gpu_monitoring_loop(self):
        """Continuously collect GPU metrics."""
        logger.info("Starting GPU monitoring loop...")
        while self.running:
            try:
                metrics = self.gpu_monitor.collect_metrics()
                for gpu_metric in metrics:
                    logger.debug(
                        f"GPU {gpu_metric['gpu_index']}: "
                        f"Util={gpu_metric['utilization_gpu']}%, "
                        f"Mem={gpu_metric['memory_used']/1024**3:.1f}GB/{gpu_metric['memory_total']/1024**3:.1f}GB, "
                        f"Temp={gpu_metric['temperature']}°C, "
                        f"Power={gpu_metric['power_usage']:.1f}W"
                    )
                time.sleep(5)  # Collect every 5 seconds
            except Exception as e:
                logger.error(f"Error in GPU monitoring loop: {e}")
                time.sleep(5)
    
    def run_job_simulation(self):
        """Simulate AI analysis jobs."""
        logger.info("Starting job simulation...")
        job_types = ["inference", "training", "preprocessing"]
        job_id = 0
        
        while self.running:
            try:
                # Create and add jobs periodically
                if len(self.job_queue.queue) < 5:
                    job_type = job_types[job_id % len(job_types)]
                    data_size = 100 * 1024 * 1024 * (1 + (job_id % 5))  # 100MB to 500MB
                    
                    job = SeismicAnalysisJob(
                        job_id=f"job_{job_id:04d}",
                        data_size=data_size,
                        job_type=job_type
                    )
                    self.job_queue.add_job(job)
                    job_id += 1
                
                # Process jobs
                if self.job_queue.queue:
                    result = self.job_queue.process_job()
                    if result:
                        logger.info(f"Job {result['job_id']} {result['status']} (duration: {result.get('duration', 0):.2f}s)")
                
                time.sleep(2)  # Process jobs every 2 seconds
            except Exception as e:
                logger.error(f"Error in job simulation: {e}")
                time.sleep(2)
    
    def run_data_processing_simulation(self):
        """Simulate seismic data processing."""
        logger.info("Starting data processing simulation...")
        pipeline_id = 0
        
        while self.running:
            try:
                # Run data processing pipeline periodically
                source = f"seismic_survey_{pipeline_id:04d}"
                data_size = 500 * 1024 * 1024 * (1 + (pipeline_id % 3))  # 500MB to 1.5GB
                num_chunks = 10 + (pipeline_id % 10)
                
                result = self.data_processor.process_pipeline(
                    source=source,
                    data_size=data_size,
                    num_chunks=num_chunks
                )
                
                logger.info(
                    f"Pipeline {source}: {result['chunks_processed']} chunks, "
                    f"quality: {result['avg_quality']:.1f}, "
                    f"total stored: {result['total_stored']/1024**3:.2f}GB"
                )
                
                pipeline_id += 1
                time.sleep(10)  # Run pipeline every 10 seconds
            except Exception as e:
                logger.error(f"Error in data processing simulation: {e}")
                time.sleep(10)
    
    def run(self):
        """Run the demo."""
        import threading
        
        logger.info("=" * 60)
        logger.info("NVIDIA GPU Monitoring Demo - Starting")
        logger.info("=" * 60)
        logger.info("Press Ctrl+C to stop")
        logger.info("=" * 60)
        
        self.running = True
        
        # Start monitoring threads
        gpu_thread = threading.Thread(target=self.run_gpu_monitoring_loop, daemon=True)
        job_thread = threading.Thread(target=self.run_job_simulation, daemon=True)
        data_thread = threading.Thread(target=self.run_data_processing_simulation, daemon=True)
        
        gpu_thread.start()
        job_thread.start()
        data_thread.start()
        
        try:
            # Keep main thread alive
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("\nShutting down...")
            self.shutdown()
    
    def shutdown(self):
        """Cleanup resources."""
        logger.info("Shutting down monitoring demo...")
        self.running = False
        
        # Shutdown GPU monitor
        self.gpu_monitor.shutdown()
        
        # Shutdown OpenTelemetry providers
        if self.otel_providers:
            logger.info("Shutting down OpenTelemetry providers...")
            # Note: In production, you'd want to flush exporters here
            time.sleep(2)  # Give time for final exports
        
        logger.info("Demo shutdown complete")

def signal_handler(sig, frame):
    """Handle shutdown signals."""
    logger.info("\nReceived shutdown signal")
    sys.exit(0)

def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="NVIDIA GPU Monitoring Demo")
    parser.add_argument(
        "--otel-endpoint",
        default="localhost:4317",
        help="OpenTelemetry Collector endpoint (default: localhost:4317)"
    )
    
    args = parser.parse_args()
    
    # Setup signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Create and run demo
    demo = MonitoringDemo(otel_endpoint=args.otel_endpoint)
    
    try:
        demo.run()
    except Exception as e:
        logger.error(f"Demo error: {e}", exc_info=True)
    finally:
        demo.shutdown()

if __name__ == "__main__":
    main()
