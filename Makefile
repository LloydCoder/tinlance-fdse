PYTHON ?= python3

.PHONY: install format format-check lint typecheck test audit build docs-check check

install:
	$(PYTHON) -m pip install -e ".[dev]"

format:
	ruff format .

format-check:
	ruff format --check .

lint:
	ruff check .

typecheck:
	mypy src

test:
	pytest

audit:
	pip-audit --skip-editable

build:
	$(PYTHON) -m build --no-isolation

docs-check:
	$(PYTHON) scripts/check_docs.py

check: lint format-check typecheck test audit build docs-check
