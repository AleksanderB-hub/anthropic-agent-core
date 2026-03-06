"""
Example: Adding a custom tool to the agent.

This file shows how to add a 'word_count' tool step by step.
Copy the pattern into tools.py when you want to add your own tools.

Steps:
  1. Write the function
  2. Write the schema
  3. Register it
"""

# ─── Step 1: Write the function ──────────────────────────────────────────────
#
# Any Python function that takes keyword arguments and returns a string.

def word_count(text: str) -> str:
    """Count words in a given text."""
    count = len(text.split())
    return f"{count} words"


# ─── Step 2: Write the schema ────────────────────────────────────────────────
#
# This is what the LLM sees. Be specific in your descriptions — the model
# uses them to decide when and how to call the tool.

WORD_COUNT_SCHEMA = {
    "name": "word_count",
    "description": "Count the number of words in a piece of text.",
    "input_schema": {
        "type": "object",
        "properties": {
            "text": {
                "type": "string",
                "description": "The text to count words in.",
            }
        },
        "required": ["text"],
    },
}


# ─── Step 3: Register it in tools.py ─────────────────────────────────────────
#
# In tools.py, you would add:
#
#   from examples.custom_tool import word_count, WORD_COUNT_SCHEMA
#
#   TOOL_SCHEMAS.append(WORD_COUNT_SCHEMA)
#   TOOL_FUNCTIONS["word_count"] = word_count
#
# That's it. The agent will now have access to your new tool.


# ─── Tips for good tools ─────────────────────────────────────────────────────
#
# - Return strings (the LLM reads the result as text).
# - Return useful error messages instead of raising exceptions.
# - Keep descriptions precise: the LLM decides when to call the tool
#   based almost entirely on the schema description.
# - Test the function standalone before plugging it into the agent.
# - For API-backed tools, handle timeouts and rate limits gracefully.
