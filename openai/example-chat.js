/**
 * HyperMemory + OpenAI Chat Example
 * 
 * This example shows how to add persistent memory to an OpenAI chat application.
 * 
 * Prerequisites:
 *   npm install openai dotenv
 * 
 * Environment variables (.env file):
 *   OPENAI_API_KEY=sk-xxx
 *   HYPERMEMORY_API_KEY=hm_live_xxx
 */

import OpenAI from 'openai';
import 'dotenv/config';
import { readFileSync } from 'fs';

// Load function definitions
const functionsConfig = JSON.parse(readFileSync('./functions.json', 'utf-8'));
const functions = functionsConfig.functions;

// Initialize OpenAI
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY
});

// HyperMemory configuration
const HYPERMEMORY_URL = 'https://api.hypermemory.io/v1/mcp/sse';
const HYPERMEMORY_API_KEY = process.env.HYPERMEMORY_API_KEY;

/**
 * Call a HyperMemory tool
 */
async function callHyperMemory(toolName, args) {
  console.log(`\n🧠 Calling HyperMemory: ${toolName}`);
  console.log(`   Arguments: ${JSON.stringify(args)}`);

  const response = await fetch(HYPERMEMORY_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${HYPERMEMORY_API_KEY}`
    },
    body: JSON.stringify({
      jsonrpc: '2.0',
      id: Date.now(),
      method: 'tools/call',
      params: {
        name: toolName,
        arguments: args
      }
    })
  });

  const data = await response.json();
  
  if (data.error) {
    console.log(`   ❌ Error: ${data.error.message}`);
    return { error: data.error.message };
  }

  console.log(`   ✅ Success`);
  return data.result;
}

/**
 * Process a chat message with memory capabilities
 */
async function chat(userMessage, conversationHistory = []) {
  // Add user message to history
  conversationHistory.push({
    role: 'user',
    content: userMessage
  });

  // Call OpenAI with function definitions
  const response = await openai.chat.completions.create({
    model: 'gpt-4-turbo-preview',
    messages: [
      {
        role: 'system',
        content: `You are a helpful assistant with persistent memory capabilities.

IMPORTANT GUIDELINES:
- Use memory_get_overview at the START of conversations to see available context
- Use memory_recall when you need to find specific information
- Use memory_store when the user shares facts, preferences, or important information
- Use memory_add_relationships to connect related pieces of information
- Always acknowledge when you've stored or recalled information

Memory helps you maintain context across conversations. Use it proactively.`
      },
      ...conversationHistory
    ],
    functions: functions,
    function_call: 'auto'
  });

  const message = response.choices[0].message;

  // Check if the model wants to call a function
  if (message.function_call) {
    const functionName = message.function_call.name;
    const functionArgs = JSON.parse(message.function_call.arguments);

    // Call HyperMemory
    const functionResult = await callHyperMemory(functionName, functionArgs);

    // Add the function call and result to history
    conversationHistory.push(message);
    conversationHistory.push({
      role: 'function',
      name: functionName,
      content: JSON.stringify(functionResult)
    });

    // Get the final response from the model
    const finalResponse = await openai.chat.completions.create({
      model: 'gpt-4-turbo-preview',
      messages: [
        {
          role: 'system',
          content: 'You are a helpful assistant with persistent memory capabilities.'
        },
        ...conversationHistory
      ],
      functions: functions,
      function_call: 'auto'
    });

    const finalMessage = finalResponse.choices[0].message;

    // Handle chained function calls (the model might want to call another function)
    if (finalMessage.function_call) {
      // Recursively handle additional function calls
      return chat('', conversationHistory);
    }

    conversationHistory.push(finalMessage);
    return {
      response: finalMessage.content,
      history: conversationHistory
    };
  }

  // No function call - direct response
  conversationHistory.push(message);
  return {
    response: message.content,
    history: conversationHistory
  };
}

/**
 * Interactive chat loop
 */
async function main() {
  const readline = await import('readline');
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });

  console.log('🧠 HyperMemory Chat');
  console.log('==================');
  console.log('Type your messages and press Enter.');
  console.log('Type "exit" to quit.\n');

  let history = [];

  const askQuestion = () => {
    rl.question('You: ', async (input) => {
      if (input.toLowerCase() === 'exit') {
        console.log('\nGoodbye!');
        rl.close();
        return;
      }

      try {
        const result = await chat(input, history);
        history = result.history;
        console.log(`\nAssistant: ${result.response}\n`);
      } catch (error) {
        console.error(`\nError: ${error.message}\n`);
      }

      askQuestion();
    });
  };

  askQuestion();
}

// Run if executed directly
main().catch(console.error);
