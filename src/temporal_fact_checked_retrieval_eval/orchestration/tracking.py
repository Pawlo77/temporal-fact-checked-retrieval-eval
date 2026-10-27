"""Local MLflow tracking helpers for resumable runs."""

import importlib
import json
import logging
import os
import warnings
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from ..config import ExperimentConfig, MLflowTrackingConfig
from .reproducibility import collect_reproducibility_report

_TRACKING_LOGGER = logging.getLogger(__name__)
_ACTIVE_MLFLOW_RUN_ID_ENV = "MLFLOW_ACTIVE_RUN_ID"


def _resolve_tracking_uri(tracking_uri: str) -> str:
    """Resolve local tracking URIs to an absolute path when needed."""
    if tracking_uri.startswith("sqlite:"):
        sqlite_target = tracking_uri.removeprefix("sqlite:")
        if sqlite_target.lstrip("/") == ":memory:":
            return "sqlite:///:memory:"

        if sqlite_target.startswith("///"):
            db_target = sqlite_target[3:]
        elif sqlite_target.startswith("//"):
            db_target = sqlite_target[2:]
        elif sqlite_target.startswith("/"):
            db_target = sqlite_target[1:]
        else:
            db_target = sqlite_target

        if not db_target:
            db_target = "mlruns.db"

        resolved_db_path = Path(db_target).expanduser().resolve()
        resolved_db_path.parent.mkdir(parents=True, exist_ok=True)
        return f"sqlite:///{resolved_db_path.as_posix()}"

    if "://" in tracking_uri and not tracking_uri.startswith("file:"):
        return tracking_uri

    resolved_path = Path(tracking_uri).expanduser().resolve()
    resolved_path.mkdir(parents=True, exist_ok=True)
    return str(resolved_path)


@dataclass(slots=True)
class MlflowRunTracker:
    """Track a single run with MLflow while tolerating offline/local-only setups."""

    tracking: MLflowTrackingConfig
    experiment_config: ExperimentConfig
    run_name: str
    model_adapter: Any = None

    _mlflow: Any = field(default=None, init=False, repr=False)
    _run_active: bool = field(default=False, init=False, repr=False)

    def start(self) -> None:
        """Start a run and log static hyperparameters and efficiency metrics."""
        if not self.tracking.enabled:
            return

        try:
            mlflow = importlib.import_module("mlflow")
            tracking_uri = _resolve_tracking_uri(self.tracking.tracking_uri)
            with warnings.catch_warnings():
                warnings.filterwarnings(
                    "ignore",
                    message="The filesystem tracking backend .*",
                    category=FutureWarning,
                )
                mlflow.set_tracking_uri(tracking_uri)
                mlflow.set_experiment(self.tracking.experiment_name)
                resume_run_id = os.environ.get(_ACTIVE_MLFLOW_RUN_ID_ENV)
                if resume_run_id:
                    try:
                        mlflow.start_run(run_id=resume_run_id)
                    except Exception:
                        _TRACKING_LOGGER.warning(
                            "Failed to resume MLflow run_id=%s; starting a new run.",
                            resume_run_id,
                        )
                        mlflow.start_run(
                            run_name=self.run_name or self.tracking.run_name
                        )
                else:
                    mlflow.start_run(run_name=self.run_name or self.tracking.run_name)

            self._mlflow = mlflow
            self._run_active = True

            active_run = mlflow.active_run()
            if active_run is not None:
                os.environ[_ACTIVE_MLFLOW_RUN_ID_ENV] = active_run.info.run_id

            mlflow.set_tag("pipeline.run_name", self.run_name)

            self._log_reproducibility_report()

        except Exception as e:
            _TRACKING_LOGGER.warning("Failed to start MLflow run: %s", e)
            self._run_active = False
            self._mlflow = None

    def _log_reproducibility_report(self) -> None:
        """Persist the reproducibility snapshot as an MLflow artifact."""
        report = collect_reproducibility_report()
        payload = report.to_dict()

        if self._run_active and self._mlflow is not None:
            self._mlflow.log_dict(payload, "reproducibility_report.json")
        else:
            _TRACKING_LOGGER.info(
                "MLflow inactive; reproducibility payload follows:\n%s",
                json.dumps(payload, indent=2, sort_keys=True),
            )

    def close(self) -> None:
        """End the active MLflow run if one was started."""
        if self._run_active and self._mlflow is not None:
            self._mlflow.end_run()
            self._run_active = False
            self._mlflow = None
            os.environ.pop(_ACTIVE_MLFLOW_RUN_ID_ENV, None)


def build_mlflow_tracker(
    experiment_config: ExperimentConfig,
    run_name: str | None = None,
    model_adapter: Any = None,
) -> MlflowRunTracker:
    """Build an MLflow tracker from an experiment configuration."""
    return MlflowRunTracker(
        tracking=experiment_config.mlflow,
        experiment_config=experiment_config,
        run_name=run_name or experiment_config.name,
        model_adapter=model_adapter,
    )
