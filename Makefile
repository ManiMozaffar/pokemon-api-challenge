# Build configuration
# -------------------

APP_NAME := `sed -n 's/^ *name.*=.*"\([^"]*\)".*/\1/p' pyproject.toml`
APP_VERSION := `sed -n 's/^ *version.*=.*"\([^"]*\)".*/\1/p' pyproject.toml`
GIT_REVISION = `git rev-parse HEAD`


# Development targets
# -------------


.PHONY: initilize
init: ## Deploy
	python -m pip install poetry
	poetry install --no-interaction --no-root

.PHONY: deploy
deploy: ## Deploy
	poetry run python run.py

.PHONY: check-lockfile
check-lockfile: ## Compares lock file with pyproject.toml
	poetry lock --check

.PHONY: test
test: ## Run the test suite
	poetry run pytest -vv -s --cache-clear
