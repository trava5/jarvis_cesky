"""Agentni runtime kontrakt pro backend."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import uuid4

from backend.schemas import MessageRequest, MessageResponse


@dataclass(frozen=True)
class RuntimeState:
    connected: bool = False
    detail: str = "Zivy agentni runtime zatim neni pripojeny k backendu."


class AgentRuntime:
    """Prvni backendova mezivrstva pro budouci sdileny agentni runtime."""

    def __init__(self) -> None:
        self._state = RuntimeState()

    @property
    def state(self) -> RuntimeState:
        return self._state

    async def handle_message(self, request: MessageRequest) -> MessageResponse:
        conversation_id = request.conversation_id or f"conv_{uuid4().hex}"
        message_id = f"msg_{uuid4().hex}"

        if not self._state.connected:
            return MessageResponse(
                status="runtime_unavailable",
                message_id=message_id,
                conversation_id=conversation_id,
                text=(
                    "Backend zpravu prijal, ale zivy agentni runtime je zatim "
                    "spusteny jen v desktopove aplikaci."
                ),
                detail=self._state.detail,
            )

        return MessageResponse(
            status="not_implemented",
            message_id=message_id,
            conversation_id=conversation_id,
            text="Agentni runtime rozhrani je pripravene, implementace odpovedi jeste chybi.",
            detail="Tento stav bude nahrazen napojenim na sdileny agentni runtime.",
        )

