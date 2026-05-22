import pytest

from andra_framework import Chatbot, ChatbotBuilder, MockProvider


@pytest.fixture()
def mock_provider() -> MockProvider:
    return MockProvider()


@pytest.fixture()
def chatbot(mock_provider: MockProvider) -> Chatbot:
    return ChatbotBuilder().with_provider(mock_provider).build()
