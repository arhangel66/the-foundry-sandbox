from __future__ import annotations

from fastapi import FastAPI

app = FastAPI(title="Foundry API")


@app.get("/")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
