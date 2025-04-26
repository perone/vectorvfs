.PHONY: lint typecheck test

lint:
	uv run ruff check vectorvfs

typecheck:
	uv run mypy vectorvfs

test:
	uv run pytest -v -s tests/

test-pdb:
	uv run pytest --pdb -v -s tests/

isort:
	uv run ruff check --select I --fix

sphinx-autobuild:
	uv run sphinx-autobuild --host 0.0.0.0 docs/source docs/build/html/
