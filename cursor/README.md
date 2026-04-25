# HyperMemory + Cursor IDE

Connect HyperMemory to Cursor as an MCP server. Cursor handles OAuth automatically — a browser window opens on first use, you log in, and tokens are managed for you.

## Setup

### Option A: OAuth (Recommended)

1. Open Cursor Settings (`Cmd+,` / `Ctrl+,`)
2. Go to **MCP** in the sidebar
3. Click **+ Add new MCP server**
4. Enter:
   - **Name:** `user-hypermemory`
   - **Type:** `streamableHttp` (or `sse`)
   - **URL:** `https://api.hypermemory.io/mcp`

Alternatively, add it to your project's `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "user-hypermemory": {
      "url": "https://api.hypermemory.io/mcp"
    }
  }
}
```

On first use, Cursor opens a browser window for Supabase Auth login. After authenticating, the MCP connection is established and tokens refresh automatically.

### Option B: API Key

If you prefer using an API key instead of OAuth:

1. Create an API key at [app.hypermemory.io/integration](https://app.hypermemory.io/integration)
2. Add to `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "user-hypermemory": {
      "url": "https://api.hypermemory.io/mcp",
      "headers": {
        "Authorization": "Bearer hm_YOUR_API_KEY_HERE"
      }
    }
  }
}
```

## Install the Skill File

The skill file teaches the AI to use memory **automatically on every message** — recalling context before responding and storing new information silently.

1. Create a `.cursor/rules/` directory in your project (if it doesn't exist)
2. Copy [skills/cursor.md](../skills/cursor.md) into `.cursor/rules/hypermemory.md`

Or download it directly:

```bash
mkdir -p .cursor/rules
curl -o .cursor/rules/hypermemory.md https://raw.githubusercontent.com/RunStack-AI/hypermemory-mcp/main/skills/cursor.md
```

The skill file configures the AI to:
- Call `hm_get_overview` and `hm_recall` at the start of every conversation
- Store new facts, decisions, and preferences automatically
- Use descriptive relationships and hyperedges for project groupings
- Never ask "should I save this?" — it just does it

## Verify It Works

Open Cursor's AI chat and ask:

> What's in my memory?

The assistant should call `hm_get_overview` and return your graph stats. If you see tool calls to `hm_*` functions, everything is connected.

## Troubleshooting

### MCP server shows as disconnected

- Check that the URL is exactly `https://api.hypermemory.io/mcp`
- If using OAuth, try removing and re-adding the server to trigger a fresh login
- If using an API key, verify it starts with `hm_` and hasn't been revoked

### OAuth login window doesn't appear

- Restart Cursor
- Ensure you have an account at [hypermemory.io](https://hypermemory.io)
- Check your browser isn't blocking popups from Cursor

### Tools appear but return errors

- Verify your plan hasn't exceeded its query limit at [app.hypermemory.io/usage](https://app.hypermemory.io/usage)
- If using a graph-scoped API key, ensure the graph isn't frozen (plan downgrade)

## Available Tools

Once connected, the AI has access to all 11 MCP tools:

| Tool | Purpose |
|------|---------|
| `hm_store` | Save a new memory node |
| `hm_recall` | Search memory (hybrid search) |
| `hm_update` | Modify an existing node |
| `hm_forget` | Delete a node |
| `hm_get_overview` | Graph stats and top nodes |
| `hm_find_related` | Traverse the graph from a node |
| `hm_ingest` | Decompose dense text into entities |
| `hm_upload_file` | Upload a file with AI summary (Pro+) |
| `hm_list_files` | Query uploaded files |
| `hm_timeline_write` | Write a diary entry |
| `hm_timeline` | Search timeline events |

See the [main README](../README.md) for full parameter details.
