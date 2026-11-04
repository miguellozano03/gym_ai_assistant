import os
from functools import lru_cache

from fastapi import HTTPException, status
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

from app.infrastructure.ai.agent import GymAssistantAgent



import os
from functools import lru_cache

from fastapi import HTTPException, status
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

from app.infrastructure.ai.agent import GymAssistantAgent


@lru_cache(maxsize=1)
def create_gym_assistant_agent() -> GymAssistantAgent:
    load_dotenv()

    api_key = os.getenv("CHAT_API_KEY")
    model = os.getenv("CHAT_MODEL")
    base_url = os.getenv("CHAT_API_BASE_URL")

    if not api_key or not model or not base_url:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Chat API configuration is incomplete.",
        )

    chat_model = ChatOpenAI(
        api_key=api_key,
        model=model,
        base_url=base_url,
        temperature=0,
    )

    return GymAssistantAgent(model=chat_model)


def get_gym_assistant_agent() -> GymAssistantAgent:
    return create_gym_assistant_agent()



def get_gym_assistant_agent() -> GymAssistantAgent:
    return create_gym_assistant_agent()
