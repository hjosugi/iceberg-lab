SHELL := /usr/bin/env bash

PYTHON ?= python3
VERSION := $(shell cat VERSION)
PACKAGE_NAME := iceberg-r2-online-lab
DIST_ZIP := dist/$(PACKAGE_NAME)-v$(VERSION).zip

.PHONY: help install install-uv doctor create append read list duckdb-sql test lint package clean docker-build docker-shell

help:
	@echo "Targets:"
	@echo "  install       Create .venv and install package"
	@echo "  install-uv    Install package using uv"
	@echo "  doctor        Check env vars"
	@echo "  create        Create namespace and table"
	@echo "  append        Append sample data"
	@echo "  read          Read sample table"
	@echo "  list          List namespaces and tables"
	@echo "  duckdb-sql    Generate DuckDB attach SQL"
	@echo "  test          Run tests"
	@echo "  lint          Run ruff"
	@echo "  package       Build release ZIP"
	@echo "  clean         Remove generated files"

install:
	$(PYTHON) -m venv .venv
	source .venv/bin/activate && python -m pip install --upgrade pip
	source .venv/bin/activate && python -m pip install -e ".[dev]"

install-uv:
	uv venv
	source .venv/bin/activate && uv pip install -e ".[dev]"

doctor:
	$(PYTHON) -m iceberg_r2_lab doctor $(ARGS)

create:
	$(PYTHON) -m iceberg_r2_lab create $(ARGS)

append:
	$(PYTHON) -m iceberg_r2_lab append $(ARGS)

read:
	$(PYTHON) -m iceberg_r2_lab read --limit 20 $(ARGS)

list:
	$(PYTHON) -m iceberg_r2_lab list $(ARGS)

duckdb-sql:
	mkdir -p .generated
	$(PYTHON) -m iceberg_r2_lab duckdb-sql > .generated/duckdb_attach.sql
	@echo "Wrote .generated/duckdb_attach.sql"

test:
	pytest

lint:
	ruff check .

package:
	$(PYTHON) scripts/package_release.py --version "$(VERSION)"

clean:
	rm -rf build dist .generated .pytest_cache .ruff_cache
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +

docker-build:
	docker compose build

docker-shell:
	docker compose run --rm lab bash
