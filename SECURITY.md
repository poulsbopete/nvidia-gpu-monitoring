# Security Guide

## API Keys and Secrets

**IMPORTANT**: Never commit API keys, passwords, or other sensitive credentials to this repository.

### Configuration Files

The following configuration files may contain sensitive data:
- `otel-collector-config.yaml` - OpenTelemetry Collector config (may contain Elasticsearch API keys)
- `otel-collector-config.local.yaml` - Local collector config (may contain API keys)
- `otel-collector-config.start-local.yaml` - Start-local collector config (uses placeholder)

### Using Configuration Files

1. **Template Files**: Use the `.example` files as templates:
   ```bash
   cp otel-collector-config.yaml.example otel-collector-config.yaml
   cp otel-collector-config.local.yaml.example otel-collector-config.local.yaml
   ```

2. **Add Your Secrets**: Edit the copied files and add your API keys locally. These files are in `.gitignore` and will not be committed.

3. **For Start-Local**: The `otel-collector-config.start-local.yaml` file uses a placeholder. After running start-local, update it with your API key from the start-local output.

### Start-Local API Keys

**Important Note**: When using Elastic start-local, API keys are ephemeral and are automatically destroyed when you stop the start-local instance. This means:
- Keys exposed in git history for start-local instances are not a permanent security risk
- However, it's still best practice to avoid committing them
- If a key is exposed, simply stopping and restarting start-local will generate a new key

### If You Accidentally Committed Secrets

If you've accidentally committed API keys or other secrets:

1. **For Start-Local Keys**: 
   - These are ephemeral and destroyed when start-local stops
   - Simply restart start-local to get a new key
   - No rotation needed, but still good practice to avoid committing them

2. **For Production Keys** (if applicable):
   - Immediately rotate the keys
   - Generate new API keys in Elasticsearch
   - Update all systems using the old keys
   - Revoke the old keys

3. **Remove from Git History** (if needed):
   ```bash
   # Option 1: Use git filter-branch (for small repos)
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch otel-collector-config.yaml otel-collector-config.local.yaml" \
     --prune-empty --tag-name-filter cat -- --all
   
   # Option 2: Use BFG Repo-Cleaner (recommended for large repos)
   # Download from: https://rtyley.github.io/bfg-repo-cleaner/
   bfg --replace-text secrets.txt
   
   # After cleaning, force push (WARNING: This rewrites history)
   git push origin --force --all
   ```

3. **Use GitGuardian or Similar Tools**: 
   - Set up secret scanning to prevent future leaks
   - Monitor your repository for exposed secrets

### Best Practices

- ✅ Use environment variables for secrets when possible
- ✅ Use `.example` or `.template` files for configs
- ✅ Add config files with secrets to `.gitignore`
- ✅ Use secret management tools (AWS Secrets Manager, HashiCorp Vault, etc.) in production
- ✅ Rotate keys regularly
- ❌ Never commit real API keys or passwords
- ❌ Never hardcode secrets in source code
- ❌ Don't share secrets in documentation or comments

### Current Status

As of the latest update:
- All hardcoded API keys have been removed from tracked files
- Template files (`.example`) are provided for reference
- Config files with placeholders are safe to commit
- Local config files are in `.gitignore`
- Start-local keys are ephemeral (destroyed when instance stops)
