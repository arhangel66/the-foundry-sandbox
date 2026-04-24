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


def test_unsupported_operation(calc: Calculator) -> None:
    with pytest.raises(ValueError, match="Unsupported operation"):
        calc.calculate(5, 3, "%")


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
    response = http_client.post("/api/calculate", data={"operand1": "5", "operand2": "3", "operation": "%"})
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
