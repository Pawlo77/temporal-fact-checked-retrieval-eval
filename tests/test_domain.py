"""Tests for the dated-corpus domain model."""

from datetime import datetime

from temporal_fact_checked_retrieval_eval.dataset.domain import earliest_time


def test_earliest_time_returns_earliest_instance() -> None:
    instances = (
        datetime(2024, 5, 1),
        datetime(2024, 6, 1),
        datetime(2024, 4, 1),
    )
    assert earliest_time(instances) == datetime(2024, 4, 1)


def test_earliest_time_returns_none_when_undated() -> None:
    assert earliest_time(()) is None
