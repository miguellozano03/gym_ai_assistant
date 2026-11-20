from functools import lru_cache

from app.core.config import Settings
from app.infrastructure.ai.agent import GymAssistantAgent
from app.infrastructure.ai.model_adapter import create_chat_model


@lru_cache(maxsize=1)
def create_gym_assistant_agent() -> GymAssistantAgent:
    chat_model = create_chat_model(Settings())
    return GymAssistantAgent(model=chat_model)


def get_gym_assistant_agent() -> GymAssistantAgent:
    return create_gym_assistant_agent()
