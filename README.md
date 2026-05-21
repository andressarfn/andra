# andra-core

Core library for the **Andra** ecosystem — LLM-powered corporate chatbots.

`andra-core` is a framework-agnostic, transport-agnostic, provider-agnostic Python library that provides the foundational building blocks for building corporate chatbot pipelines powered by Large Language Models.

---

## Architecture

`andra-core` follows a simplified **Hexagonal Architecture** (ports and adapters):

- **Models** — Domain entities (pure dataclasses, no dependencies)
- **Contracts** — Abstract base classes (ports) for all extension points
- **Pipeline** — Orchestrates the full conversation flow
- **Memory** — Conversation history storage
- **Providers** — LLM provider adapters
- **Agents** — Agents that process requests and produce results
- **Guardrails** — Input/output validation logic
- **Exceptions** — Typed exception hierarchy

The core has **no dependency** on FastAPI, Flask, OpenAI, Azure, or any other external system. Those integrations belong in separate packages (`andra-fastapi`, `andra-openai`, etc.).

---

## Pipeline Flow

```
ChatRequest
    │
    ▼
ExecutionContext (created / enriched)
    │
    ▼
Memory (retrieve conversation history)
    │
    ▼
Guardrails (validate input)
    │
    ▼
Agent (process request)
    │
    ▼
LLM Provider (generate response)
    │
    ▼
Guardrails (validate output)
    │
    ▼
Memory (persist history)
    │
    ▼
ChatResponse
```

---

## Requirements

- Python 3.12+
- [Poetry](https://python-poetry.org/) for dependency management

---

## Getting Started

### 1. Install Poetry

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### 2. Clone and install dependencies

```bash
git clone https://github.com/andra-ai/andra-core.git
cd andra-core
poetry install
```

### 3. Activate the virtual environment

```bash
poetry shell
```

### 4. Install the package locally (editable)

```bash
pip install -e .
# or simply use Poetry's install, which handles this automatically
poetry install
```

### 5. Run the basic example

```bash
python examples/basic_usage.py
```

---

## Usage

```python
from andra_core.models import ChatRequest
from andra_core.pipeline import DefaultConversationPipeline
from andra_core.providers import MockLLMProvider
from andra_core.agents import SimpleAgent
from andra_core.guardrails import DefaultGuardrail
from andra_core.memory import InMemoryMemoryStore

# Compose the pipeline
pipeline = DefaultConversationPipeline(
    provider=MockLLMProvider(),
    agent=SimpleAgent(),
    guardrails=[DefaultGuardrail()],
    memory_store=InMemoryMemoryStore(),
)

# Run a conversation turn
request = ChatRequest(
    conversation_id="conv-001",
    user_message="Hello, Andra!",
)

response = pipeline.run(request)
print(response.assistant_message)
```

---

## Project Structure

```
src/
└── andra_core/
    ├── models/        # Domain entities
    ├── contracts/     # Abstract interfaces (ports)
    ├── pipeline/      # DefaultConversationPipeline
    ├── memory/        # InMemoryMemoryStore
    ├── providers/     # MockLLMProvider
    ├── agents/        # SimpleAgent
    ├── guardrails/    # DefaultGuardrail
    └── exceptions/    # Typed exception hierarchy
examples/
└── basic_usage.py
```

---

## Extending the Core

To create a real LLM provider, implement `BaseLLMProvider`:

```python
from andra_core.contracts import BaseLLMProvider
from andra_core.models import ChatRequest, ChatResponse, ExecutionContext

class OpenAIProvider(BaseLLMProvider):
    def complete(self, request: ChatRequest, context: ExecutionContext) -> ChatResponse:
        # call OpenAI API here
        ...
```

The same pattern applies to `BaseAgent`, `BaseGuardrail`, and `BaseMemoryStore`.

---

## License

MIT
