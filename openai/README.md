# HyperMemory + OpenAI / ChatGPT

This guide shows you how to use HyperMemory with OpenAI's APIs.

## Understanding the Challenge

OpenAI doesn't natively support MCP (Model Context Protocol). That means we need to use one of these approaches:

| Approach | Difficulty | Best For |
|----------|------------|----------|
| [Function Calling](#option-1-function-calling) | Medium | Custom apps |
| [Assistants API](#option-2-assistants-api) | Easy | Quick setup |
| [Bridge Server](#option-3-bridge-server) | Advanced | Full MCP support |

## Option 1: Function Calling

Use OpenAI's function calling feature to make your app talk to HyperMemory.

### How It Works

```
Your App → OpenAI API → Function Call → Your App → HyperMemory API
```

When OpenAI decides to use a function, you handle the call and forward it to HyperMemory.

### Step 1: Define the Functions

Add these function definitions to your OpenAI API calls:

```javascript
const functions = [
  {
    name: "memory_store",
    description: "Store information in long-term memory for later recall",
    parameters: {
      type: "object",
      properties: {
        key: {
          type: "string",
          description: "Unique identifier for this memory (use snake_case)"
        },
        description: {
          type: "string", 
          description: "Human-readable description of what this memory contains"
        },
        data: {
          type: "object",
          description: "Additional structured data to store"
        }
      },
      required: ["key", "description"]
    }
  },
  {
    name: "memory_recall",
    description: "Search memory for relevant information",
    parameters: {
      type: "object",
      properties: {
        query: {
          type: "string",
          description: "What to search for in memory"
        },
        max_results: {
          type: "integer",
          description: "Maximum number of results to return (default: 10)"
        }
      },
      required: ["query"]
    }
  },
  {
    name: "memory_get_overview",
    description: "Get a summary of what's currently stored in memory",
    parameters: {
      type: "object",
      properties: {}
    }
  }
];
```

See [functions.json](./functions.json) for the complete list.

### Step 2: Handle Function Calls

When OpenAI returns a function call, forward it to HyperMemory:

```javascript
async function handleFunctionCall(functionName, arguments) {
  const response = await fetch('https://api.hypermemory.io/v1/mcp/sse', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${process.env.HYPERMEMORY_API_KEY}`
    },
    body: JSON.stringify({
      jsonrpc: "2.0",
      id: Date.now(),
      method: "tools/call",
      params: {
        name: functionName,
        arguments: arguments
      }
    })
  });
  
  const data = await response.json();
  return data.result;
}
```

### Step 3: Complete Example

```javascript
import OpenAI from 'openai';

const openai = new OpenAI();

async function chat(userMessage) {
  const response = await openai.chat.completions.create({
    model: "gpt-4",
    messages: [{ role: "user", content: userMessage }],
    functions: functions,
    function_call: "auto"
  });

  const message = response.choices[0].message;

  // Check if the model wants to call a function
  if (message.function_call) {
    const functionName = message.function_call.name;
    const args = JSON.parse(message.function_call.arguments);
    
    // Call HyperMemory
    const result = await handleFunctionCall(functionName, args);
    
    // Send the result back to get a final response
    const finalResponse = await openai.chat.completions.create({
      model: "gpt-4",
      messages: [
        { role: "user", content: userMessage },
        message,
        { role: "function", name: functionName, content: JSON.stringify(result) }
      ]
    });
    
    return finalResponse.choices[0].message.content;
  }

  return message.content;
}
```

## Option 2: Assistants API

OpenAI Assistants can use function tools with persistent threads.

### Step 1: Create an Assistant

```javascript
const assistant = await openai.beta.assistants.create({
  name: "Memory Assistant",
  instructions: "You are a helpful assistant with long-term memory capabilities. Use the memory tools to store and recall information about the user.",
  model: "gpt-4-turbo",
  tools: [
    {
      type: "function",
      function: {
        name: "memory_store",
        description: "Store information in long-term memory",
        parameters: {
          type: "object",
          properties: {
            key: { type: "string" },
            description: { type: "string" }
          },
          required: ["key", "description"]
        }
      }
    },
    {
      type: "function",
      function: {
        name: "memory_recall",
        description: "Search memory",
        parameters: {
          type: "object",
          properties: {
            query: { type: "string" }
          },
          required: ["query"]
        }
      }
    }
  ]
});
```

### Step 2: Handle Tool Calls

When running the assistant, check for required actions:

```javascript
const run = await openai.beta.threads.runs.create(threadId, {
  assistant_id: assistantId
});

// Poll for completion
let runStatus = await openai.beta.threads.runs.retrieve(threadId, run.id);

while (runStatus.status !== 'completed') {
  if (runStatus.status === 'requires_action') {
    const toolCalls = runStatus.required_action.submit_tool_outputs.tool_calls;
    
    const toolOutputs = await Promise.all(
      toolCalls.map(async (call) => ({
        tool_call_id: call.id,
        output: JSON.stringify(
          await handleFunctionCall(call.function.name, JSON.parse(call.function.arguments))
        )
      }))
    );
    
    await openai.beta.threads.runs.submitToolOutputs(threadId, run.id, {
      tool_outputs: toolOutputs
    });
  }
  
  await sleep(1000);
  runStatus = await openai.beta.threads.runs.retrieve(threadId, run.id);
}
```

## Option 3: Bridge Server

Run a local server that bridges OpenAI and MCP. This gives you full MCP compatibility.

### Installation

```bash
npm install -g @hypermemory/openai-bridge
```

### Running

```bash
HYPERMEMORY_API_KEY=hm_live_xxx hypermemory-openai-bridge --port 3000
```

### Using

Point your OpenAI calls to the bridge:

```javascript
const openai = new OpenAI({
  baseURL: 'http://localhost:3000/v1'  // Bridge server
});

// Now use OpenAI normally - memory is handled automatically
```

## Files in This Directory

- `functions.json` - Complete function definitions for all memory tools
- `example-chat.js` - Full working example with function calling
- `example-assistant.js` - Full working example with Assistants API

## Troubleshooting

### "Invalid function call"

OpenAI didn't format the function call correctly.

**Fix:** Make sure your function definitions match the expected schema exactly.

### "Rate limit exceeded"

Too many calls to either OpenAI or HyperMemory.

**Fix:** Add retry logic with exponential backoff.

### Functions aren't being called

The model might not understand when to use memory.

**Fix:** Be more explicit in your system prompt:

```javascript
const systemPrompt = `You have access to persistent memory. 
ALWAYS use memory_recall at the start of a conversation.
ALWAYS use memory_store when the user shares personal information.`;
```

---

Need help? [Open an issue](https://github.com/RunStack-AI/hypermemory-mcp/issues)
