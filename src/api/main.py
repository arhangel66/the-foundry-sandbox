from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from foundry import state
from foundry.config import ConfigError, load_settings
from foundry.models import TaskStatus

app = FastAPI(title="The Foundry API")


@app.get("/")
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}


@app.get("/api/tasks")
async def get_tasks(status: str | None = None) -> JSONResponse:
    """Get all tasks from database, optionally filtered by status."""
    try:
        settings = load_settings()
    except ConfigError as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Configuration error: {str(e)}"},
        )

    state.init_db(settings.db_path)

    try:
        if status:
            task_status = TaskStatus(status)
            tasks = state.list_tasks(settings.db_path, task_status)
        else:
            tasks = state.list_tasks(settings.db_path)
    except ValueError:
        return JSONResponse(
            status_code=400,
            content={"error": f"Invalid status: {status}"},
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Failed to fetch tasks: {str(e)}"},
        )

    return JSONResponse(
        content={
            "tasks": [
                {
                    "id": t.id,
                    "issue_number": t.issue_number,
                    "issue_title": t.issue_title,
                    "status": t.status.value,
                    "current_stage": t.current_stage.value,
                    "pr_url": t.pr_url,
                }
                for t in tasks
            ]
        }
    )
