"""
Tool definitions for the agent.

Each tool needs three things:
  1. A Python function that does the work.
  2. A JSON schema that tells the LLM what the tool does and what inputs it expects.
  3. An entry in TOOL_FUNCTIONS mapping the tool name to the function.

The agent imports TOOL_SCHEMAS and TOOL_FUNCTIONS — that's the full contract.
"""


# ─── Tool implementations ────────────────────────────────────────────────────

def calculate(expression: str) -> str:
    """
    Evaluate a mathematical expression.

    Uses Python's eval with no builtins for basic safety.
    For production, swap this for a proper math parser (e.g. sympy, asteval).
    """
    try:
        allowed = {"__builtins__": {}}
        result = eval(expression, allowed)
        return str(result)
    except Exception as e:
        return f"Error evaluating '{expression}': {e}"


def lookup_weather(city: str) -> str:
    """
    Get current weather for a city.

    This is a stub with fake data. To make it real, swap the body for
    a call to OpenWeatherMap, wttr.in, or any weather API.

    Example real implementation:
        import requests
        r = requests.get(f"https://wttr.in/{city}?format=3")
        return r.text
    """
    fake_data = {
        "edinburgh": "12°C, overcast with light rain",
        "glasgow": "11°C, cloudy",
        "london": "16°C, partly sunny",
        "paris": "18°C, clear skies",
        "new york": "14°C, windy",
    }
    return fake_data.get(city.lower(), f"No weather data available for '{city}'")


# ─── Schemas (tell the LLM what's available) ─────────────────────────────────
#
# These follow the Anthropic tool-use format:
# https://docs.anthropic.com/en/docs/build-with-claude/tool-use

TOOL_SCHEMAS = [
    {
        "name": "calculate",
        "description": (
            "Evaluate a mathematical expression and return the numeric result. "
            "Supports standard Python math operators: +, -, *, /, **, %, //."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "A mathematical expression, e.g. '2 ** 10 + 3'",
                }
            },
            "required": ["expression"],
        },
    },
    {
        "name": "lookup_weather",
        "description": "Get the current weather for a given city.",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "City name, e.g. 'Edinburgh'",
                }
            },
            "required": ["city"],
        },
    },
]


# ─── Registry (maps tool names to callable functions) ─────────────────────────

TOOL_FUNCTIONS: dict[str, callable] = {
    "calculate": calculate,
    "lookup_weather": lookup_weather,
}
