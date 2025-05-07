list:
  just --list

run:
  uv run carousel

python *arguments:
  uv run python -c "import code; from rich import pretty; pretty.install(); code.interact()" {{arguments}}

check:
  uv run pyright src

test:
  uv run pytest -vvv --tb=short --log-cli-level=INFO

format:
  uv run ruff format src test

compile:
  uv run pyinstaller src/cli.py
  uv run pyinstaller src/gui.py

clean:
  uv run pyclean src test
  uv run ruff clean
  rm -rf main.spec cli.spec gui.spec build dist .pytest_cache .hypothesis .benchmarks __marimo__

wipe:
  just clean
  rm -rf .venv

lock:
  uv pip compile pyproject.toml -o requirements.txt --group dev
