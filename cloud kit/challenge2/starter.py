# ============================================================
# Challenge 2: Tools Agent using Strands SDK + Ollama
# ============================================================

import random
from datetime import datetime
from strands import Agent, tool
from strands.models.ollama import OllamaModel

# -----------------------------------------------------------
# Step 1: Model Configuration
# -----------------------------------------------------------
# The model ID should match an Ollama model pulled on your local machine.
# By default, Challenge 2 requests 'llama3.2:3b'. However, we use 'qwen3:4b'
# here because it is already installed and verified on this machine.
# Feel free to change this back to 'llama3.2:3b' or any other model.
MODEL_ID = "qwen3:4b"

# Connect to the local Ollama server
ollama_model = OllamaModel(
    host="http://localhost:11434",
    model_id=MODEL_ID
)

# -----------------------------------------------------------
# Step 2: Define Tools with the @tool decorator
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
# Step 3: Initialize the Agent with the Tools
# -----------------------------------------------------------
# The system prompt instructs the agent on its behavior and lists its tools.
system_prompt = (
    "You are a helpful AI assistant equipped with specific tools to help answer user questions. "
    "Use the calculator tool for math, get_weather tool for weather forecasts, and calculate_age "
    "tool for calculating ages. If a question cannot be answered using a tool, respond with your own knowledge."
)

agent = Agent(
    model=ollama_model,
    system_prompt=system_prompt,
    tools=[calculator, get_weather, calculate_age]
)

# -----------------------------------------------------------
# Step 4: Interactive Main CLI Loop
# -----------------------------------------------------------
def main():
    print("=" * 60)
    print(f"Strands Agent initialized with model: {MODEL_ID}")
    print("Available tools:")
    print("  1. calculator (e.g. '123 + 456')")
    print("  2. get_weather (e.g. 'Tokyo')")
    print("  3. calculate_age (e.g. '1990-05-15')")
    print("=" * 60)
    print("Type your questions below. Type 'exit' or 'quit' to close the assistant.")
    
    while True:
        try:
            user_query = input("\nYou: ")
            if user_query.strip().lower() in ["exit", "quit"]:
                print("Goodbye!")
                break
            if not user_query.strip():
                continue
                
            print("Agent thinking...")
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
