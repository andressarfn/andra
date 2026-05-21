.DEFAULT_GOAL := help

.PHONY: help install test test-cov lint typecheck

help:
	@echo ""
	@echo "  andra-framework"
	@echo ""
	@echo "  make install     Install all dependencies (including dev)"
	@echo "  make test        Run the test suite"
	@echo "  make test-cov    Run tests with coverage report"
	@echo "  make lint        Run ruff linter"
	@echo "  make typecheck   Run mypy type checker"
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
