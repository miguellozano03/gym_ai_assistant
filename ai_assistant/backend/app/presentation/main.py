from fastapi import FastAPI

from app.presentation.ai.api.chat import router as chat_router
from app.presentation.admin.api.routers import admin_router

app = FastAPI(
    title="Gym AI Assistant",
    version="0.1.0",
)

app.include_router(chat_router)
app.include_router(admin_router)
