from __future__ import annotations

from abc import ABC, abstractmethod

from andra_core.models.chat import ChatRequest, ChatResponse


class BaseConversationPipeline(ABC):
    """Port for the conversation pipeline.

    The pipeline orchestrates all steps of a conversation turn:
    context creation, memory retrieval, guardrail validation,
    agent execution, LLM completion, and history persistence.
    """

    @abstractmethod
    def run(self, request: ChatRequest) -> ChatResponse:
        """Execute a full conversation turn.

        Args:
            request: The chat request from the user.

        Returns:
            A ChatResponse with the assistant's reply.
        """
        ...
