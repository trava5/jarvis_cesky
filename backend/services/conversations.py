"""Repository rozhrani pro konverzacni relace."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from threading import Lock
from uuid import uuid4

from backend.schemas import ConversationDetail, ConversationSummary, StoredMessage


@dataclass
class ConversationRecord:
    conversation_id: str
    channel: str
    client_id: str | None
    created_at: datetime
    updated_at: datetime
    messages: list[StoredMessage] = field(default_factory=list)


class ConversationRepository(ABC):
    """Rozhrani uloziste konverzacnich relaci."""

    @abstractmethod
    def get_or_create(
        self,
        conversation_id: str | None,
        channel: str,
        client_id: str | None,
    ) -> ConversationRecord:
        raise NotImplementedError

    @abstractmethod
    def append_message(
        self,
        conversation_id: str,
        role: str,
        text: str,
        channel: str,
        client_id: str | None,
        status: str | None = None,
    ) -> StoredMessage:
        raise NotImplementedError

    @abstractmethod
    def get(self, conversation_id: str) -> ConversationDetail | None:
        raise NotImplementedError

    @abstractmethod
    def list(self) -> list[ConversationSummary]:
        raise NotImplementedError


class InMemoryConversationRepository(ConversationRepository):
    """In-memory repository pro MIG-003 pred zapojenim PostgreSQL."""

    def __init__(self) -> None:
        self._records: dict[str, ConversationRecord] = {}
        self._lock = Lock()

    def get_or_create(
        self,
        conversation_id: str | None,
        channel: str,
        client_id: str | None,
    ) -> ConversationRecord:
        now = datetime.now(timezone.utc)
        with self._lock:
            if conversation_id and conversation_id in self._records:
                record = self._records[conversation_id]
                record.updated_at = now
                return record

            new_id = conversation_id or f"conv_{uuid4().hex}"
            record = ConversationRecord(
                conversation_id=new_id,
                channel=channel,
                client_id=client_id,
                created_at=now,
                updated_at=now,
            )
            self._records[new_id] = record
            return record

    def append_message(
        self,
        conversation_id: str,
        role: str,
        text: str,
        channel: str,
        client_id: str | None,
        status: str | None = None,
    ) -> StoredMessage:
        now = datetime.now(timezone.utc)
        message = StoredMessage(
            message_id=f"msg_{uuid4().hex}",
            role=role,
            text=text,
            channel=channel,
            client_id=client_id,
            created_at=now,
            status=status,
        )
        with self._lock:
            record = self._records[conversation_id]
            record.messages.append(message)
            record.updated_at = now
        return message

    def get(self, conversation_id: str) -> ConversationDetail | None:
        with self._lock:
            record = self._records.get(conversation_id)
            if not record:
                return None
            return self._to_detail(record)

    def list(self) -> list[ConversationSummary]:
        with self._lock:
            records = sorted(
                self._records.values(),
                key=lambda record: record.updated_at,
                reverse=True,
            )
            return [self._to_summary(record) for record in records]

    @staticmethod
    def _to_summary(record: ConversationRecord) -> ConversationSummary:
        return ConversationSummary(
            conversation_id=record.conversation_id,
            client_id=record.client_id,
            channel=record.channel,
            created_at=record.created_at,
            updated_at=record.updated_at,
            message_count=len(record.messages),
        )

    @classmethod
    def _to_detail(cls, record: ConversationRecord) -> ConversationDetail:
        summary = cls._to_summary(record)
        return ConversationDetail(
            **summary.model_dump(),
            messages=list(record.messages),
        )
