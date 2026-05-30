.PHONY: install help test lint check

install:
	pip install -e .

help:
	citeevidence --help

test:
	pytest

lint:
	ruff check

check: lint test
