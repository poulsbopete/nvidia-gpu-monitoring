# Start-Local Elastic Setup

This guide explains how to configure the demo to use a start-local Elastic instance with API key authentication.

## Configuration

The API key and endpoint are configured in `otel-collector-config.start-local.yaml`:

```yaml
elasticsearch:
  endpoints:
    - http://localhost:9200
  api_key: cS1LS0Fad0IweERGVE5FUFl6UFk6b3FDcm8zSExPMnhiMUh3YVlvZW42QQ==
```

## Running with Start-Local

1. **Start the OpenTelemetry Collector**:
   ```bash
   otelcol --config=otel-collector-config.start-local.yaml
   ```

2. **Run the demo application** (in a separate terminal):
   ```bash
   source venv/bin/activate
   python demo.py
   ```

## Updating the API Key

If you need to update the API key, edit `otel-collector-config.start-local.yaml`:

```yaml
elasticsearch:
  api_key: YOUR_NEW_API_KEY_HERE
```

## Verifying Connection

Test the Elasticsearch connection with API key:

```bash
curl -H "Authorization: ApiKey cS1LS0Fad0IweERGVE5FUFl6UFk6b3FDcm8zSExPMnhiMUh3YVlvZW42QQ==" \
  http://localhost:9200/_cluster/health
```

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
