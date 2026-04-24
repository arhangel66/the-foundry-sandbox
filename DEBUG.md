# DEBUG.md

Верифицированные команды для запуска, тестирования и отладки.

## Запуск сервера

```bash
# Dev-режим с авто-перезагрузкой
uv run uvicorn src.api.main:app --reload --port 8101

# Из корня проекта без --reload
uv run uvicorn src.api.main:app --port 8101
```

## Тесты

```bash
# Все тесты
uv run pytest

# Один тест
uv run pytest tests/test_calculator.py::test_addition -v

# Только HTTP-интеграционные тесты
uv run pytest tests/test_calculator.py -k "http" -v
```

## Проверка API вручную (curl)

```bash
# Health check
curl http://localhost:8101/health

# Сложение
curl -X POST http://localhost:8101/api/calculate \
  -d "operand1=1&operand2=2&operation=+" \
  -H "Content-Type: application/x-www-form-urlencoded"
# → {"result":3.0}

# Деление на ноль
curl -X POST http://localhost:8101/api/calculate \
  -d "operand1=5&operand2=0&operation=/" \
  -H "Content-Type: application/x-www-form-urlencoded"
# → {"detail":"Division by zero"}

# Неизвестная операция
curl -X POST http://localhost:8101/api/calculate \
  -d "operand1=5&operand2=3&operation=%" \
  -H "Content-Type: application/x-www-form-urlencoded"
# → {"detail":"Unsupported operation: %"}
```

## Диагностика типичных ошибок

### `RuntimeError: Form data requires "python-multipart"`

Причина: `python-multipart` не установлен, но `main.py` использует `Form(...)`.

```bash
uv add python-multipart
uv sync
```

### `405 Method Not Allowed` на POST /api/calculate

Причина: `StaticFiles` смонтирован на `/` ДО регистрации роутов. Mount на `/` перехватывает все пути.

Исправление: вызов `app.mount("/", ...)` должен быть последним в `main.py`, после всех `@app.post`/`@app.get`.

### Тесты запускаются с родительским venv (в git worktree)

`uv run pytest` может подхватить venv родительского проекта, если `pytest` не установлен локально.

```bash
uv add --dev pytest httpx
uv run pytest
```

### Импорт `api.main` падает при коллекции тестов

Проверь, что `pythonpath = ["src"]` задан в `[tool.pytest.ini_options]` в `pyproject.toml`.
