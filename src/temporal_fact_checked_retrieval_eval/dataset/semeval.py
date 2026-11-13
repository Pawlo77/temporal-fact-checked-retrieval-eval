"""SemEval-2025 Task 7 loader producing a :class:`DatedCorpus`."""

import json
import logging
from pathlib import Path

from .adapter import DatedCorpus
from .domain import GoldPair
from .multiclaim import _load_fact_checks, _load_posts

logger = logging.getLogger(__name__)


def load_semeval(
    *,
    fact_checks_csv: Path,
    posts_csv: Path,
    reference_jsons: tuple[Path, ...],
) -> DatedCorpus:
    """Load a SemEval-2025 Task 7 corpus from CSVs and gold qrels.

    Args:
        fact_checks_csv: CSV with ``fact_check_id`` and ``instances`` (plus
            ``claim``/``title``, which are ignored).
        posts_csv: CSV with ``post_id`` and ``instances``; posts without dated
            instances are dropped and counted.
        reference_jsons: Gold qrels, each a JSON dict mapping a ``post_id`` to
            a list of fact-check ids.

    Returns:
        A corpus with all fact-checks, the dated posts, and the surviving pairs.
    """
    fact_checks = _load_fact_checks(fact_checks_csv)
    posts, dropped = _load_posts(posts_csv)
    logger.info("dropped %d undated posts", dropped)
    pairs: list[GoldPair] = []
    dropped_pairs = 0
    for reference_json in reference_jsons:
        with reference_json.open(encoding="utf-8") as handle:
            qrels = json.load(handle)
        for post_id, fact_check_ids in qrels.items():
            if post_id not in posts:
                dropped_pairs += len(fact_check_ids)
                continue
            pairs.extend(
                GoldPair(post_id=post_id, fact_check_id=str(fc_id), relationship=None)
                for fc_id in fact_check_ids
            )
    logger.info("dropped %d pairs for undated posts", dropped_pairs)
    return DatedCorpus(posts=posts, fact_checks=fact_checks, pairs=tuple(pairs))
