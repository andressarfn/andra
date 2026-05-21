from __future__ import annotations

from andra_core.contracts.pipeline import BaseConversationPipeline
from andra_core.models.chat import ChatRequest, ChatResponse

from andra_framework.config.settings import FrameworkSettings


class Chatbot:
    """High-level interface for running a conversational AI chatbot.

    Wraps a core pipeline and exposes a simple chat() method that accepts
    plain strings instead of requiring callers to construct ChatRequest objects.

    Args:
        pipeline: The underlying conversation pipeline (core contract).
        settings: Framework-level settings. Defaults to FrameworkSettings().
    """

    def __init__(
        self,
        pipeline: BaseConversationPipeline,
        settings: FrameworkSettings | None = None,
    ) -> None:
        self._pipeline = pipeline
        self._settings = settings or FrameworkSettings()

    @property
    def settings(self) -> FrameworkSettings:
        """The active framework settings for this chatbot."""
        return self._settings

    def chat(
        self,
        message: str,
        conversation_id: str,
        user_id: str | None = None,
    ) -> ChatResponse:
        """Send a message and receive the assistant's response.

        Args:
            message: The user's input message.
            conversation_id: Identifies the ongoing conversation thread.
            user_id: Optional identifier for the end user. Stored in metadata.

        Returns:
            ChatResponse with the assistant's reply.
        """
        metadata: dict[str, str] = {}
        if user_id is not None:
            metadata["user_id"] = user_id

        request = ChatRequest(
            conversation_id=conversation_id,
            user_message=message,
            metadata=metadata,
        )
        return self._pipeline.run(request)
