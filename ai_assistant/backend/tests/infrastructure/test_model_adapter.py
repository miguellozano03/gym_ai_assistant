import pytest

from app.core.config import Settings
from app.infrastructure.ai.model_adapter import create_chat_model


def test_create_bharatcode_chat_model(tmp_path):
    env_file = tmp_path / "bharatcode.env"
    env_file.write_text(
        """
CHAT_PROVIDER=bharatcode
CHAT_API_KEY=bc_test_key
CHAT_MODEL=qwen-3.8-27b
CHAT_API_BASE_URL=https://bharatcode.ai/api/model/v1
CHAT_TEMPERATURE=0
        """.strip()
    )

    settings = Settings(_env_file=env_file)
    model = create_chat_model(settings)

    assert model.model_name == "qwen-3.8-27b"
    assert str(model.openai_api_base) == "https://bharatcode.ai/api/model/v1"


def test_rejects_invalid_bharatcode_base_url(tmp_path):
    env_file = tmp_path / "bharatcode.env"
    env_file.write_text(
        """
CHAT_PROVIDER=bharatcode
CHAT_API_KEY=bc_test_key
CHAT_MODEL=qwen-3.8-27b
CHAT_API_BASE_URL=https://bharatcode.ai/api/model
CHAT_TEMPERATURE=0
        """.strip()
    )

    settings = Settings(_env_file=env_file)

    with pytest.raises(ValueError, match="/v1"):
        create_chat_model(settings)
