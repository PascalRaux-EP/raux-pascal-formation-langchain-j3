"""Haystack (composant Agent)."""

from haystack.components.agents import Agent
from haystack.components.generators.chat import OpenAIChatGenerator
from haystack.dataclasses import ChatMessage
from haystack.tools import create_tool_from_function
from haystack.utils import Secret

import common
from common import QUESTION, SYSTEM_PROMPT, Reponse

agent = Agent(
    chat_generator=OpenAIChatGenerator(
        model=common.OPENROUTER_MODEL,
        api_base_url=common.OPENROUTER_URL,
        api_key=Secret.from_token(common.openrouter_key()),
    ),
    tools=[
        create_tool_from_function(common.utc_now),
        create_tool_from_function(common.multiply),
        create_tool_from_function(common.search_docs),
    ],
    system_prompt=SYSTEM_PROMPT,
)

if __name__ == "__main__":
    # Pas de sortie structurée native au niveau Agent : on valide nous-mêmes.
    prompt = QUESTION + f"\nRéponds uniquement en JSON conforme à : {Reponse.model_json_schema()}"
    result = agent.run(messages=[ChatMessage.from_user(prompt)])
    text = result["last_message"].text.strip().removeprefix("```json").removesuffix("```")
    print(Reponse.model_validate_json(text))
