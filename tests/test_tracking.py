"""Tests for MLflow tracking URI handling."""

from pathlib import Path

import pytest

from temporal_fact_checked_retrieval_eval.orchestration import tracking


def test_sqlite_busy_timeout_survives_resolution(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The ``?timeout=`` query stays outside the resolved database path."""
    monkeypatch.chdir(tmp_path)
    uri = tracking._resolve_tracking_uri("sqlite:///mlruns.db?timeout=300")
    db = (tmp_path / "mlruns.db").resolve().as_posix()
    assert uri == f"sqlite:///{db}?timeout=300"
