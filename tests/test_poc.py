"""Tests for the BM25 proof of concept."""

from datetime import datetime

import numpy as np
import pytest

from temporal_fact_checked_retrieval_eval.dataset import (
    DatedCorpus,
    FactCheck,
    GoldPair,
    Post,
)
from temporal_fact_checked_retrieval_eval.poc import (
    did_interval,
    evaluate,
    evaluate_scores,
    paired_permutation_p,
    summarise,
    tokenize,
)


def _setup() -> tuple[DatedCorpus, dict[str, str], dict[str, str]]:
    fc_texts = {
        "f_early": "vaccine microchip claim debunked",
        "f_late": "election fraud claim debunked",
        "f_noise1": "moon landing hoax",
        "f_noise2": "flat earth theory",
        "f_noise3": "water fluoride plot",
    }
    fact_checks = {
        "f_early": FactCheck("f_early", (datetime(2024, 1, 1),)),
        "f_late": FactCheck("f_late", (datetime(2024, 6, 1),)),
        "f_noise1": FactCheck("f_noise1", (datetime(2023, 1, 1),)),
        "f_noise2": FactCheck("f_noise2", (datetime(2023, 2, 1),)),
        "f_noise3": FactCheck("f_noise3", ()),
    }
    posts = {
        "p_ok": Post("p_ok", (datetime(2024, 3, 1),)),
        "p_late": Post("p_late", (datetime(2024, 3, 1),)),
    }
    post_texts = {
        "p_ok": "vaccine microchip claim",
        "p_late": "election fraud claim",
    }
    pairs = (GoldPair("p_ok", "f_early"), GoldPair("p_late", "f_late"))
    return DatedCorpus(posts, fact_checks, pairs), fc_texts, post_texts


def test_tokenize_lowercases_words() -> None:
    assert tokenize("Hello, WORLD-wide 2024!") == ["hello", "world", "wide", "2024"]


def test_causal_pool_hides_later_gold_but_random_finds_it() -> None:
    corpus, fc_texts, post_texts = _setup()
    rows = {
        r["post_id"]: r
        for r in evaluate(corpus, fc_texts, post_texts, ["p_ok", "p_late"])
    }
    assert rows["p_ok"]["answerable"] is True
    assert rows["p_ok"]["causal"] == 1.0
    assert rows["p_late"]["answerable"] is False
    assert rows["p_late"]["random"] == 1.0
    assert rows["p_late"]["causal"] == 0.0


def test_size_matched_keeps_answerable_gold_and_pool_size() -> None:
    corpus, fc_texts, post_texts = _setup()
    rows = evaluate(corpus, fc_texts, post_texts, ["p_ok"], seed=3)
    assert rows[0]["size_matched"] == 1.0
    assert rows[0]["pool_size"] == 3  # f_early, f_noise1, f_noise2 are before the post


def test_summarise_means_and_interval() -> None:
    corpus, fc_texts, post_texts = _setup()
    rows = evaluate(corpus, fc_texts, post_texts, ["p_ok", "p_late"])
    out = summarise(rows, resamples=200)
    assert out["causal"]["all"]["s10"] == 0.5
    assert out["causal"]["answerable"]["s10"] == 1.0
    assert out["random"]["all"]["s10"] == 1.0
    low, high = out["causal"]["all"]["s10_ci"]
    assert low <= 0.5 <= high
    assert out["n"] == 2
    assert out["n_answerable"] == 1


def test_summarise_rejects_empty() -> None:
    with pytest.raises(ValueError, match="no queries"):
        summarise([])


def test_permutation_p_detects_a_shift_and_accepts_equal_scores() -> None:
    zeros = [0.0] * 200
    ones = [1.0] * 200
    assert paired_permutation_p(ones, zeros, resamples=999) < 0.01
    assert paired_permutation_p(ones, ones, resamples=999) == 1.0


def test_summarise_reports_paired_tests() -> None:
    rows = [
        {"answerable": True, "random": 1.0, "size_matched": 1.0, "causal": 0.0}
        for _ in range(60)
    ]
    out = summarise(rows, resamples=100, permutations=499)
    assert out["tests"]["all"]["random_vs_causal"] < 0.05
    assert out["tests"]["answerable"]["size_matched_vs_causal"] < 0.05


def test_did_interval_is_the_difference_of_penalties() -> None:
    pl = [{"random": 1.0, "causal": 0.0}] * 50 + [{"random": 1.0, "causal": 1.0}] * 50
    en = [{"random": 1.0, "causal": 0.0}] * 20 + [{"random": 1.0, "causal": 1.0}] * 80
    out = did_interval(pl, en, resamples=300)
    assert out["estimate"] == pytest.approx(-0.30)
    assert out["ci"][0] < -0.30 < out["ci"][1]


def test_evaluate_scores_uses_the_given_scores_under_every_pool() -> None:
    corpus, _, _ = _setup()
    order = list(corpus.fact_checks)

    def oracle(post_id: str) -> np.ndarray:
        gold = {p.fact_check_id for p in corpus.pairs if p.post_id == post_id}
        return np.array([1.0 if f in gold else 0.0 for f in order])

    rows = {
        r["post_id"]: r for r in evaluate_scores(corpus, oracle, ["p_ok", "p_late"])
    }
    assert rows["p_ok"]["causal"] == 1.0
    assert rows["p_late"]["random"] == 1.0
    assert rows["p_late"]["causal"] == 0.0
