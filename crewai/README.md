# HyperMemory + CrewAI

This guide shows you how to give your CrewAI agents persistent memory.

## What is CrewAI?

CrewAI is a framework for creating teams of AI agents that work together. Each agent has a role, goals, and tools.

## What You'll Get

After setup, your crews will be able to:
- ✅ Remember information across different runs
- ✅ Share memory between agents
- ✅ Build knowledge over time
- ✅ Recall context from previous tasks

## Requirements

- Python 3.10+
- CrewAI installed (`pip install crewai`)
- A HyperMemory API key from [hypermemory.io](https://hypermemory.io)

## Installation

Install the HyperMemory CrewAI integration:

```bash
pip install hypermemory-crewai
```

Or install directly from source:

```bash
pip install git+https://github.com/RunStack-AI/hypermemory-crewai.git
```

## Quick Start

### Step 1: Set Up Your API Key

Create a `.env` file in your project:

```bash
HYPERMEMORY_API_KEY=hm_live_xxx
```

Or set it in your code:

```python
import os
os.environ["HYPERMEMORY_API_KEY"] = "hm_live_xxx"
```

### Step 2: Create Memory Tools

```python
from hypermemory_crewai import HyperMemoryTools

# Create the memory toolkit
memory = HyperMemoryTools(
    api_key=os.environ["HYPERMEMORY_API_KEY"],
    gateway_url="https://api.hypermemory.io"
)

# Get individual tools
store_tool = memory.get_tool("store")
recall_tool = memory.get_tool("recall")
overview_tool = memory.get_tool("overview")
related_tool = memory.get_tool("find_related")
```

### Step 3: Add Tools to Your Agent

```python
from crewai import Agent

researcher = Agent(
    role="Research Analyst",
    goal="Research topics thoroughly and remember key findings",
    backstory="You are a diligent researcher who maintains detailed notes.",
    tools=[
        memory.get_tool("store"),
        memory.get_tool("recall"),
        memory.get_tool("overview")
    ],
    verbose=True
)
```

### Step 4: Create Tasks That Use Memory

```python
from crewai import Task

research_task = Task(
    description="""
    Research the topic of renewable energy trends.
    
    First, check memory for any existing research on this topic.
    Then, conduct new research and store key findings.
    Make sure to link new information to related existing memories.
    """,
    agent=researcher,
    expected_output="A summary of findings with references to stored memories"
)
```

### Step 5: Run Your Crew

```python
from crewai import Crew

crew = Crew(
    agents=[researcher],
    tasks=[research_task]
)

result = crew.kickoff()
print(result)
```

## Complete Example

```python
import os
from crewai import Agent, Task, Crew
from hypermemory_crewai import HyperMemoryTools

# Setup
os.environ["HYPERMEMORY_API_KEY"] = "hm_live_xxx"

# Create memory tools
memory = HyperMemoryTools(gateway_url="https://api.hypermemory.io")

# Create agents with memory
lead_researcher = Agent(
    role="Lead Research Analyst",
    goal="Conduct thorough research and maintain organizational knowledge",
    backstory="""You are a senior researcher responsible for building 
    and maintaining the team's knowledge base. You always check existing 
    knowledge before starting new research.""",
    tools=[
        memory.get_tool("store"),
        memory.get_tool("recall"),
        memory.get_tool("overview"),
        memory.get_tool("find_related")
    ],
    verbose=True,
    allow_delegation=False
)

writer = Agent(
    role="Technical Writer",
    goal="Transform research into clear, actionable content",
    backstory="""You are an expert at taking complex research and 
    making it accessible. You always reference existing knowledge 
    to maintain consistency.""",
    tools=[
        memory.get_tool("recall"),
        memory.get_tool("overview")
    ],
    verbose=True,
    allow_delegation=False
)

# Create tasks
research_task = Task(
    description="""
    Research the current state of AI in healthcare.
    
    Instructions:
    1. First, use memory_get_overview to see what we already know
    2. Use memory_recall to find any related existing research
    3. Conduct your research on AI in healthcare
    4. Use memory_store to save key findings with keys like:
       - healthcare_ai_diagnosis
       - healthcare_ai_treatment
       - healthcare_ai_challenges
    5. Link related findings together
    """,
    agent=lead_researcher,
    expected_output="Comprehensive research notes stored in memory"
)

writing_task = Task(
    description="""
    Write a brief report on AI in healthcare.
    
    Instructions:
    1. Use memory_recall to gather all healthcare AI research
    2. Synthesize into a clear 500-word summary
    3. Include key statistics and trends
    """,
    agent=writer,
    expected_output="A 500-word summary report on AI in healthcare"
)

# Run the crew
crew = Crew(
    agents=[lead_researcher, writer],
    tasks=[research_task, writing_task],
    verbose=True
)

result = crew.kickoff()
print("\n" + "="*50)
print("FINAL REPORT")
print("="*50)
print(result)
```

## Available Tools

| Tool | Method | Description |
|------|--------|-------------|
| Store | `memory.get_tool("store")` | Save new information |
| Recall | `memory.get_tool("recall")` | Search for information |
| Overview | `memory.get_tool("overview")` | Get summary of all memory |
| Find Related | `memory.get_tool("find_related")` | Find connected information |
| Update | `memory.get_tool("update")` | Modify existing information |
| Forget | `memory.get_tool("forget")` | Remove information |

## Best Practices

### 1. Always Check Memory First

In your task descriptions, tell agents to check existing knowledge:

```python
task = Task(
    description="""
    Before starting, use memory_recall to check for existing 
    information on this topic. Build on what we already know.
    """
)
```

### 2. Use Consistent Key Naming

Establish a naming convention for your keys:

```python
# Good - consistent, searchable
"customer_preferences_john"
"project_status_alpha"
"research_topic_ai_healthcare"

# Bad - inconsistent, hard to find
"john stuff"
"Alpha"
"ai-research"
```

### 3. Link Related Information

When storing, connect related memories:

```python
# In your task description:
"""
When storing findings about AI diagnosis, link them to 
existing healthcare research using relationships.
"""
```

### 4. Give Agents Clear Memory Instructions

Be specific about when and how to use memory:

```python
backstory="""You maintain detailed records of all research.
At the START of every task, you check memory_get_overview.
At the END of every task, you store key findings."""
```

## Troubleshooting

### Agent Doesn't Use Memory Tools

The agent might not understand when to use them.

**Fix:** Be very explicit in the task description:
```python
description="""
REQUIRED: Use memory_recall with query 'previous research' 
before proceeding with any new work.
"""
```

### "Connection Error"

Can't reach HyperMemory.

**Fix:** Check your API key and internet connection. Test with:
```python
memory = HyperMemoryTools()
print(memory.test_connection())  # Should print "OK"
```

### Memory Not Persisting

Make sure you're using the same API key across runs.

**Fix:** Store your API key in environment variables, not hardcoded.

### Too Many API Calls

Your crew is making too many memory requests.

**Fix:** 
- Use `memory_get_overview` once at the start instead of multiple recalls
- Batch information into fewer, larger store operations

## Integration with Other Tools

### With Web Search

```python
from crewai_tools import SerperDevTool

search = SerperDevTool()

researcher = Agent(
    tools=[
        search,
        memory.get_tool("store"),
        memory.get_tool("recall")
    ]
)
```

### With File Operations

```python
from crewai_tools import FileReadTool

file_reader = FileReadTool()

analyst = Agent(
    tools=[
        file_reader,
        memory.get_tool("store"),
        memory.get_tool("recall")
    ]
)
```

---

Need help? [Open an issue](https://github.com/RunStack-AI/hypermemory-mcp/issues)
