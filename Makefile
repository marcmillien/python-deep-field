export PIPENV_VENV_IN_PROJECT=true
export PYTHONPATH=$(PWD)/src

all: help

.PHONY: help
help:
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' | sed -e "s/| \(.*\)$$/| $$(printf "\033")[37m\1$$(printf "\033")[0m/g"

.PHONY: fmt
fmt: ## Format code
	pipenv run black src tests
	pipenv run isort --profile black src tests

.PHONY: lint
lint: ## Lint code
	pipenv run flake8 src tests
	pipenv run mypy src
	pipenv run black --check src tests
	pipenv run isort --check-only --profile black src tests


.PHONY: setup
setup: ## Setup development environment
	pipenv sync --dev

.PHONY: test
test: ## Run test suite | make test
	pipenv run pytest tests
