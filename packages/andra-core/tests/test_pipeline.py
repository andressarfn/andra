from __future__ import annotations

import pytest

from andra_core.agents.simple import SimpleAgent
from andra_core.contracts.agent import BaseAgent
from andra_core.contracts.guardrail import BaseGuardrail
from andra_core.contracts.llm_provider import BaseLLMProvider
from andra_core.exceptions.core import GuardrailViolationError, PipelineError
from andra_core.guardrails.default import DefaultGuardrail
from andra_core.memory.in_memory import InMemoryMemoryStore
from andra_core.models.agent import AgentResult
from andra_core.models.chat import ChatMessage, ChatRequest, ChatResponse, MessageRole
from andra_core.models.context import ExecutionContext
from andra_core.models.guardrail import GuardrailResult
from andra_core.pipeline.default import DefaultConversationPipeline
from andra_core.providers.mock import MockLLMProvider

# ---------------------------------------------------------------------------
# Spy / stub helpers
# ---------------------------------------------------------------------------


class SpyAgent(BaseAgent):
    """Agent that records whether it was called."""

    def __init__(self) -> None:
        self.called = False
        self._inner = SimpleAgent()

    @property
    def name(self) -> str:
        return "spy_agent"

    def run(self, request: ChatRequest, context: ExecutionContext) -> AgentResult:
        self.called = True
        return self._inner.run(request, context)


class SpyProvider(BaseLLMProvider):
    """Provider that records whether it was called."""

    def __init__(self) -> None:
        self.called = False
        self._inner = MockLLMProvider()

    def complete(self, request: ChatRequest, context: ExecutionContext) -> ChatResponse:
        self.called = True
        return self._inner.complete(request, context)


class FailingAgent(BaseAgent):
    @property
    def name(self) -> str:
        return "failing_agent"

    def run(self, request: ChatRequest, context: ExecutionContext) -> AgentResult:
        raise RuntimeError("agent failure")


class FailingProvider(BaseLLMProvider):
    def complete(self, request: ChatRequest, context: ExecutionContext) -> ChatResponse:
        raise RuntimeError("provider failure")


class RejectAllGuardrail(BaseGuardrail):
    """Guardrail that always blocks, regardless of content."""

    @property
    def name(self) -> str:
        return "reject_all"

    def validate(self, text: str, context: ExecutionContext) -> GuardrailResult:
        return GuardrailResult(
            passed=False, guardrail_name=self.name, reason="rejected"
        )


class BlankResponseProvider(BaseLLMProvider):
    """Returns a whitespace-only message to trigger the output guardrail."""

    def complete(self, request: ChatRequest, context: ExecutionContext) -> ChatResponse:
        return ChatResponse(
            conversation_id=request.conversation_id,
            assistant_message="   ",
        )


# ---------------------------------------------------------------------------
# Happy path
# ---------------------------------------------------------------------------


class TestPipelineHappyPath:
    def test_happy_path_returns_chat_response(self, basic_request: ChatRequest) -> None:
        pipeline = DefaultConversationPipeline(
            provider=MockLLMProvider(),
            agent=SimpleAgent(),
        )
        response = pipeline.run(basic_request)
        assert isinstance(response, ChatResponse)

    def test_response_has_correct_conversation_id(
        self, basic_request: ChatRequest
    ) -> None:
        pipeline = DefaultConversationPipeline(
            provider=MockLLMProvider(),
            agent=SimpleAgent(),
        )
        response = pipeline.run(basic_request)
        assert response.conversation_id == basic_request.conversation_id

    def test_response_has_non_empty_assistant_message(
        self, basic_request: ChatRequest
    ) -> None:
        pipeline = DefaultConversationPipeline(
            provider=MockLLMProvider(),
            agent=SimpleAgent(),
        )
        response = pipeline.run(basic_request)
        assert response.assistant_message.strip()

    def test_pipeline_without_guardrails_works(
        self, basic_request: ChatRequest
    ) -> None:
        pipeline = DefaultConversationPipeline(
            provider=MockLLMProvider(),
            agent=SimpleAgent(),
            guardrails=[],
        )
        response = pipeline.run(basic_request)
        assert isinstance(response, ChatResponse)


# ---------------------------------------------------------------------------
# Integration: agent and provider are called in order
# ---------------------------------------------------------------------------


class TestPipelineIntegration:
    def test_pipeline_calls_agent(self, basic_request: ChatRequest) -> None:
        spy_agent = SpyAgent()
        pipeline = DefaultConversationPipeline(
            provider=MockLLMProvider(),
            agent=spy_agent,
        )
        pipeline.run(basic_request)
        assert spy_agent.called

    def test_pipeline_calls_provider(self, basic_request: ChatRequest) -> None:
        spy_provider = SpyProvider()
        pipeline = DefaultConversationPipeline(
            provider=spy_provider,
            agent=SimpleAgent(),
        )
        pipeline.run(basic_request)
        assert spy_provider.called

    def test_pipeline_calls_agent_before_provider(
        self, basic_request: ChatRequest
    ) -> None:
        call_order: list[str] = []

        class OrderedAgent(BaseAgent):
            @property
            def name(self) -> str:
                return "ordered_agent"

            def run(
                self, request: ChatRequest, context: ExecutionContext
            ) -> AgentResult:
                call_order.append("agent")
                return AgentResult(content=request.user_message, agent_name=self.name)

        class OrderedProvider(BaseLLMProvider):
            def complete(
                self, request: ChatRequest, context: ExecutionContext
            ) -> ChatResponse:
                call_order.append("provider")
                return ChatResponse(
                    conversation_id=request.conversation_id, assistant_message="ok"
                )

        pipeline = DefaultConversationPipeline(
            provider=OrderedProvider(),
            agent=OrderedAgent(),
        )
        pipeline.run(basic_request)
        assert call_order == ["agent", "provider"]


# ---------------------------------------------------------------------------
# Memory
# ---------------------------------------------------------------------------


class TestPipelineMemory:
    def test_pipeline_without_memory_store_works(
        self, basic_request: ChatRequest
    ) -> None:
        pipeline = DefaultConversationPipeline(
            provider=MockLLMProvider(),
            agent=SimpleAgent(),
            memory_store=None,
        )
        response = pipeline.run(basic_request)
        assert isinstance(response, ChatResponse)

    def test_pipeline_loads_history_into_context(
        self, basic_request: ChatRequest
    ) -> None:
        memory = InMemoryMemoryStore()
        memory.append(
            basic_request.conversation_id,
            ChatMessage(role=MessageRole.USER, content="Previous message"),
        )

        received_history: list[ChatMessage] = []

        class HistoryCapturingAgent(BaseAgent):
            @property
            def name(self) -> str:
                return "capturing_agent"

            def run(
                self, request: ChatRequest, context: ExecutionContext
            ) -> AgentResult:
                received_history.extend(context.history)
                return AgentResult(content=request.user_message, agent_name=self.name)

        pipeline = DefaultConversationPipeline(
            provider=MockLLMProvider(),
            agent=HistoryCapturingAgent(),
            memory_store=memory,
        )
        pipeline.run(basic_request)

        assert len(received_history) == 1
        assert received_history[0].content == "Previous message"

    def test_pipeline_persists_user_and_assistant_messages(
        self, basic_request: ChatRequest
    ) -> None:
        memory = InMemoryMemoryStore()
        pipeline = DefaultConversationPipeline(
            provider=MockLLMProvider(),
            agent=SimpleAgent(),
            memory_store=memory,
        )
        pipeline.run(basic_request)

        history = memory.get_history(basic_request.conversation_id)
        assert len(history) == 2
        assert history[0].role == MessageRole.USER
        assert history[0].content == basic_request.user_message
        assert history[1].role == MessageRole.ASSISTANT

    def test_pipeline_does_not_persist_on_input_guardrail_failure(
        self, basic_request: ChatRequest
    ) -> None:
        memory = InMemoryMemoryStore()
        pipeline = DefaultConversationPipeline(
            provider=MockLLMProvider(),
            agent=SimpleAgent(),
            guardrails=[RejectAllGuardrail()],
            memory_store=memory,
        )
        with pytest.raises(GuardrailViolationError):
            pipeline.run(basic_request)

        assert memory.get_history(basic_request.conversation_id) == []


# ---------------------------------------------------------------------------
# Guardrails
# ---------------------------------------------------------------------------


class TestPipelineGuardrails:
    def test_input_guardrail_violation_raises_guardrail_error(
        self, basic_request: ChatRequest
    ) -> None:
        pipeline = DefaultConversationPipeline(
            provider=MockLLMProvider(),
            agent=SimpleAgent(),
            guardrails=[RejectAllGuardrail()],
        )
        with pytest.raises(GuardrailViolationError):
            pipeline.run(basic_request)

    def test_output_guardrail_violation_raises_guardrail_error(
        self, basic_request: ChatRequest
    ) -> None:
        pipeline = DefaultConversationPipeline(
            provider=BlankResponseProvider(),
            agent=SimpleAgent(),
            guardrails=[DefaultGuardrail()],
        )
        with pytest.raises(GuardrailViolationError):
            pipeline.run(basic_request)

    def test_guardrail_violation_exposes_guardrail_name(
        self, basic_request: ChatRequest
    ) -> None:
        pipeline = DefaultConversationPipeline(
            provider=MockLLMProvider(),
            agent=SimpleAgent(),
            guardrails=[RejectAllGuardrail()],
        )
        with pytest.raises(GuardrailViolationError) as exc_info:
            pipeline.run(basic_request)
        assert exc_info.value.guardrail_name == "reject_all"

    def test_input_guardrail_violation_includes_stage_in_reason(
        self, basic_request: ChatRequest
    ) -> None:
        pipeline = DefaultConversationPipeline(
            provider=MockLLMProvider(),
            agent=SimpleAgent(),
            guardrails=[RejectAllGuardrail()],
        )
        with pytest.raises(GuardrailViolationError) as exc_info:
            pipeline.run(basic_request)
        assert "[input]" in exc_info.value.reason

    def test_output_guardrail_violation_includes_stage_in_reason(
        self, basic_request: ChatRequest
    ) -> None:
        pipeline = DefaultConversationPipeline(
            provider=BlankResponseProvider(),
            agent=SimpleAgent(),
            guardrails=[DefaultGuardrail()],
        )
        with pytest.raises(GuardrailViolationError) as exc_info:
            pipeline.run(basic_request)
        assert "[output]" in exc_info.value.reason


# ---------------------------------------------------------------------------
# Error handling
# ---------------------------------------------------------------------------


class TestPipelineErrors:
    def test_agent_exception_raises_pipeline_error(
        self, basic_request: ChatRequest
    ) -> None:
        pipeline = DefaultConversationPipeline(
            provider=MockLLMProvider(),
            agent=FailingAgent(),
        )
        with pytest.raises(PipelineError):
            pipeline.run(basic_request)

    def test_provider_exception_raises_pipeline_error(
        self, basic_request: ChatRequest
    ) -> None:
        pipeline = DefaultConversationPipeline(
            provider=FailingProvider(),
            agent=SimpleAgent(),
        )
        with pytest.raises(PipelineError):
            pipeline.run(basic_request)

    def test_pipeline_error_wraps_original_cause(
        self, basic_request: ChatRequest
    ) -> None:
        pipeline = DefaultConversationPipeline(
            provider=FailingProvider(),
            agent=SimpleAgent(),
        )
        with pytest.raises(PipelineError) as exc_info:
            pipeline.run(basic_request)
        assert exc_info.value.__cause__ is not None
