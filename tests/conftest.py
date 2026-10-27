"""Pytest configuration and fixtures for temporal-fact-checked-retrieval-eval tests."""

import shutil
from contextlib import suppress
from pathlib import Path

import pytest


@pytest.fixture(autouse=True)
def cleanup_mlflow_artifacts() -> None:
    """Remove repository-root MLflow data created during a test."""
    root = Path(__file__).resolve().parents[1]
    tracked_root = root / "mlruns"
    tracked_files = [
        root / "mlruns.db",
        root / "mlruns.db-wal",
        root / "mlruns.db-shm",
        root / "mlruns.db-journal",
    ]

    baseline_file_exists = {path: path.exists() for path in tracked_files}
    baseline_paths = set()
    if tracked_root.exists():
        baseline_paths = {path.relative_to(root) for path in tracked_root.rglob("*")}

    try:
        yield
    finally:
        if tracked_root.exists():
            current_paths = sorted(
                (path for path in tracked_root.rglob("*") if path != tracked_root),
                key=lambda path: len(path.parts),
                reverse=True,
            )
            for path in current_paths:
                relative_path = path.relative_to(root)
                if relative_path in baseline_paths:
                    continue
                if path.is_dir():
                    shutil.rmtree(path, ignore_errors=True)
                else:
                    with suppress(FileNotFoundError):
                        path.unlink()

        for path in tracked_files:
            if path.exists() and path.is_file() and not baseline_file_exists[path]:
                with suppress(FileNotFoundError):
                    path.unlink()
