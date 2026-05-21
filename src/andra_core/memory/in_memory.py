from __future__ import annotations

from collections import defaultdict

from andra_core.contracts.memory_store import BaseMemoryStore
from andra_core.models.chat import ChatMessage


class InMemoryMemoryStore(BaseMemoryStore):
    """In-memory implementation of BaseMemoryStore.

    Stores conversation history in a plain Python dict. This implementation
    is suitable for development, testing, and single-process deployments.
    It does not persist state across process restarts.
    """

    def __init__(self) -> None:
        self._store: dict[str, list[ChatMessage]] = defaultdict(list)

    def get_history(self, conversation_id: str) -> list[ChatMessage]:
        """Return a shallow copy of the history to prevent external mutation."""
        return list(self._store[conversation_id])

    def append(self, conversation_id: str, message: ChatMessage) -> None:
        self._store[conversation_id].append(message)

    def clear(self, conversation_id: str) -> None:
        self._store[conversation_id] = []
