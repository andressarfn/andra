"""Typed exception hierarchy for andra-core."""


class AndraError(Exception):
    """Base exception for all andra-core errors."""


class PipelineError(AndraError):
    """Raised when the conversation pipeline encounters an unrecoverable error."""


class GuardrailViolationError(AndraError):
    """Raised when a guardrail blocks execution due to a policy violation.

    Attributes:
        guardrail_name: The name of the guardrail that triggered the violation.
        reason: A human-readable explanation of why the content was blocked.
    """

    def __init__(self, guardrail_name: str, reason: str) -> None:
        self.guardrail_name = guardrail_name
        self.reason = reason
        super().__init__(f"Guardrail '{guardrail_name}' blocked execution: {reason}")


class ProviderError(AndraError):
    """Raised when an LLM provider fails to produce a response."""


class MemoryStoreError(AndraError):
    """Raised when a memory store operation fails."""


class AgentError(AndraError):
    """Raised when an agent fails to process a request."""
