# Kibana Exploration Guide

This guide provides step-by-step instructions for exploring your NVIDIA GPU monitoring data in Kibana.

## Prerequisites

- Kibana running at http://localhost:5601
- Demo application running and generating data
- OpenTelemetry Collector running and exporting to Elasticsearch

## Step 1: Create Index Patterns

Index patterns tell Kibana which indices to search. You need to create one for each telemetry type.

### Creating Index Patterns

1. Navigate to **Stack Management** > **Index Patterns**
2. Click **Create Index Pattern**
3. For each pattern, follow these steps:

   **Metrics Pattern:**
   ```
   Index pattern name: metrics-nvidia-gpu-monitoring-*
   Time field: @timestamp
   Click "Create index pattern"
   ```

   **Traces Pattern:**
   ```
   Index pattern name: traces-nvidia-gpu-monitoring-*
   Time field: @timestamp
   Click "Create index pattern"
   ```

   **Logs Pattern:**
   ```
   Index pattern name: logs-nvidia-gpu-monitoring-*
   Time field: @timestamp
   Click "Create index pattern"
   ```

## Step 2: Explore Metrics

Metrics show numerical data over time - perfect for monitoring GPU performance and job statistics.

### Accessing Metrics

1. Go to **Discover** in Kibana
2. Select `metrics-nvidia-gpu-monitoring-*` from the index pattern dropdown (top left)
3. Adjust the time range if needed (top right)

### Key Metrics to Explore

**GPU Metrics:**
- `gpu.utilization.percent` - How busy the GPU is (0-100%)
- `gpu.memory.used.bytes` - GPU memory currently in use
- `gpu.memory.total.bytes` - Total GPU memory available
- `gpu.temperature.celsius` - GPU temperature
- `gpu.power.usage.watts` - Current power consumption
- `gpu.clock.graphics.mhz` - Graphics clock speed
- `gpu.clock.memory.mhz` - Memory clock speed

**Job Metrics:**
- `seismic.job.duration.seconds` - How long jobs take to complete
- `seismic.job.success.count` - Number of successful jobs
- `seismic.job.failure.count` - Number of failed jobs
- `seismic.job.data.processed.bytes` - Amount of data processed

**Data Pipeline Metrics:**
- `seismic.data.ingestion.rate.bytes_per_second` - Data ingestion speed
- `seismic.data.processing.latency.seconds` - Processing time
- `seismic.data.storage.size.bytes` - Total data stored
- `seismic.data.quality.score` - Data quality (0-100)

### Filtering Metrics

Click on any field in the left sidebar to filter:
- **By GPU**: Click `gpu.index` to see metrics for specific GPUs
- **By Job Type**: Click `job.type` to filter by inference, training, or preprocessing
- **Mock vs Real**: Click `gpu.mock` to see if using mock data

### Creating Metric Visualizations

1. Click the **Lens** icon (or go to **Visualize** > **Create Visualization**)
2. Select `metrics-nvidia-gpu-monitoring-*` index pattern
3. Choose visualization type:
   - **Line Chart**: For trends over time (GPU utilization, temperature)
   - **Area Chart**: For cumulative metrics (memory usage)
   - **Bar Chart**: For comparisons (job types, GPU comparison)
   - **Metric**: For single values (current GPU utilization)

## Step 3: Explore Traces

Traces show the execution flow of operations, helping you understand performance bottlenecks.

### Accessing Traces

1. In **Discover**, select `traces-nvidia-gpu-monitoring-*` index pattern
2. Traces are organized by operation name

### Key Traces to Explore

**Analysis Job Traces:**
- `seismic.analysis.inference` - Complete inference job execution
  - Nested spans: model loading, data loading, GPU computation, post-processing
- `seismic.analysis.training` - Training job with epochs
- `seismic.analysis.preprocessing` - Data preprocessing operations

**Data Pipeline Traces:**
- `seismic.data.ingestion` - Data ingestion operations
- `seismic.data.processing` - Individual chunk processing
- `seismic.data.pipeline` - Complete end-to-end pipeline

### Viewing Trace Details

1. Click on any trace entry in Discover
2. Expand the trace to see:
   - **Duration**: How long each operation took
   - **Spans**: Nested operations within the trace
   - **Attributes**: Job ID, data size, quality scores, etc.
   - **Status**: Success or failure

### Filtering Traces

- Filter by `trace.name` to see specific operations
- Filter by `job.type` to see only inference, training, or preprocessing
- Filter by `job.id` to track a specific job
- Filter by duration to find slow operations

## Step 4: Explore Logs

Logs provide detailed information about what's happening in the application.

### Accessing Logs

1. In **Discover**, select `logs-nvidia-gpu-monitoring-*` index pattern
2. Logs show real-time application activity

### What You'll See in Logs

**Job Operations:**
- "Added job job_XXXX to queue"
- "Job job_XXXX completed successfully in X.XXs"
- "Job job_XXXX failed: [error message]"

**Data Pipeline Operations:**
- "Ingesting X bytes of seismic data from [source]"
- "Processing chunk [chunk_id]"
- "Pipeline completed: X chunks, avg quality: XX.X"
- "Data [data_id] stored successfully"

**GPU Monitoring:**
- "Initialized GPU monitoring for X GPU(s)"
- "GPU X: Util=XX%, Mem=XX.XGB/XX.XGB, Temp=XX°C, Power=XXXW"

### Filtering Logs

**By Log Level:**
- Click `log.level` to filter by INFO, WARN, or ERROR

**By Message Content:**
- Use the search bar: `job_0020` to find specific job logs
- Search: `completed successfully` to see only successful jobs
- Search: `failed` to see errors

**By Service:**
- Filter: `resource.attributes.service.name: "nvidia-gpu-monitoring"`

## Step 5: Create Dashboards

Dashboards combine multiple visualizations for comprehensive monitoring.

### Creating a Dashboard

1. Go to **Dashboard** > **Create Dashboard**
2. Click **Add** > **Add from library**
3. Create visualizations or add existing ones

### Recommended Dashboard Panels

**GPU Monitoring Panel:**
- Line chart: GPU utilization over time
- Area chart: GPU memory usage
- Metric: Current GPU temperature
- Metric: Current power consumption

**Job Performance Panel:**
- Bar chart: Job duration by type
- Pie chart: Success vs failure rates
- Metric: Average job duration
- Table: Recent jobs with status

**Data Pipeline Panel:**
- Line chart: Data ingestion rate
- Bar chart: Processing latency
- Metric: Total data stored
- Histogram: Data quality scores

### Saving and Sharing

1. Click **Save** to save your dashboard
2. Give it a name like "NVIDIA GPU Monitoring"
3. Dashboards can be shared with team members

## Tips and Tricks

### Time Range Selection

- Use **Last 15 minutes** for real-time monitoring
- Use **Last 1 hour** for recent trends
- Use **Last 24 hours** for daily patterns
- Use custom ranges for specific time periods

### Field Statistics

Click on any field in the left sidebar to see:
- Top values
- Field statistics (min, max, average)
- Document count

### Exporting Data

1. In Discover, use the **Share** button
2. Export as CSV for analysis in Excel/Python
3. Generate reports for documentation

### Alerts (Advanced)

Set up alerts in **Stack Management** > **Rules and Connectors**:
- Alert when GPU temperature exceeds threshold
- Alert when job failure rate is high
- Alert when data quality drops below threshold

## Troubleshooting

### No Data Showing

1. Check time range - data might be outside selected range
2. Verify index patterns are created correctly
3. Check OpenTelemetry Collector logs
4. Verify demo application is running

### Missing Fields

1. Wait a few minutes for data to be indexed
2. Refresh the index pattern (Stack Management > Index Patterns > Refresh)
3. Check that the demo is generating the expected metrics

### Performance Issues

1. Reduce time range if viewing large datasets
2. Use filters to narrow down data
3. Consider using saved searches for frequently used queries
