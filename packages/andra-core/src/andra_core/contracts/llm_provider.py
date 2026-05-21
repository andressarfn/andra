from __future__ import annotations

from abc import ABC, abstractmethod

from andra_core.models.chat import ChatRequest, ChatResponse
from andra_core.models.context import ExecutionContext


class BaseLLMProvider(ABC):
    """Port for LLM provider adapters.

    Implement this interface to connect any LLM backend
    (OpenAI, Azure OpenAI, Anthropic, local models, etc.) to the pipeline.
    """

    @abstractmethod
    def complete(self, request: ChatRequest, context: ExecutionContext) -> ChatResponse:
        """Generate a completion for the given request and context.

        Args:
            request: The original chat request from the user.
            context: The current execution context, including conversation history.

        Returns:
            A ChatResponse with the assistant's reply.
        """
        ...
