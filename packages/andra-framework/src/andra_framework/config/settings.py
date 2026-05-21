from __future__ import annotations

from dataclasses import dataclass, field

from andra_framework.policies.memory_policy import MemoryPolicy


@dataclass
class FrameworkSettings:
    """Top-level configuration for the Andra framework.

    Attributes:
        memory_policy: Determines how conversation history is stored.
            Defaults to IN_MEMORY (full in-process history).
    """

    memory_policy: MemoryPolicy = field(default=MemoryPolicy.IN_MEMORY)
