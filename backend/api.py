"""HTTP API pro serverovy backend JARVIS."""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException

from .config import BackendSettings
from .database import check_database
from .schemas import ConversationDetail, ConversationSummary, MessageRequest, MessageResponse
from .services.agent_runtime import AgentRuntime
from .storage import create_conversation_repository


def create_api_router(settings: BackendSettings) -> APIRouter:
    router = APIRouter(prefix=settings.api_prefix)
    conversations = create_conversation_repository(settings)
    agent_runtime = AgentRuntime(conversations)

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

    @router.get("/conversations", response_model=list[ConversationSummary])
    async def list_conversations() -> list[ConversationSummary]:
        return conversations.list()

    @router.get("/conversations/{conversation_id}", response_model=ConversationDetail)
    async def get_conversation(conversation_id: str) -> ConversationDetail:
        conversation = conversations.get(conversation_id)
        if not conversation:
            raise HTTPException(status_code=404, detail="Konverzacni relace nebyla nalezena.")
        return conversation

    return router
