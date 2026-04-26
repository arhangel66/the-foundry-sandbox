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
        "**": lambda a, b: a ** b,
        "%": lambda a, b: a % b,
    }

    _unary_ops: dict[str, Callable[[float], float]] = {
        "sqrt": lambda x: math.sqrt(x) if x >= 0 else (_ for _ in ()).throw(ValueError("sqrt of negative")),
        "log": lambda x: math.log10(x) if x > 0 else (_ for _ in ()).throw(ValueError("log of non-positive")),
    }

    def calculate(
        self,
        operand1: float,
        operand2: float | None,
        operation: str,
    ) -> float:
        if operation in self._unary_ops:
            return self._unary_ops[operation](operand1)
        elif operation in self._binary_ops:
            if operand2 is None:
                raise ValueError(f"Operation '{operation}' requires two operands")
            if operation == "/" and operand2 == 0:
                raise ValueError("Division by zero")
            return self._binary_ops[operation](operand1, operand2)
        else:
            raise ValueError(f"Unsupported operation: {operation}")
