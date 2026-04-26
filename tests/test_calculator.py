from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from api.calculator import Calculator
from api.main import app


@pytest.fixture
def calc() -> Calculator:
    return Calculator()


@pytest.fixture
def http_client() -> TestClient:
    return TestClient(app)


def test_addition(calc: Calculator) -> None:
    assert calc.calculate(2, 3, "+") == 5


def test_subtraction(calc: Calculator) -> None:
    assert calc.calculate(5, 3, "-") == 2


def test_subtraction_negative_result(calc: Calculator) -> None:
    assert calc.calculate(3, 5, "-") == -2


def test_multiplication(calc: Calculator) -> None:
    assert calc.calculate(4, 5, "*") == 20


def test_division(calc: Calculator) -> None:
    assert calc.calculate(10, 2, "/") == 5


def test_division_with_floats(calc: Calculator) -> None:
    assert calc.calculate(7, 2, "/") == 3.5


def test_division_negative_result(calc: Calculator) -> None:
    assert calc.calculate(-10, 2, "/") == -5


def test_division_by_zero(calc: Calculator) -> None:
    with pytest.raises(ValueError, match="Division by zero"):
        calc.calculate(5, 0, "/")


def test_power(calc: Calculator) -> None:
    assert calc.calculate(2, 3, "**") == 8


def test_power_zero_exponent(calc: Calculator) -> None:
    assert calc.calculate(5, 0, "**") == 1


def test_power_zero_base(calc: Calculator) -> None:
    assert calc.calculate(0, 5, "**") == 0


def test_power_zero_to_zero(calc: Calculator) -> None:
    assert calc.calculate(0, 0, "**") == 1


def test_modulo(calc: Calculator) -> None:
    assert calc.calculate(10, 3, "%") == 1


def test_modulo_negative(calc: Calculator) -> None:
    assert calc.calculate(-10, 3, "%") == 2


def test_sqrt(calc: Calculator) -> None:
    assert calc.calculate(16, None, "sqrt") == 4


def test_sqrt_float(calc: Calculator) -> None:
    assert calc.calculate(2, None, "sqrt") == pytest.approx(1.414213562)


def test_sqrt_zero(calc: Calculator) -> None:
    assert calc.calculate(0, None, "sqrt") == 0


def test_sqrt_negative(calc: Calculator) -> None:
    with pytest.raises(ValueError, match="sqrt of negative"):
        calc.calculate(-4, None, "sqrt")


def test_log(calc: Calculator) -> None:
    assert calc.calculate(100, None, "log") == 2


def test_log_one(calc: Calculator) -> None:
    assert calc.calculate(1, None, "log") == 0


def test_log_ten(calc: Calculator) -> None:
    assert calc.calculate(10, None, "log") == 1


def test_log_zero(calc: Calculator) -> None:
    with pytest.raises(ValueError, match="log of non-positive"):
        calc.calculate(0, None, "log")


def test_log_negative(calc: Calculator) -> None:
    with pytest.raises(ValueError, match="log of non-positive"):
        calc.calculate(-5, None, "log")


def test_unsupported_operation(calc: Calculator) -> None:
    with pytest.raises(ValueError, match="Unsupported operation"):
        calc.calculate(5, 3, "^")


def test_addition_with_negatives(calc: Calculator) -> None:
    assert calc.calculate(-5, 3, "+") == -2


def test_multiplication_by_zero(calc: Calculator) -> None:
    assert calc.calculate(100, 0, "*") == 0


# HTTP integration tests


def test_health_check(http_client: TestClient) -> None:
    response = http_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_hello_world(http_client: TestClient) -> None:
    response = http_client.get("/hello-world")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}


def test_http_post_addition(http_client: TestClient) -> None:
    response = http_client.post("/api/calculate", data={"operand1": "1", "operand2": "2", "operation": "+"})
    assert response.status_code == 200
    assert response.json() == {"result": 3.0}


def test_http_post_subtraction(http_client: TestClient) -> None:
    response = http_client.post("/api/calculate", data={"operand1": "5", "operand2": "3", "operation": "-"})
    assert response.status_code == 200
    assert response.json() == {"result": 2.0}


def test_http_post_multiplication(http_client: TestClient) -> None:
    response = http_client.post("/api/calculate", data={"operand1": "4", "operand2": "5", "operation": "*"})
    assert response.status_code == 200
    assert response.json() == {"result": 20.0}


def test_http_post_division(http_client: TestClient) -> None:
    response = http_client.post("/api/calculate", data={"operand1": "10", "operand2": "2", "operation": "/"})
    assert response.status_code == 200
    assert response.json() == {"result": 5.0}


def test_http_post_division_by_zero(http_client: TestClient) -> None:
    response = http_client.post("/api/calculate", data={"operand1": "5", "operand2": "0", "operation": "/"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Division by zero"


def test_http_post_unsupported_operation(http_client: TestClient) -> None:
    response = http_client.post("/api/calculate", data={"operand1": "5", "operand2": "3", "operation": "^"})
    assert response.status_code == 400
    assert "Unsupported operation" in response.json()["detail"]


def test_http_post_negative_numbers(http_client: TestClient) -> None:
    response = http_client.post("/api/calculate", data={"operand1": "-5", "operand2": "3", "operation": "+"})
    assert response.status_code == 200
    assert response.json() == {"result": -2.0}


def test_http_post_float_division(http_client: TestClient) -> None:
    response = http_client.post("/api/calculate", data={"operand1": "7", "operand2": "2", "operation": "/"})
    assert response.status_code == 200
    assert response.json() == {"result": 3.5}


def test_http_post_power(http_client: TestClient) -> None:
    response = http_client.post("/api/calculate", data={"operand1": "2", "operand2": "3", "operation": "**"})
    assert response.status_code == 200
    assert response.json() == {"result": 8.0}


def test_http_post_modulo(http_client: TestClient) -> None:
    response = http_client.post("/api/calculate", data={"operand1": "10", "operand2": "3", "operation": "%"})
    assert response.status_code == 200
    assert response.json() == {"result": 1.0}


def test_http_post_sqrt(http_client: TestClient) -> None:
    response = http_client.post("/api/calculate", data={"operand1": "16", "operation": "sqrt"})
    assert response.status_code == 200
    assert response.json() == {"result": 4.0}


def test_http_post_sqrt_negative(http_client: TestClient) -> None:
    response = http_client.post("/api/calculate", data={"operand1": "-4", "operation": "sqrt"})
    assert response.status_code == 400
    assert "sqrt of negative" in response.json()["detail"]


def test_http_post_log(http_client: TestClient) -> None:
    response = http_client.post("/api/calculate", data={"operand1": "100", "operation": "log"})
    assert response.status_code == 200
    assert response.json() == {"result": 2.0}


def test_http_post_log_zero(http_client: TestClient) -> None:
    response = http_client.post("/api/calculate", data={"operand1": "0", "operation": "log"})
    assert response.status_code == 400
    assert "log of non-positive" in response.json()["detail"]


def test_http_post_binary_op_without_operand2(http_client: TestClient) -> None:
    response = http_client.post("/api/calculate", data={"operand1": "5", "operation": "+"})
    assert response.status_code == 400
    assert "requires two operands" in response.json()["detail"]
