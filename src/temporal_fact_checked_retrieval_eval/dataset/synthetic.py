"""Synthetic dated fact-check retrieval corpus generator."""

import random
from datetime import date, datetime, time

from .adapter import DatedCorpus
from .domain import FactCheck, GoldPair, Post, earliest_time

_START_DAY = date(2023, 1, 1)
_END_DAY = date(2024, 6, 1)
_UNDATED_SHARE = 0.02
_ANSWERABLE_SHARE = 0.5


def make_synthetic_corpus(
    *,
    seed: int = 0,
    n_posts: int = 200,
    n_fact_checks: int = 300,
    languages: tuple[str, ...] = ("pl", "en"),
) -> DatedCorpus:
    """Build a deterministic synthetic corpus of dated posts and fact-checks.

    Args:
        seed: Seed for the local random generator, so results are reproducible.
        n_posts: Number of synthetic posts to generate.
        n_fact_checks: Number of synthetic fact-checks to generate.
        languages: Languages assigned at random (seeded) to each item.

    Returns:
        A corpus with ``n_posts`` posts, ``n_fact_checks`` fact-checks, and one
        gold pair per post split roughly evenly between answerable and not.
    """
    rng = random.Random(seed)  # nosec B311 - seeded for reproducibility, not security
    posts = {
        post_id: _make_post(rng, post_id, languages) for post_id in _ids("p", n_posts)
    }
    fact_checks = {
        fact_check_id: _make_fact_check(rng, fact_check_id, languages)
        for fact_check_id in _ids("fc", n_fact_checks)
    }
    pairs = _make_pairs(rng, posts, fact_checks)
    return DatedCorpus(posts=posts, fact_checks=fact_checks, pairs=pairs)


def _ids(prefix: str, count: int) -> list[str]:
    """Return zero-padded ids ``prefix000``..``prefix{count-1}``."""
    width = max(3, len(str(count)))
    return [f"{prefix}{index:0{width}d}" for index in range(count)]


def _make_post(rng: random.Random, post_id: str, languages: tuple[str, ...]) -> Post:
    """Create a post with 1-3 dated instances, or ~2% undated."""
    if rng.random() < _UNDATED_SHARE:
        instances: tuple[datetime, ...] = ()
    else:
        instances = tuple(_random_day(rng) for _ in range(rng.randint(1, 3)))
    return Post(id=post_id, instances=instances, language=rng.choice(languages))


def _make_fact_check(
    rng: random.Random, fact_check_id: str, languages: tuple[str, ...]
) -> FactCheck:
    """Create a fact-check with 1-2 dated instances."""
    instances = tuple(_random_day(rng) for _ in range(rng.randint(1, 2)))
    return FactCheck(
        id=fact_check_id, instances=instances, language=rng.choice(languages)
    )


def _random_day(rng: random.Random) -> datetime:
    """Return a naive UTC datetime at midnight on a random day in range."""
    ordinal = rng.randint(_START_DAY.toordinal(), _END_DAY.toordinal())
    return datetime.combine(date.fromordinal(ordinal), time.min)


def _make_pairs(
    rng: random.Random,
    posts: dict[str, Post],
    fact_checks: dict[str, FactCheck],
) -> tuple[GoldPair, ...]:
    """Link each post to one fact-check, roughly half answerable."""
    fact_check_ids = list(fact_checks)
    return tuple(
        GoldPair(
            post_id=post.id,
            fact_check_id=_pick_fact_check(rng, post, fact_checks, fact_check_ids),
            relationship=rng.choice(("claimreview_schema", None)),
        )
        for post in posts.values()
    )


def _pick_fact_check(
    rng: random.Random,
    post: Post,
    fact_checks: dict[str, FactCheck],
    fact_check_ids: list[str],
) -> str:
    """Choose a fact-check, before the post when the coin wants answerable."""
    post_time = earliest_time(post.instances)
    if post_time is None:
        return rng.choice(fact_check_ids)
    answerable = rng.random() < _ANSWERABLE_SHARE
    candidates: list[str] = []
    for fact_check_id in fact_check_ids:
        fact_check_time = earliest_time(fact_checks[fact_check_id].instances)
        if fact_check_time is None:
            continue
        before = fact_check_time < post_time
        if (answerable and before) or (not answerable and not before):
            candidates.append(fact_check_id)
    if not candidates:
        return rng.choice(fact_check_ids)
    return rng.choice(candidates)
