# Minimal FastAPI Project

A minimal, but working FastAPI application.

## Quick Start

1. Install dependencies:
```bash
uv sync
```

2. Run the development server:
```bash
uv run uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

3. Run tests:
```bash
uv run pytest
```

## API Endpoints

- `GET /` — Returns a greeting message
- `GET /health` — Health check endpoint

## Project Structure

```
src/app/
├── __init__.py
└── main.py       # FastAPI application
tests/
└── test_app.py   # Unit tests
pyproject.toml    # Dependencies and configuration
```
