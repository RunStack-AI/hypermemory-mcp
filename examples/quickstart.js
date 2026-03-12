/**
 * HyperMemory Quick Start Example (JavaScript)
 *
 * This simple example shows the basics of using HyperMemory.
 *
 * Usage:
 *   HYPERMEMORY_API_KEY=hm_live_xxx node quickstart.js
 */

const API_KEY = process.env.HYPERMEMORY_API_KEY || "YOUR_API_KEY_HERE";
const ENDPOINT = "https://api.hypermemory.io/v1/mcp/sse";

/**
 * Call a HyperMemory tool
 */
async function callMemory(toolName, args) {
  const response = await fetch(ENDPOINT, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${API_KEY}`,
    },
    body: JSON.stringify({
      jsonrpc: "2.0",
      id: 1,
      method: "tools/call",
      params: {
        name: toolName,
        arguments: args,
      },
    }),
  });
  return response.json();
}

async function main() {
  console.log("=".repeat(50));
  console.log("HyperMemory Quick Start (JavaScript)");
  console.log("=".repeat(50));

  // Step 1: Check what's in memory
  console.log("\n1. Getting memory overview...");
  let result = await callMemory("memory_get_overview", {});
  console.log("   Result:", JSON.stringify(result, null, 2));

  // Step 2: Store something
  console.log("\n2. Storing a memory...");
  result = await callMemory("memory_store", {
    key: "quickstart_test_js",
    description: "This is a test from the JavaScript quickstart",
    data: {
      created_by: "quickstart.js",
      test: true,
    },
  });
  console.log("   Result:", JSON.stringify(result, null, 2));

  // Step 3: Recall it
  console.log("\n3. Recalling the memory...");
  result = await callMemory("memory_recall", {
    query: "quickstart test",
  });
  console.log("   Result:", JSON.stringify(result, null, 2));

  // Step 4: Update it
  console.log("\n4. Updating the memory...");
  result = await callMemory("memory_update", {
    key: "quickstart_test_js",
    description: "Updated test from JavaScript quickstart",
  });
  console.log("   Result:", JSON.stringify(result, null, 2));

  // Step 5: Delete it
  console.log("\n5. Deleting the memory...");
  result = await callMemory("memory_forget", {
    key: "quickstart_test_js",
  });
  console.log("   Result:", JSON.stringify(result, null, 2));

  console.log("\n" + "=".repeat(50));
  console.log("Quick Start Complete!");
  console.log("=".repeat(50));
}

main().catch(console.error);
