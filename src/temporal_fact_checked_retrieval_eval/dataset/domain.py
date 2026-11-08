"""Core data model for a dated fact-check retrieval corpus.

Times are naive UTC datetimes at full precision (second resolution). A post or
fact-check may carry several dated instances (republications); the publication
time of an item is its earliest instance.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class Post:
    """A social-media post with one or more dated instances."""

    id: str
    instances: tuple[datetime, ...]
    language: str | None = None


@dataclass(frozen=True, slots=True)
class FactCheck:
    """A fact-check with one or more dated publication instances."""

    id: str
    instances: tuple[datetime, ...]
    language: str | None = None


@dataclass(frozen=True, slots=True)
class GoldPair:
    """A gold link between a post and the fact-check that debunks it."""

    post_id: str
    fact_check_id: str
    relationship: str | None = None


def earliest_time(instances: tuple[datetime, ...]) -> datetime | None:
    """Return the earliest instance time, or None when the item is undated."""
    return min(instances) if instances else None
