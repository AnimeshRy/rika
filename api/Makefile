help:
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

activate:
	@echo "Run 'source .venv/bin/activate' to activate the virtualenv"

install:
	uv run

dev-install:
	uv run --dev

rund: ## TODO
	uvicorn app:

run: ## TODO
	uvicorn app:
