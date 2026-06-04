# AWS---LLM-
# 🚀 Builders Skill Sprint - Strands SDK + Ollama

A collection of beginner-friendly AI Agent projects built using **Strands SDK**, **Ollama**, **Llama 3.2:3B**, **Mem0**, **FAISS**, and **MCP**.

## 📌 Overview

This repository contains solutions for the Builders Skill Sprint challenges.

Each challenge gradually introduces new AI agent capabilities:

* Challenge 1 → Basic AI Agent
* Challenge 2 → Tool-Enabled Agent
* Challenge 3 → Memory Agent
* Challenge 4 → Full Agent
* Challenge 5 → MCP Chatbot

---

# 🏆 Challenge 1 - Simple AI Agent

### Features

* Strands SDK integration
* Ollama Llama3.2:3B model
* Interactive chat loop
* Basic conversational AI

### Run

```bash
python starter.py
```

### Example

```text
You: Hello
Agent: Hi! How can I help you today?
```

---

# 🏆 Challenge 2 - Tools Agent

### Features

* Calculator Tool
* Weather Tool
* Age Calculator Tool
* Interactive multi-turn conversation

### Example Questions

```text
What is 2 ** 10?
What is the weather in Paris?
How old is someone born in 2006?
```

### Run

```bash
python starter.py
```

---

# 🏆 Challenge 3 - Memory Agent

### Features

* Persistent Memory
* Mem0 Integration
* FAISS Vector Storage
* User Information Recall

### Installation

```bash
pip install "mem0ai[nlp]"
```

### Example

```text
You: My name is Thamarai

You: What is my name?

Agent: Your name is Thamarai
```

### Run

```bash
python starter.py
```

---

# 🏆 Challenge 4 - Full Agent

### Features

✅ Calculator Tool

✅ Weather Tool

✅ Age Calculator Tool

✅ Persistent Memory

✅ User Recall

✅ Interactive Chat

### Example

```text
You: My name is Thamarai

You: I was born in 2006

You: What is 2 ** 16?

You: Show me all my memories
```

### Run

```bash
python starter.py
```

---

# 🏆 Challenge 5 - MCP Chatbot

### Features

* Local MCP Server
* MCP Tool Integration
* Memory Support
* Calculator Functions
* Text Utilities
* Interactive Chatbot

### Start MCP Server

```bash
python mcp_server.py
```

### Start Agent

```bash
python starter.py
```

### Example Questions

```text
What is 128 * 7?
Divide 1000 by 8
Reverse the word python
Remember that my name is Thamarai
What is my name?
```

---

# 🛠️ Tech Stack

* Python
* Strands SDK
* Ollama
* Llama 3.2:3B
* Mem0
* FAISS
* MCP (Model Context Protocol)

---

# 📂 Project Structure

```text
builders-skill-sprint/
│
├── challenge1/
│   └── starter.py
│
├── challenge2/
│   └── starter.py
│
├── challenge3/
│   └── starter.py
│
├── challenge4/
│   └── starter.py
│
├── challenge5/
│   ├── starter.py
│   └── mcp_server.py
│
└── README.md
```

---

# 🎯 Learning Outcomes

By completing these challenges, you will learn:

* Building AI Agents
* Tool Calling
* Memory Management
* Retrieval-Augmented AI
* MCP Integration
* Local LLM Development
* Agent Architecture Design

---

# 🙌 Acknowledgements

Built as part of the Builders Skill Sprint using:

* Strands SDK
* Ollama
* Llama 3.2
* Mem0
* FAISS
* MCP

Happy Building! 🚀
