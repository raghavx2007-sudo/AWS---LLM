# ============================================================
# Challenge 5: MCP Agent using Strands SDK + Ollama
# ============================================================
#
# SETUP COMMANDS:
# 1. Install required packages:
#    pip install mcp
#
# 2. Make sure you have pulled the required Ollama model:
#    ollama pull qwen3:4b             (used for the LLM agent)
#
# ============================================================

import os
import sys
from mcp import stdio_client, StdioServerParameters
from strands import Agent
from strands.models.ollama import OllamaModel
from strands.tools.mcp import MCPClient

# Force UTF-8 encoding for stdout on Windows to prevent UnicodeEncodeError with emojis
if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding='utf-8')

# -----------------------------------------------------------
# Step 1: Model & Path Configuration
# -----------------------------------------------------------
# The model ID should match an Ollama model pulled on your local machine.
# By default, Challenge 5 requests 'llama3.2:3b'. However, we use 'qwen3:4b'
# here because it is already installed and verified on this machine.
# Feel free to change this back to 'llama3.2:3b' or any other model.
MODEL_ID = "qwen3:4b"

# Absolute path to our local FastMCP server script
SERVER_SCRIPT_PATH = os.path.abspath("server.py")

# -----------------------------------------------------------
# Step 2: Initialize MCP Client with STDIO Connection
# -----------------------------------------------------------
print(f"Configuring local MCP server launch parameters...")
server_params = StdioServerParameters(
    command="python",
    args=[SERVER_SCRIPT_PATH]
)

print(f"Connecting to the local MCP server via STDIO...")
# Wrap the standard mcp stdio_client context manager in the Strands MCPClient.
# MCPClient handles the connection lifecycle and tool discovery in a background thread.
mcp_client = MCPClient(lambda: stdio_client(server_params))

# -----------------------------------------------------------
# Step 3: Initialize Strands Agent with the MCP Server
# -----------------------------------------------------------
ollama_model = OllamaModel(
    host="http://localhost:11434",
    model_id=MODEL_ID
)

# System prompt giving the agent its identity and instructing it on MCP tool usage
system_prompt = (
    "You are a helpful AI assistant equipped with a local Model Context Protocol (MCP) server. "
    "You have access to a tool named get_mcp_message (or get_mcp_message_get_mcp_message depending on prefixing). "
    "Always use the local MCP server greeting tool if the user asks for a greeting or a message from the MCP server. "
    "Do not simulate the greeting yourself; invoke the tool."
)

print("Booting the Strands agent and loading tools...")
agent = Agent(
    model=ollama_model,
    system_prompt=system_prompt,
    tools=[mcp_client]
)
print("Agent initialized successfully!")

# -----------------------------------------------------------
# Step 4: Interactive CLI Chat Loop
# -----------------------------------------------------------
def main():
    print("=" * 60)
    print("MCP Chatbot initialized!")
    print(f"LLM Model: {MODEL_ID}")
    print(f"MCP Server: {SERVER_SCRIPT_PATH}")
    print("Available tools loaded from MCP server:")
    # Print the tool names that were discovered on the MCP server
    print(f"  Tools: {list(agent.tool_names)}")
    print("=" * 60)
    print("Try asking: 'Call the local MCP tool for Thamarai'")
    print("Type 'exit' or 'quit' to close the assistant.")
    
    while True:
        try:
            user_query = input("\nYou: ").strip()
            if not user_query:
                continue
                
            if user_query.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break
                
            print("Agent is thinking...")
            # Query the agent (Strands automatically executes MCP tools if needed)
            response = agent(user_query)
            
            print("-" * 40)
            print(f"Agent:\n{response}")
            print("-" * 40)
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")

if __name__ == "__main__":
    main()
