"""Tests for the synthetic dated corpus generator."""

from temporal_fact_checked_retrieval_eval.dataset import earliest_time
from temporal_fact_checked_retrieval_eval.dataset.synthetic import make_synthetic_corpus


def test_same_seed_is_deterministic() -> None:
    first = make_synthetic_corpus(seed=123)
    second = make_synthetic_corpus(seed=123)
    assert list(first.posts) == list(second.posts)
    assert list(first.fact_checks) == list(second.fact_checks)
    assert first.pairs == second.pairs


def test_has_answerable_and_unanswerable_pairs() -> None:
    corpus = make_synthetic_corpus(seed=0)
    answerable = 0
    unanswerable = 0
    for pair in corpus.pairs:
        post_time = earliest_time(corpus.posts[pair.post_id].instances)
        fact_check_time = earliest_time(
            corpus.fact_checks[pair.fact_check_id].instances
        )
        if (
            post_time is not None
            and fact_check_time is not None
            and fact_check_time < post_time
        ):
            answerable += 1
        else:
            unanswerable += 1
    assert answerable > 0
    assert unanswerable > 0


def test_includes_undated_post() -> None:
    corpus = make_synthetic_corpus(seed=0)
    undated = [
        post for post in corpus.posts.values() if earliest_time(post.instances) is None
    ]
    assert undated


def test_all_pairs_resolve() -> None:
    corpus = make_synthetic_corpus(seed=0)
    assert len(corpus.pairs) == len(corpus.posts)
    for pair in corpus.pairs:
        assert pair.post_id in corpus.posts
        assert pair.fact_check_id in corpus.fact_checks
