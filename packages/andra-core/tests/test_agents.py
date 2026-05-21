from __future__ import annotations

import pytest

from andra_core.agents.simple import SimpleAgent
from andra_core.models.agent import AgentResult
from andra_core.models.chat import ChatRequest
from andra_core.models.context import ExecutionContext


@pytest.fixture
def agent() -> SimpleAgent:
    return SimpleAgent()


@pytest.fixture
def request_fixture() -> ChatRequest:
    return ChatRequest(conversation_id="conv-test", user_message="Hello, agent!")


@pytest.fixture
def context() -> ExecutionContext:
    return ExecutionContext(conversation_id="conv-test")


class TestSimpleAgent:
    def test_agent_name(self, agent: SimpleAgent) -> None:
        assert agent.name == "simple_agent"

    def test_run_returns_agent_result(
        self,
        agent: SimpleAgent,
        request_fixture: ChatRequest,
        context: ExecutionContext,
    ) -> None:
        result = agent.run(request_fixture, context)
        assert isinstance(result, AgentResult)

    def test_run_returns_user_message_as_content(
        self,
        agent: SimpleAgent,
        request_fixture: ChatRequest,
        context: ExecutionContext,
    ) -> None:
        result = agent.run(request_fixture, context)
        assert result.content == request_fixture.user_message

    def test_result_agent_name_matches_agent(
        self,
        agent: SimpleAgent,
        request_fixture: ChatRequest,
        context: ExecutionContext,
    ) -> None:
        result = agent.run(request_fixture, context)
        assert result.agent_name == agent.name

    def test_result_metadata_has_passthrough_strategy(
        self,
        agent: SimpleAgent,
        request_fixture: ChatRequest,
        context: ExecutionContext,
    ) -> None:
        result = agent.run(request_fixture, context)
        assert result.metadata.get("strategy") == "passthrough"

    def test_run_is_deterministic(
        self,
        agent: SimpleAgent,
        request_fixture: ChatRequest,
        context: ExecutionContext,
    ) -> None:
        result_a = agent.run(request_fixture, context)
        result_b = agent.run(request_fixture, context)
        assert result_a.content == result_b.content
        assert result_a.agent_name == result_b.agent_name
