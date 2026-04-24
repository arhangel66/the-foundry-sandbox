from __future__ import annotations

import pytest

from api.calculator import Calculator


def test_addition():
    calc = Calculator()
    assert calc.calculate(2, 3, "+") == 5


def test_subtraction():
    calc = Calculator()
    assert calc.calculate(5, 3, "-") == 2


def test_multiplication():
    calc = Calculator()
    assert calc.calculate(4, 5, "*") == 20


def test_division():
    calc = Calculator()
    assert calc.calculate(10, 2, "/") == 5


def test_division_with_floats():
    calc = Calculator()
    assert calc.calculate(7, 2, "/") == 3.5


def test_division_by_zero():
    calc = Calculator()
    with pytest.raises(ValueError, match="Division by zero"):
        calc.calculate(5, 0, "/")


def test_unsupported_operation():
    calc = Calculator()
    with pytest.raises(ValueError, match="Unsupported operation"):
        calc.calculate(5, 3, "%")


def test_addition_with_negatives():
    calc = Calculator()
    assert calc.calculate(-5, 3, "+") == -2


def test_multiplication_by_zero():
    calc = Calculator()
    assert calc.calculate(100, 0, "*") == 0
