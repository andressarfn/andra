import pytest

from andra_core.providers.mock import MockLLMProvider

from andra_framework import (
    Chatbot,
    ChatbotBuilder,
    ChatbotConfigurationError,
    FrameworkSettings,
    MemoryPolicy,
)


class TestChatbotBuilderDefaults:
    def test_build_requires_provider(self) -> None:
        with pytest.raises(ChatbotConfigurationError, match="provider is required"):
            ChatbotBuilder().build()

    def test_build_with_provider_returns_chatbot(
        self, mock_provider: MockLLMProvider
    ) -> None:
        chatbot = ChatbotBuilder().with_provider(mock_provider).build()
        assert isinstance(chatbot, Chatbot)

    def test_default_settings_applied(self, mock_provider: MockLLMProvider) -> None:
        chatbot = ChatbotBuilder().with_provider(mock_provider).build()
        assert chatbot.settings.memory_policy == MemoryPolicy.IN_MEMORY

    def test_custom_settings_applied(self, mock_provider: MockLLMProvider) -> None:
        settings = FrameworkSettings(memory_policy=MemoryPolicy.NONE)
        chatbot = (
            ChatbotBuilder()
            .with_provider(mock_provider)
            .with_settings(settings)
            .build()
        )
        assert chatbot.settings.memory_policy == MemoryPolicy.NONE

    def test_builder_is_fluent(self, mock_provider: MockLLMProvider) -> None:
        builder = ChatbotBuilder()
        result = builder.with_provider(mock_provider)
        assert result is builder

    def test_with_guardrails_accepts_empty_list(
        self, mock_provider: MockLLMProvider
    ) -> None:
        chatbot = (
            ChatbotBuilder().with_provider(mock_provider).with_guardrails([]).build()
        )
        assert isinstance(chatbot, Chatbot)
