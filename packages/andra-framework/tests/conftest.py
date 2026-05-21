import pytest

from andra_core.providers.mock import MockLLMProvider

from andra_framework import Chatbot, ChatbotBuilder


@pytest.fixture()
def mock_provider() -> MockLLMProvider:
    return MockLLMProvider()


@pytest.fixture()
def chatbot(mock_provider: MockLLMProvider) -> Chatbot:
    return ChatbotBuilder().with_provider(mock_provider).build()
