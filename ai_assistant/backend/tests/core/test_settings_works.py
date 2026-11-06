from app.core.config import Settings


def test_settings_work(tmp_path):
    env_file = tmp_path / "test.env"

    env_file.write_text(
        """ 
        CHAT_API_KEY=test-api-key
        CHAT_MODEL=test-model
        CHAT_API_BASE_URL=https://test_api_url/v1
        CHAT_TEMPERATURE=0
        """
    )

    settings = Settings(_env_file=env_file)

    assert settings.chat_api_key == "test-api-key"
    assert settings.chat_model == "test-model"
    assert settings.chat_api_base_url == "https://test_api_url/v1"
    assert settings.chat_temperature == "0"

