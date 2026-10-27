"""Tests for YAML experiment configuration."""

from pathlib import Path

import pytest

from temporal_fact_checked_retrieval_eval.config import (
    ConfigValidationError,
    ExperimentConfig,
    load_experiment_config,
)


def test_load_default_experiment_yaml() -> None:
    """Default config file parses with expected experiment name."""
    config = load_experiment_config(Path("configs/experiment.yaml"))
    assert config.name == "default-experiment"
    assert config.mlflow.experiment_name == "default-experiment"
    assert config.mlflow.enabled is True


def test_experiment_config_requires_name() -> None:
    """Empty experiment names are rejected."""
    with pytest.raises(ConfigValidationError):
        ExperimentConfig.from_dict({"name": "   "})


def test_mlflow_legacy_uri_normalized() -> None:
    """Legacy mlruns URI maps to SQLite backend."""
    config = ExperimentConfig.from_dict({
        "name": "run-a",
        "mlflow": {"tracking_uri": "mlruns"},
    })
    assert config.mlflow.tracking_uri == "sqlite:///mlruns.db"
