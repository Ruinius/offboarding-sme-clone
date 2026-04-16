---
trigger: always_on
---

### Python Environment & Dependency Management

- **Tooling:** Always use `uv` for Python-related tasks. Never use `pip` or `venv` directly.
- **Execution:** Run Python scripts and tools exclusively using `uv run`.
- **Dependencies:** Use `uv add <package>` to install new dependencies and ensure `pyproject.toml` and `uv.lock` are updated.
- **Environment:** If a virtual environment is missing, initialize it using `uv venv` before performing other tasks.
- **Commands:** Preferred pattern is `uv run python <file>.py` or `uv run <command>`.
