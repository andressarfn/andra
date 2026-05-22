# Load .env from this package directory (set GITHUB_TOKEN here for real-provider examples)
ifneq (,$(wildcard .env))
  include .env
  export
endif

.DEFAULT_GOAL := help

.PHONY: help install test test-cov lint typecheck mock install-examples real shell

help:
	@echo ""
	@echo "  andra-framework"
	@echo ""
	@echo "  make install            Install all dependencies (including dev)"
	@echo "  make test               Run the test suite"
	@echo "  make test-cov           Run tests with coverage report"
	@echo "  make lint               Run ruff linter"
	@echo "  make typecheck          Run mypy type checker"
	@echo "  make install-examples   Install example dependencies (openai)"
	@echo "  make mock               Run examples/mock_chatbot.py (no external API)"
	@echo "  make real               Run examples/copilot_chatbot.py (requires GITHUB_TOKEN in .env)"
	@echo "  make shell              Activate the framework venv (exit to leave)"
	@echo ""

install:
	poetry install

test:
	poetry run pytest

test-cov:
	poetry run pytest --cov=andra_framework --cov-report=term-missing

lint:
	poetry run ruff check src/ tests/

typecheck:
	poetry run mypy src/

mock:
	poetry run python examples/mock_chatbot.py

install-examples:
	poetry install --with providers

real: install-examples
	poetry run python examples/copilot_chatbot.py

shell:
	SHELL=/bin/zsh poetry shell
