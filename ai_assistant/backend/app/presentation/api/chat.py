import logging
from typing import Protocol

from fastapi import APIRouter, Depends, HTTPException, status

from app.presentation.api.dependencies import get_gym_assistant_agent
from app.presentation.api.schemas import ChatRequest, ChatResponse


logger = logging.getLogger(__name__)

class GymAssistant(Protocol):
    def run(self, message: str) -> str:
        ...


router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    agent: GymAssistant = Depends(get_gym_assistant_agent),
) -> ChatResponse:
    try:
        reply = agent.run(request.message)
    except ValueError as error:
        logger.exception("Unexpected gym assistant error")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(error),
        ) from error
    except Exception as error:
        logger.exception("Unexpected gym assistant error")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="The gym assistant could not process the request.",
        ) from error

    return ChatResponse(reply=reply)
