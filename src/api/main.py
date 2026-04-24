from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, Form, HTTPException
from fastapi.staticfiles import StaticFiles

from .calculator import Calculator

app = FastAPI(title="Foundry API")
calculator = Calculator()


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/hello-world")
def hello_world() -> dict[str, str]:
    return {"message": "Hello, World!"}


@app.post("/api/calculate")
def calculate(
    operand1: float = Form(...),
    operand2: float = Form(...),
    operation: str = Form(...),
) -> dict[str, float | str]:
    try:
        result = calculator.calculate(operand1, operand2, operation)
        return {"result": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# Static files must be mounted last — a "/" mount matches all paths
# and would shadow API routes if registered first.
static_dir = Path(__file__).parent.parent.parent / "static"
if static_dir.exists():
    app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")
