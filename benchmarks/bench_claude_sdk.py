"""Claude Agent SDK (boucle d'agent de Claude Code)."""

import asyncio

from claude_agent_sdk import (
    ClaudeAgentOptions,
    ResultMessage,
    create_sdk_mcp_server,
    query,
    tool,
)

import common
from common import QUESTION, SYSTEM_PROMPT, Reponse


@tool("utc_now", "Return the current UTC timestamp in ISO format.", {})
async def utc_now(args):
    return {"content": [{"type": "text", "text": common.utc_now()}]}


@tool("multiply", "Multiply two integers.", {"a": int, "b": int})
async def multiply(args):
    return {"content": [{"type": "text", "text": str(common.multiply(args["a"], args["b"]))}]}


options = ClaudeAgentOptions(
    system_prompt=SYSTEM_PROMPT,
    mcp_servers={"bench": create_sdk_mcp_server("bench", tools=[utc_now, multiply])},
    allowed_tools=["mcp__bench__utc_now", "mcp__bench__multiply"],
    tools=[],  # aucun outil natif de Claude Code (Bash, Read, ...)
    setting_sources=[],
    output_format={"type": "json_schema", "schema": Reponse.model_json_schema()},
    max_turns=6,
)


async def main() -> Reponse:
    async for msg in query(prompt=QUESTION, options=options):
        if isinstance(msg, ResultMessage):
            return Reponse.model_validate(msg.structured_output)
    raise RuntimeError("Pas de résultat")


if __name__ == "__main__":
    print(asyncio.run(main()))
