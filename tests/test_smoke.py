"""Smoke tests for the temporal-fact-checked-retrieval-eval scaffold."""

from pathlib import Path


def test_package_imports() -> None:
    """Smoke test: package can be imported."""
    import temporal_fact_checked_retrieval_eval  # noqa: F401


def test_project_scaffold_layout() -> None:
    """Smoke test: expected top-level scaffold directories exist."""
    root = Path(__file__).resolve().parents[1]

    expected_paths = [
        root / "src" / "temporal_fact_checked_retrieval_eval",
        root / "tests",
        root / "notebooks",
        root / "configs",
        root / "configs" / "experiment.yaml",
        root / "report",
        root / "pyproject.toml",
        root / "README.md",
    ]

    missing = [
        str(path.relative_to(root)) for path in expected_paths if not path.exists()
    ]
    assert not missing, f"Missing scaffold paths: {missing}"
