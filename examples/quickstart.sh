#!/bin/bash
#
# HyperMemory Quick Start Example (Bash/cURL)
#
# This simple example shows the basics of using HyperMemory with curl.
#
# Usage:
#   export HYPERMEMORY_API_KEY=hm_live_xxx
#   ./quickstart.sh
#

API_KEY="${HYPERMEMORY_API_KEY:-YOUR_API_KEY_HERE}"
ENDPOINT="https://api.hypermemory.io/v1/mcp/sse"

echo "=================================================="
echo "HyperMemory Quick Start (cURL)"
echo "=================================================="

# Step 1: Get overview
echo ""
echo "1. Getting memory overview..."
curl -s -X POST "$ENDPOINT" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "memory_get_overview",
      "arguments": {}
    }
  }' | jq .

# Step 2: Store
echo ""
echo "2. Storing a memory..."
curl -s -X POST "$ENDPOINT" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/call",
    "params": {
      "name": "memory_store",
      "arguments": {
        "key": "quickstart_test_curl",
        "description": "Test from curl quickstart"
      }
    }
  }' | jq .

# Step 3: Recall
echo ""
echo "3. Recalling the memory..."
curl -s -X POST "$ENDPOINT" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "jsonrpc": "2.0",
    "id": 3,
    "method": "tools/call",
    "params": {
      "name": "memory_recall",
      "arguments": {
        "query": "quickstart"
      }
    }
  }' | jq .

# Step 4: Delete
echo ""
echo "4. Deleting the memory..."
curl -s -X POST "$ENDPOINT" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "jsonrpc": "2.0",
    "id": 4,
    "method": "tools/call",
    "params": {
      "name": "memory_forget",
      "arguments": {
        "key": "quickstart_test_curl"
      }
    }
  }' | jq .

echo ""
echo "=================================================="
echo "Quick Start Complete!"
echo "=================================================="
