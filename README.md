# Simple AI Agent

A minimal, working AI agent in Python using the Anthropic API. Built as a reference implementation to understand the core agent loop before developing more complex agentic systems.

## How It Works

An agent is a loop with three steps:

```
User prompt → LLM decides → calls tool(s) → results fed back → LLM decides again → ... → final text response
```

There is no framework magic. The "agency" comes from the LLM choosing when and which tools to call. Your code provides the execution layer and the feedback loop. That's it.

### Architecture

```
┌─────────────┐
│  User Input  │
└──────┬───────┘
       ▼
┌──────────────────────────────────────────┐
│              Agent Loop                   │
│                                          │
│  1. Send messages + tool schemas to LLM  │
│  2. LLM responds with:                  │
│     ├─ tool_use  → execute, loop back    │
│     └─ text      → done, return answer   │
│                                          │
└──────────────────────────────────────────┘
       │
       ▼
┌──────────────────┐     ┌──────────────────┐
│  Tool: calculate │     │  Tool: weather   │
│  (local function)│     │  (stub / API)    │
└──────────────────┘     └──────────────────┘
```

The agent can call multiple tools in sequence or parallel within a single run, and the LLM autonomously decides the order.

## Quick Start

```bash
# Clone
git clone https://github.com/YOUR_USERNAME/simple-ai-agent.git
cd simple-ai-agent

# Set up environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set your API key
cp .env.example .env
# Edit .env and add your Anthropic API key

# Run
python agent.py
```

## Usage

### From the terminal (interactive mode)

```bash
python agent.py
```

This starts a REPL where you can type prompts and watch the agent reason, call tools, and respond. Type `quit` or `exit` to stop.

### Single query

```bash
python agent.py --query "What's 2**16, and is it warmer in Paris or Edinburgh?"
```

### As a module in your own code

```python
from agent import Agent

agent = Agent(verbose=True)
response = agent.run("What's the weather in Glasgow?")
print(response)
```

## Project Structure

```
simple-ai-agent/
├── agent.py           # Core agent: loop, tool dispatch, LLM calls
├── tools.py           # Tool definitions: functions + schemas
├── config.py          # Configuration (model, API key, system prompt)
├── requirements.txt   # Dependencies
├── .env.example       # Template for your API key
├── .gitignore
├── examples/
│   └── custom_tool.py # How to add your own tool
└── README.md
```

## Adding Your Own Tools

This is designed to be extended. To add a tool:

1. Write a Python function in `tools.py`
2. Add its JSON schema to `TOOL_SCHEMAS`
3. Register it in `TOOL_FUNCTIONS`

See [`examples/custom_tool.py`](examples/custom_tool.py) for a worked example.

## Developing This Into Something Real

This repo gives you the working skeleton. Here are the natural next steps depending on what you're building:

| Goal | What to add |
|---|---|
| **Persistent memory** | Store conversation history in a list or database between runs |
| **More tools** | Web search, file I/O, database queries, API calls |
| **Multi-step planning** | Add a "plan" tool that decomposes tasks before execution |
| **Error recovery** | Wrap tool execution in try/except, feed errors back to the LLM |
| **Streaming** | Use `client.messages.stream()` for real-time output |
| **Guardrails** | Validate tool inputs before execution, cap loop iterations |

The loop structure stays the same regardless of complexity.

## Requirements

- Python 3.9+
- An [Anthropic API key](https://console.anthropic.com/)

## License

MIT
