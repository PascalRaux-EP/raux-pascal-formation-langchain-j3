"""PydanticAI."""

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openrouter import OpenRouterProvider

import common
from common import QUESTION, SYSTEM_PROMPT, Reponse

agent = Agent(
    OpenAIChatModel(
        common.OPENROUTER_MODEL,
        provider=OpenRouterProvider(api_key=common.openrouter_key()),
    ),
    output_type=Reponse,
    system_prompt=SYSTEM_PROMPT,
    tools=[common.utc_now, common.multiply, common.search_docs],
)

if __name__ == "__main__":
    print(agent.run_sync(QUESTION).output)
