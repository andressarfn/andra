from __future__ import annotations

from abc import ABC, abstractmethod

from andra_core.models.chat import ChatMessage


class BaseMemoryStore(ABC):
    """Port for conversation memory storage adapters.

    Implement this interface to provide different storage backends
    (in-memory, Redis, database, vector store, etc.).
    """

    @abstractmethod
    def get_history(self, conversation_id: str) -> list[ChatMessage]:
        """Retrieve the conversation history for the given ID.

        Args:
            conversation_id: The unique identifier of the conversation.

        Returns:
            An ordered list of ChatMessage objects, oldest first.
        """
        ...

    @abstractmethod
    def append(self, conversation_id: str, message: ChatMessage) -> None:
        """Append a single message to the conversation history.

        Args:
            conversation_id: The unique identifier of the conversation.
            message: The message to append.
        """
        ...

    @abstractmethod
    def clear(self, conversation_id: str) -> None:
        """Clear the conversation history for the given ID.

        Args:
            conversation_id: The unique identifier of the conversation.
        """
        ...
