# HyperMemory + n8n

This guide shows you how to add long-term memory to your n8n workflows.

## What is n8n?

n8n is a visual workflow automation tool - think "Zapier you can host yourself." It lets you connect different apps and automate tasks without writing code.

## What You'll Build

After this guide, you'll be able to:
- ✅ Store information from forms, emails, or any data source
- ✅ Recall context for AI chatbots
- ✅ Keep track of customer preferences
- ✅ Build memory-powered automations

## Before You Start

You'll need:
- n8n installed ([cloud](https://n8n.io) or [self-hosted](https://docs.n8n.io/hosting/))
- A HyperMemory API key from [hypermemory.io](https://hypermemory.io)

## Basic Setup

### Step 1: Create a New Workflow

1. Open n8n
2. Click **"New Workflow"**
3. Give it a name like "Memory Test"

### Step 2: Add an HTTP Request Node

This node will talk to HyperMemory.

1. Click **"+"** to add a node
2. Search for **"HTTP Request"**
3. Click to add it

### Step 3: Configure the Node

Fill in these settings:

| Setting | Value |
|---------|-------|
| **Method** | POST |
| **URL** | `https://api.hypermemory.io/v1/mcp/sse` |
| **Authentication** | Header Auth |
| **Name** | `Authorization` |
| **Value** | `Bearer YOUR_API_KEY` |
| **Body Content Type** | JSON |

### Step 4: Set the Request Body

For **storing** information:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "memory_store",
    "arguments": {
      "key": "customer_alice",
      "description": "Customer Alice prefers email communication"
    }
  }
}
```

For **recalling** information:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "memory_recall",
    "arguments": {
      "query": "customer preferences"
    }
  }
}
```

### Step 5: Test It

1. Click **"Test Node"**
2. You should see a successful response with your stored/recalled data

## Common Workflows

### Workflow 1: Store Customer Info from Forms

```
Webhook → Set (format data) → HTTP Request (store in HyperMemory)
```

**Webhook Node:**
- Create a webhook that receives form submissions

**Set Node:**
- Transform the form data:
```json
{
  "key": "customer_{{ $json.email }}",
  "description": "{{ $json.name }} submitted contact form",
  "data": {
    "name": "{{ $json.name }}",
    "email": "{{ $json.email }}",
    "message": "{{ $json.message }}"
  }
}
```

**HTTP Request Node:**
- Use the body template from Step 4, but use expressions:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "memory_store",
    "arguments": {{ $json }}
  }
}
```

### Workflow 2: AI Chatbot with Memory

```
Webhook → HTTP Request (recall) → OpenAI → HTTP Request (store) → Respond
```

1. **Receive message** via webhook
2. **Recall relevant context** from HyperMemory
3. **Generate response** with OpenAI (including context)
4. **Store important info** from the conversation
5. **Send response** back

### Workflow 3: Daily Summary Email

```
Schedule → HTTP Request (get overview) → Send Email
```

1. **Schedule Trigger:** Every day at 9 AM
2. **HTTP Request:** Get memory overview
3. **Email:** Send summary to yourself

## Tips & Tricks

### Use Dynamic Keys

Instead of hardcoding keys, use expressions:

```
customer_{{ $json.customer_id }}
project_{{ $json.project_name | lowercase | replace(' ', '_') }}
```

### Handle Errors

Add an **IF** node after the HTTP Request to check for errors:

```
{{ $json.error }} is not empty → Send alert
{{ $json.error }} is empty → Continue workflow
```

### Rate Limiting

HyperMemory allows many requests, but if you're processing lots of data:

1. Add a **Wait** node (0.1 seconds) between requests
2. Use **SplitInBatches** for bulk operations

## Pre-built Templates

Import these directly into n8n:

| Template | Description | Download |
|----------|-------------|----------|
| Memory Test | Simple store & recall | [store-test.json](./workflows/store-test.json) |
| Form Memory | Store form submissions | [form-memory.json](./workflows/form-memory.json) |
| Chat Context | Add memory to chatbots | [chat-context.json](./workflows/chat-context.json) |
| CRM Sync | Sync with customer data | [crm-sync.json](./workflows/crm-sync.json) |

### How to Import

1. Download the JSON file
2. In n8n, click **"..."** → **"Import from file"**
3. Select the downloaded file
4. Update your API key in the HTTP Request nodes

## Troubleshooting

### "401 Unauthorized"

Your API key is wrong or missing.

**Fix:** Check the Authorization header has `Bearer ` (with space) before your key.

### "Invalid JSON"

The body isn't valid JSON.

**Fix:** Use n8n's JSON editor and check for:
- Missing commas
- Extra commas at the end of lists
- Mismatched quotes

### "Connection Timeout"

n8n can't reach HyperMemory.

**Fix:** 
- Check your internet connection
- If self-hosting n8n, ensure outbound HTTPS is allowed

### Node Shows "No Data"

The response came back empty.

**Fix:** Check that you're using the right tool name and arguments. For `memory_recall`, make sure there's data stored first.

---

Need help? [Open an issue](https://github.com/RunStack-AI/hypermemory-mcp/issues)
