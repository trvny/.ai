"""Minimal OpenAI Agents SDK scaffold.

Keep style instructions separate from tools, handoffs, guardrails, sessions,
and tracing. Add capabilities only when the workflow genuinely needs them.
"""

from __future__ import annotations

import os

from agents import Agent, Runner


INSTRUCTIONS = """
Respond naturally and directly. Plain chat is the default mode.

Lead with the answer. Avoid routine praise, corporate filler, theatrical role
claims, and automatic offers of further help. Be honest about uncertainty,
sources, and completed actions.

Use tools only when they are needed for freshness, access, verification, or
execution. Report meaningful actions, results, limitations, and partial
failures without exposing private chain-of-thought or raw telemetry.

Prefer small, reversible changes. Do not create subagents or abstractions when
a direct answer, simple function, or deterministic runtime rule is enough.
""".strip()


agent = Agent(
    name="assistant",
    instructions=INSTRUCTIONS,
    tools=[],
)


def main() -> None:
    """Run one local prompt from the AI_PROMPT environment variable."""
    prompt = os.environ.get("AI_PROMPT", "Summarize what this agent is for.")
    result = Runner.run_sync(agent, prompt)
    print(result.final_output)


if __name__ == "__main__":
    main()
