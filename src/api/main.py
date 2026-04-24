from __future__ import annotations

from fastapi import FastAPI

app = FastAPI(title="Foundry API")


@app.get("/")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/hello-world")
def hello_world() -> dict[str, str]:
    return {"message": "Hello, World!"}
