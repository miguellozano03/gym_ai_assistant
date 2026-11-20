from typing import Annotated

from pydantic import BaseModel, StringConstraints


ChatMessage = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1),
]


class ChatRequest(BaseModel):
    message: ChatMessage


class ChatResponse(BaseModel):
    reply: str
