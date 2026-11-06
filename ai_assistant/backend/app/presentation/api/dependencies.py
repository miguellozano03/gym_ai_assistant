from functools import lru_cache
from langchain_openai import ChatOpenAI

from app.core.config import settings
from app.infrastructure.ai.agent import GymAssistantAgent


@lru_cache(maxsize=1)
def create_gym_assistant_agent() -> GymAssistantAgent:

    chat_model = ChatOpenAI(
        api_key=settings.chat_api_key,
        model=settings.chat_model,
        base_url=settings.chat_api_base_url,
        temperature=settings.chat_temperature,
    )

    return GymAssistantAgent(model=chat_model)


def get_gym_assistant_agent() -> GymAssistantAgent:
    return create_gym_assistant_agent()

