<p align="center">
  <img src="hypermemory_mcp.svg" alt="HyperMemory MCP" width="250">
</p>

# HyperMemory MCP Integration

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MCP Compatible](https://img.shields.io/badge/MCP-2024--11--05-green.svg)](https://modelcontextprotocol.io)

Give your AI assistant **persistent memory** that lasts forever. HyperMemory remembers everything across conversations - user preferences, project details, decisions, and relationships between information.

## What is This?

This repository shows you how to connect HyperMemory to your AI tools using **MCP (Model Context Protocol)** - a standard way for AI assistants to use external tools.

**No coding required for most setups!**

## Quick Links

| Platform | Difficulty | Time to Setup |
|----------|------------|---------------|
| [Claude Desktop](#claude-desktop) | Easy | 5 minutes |
| [OpenAI / ChatGPT](#openai--chatgpt) | Medium | 10 minutes |
| [n8n](#n8n-workflow-automation) | Easy | 10 minutes |
| [CrewAI](#crewai) | Advanced | 15 minutes |
| [General MCP](#general-mcp-integration) | Varies | Varies |

---

## Before You Start

### Step 1: Get Your API Key

1. Go to [hypermemory.io](https://hypermemory.io) and sign up (it's free to start)
2. Click on **Dashboard** after logging in
3. Click **Create API Key**
4. Give it a name like "My AI Assistant"
5. Copy the key - it looks like `hm_live_abc123...`

> ⚠️ **Keep your API key secret!** Don't share it or put it in public code.

### Step 2: Note Your Gateway URL

Your HyperMemory gateway URL is:
```
https://api.hypermemory.io
```

That's it! Now pick your platform below.

---

## Claude Desktop

**Difficulty:** Easy | **Time:** 5 minutes

Claude Desktop has built-in MCP support. Here's how to add HyperMemory:

### Step-by-Step Instructions

1. **Find your Claude config file**
   
   - **Mac:** `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

2. **Open the file** in any text editor (TextEdit, Notepad, VS Code, etc.)

3. **Add this configuration** (replace `YOUR_API_KEY` with your actual key):

```json
{
  "mcpServers": {
    "hypermemory": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "https://api.hypermemory.io/v1/mcp/sse",
        "--header",
        "Authorization: Bearer YOUR_API_KEY"
      ]
    }
  }
}
```

4. **Save the file** and **restart Claude Desktop**

5. **Test it!** Ask Claude: *"What's in my memory?"*

### Troubleshooting

- **"Command not found"** - Make sure you have Node.js installed. Download it from [nodejs.org](https://nodejs.org)
- **"Connection refused"** - Check that your API key is correct
- **Claude doesn't see the tools** - Restart Claude Desktop completely

📖 [Detailed Claude setup guide](./claude/README.md)

---

## OpenAI / ChatGPT

**Difficulty:** Medium | **Time:** 10 minutes

OpenAI doesn't have native MCP support, but you can use HyperMemory through function calling or the Assistants API.

### Option A: Using the Assistants API (Recommended)

1. Go to [platform.openai.com/assistants](https://platform.openai.com/assistants)
2. Create a new Assistant
3. Enable **Functions** and add the HyperMemory tools
4. Use our [function definitions](./openai/functions.json)

### Option B: Using a Proxy Server

Run a simple bridge that translates between OpenAI and MCP:

```bash
# Install the bridge
npm install -g hypermemory-openai-bridge

# Run it (replace with your keys)
HYPERMEMORY_API_KEY=hm_live_xxx OPENAI_API_KEY=sk-xxx hypermemory-bridge
```

📖 [Detailed OpenAI setup guide](./openai/README.md)

---

## n8n Workflow Automation

**Difficulty:** Easy | **Time:** 10 minutes

n8n is a visual workflow automation tool. You can add HyperMemory as a custom node.

### Step-by-Step Instructions

1. **Open n8n** and create a new workflow

2. **Add an HTTP Request node** with these settings:
   - **Method:** POST
   - **URL:** `https://api.hypermemory.io/v1/mcp/sse`
   - **Authentication:** Bearer Token
   - **Token:** Your HyperMemory API key

3. **Set the body** (JSON):
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "memory_store",
    "arguments": {
      "key": "example",
      "description": "This is a test memory"
    }
  }
}
```

4. **Connect it** to your workflow and test!

### Pre-built Workflows

We've created ready-to-use workflows for common tasks:

- [Store user data from forms](./n8n/workflows/store-form-data.json)
- [Recall context for chatbots](./n8n/workflows/chatbot-context.json)
- [Sync with CRM systems](./n8n/workflows/crm-sync.json)

📖 [Detailed n8n setup guide](./n8n/README.md)

---

## CrewAI

**Difficulty:** Advanced | **Time:** 15 minutes

CrewAI lets you create teams of AI agents. Add HyperMemory to give your crew shared memory.

### Installation

```bash
pip install hypermemory-crewai
```

### Usage

```python
from crewai import Agent, Task, Crew
from hypermemory_crewai import HyperMemoryTool

# Create the memory tool
memory = HyperMemoryTool(
    api_key="hm_live_xxx",
    gateway_url="https://api.hypermemory.io"
)

# Create an agent with memory
researcher = Agent(
    role="Research Assistant",
    goal="Research topics and remember findings",
    tools=[memory.store, memory.recall, memory.find_related],
    verbose=True
)

# Create a task
task = Task(
    description="Research renewable energy trends and store key findings",
    agent=researcher
)

# Run the crew
crew = Crew(agents=[researcher], tasks=[task])
result = crew.kickoff()
```

📖 [Detailed CrewAI setup guide](./crewai/README.md)

---

## General MCP Integration

**Difficulty:** Varies | **Time:** Varies

If you're using a different platform or building your own integration, here's how MCP works with HyperMemory.

### What is MCP?

MCP (Model Context Protocol) is like a universal language for AI tools. It was created by Anthropic and lets AI assistants use external tools in a standard way.

Think of it like USB - before USB, every device had different connectors. MCP does the same thing for AI tools.

### How to Connect

HyperMemory supports the **Streamable HTTP Transport**:

- **Endpoint:** `https://api.hypermemory.io/v1/mcp/sse`
- **Method:** POST
- **Authentication:** Bearer token in the Authorization header
- **Format:** JSON-RPC 2.0

### Example Request

```bash
curl -X POST https://api.hypermemory.io/v1/mcp/sse \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer hm_live_xxx" \
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

📖 [Detailed MCP integration guide](./general/README.md)

---

## Available Memory Tools

HyperMemory provides these tools through MCP:

| Tool | What it Does | When to Use |
|------|--------------|-------------|
| `memory_store` | Save new information | User shares facts, preferences, or decisions |
| `memory_recall` | Search for information | Need context from past conversations |
| `memory_update` | Change existing information | Information has changed |
| `memory_forget` | Remove information | User asks to delete something |
| `memory_get_overview` | See what's stored | Start of conversation, check memory status |
| `memory_find_related` | Find connected info | Explore relationships between facts |
| `memory_add_relationships` | Connect information | Link related facts together |

### Tool Parameters

<details>
<summary><strong>memory_store</strong> - Save new information</summary>

```json
{
  "key": "user_name",           // Unique identifier (required)
  "description": "User's name is Alex",  // What this is (required)
  "data": {                     // Extra details (optional)
    "first_name": "Alex",
    "last_name": "Smith"
  },
  "relationships": [            // Connect to other memories (optional)
    {
      "nodes": ["user_name", "user_profile"],
      "relationship": "part_of"
    }
  ]
}
```
</details>

<details>
<summary><strong>memory_recall</strong> - Search for information</summary>

```json
{
  "query": "user preferences",  // What to search for (required)
  "max_results": 10,            // How many results (optional, default: 10)
  "max_depth": 2                // How far to follow connections (optional)
}
```
</details>

<details>
<summary><strong>memory_update</strong> - Change existing information</summary>

```json
{
  "key": "user_name",           // Which memory to update (required)
  "description": "User's name is Alexander",  // New description (optional)
  "data": {                     // New data (optional)
    "first_name": "Alexander"
  }
}
```
</details>

<details>
<summary><strong>memory_forget</strong> - Remove information</summary>

```json
{
  "key": "old_preference",      // Which memory to delete (required)
  "cascade": true               // Also remove connections (optional, default: true)
}
```
</details>

---

## Pricing

| Plan | Price | Queries/Month | Best For |
|------|-------|---------------|----------|
| **Free** | $0 | 10,000 | Trying it out |
| **Developer** | $29/mo | 50,000 | Personal projects |
| **Pro** | $99/mo | 500,000 | Production apps |
| **Enterprise** | Contact us | Unlimited | Large teams |

A "query" = any memory operation (store, recall, update, delete)

---

## Getting Help

- **Documentation:** [docs.hypermemory.io](https://docs.hypermemory.io)
- **Issues:** [GitHub Issues](https://github.com/RunStack-AI/hypermemory-mcp/issues)
- **Email:** support@hypermemory.io
- **Discord:** [Join our community](https://discord.gg/hypermemory)

## Contributing

Found a bug? Have an idea? We'd love your help!

1. Fork this repository
2. Make your changes
3. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE) for details.

---

Made with ❤️ by [RunStack AI](https://runstack.ai)
