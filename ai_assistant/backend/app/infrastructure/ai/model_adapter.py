from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI

from app.core.config import Settings


def create_chat_model(settings: Settings) -> BaseChatModel:
    """Create a chat model for an OpenAI-compatible provider."""
    if settings.chat_provider == "bharatcode":
        base_url = settings.chat_api_base_url.rstrip("/")
        if not base_url.endswith("/v1"):
            raise ValueError(
                "BharatCode CHAT_API_BASE_URL must end with /v1."
            )

    return ChatOpenAI(
        api_key=settings.chat_api_key,
        model=settings.chat_model,
        base_url=settings.chat_api_base_url,
        temperature=settings.chat_temperature,
    )
