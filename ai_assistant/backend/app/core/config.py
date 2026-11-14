from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # Database Settings
    db_username: str
    db_password: str
    db_host: str
    db_port: int
    database_name: str

    # LLM Settings
    chat_api_key: str
    chat_model: str
    chat_api_base_url: str
    chat_temperature: float = 0.0
    chat_provider: Literal["openai-compatible", "bharatcode"] = "openai-compatible"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
