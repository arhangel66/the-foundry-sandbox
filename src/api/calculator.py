from __future__ import annotations

from collections.abc import Callable


class Calculator:
    """Simple arithmetic calculator."""

    _ops: dict[str, Callable[[float, float], float]] = {
        "+": lambda a, b: a + b,
        "-": lambda a, b: a - b,
        "*": lambda a, b: a * b,
        "/": lambda a, b: a / b,
    }

    def calculate(self, operand1: float, operand2: float, operation: str) -> float:
        if operation not in self._ops:
            raise ValueError(f"Unsupported operation: {operation}")
        if operation == "/" and operand2 == 0:
            raise ValueError("Division by zero")
        return self._ops[operation](operand1, operand2)
