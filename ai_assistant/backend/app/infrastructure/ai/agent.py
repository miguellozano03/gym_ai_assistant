from typing import Any

from langchain.agents import create_agent
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage
from langchain_core.tools import BaseTool

from app.infrastructure.ai.prompt import GYM_ASSISTANT_SYSTEM_PROMPT
from app.infrastructure.ai.tools import create_gym_tools


class GymAssistantAgent:

    def __init__(
        self,
        model: BaseChatModel,
        tools: list[BaseTool] | None = None,
    ):
        self.model = model
        self.tools = tools if tools is not None else create_gym_tools()
        self.agent = create_agent(
            model=self.model,
            tools=self.tools,
            system_prompt=GYM_ASSISTANT_SYSTEM_PROMPT,
        )

    def run(self, message: str) -> str:
        if not isinstance(message, str) or not message.strip():
            raise ValueError("Message cannot be empty")

        result: dict[str, Any] = self.agent.invoke(
            {"messages": [{"role": "user", "content": message}]}
        )
        messages = result.get("messages", [])
        if not messages:
            return "I could not generate a response."

        final_message = messages[-1]
        if isinstance(final_message, AIMessage):
            if isinstance(final_message.content, str):
                return final_message.content
            return str(final_message.content)

        return "I could not generate a response."
