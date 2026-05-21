from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class GuardrailResult:
    """Result of a guardrail validation step."""

    passed: bool
    guardrail_name: str
    reason: str = ""
    metadata: dict[str, str] = field(default_factory=dict)
