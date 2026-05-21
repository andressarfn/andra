from __future__ import annotations

from andra_core.agents.simple import SimpleAgent
from andra_core.contracts.agent import BaseAgent
from andra_core.contracts.guardrail import BaseGuardrail
from andra_core.contracts.llm_provider import BaseLLMProvider
from andra_core.contracts.memory_store import BaseMemoryStore
from andra_core.memory.in_memory import InMemoryMemoryStore
from andra_core.pipeline.default import DefaultConversationPipeline

from andra_framework.chatbot import Chatbot
from andra_framework.config.settings import FrameworkSettings
from andra_framework.exceptions.framework_errors import ChatbotConfigurationError
from andra_framework.policies.memory_policy import MemoryPolicy


class ChatbotBuilder:
    """Fluent builder for constructing a configured Chatbot instance.

    Usage::

        chatbot = (
            ChatbotBuilder()
            .with_provider(my_provider)
            .with_guardrails([DefaultGuardrail()])
            .build()
        )

    Only with_provider() is required. All other options have sensible defaults:
    - agent: SimpleAgent (passthrough)
    - guardrails: none
    - settings: FrameworkSettings() with IN_MEMORY memory policy
    """

    def __init__(self) -> None:
        self._provider: BaseLLMProvider | None = None
        self._agent: BaseAgent | None = None
        self._guardrails: list[BaseGuardrail] = []
        self._settings: FrameworkSettings = FrameworkSettings()

    def with_provider(self, provider: BaseLLMProvider) -> ChatbotBuilder:
        """Set the LLM provider used to generate responses."""
        self._provider = provider
        return self

    def with_agent(self, agent: BaseAgent) -> ChatbotBuilder:
        """Override the default agent (SimpleAgent) with a custom one."""
        self._agent = agent
        return self

    def with_guardrails(self, guardrails: list[BaseGuardrail]) -> ChatbotBuilder:
        """Set the list of guardrails applied to input and output."""
        self._guardrails = list(guardrails)
        return self

    def with_settings(self, settings: FrameworkSettings) -> ChatbotBuilder:
        """Override the default framework settings."""
        self._settings = settings
        return self

    def build(self) -> Chatbot:
        """Build and return a configured Chatbot.

        Raises:
            ChatbotConfigurationError: If no provider has been set.
        """
        if self._provider is None:
            raise ChatbotConfigurationError(
                "A provider is required. Call with_provider() before build()."
            )

        agent = self._agent or SimpleAgent()
        memory_store = self._resolve_memory_store()

        pipeline = DefaultConversationPipeline(
            provider=self._provider,
            agent=agent,
            guardrails=self._guardrails,
            memory_store=memory_store,
        )

        return Chatbot(pipeline=pipeline, settings=self._settings)

    def _resolve_memory_store(self) -> BaseMemoryStore | None:
        if self._settings.memory_policy == MemoryPolicy.NONE:
            return None
        return InMemoryMemoryStore()
