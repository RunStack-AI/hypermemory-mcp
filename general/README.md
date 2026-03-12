# General MCP Integration Guide

This guide explains how to integrate HyperMemory using the Model Context Protocol (MCP) in any platform or custom application.

## What is MCP?

**MCP (Model Context Protocol)** is a standard way for AI assistants to use external tools. Think of it like a common language that different AI systems can speak.

Before MCP, every AI platform had its own way of connecting to tools. Now, with MCP, you can build one integration that works across many platforms.

## How HyperMemory Uses MCP

HyperMemory implements the **Streamable HTTP Transport** variant of MCP. This means:

- You send HTTP POST requests
- You receive JSON responses
- It works with any programming language

## Connection Details

| Setting | Value |
|---------|-------|
| **Endpoint** | `https://api.hypermemory.io/v1/mcp/sse` |
| **Method** | POST |
| **Content-Type** | application/json |
| **Authentication** | Bearer token |

## Making Your First Request

### Step 1: Get an Overview

This checks what's in memory:

```bash
curl -X POST https://api.hypermemory.io/v1/mcp/sse \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "memory_get_overview",
      "arguments": {}
    }
  }'
```

### Step 2: Store Something

Save information to memory:

```bash
curl -X POST https://api.hypermemory.io/v1/mcp/sse \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/call",
    "params": {
      "name": "memory_store",
      "arguments": {
        "key": "test_memory",
        "description": "This is a test memory from the API"
      }
    }
  }'
```

### Step 3: Recall Information

Search for stored information:

```bash
curl -X POST https://api.hypermemory.io/v1/mcp/sse \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "jsonrpc": "2.0",
    "id": 3,
    "method": "tools/call",
    "params": {
      "name": "memory_recall",
      "arguments": {
        "query": "test"
      }
    }
  }'
```

## Understanding the Protocol

### Request Format

Every request follows this structure:

```json
{
  "jsonrpc": "2.0",          // Always "2.0"
  "id": 1,                    // Unique request ID (any number)
  "method": "tools/call",     // The MCP method
  "params": {
    "name": "memory_store",   // Which tool to call
    "arguments": {            // Tool parameters
      "key": "example",
      "description": "Example description"
    }
  }
}
```

### Response Format

Successful responses look like:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Successfully stored memory: example"
      }
    ]
  }
}
```

Error responses look like:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32600,
    "message": "Invalid request"
  }
}
```

## Available Tools

### memory_store

Save new information.

**Arguments:**
```json
{
  "key": "unique_key",           // Required: Unique identifier
  "description": "What this is", // Required: Human-readable description
  "data": {},                    // Optional: Additional structured data
  "relationships": []            // Optional: Links to other memories
}
```

### memory_recall

Search for information.

**Arguments:**
```json
{
  "query": "search terms",  // Required: What to search for
  "max_results": 10,        // Optional: Limit results (default: 10)
  "max_depth": 2            // Optional: How far to follow links
}
```

### memory_update

Change existing information.

**Arguments:**
```json
{
  "key": "existing_key",         // Required: Which memory to update
  "description": "New text",     // Optional: New description
  "data": {}                     // Optional: New/updated data
}
```

### memory_forget

Remove information.

**Arguments:**
```json
{
  "key": "key_to_delete",  // Required: Which memory to remove
  "cascade": true          // Optional: Also remove links (default: true)
}
```

### memory_get_overview

Get a summary of all stored information.

**Arguments:**
```json
{}  // No arguments needed
```

### memory_find_related

Find information connected to a specific memory.

**Arguments:**
```json
{
  "key": "starting_key",   // Required: Start from this memory
  "max_depth": 3           // Optional: How many links to follow
}
```

### memory_add_relationships

Connect memories together.

**Arguments:**
```json
{
  "edges": [
    {
      "nodes": ["key1", "key2"],        // Required: Keys to connect
      "relationship": "related_to",     // Required: Type of connection
      "data": {}                        // Optional: Extra info about link
    }
  ]
}
```

## Code Examples

### Python

```python
import requests
import json

API_KEY = "hm_live_xxx"
ENDPOINT = "https://api.hypermemory.io/v1/mcp/sse"

def call_memory(tool_name, arguments):
    response = requests.post(
        ENDPOINT,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        },
        json={
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            }
        }
    )
    return response.json()

# Store something
result = call_memory("memory_store", {
    "key": "user_preference",
    "description": "User prefers dark mode"
})
print(result)

# Recall it
result = call_memory("memory_recall", {
    "query": "user preference"
})
print(result)
```

### JavaScript / Node.js

```javascript
const API_KEY = "hm_live_xxx";
const ENDPOINT = "https://api.hypermemory.io/v1/mcp/sse";

async function callMemory(toolName, arguments) {
  const response = await fetch(ENDPOINT, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${API_KEY}`
    },
    body: JSON.stringify({
      jsonrpc: "2.0",
      id: 1,
      method: "tools/call",
      params: {
        name: toolName,
        arguments: arguments
      }
    })
  });
  return response.json();
}

// Store something
const storeResult = await callMemory("memory_store", {
  key: "user_preference",
  description: "User prefers dark mode"
});
console.log(storeResult);

// Recall it
const recallResult = await callMemory("memory_recall", {
  query: "user preference"
});
console.log(recallResult);
```

### Go

```go
package main

import (
    "bytes"
    "encoding/json"
    "fmt"
    "io"
    "net/http"
)

const (
    apiKey   = "hm_live_xxx"
    endpoint = "https://api.hypermemory.io/v1/mcp/sse"
)

type MCPRequest struct {
    JSONRPC string      `json:"jsonrpc"`
    ID      int         `json:"id"`
    Method  string      `json:"method"`
    Params  MCPParams   `json:"params"`
}

type MCPParams struct {
    Name      string                 `json:"name"`
    Arguments map[string]interface{} `json:"arguments"`
}

func callMemory(toolName string, arguments map[string]interface{}) (map[string]interface{}, error) {
    request := MCPRequest{
        JSONRPC: "2.0",
        ID:      1,
        Method:  "tools/call",
        Params: MCPParams{
            Name:      toolName,
            Arguments: arguments,
        },
    }

    body, _ := json.Marshal(request)
    req, _ := http.NewRequest("POST", endpoint, bytes.NewBuffer(body))
    req.Header.Set("Content-Type", "application/json")
    req.Header.Set("Authorization", "Bearer "+apiKey)

    client := &http.Client{}
    resp, err := client.Do(req)
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()

    responseBody, _ := io.ReadAll(resp.Body)
    var result map[string]interface{}
    json.Unmarshal(responseBody, &result)
    return result, nil
}

func main() {
    // Store something
    result, _ := callMemory("memory_store", map[string]interface{}{
        "key":         "user_preference",
        "description": "User prefers dark mode",
    })
    fmt.Println(result)
}
```

## Error Codes

| Code | Meaning | Solution |
|------|---------|----------|
| -32700 | Parse error | Check your JSON syntax |
| -32600 | Invalid request | Verify the request structure |
| -32601 | Method not found | Check the tool name |
| -32602 | Invalid params | Verify the arguments |
| -32603 | Internal error | Try again, contact support if persists |

## Best Practices

### 1. Use Descriptive Keys

```
✅ user_preference_theme
✅ project_alpha_status
✅ customer_john_notes

❌ pref1
❌ data
❌ stuff
```

### 2. Handle Errors Gracefully

Always check for errors in responses:

```python
result = call_memory("memory_recall", {"query": "test"})
if "error" in result:
    print(f"Error: {result['error']['message']}")
else:
    print(f"Success: {result['result']}")
```

### 3. Use Relationships

Connect related information for better recall:

```json
{
  "name": "memory_store",
  "arguments": {
    "key": "project_budget",
    "description": "Budget for Project Alpha is $50,000",
    "relationships": [
      {
        "nodes": ["project_budget", "project_alpha"],
        "relationship": "belongs_to"
      }
    ]
  }
}
```

### 4. Rate Limiting

While HyperMemory handles high loads, be respectful:
- Don't make more than 100 requests per second
- Cache responses when appropriate
- Batch operations when possible

---

Need help? [Open an issue](https://github.com/RunStack-AI/hypermemory-mcp/issues)
