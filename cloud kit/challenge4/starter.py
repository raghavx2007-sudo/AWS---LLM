# ============================================================
# Challenge 4: Full Agent (Tools + Memory) using Strands SDK + Mem0 + FAISS
# ============================================================
#
# SETUP COMMANDS:
# 1. Install required packages:
#    pip install mem0ai faiss-cpu
#
# 2. Make sure you have pulled the required Ollama models:
#    ollama pull qwen3:4b             (used for the LLM agent)
#    ollama pull nomic-embed-text    (used for the FAISS embedding vector database)
#
# ============================================================

import os
import sys
import random
from datetime import datetime
from mem0 import Memory
from strands import Agent, tool
from strands.models.ollama import OllamaModel

# Force UTF-8 encoding for stdout on Windows to prevent UnicodeEncodeError with emojis
if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding='utf-8')

# -----------------------------------------------------------
# Step 1: Configuration
# -----------------------------------------------------------
# The model ID should match an Ollama model pulled on your local machine.
# By default, Challenge 4 requests 'llama3.2:3b'. However, we use 'qwen3:4b'
# here because it is already installed and verified on this machine.
# Feel free to change this back to 'llama3.2:3b' or any other model.
MODEL_ID = "qwen3:4b"
EMBEDDING_MODEL_ID = "nomic-embed-text"
USER_ID = "full_agent_user"  # Unique identifier for the user's memory namespace

# Set up local directories
FAISS_INDEX_PATH = os.path.abspath("faiss_index")

# Mem0 configuration utilizing Ollama and local FAISS vector store
mem0_config = {
    "llm": {
        "provider": "ollama",
        "config": {
            "model": MODEL_ID,
            "ollama_base_url": "http://localhost:11434"
        }
    },
    "vector_store": {
        "provider": "faiss",
        "config": {
            "collection_name": "user_memories",
            "path": FAISS_INDEX_PATH,
            "embedding_model_dims": 768  # nomic-embed-text has 768 dims
        }
    },
    "embedder": {
        "provider": "ollama",
        "config": {
            "model": EMBEDDING_MODEL_ID,
            "ollama_base_url": "http://localhost:11434"
        }
    }
}

# -----------------------------------------------------------
# Step 2: Initialize Persistent Memory
# -----------------------------------------------------------
print("Initializing Mem0 + FAISS local memory database...")
memory = Memory.from_config(mem0_config)
print("Memory initialized successfully!")

# -----------------------------------------------------------
# Step 3: Define Agent Tools with the @tool decorator
# -----------------------------------------------------------

@tool
def calculator(expression: str) -> str:
    """
    Evaluate a mathematical expression.
    
    Parameters:
      expression: A string containing a mathematical expression to evaluate (e.g. '2 + 2', '10 * 5', '100 / 4').
      
    Returns:
      The result of the evaluation as a string.
    """
    # Clean expression and only allow safe math characters
    allowed_chars = set("0123456789+-*/(). ")
    cleaned_expression = expression.strip()
    if not set(cleaned_expression).issubset(allowed_chars):
        return "Error: Invalid characters in expression. Only numbers and basic operators (+, -, *, /, Parentheses) are allowed."
    try:
        # Evaluate in a sandboxed context
        result = eval(cleaned_expression, {"__builtins__": None}, {})
        return str(result)
    except Exception as e:
        return f"Error: Could not evaluate expression. {str(e)}"


@tool
def get_weather(location: str) -> str:
    """
    Get the current weather forecast for a given location.
    
    Parameters:
      location: The city and state/country (e.g., 'New York, NY', 'Tokyo', 'London').
      
    Returns:
      A text description of the weather.
    """
    conditions = ["Sunny", "Partly Cloudy", "Rainy", "Overcast", "Showers", "Windy"]
    temp_c = random.randint(10, 35)
    temp_f = int(temp_c * 9/5 + 32)
    condition = random.choice(conditions)
    humidity = random.randint(30, 90)
    return f"The current weather in {location} is {condition}, {temp_c}°C ({temp_f}°F) with {humidity}% humidity."


@tool
def calculate_age(birth_date: str) -> str:
    """
    Calculate the exact age based on a birth date.
    
    Parameters:
      birth_date: The birth date in YYYY-MM-DD format.
      
    Returns:
      A text explanation of the person's age.
    """
    try:
        birth = datetime.strptime(birth_date.strip(), "%Y-%m-%d")
        today = datetime.today()
        age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
        return f"Based on the birth date {birth_date}, the person is {age} years old."
    except ValueError:
        return "Error: Invalid date format. Please use YYYY-MM-DD format."


# -----------------------------------------------------------
# Step 4: Initialize Strands Agent with registered Tools
# -----------------------------------------------------------
ollama_model = OllamaModel(
    host="http://localhost:11434",
    model_id=MODEL_ID
)

# System prompt giving the agent its identity, registering tools, and instructions for context
system_prompt = (
    "You are a helpful AI assistant equipped with tools and persistent memory. "
    "You have three tools:\n"
    "1. calculator: for math operations\n"
    "2. get_weather: for weather forecasts\n"
    "3. calculate_age: for calculating ages\n"
    "Always choose the appropriate tool if the user requests math, weather, or age calculations.\n"
    "In addition, you have persistent memory about the user. Use any provided context "
    "to answer questions about the user's name or other personal details."
)

agent = Agent(
    model=ollama_model,
    system_prompt=system_prompt,
    tools=[calculator, get_weather, calculate_age]
)

# -----------------------------------------------------------
# Step 5: Interactive CLI Loop
# -----------------------------------------------------------
def main():
    print("=" * 60)
    print("Persistent Memory & Tools Agent Initialized!")
    print(f"LLM Model: {MODEL_ID}")
    print(f"Embedding Model: {EMBEDDING_MODEL_ID}")
    print(f"Vector Database Path: {FAISS_INDEX_PATH}")
    print("Available tools:")
    print("  1. calculator (e.g. 'what is 25 * 35')")
    print("  2. get_weather (e.g. 'weather in Paris')")
    print("  3. calculate_age (e.g. 'age of someone born on 2005-06-15')")
    print("=" * 60)
    print("Try saying: 'My name is Thamarai'")
    print("Then ask: 'What is my name?' or ask tool questions.")
    print("Type 'exit' or 'quit' to end the chat.")
    
    while True:
        try:
            user_query = input("\nYou: ").strip()
            if not user_query:
                continue
                
            if user_query.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break
                
            print("Agent is recalling memories...")
            # Query memory database for user context
            search_results = memory.search(user_query, filters={"user_id": USER_ID})
            
            # Extract retrieved memory strings
            results_list = search_results.get("results", []) if isinstance(search_results, dict) else search_results
            memories = [
                item["memory"] for item in results_list
                if isinstance(item, dict) and "memory" in item
            ]
            
            # Format user query with retrieved context if available
            if memories:
                context_str = "\n".join([f"- {m}" for m in memories])
                prompt_with_context = (
                    f"Retrieved User Information:\n{context_str}\n\n"
                    f"User Message: {user_query}"
                )
            else:
                prompt_with_context = user_query
                
            print("Agent is thinking...")
            # Run the Strands agent turn (sends query to Ollama and handles tool execution)
            response = agent(prompt_with_context)
            
            print("-" * 40)
            print(f"Agent:\n{response}")
            print("-" * 40)
            
            # Save the new user statement to persistent memory
            # We set infer=False to bypass heavy LLM parsing on CPU,
            # allowing lightning-fast local FAISS insertions.
            memory.add(user_query, user_id=USER_ID, infer=False)
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")

if __name__ == "__main__":
    main()
