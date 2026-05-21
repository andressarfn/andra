from __future__ import annotations

import pytest

from andra_core.models.chat import ChatRequest, ChatResponse
from andra_core.models.context import ExecutionContext
from andra_core.providers.mock import MockLLMProvider


@pytest.fixture
def provider() -> MockLLMProvider:
    return MockLLMProvider()


@pytest.fixture
def request_fixture() -> ChatRequest:
    return ChatRequest(conversation_id="conv-001", user_message="Hello!")


@pytest.fixture
def context() -> ExecutionContext:
    return ExecutionContext(conversation_id="conv-001")


class TestMockLLMProvider:
    def test_returns_chat_response(
        self,
        provider: MockLLMProvider,
        request_fixture: ChatRequest,
        context: ExecutionContext,
    ) -> None:
        response = provider.complete(request_fixture, context)
        assert isinstance(response, ChatResponse)

    def test_default_template_produces_expected_output(
        self,
        provider: MockLLMProvider,
        request_fixture: ChatRequest,
        context: ExecutionContext,
    ) -> None:
        response = provider.complete(request_fixture, context)
        expected = f"Mock response to: {request_fixture.user_message}"
        assert response.assistant_message == expected

    def test_default_template_includes_user_message(
        self,
        provider: MockLLMProvider,
        request_fixture: ChatRequest,
        context: ExecutionContext,
    ) -> None:
        response = provider.complete(request_fixture, context)
        assert request_fixture.user_message in response.assistant_message

    def test_custom_template_is_used(
        self, request_fixture: ChatRequest, context: ExecutionContext
    ) -> None:
        provider = MockLLMProvider(response_template="Custom: {message}")
        response = provider.complete(request_fixture, context)
        assert response.assistant_message == f"Custom: {request_fixture.user_message}"

    def test_response_preserves_conversation_id(
        self,
        provider: MockLLMProvider,
        request_fixture: ChatRequest,
        context: ExecutionContext,
    ) -> None:
        response = provider.complete(request_fixture, context)
        assert response.conversation_id == request_fixture.conversation_id

    def test_response_metadata_has_provider_key(
        self,
        provider: MockLLMProvider,
        request_fixture: ChatRequest,
        context: ExecutionContext,
    ) -> None:
        response = provider.complete(request_fixture, context)
        assert response.metadata.get("provider") == "mock"

    def test_different_messages_produce_different_responses(
        self, provider: MockLLMProvider, context: ExecutionContext
    ) -> None:
        req_a = ChatRequest(conversation_id="conv-a", user_message="Hello")
        req_b = ChatRequest(conversation_id="conv-b", user_message="Goodbye")
        assert (
            provider.complete(req_a, context).assistant_message
            != provider.complete(req_b, context).assistant_message
        )
