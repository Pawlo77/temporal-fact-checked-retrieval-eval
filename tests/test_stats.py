"""Tests for corpus summary statistics."""

from datetime import datetime

from temporal_fact_checked_retrieval_eval.dataset import (
    DatedCorpus,
    FactCheck,
    GoldPair,
    Post,
)
from temporal_fact_checked_retrieval_eval.stats import corpus_summary


def _corpus() -> DatedCorpus:
    posts = {
        "p1": Post("p1", (datetime(2024, 3, 1, 12),), "pl"),
        "p2": Post("p2", (datetime(2024, 3, 1, 8), datetime(2024, 4, 1)), "pl"),
        "p3": Post("p3", (datetime(2024, 1, 1),), "en"),
    }
    fact_checks = {
        "f1": FactCheck("f1", (datetime(2024, 2, 1),), "pl"),
        "f2": FactCheck("f2", (datetime(2024, 3, 1, 9),), "pl"),
        "f3": FactCheck("f3", (), "pl"),
        "f4": FactCheck("f4", (datetime(2024, 5, 1),), "en"),
    }
    pairs = (
        GoldPair("p1", "f1"),  # fc 29 days before the post
        GoldPair("p1", "f2"),  # fc 3 h before, same day
        GoldPair("p2", "f2"),  # post 1 h before the fc, same day
        GoldPair("p3", "f4"),  # fc after the post
    )
    return DatedCorpus(posts=posts, fact_checks=fact_checks, pairs=pairs)


def test_counts_and_balance() -> None:
    s = corpus_summary(_corpus())
    assert (s["posts"], s["fact_checks"], s["pairs"]) == (3, 4, 4)
    assert s["dated_fact_checks"] == 3
    assert s["multi_instance_posts"] == 1
    assert s["gold_per_post_mean"] == 4 / 3
    assert s["gold_per_post_median"] == 1
    assert s["fc_linked_share"] == 3 / 4


def test_order_ties_and_answerable() -> None:
    s = corpus_summary(_corpus())
    assert s["post_first_pairs"] == 2
    assert s["same_day_pairs"] == 2
    assert s["answerable_pairs_m0"] == 2
    assert s["answerable_pairs_m1"] == 1
    assert s["answerable_pairs_m7"] == 1
    assert s["answerable_posts_m0"] == 1
    assert s["answerable_post_share_m0"] == 1 / 3


def test_language_slice_is_monolingual() -> None:
    s = corpus_summary(_corpus(), language="pl")
    assert (s["posts"], s["fact_checks"], s["pairs"]) == (2, 3, 3)
    assert s["answerable_posts_m0"] == 1


def test_empty_corpus() -> None:
    empty = DatedCorpus(posts={}, fact_checks={}, pairs=())
    s = corpus_summary(empty)
    assert s["pairs"] == 0
    assert s["gold_per_post_mean"] == 0.0
    assert s["answerable_post_share_m0"] == 0.0
