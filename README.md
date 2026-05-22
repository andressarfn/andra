# andra

Monorepo for the **Andra** ecosystem — LLM-powered corporate chatbots.

---

## Packages

| Package | Description | Status |
|---|---|---|
| [`andra-framework`](packages/andra-framework/README.md) | Public API — fluent builder, sensible defaults, built-in providers | Alpha |
| [`andra-core`](packages/andra-core/README.md) | Internal foundation — contracts, pipeline, models | Alpha |

`andra-framework` is the recommended entry point. End users import exclusively from `andra_framework`.
`andra-core` is an internal implementation detail and is not part of the public API.

---

## Getting Started

```bash
cd packages/andra-framework
poetry install        # install dependencies
make mock             # run the mock example
```

See [`packages/andra-framework/README.md`](packages/andra-framework/README.md) for the full usage guide.

---

## Repository Structure

```
andra/
├── README.md
└── packages/
    ├── andra-framework/            # Framework package — start here
    │   ├── Makefile
    │   ├── .env.example
    │   ├── pyproject.toml
    │   ├── README.md
    │   ├── examples/
    │   │   ├── mock_chatbot.py
    │   │   └── copilot_chatbot.py
    │   ├── src/andra_framework/
    │   └── tests/
    └── andra-core/                 # Core library (internal)
        ├── Makefile
        ├── pyproject.toml
        ├── README.md
        ├── src/andra_core/
        └── tests/
```

---

## License

MIT


The recommended entry point for users is [`andra-framework`](packages/andra-framework/README.md).
