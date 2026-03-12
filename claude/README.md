# HyperMemory + Claude Desktop

This guide walks you through setting up HyperMemory with Claude Desktop step by step.

## What You'll Get

After setup, Claude will be able to:
- ✅ Remember things you tell it across conversations
- ✅ Recall information from past chats
- ✅ Connect related pieces of information
- ✅ Forget information when you ask

## Requirements

- **Claude Desktop app** (download from [claude.ai/download](https://claude.ai/download))
- **Node.js** installed (download from [nodejs.org](https://nodejs.org) - the LTS version is fine)
- **A HyperMemory API key** (get one at [hypermemory.io](https://hypermemory.io))

## Step 1: Check Node.js is Installed

Open Terminal (Mac) or Command Prompt (Windows) and type:

```bash
node --version
```

You should see something like `v18.17.0` or higher. If you get an error, [download Node.js first](https://nodejs.org).

## Step 2: Find Your Claude Config File

### On Mac

1. Open Finder
2. Press `Cmd + Shift + G` (Go to Folder)
3. Paste this path: `~/Library/Application Support/Claude/`
4. Look for `claude_desktop_config.json`

If the file doesn't exist, create it.

### On Windows

1. Press `Win + R` (Run dialog)
2. Paste this path: `%APPDATA%\Claude\`
3. Look for `claude_desktop_config.json`

If the file doesn't exist, create it.

## Step 3: Edit the Config File

Open `claude_desktop_config.json` in any text editor.

### If the file is empty or doesn't exist

Copy and paste this entire block (replace `YOUR_API_KEY` with your real key):

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

### If the file already has content

Add the `hypermemory` section inside `mcpServers`. For example:

```json
{
  "mcpServers": {
    "some-other-tool": {
      "command": "...",
      "args": ["..."]
    },
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

## Step 4: Restart Claude

1. **Completely quit Claude** (not just close the window)
   - Mac: Click Claude in the menu bar → Quit Claude
   - Windows: Right-click Claude in system tray → Exit

2. **Open Claude Desktop again**

## Step 5: Test It Works

Ask Claude any of these:

> "What's in my memory?"

> "Remember that my favorite color is blue"

> "What do you remember about me?"

If Claude responds with information about your memory, it's working! 🎉

## Troubleshooting

### "npx: command not found"

Node.js isn't installed or isn't in your system PATH.

**Fix:** 
1. Download Node.js from [nodejs.org](https://nodejs.org)
2. Run the installer
3. Restart your computer
4. Try again

### "Connection refused" or "Unauthorized"

Your API key might be wrong.

**Fix:**
1. Go to [hypermemory.io/dashboard](https://hypermemory.io/dashboard)
2. Check your API key is correct
3. Make sure there are no extra spaces around the key

### Claude doesn't see any memory tools

The config file might have a syntax error.

**Fix:**
1. Make sure all quotes are straight quotes `"` not curly quotes `""`
2. Check for missing commas between items
3. Use a JSON validator like [jsonlint.com](https://jsonlint.com)

### "MCP server disconnected"

This can happen if your network connection is unstable.

**Fix:**
1. Check your internet connection
2. Restart Claude Desktop
3. Try again

## Example Conversations

Here are some things you can ask Claude to do with memory:

### Save Information
> "Remember that I'm working on a project called 'Solar Panel Dashboard' using Python and React"

### Recall Information  
> "What do you remember about my projects?"

### Connect Information
> "Link my 'Solar Panel Dashboard' project to my preference for React"

### Update Information
> "Update my Solar Panel project - we're now using Vue instead of React"

### Delete Information
> "Forget about the Solar Panel Dashboard project"

## Next Steps

- [Learn about memory key naming conventions](../general/naming-conventions.md)
- [See all available memory tools](../general/tool-reference.md)
- [Read the main documentation](../README.md)

---

Need help? [Open an issue](https://github.com/RunStack-AI/hypermemory-mcp/issues) or email support@hypermemory.io
