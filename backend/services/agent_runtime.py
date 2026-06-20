"""Agentni runtime kontrakt pro backend."""

from __future__ import annotations

from dataclasses import dataclass

from backend.schemas import MessageRequest, MessageResponse
from backend.services.conversations import ConversationRepository


@dataclass(frozen=True)
class RuntimeState:
    connected: bool = False
    detail: str = "Zivy agentni runtime zatim neni pripojeny k backendu."


class AgentRuntime:
    """Prvni backendova mezivrstva pro budouci sdileny agentni runtime."""

    def __init__(self, conversations: ConversationRepository) -> None:
        self._state = RuntimeState()
        self._conversations = conversations

    @property
    def state(self) -> RuntimeState:
        return self._state

    async def handle_message(self, request: MessageRequest) -> MessageResponse:
        conversation = await self._conversations.get_or_create(
            conversation_id=request.conversation_id,
            channel=request.channel,
            client_id=request.client_id,
        )
        user_message = await self._conversations.append_message(
            conversation_id=conversation.conversation_id,
            role="user",
            text=request.text,
            channel=request.channel,
            client_id=request.client_id,
            status="received",
        )

        if not self._state.connected:
            text = (
                "Backend zpravu prijal, ale zivy agentni runtime je zatim "
                "spusteny jen v desktopove aplikaci."
            )
            await self._conversations.append_message(
                conversation_id=conversation.conversation_id,
                role="assistant",
                text=text,
                channel=request.channel,
                client_id=request.client_id,
                status="runtime_unavailable",
            )
            return MessageResponse(
                status="runtime_unavailable",
                message_id=user_message.message_id,
                conversation_id=conversation.conversation_id,
                text=text,
                detail=self._state.detail,
            )

        text = "Agentni runtime rozhrani je pripravene, implementace odpovedi jeste chybi."
        await self._conversations.append_message(
            conversation_id=conversation.conversation_id,
            role="assistant",
            text=text,
            channel=request.channel,
            client_id=request.client_id,
            status="not_implemented",
        )
        return MessageResponse(
            status="not_implemented",
            message_id=user_message.message_id,
            conversation_id=conversation.conversation_id,
            text=text,
            detail="Tento stav bude nahrazen napojenim na sdileny agentni runtime.",
        )
