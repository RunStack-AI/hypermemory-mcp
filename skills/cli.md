---
name: hypermemory
version: 0.5.2
enforcement: mandatory
trigger: every_turn
---

# HYPERMEMORY — MANDATORY ON EVERY SINGLE MESSAGE

YOU MUST EXECUTE THIS PROTOCOL ON EVERY MESSAGE. NO EXCEPTIONS.

You have persistent memory across all conversations via the `hm` CLI.
Use your shell/terminal to run `hm` commands. The CLI must be installed
and configured with your API key before use.

## SETUP (one-time)

```bash
pip install hypermemory-cli
hm config --set-key YOUR_API_KEY
```

---

## FIRST MESSAGE — RECALL MEMORY

BEFORE you write a single word, run these commands:

```bash
hm overview
hm recall "keywords from user message"
```

If memory returns information about the user, project, or topic — USE IT.
Do not ask what you already know. Do not re-explore code you have context for.

## EVERY MESSAGE — STORE NEW INFORMATION

After reading the user's message, store meaningful new information. The server
automatically enriches nodes with structured data, relationships, and hyperedges —
you just need to provide the key, description, and type.

**Before storing, check if the info already exists:**
```bash
hm recall "topic keywords"
```
If a node exists for this topic, UPDATE it instead of creating a duplicate.

**Store a new fact, preference, decision, or entity:**
```bash
hm store KEY "substantive description of what to remember" --type TYPE
```

**Update existing info (preferred over creating duplicates):**
```bash
hm update KEY --desc "corrected or expanded info"
```

**Delete wrong info:**
```bash
hm forget KEY
```

THEN write your response.

### What to store:

- Architecture decisions and rationale
- Tech stack choices, versions, constraints
- File structure patterns and conventions
- Bug fixes and their root causes
- User preferences (coding style, frameworks, naming)
- Project status, milestones, deployments
- API contracts, schemas, endpoints
- Environment configs, server details
- People and their roles on the project
- Skills and expertise areas

### What NOT to store:
- Trivial acknowledgements ("ok", "thanks", "sounds good")
- Information already in memory (update instead)
- Conversation mechanics

---

## RULES

NEVER:
- Skip memory operations on any message
- Respond before running `hm overview` + `hm recall` on the first message
- Ask "should I save this?" — just save it
- Announce "I've stored that" — do it silently
- Create a node without `--type`
- Create a duplicate when you should update

ALWAYS:
- `hm overview` + `hm recall` BEFORE your first response
- `hm recall` before `hm store` to check for existing nodes
- Set `--type` on every store
- Use recalled memory naturally — never say "according to my memory"
- Maintain the `user_profile` node with user's name, role, preferences

---

## NODE TYPES (--type)

```
user person organization component event decision concept artifact
project technology preference fact skill
```

## RELATIONSHIPS (--rels)

When storing, add relationships with `--rels` (JSON array):

```bash
hm store tech_redis "Redis for session caching" --type technology \
  --rels '[{"to_key": "project_api", "relationship": "provides session caching for the API layer"}]'
```

Describe connections in plain language. Be specific about WHY.

BAD:  "depends_on"
BAD:  "uses"
GOOD: "The search pipeline depends on Qdrant because it provides
       vector similarity matching for the hybrid search system"

The server automatically summarizes long labels for readability.
Include `--data '{"priority":"high"}'` for structured metadata when useful.

## KEY FORMAT

`{type}_{name}` — e.g. `decision_jwt_auth`, `person_alice`, `tech_redis`, `pref_dark_mode`

Special: `user_profile` — singleton node for the primary user.

## HYPEREDGES — GROUP 3+ NODES

When 3+ nodes participate in a single indivisible relationship, use
`participant_keys` in the `--rels` JSON:

```bash
hm store project_alpha "Alpha project — frontend rewrite" --type project \
  --rels '[{"participant_keys":["person_alice","person_bob","person_carol","project_alpha"],"relationship":"core team — these three jointly constitute the decision-making unit for Alpha"}]'
```

**The removal test:** If removing any single participant still leaves the
relationship fully intact, use binary edges instead. Hyperedges capture
joint necessity that no chain of pairwise edges can express.

Do NOT overuse hyperedges. Most relationships are binary (A -> B). Only use
hyperedges when removing any participant would fundamentally change the meaning.

## FILE STORAGE (Pro, Business, Enterprise, RunStack plans)

When the user wants to store a file in HyperMemory, use the MCP tool
`hm_upload_file` with `filename` and `content_base64`. The file is uploaded
to S3 and a graph node is created with an AI-generated summary.

- Supported: pdf, doc/x, ppt/x, xls/x, csv, txt, md, rdf, jpg, png, gif, webp, mp3, wav, ogg, mp4, webm, mov
- Limits: Pro 1GB, Business 100GB, Enterprise 1TB, RunStack 10GB
- Use `hm_list_files` to query stored files
- Only upload when user explicitly asks

## TIMELINE DIARY (optional)

The **timeline** auto-records meaningful server-side activity. It is not part of the default
graph context. Use CLI commands when the user needs a diary or "what did we do when?"

```bash
hm timeline-write "Plain-language line (e.g. major topic you did not store as a node)"
hm timeline   # add filters: --query, --period, --node, --start, --end
```

## FULL COMMAND REFERENCE

| Command | When |
|---------|------|
| `hm overview` | First message |
| `hm recall "query"` | First message + before storing |
| `hm store KEY "desc" --type TYPE` | New information |
| `hm update KEY --desc "new"` | Correcting / expanding info |
| `hm forget KEY` | Removing info |
| `hm find KEY` | Graph traversal from a node |
| `hm relate --from A --to B --rel "..."` | Create a relationship |
| `hm relationships KEY` | List edges for a node |
| `hm ingest "text" --context "label"` | Complex multi-entity text |
| `hm timeline-write "..."` | Optional: explicit diary line |
| `hm timeline` | Optional: look back at past timeline events |

---

THIS IS NOT OPTIONAL. EXECUTE ON EVERY MESSAGE. NO EXCEPTIONS.
