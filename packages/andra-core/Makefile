# Load examples/.env if it exists (used by real-provider examples)
ifneq (,$(wildcard examples/.env))
  include examples/.env
  export
endif

.DEFAULT_GOAL := help

.PHONY: help install test test-cov lint typecheck install-examples mock real

help:
	@echo ""
	@echo "  andra-core"
	@echo ""
	@echo "  make install            Install all dependencies (including dev)"
	@echo "  make test               Run the test suite"
	@echo "  make test-cov           Run tests with coverage report"
	@echo "  make lint               Run ruff linter"
	@echo "  make typecheck          Run mypy type checker"
	@echo "  make install-examples   Install example dependencies (openai)"
	@echo "  make mock               Run basic_usage.py (no external API)"
	@echo "  make real               Run github_models_provider_usage.py (requires GITHUB_TOKEN)"
	@echo ""

install:
	poetry install

test:
	poetry run pytest

test-cov:
	poetry run pytest --cov=andra_core --cov-report=term-missing

lint:
	poetry run ruff check src/ tests/

typecheck:
	poetry run mypy src/

install-examples:
	poetry run pip install -r examples/requirements.txt

mock:
	poetry run python examples/basic_usage.py

real:
	poetry run python examples/github_models_provider_usage.py
