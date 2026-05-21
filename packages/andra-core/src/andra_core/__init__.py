"""
andra-core — Core library for the Andra LLM chatbot ecosystem.

Public API surface:

Models:
    ChatMessage, ChatRequest, ChatResponse, ExecutionContext,
    GuardrailResult, AgentResult, MessageRole

Contracts (abstract interfaces):
    BaseLLMProvider, BaseAgent, BaseGuardrail,
    BaseMemoryStore, BaseConversationPipeline

Pipeline:
    DefaultConversationPipeline

Memory:
    InMemoryMemoryStore

Providers:
    MockLLMProvider

Agents:
    SimpleAgent

Guardrails:
    DefaultGuardrail

Exceptions:
    AndraError, PipelineError, GuardrailViolationError,
    ProviderError, MemoryStoreError, AgentError
"""

__version__ = "0.1.0"

from andra_core.agents import SimpleAgent
from andra_core.contracts import (
    BaseAgent,
    BaseConversationPipeline,
    BaseGuardrail,
    BaseLLMProvider,
    BaseMemoryStore,
)
from andra_core.exceptions import (
    AgentError,
    AndraError,
    GuardrailViolationError,
    MemoryStoreError,
    PipelineError,
    ProviderError,
)
from andra_core.guardrails import DefaultGuardrail
from andra_core.memory import InMemoryMemoryStore
from andra_core.models import (
    AgentResult,
    ChatMessage,
    ChatRequest,
    ChatResponse,
    ExecutionContext,
    GuardrailResult,
    MessageRole,
)
from andra_core.pipeline import DefaultConversationPipeline
from andra_core.providers import MockLLMProvider

__all__ = [
    # version
    "__version__",
    # models
    "AgentResult",
    "ChatMessage",
    "ChatRequest",
    "ChatResponse",
    "ExecutionContext",
    "GuardrailResult",
    "MessageRole",
    # contracts
    "BaseAgent",
    "BaseConversationPipeline",
    "BaseGuardrail",
    "BaseLLMProvider",
    "BaseMemoryStore",
    # pipeline
    "DefaultConversationPipeline",
    # memory
    "InMemoryMemoryStore",
    # providers
    "MockLLMProvider",
    # agents
    "SimpleAgent",
    # guardrails
    "DefaultGuardrail",
    # exceptions
    "AgentError",
    "AndraError",
    "GuardrailViolationError",
    "MemoryStoreError",
    "PipelineError",
    "ProviderError",
]
