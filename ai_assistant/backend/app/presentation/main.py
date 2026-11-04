from fastapi import FastAPI

from app.presentation.api.chat import router as chat_router


app = FastAPI(
    title="Gym AI Assistant",
    version="0.1.0",
)

app.include_router(chat_router)
