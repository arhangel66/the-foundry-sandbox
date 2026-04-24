# foundry-api

Minimal FastAPI server for The Foundry orchestrator.

## Setup

```bash
pip install -e .
# or
uv sync
```

## Run

```bash
uvicorn src.api.main:app --reload
```

Server will start at `http://localhost:8000`

## Health Check

```bash
curl http://localhost:8000/
# Response: {"status":"ok"}
```
