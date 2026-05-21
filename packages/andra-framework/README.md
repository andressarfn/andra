# andra-framework

Opinionated framework layer for the **Andra** ecosystem — built on top of [`andra-core`](../andra-core/README.md).

`andra-framework` provides a high-level, batteries-included API for assembling and running LLM-powered chatbots, without requiring callers to wire up core contracts manually.

---

## Relationship to andra-core

| Package | Role |
|---|---|
| `andra-core` | Framework-agnostic building blocks (contracts, pipeline, models) |
| `andra-framework` | Opinionated layer — sensible defaults, fluent builder, simplified API |

---

## Quick Start

```python
from andra_core.providers.mock import MockLLMProvider  # swap for a real provider
from andra_framework import ChatbotBuilder, FrameworkSettings, MemoryPolicy

chatbot = (
    ChatbotBuilder()
    .with_provider(MockLLMProvider())
    .build()
)

response = chatbot.chat(
    message="What can you help me with?",
    conversation_id="session-001",
    user_id="user-42",
)
print(response.assistant_message)
```

### Custom settings

```python
from andra_framework import ChatbotBuilder, FrameworkSettings, MemoryPolicy
from andra_core.guardrails.default import DefaultGuardrail

chatbot = (
    ChatbotBuilder()
    .with_provider(my_provider)
    .with_guardrails([DefaultGuardrail(max_length=5_000)])
    .with_settings(FrameworkSettings(memory_policy=MemoryPolicy.NONE))
    .build()
)
```

---

## Components

| Class | Description |
|---|---|
| `Chatbot` | Main interface — accepts `message`, `conversation_id`, `user_id` |
| `ChatbotBuilder` | Fluent builder for assembling a `Chatbot` |
| `FrameworkSettings` | Top-level configuration (memory policy, etc.) |
| `MemoryPolicy` | `IN_MEMORY` (default) or `NONE` |
| `FrameworkError` | Base framework exception |
| `ChatbotConfigurationError` | Raised when the builder is misconfigured |

---

## Installation

```bash
# From the monorepo (development)
cd packages/andra-framework
poetry install
```

---

## Development

```bash
make install     # install dependencies
make test        # run tests
make lint        # ruff
make typecheck   # mypy
```

This package is part of the [`andra`](../../README.md) monorepo.
