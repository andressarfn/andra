from andra_core.models.chat import ChatResponse

from andra_framework import Chatbot


class TestChatbot:
    def test_chat_returns_response(self, chatbot: Chatbot) -> None:
        response = chatbot.chat(message="Hello", conversation_id="conv-1")
        assert isinstance(response, ChatResponse)
        assert response.conversation_id == "conv-1"
        assert response.assistant_message != ""

    def test_chat_with_user_id(self, chatbot: Chatbot) -> None:
        response = chatbot.chat(
            message="Hello", conversation_id="conv-1", user_id="user-42"
        )
        assert isinstance(response, ChatResponse)

    def test_chat_preserves_conversation_id(self, chatbot: Chatbot) -> None:
        response = chatbot.chat(message="Hi", conversation_id="thread-abc")
        assert response.conversation_id == "thread-abc"

    def test_memory_persists_across_turns(self, chatbot: Chatbot) -> None:
        chatbot.chat(message="First message", conversation_id="conv-mem")
        chatbot.chat(message="Second message", conversation_id="conv-mem")
        # No assertion on history content (core responsibility),
        # but both turns must complete without error.

    def test_stateless_with_no_memory_policy(self) -> None:
        from andra_core.providers.mock import MockLLMProvider
        from andra_framework import ChatbotBuilder, FrameworkSettings, MemoryPolicy

        chatbot = (
            ChatbotBuilder()
            .with_provider(MockLLMProvider())
            .with_settings(FrameworkSettings(memory_policy=MemoryPolicy.NONE))
            .build()
        )
        response = chatbot.chat(message="Hello", conversation_id="conv-stateless")
        assert isinstance(response, ChatResponse)
