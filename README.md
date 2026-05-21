# andra

Monorepo for the **Andra** ecosystem — LLM-powered corporate chatbots.

---

## Packages

| Package | Description | Status |
|---|---|---|
| [`andra-core`](packages/andra-core/README.md) | Framework-agnostic core library — contracts, pipeline, models, memory, agents, guardrails | Alpha |
| [`andra-framework`](packages/andra-framework/README.md) | Opinionated framework layer built on top of `andra-core` | Pre-Alpha |

### andra-core

`andra-core` provides the foundational building blocks for assembling LLM-powered conversation pipelines. It is framework-agnostic, transport-agnostic, and provider-agnostic — no dependency on FastAPI, OpenAI, Azure, or any other external system. Integrations belong in separate packages.

### andra-framework

`andra-framework` is the future opinionated layer of the Andra ecosystem. It will build on top of `andra-core` to provide higher-level abstractions, sensible defaults, and production-ready integrations. Not yet implemented.

---

## Repository Structure

```
andra/
├── Makefile                        # Monorepo-level convenience targets
├── packages/
│   ├── andra-core/                 # Core library
│   │   ├── pyproject.toml
│   │   ├── poetry.toml
│   │   ├── README.md
│   │   ├── Makefile
│   │   ├── src/andra_core/
│   │   ├── tests/
│   │   └── examples/
│   └── andra-framework/            # Framework layer (scaffolded, not yet implemented)
│       ├── pyproject.toml
│       ├── README.md
│       └── src/andra_framework/
```

---

## Working Locally

Each package is an independent Poetry project. Work inside the package directory.

### andra-core

```bash
cd packages/andra-core

# Install dependencies (creates .venv inside the package)
poetry install

# Run tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=andra_core --cov-report=term-missing

# Lint
poetry run ruff check src/ tests/

# Type check
poetry run mypy src/
```

Or use the monorepo-level Makefile from the root:

```bash
make install-core
make test-core
make lint-core
make typecheck-core
```

### Examples

```bash
cd packages/andra-core/examples

# Run the mock pipeline (no external API required)
make mock

# Install real-provider dependencies and run
make install
make real   # requires GITHUB_TOKEN in a .env file
```

### andra-framework

```bash
cd packages/andra-framework

# Install (includes andra-core as a local path dependency)
poetry install
```

---

## License

MIT
