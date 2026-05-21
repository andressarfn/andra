from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class AgentResult:
    """Result produced by an agent after processing a request."""

    content: str
    agent_name: str
    metadata: dict[str, str] = field(default_factory=dict)
