#!/bin/bash
# Helper script to find start-local API key

echo "Checking for start-local API key..."
echo ""

# Check if start-local containers are running
if docker ps | grep -q "es-local-dev"; then
    echo "✓ start-local Elastic is running"
    echo ""
    echo "The API key was displayed when you ran:"
    echo "  curl -fsSL https://elastic.co/start-local | sh -s -- --edot"
    echo ""
    echo "If you can't find it in your terminal history, you can:"
    echo "1. Check the terminal where you ran start-local"
    echo "2. Look for a line containing 'elastic:' followed by a long string"
    echo "3. Or restart start-local to see the API key again"
    echo ""
    echo "To restart and see the API key:"
    echo "  # Stop current instance (if needed)"
    echo "  # Then run: curl -fsSL https://elastic.co/start-local | sh -s -- --edot"
else
    echo "start-local Elastic is not running"
    echo "Start it with: curl -fsSL https://elastic.co/start-local | sh -s -- --edot"
fi
