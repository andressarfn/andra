from __future__ import annotations

import pytest

from andra_core.memory.in_memory import InMemoryMemoryStore
from andra_core.models.chat import ChatMessage, MessageRole


@pytest.fixture
def store() -> InMemoryMemoryStore:
    return InMemoryMemoryStore()


@pytest.fixture
def user_msg() -> ChatMessage:
    return ChatMessage(role=MessageRole.USER, content="Hello")


@pytest.fixture
def assistant_msg() -> ChatMessage:
    return ChatMessage(role=MessageRole.ASSISTANT, content="Hi there!")


class TestInMemoryMemoryStore:
    def test_get_history_returns_empty_for_new_conversation(
        self, store: InMemoryMemoryStore
    ) -> None:
        assert store.get_history("brand-new-conv") == []

    def test_append_stores_message(
        self, store: InMemoryMemoryStore, user_msg: ChatMessage
    ) -> None:
        store.append("conv-1", user_msg)
        history = store.get_history("conv-1")
        assert len(history) == 1
        assert history[0] is user_msg

    def test_get_history_returns_messages_in_insertion_order(
        self,
        store: InMemoryMemoryStore,
        user_msg: ChatMessage,
        assistant_msg: ChatMessage,
    ) -> None:
        store.append("conv-1", user_msg)
        store.append("conv-1", assistant_msg)
        history = store.get_history("conv-1")
        assert history[0] is user_msg
        assert history[1] is assistant_msg

    def test_get_history_returns_copy_not_reference(
        self, store: InMemoryMemoryStore, user_msg: ChatMessage
    ) -> None:
        store.append("conv-1", user_msg)
        returned = store.get_history("conv-1")
        returned.clear()
        assert len(store.get_history("conv-1")) == 1

    def test_clear_empties_history(
        self, store: InMemoryMemoryStore, user_msg: ChatMessage
    ) -> None:
        store.append("conv-1", user_msg)
        store.clear("conv-1")
        assert store.get_history("conv-1") == []

    def test_clear_unknown_conversation_does_not_raise(
        self, store: InMemoryMemoryStore
    ) -> None:
        store.clear("never-used-conv")
        assert store.get_history("never-used-conv") == []

    def test_multiple_conversations_are_isolated(
        self,
        store: InMemoryMemoryStore,
        user_msg: ChatMessage,
        assistant_msg: ChatMessage,
    ) -> None:
        store.append("conv-1", user_msg)
        store.append("conv-2", assistant_msg)

        assert len(store.get_history("conv-1")) == 1
        assert len(store.get_history("conv-2")) == 1
        assert store.get_history("conv-1")[0] is user_msg
        assert store.get_history("conv-2")[0] is assistant_msg

    def test_append_accumulates_multiple_messages(
        self, store: InMemoryMemoryStore
    ) -> None:
        for i in range(5):
            store.append(
                "conv-1", ChatMessage(role=MessageRole.USER, content=f"msg {i}")
            )
        assert len(store.get_history("conv-1")) == 5
