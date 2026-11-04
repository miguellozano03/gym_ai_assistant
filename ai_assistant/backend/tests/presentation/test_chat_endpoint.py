from fastapi.testclient import TestClient

from app.infrastructure.ai.agent import GymAssistantAgent
from app.presentation.api.dependencies import (
    create_gym_assistant_agent,
    get_gym_assistant_agent,
)
from app.presentation.main import app


class FakeGymAssistant:
    def __init__(self, reply: str = "Extreme Gym has the requested information."):
        self.reply = reply

    def run(self, message: str) -> str:
        return self.reply


def test_chat_endpoint_returns_agent_reply():
    client = TestClient(app)
    app.dependency_overrides[get_gym_assistant_agent] = lambda: FakeGymAssistant(
        reply="We are open on Monday from 6 AM to 11 AM and 3 PM to 8 PM."
    )

    try:
        response = client.post(
            "/chat",
            json={"message": "What are Monday opening hours?"},
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == {
        "reply": "We are open on Monday from 6 AM to 11 AM and 3 PM to 8 PM."
    }


def test_chat_endpoint_rejects_blank_message():
    client = TestClient(app)
    app.dependency_overrides[get_gym_assistant_agent] = lambda: FakeGymAssistant()

    try:
        response = client.post("/chat", json={"message": "   "})
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 422


def test_create_gym_assistant_agent_from_grok_environment(monkeypatch):
    monkeypatch.setenv("CHAT_API_KEY", "test-grok-key")
    monkeypatch.setenv("CHAT_MODEL", "grok-test-model")
    monkeypatch.setenv("CHAT_API_BASE_URL", "https://api.x.ai/v1")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    create_gym_assistant_agent.cache_clear()

    try:
        agent = create_gym_assistant_agent()
    finally:
        create_gym_assistant_agent.cache_clear()

    assert isinstance(agent, GymAssistantAgent)
    assert agent.model.model_name == "grok-test-model"
    assert str(agent.model.openai_api_base) == "https://api.x.ai/v1"
