# andra-framework

Opinionated framework layer for the **Andra** ecosystem — built on top of `andra-core`.

`andra-framework` provides a high-level, batteries-included API for assembling and running LLM-powered chatbots. Users import exclusively from `andra_framework` — the underlying `andra-core` is an internal implementation detail.

---

## Quick Start

```python
from andra_framework import ChatbotBuilder, MockLLMProvider

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

---

## Local Setup

```bash
cd packages/andra-framework

# Install dependencies
make install

# Run the mock example (no external API required)
make mock

# Run tests
make test
```

### Real provider (GitHub Models API)

1. Copy `.env.example` to `.env` and set your token:

   ```bash
   cp .env.example .env
   # edit .env and set: GITHUB_TOKEN=github_pat_...
   ```

2. Run the real example:

   ```bash
   make real   # installs openai automatically, then runs examples/copilot_chatbot.py
   ```

3. Activate the venv to run examples directly:

   ```bash
   make shell
   python examples/mock_chatbot.py
   python examples/copilot_chatbot.py
   exit
   ```

---

## Examples

| File | Description |
|---|---|
| [`examples/mock_chatbot.py`](examples/mock_chatbot.py) | Multi-turn chatbot with in-memory history — no external API |
| [`examples/copilot_chatbot.py`](examples/copilot_chatbot.py) | Real provider via GitHub Models API — requires `GITHUB_TOKEN` |

---

## API Reference

All symbols are importable directly from `andra_framework`.

### Core classes

| Symbol | Kind | Description |
|---|---|---|
| `Chatbot` | Class | Main interface — `chat(message, conversation_id, user_id?)` |
| `ChatbotBuilder` | Class | Fluent builder |
| `FrameworkSettings` | Dataclass | Top-level configuration |
| `MemoryPolicy` | Enum | `IN_MEMORY` (default) or `NONE` |

### Built-in implementations

| Symbol | Kind | Description |
|---|---|---|
| `MockLLMProvider` | Class | Deterministic mock provider for dev / tests |
| `DefaultGuardrail` | Class | Length + empty-content guardrail |

### Extension API — subclass to build custom integrations

| Symbol | Kind | Description |
|---|---|---|
| `BaseLLMProvider` | ABC | Connect any LLM backend |
| `BaseAgent` | ABC | Custom agent logic |
| `BaseGuardrail` | ABC | Custom validation rules |
| `BaseMemoryStore` | ABC | Custom memory backend |

### Data models

| Symbol | Kind | Description |
|---|---|---|
| `ChatResponse` | Dataclass | Return type of `chat()` |
| `ChatMessage` | Dataclass | A single turn in a conversation |
| `MessageRole` | Enum | `USER`, `ASSISTANT`, `SYSTEM` |
| `ChatRequest` | Dataclass | Input model (used in `BaseLLMProvider.complete()`) |
| `ExecutionContext` | Dataclass | Context passed to `BaseLLMProvider.complete()` |
| `AgentResult` | Dataclass | Return type of `BaseAgent.run()` |
| `GuardrailResult` | Dataclass | Return type of `BaseGuardrail.validate()` |

### Exceptions

| Symbol | Description |
|---|---|
| `FrameworkError` | Base framework exception |
| `ChatbotConfigurationError` | Builder misconfigured |
| `PipelineError` | Pipeline execution failure |
| `GuardrailViolationError` | Guardrail blocked execution |

---

## Providers

Optional providers with external dependencies live in `andra_framework.providers`:

| Provider | Import | Requirements |
|---|---|---|
| `GitHubModelsProvider` | `from andra_framework.providers.github_models import GitHubModelsProvider` | `openai`, `GITHUB_TOKEN` |

Install provider dependencies:

```bash
make install-examples
```

---

## Usage Patterns

### Custom provider

```python
from andra_framework import (
    BaseLLMProvider,
    ChatRequest,
    ChatResponse,
    ExecutionContext,
)


class MyProvider(BaseLLMProvider):
    def complete(self, request: ChatRequest, context: ExecutionContext) -> ChatResponse:
        return ChatResponse(
            conversation_id=request.conversation_id,
            assistant_message="...",
        )
```

### Custom guardrail

```python
from andra_framework import BaseGuardrail, ExecutionContext, GuardrailResult


class MyGuardrail(BaseGuardrail):
    @property
    def name(self) -> str:
        return "my_guardrail"

    def validate(self, text: str, context: ExecutionContext) -> GuardrailResult:
        passed = "forbidden" not in text.lower()
        return GuardrailResult(passed=passed, guardrail_name=self.name)
```

### Stateless chatbot (no memory)

```python
from andra_framework import ChatbotBuilder, FrameworkSettings, MemoryPolicy, MockLLMProvider

chatbot = (
    ChatbotBuilder()
    .with_provider(MockLLMProvider())
    .with_settings(FrameworkSettings(memory_policy=MemoryPolicy.NONE))
    .build()
)
```

---

## Development

```bash
make install       # install all dependencies
make test          # run tests
make test-cov      # run tests with coverage
make lint          # ruff
make typecheck     # mypy
```

This package is part of the [`andra`](../../README.md) monorepo.
