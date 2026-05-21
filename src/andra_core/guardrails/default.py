from __future__ import annotations

from andra_core.contracts.guardrail import BaseGuardrail
from andra_core.models.context import ExecutionContext
from andra_core.models.guardrail import GuardrailResult

# Maximum allowed length for any input or output message.
_MAX_CONTENT_LENGTH = 10_000


class DefaultGuardrail(BaseGuardrail):
    """A minimal guardrail that enforces basic content safety rules.

    Current checks:
    - Rejects empty or whitespace-only content.
    - Rejects content that exceeds a configurable maximum length.

    This guardrail is intentionally permissive. In production, replace or
    extend it with domain-specific rules, PII detection, topic filtering,
    moderation API calls, etc.

    Args:
        max_length: Maximum number of characters allowed. Defaults to 10,000.
    """

    GUARDRAIL_NAME = "default_guardrail"

    def __init__(self, max_length: int = _MAX_CONTENT_LENGTH) -> None:
        self._max_length = max_length

    @property
    def name(self) -> str:
        return self.GUARDRAIL_NAME

    def validate(self, text: str, context: ExecutionContext) -> GuardrailResult:
        """Validate that the text is non-empty and within the length limit."""
        if not text or not text.strip():
            return GuardrailResult(
                passed=False,
                guardrail_name=self.name,
                reason="Content must not be empty.",
            )

        if len(text) > self._max_length:
            return GuardrailResult(
                passed=False,
                guardrail_name=self.name,
                reason=f"Content exceeds maximum allowed length of {self._max_length} characters.",
            )

        return GuardrailResult(passed=True, guardrail_name=self.name)
