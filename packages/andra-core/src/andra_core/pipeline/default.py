from __future__ import annotations

from andra_core.contracts.agent import BaseAgent
from andra_core.contracts.guardrail import BaseGuardrail
from andra_core.contracts.llm_provider import BaseLLMProvider
from andra_core.contracts.memory_store import BaseMemoryStore
from andra_core.contracts.pipeline import BaseConversationPipeline
from andra_core.exceptions.core import GuardrailViolationError, PipelineError
from andra_core.models.chat import ChatMessage, ChatRequest, ChatResponse, MessageRole
from andra_core.models.context import ExecutionContext


class DefaultConversationPipeline(BaseConversationPipeline):
    """Default implementation of the conversation pipeline.

    Orchestrates a full conversation turn in the following order:

    1. Create an ExecutionContext for the turn.
    2. Retrieve conversation history from the memory store.
    3. Validate the user's input through all guardrails.
    4. Run the agent to produce an AgentResult.
    5. Ask the LLM provider to generate the final response.
    6. Validate the LLM output through all guardrails.
    7. Persist both the user message and assistant reply to memory.
    8. Return the ChatResponse.

    Args:
        provider: The LLM provider used to generate responses.
        agent: The agent that processes the request before calling the provider.
        guardrails: An ordered list of guardrails applied to both input and output.
        memory_store: The memory backend for conversation history persistence.
    """

    def __init__(
        self,
        provider: BaseLLMProvider,
        agent: BaseAgent,
        guardrails: list[BaseGuardrail] | None = None,
        memory_store: BaseMemoryStore | None = None,
    ) -> None:
        self._provider = provider
        self._agent = agent
        self._guardrails: list[BaseGuardrail] = guardrails or []
        self._memory_store = memory_store

    def run(self, request: ChatRequest) -> ChatResponse:
        """Execute a full conversation turn and return the assistant's response."""
        # Step 1: create execution context
        context = ExecutionContext(conversation_id=request.conversation_id)

        # Step 2: retrieve history from memory
        if self._memory_store is not None:
            context.history = self._memory_store.get_history(request.conversation_id)

        # Step 3: validate input with guardrails
        self._run_guardrails(request.user_message, context, stage="input")

        # Step 4: run the agent
        try:
            _ = self._agent.run(request, context)
        except Exception as exc:
            raise PipelineError(f"Agent '{self._agent.name}' raised an error.") from exc

        # Step 5: generate response from the LLM provider
        # The agent result content enriches the request passed to the provider.
        # For the MVP, the agent acts as a passthrough, so we forward the original
        # request. Future agents may produce a transformed or augmented request.
        try:
            response = self._provider.complete(request, context)
        except Exception as exc:
            raise PipelineError("LLM provider failed to complete the request.") from exc

        # Step 6: validate output with guardrails
        self._run_guardrails(response.assistant_message, context, stage="output")

        # Step 7: persist history
        if self._memory_store is not None:
            self._memory_store.append(
                request.conversation_id,
                ChatMessage(role=MessageRole.USER, content=request.user_message),
            )
            self._memory_store.append(
                request.conversation_id,
                ChatMessage(
                    role=MessageRole.ASSISTANT, content=response.assistant_message
                ),
            )

        return response

    def _run_guardrails(
        self,
        text: str,
        context: ExecutionContext,
        stage: str,
    ) -> None:
        """Run all guardrails against the given text.

        Raises:
            GuardrailViolationError: If any guardrail blocks the content.
        """
        for guardrail in self._guardrails:
            result = guardrail.validate(text, context)
            if not result.passed:
                raise GuardrailViolationError(
                    guardrail_name=result.guardrail_name,
                    reason=f"[{stage}] {result.reason}",
                )
