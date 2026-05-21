from __future__ import annotations

from abc import ABC, abstractmethod

from andra_core.models.context import ExecutionContext
from andra_core.models.guardrail import GuardrailResult


class BaseGuardrail(ABC):
    """Port for guardrail implementations.

    Guardrails validate text content (user input or assistant output)
    against a set of rules (content policy, length limits, topic restrictions, etc.).
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique identifier for this guardrail."""
        ...

    @abstractmethod
    def validate(self, text: str, context: ExecutionContext) -> GuardrailResult:
        """Validate the given text.

        Args:
            text: The text to validate (input or output).
            context: The current execution context.

        Returns:
            A GuardrailResult indicating whether the text passed validation.
        """
        ...
