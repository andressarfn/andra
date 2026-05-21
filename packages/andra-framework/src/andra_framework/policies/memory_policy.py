from __future__ import annotations

from enum import Enum


class MemoryPolicy(Enum):
    """Controls how conversation history is stored and retrieved.

    NONE:      No memory. Each conversation turn is stateless.
    IN_MEMORY: Full history kept in-process using InMemoryMemoryStore.
    """

    NONE = "none"
    IN_MEMORY = "in_memory"
