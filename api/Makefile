help:
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

activate:
	@echo "Run 'source .venv/bin/activate' to activate the virtualenv"

install:
	uv run

dev-install:
	uv run --dev

run: ## TODO
	uvicorn chatbot.main:app --host 0.0.0.0 --port 8000 --reload

