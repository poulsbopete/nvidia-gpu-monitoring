# Start-Local Elastic Setup

This guide explains how to configure the demo to use a start-local Elastic instance with observability features enabled.

## Getting Started with Start-Local

### 1. Start Elastic with Observability

Run the start-local script with the `--edot` flag to enable Elastic Observability:

```bash
curl -fsSL https://elastic.co/start-local | sh -s -- --edot
```

This will:
- Start Elasticsearch with observability features
- Start Kibana
- Generate API keys automatically
- Display connection information including the API key

**Note**: The script will output important information including:
- Elasticsearch endpoint (typically `http://localhost:9200`)
- Kibana URL (typically `http://localhost:5601`)
- API key for authentication

### 2. Configure the OpenTelemetry Collector

After start-local completes, you'll need to update `otel-collector-config.start-local.yaml` with the API key that was generated:

```yaml
elasticsearch:
  endpoints:
    - http://localhost:9200
  api_key: YOUR_API_KEY_FROM_START_LOCAL_OUTPUT
```

The API key format from start-local will look like:
```
elastic:xxxxx==
```

Copy the entire API key (including the `elastic:` prefix) into the config file.

### 3. Start the OpenTelemetry Collector

```bash
otelcol --config=otel-collector-config.start-local.yaml
```

### 4. Run the demo application** (in a separate terminal):
   ```bash
   source venv/bin/activate
   python demo.py
   ```

## Updating the API Key

If you need to update the API key (e.g., after restarting start-local), edit `otel-collector-config.start-local.yaml`:

```yaml
elasticsearch:
  api_key: YOUR_API_KEY_FROM_START_LOCAL
```

**Getting the API Key from start-local:**
- The API key is displayed in the terminal output when you run the start-local script
- It's also available in the `.env` file created by start-local (if present)
- Format: `elastic:xxxxx==`

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
1. Verify start-local Elastic is running
2. Check the endpoint URL matches your Elastic instance
3. Ensure port 9200 is accessible
