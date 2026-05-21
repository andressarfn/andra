from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone

from andra_core.models.chat import ChatMessage


@dataclass
class ExecutionContext:
    """Carries state and metadata throughout a single pipeline execution."""

    conversation_id: str
    execution_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    history: list[ChatMessage] = field(default_factory=list)
    metadata: dict[str, str] = field(default_factory=dict)
    started_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
