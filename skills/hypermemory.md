---
name: hypermemory
version: 0.5.2
enforcement: mandatory
trigger: every_turn
---

# HYPERMEMORY — MANDATORY ON EVERY SINGLE MESSAGE

YOU MUST EXECUTE THIS PROTOCOL ON EVERY MESSAGE. NO EXCEPTIONS.

You have the `hypermemory` MCP server connected. Use its tools directly.

---

## FIRST MESSAGE — RECALL MEMORY

BEFORE you write a single word, call these MCP tools:

1. `hm_get_overview` — see what exists in memory
2. `hm_recall` with query keywords from the user's message

If memory returns information about the user or topic — USE IT.
Do not ask what you already know. Do not introduce yourself as if you have never met.

## EVERY MESSAGE — STORE NEW INFORMATION

After reading the user's message, store meaningful new information silently.

1. Call `hm_recall` first to check if it exists
2. If new: call `hm_store` with `key`, `description`, and `node_type`
3. If exists: call `hm_update` to modify it

### What to store:
- Decisions and their rationale
- User preferences and working style
- People, their roles, and relationships
- Projects, tech stacks, and status
- Architecture choices and bug fixes
- Important facts and data points
- Skills and expertise

### What NOT to store:
- Trivial acknowledgements ("ok", "thanks", "sounds good")
- Information already in memory (update instead)
- Conversation mechanics

---

## RULES

NEVER:
- Skip memory operations on any message
- Respond before calling `hm_get_overview` + `hm_recall` on the first message
- Ask "should I save this?" — just save it
- Announce "I've stored that" — do it silently
- Store without `node_type`
- Create a duplicate when you should update

ALWAYS:
- `hm_get_overview` + `hm_recall` BEFORE your first response
- `hm_recall` before `hm_store` to check for existing nodes
- Set `node_type` on every store
- Use recalled memory naturally — never say "according to my memory"
- Maintain the `user_profile` node — store the user's name, role, preferences there

---

## NODE TYPES

```
user person organization component event decision concept artifact
project technology preference fact skill
```

## RELATIONSHIPS

When storing, describe connections in plain language. Be specific about WHY.

```json
{"relationships": [{"to_key": "tech_qdrant", "relationship": "search pipeline depends on Qdrant for vector similarity"}]}
```

BAD: `"depends_on"`
BAD: `"uses"`
GOOD: `"search pipeline depends on Qdrant for vector similarity matching"`
GOOD: `"Ken chose SvelteKit for the frontend because it supports SSR and progressive enhancement"`

The server automatically summarizes long labels for readability.

## HYPEREDGES — GROUP NODES BY PROJECT

When the user is working on a project, create a **hyperedge** to group all related nodes together.
A hyperedge connects 3+ nodes that share a common context (a project, an initiative, a system).

When storing a node that belongs to a project, include a hyperedge relationship:

```json
{
  "relationships": [
    {
      "relationship": "components of the HyperMemory platform",
      "participant_keys": ["project_hypermemory", "tech_surrealdb", "tech_qdrant", "tech_redis", "component_mcp_server"]
    }
  ]
}
```

- Use `participant_keys` (array of 3+ keys) instead of `to_key` to create a hyperedge
- The project node itself should be one of the participants
- Add new participants to existing hyperedges as you discover them
- Every project-scoped node (tech choices, decisions, components, people) should be linked via the project hyperedge

**When to create a hyperedge:**
- User mentions a project by name and discusses its parts
- Multiple nodes clearly belong to the same initiative or system
- A decision, technology, or person is tied to a specific project

## KEY FORMAT

`{type}_{name}` — e.g. `decision_jwt_auth`, `person_alice`, `tech_redis`, `pref_dark_mode`

Special: `user_profile` — singleton node for the primary user.

## FILE STORAGE (Pro, Business, Enterprise, RunStack plans)

When the user wants to store a file in HyperMemory, use `hm_upload_file`:

```json
{
  "filename": "architecture.pdf",
  "content_base64": "<base64-encoded file content>",
  "description": "Optional custom description",
  "node_key": "optional_existing_node_to_link"
}
```

- Supported: pdf, doc/x, ppt/x, xls/x, csv, txt, md, rdf, jpg, png, gif, webp, mp3, wav, ogg, mp4, webm, mov
- Server uploads to S3, creates a graph node with AI summary, and links it
- Use `hm_list_files` to query stored files (filter by type, search by name)
- Limits: Pro 1GB, Business 100GB, Enterprise 1TB, RunStack 10GB
- Only upload when user explicitly asks to store the file

## TIMELINE DIARY (optional)

The **timeline** auto-records meaningful activity; it is **not** in default context. Use
`hm_timeline_write` for a rare plain-language line the graph does not cover; use
`hm_timeline` for temporal lookback (`query`, `period`, `node_key`, dates). Do not spam.

## MCP TOOL REFERENCE

| Tool | When |
|------|------|
| `hm_get_overview` | First message |
| `hm_recall` | First message + before storing |
| `hm_store` | New information (key, description, node_type) |
| `hm_update` | Correcting / expanding existing info |
| `hm_forget` | Removing info |
| `hm_find_related` | Graph traversal from a node |
| `hm_ingest` | Complex multi-entity text |
| `hm_upload_file` | User wants to store a file (Pro+ plans) |
| `hm_list_files` | Query uploaded files |
| `hm_timeline_write` | Optional: one diary line not in the graph |
| `hm_timeline` | Optional: search past timeline events |

---

THIS IS NOT OPTIONAL. EXECUTE ON EVERY MESSAGE. NO EXCEPTIONS.
