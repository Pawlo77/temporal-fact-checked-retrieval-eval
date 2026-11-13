"""MultiClaim CSV loader producing a :class:`DatedCorpus`.

The MultiClaim (v1/v2) and SemEval-2025 Task 7 records are access-restricted and
research-only: their raw CSV files must never be committed to this repository.
Keep them in a gitignored directory (``data/``) or on the cluster and point this
loader at them. The repository ships only this loader and a synthetic fixture,
never post text.
"""

import ast
import csv
import logging
from datetime import UTC, datetime
from pathlib import Path

from .adapter import DatedCorpus
from .domain import FactCheck, GoldPair, Post

logger = logging.getLogger(__name__)

# shortcut: v1 posts carry no language column (detected language lives in the
# text tuple), so v1 post language is None; parse it only if the split needs v1.


def load_multiclaim(
    *,
    fact_checks_csv: Path,
    posts_csv: Path,
    mapping_csv: Path,
) -> DatedCorpus:
    """Load a MultiClaim corpus from three CSV files into a dated corpus.

    Args:
        fact_checks_csv: CSV with ``fact_check_id``, ``instances`` and an
            optional ``claim_detected_language_iso`` column.
        posts_csv: CSV with ``post_id``, ``instances`` and an optional
            ``post_detected_language_iso``; posts without dated instances are
            dropped and counted.
        mapping_csv: CSV with ``fact_check_id``, ``post_id`` and an optional
            ``relationship`` column.

    Returns:
        A corpus with all fact-checks, the dated posts, and the surviving pairs.
    """
    fact_checks = _load_fact_checks(fact_checks_csv)
    posts, dropped = _load_posts(posts_csv)
    logger.info("dropped %d undated posts", dropped)
    pairs = _load_pairs(mapping_csv, posts)
    return DatedCorpus(posts=posts, fact_checks=fact_checks, pairs=pairs)


def _parse_instances(raw: str) -> tuple[datetime, ...]:
    """Parse a Python-repr instance list into naive UTC datetimes.

    Instances are ``(timestamp, ref)`` tuples whose timestamp is either a unix
    float or an ISO datetime string (with or without an offset); ``None`` and the
    string ``"nan"`` mark a missing date and are skipped. Full second precision is
    kept so "before the post" means strictly before, down to the second.
    """
    entries = ast.literal_eval(raw) if raw and raw.strip() else ()
    times: list[datetime] = []
    for item in entries:
        timestamp = item[0]
        if timestamp is None:
            continue
        if isinstance(timestamp, str):
            if timestamp.strip().lower() == "nan":
                continue
            parsed = datetime.fromisoformat(timestamp)
            if parsed.tzinfo is None:
                parsed = parsed.replace(tzinfo=UTC)
        else:
            parsed = datetime.fromtimestamp(float(timestamp), tz=UTC)
        times.append(parsed.astimezone(UTC).replace(tzinfo=None))
    return tuple(times)


def _load_fact_checks(path: Path) -> dict[str, FactCheck]:
    """Read fact-checks from CSV, keeping every row including undated ones."""
    fact_checks: dict[str, FactCheck] = {}
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            fact_checks[row["fact_check_id"]] = FactCheck(
                id=row["fact_check_id"],
                instances=_parse_instances(row["instances"]),
                language=row.get("claim_detected_language_iso") or None,
            )
    return fact_checks


def _load_posts(path: Path) -> tuple[dict[str, Post], int]:
    """Read posts, dropping and counting rows without dated instances."""
    posts: dict[str, Post] = {}
    dropped = 0
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            instances = _parse_instances(row["instances"])
            if not instances:
                dropped += 1
                continue
            posts[row["post_id"]] = Post(
                id=row["post_id"],
                instances=instances,
                language=row.get("post_detected_language_iso") or None,
            )
    return posts, dropped


def _load_pairs(path: Path, posts: dict[str, Post]) -> tuple[GoldPair, ...]:
    """Read gold links, keeping only pairs whose post survived."""
    pairs: list[GoldPair] = []
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            post_id = row["post_id"]
            if post_id not in posts:
                continue
            pairs.append(
                GoldPair(
                    post_id=post_id,
                    fact_check_id=row["fact_check_id"],
                    relationship=row.get("relationship") or None,
                )
            )
    return tuple(pairs)
