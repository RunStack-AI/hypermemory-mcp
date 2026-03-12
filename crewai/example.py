"""
HyperMemory + CrewAI Example

This example demonstrates how to create a CrewAI crew with persistent memory.

Prerequisites:
    pip install crewai requests python-dotenv

Environment variables (.env file):
    HYPERMEMORY_API_KEY=hm_live_xxx
    OPENAI_API_KEY=sk-xxx
"""

import os
import json
import requests
from typing import Any, Optional
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai_tools import BaseTool

# Load environment variables
load_dotenv()

# HyperMemory configuration
HYPERMEMORY_URL = "https://api.hypermemory.io/v1/mcp/sse"
HYPERMEMORY_API_KEY = os.environ.get("HYPERMEMORY_API_KEY")


def call_hypermemory(tool_name: str, arguments: dict) -> dict:
    """Make a request to the HyperMemory API."""
    response = requests.post(
        HYPERMEMORY_URL,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {HYPERMEMORY_API_KEY}",
        },
        json={
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {"name": tool_name, "arguments": arguments},
        },
    )
    data = response.json()
    if "error" in data:
        return {"error": data["error"]["message"]}
    return data.get("result", {})


# =============================================================================
# Custom CrewAI Tools for HyperMemory
# =============================================================================


class MemoryStoreTool(BaseTool):
    name: str = "memory_store"
    description: str = """Store information in long-term memory.
    Use this when you learn important facts about users, projects, or decisions.
    
    Arguments:
    - key (required): Unique identifier for this memory (use snake_case)
    - description (required): What this memory contains
    - data (optional): Additional structured data as JSON
    """

    def _run(self, key: str, description: str, data: Optional[dict] = None) -> str:
        arguments = {"key": key, "description": description}
        if data:
            arguments["data"] = data
        result = call_hypermemory("memory_store", arguments)
        return json.dumps(result)


class MemoryRecallTool(BaseTool):
    name: str = "memory_recall"
    description: str = """Search for information in memory.
    Use this to find relevant context from previous conversations or stored facts.
    
    Arguments:
    - query (required): What to search for
    - max_results (optional): Maximum results to return (default: 10)
    """

    def _run(self, query: str, max_results: int = 10) -> str:
        result = call_hypermemory(
            "memory_recall", {"query": query, "max_results": max_results}
        )
        return json.dumps(result)


class MemoryOverviewTool(BaseTool):
    name: str = "memory_get_overview"
    description: str = """Get a summary of what's stored in memory.
    Use this at the start of tasks to understand available context.
    
    No arguments required.
    """

    def _run(self) -> str:
        result = call_hypermemory("memory_get_overview", {})
        return json.dumps(result)


class MemoryFindRelatedTool(BaseTool):
    name: str = "memory_find_related"
    description: str = """Find memories related to a specific key.
    Use this to explore connections between stored information.
    
    Arguments:
    - key (required): The memory key to find relationships for
    - max_depth (optional): How far to follow connections (default: 3)
    """

    def _run(self, key: str, max_depth: int = 3) -> str:
        result = call_hypermemory(
            "memory_find_related", {"key": key, "max_depth": max_depth}
        )
        return json.dumps(result)


class MemoryUpdateTool(BaseTool):
    name: str = "memory_update"
    description: str = """Update existing information in memory.
    Use when facts have changed or need correction.
    
    Arguments:
    - key (required): The memory key to update
    - description (optional): New description
    - data (optional): New/updated data as JSON
    """

    def _run(
        self, key: str, description: Optional[str] = None, data: Optional[dict] = None
    ) -> str:
        arguments = {"key": key}
        if description:
            arguments["description"] = description
        if data:
            arguments["data"] = data
        result = call_hypermemory("memory_update", arguments)
        return json.dumps(result)


class MemoryForgetTool(BaseTool):
    name: str = "memory_forget"
    description: str = """Remove information from memory.
    Use when information is no longer relevant or should be deleted.
    
    Arguments:
    - key (required): The memory key to delete
    - cascade (optional): Also remove connections (default: true)
    """

    def _run(self, key: str, cascade: bool = True) -> str:
        result = call_hypermemory("memory_forget", {"key": key, "cascade": cascade})
        return json.dumps(result)


# =============================================================================
# Example Crew
# =============================================================================


def create_memory_tools():
    """Create all memory tools."""
    return [
        MemoryStoreTool(),
        MemoryRecallTool(),
        MemoryOverviewTool(),
        MemoryFindRelatedTool(),
        MemoryUpdateTool(),
        MemoryForgetTool(),
    ]


def main():
    """Run an example crew with memory capabilities."""

    # Create memory tools
    memory_tools = create_memory_tools()

    # Create agents
    researcher = Agent(
        role="Research Analyst",
        goal="Research topics thoroughly and maintain organized knowledge",
        backstory="""You are a meticulous researcher who always checks existing 
        knowledge before starting new research. You document everything carefully 
        and create connections between related information.""",
        tools=memory_tools,
        verbose=True,
        allow_delegation=False,
    )

    writer = Agent(
        role="Content Writer",
        goal="Create clear, informative content based on research",
        backstory="""You transform complex research into accessible content.
        You always reference existing knowledge to maintain consistency and
        build on previous work.""",
        tools=[MemoryRecallTool(), MemoryOverviewTool()],  # Read-only access
        verbose=True,
        allow_delegation=False,
    )

    # Create tasks
    research_task = Task(
        description="""
        Research the topic: "Benefits of renewable energy"
        
        Follow these steps:
        1. Use memory_get_overview to check what we already know
        2. Use memory_recall to find any related existing research
        3. Conduct your research on the topic
        4. Store your findings using memory_store with these keys:
           - renewable_energy_benefits
           - renewable_energy_challenges
           - renewable_energy_trends
        5. Make sure to include specific facts and statistics
        """,
        agent=researcher,
        expected_output="A comprehensive set of research notes stored in memory",
    )

    writing_task = Task(
        description="""
        Write a brief article on renewable energy benefits.
        
        Follow these steps:
        1. Use memory_recall to gather all renewable energy research
        2. Synthesize the information into a clear 300-word article
        3. Include key statistics and trends
        4. Make it accessible to a general audience
        """,
        agent=writer,
        expected_output="A 300-word article on renewable energy benefits",
        context=[research_task],
    )

    # Create and run the crew
    crew = Crew(
        agents=[researcher, writer],
        tasks=[research_task, writing_task],
        process=Process.sequential,
        verbose=True,
    )

    print("\n" + "=" * 60)
    print("Starting HyperMemory CrewAI Example")
    print("=" * 60 + "\n")

    result = crew.kickoff()

    print("\n" + "=" * 60)
    print("FINAL OUTPUT")
    print("=" * 60)
    print(result)


if __name__ == "__main__":
    main()
