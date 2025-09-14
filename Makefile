SHELL := /bin/bash
.PHONY: dev-up dev-down test fmt lint

dev-up:
\tdocker compose -f infra/docker/compose.dev.yml up -d --build

dev-down:
\tdocker compose -f infra/docker/compose.dev.yml down -v

test:
\tpytest -q

fmt:
\trufflehog --help >/dev/null 2>&1 || true
\tblack src tests

lint:
\tflake8 src tests || true
