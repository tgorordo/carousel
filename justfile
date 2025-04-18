run:
  uv run carousel

check:
  uv run pyright src

test:
  uv run pytest -vv --tb=short

format:
  uv run ruff format src test

clean:
  uv run pyclean src test
  uv run ruff clean
  rm -rf .pytest_cache .hypothesis .benchmarks

wipe:
  just clean
  rm -rf .venv

lock:
  uv pip compile pyproject.toml -o requirements.txt
