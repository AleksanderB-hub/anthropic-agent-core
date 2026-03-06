"""
Core agent loop.

This is the only file that talks to the Anthropic API.
It imports tool definitions from tools.py and settings from config.py.

Usage:
    # Interactive REPL
    python agent.py

    # Single query
    python agent.py --query "What is 2**20?"

    # Quiet mode (no tool-call tracing)
    python agent.py --query "Weather in Edinburgh?" --quiet
"""

import argparse
import json
import sys

import anthropic

from config import MODEL, MAX_TOKENS, MAX_ITERATIONS, SYSTEM_PROMPT
from tools import TOOL_SCHEMAS, TOOL_FUNCTIONS


class Agent:
    """
    A minimal agent that loops between LLM reasoning and local tool execution.

    Attributes:
        client:   Anthropic API client (reads ANTHROPIC_API_KEY from env).
        verbose:  If True, prints each tool call and result to stderr.
    """

    def __init__(self, verbose: bool = True):
        self.client = anthropic.Anthropic()
        self.verbose = verbose

    def run(self, user_message: str) -> str:
        """
        Run the agent loop for a single user message.

        Returns the final text response from the LLM.
        """
        messages = [{"role": "user", "content": user_message}]

        self._log(f"\n{'='*60}")
        self._log(f"  USER: {user_message}")
        self._log(f"{'='*60}")

        for iteration in range(1, MAX_ITERATIONS + 1):
            response = self.client.messages.create(
                model=MODEL,
                max_tokens=MAX_TOKENS,
                system=SYSTEM_PROMPT,
                tools=TOOL_SCHEMAS,
                messages=messages,
            )

            self._log(f"\n  [iteration {iteration}, stop_reason: {response.stop_reason}]")

            # ── Done: model produced a final answer ──
            if response.stop_reason == "end_turn":
                final_text = "".join(
                    block.text for block in response.content if block.type == "text"
                )
                self._log(f"\n  AGENT: {final_text}\n")
                return final_text

            # ── Not done: process tool calls ──
            messages.append({"role": "assistant", "content": response.content})

            tool_results = []
            for block in response.content:
                if block.type != "tool_use":
                    continue

                tool_name = block.name
                tool_input = block.input

                self._log(f"    → TOOL CALL:   {tool_name}({json.dumps(tool_input)})")

                # Look up and execute the tool
                func = TOOL_FUNCTIONS.get(tool_name)
                if func is None:
                    result = f"Error: unknown tool '{tool_name}'"
                else:
                    try:
                        result = func(**tool_input)
                    except Exception as e:
                        result = f"Error executing {tool_name}: {e}"

                self._log(f"    ← TOOL RESULT: {result}")

                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result,
                })

            # Feed all tool results back in a single user turn
            messages.append({"role": "user", "content": tool_results})

        # Safety cap reached
        return "[Agent stopped: reached maximum iteration limit]"

    def _log(self, msg: str):
        if self.verbose:
            print(msg, file=sys.stderr)


# ─── CLI ──────────────────────────────────────────────────────────────────────

def repl(agent: Agent):
    """Interactive read-eval-print loop."""
    print("Simple AI Agent (type 'quit' to exit)\n")
    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye.")
            break

        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit"):
            print("Bye.")
            break

        response = agent.run(user_input)
        print(f"\nAgent: {response}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Run a simple AI agent with tool use."
    )
    parser.add_argument(
        "--query", "-q",
        type=str,
        default=None,
        help="Single query to run (omit for interactive mode).",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress tool-call tracing output.",
    )
    args = parser.parse_args()

    agent = Agent(verbose=not args.quiet)

    if args.query:
        response = agent.run(args.query)
        print(response)
    else:
        repl(agent)


if __name__ == "__main__":
    main()
