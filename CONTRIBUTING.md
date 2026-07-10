# Contributing

## Development setup

```bash
python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Test

```bash
pytest
ruff check .
```

## Release

```bash
git tag v1.0.0
git push origin v1.0.0
```

The release workflow builds a ZIP and uploads it to GitHub Releases.

## Commit style

Simple conventional commits are recommended.

```text
feat: add duckdb example
fix: handle missing token
docs: update r2 setup guide
```
