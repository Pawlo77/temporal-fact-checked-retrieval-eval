"""Descriptive statistics of a dated corpus: class balance, order, answerability."""

from collections import Counter
from datetime import datetime, timedelta
from statistics import median

from temporal_fact_checked_retrieval_eval.dataset import DatedCorpus, earliest_time


def corpus_summary(
    corpus: DatedCorpus,
    *,
    language: str | None = None,
    margins_days: tuple[int, ...] = (0, 1, 7),
) -> dict[str, float]:
    """Summarise ``corpus``, optionally as the monolingual slice of ``language``.

    Args:
        corpus: The dated corpus.
        language: Keep only posts and fact-checks of this language and the pairs
            between them; None keeps everything.
        margins_days: A pair is answerable at margin m when the fact-check is
            earlier than the post by more than m days.

    Returns:
        Counts, gold links per post, share of fact-checks with a linked post,
        pair order (post first, same day), and answerable pairs and posts per
        margin (``_m<days>`` keys). Posts with no pair are excluded from the
        answerable post share.
    """
    posts = {k: p for k, p in corpus.posts.items() if language in (None, p.language)}
    fcs = {
        k: f for k, f in corpus.fact_checks.items() if language in (None, f.language)
    }
    pairs = [p for p in corpus.pairs if p.post_id in posts and p.fact_check_id in fcs]
    per_post = Counter(p.post_id for p in pairs)
    timed: list[tuple[str, datetime, datetime]] = []
    for p in pairs:
        pt = earliest_time(posts[p.post_id].instances)
        ft = earliest_time(fcs[p.fact_check_id].instances)
        if pt is not None and ft is not None:
            timed.append((p.post_id, pt, ft))
    out: dict[str, float] = {
        "posts": len(posts),
        "fact_checks": len(fcs),
        "pairs": len(pairs),
        "dated_fact_checks": sum(bool(f.instances) for f in fcs.values()),
        "multi_instance_posts": sum(len(p.instances) > 1 for p in posts.values()),
        "multi_instance_fact_checks": sum(len(f.instances) > 1 for f in fcs.values()),
        "gold_per_post_mean": sum(per_post.values()) / len(per_post)
        if per_post
        else 0.0,
        "gold_per_post_median": median(per_post.values()) if per_post else 0.0,
        "fc_linked_share": (
            len({p.fact_check_id for p in pairs}) / len(fcs) if fcs else 0.0
        ),
        "post_first_pairs": sum(pt < ft for _, pt, ft in timed),
        "same_day_pairs": sum(pt.date() == ft.date() for _, pt, ft in timed),
    }
    for days in margins_days:
        hits = {i for i, pt, ft in timed if ft < pt - timedelta(days=days)}
        out[f"answerable_pairs_m{days}"] = sum(
            ft < pt - timedelta(days=days) for _, pt, ft in timed
        )
        out[f"answerable_posts_m{days}"] = len(hits)
        out[f"answerable_post_share_m{days}"] = (
            len(hits) / len(per_post) if per_post else 0.0
        )
    return out
