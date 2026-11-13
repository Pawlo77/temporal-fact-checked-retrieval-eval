"""Dataset-agnostic view of a dated fact-check retrieval corpus.

Every loader (synthetic, MultiClaim v1/v2, SemEval, a second dated dataset)
produces one :class:`DatedCorpus`; the protocol module reads only this shape, so
a new corpus is added by writing a loader, never by changing the protocols.
"""

from collections.abc import Mapping
from dataclasses import dataclass

from .domain import FactCheck, GoldPair, Post


@dataclass(frozen=True, slots=True)
class DatedCorpus:
    """Posts, fact-checks and gold pairs, keyed by id."""

    posts: Mapping[str, Post]
    fact_checks: Mapping[str, FactCheck]
    pairs: tuple[GoldPair, ...]
