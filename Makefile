.DEFAULT_GOAL := help

.PHONY: help install-core install-framework install-examples-core test-core test-framework lint-core typecheck-core shell-core shell-framework mock-core real-core

help:
	@echo ""
	@echo "  andra monorepo"
	@echo ""
	@echo "  -- andra-core --"
	@echo "  make install-core            Install andra-core dependencies"
	@echo "  make install-examples-core   Install example dependencies (openai)"
	@echo "  make test-core               Run test suite"
	@echo "  make lint-core               Run ruff linter"
	@echo "  make typecheck-core          Run mypy type checker"
	@echo "  make mock-core               Run mock example (no external API)"
	@echo "  make real-core               Run real provider example (requires GITHUB_TOKEN)"
	@echo "  make shell-core              Activate venv (exit to deactivate)"
	@echo ""
	@echo "  -- andra-framework --"
	@echo "  make install-framework       Install andra-framework dependencies"
	@echo "  make test-framework          Run test suite"
	@echo "  make shell-framework         Activate venv (exit to deactivate)"
	@echo ""

install-core:
	$(MAKE) -C packages/andra-core install

install-framework:
	$(MAKE) -C packages/andra-framework install

install-examples-core:
	$(MAKE) -C packages/andra-core install-examples

test-core:
	$(MAKE) -C packages/andra-core test

test-framework:
	$(MAKE) -C packages/andra-framework test

lint-core:
	$(MAKE) -C packages/andra-core lint

typecheck-core:
	$(MAKE) -C packages/andra-core typecheck

mock-core:
	$(MAKE) -C packages/andra-core mock

real-core:
	$(MAKE) -C packages/andra-core real
