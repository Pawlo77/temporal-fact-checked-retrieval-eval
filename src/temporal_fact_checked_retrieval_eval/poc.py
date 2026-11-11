"""BM25 proof of concept: one query set under random, size-matched and causal pools."""

import re
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Any

import bm25s  # type: ignore[import-untyped]
import numpy as np

from temporal_fact_checked_retrieval_eval.dataset import DatedCorpus, earliest_time

PROTOCOLS = ("random", "size_matched", "causal")
_EPOCH = datetime(1970, 1, 1)
_TOKEN = re.compile(r"\w+")


def tokenize(text: str) -> list[str]:
    """Lowercase word tokens."""
    return _TOKEN.findall(text.lower())


def _rank_score(
    scores: np.ndarray, mask: np.ndarray, gold: np.ndarray, k: int
) -> float:
    """Reciprocal rank of the first gold item in the top ``k`` of the masked pool."""
    in_pool = np.flatnonzero(mask)
    if in_pool.size == 0:
        return 0.0
    top = in_pool[np.argsort(-scores[in_pool], kind="stable")[:k]]
    hits = np.flatnonzero(np.isin(top, gold))
    return 1.0 / (hits[0] + 1) if hits.size else 0.0


def evaluate(
    corpus: DatedCorpus,
    fc_texts: Mapping[str, str],
    post_texts: Mapping[str, str],
    post_ids: Sequence[str],
    *,
    seed: int = 0,
    k: int = 10,
) -> list[dict[str, Any]]:
    """Score each post with BM25 under the three pools of one fixed query set.

    Document-frequency statistics come from the whole corpus; only the candidate
    set is restricted, so the causal pool still shares full-corpus statistics.

    Args:
        corpus: Dated corpus; its fact-checks are the full pool.
        fc_texts: Fact-check id to text.
        post_texts: Post id to text.
        post_ids: The query set, scored identically under every protocol.
        seed: Seed of the size-matched sampling.
        k: Cut-off of the reciprocal rank (MRR@k).

    Returns:
        One row per post: ``answerable`` (a gold fact-check predates it),
        ``pool_size`` (causal pool size) and the reciprocal rank at ``k`` under
        ``random``, ``size_matched`` and ``causal``; 0 when no gold is in the top ``k``.
    """
    fc_ids = list(corpus.fact_checks)
    index = {fc: i for i, fc in enumerate(fc_ids)}
    times = np.array([
        (t - _EPOCH).total_seconds()
        if (t := earliest_time(corpus.fact_checks[f].instances))
        else np.inf
        for f in fc_ids
    ])
    retriever = bm25s.BM25()
    retriever.index(
        [tokenize(fc_texts.get(f, "")) for f in fc_ids], show_progress=False
    )
    gold_of: dict[str, list[int]] = {}
    for pair in corpus.pairs:
        if pair.fact_check_id in index:
            gold_of.setdefault(pair.post_id, []).append(index[pair.fact_check_id])
    rng = np.random.default_rng(seed)
    rows = []
    for post_id in post_ids:
        post_time = earliest_time(corpus.posts[post_id].instances)
        if post_time is None:
            msg = f"post {post_id} is undated"
            raise ValueError(msg)
        causal = times < (post_time - _EPOCH).total_seconds()
        gold = np.array(gold_of.get(post_id, []), dtype=int)
        gold_in_pool = gold[causal[gold]] if gold.size else gold
        scores = retriever.get_scores(tokenize(post_texts.get(post_id, "")))
        size = int(causal.sum())
        forced = np.unique(gold_in_pool)[:size]
        pool = np.zeros_like(causal)
        pool[forced] = True
        others = np.flatnonzero(~pool)
        pool[rng.choice(others, size - forced.size, replace=False)] = True
        rows.append({
            "post_id": post_id,
            "answerable": bool(gold_in_pool.size),
            "pool_size": size,
            "random": _rank_score(scores, np.ones_like(causal), gold, k),
            "size_matched": _rank_score(scores, pool, gold, k),
            "causal": _rank_score(scores, causal, gold, k),
        })
    return rows


def summarise(
    rows: Sequence[dict[str, Any]], *, resamples: int = 1000, seed: int = 0
) -> dict[str, Any]:
    """Mean S@10 and MRR@10 per protocol with paired bootstrap 95% intervals.

    Args:
        rows: Output of :func:`evaluate`.
        resamples: Bootstrap resamples over queries, shared by all protocols.
        seed: Bootstrap seed.

    Returns:
        ``n``, ``n_answerable`` and, per protocol, ``all`` and ``answerable`` entries
        with ``s10``, ``mrr`` and their intervals ``s10_ci`` and ``mrr_ci``.
    """
    if not rows:
        msg = "no queries to summarise"
        raise ValueError(msg)
    answerable = np.array([r["answerable"] for r in rows], dtype=float)
    draws = np.random.default_rng(seed).integers(0, len(rows), (resamples, len(rows)))
    out: dict[str, Any] = {"n": len(rows), "n_answerable": int(answerable.sum())}
    for name in PROTOCOLS:
        rr = np.array([r[name] for r in rows])
        out[name] = {}
        for label, weight in (("all", np.ones(len(rows))), ("answerable", answerable)):
            out[name][label] = {}
            for key, values in (("s10", (rr > 0).astype(float)), ("mrr", rr)):
                total = weight.sum()
                denominator = weight[draws].sum(axis=1)
                boot = (values * weight)[draws].sum(axis=1) / np.where(
                    denominator, denominator, np.nan
                )
                out[name][label][key] = (
                    float((values * weight).sum() / total) if total else 0.0
                )
                out[name][label][f"{key}_ci"] = (
                    [float(x) for x in np.nanpercentile(boot, [2.5, 97.5])]
                    if total
                    else [0.0, 0.0]
                )
    return out
