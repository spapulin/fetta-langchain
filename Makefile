.PHONY: up down start stop shell sync test smoke lint jupyter publish

up:
	docker compose up -d --build

down:
	docker compose down

start:
	docker compose start

stop:
	docker compose stop

sync:
	docker compose exec fetta-langchain uv sync

shell:
	docker compose exec fetta bash

test:
	docker compose exec fetta uv run pytest -v

lint:
	docker compose exec fetta uv run ruff check src tests

smoke:
	docker compose exec fetta uv run python scripts/smoke.py

jupyter:
	docker compose exec fetta-langchain uv run jupyter lab \
		--ip=0.0.0.0 \
		--port=8888 \
		--no-browser \
		--ServerApp.token='' \
		--ServerApp.password=''

publish:
	@if [ -z "$(BUMP)" ]; then \
		echo "Usage: make publish BUMP=patch|minor|major"; \
		exit 1; \
	fi
	uv version --bump $(BUMP)
	$(eval VERSION := $(shell uv version --short))
	git add pyproject.toml uv.lock
	git commit -m "chore: release $(VERSION)"
	git tag v$(VERSION)
	git push && git push --tags
	@echo "Released $(VERSION)"

#deploy-env:
#	uv init --python 3.12 --package --name fetta-langchain
#	uv venv
#	source .venv/bin/activate && uv add "langchain-core>=1.6.4,<2" "fetta"
#	source .venv/bin/activate && uv add --dev "pytest>=8" "pytest-asyncio>=0.24" "ruff>=0.6" jupyterlab ipykernel langchain-classic langchain-deepseek python-dotenv
#	source .venv/bin/activate && uv add --editable ../fetta


