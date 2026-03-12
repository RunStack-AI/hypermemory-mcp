# HyperMemory Tool Reference

Complete reference for all HyperMemory MCP tools.

## Overview

HyperMemory provides 7 core tools for managing persistent memory:

| Tool | Purpose | Common Use Case |
|------|---------|-----------------|
| `memory_store` | Save new information | User shares facts |
| `memory_recall` | Search for information | Find past context |
| `memory_update` | Change existing info | Correct or update data |
| `memory_forget` | Delete information | Remove outdated data |
| `memory_get_overview` | Summarize memory | Start of conversation |
| `memory_find_related` | Find connections | Explore relationships |
| `memory_add_relationships` | Link memories | Connect related info |

---

## memory_store

Save new information to memory.

### When to Use

- User shares personal information (name, preferences)
- Important decisions are made
- Facts need to be remembered for later
- Creating notes about projects or tasks

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `key` | string | Yes | Unique identifier (snake_case) |
| `description` | string | Yes | Human-readable summary |
| `data` | object | No | Additional structured data |
| `relationships` | array | No | Links to other memories |

### Example Request

```json
{
  "name": "memory_store",
  "arguments": {
    "key": "user_preference_theme",
    "description": "User prefers dark mode for all applications",
    "data": {
      "theme": "dark",
      "updated": "2024-03-15"
    }
  }
}
```

### Example Response

```json
{
  "content": [
    {
      "type": "text",
      "text": "Stored memory: user_preference_theme"
    }
  ]
}
```

---

## memory_recall

Search for information in memory.

### When to Use

- Need context from previous conversations
- Looking for specific facts
- Starting a conversation (check what's known)
- Answering questions that require past information

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `query` | string | Yes | Search terms or question |
| `max_results` | integer | No | Maximum results (default: 10) |
| `max_depth` | integer | No | Relationship depth (default: 2) |

### Example Request

```json
{
  "name": "memory_recall",
  "arguments": {
    "query": "user preferences",
    "max_results": 5
  }
}
```

### Example Response

```json
{
  "content": [
    {
      "type": "text",
      "text": "Found 2 relevant memories:\n\n1. user_preference_theme: User prefers dark mode\n2. user_preference_language: User prefers English"
    }
  ]
}
```

---

## memory_update

Modify existing information.

### When to Use

- Information has changed
- Need to correct a mistake
- Adding more details to existing memory
- Updating outdated facts

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `key` | string | Yes | Key of memory to update |
| `description` | string | No | New description |
| `data` | object | No | New/updated data |

### Example Request

```json
{
  "name": "memory_update",
  "arguments": {
    "key": "user_preference_theme",
    "description": "User now prefers light mode",
    "data": {
      "theme": "light",
      "updated": "2024-03-16"
    }
  }
}
```

### Example Response

```json
{
  "content": [
    {
      "type": "text",
      "text": "Updated memory: user_preference_theme"
    }
  ]
}
```

---

## memory_forget

Remove information from memory.

### When to Use

- User requests deletion
- Information is no longer relevant
- Cleaning up old/incorrect data
- Privacy requests

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `key` | string | Yes | Key of memory to delete |
| `cascade` | boolean | No | Remove connected edges (default: true) |

### Example Request

```json
{
  "name": "memory_forget",
  "arguments": {
    "key": "old_project_notes",
    "cascade": true
  }
}
```

### Example Response

```json
{
  "content": [
    {
      "type": "text",
      "text": "Deleted memory: old_project_notes (and 3 relationships)"
    }
  ]
}
```

---

## memory_get_overview

Get a summary of all stored information.

### When to Use

- Starting a new conversation
- Understanding what's available
- Debugging memory contents
- Getting a high-level view

### Arguments

None required.

### Example Request

```json
{
  "name": "memory_get_overview",
  "arguments": {}
}
```

### Example Response

```json
{
  "content": [
    {
      "type": "text",
      "text": "Memory Overview:\n\nTotal memories: 15\nTotal relationships: 8\n\nCategories:\n- user_*: 5 memories\n- project_*: 7 memories\n- config_*: 3 memories\n\nRecent:\n- user_name (updated 2h ago)\n- project_alpha_status (updated 1d ago)"
    }
  ]
}
```

---

## memory_find_related

Find memories connected to a specific key.

### When to Use

- Exploring connections between facts
- Understanding context around a topic
- Finding all information about a subject
- Building comprehensive understanding

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `key` | string | Yes | Starting memory key |
| `max_depth` | integer | No | How far to follow links (default: 3) |

### Example Request

```json
{
  "name": "memory_find_related",
  "arguments": {
    "key": "project_alpha",
    "max_depth": 2
  }
}
```

### Example Response

```json
{
  "content": [
    {
      "type": "text",
      "text": "Related to project_alpha:\n\nDirect connections:\n- project_alpha_deadline (deadline)\n- project_alpha_team (team)\n- customer_acme (client)\n\n2nd degree:\n- user_john (team member)\n- customer_acme_contacts (via customer_acme)"
    }
  ]
}
```

---

## memory_add_relationships

Create connections between memories.

### When to Use

- Linking related information
- Building knowledge graphs
- Connecting people to projects
- Creating hierarchies

### Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `edges` | array | Yes | List of relationships to create |

Each edge object:

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `nodes` | array[2] | Yes | Two memory keys to connect |
| `relationship` | string | Yes | Type of relationship |
| `data` | object | No | Metadata about relationship |

### Common Relationship Types

- `related_to` - General association
- `part_of` - Belongs to / contained in
- `depends_on` - Requires / needs
- `leads_to` - Results in / causes
- `belongs_to` - Ownership
- `works_on` - Person-project relationship
- `reports_to` - Hierarchy

### Example Request

```json
{
  "name": "memory_add_relationships",
  "arguments": {
    "edges": [
      {
        "nodes": ["user_john", "project_alpha"],
        "relationship": "works_on",
        "data": {
          "role": "lead developer",
          "since": "2024-01-15"
        }
      },
      {
        "nodes": ["project_alpha", "customer_acme"],
        "relationship": "belongs_to"
      }
    ]
  }
}
```

### Example Response

```json
{
  "content": [
    {
      "type": "text",
      "text": "Created 2 relationships:\n- user_john --[works_on]--> project_alpha\n- project_alpha --[belongs_to]--> customer_acme"
    }
  ]
}
```

---

## Error Handling

### Common Error Codes

| Code | Meaning | Solution |
|------|---------|----------|
| -32602 | Invalid params | Check required arguments |
| -32603 | Internal error | Try again, contact support |
| 404 | Key not found | Verify the key exists |
| 409 | Key already exists | Use `memory_update` instead |

### Error Response Format

```json
{
  "error": {
    "code": -32602,
    "message": "Invalid params: 'key' is required"
  }
}
```

---

## Best Practices

1. **Always check overview first** - Use `memory_get_overview` at conversation start
2. **Use descriptive keys** - Follow [naming conventions](./naming-conventions.md)
3. **Create relationships** - Connect related memories for better recall
4. **Update, don't duplicate** - Use `memory_update` for existing keys
5. **Clean up regularly** - Remove outdated information with `memory_forget`

---

Need help? [Open an issue](https://github.com/RunStack-AI/hypermemory-mcp/issues)
