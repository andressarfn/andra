from __future__ import annotations

from andra_core.contracts.llm_provider import BaseLLMProvider
from andra_core.models.chat import ChatRequest, ChatResponse
from andra_core.models.context import ExecutionContext


class MockLLMProvider(BaseLLMProvider):
    """Mock LLM provider for development and testing.

    Returns a deterministic echo response without making any external calls.
    This is intentionally simple — it is not a stub for a real provider.

    Args:
        response_template: A string template for the mock response.
            Use ``{message}`` as a placeholder for the user's message.
    """

    DEFAULT_TEMPLATE = "Mock response to: {message}"

    def __init__(self, response_template: str | None = None) -> None:
        self._template = response_template or self.DEFAULT_TEMPLATE

    def complete(self, request: ChatRequest, context: ExecutionContext) -> ChatResponse:
        """Return a mock response without calling any external service."""
        content = self._template.format(
            message=request.user_message,
            conversation_id=request.conversation_id,
        )
        return ChatResponse(
            conversation_id=request.conversation_id,
            assistant_message=content,
            metadata={"provider": "mock"},
        )
