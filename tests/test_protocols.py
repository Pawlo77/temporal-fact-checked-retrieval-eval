"""Tests for the temporal retrieval protocol layer."""

import random
from datetime import datetime

from temporal_fact_checked_retrieval_eval.dataset import (
    DatedCorpus,
    FactCheck,
    GoldPair,
    Post,
)
from temporal_fact_checked_retrieval_eval.protocols import (
    answerable,
    answerable_rate,
    build_causal_pool,
    build_size_matched_pool,
)


def _corpus() -> DatedCorpus:
    posts = {
        "p_early": Post("p_early", (datetime(2024, 2, 15),)),
        "p_mid": Post("p_mid", (datetime(2024, 3, 15),)),
        "p_late": Post("p_late", (datetime(2024, 5, 1),)),
        "p_undated": Post("p_undated", ()),
    }
    fact_checks = {
        "fc1": FactCheck("fc1", (datetime(2024, 1, 1),)),
        "fc2": FactCheck("fc2", (datetime(2024, 2, 1),)),
        "fc3": FactCheck("fc3", (datetime(2024, 3, 1),)),
        "fc4": FactCheck("fc4", (datetime(2024, 4, 1),)),
        "fc5": FactCheck("fc5", ()),
    }
    pairs = (
        GoldPair("p_early", "fc1"),
        GoldPair("p_mid", "fc4"),
        GoldPair("p_late", "missing_fc"),
        GoldPair("missing_post", "fc1"),
    )
    return DatedCorpus(posts=posts, fact_checks=fact_checks, pairs=pairs)


def test_build_causal_pool_strictly_before() -> None:
    corpus = _corpus()
    assert build_causal_pool(corpus, corpus.posts["p_late"]) == (
        "fc1",
        "fc2",
        "fc3",
        "fc4",
    )


def test_build_causal_pool_excludes_on_or_after() -> None:
    corpus = _corpus()
    assert build_causal_pool(corpus, corpus.posts["p_mid"]) == ("fc1", "fc2", "fc3")
    equal_time_post = Post("p_eq", (datetime(2024, 1, 1),))
    assert build_causal_pool(corpus, equal_time_post) == ()


def test_build_causal_pool_is_sorted() -> None:
    corpus = _corpus()
    pool = build_causal_pool(corpus, corpus.posts["p_late"])
    assert pool == tuple(sorted(pool))


def test_build_causal_pool_is_monotone() -> None:
    corpus = _corpus()
    early = set(build_causal_pool(corpus, corpus.posts["p_early"]))
    mid = set(build_causal_pool(corpus, corpus.posts["p_mid"]))
    late = set(build_causal_pool(corpus, corpus.posts["p_late"]))
    assert early <= mid <= late


def test_build_causal_pool_undated_post() -> None:
    corpus = _corpus()
    assert build_causal_pool(corpus, corpus.posts["p_undated"]) == ()


def test_answerable_true_when_gold_predates() -> None:
    corpus = _corpus()
    assert answerable(corpus, GoldPair("p_early", "fc1"))


def test_answerable_false_when_gold_postdates() -> None:
    corpus = _corpus()
    assert not answerable(corpus, GoldPair("p_mid", "fc4"))


def test_answerable_false_when_id_missing() -> None:
    corpus = _corpus()
    assert not answerable(corpus, GoldPair("p_late", "missing_fc"))
    assert not answerable(corpus, GoldPair("missing_post", "fc1"))


def test_answerable_rate_matches_fixture() -> None:
    corpus = _corpus()
    assert answerable_rate(corpus) == 0.25


def test_answerable_rate_empty_pairs() -> None:
    corpus = _corpus()
    empty = DatedCorpus(posts=corpus.posts, fact_checks=corpus.fact_checks, pairs=())
    assert answerable_rate(empty) == 0.0


def test_build_size_matched_pool_size_and_subset() -> None:
    corpus = _corpus()
    post = corpus.posts["p_early"]
    pool = build_size_matched_pool(corpus, post, random.Random(0))
    assert len(pool) == len(build_causal_pool(corpus, post))
    assert set(pool) <= set(corpus.fact_checks)
    assert "fc1" in pool


def test_build_size_matched_pool_empty_when_causal_empty() -> None:
    corpus = _corpus()
    pool = build_size_matched_pool(corpus, corpus.posts["p_undated"], random.Random(0))
    assert pool == ()


def test_build_size_matched_pool_deterministic() -> None:
    corpus = _corpus()
    post = corpus.posts["p_late"]
    first = build_size_matched_pool(corpus, post, random.Random(42))
    second = build_size_matched_pool(corpus, post, random.Random(42))
    assert first == second
