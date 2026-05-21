from __future__ import annotations

import pytest

from andra_core.agents.simple import SimpleAgent
from andra_core.guardrails.default import DefaultGuardrail
from andra_core.memory.in_memory import InMemoryMemoryStore
from andra_core.models.chat import ChatRequest
from andra_core.providers.mock import MockLLMProvider


@pytest.fixture
def basic_request() -> ChatRequest:
    return ChatRequest(conversation_id="conv-test", user_message="Hello, Andra!")


@pytest.fixture
def simple_agent() -> SimpleAgent:
    return SimpleAgent()


@pytest.fixture
def mock_provider() -> MockLLMProvider:
    return MockLLMProvider()


@pytest.fixture
def memory_store() -> InMemoryMemoryStore:
    return InMemoryMemoryStore()


@pytest.fixture
def default_guardrail() -> DefaultGuardrail:
    return DefaultGuardrail()
