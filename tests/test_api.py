from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from api.main import app
from foundry import state
from foundry.models import Task, TaskStatus


@pytest.fixture
def _setup_env(tmp_path: Path, monkeypatch) -> Path:
    db_path = tmp_path / "test.sqlite"
    monkeypatch.setenv("SOURCE_REPO", "test/repo")
    monkeypatch.setenv("TARGET_REPO", "test/repo")
    monkeypatch.setenv("DB_PATH", str(db_path))
    return db_path


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_health_check(client: TestClient) -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_tasks_empty(client: TestClient, _setup_env: Path) -> None:
    db_path = _setup_env
    state.init_db(db_path)

    response = client.get("/api/tasks")
    assert response.status_code == 200
    assert response.json()["tasks"] == []


def test_get_tasks_with_data(client: TestClient, _setup_env: Path) -> None:
    db_path = _setup_env
    state.init_db(db_path)

    task = Task(
        repo="owner/repo",
        issue_number=42,
        issue_title="Test issue",
        issue_body="Body",
    )
    state.upsert_task(db_path, task)

    response = client.get("/api/tasks")
    assert response.status_code == 200
    data = response.json()
    assert len(data["tasks"]) == 1
    assert data["tasks"][0]["issue_number"] == 42
    assert data["tasks"][0]["status"] == "pending"


def test_get_tasks_filter_by_status(
    client: TestClient, _setup_env: Path
) -> None:
    db_path = _setup_env
    state.init_db(db_path)

    state.upsert_task(
        db_path,
        Task(
            repo="owner/repo",
            issue_number=1,
            issue_title="Task 1",
            issue_body="Body 1",
        ),
    )
    t2 = state.upsert_task(
        db_path,
        Task(
            repo="owner/repo",
            issue_number=2,
            issue_title="Task 2",
            issue_body="Body 2",
        ),
    )
    t2.status = TaskStatus.DONE
    state.upsert_task(db_path, t2)

    response = client.get("/api/tasks?status=pending")
    assert response.status_code == 200
    data = response.json()
    assert len(data["tasks"]) == 1
    assert data["tasks"][0]["issue_number"] == 1

    response = client.get("/api/tasks?status=done")
    assert response.status_code == 200
    data = response.json()
    assert len(data["tasks"]) == 1
    assert data["tasks"][0]["issue_number"] == 2


def test_get_tasks_invalid_status(client: TestClient, _setup_env: Path) -> None:
    db_path = _setup_env
    state.init_db(db_path)

    response = client.get("/api/tasks?status=invalid")
    assert response.status_code == 400
    assert "Invalid status" in response.json()["error"]
