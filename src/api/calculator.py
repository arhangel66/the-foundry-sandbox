from __future__ import annotations


class Calculator:
    """Simple arithmetic calculator."""

    def calculate(self, operand1: float, operand2: float, operation: str) -> float:
        """
        Perform arithmetic operation.

        Args:
            operand1: First operand
            operand2: Second operand
            operation: One of '+', '-', '*', '/'

        Returns:
            Result of operation

        Raises:
            ValueError: If operation is not supported or division by zero
        """
        if operation == "+":
            return operand1 + operand2
        elif operation == "-":
            return operand1 - operand2
        elif operation == "*":
            return operand1 * operand2
        elif operation == "/":
            if operand2 == 0:
                raise ValueError("Division by zero")
            return operand1 / operand2
        else:
            raise ValueError(f"Unsupported operation: {operation}")
