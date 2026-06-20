"""Factory pro backendova uloziste."""

from __future__ import annotations

from .config import BackendSettings
from .services.conversations import ConversationRepository, InMemoryConversationRepository


def create_conversation_repository(settings: BackendSettings) -> ConversationRepository:
    """Vrati repository pro konverzace.

    PostgreSQL implementace bude doplnena v dalsim kroku MIG-003. Do te doby se
    pouziva in-memory fallback, aby API zustalo funkcni i bez DATABASE_URL.
    """

    return InMemoryConversationRepository()

