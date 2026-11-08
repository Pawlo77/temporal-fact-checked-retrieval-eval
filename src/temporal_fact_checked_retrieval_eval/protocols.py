"""Temporal retrieval protocols: causal pools and answerability."""

import random

from temporal_fact_checked_retrieval_eval.dataset import (
    DatedCorpus,
    GoldPair,
    Post,
    earliest_time,
)


def build_causal_pool(corpus: DatedCorpus, post: Post) -> tuple[str, ...]:
    """Return ids of fact-checks published strictly before ``post``.

    Args:
        corpus: The dated corpus.
        post: The post whose causal pool is built.

    Returns:
        Sorted fact-check ids whose earliest time precedes the post's earliest
        time. Empty when the post is undated or nothing predates it.
    """
    post_time = earliest_time(post.instances)
    if post_time is None:
        return ()
    ids: list[str] = []
    for fc_id, fc in corpus.fact_checks.items():
        fc_time = earliest_time(fc.instances)
        if fc_time is not None and fc_time < post_time:
            ids.append(fc_id)
    return tuple(sorted(ids))


def answerable(corpus: DatedCorpus, pair: GoldPair) -> bool:
    """Return whether ``pair`` is answerable.

    A pair is answerable when both its post and fact-check exist in the corpus
    and the fact-check was published strictly before the post.

    Args:
        corpus: The dated corpus.
        pair: The gold pair to test.

    Returns:
        True when the pair is answerable, otherwise False.
    """
    post = corpus.posts.get(pair.post_id)
    fact_check = corpus.fact_checks.get(pair.fact_check_id)
    if post is None or fact_check is None:
        return False
    post_time = earliest_time(post.instances)
    fact_check_time = earliest_time(fact_check.instances)
    return (
        post_time is not None
        and fact_check_time is not None
        and fact_check_time < post_time
    )


def build_size_matched_pool(
    corpus: DatedCorpus, post: Post, rng: random.Random
) -> tuple[str, ...]:
    """Return a random control pool matched in size to the causal pool.

    Samples without replacement from the full fact-check pool, forcing any
    answerable gold fact-check for ``post`` into the sample.

    Args:
        corpus: The dated corpus.
        post: The post whose pool is built.
        rng: Random number generator; the caller controls the seed.

    Returns:
        Sorted fact-check ids sized equal to the causal pool. Empty when the
        causal pool is empty.
    """
    target_size = len(build_causal_pool(corpus, post))
    if target_size == 0:
        return ()

    gold_ids = [
        pair.fact_check_id
        for pair in corpus.pairs
        if pair.post_id == post.id and answerable(corpus, pair)
    ]
    # shortcut: cap forced golds so the pool size invariant always holds.
    forced = sorted(set(gold_ids))[:target_size]
    forced_set = set(forced)
    candidates = [fc_id for fc_id in corpus.fact_checks if fc_id not in forced_set]
    sample = rng.sample(candidates, target_size - len(forced))
    return tuple(sorted([*forced, *sample]))


def answerable_rate(corpus: DatedCorpus) -> float:
    """Return the share of gold pairs that are answerable.

    Args:
        corpus: The dated corpus.

    Returns:
        Fraction of pairs that are answerable, or 0.0 when there are none.
    """
    if not corpus.pairs:
        return 0.0
    answerable_count = sum(answerable(corpus, pair) for pair in corpus.pairs)
    return answerable_count / len(corpus.pairs)
