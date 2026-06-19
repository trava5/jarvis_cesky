"""HTTP API pro serverovy backend JARVIS."""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter

from .config import BackendSettings
from .database import check_database
from .schemas import MessageRequest, MessageResponse
from .services.agent_runtime import AgentRuntime


def create_api_router(settings: BackendSettings) -> APIRouter:
    router = APIRouter(prefix=settings.api_prefix)
    agent_runtime = AgentRuntime()

    @router.get("/health")
    async def health() -> dict:
        return {
            "status": "ok",
            "service": settings.app_name,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    @router.get("/status")
    async def status() -> dict:
        database = await check_database(settings)
        return {
            "status": "ok",
            "service": settings.app_name,
            "api_prefix": settings.api_prefix,
            "agent_runtime": {
                "connected": agent_runtime.state.connected,
                "detail": agent_runtime.state.detail,
            },
            "database": {
                "configured": database.configured,
                "ok": database.ok,
                "detail": database.detail,
            },
        }

    @router.post("/messages", response_model=MessageResponse)
    async def create_message(message: MessageRequest) -> MessageResponse:
        return await agent_runtime.handle_message(message)

    return router
