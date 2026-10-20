"""Deep Agents (LangChain) : harnais avec planification, fichiers, sous-agents."""

from deepagents import create_deep_agent
from langchain.agents.structured_output import ToolStrategy
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool

import common
from common import QUESTION, SYSTEM_PROMPT, Reponse

model = init_chat_model(
    model=common.OPENROUTER_MODEL,
    model_provider="openai",
    base_url=common.OPENROUTER_URL,
    api_key=common.openrouter_key(),
)

agent = create_deep_agent(
    model=model,
    tools=[tool(common.utc_now), tool(common.multiply), tool(common.search_docs)],
    system_prompt=SYSTEM_PROMPT,
    response_format=ToolStrategy(Reponse),
)

if __name__ == "__main__":
    result = agent.invoke({"messages": [("user", QUESTION)]})
    print(result["structured_response"])
