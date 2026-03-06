"""
Configuration for the agent.

Reads the API key from the environment or a .env file.
Adjust MODEL and SYSTEM_PROMPT here to change agent behaviour globally.
"""

import os
from pathlib import Path


def _load_dotenv():
    """Minimal .env loader — no extra dependency needed."""
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, value = line.partition("=")
                os.environ.setdefault(key.strip(), value.strip())


_load_dotenv()

# ─── Settings ────────────────────────────────────────────────────────────────

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

MODEL = "claude-sonnet-4-20250514"

MAX_TOKENS = 1024

MAX_ITERATIONS = 10  # safety cap on agent loop to prevent runaway calls

SYSTEM_PROMPT = (
    "You are a helpful assistant. Use the provided tools when they would "
    "help you answer the user's question accurately. If you don't need a "
    "tool, just respond directly."
)
