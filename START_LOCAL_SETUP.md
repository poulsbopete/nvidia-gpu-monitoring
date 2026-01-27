# Start-Local Elastic Setup

This guide explains how to configure the demo to use a start-local Elastic instance with observability features enabled.

## Getting Started with Start-Local

### 1. Start Elastic with Observability

Run the start-local script with the `--edot` flag to enable Elastic Observability:

```bash
curl -fsSL https://elastic.co/start-local | sh -s -- --edot
```

This will:
- Start Elasticsearch with observability features on port 9200
- Start Kibana on port 5601
- **Start a built-in OpenTelemetry Collector** on ports 4317 (gRPC) and 4318 (HTTP)
- Generate API keys automatically
- Display connection information including the API key

**Important**: Save the API key from the output! It looks like `elastic:xxxxx==` and you'll need it if you want to use your own collector.

**Note**: The script will output important information including:
- Elasticsearch endpoint (typically `http://localhost:9200`)
- Kibana URL (typically `http://localhost:5601`)
- API key for authentication
- OpenTelemetry Collector endpoints (ports 4317 and 4318)

### 2. Choose Your OpenTelemetry Collector Option

start-local with `--edot` includes a built-in OpenTelemetry Collector that's already running. You have two options:

#### Option A: Use the Built-in Collector (Simplest - Recommended)

The built-in collector is already running and ready to receive data. **No additional setup needed!**

Just run your demo:
```bash
source venv/bin/activate
python demo.py
```

The demo will automatically send data to `localhost:4317` (the built-in collector).

#### Option B: Use Your Own Collector (More Control)

If you want to use your own collector with custom configuration:

1. **Update the config file** with your API key:
   
   Edit `otel-collector-config.start-local.yaml` and replace `YOUR_API_KEY_FROM_START_LOCAL_OUTPUT` with the API key from step 1:
   
   ```yaml
   elasticsearch:
     endpoints:
       - http://localhost:9200
     api_key: elastic:xxxxx==  # Your actual API key here
   ```
   
   The API key format from start-local looks like: `elastic:xxxxx==`
   
   Copy the entire API key (including the `elastic:` prefix).

2. **Start your OpenTelemetry Collector**:
   ```bash
   otelcol --config=otel-collector-config.start-local.yaml
   ```
   
   **Note**: Make sure the built-in collector isn't using ports 4317-4318, or use different ports in your config.

3. **Run the demo application** (in a separate terminal):
   ```bash
   source venv/bin/activate
   python demo.py
   ```

### 3. Run the Demo

```bash
source venv/bin/activate
python demo.py
```

If using the built-in collector (Option A), the demo will automatically connect to it.
If using your own collector (Option B), ensure it's running first.

## Updating the API Key

If you need to update the API key (e.g., after restarting start-local), edit `otel-collector-config.start-local.yaml`:

```yaml
elasticsearch:
  api_key: YOUR_API_KEY_FROM_START_LOCAL
```

**Getting the API Key from start-local:**
- The API key is displayed in the terminal output when you run the start-local script
- Look for a line containing `elastic:` followed by a long base64-encoded string
- The API key format is: `elastic:xxxxx==`
- **Important**: Copy the entire key including the `elastic:` prefix
- If you can't find it, scroll back in your terminal or check the terminal where you ran start-local
- You can also restart start-local to see the API key again (but this will stop your current instance)

## Verifying Connection

Test the Elasticsearch connection with your API key:

```bash
# Replace YOUR_API_KEY with the actual key from start-local output
curl -H "Authorization: ApiKey YOUR_API_KEY" \
  http://localhost:9200/_cluster/health
```

You should see a JSON response with `"status":"green"` or `"status":"yellow"`.

## Configuration Files

- `otel-collector-config.start-local.yaml` - For start-local Elastic with API key
- `otel-collector-config.local.yaml` - For local Elastic without authentication
- `otel-collector-config.yaml` - For Docker Compose setup

## Troubleshooting

### Authentication Errors

If you see authentication errors in the collector logs:
1. Verify the API key is correct
2. Check that the endpoint URL is correct (http://localhost:9200)
3. Ensure the API key has proper permissions for writing indices

### Connection Refused

If the collector can't connect:
1. Verify start-local Elastic is running: `docker ps | grep es-local-dev`
2. Check the endpoint URL matches your Elastic instance (http://localhost:9200)
3. Ensure port 9200 is accessible
4. Verify the API key is correct and includes the `elastic:` prefix

### Port Already Allocated

If you see "port is already allocated" errors:
- This usually means start-local is already running
- Check running containers: `docker ps | grep -E "(es-local|kibana|edot-collector)"`
- You can use the existing start-local instance - no need to start docker-compose
- If you want to use docker-compose instead, stop start-local first

### Using Both Built-in and Custom Collectors

If you want to use your own collector while start-local is running:
- The built-in collector uses ports 4317-4318
- Configure your collector to use different ports (e.g., 4319-4320)
- Update your demo to use the custom endpoint: `python demo.py --otel-endpoint localhost:4319`
