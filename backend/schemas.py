"""Datove modely backend API."""

from __future__ import annotations

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

