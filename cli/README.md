# HyperMemory CLI

The `hm` command-line tool gives terminal-based agents and developers direct access to HyperMemory. It communicates with the server via the REST API using an API key.

## Installation

```bash
pip install hypermemory-cli
```

Verify:

```bash
hm version
```

## Authentication

### Option A: API Key (Recommended for CLI)

1. Create an API key at [app.hypermemory.io/integration](https://app.hypermemory.io/integration)
2. Configure the CLI:

```bash
hm config --set-key hm_YOUR_API_KEY_HERE
```

Or set it as an environment variable:

```bash
export HYPERMEMORY_API_KEY=hm_YOUR_API_KEY_HERE
```

The config file is stored at `~/.config/hypermemory/config.json`.

**Priority order:** environment variable > config file.

### Option B: OAuth Login

For interactive use, you can authenticate via browser:

```bash
hm login
```

This opens a browser window for Supabase Auth login using OAuth 2.1 + PKCE. Tokens are saved to the config file and refreshed automatically on 401 responses.

To log out:

```bash
hm logout
```

### Custom Server URL

To point at a different server (e.g. self-hosted):

```bash
hm config --set-url https://your-server.example.com
```

Default: `https://api.hypermemory.io`

## Command Reference

### Core Memory Operations

#### `hm overview`

Get graph statistics — node count, types, and top nodes.

```bash
hm overview
```

#### `hm recall <query>`

Search memory using hybrid search (BM25 + vector + session context).

```bash
hm recall "user preferences for frontend frameworks"
```

#### `hm store <key> <description> --type <TYPE>`

Store a new memory node. `--type` is required.

```bash
hm store tech_redis "Redis is used for rate limiting and session caching" --type technology
```

With optional structured data:

```bash
hm store tech_redis "Redis 7.x for caching" --type technology \
  --data '{"version": "7.x", "role": "cache"}'
```

With relationships:

```bash
hm store tech_redis "Redis for caching" --type technology \
  --rels '[{"to_key": "project_api", "relationship": "provides session caching for the API"}]'
```

#### `hm update <key>`

Update an existing node's description, type, or data.

```bash
hm update tech_redis --desc "Redis 7.2 — now also used for pub/sub"
hm update tech_redis --type technology --data '{"version": "7.2"}'
```

#### `hm forget <key>`

Delete a node. Use `--cascade` to also remove connected edges.

```bash
hm forget old_preference
hm forget old_preference --cascade
```

#### `hm ingest <text>`

Send dense text to the server for LLM-powered decomposition into entities and relationships.

```bash
hm ingest "The API is built with FastAPI, uses Redis for caching, and PostgreSQL for storage. The team decided on JWT auth after evaluating session-based alternatives."
```

With an optional context label:

```bash
hm ingest "..." --context "architecture meeting notes"
```

### Graph Traversal

#### `hm find <key>`

Traverse the graph from a starting node to discover related information.

```bash
hm find tech_redis
hm find tech_redis --depth 3
```

#### `hm relationships <key>`

List all edges connected to a node.

```bash
hm relationships tech_redis
```

#### `hm relate`

Create a relationship between two nodes.

```bash
hm relate --from tech_redis --to project_api --rel "provides session caching"
```

### Timeline

#### `hm timeline`

Query the activity timeline. Supports filtering by query, time period, node, or date range.

```bash
hm timeline
hm timeline --query "deployment"
hm timeline --period 24h
hm timeline --period 7d --limit 20
hm timeline --start 2025-01-01 --end 2025-01-31
hm timeline --node tech_redis
```

Period values: `1h`, `3h`, `6h`, `12h`, `24h`, `3d`, `7d`, `14d`, `30d`, `90d`, `1y`.

#### `hm timeline-write <summary>`

Write a manual diary entry to the timeline.

```bash
hm timeline-write "Completed the database migration to PostgreSQL 16"
```

### System

#### `hm health`

Check server connectivity.

```bash
hm health
```

#### `hm export`

Export the full graph as JSON. Use `--no-ontology` to exclude type definitions.

```bash
hm export
hm export --no-ontology
```

#### `hm config`

View or update CLI configuration.

```bash
hm config                           # Show current config
hm config --set-key hm_xxxx        # Set API key
hm config --set-url https://...    # Set server URL
```

#### `hm login` / `hm logout`

OAuth browser login and token cleanup.

```bash
hm login
hm logout
```

#### `hm version`

Print the CLI version.

```bash
hm version
```

## Full Command Summary

| Command | Purpose |
|---------|---------|
| `hm overview` | Graph stats and top nodes |
| `hm recall "query"` | Search memory |
| `hm store KEY "desc" --type TYPE` | Store new information |
| `hm ingest "text"` | Decompose text into entities |
| `hm update KEY --desc "..."` | Update existing node |
| `hm forget KEY` | Delete a node |
| `hm relate --from A --to B --rel "..."` | Create a relationship |
| `hm find KEY` | Graph traversal |
| `hm relationships KEY` | List edges for a node |
| `hm timeline` | Query timeline events |
| `hm timeline-write "..."` | Write a diary entry |
| `hm health` | Check server status |
| `hm export` | Export full graph |
| `hm config` | View/set configuration |
| `hm login` | OAuth browser login |
| `hm logout` | Clear OAuth tokens |
| `hm version` | Print version |

## Using with Terminal Agents

The CLI is designed for agentic systems like [OpenClaw](https://github.com/RunStack-AI/openclaw) that run in a terminal. Install the [CLI skill file](../skills/cli.md) to teach the agent how to use `hm` commands on every message.

**Environment setup for agents:**

```bash
export HYPERMEMORY_API_KEY=hm_YOUR_KEY
```

The agent's skill instructs it to:
1. Run `hm overview` + `hm recall` at the start of every conversation
2. Store new information with `hm store` automatically
3. Use `hm recall` before storing to avoid duplicates

## API Endpoint

The CLI sends requests to `{api_url}/api/v1/memory/*`. All commands map to REST endpoints — see the [API reference](../api/) for details.
