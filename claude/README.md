# HyperMemory + Claude

Setup guides for Claude Desktop and Claude Code.

---

## Claude Desktop

Claude Desktop supports MCP servers natively. HyperMemory connects via Streamable HTTP transport.

### Option A: OAuth (Recommended)

Edit your Claude Desktop config file:

- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

Add the HyperMemory server:

```json
{
  "mcpServers": {
    "hypermemory": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "https://api.hypermemory.io/mcp"
      ]
    }
  }
}
```

On first use, a browser window opens for login via Supabase Auth. Tokens are cached and refreshed automatically by `mcp-remote`.

**Prerequisite:** Node.js must be installed. Download from [nodejs.org](https://nodejs.org) if `npx` is not available.

### Option B: API Key

If you prefer using an API key:

1. Create one at [app.hypermemory.io/integration](https://app.hypermemory.io/integration)
2. Use the key in the config:

```json
{
  "mcpServers": {
    "hypermemory": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "https://api.hypermemory.io/mcp",
        "--header",
        "Authorization: Bearer hm_YOUR_API_KEY_HERE"
      ]
    }
  }
}
```

### Adding to an Existing Config

If your config already has other MCP servers, add `hypermemory` alongside them:

```json
{
  "mcpServers": {
    "existing-server": {
      "command": "...",
      "args": ["..."]
    },
    "hypermemory": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "https://api.hypermemory.io/mcp"
      ]
    }
  }
}
```

After saving, **fully quit and restart Claude Desktop** (not just close the window).

---

## Claude Code (CLI)

Claude Code supports MCP servers via the `--mcp` flag or a config file.

### Add the MCP server

```bash
claude mcp add hypermemory --transport http --url https://api.hypermemory.io/mcp
```

Or with an API key:

```bash
claude mcp add hypermemory --transport http --url https://api.hypermemory.io/mcp \
  --header "Authorization: Bearer hm_YOUR_API_KEY_HERE"
```

### Install the Skill File

Copy [skills/hypermemory.md](../skills/hypermemory.md) to your project's `.claude/rules/` directory:

```bash
mkdir -p .claude/rules
curl -o .claude/rules/hypermemory.md https://raw.githubusercontent.com/RunStack-AI/hypermemory-mcp/main/skills/hypermemory.md
```

Or add it as a global CLAUDE.md instruction.

---

## Verify Setup

Ask Claude:

> What's in my memory?

You should see it call `hm_get_overview` and return your graph statistics (node count, types, top nodes).

## Troubleshooting

### "npx: command not found"

Node.js is not installed. Download it from [nodejs.org](https://nodejs.org) and restart your terminal.

### "Connection refused" or "Unauthorized"

- Check your API key is correct and starts with `hm_`
- Verify the URL is `https://api.hypermemory.io/mcp` (not `/v1/mcp/sse`)
- Try creating a fresh API key at [app.hypermemory.io/integration](https://app.hypermemory.io/integration)

### Claude doesn't see the tools

- Fully restart Claude Desktop (quit from the menu bar / system tray, then reopen)
- Check the config file for JSON syntax errors — use [jsonlint.com](https://jsonlint.com) to validate
- Ensure there are no curly quotes (" ") — only straight quotes (" ")

### OAuth login loop

- Clear the `mcp-remote` cache: `rm -rf ~/.mcp-auth`
- Restart Claude Desktop and try again

## Available Tools

Once connected, Claude has access to all 11 HyperMemory tools. See the [main README](../README.md) for the full tool reference.

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
