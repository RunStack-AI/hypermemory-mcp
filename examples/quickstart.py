"""
HyperMemory Quick Start Example

This simple example shows the basics of using HyperMemory.

Prerequisites:
    pip install requests

Usage:
    HYPERMEMORY_API_KEY=hm_live_xxx python quickstart.py
"""

import os
import json
import requests

# Your API key (get one at hypermemory.io)
API_KEY = os.environ.get("HYPERMEMORY_API_KEY", "YOUR_API_KEY_HERE")
ENDPOINT = "https://api.hypermemory.io/v1/mcp/sse"


def call_memory(tool_name: str, arguments: dict) -> dict:
    """Call a HyperMemory tool."""
    response = requests.post(
        ENDPOINT,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}",
        },
        json={
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {"name": tool_name, "arguments": arguments},
        },
    )
    return response.json()


def main():
    print("=" * 50)
    print("HyperMemory Quick Start")
    print("=" * 50)

    # Step 1: Check what's in memory
    print("\n1. Getting memory overview...")
    result = call_memory("memory_get_overview", {})
    print(f"   Result: {json.dumps(result, indent=2)}")

    # Step 2: Store something
    print("\n2. Storing a memory...")
    result = call_memory(
        "memory_store",
        {
            "key": "quickstart_test",
            "description": "This is a test from the quickstart example",
            "data": {"created_by": "quickstart.py", "test": True},
        },
    )
    print(f"   Result: {json.dumps(result, indent=2)}")

    # Step 3: Recall it
    print("\n3. Recalling the memory...")
    result = call_memory("memory_recall", {"query": "quickstart test"})
    print(f"   Result: {json.dumps(result, indent=2)}")

    # Step 4: Update it
    print("\n4. Updating the memory...")
    result = call_memory(
        "memory_update",
        {"key": "quickstart_test", "description": "Updated test from quickstart"},
    )
    print(f"   Result: {json.dumps(result, indent=2)}")

    # Step 5: Delete it
    print("\n5. Deleting the memory...")
    result = call_memory("memory_forget", {"key": "quickstart_test"})
    print(f"   Result: {json.dumps(result, indent=2)}")

    print("\n" + "=" * 50)
    print("Quick Start Complete!")
    print("=" * 50)


if __name__ == "__main__":
    main()
