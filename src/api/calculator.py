from __future__ import annotations

import math
from collections.abc import Callable


class Calculator:
    """Engineering calculator with binary and unary operations."""

    _binary_ops: dict[str, Callable[[float, float], float]] = {
        "+": lambda a, b: a + b,
        "-": lambda a, b: a - b,
        "*": lambda a, b: a * b,
        "/": lambda a, b: a / b,
        "**": lambda a, b: a**b,
        "%": lambda a, b: a % b,
    }

    @staticmethod
    def _sqrt(x: float) -> float:
        if x < 0:
            raise ValueError("sqrt of negative")
        return math.sqrt(x)

    @staticmethod
    def _log(x: float) -> float:
        if x <= 0:
            raise ValueError("log of non-positive")
        return math.log10(x)

    def calculate(
        self,
        operand1: float,
        operand2: float | None,
        operation: str,
    ) -> float:
        unary_ops: dict[str, Callable[[float], float]] = {
            "sqrt": self._sqrt,
            "log": self._log,
        }
        if operation in unary_ops:
            return unary_ops[operation](operand1)
        if operation in self._binary_ops:
            if operand2 is None:
                raise ValueError(f"Operation '{operation}' requires two operands")
            if operation == "/" and operand2 == 0:
                raise ValueError("Division by zero")
            return self._binary_ops[operation](operand1, operand2)
        raise ValueError(f"Unsupported operation: {operation}")
