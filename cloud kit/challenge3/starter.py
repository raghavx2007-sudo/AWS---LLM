# ============================================================
# Challenge 3: Persistent Memory Agent using Strands SDK + Mem0 + FAISS
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

import sys
if sys.platform.startswith("win"):
    # Force UTF-8 encoding for stdout on Windows to prevent UnicodeEncodeError with emojis
    sys.stdout.reconfigure(encoding='utf-8')

import os
from mem0 import Memory
from strands import Agent
from strands.models.ollama import OllamaModel

# -----------------------------------------------------------
# Step 1: Configuration
# -----------------------------------------------------------
# The model ID should match an Ollama model pulled on your local machine.
# By default, Challenge 3 requests 'llama3.2:3b'. However, we use 'qwen3:4b'
# here because it is already installed and verified on this machine.
# Feel free to change this back to 'llama3.2:3b' or any other model.
MODEL_ID = "qwen3:4b"
EMBEDDING_MODEL_ID = "nomic-embed-text"
USER_ID = "thamarai_user"  # Unique identifier for the user

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
# Step 3: Initialize Strands Agent
# -----------------------------------------------------------
ollama_model = OllamaModel(
    host="http://localhost:11434",
    model_id=MODEL_ID
)

# System prompt directing the agent on how to use retrieved context
system_prompt = (
    "You are a helpful AI assistant that remembers details about the user. "
    "Use the provided context to answer questions about the user's name or other "
    "personal information. If no context is provided, answer using your own knowledge."
)

agent = Agent(
    model=ollama_model,
    system_prompt=system_prompt
)

# -----------------------------------------------------------
# Step 4: Interactive CLI Loop
# -----------------------------------------------------------
def main():
    print("=" * 60)
    print("Persistent Memory Agent Initialized!")
    print(f"LLM Model: {MODEL_ID}")
    print(f"Embedding Model: {EMBEDDING_MODEL_ID}")
    print(f"Vector Database Path: {FAISS_INDEX_PATH}")
    print("=" * 60)
    print("Try saying: 'My name is Thamarai'")
    print("Then ask: 'What is my name?'")
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
            # Search memory database for relevant details
            search_results = memory.search(user_query, filters={"user_id": USER_ID})
            
            # Extract retrieved memory strings
            results_list = search_results.get("results", []) if isinstance(search_results, dict) else search_results
            memories = [
                item["memory"] for item in results_list
                if isinstance(item, dict) and "memory" in item
            ]
            
            # Format query with context if memories were found
            if memories:
                context_str = "\n".join([f"- {m}" for m in memories])
                prompt_with_context = (
                    f"Retrieved User Information:\n{context_str}\n\n"
                    f"User Message: {user_query}"
                )
            else:
                prompt_with_context = user_query
                
            print("Agent is thinking...")
            # Query the agent
            response = agent(prompt_with_context)
            
            print("-" * 40)
            print(f"Agent:\n{response}")
            print("-" * 40)
            
            # Save the new input to persistent memory database
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
