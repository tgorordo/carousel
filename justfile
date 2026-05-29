list:
  just --list

run *args:
  uv run src/carouselcmd.py {{args}}

python *arguments:
  uv run python -c {{arguments}}

marimo:
  uv run marimo --edit

sync *args:
  uv sync {{args}}

format:
  uv run ruff format src test

check:
  uv run pyright src

test:
  uv run pytest -vvv --tb=short --log-cli-level=INFO

compile:
  uv run --with-requirements src/carouselcmd.py pyinstaller --clean -F src/carouselcmd.py

clean:
  uv run pyclean src test
  uv run ruff clean
  rm -rf carouselcmd.spec carouselgui.spec build dist .pytest_cache .hypothesis .benchmarks __marimo__

wipe:
  just clean
  rm -rf .venv

lock:
  uv lock
  uv pip compile pyproject.toml -o requirements.txt --group dev
