.DEFAULT_GOAL := help
FLASK := uv run flask --app app

.PHONY: help
help: ## Show this help
	@awk 'BEGIN {FS = ":.*## "} /^[a-zA-Z_-]+:.*## / {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: install
install: ## Install dependencies and git hooks
	uv sync
	uv run pre-commit install

.PHONY: dev
dev: ## Run the dev server with auto-reload on http://127.0.0.1:5000
	$(FLASK) run --debug

.PHONY: test
test: ## Run the test suite with coverage
	uv run pytest --cov

.PHONY: lint
lint: ## Lint, check formatting and type-check
	uv run ruff check .
	uv run ruff format --check .
	uv run mypy

.PHONY: fmt
fmt: ## Auto-format and fix lint issues
	uv run ruff format .
	uv run ruff check --fix .

.PHONY: migrate
migrate: ## Apply database migrations
	$(FLASK) db upgrade

.PHONY: migration
migration: ## Create a migration from model changes: make migration m="add foo"
	$(FLASK) db migrate -m "$(m)"

.PHONY: seed
seed: ## Add sample stories to the database
	$(FLASK) seed

.PHONY: up
up: ## Start the Docker stack (nginx + app + Postgres) on http://localhost:8080
	docker compose up --build

.PHONY: down
down: ## Stop the Docker stack
	docker compose down

.PHONY: clean
clean: ## Remove caches and build artefacts
	rm -rf .pytest_cache .mypy_cache .ruff_cache .coverage htmlcov
	find . -type d -name __pycache__ -not -path './.venv/*' -exec rm -rf {} +
