"""Typed experiment configuration loaded from YAML."""

from collections.abc import Mapping
from dataclasses import dataclass, field, fields, is_dataclass
from pathlib import Path
from typing import Any, Self, cast

import yaml


class ConfigValidationError(ValueError):
    """Raised when a configuration value is invalid."""


def _require(condition: bool, message: str) -> None:
    """Raise a validation error when a condition is false."""
    if not condition:
        raise ConfigValidationError(message)


def _require_str(name: str, value: str) -> None:
    """Validate that a value is a non-empty string."""
    _require(isinstance(value, str), f"{name} must be a string.")
    _require(bool(value.strip()), f"{name} must not be empty.")


def _serialize(value: Any) -> Any:
    """Convert nested dataclasses and tuples into JSON-friendly values."""
    if is_dataclass(value):
        return {
            field.name: _serialize(getattr(value, field.name))
            for field in fields(value)
        }
    if isinstance(value, tuple):
        return [_serialize(item) for item in value]
    if isinstance(value, list):
        return [_serialize(item) for item in value]
    if isinstance(value, Mapping):
        return {str(key): _serialize(item) for key, item in value.items()}
    return value


def _extract_mapping(data: Mapping[str, Any] | Any, name: str) -> Mapping[str, Any]:
    """Validate and return a mapping for deserialization."""
    _require(isinstance(data, Mapping), f"{name} must be a mapping.")
    return data


@dataclass(frozen=True, slots=True)
class MLflowTrackingConfig:
    """Local MLflow tracking configuration."""

    enabled: bool = True
    """Enable MLflow tracking."""
    tracking_uri: str = "sqlite:///mlruns.db"
    """MLflow tracking URI (SQLite backend for SQL-based trace metrics support)."""
    experiment_name: str = "default-experiment"
    """MLflow experiment name."""
    run_name: str | None = None
    """Optional MLflow run name."""
    log_params: bool = True
    """Log hyperparameters to MLflow."""
    log_metrics: bool = True
    """Log metrics to MLflow."""
    log_artifacts: bool = True
    """Log artifacts to MLflow."""
    retain_local_checkpoints: bool = False
    """Keep local checkpoint files after they are uploaded to MLflow artifacts."""

    def __post_init__(self) -> None:
        """Validate the field values."""
        if self.enabled:
            _require_str("tracking_uri", self.tracking_uri)
        _require_str("experiment_name", self.experiment_name)
        if self.run_name is not None:
            _require_str("run_name", self.run_name)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable representation of the MLflow config."""
        return dict(_serialize(self))

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Self:
        """Build an MLflow tracking config from a mapping."""
        mapping = _extract_mapping(data, name="MLflowTrackingConfig")
        if mapping.get("tracking_uri") == "mlruns":
            mapping = {**mapping, "tracking_uri": "sqlite:///mlruns.db"}
        return cls(**cast("dict[str, Any]", dict(mapping)))


@dataclass(frozen=True, slots=True)
class ExperimentConfig:
    """Top-level experiment configuration."""

    name: str = "default-experiment"
    """Human-readable experiment name."""
    mlflow: MLflowTrackingConfig = field(default_factory=MLflowTrackingConfig)
    """MLflow tracking settings for this experiment."""

    def __post_init__(self) -> None:
        """Validate the field values."""
        _require_str("name", self.name)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable representation of the experiment config."""
        return dict(_serialize(self))

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Self:
        """Build an experiment config from a mapping."""
        mapping = _extract_mapping(data, name="ExperimentConfig")
        mlflow_data = mapping.get("mlflow", {})
        mlflow_config = (
            MLflowTrackingConfig.from_dict(mlflow_data)
            if mlflow_data
            else MLflowTrackingConfig()
        )
        name = str(mapping.get("name", "default-experiment"))
        return cls(name=name, mlflow=mlflow_config)


def load_experiment_config(path: Path | str) -> ExperimentConfig:
    """Load and validate an experiment config from a YAML file.

    Args:
        path: Path to a YAML file with ``experiment`` and ``mlflow`` sections.

    Returns:
        Parsed experiment configuration.

    Raises:
        ConfigValidationError: If the file structure or values are invalid.
        FileNotFoundError: If ``path`` does not exist.
    """
    config_path = Path(path)
    raw = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    _require(isinstance(raw, Mapping), "Config root must be a mapping.")

    experiment_section = raw.get("experiment", {})
    _require(
        isinstance(experiment_section, Mapping),
        "experiment section must be a mapping.",
    )
    merged: dict[str, Any] = dict(experiment_section)
    if "mlflow" in raw:
        merged["mlflow"] = raw["mlflow"]
    return ExperimentConfig.from_dict(merged)
