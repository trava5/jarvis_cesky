"""Datove modely backend API."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class MessageRequest(BaseModel):
    text: str = Field(min_length=1, max_length=12000)
    channel: str = Field(default="api", max_length=64)
    client_id: str | None = Field(default=None, max_length=128)
    conversation_id: str | None = Field(default=None, max_length=128)
    want_audio: bool = False


class MessageResponse(BaseModel):
    status: str
    message_id: str
    conversation_id: str
    text: str
    audio_url: str | None = None
    detail: str | None = None


class StoredMessage(BaseModel):
    message_id: str
    role: str
    text: str
    channel: str
    client_id: str | None = None
    created_at: datetime
    status: str | None = None


class ConversationSummary(BaseModel):
    conversation_id: str
    client_id: str | None = None
    channel: str
    created_at: datetime
    updated_at: datetime
    message_count: int


class ConversationDetail(ConversationSummary):
    messages: list[StoredMessage]
