run:
  uv run carousel

check:
  uv run pyright src

test:
  uv run pytest -vv --tb=short

format:
  uv run ruff format src test

compile:
  uv run pyinstaller src/main.py

clean:
  uv run pyclean src test
  uv run ruff clean
  rm -rf main.spec build dist .pytest_cache .hypothesis .benchmarks

wipe:
  just clean
  rm -rf .venv

lock:
  uv pip compile pyproject.toml -o requirements.txt
