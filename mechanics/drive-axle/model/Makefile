.PHONY: clean lint

all: lint

clean:

lint:
	uv run ruff check src
	uv run ruff format --check --diff src

