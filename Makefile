.PHONY: help install dev run test integration-tests lint format

help:  ## Show this help
	@grep -hE '^[a-z-]+:.*?## ' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-8s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "  IMAGE=$(IMAGE):$(TAG) PORT=$(PORT) DOCKER=$(DOCKER)"
	@echo "  CACHE_DIR=$(CACHE_DIR)  ENV_FILE=$(ENV_FILE)  as uid $(RUN_UID):$(RUN_GID)"

install: ## Sync runtime dependencies with uv
	uv sync --no-dev

dev:  ## Sync project + dev dependencies with uv
	uv sync

run:  ## Start the local LangGraph dev server
	uv run langgraph dev

test:  ## Run unit tests
	uv run python -m pytest tests/unit_tests -q

integration-tests:  ## Run integration tests
	uv run python -m pytest tests/integration_tests -q

lint:  ## Run Ruff checks
	uv run python -m ruff check src tests

format:  ## Format with ruff
	uv run python -m ruff format src tests

run-studio-eu:  ## run dev with eu studio
	uv run langgraph dev --studio-url https://eu.smith.langchain.com

run-studio-with-tunnel:  ## run dev using eu studio and auto tunnel
	uv run langgraph dev --tunnel --studio-url https://eu.smith.langchain.com

run-headless-on-render: ## for render but does not work (yet) if invoked by makefile
	uv run langgraph dev --port $PORT --host 0.0.0.0 --no-browser