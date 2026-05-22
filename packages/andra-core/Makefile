# Load .env from monorepo root if it exists
ifneq (,$(wildcard ../../.env))
  include ../../.env
  export
endif

.DEFAULT_GOAL := help

.PHONY: help install test test-cov lint typecheck

help:
	@echo ""
	@echo "  andra-core"
	@echo ""
	@echo "  make install            Install all dependencies (including dev)"
	@echo "  make test               Run the test suite"
	@echo "  make test-cov           Run tests with coverage report"
	@echo "  make lint               Run ruff linter"
	@echo "  make typecheck          Run mypy type checker"
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
