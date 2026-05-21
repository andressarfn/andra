ROOT := $(shell cd .. && pwd)

# Load .env if it exists
ifneq (,$(wildcard .env))
  include .env
  export
endif

.DEFAULT_GOAL := help

.PHONY: help mock real install

help:
	@echo ""
	@echo "  andra-core / examples"
	@echo ""
	@echo "  make install   Install example dependencies (openai) into the project venv"
	@echo "  make mock      Run basic_usage.py (no external API)"
	@echo "  make real      Run github_models_provider_usage.py (requires GITHUB_TOKEN in .env)"
	@echo ""

install:
	cd $(ROOT) && poetry run pip install -r examples/requirements.txt

mock:
	cd $(ROOT) && poetry run python examples/basic_usage.py

real:
	cd $(ROOT) && poetry run python examples/github_models_provider_usage.py
