from andra_core.contracts.agent import BaseAgent
from andra_core.contracts.guardrail import BaseGuardrail
from andra_core.contracts.llm_provider import BaseLLMProvider
from andra_core.contracts.memory_store import BaseMemoryStore
from andra_core.exceptions.core import GuardrailViolationError, PipelineError
from andra_core.guardrails.default import DefaultGuardrail
from andra_core.models.agent import AgentResult
from andra_core.models.chat import ChatMessage, ChatRequest, ChatResponse, MessageRole
from andra_core.models.context import ExecutionContext
from andra_core.models.guardrail import GuardrailResult

from andra_framework.providers.mock import MockProvider

from andra_framework.builders.chatbot_builder import ChatbotBuilder
from andra_framework.chatbot import Chatbot
from andra_framework.config.settings import FrameworkSettings
from andra_framework.exceptions.framework_errors import (
    ChatbotConfigurationError,
    FrameworkError,
)
from andra_framework.policies.memory_policy import MemoryPolicy

__all__ = [
    # Core framework classes
    "Chatbot",
    "ChatbotBuilder",
    "FrameworkSettings",
    "MemoryPolicy",
    # Exceptions — catch these without importing from andra_core
    "FrameworkError",
    "ChatbotConfigurationError",
    "PipelineError",
    "GuardrailViolationError",
    # Built-in providers and guardrails
    "MockProvider",
    "DefaultGuardrail",
    # Extension API — subclass these to build custom providers, agents, guardrails
    "BaseLLMProvider",
    "BaseAgent",
    "BaseGuardrail",
    "BaseMemoryStore",
    # Data models — used in method signatures and return types
    "ChatRequest",
    "ChatResponse",
    "ChatMessage",
    "MessageRole",
    "ExecutionContext",
    "AgentResult",
    "GuardrailResult",
]
