# ============================================================
# Challenge 1: Simple AI Agent using Strands SDK + Ollama
# ============================================================

# Import the Agent class from the Strands SDK
# Agent is the core object that manages the conversation loop
from strands import Agent

# Import OllamaModel so we can connect to our local Ollama server
from strands.models.ollama import OllamaModel

# -----------------------------------------------------------
# Step 1: Connect to the local Ollama server and pick a model
# -----------------------------------------------------------
# Ollama runs on your machine at port 11434 by default
# model_id must match a model you have pulled (ollama pull llama3.2:3b)
ollama_model = OllamaModel(
    host="http://localhost:11434",
    model_id="qwen3:4b"
)

# -----------------------------------------------------------
# Step 2: Write a system prompt to give the agent a personality
# -----------------------------------------------------------
# The system prompt tells the agent WHO it is and HOW it should behave.
# Think of it as instructions written on a sticky note for the AI.
system_prompt = (
    "You are a helpful AI assistant that explains complex technology concepts "
    "using simple, easy-to-understand language and short summaries."
)

# -----------------------------------------------------------
# Step 3: Create the Agent
# -----------------------------------------------------------
# We pass the model (Ollama) and the system prompt to create our agent.
agent = Agent(
    model=ollama_model,
    system_prompt=system_prompt
)

# -----------------------------------------------------------
# Step 4: Ask the agent a question
# -----------------------------------------------------------
user_query = "Explain what a Large Language Model (LLM) is in two sentences."

print("=" * 50)
print("Prompting the Strands Agent...")
print(f"Question: {user_query}")
print("=" * 50)

# -----------------------------------------------------------
# Step 5: Run the agent — it sends the query to Ollama and
#         returns the model's response
# -----------------------------------------------------------
response = agent(user_query)

# -----------------------------------------------------------
# Step 6: Print the response
# -----------------------------------------------------------
print("\nAgent Response:")
print(response)
