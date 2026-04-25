# HyperMemory REST API

All HyperMemory tools are available via REST endpoints at `https://api.hypermemory.io/api/v1/memory/`. These are the same operations exposed through MCP, accessible over plain HTTP for custom integrations.

## Authentication

All endpoints require a Bearer token in the `Authorization` header:

```
Authorization: Bearer hm_YOUR_API_KEY_HERE
```

The token can be either:
- An **API key** (starts with `hm_`) — created at [app.hypermemory.io/integration](https://app.hypermemory.io/integration)
- A **JWT** — obtained via the OAuth 2.1 flow

### Multi-Graph

To target a specific graph (if your account has multiple), include the graph ID header:

```
X-Graph-Id: graph_id_here
```

If omitted, requests go to the default graph.

---

## Endpoints

### Store a Node

```
POST /api/v1/memory/store
```

```bash
curl -X POST https://api.hypermemory.io/api/v1/memory/store \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer hm_YOUR_KEY" \
  -d '{
    "key": "tech_redis",
    "description": "Redis is used for rate limiting and session caching",
    "node_type": "technology",
    "data": {"version": "7.x"},
    "relationships": [
      {"to_key": "project_api", "relationship": "provides caching for the API layer"}
    ]
  }'
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `key` | string | yes | Unique node identifier (`{type}_{name}` format) |
| `description` | string | yes | Human-readable description (used for search and embeddings) |
| `node_type` | string | no | One of the supported node types |
| `data` | object | no | Structured metadata |
| `assets` | string[] | no | Asset references |
| `relationships` | object[] | no | Edges to create (see below) |

**Relationship object (binary edge):**
```json
{"to_key": "other_node", "relationship": "descriptive sentence about the connection"}
```

**Relationship object (hyperedge):**
```json
{"participant_keys": ["node_a", "node_b", "node_c"], "relationship": "description of group relationship"}
```

---

### Recall (Search)

```
POST /api/v1/memory/recall
```

```bash
curl -X POST https://api.hypermemory.io/api/v1/memory/recall \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer hm_YOUR_KEY" \
  -d '{
    "query": "user preferences for frontend frameworks",
    "max_results": 10
  }'
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `query` | string | yes | Search query (natural language) |
| `session_id` | string | no | Session identifier for context weighting (default: `"default"`) |
| `max_results` | int | no | Maximum results to return (default: 20) |
| `force_regex` | bool | no | Force regex-only search (default: false) |

---

### Update a Node

```
POST /api/v1/memory/update
```

```bash
curl -X POST https://api.hypermemory.io/api/v1/memory/update \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer hm_YOUR_KEY" \
  -d '{
    "key": "tech_redis",
    "description": "Redis 7.2 — now also used for pub/sub messaging"
  }'
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `key` | string | yes | Node to update |
| `description` | string | no | New description |
| `data` | object | no | New/merged metadata |
| `node_type` | string | no | Change the node type |

---

### Forget (Delete)

```
POST /api/v1/memory/forget
```

```bash
curl -X POST https://api.hypermemory.io/api/v1/memory/forget \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer hm_YOUR_KEY" \
  -d '{
    "key": "old_preference",
    "cascade": true
  }'
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `key` | string | yes | Node to delete |
| `cascade` | bool | no | Also remove connected edges (default: true) |

---

### Get Overview

```
GET /api/v1/memory/overview
```

```bash
curl https://api.hypermemory.io/api/v1/memory/overview \
  -H "Authorization: Bearer hm_YOUR_KEY"
```

Returns graph statistics: total nodes, node types, top nodes by connectivity.

---

### Find Related

```
POST /api/v1/memory/find-related
```

```bash
curl -X POST https://api.hypermemory.io/api/v1/memory/find-related \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer hm_YOUR_KEY" \
  -d '{
    "start_node": "tech_redis",
    "max_depth": 2,
    "max_nodes": 50
  }'
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `start_node` | string | yes | Node key to start traversal from |
| `query` | string | no | Filter results by relevance to query |
| `max_nodes` | int | no | Maximum nodes to return (default: 50) |
| `max_depth` | int | no | Maximum traversal depth |
| `relationship_pattern` | string | no | Filter by relationship pattern |
| `lens` | string | no | Traversal strategy hint |

---

### Ingest Text

```
POST /api/v1/memory/ingest
```

```bash
curl -X POST https://api.hypermemory.io/api/v1/memory/ingest \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer hm_YOUR_KEY" \
  -d '{
    "text": "The API uses FastAPI with Redis for caching and PostgreSQL for storage. JWT was chosen over sessions after a team discussion.",
    "context": "architecture meeting notes"
  }'
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `text` | string | yes | Dense text to decompose into entities and relationships |
| `context` | string | no | Label for the source context |

---

### Add Relationships

```
POST /api/v1/memory/relationships
```

```bash
curl -X POST https://api.hypermemory.io/api/v1/memory/relationships \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer hm_YOUR_KEY" \
  -d '{
    "relationships": [
      {"from_key": "tech_redis", "to_key": "project_api", "relationship": "provides session caching"}
    ]
  }'
```

---

### Get Relationships

```
GET /api/v1/memory/relationships/{key}
```

```bash
curl https://api.hypermemory.io/api/v1/memory/relationships/tech_redis \
  -H "Authorization: Bearer hm_YOUR_KEY"
```

Optional query parameter: `?pattern=caching` to filter by relationship text.

---

### Timeline Query

```
POST /api/v1/memory/timeline
```

```bash
curl -X POST https://api.hypermemory.io/api/v1/memory/timeline \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer hm_YOUR_KEY" \
  -d '{
    "query": "deployment",
    "period": "7d",
    "limit": 20
  }'
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `query` | string | no | Full-text search on timeline entries |
| `node_key` | string | no | Filter by associated node |
| `period` | string | no | Time period (`1h`, `3h`, `6h`, `12h`, `24h`, `3d`, `7d`, `14d`, `30d`, `90d`, `1y`) |
| `start` | string | no | ISO 8601 start date |
| `end` | string | no | ISO 8601 end date |
| `limit` | int | no | Max entries (default: 50) |

---

### Timeline Write

```
POST /api/v1/memory/timeline/write
```

```bash
curl -X POST https://api.hypermemory.io/api/v1/memory/timeline/write \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer hm_YOUR_KEY" \
  -d '{
    "summary": "Completed the database migration to PostgreSQL 16"
  }'
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `summary` | string | yes | Plain-language diary entry |
| `meta` | object | no | Optional metadata |

---

### Health Check

```
GET /api/v1/memory/health
```

```bash
curl https://api.hypermemory.io/api/v1/memory/health \
  -H "Authorization: Bearer hm_YOUR_KEY"
```

---

### Export Graph

```
GET /api/v1/memory/export
```

```bash
curl "https://api.hypermemory.io/api/v1/memory/export?include_ontology=true&include_session_data=false" \
  -H "Authorization: Bearer hm_YOUR_KEY"
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `include_ontology` | string | `"true"` | Include type definitions |
| `include_session_data` | string | `"false"` | Include session access data |

---

## Error Responses

| Status | Meaning |
|--------|---------|
| 401 | Invalid or missing API key / JWT |
| 403 | Graph is frozen (plan downgrade) or insufficient plan |
| 404 | Node not found |
| 429 | Rate limit exceeded |
| 500 | Server error |

Rate limit responses include `Retry-After` headers. See the [main README](../README.md) for plan-specific rate limits.
