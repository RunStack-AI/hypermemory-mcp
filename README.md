<p align="center">
  <img src="hypermemory_mcp.svg" alt="HyperMemory MCP" width="400" />
</p>

<p align="center">
  <a href="https://hypermemory.io">Website</a> &middot;
  <a href="https://app.hypermemory.io">Dashboard</a> &middot;
  <a href="https://github.com/RunStack-AI/hypermemory-mcp/issues">Issues</a>
</p>

# HyperMemory MCP Integration

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io)

Persistent, cross-conversation memory for AI assistants. HyperMemory stores knowledge as a **hypergraph** — nodes, edges, and hyperedges — so your AI remembers facts, preferences, decisions, and relationships between them.

This repository contains setup guides, skill files, and API references for connecting HyperMemory to your AI tools via **MCP (Model Context Protocol)**, the **CLI**, or the **REST API**.

---

## Quick Start

| Platform | Guide | Auth Method | Setup Time |
|----------|-------|-------------|------------|
| [Cursor IDE](cursor/) | MCP server | OAuth (automatic) | 2 min |
| [Claude Desktop / Code](claude/) | MCP server | OAuth or API key | 5 min |
| [CLI / Terminal Agents](cli/) | `hm` command | API key | 3 min |
| [REST API](api/) | HTTP endpoints | API key or JWT | 5 min |

### Step 1 — Get Credentials

1. Sign up at [hypermemory.io](https://hypermemory.io) (free tier available)
2. Go to [app.hypermemory.io/integration](https://app.hypermemory.io/integration)
3. For **MCP clients** (Cursor, Claude): use OAuth — no key needed, login happens in-browser
4. For **CLI or API**: create an API key — it starts with `hm_` followed by 64 hex characters

### Step 2 — Connect

Pick your platform from the table above and follow the guide.

### Step 3 — Install a Skill (optional but recommended)

Drop a [skill file](skills/) into your AI tool to teach it **when** and **how** to use memory automatically on every message.

---

## How It Works

HyperMemory exposes tools via MCP (Model Context Protocol) — an open standard for giving AI assistants access to external capabilities. Your AI calls tools like `hm_store` and `hm_recall` to read and write memory.

```
AI Assistant  --->  MCP (Streamable HTTP)  --->  HyperMemory Server
                    https://api.hypermemory.io/mcp
```

### Authentication

| Method | Use Case | How |
|--------|----------|-----|
| **OAuth 2.1 + PKCE** | MCP clients (Cursor, Claude, Windsurf) | Browser popup, automatic token management |
| **API Key** | CLI, REST API, server-to-server | `Authorization: Bearer hm_xxxx...` header |

OAuth is the primary method for interactive MCP clients. The server implements the full OAuth 2.1 Authorization Code flow with PKCE, dynamic client registration (RFC 7591), and authorization server metadata (RFC 8414). Identity is provided by Supabase Auth.

API keys start with `hm_` and are created in the [dashboard](https://app.hypermemory.io/integration). They can be scoped to a specific graph.

---

## Data Model

HyperMemory stores knowledge as a **hypergraph** with three primitives:

### Nodes

A node is a single piece of knowledge — a fact, person, decision, technology, preference, etc.

```json
{
  "key": "tech_redis",
  "description": "Redis is used for rate limiting, session caching, and OAuth code storage",
  "node_type": "technology",
  "data": { "version": "7.x" }
}
```

Every node has a unique `key` (format: `{type}_{name}`), a human-readable `description`, and an optional `data` object for structured metadata. The server generates vector embeddings from the description for semantic search.

### Edges (Binary Relationships)

An edge connects exactly two nodes with a described relationship.

```json
{
  "to_key": "tech_qdrant",
  "relationship": "search pipeline depends on Qdrant for vector similarity matching"
}
```

Relationships should be descriptive sentences, not single words. The server auto-summarizes long labels.

### Hyperedges (Group Relationships)

A hyperedge connects **3 or more nodes** that participate in a single indivisible relationship — like a project team, a tech stack, or a system architecture.

```json
{
  "participant_keys": ["project_api", "tech_fastapi", "tech_redis", "tech_postgres"],
  "relationship": "production API stack — all three are co-dependent"
}
```

Use the removal test: if removing any single participant still leaves the relationship intact, use binary edges instead.

### Node Types

```
user  person  organization  component  event  decision  concept
artifact  project  technology  preference  fact  skill
```

Plus system-level types: `location`, `group`, `product`, `asset`, `document`, `URL`.

### Multiple Graphs

Each account can have multiple isolated memory graphs. Pro plans get 4, Business gets 20, Enterprise is unlimited. Switch between them in the dashboard or via the `X-Graph-Id` header.

---

## MCP Tools

HyperMemory exposes **11 public MCP tools**. These are available to any connected MCP client.

| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `hm_store` | Save a new memory node | `key`, `description`, `node_type`, `data?`, `relationships?` |
| `hm_recall` | Search memory (hybrid: BM25 + vector + session) | `query`, `max_results?` (default 20) |
| `hm_update` | Modify an existing node | `key`, `description?`, `data?`, `node_type?` |
| `hm_forget` | Delete a node | `key`, `cascade?` (default true) |
| `hm_get_overview` | Graph stats and top nodes | `include_top_nodes?` (default 10) |
| `hm_find_related` | Traverse the graph from a seed node | `start_node`, `query?`, `max_nodes?`, `max_depth?` |
| `hm_ingest` | Decompose dense text into entities and edges (LLM) | `text`, `context?` |
| `hm_upload_file` | Upload a file to S3 with AI summary (Pro+) | `filename`, `content_base64`, `description?` |
| `hm_list_files` | Query uploaded files | `file_type?`, `search?`, `limit?` |
| `hm_timeline_write` | Write a diary entry to the timeline | `summary`, `meta?` |
| `hm_timeline` | Search past timeline events | `query?`, `period?`, `node_key?`, `start?`, `end?` |

### Search Pipeline

`hm_recall` runs a parallel hybrid search:

1. **Session cache** — recently accessed nodes, weighted by conversation phase
2. **BM25** — full-text search on node descriptions
3. **Vector** — semantic similarity via Qdrant embeddings
4. **Edge BM25** — full-text search on relationship labels
5. **Regex fallback** — pattern matching when other methods return nothing

Results are scored, deduplicated, and ranked by a composite of session relevance, topical fit, and general importance.

### Enrichment

Stored nodes are asynchronously enriched by a background worker that:
- Detects and creates relationships to existing nodes
- Classifies node types against the ontology
- Generates structured metadata
- Links nodes into relevant hyperedges

---

## Plans and Limits

| Plan | Price | Queries/mo | Graphs | File Storage |
|------|-------|------------|--------|--------------|
| **Free** | $0 | 2,000 | 1 | — |
| **Basic** | $8/mo | 10,000 | 1 | — |
| **Pro** | $15/mo | 200,000 | 4 | 1 GB |
| **Business** | $50/mo | 500,000 | 20 | 100 GB |
| **Enterprise** | Custom | Unlimited | Unlimited | 1 TB |

Annual billing saves ~17%. All paid plans include all MCP tools. File upload requires Pro or higher.

### Rate Limits

| Plan | API requests/min | Write tools/min | Ingest tools/min | Read tools/min |
|------|-----------------|-----------------|-------------------|----------------|
| Free | 60 | 10 | 3 | 30 |
| Basic | 120 | 20 | 5 | 60 |
| Pro | 300 | 60 | 15 | 120 |
| Business | 600 | 120 | 30 | 240 |
| Enterprise | Unlimited | 300 | 60 | 600 |

---

## Skill Files

Skill files teach your AI assistant **how** to use HyperMemory automatically. Drop one into your tool's configuration:

| File | For | MCP Server Name |
|------|-----|-----------------|
| [skills/hypermemory.md](skills/hypermemory.md) | Generic MCP client | `hypermemory` |
| [skills/cursor.md](skills/cursor.md) | Cursor IDE | `user-hypermemory` |
| [skills/cli.md](skills/cli.md) | Terminal agents (OpenClaw, etc.) | N/A (uses `hm` CLI) |
| [skills/chatgpt.txt](skills/chatgpt.txt) | ChatGPT custom instructions | N/A |

---

## Repository Structure

```
README.md           Overview, data model, tools, plans (this file)
cursor/             Cursor IDE setup guide
claude/             Claude Desktop & Claude Code setup guide
cli/                CLI installation and command reference
api/                REST API endpoint reference
skills/             Drop-in skill files for AI tools
LICENSE             MIT License
```

---

## Support

- **Issues:** [GitHub Issues](https://github.com/RunStack-AI/hypermemory-mcp/issues)
- **Email:** support@hypermemory.io
- **Dashboard:** [app.hypermemory.io](https://app.hypermemory.io)

## License

MIT — see [LICENSE](LICENSE).

---

Built by [RunStack AI](https://runstack.ai)
