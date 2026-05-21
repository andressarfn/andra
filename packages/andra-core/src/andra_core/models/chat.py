from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum


class MessageRole(str, Enum):
    """Role of a participant in a conversation."""

    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


@dataclass
class ChatMessage:
    """A single message in a conversation."""

    role: MessageRole
    content: str
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self) -> None:
        if not self.content or not self.content.strip():
            raise ValueError("ChatMessage content must not be empty.")


@dataclass
class ChatRequest:
    """Input to the conversation pipeline."""

    conversation_id: str
    user_message: str
    metadata: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.conversation_id or not self.conversation_id.strip():
            raise ValueError("ChatRequest conversation_id must not be empty.")
        if not self.user_message or not self.user_message.strip():
            raise ValueError("ChatRequest user_message must not be empty.")


@dataclass
class ChatResponse:
    """Output of the conversation pipeline."""

    conversation_id: str
    assistant_message: str
    metadata: dict[str, str] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
