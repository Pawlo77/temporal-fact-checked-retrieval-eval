"""BM25 proof of concept: one query set under random, size-matched and causal pools."""

import re
from collections.abc import Callable, Mapping, Sequence
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


def evaluate_scores(
    corpus: DatedCorpus,
    score_fn: Callable[[str], np.ndarray],
    post_ids: Sequence[str],
    *,
    seed: int = 0,
    k: int = 10,
) -> list[dict[str, Any]]:
    """Rank each post under the three pools of one fixed query set.

    Args:
        corpus: Dated corpus; its fact-checks, in insertion order, are the full pool.
        score_fn: Post id to the scores of every fact-check, in corpus order.
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
        scores = score_fn(post_id)
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


def evaluate(
    corpus: DatedCorpus,
    fc_texts: Mapping[str, str],
    post_texts: Mapping[str, str],
    post_ids: Sequence[str],
    *,
    seed: int = 0,
    k: int = 10,
) -> list[dict[str, Any]]:
    """BM25 scores under the three pools (see :func:`evaluate_scores`).

    Document-frequency statistics come from the whole corpus; only the candidate
    set is restricted, so the causal pool still shares full-corpus statistics.

    Args:
        corpus: Dated corpus; its fact-checks are the full pool.
        fc_texts: Fact-check id to text.
        post_texts: Post id to text.
        post_ids: The query set.
        seed: Seed of the size-matched sampling.
        k: Cut-off of the reciprocal rank (MRR@k).

    Returns:
        The rows of :func:`evaluate_scores`.
    """
    retriever = bm25s.BM25()
    retriever.index(
        [tokenize(fc_texts.get(f, "")) for f in corpus.fact_checks], show_progress=False
    )
    return evaluate_scores(
        corpus,
        lambda post_id: retriever.get_scores(tokenize(post_texts.get(post_id, ""))),
        post_ids,
        seed=seed,
        k=k,
    )


def paired_permutation_p(
    a: Sequence[float] | np.ndarray,
    b: Sequence[float] | np.ndarray,
    *,
    resamples: int = 10_000,
    seed: int = 0,
) -> float:
    """Two-sided paired sign-flip permutation p-value for equal means.

    Args:
        a: Per-query scores of one system.
        b: Per-query scores of the other, aligned with ``a``.
        resamples: Random sign assignments of the per-query differences.
        seed: Seed of the sign draws.

    Returns:
        ``(hits + 1) / (resamples + 1)``, where a hit is a permuted mean difference at
        least as large in absolute value as the observed one.
    """
    diff = np.asarray(a, dtype=float) - np.asarray(b, dtype=float)
    if not diff.any():
        return 1.0
    rng = np.random.default_rng(seed)
    observed = abs(diff.sum())
    chunk = max(1, 2_000_000 // diff.size)
    hits = 0
    for start in range(0, resamples, chunk):
        signs = rng.choice((-1.0, 1.0), size=(min(chunk, resamples - start), diff.size))
        hits += int((np.abs(signs @ diff) >= observed - 1e-9).sum())
    return (hits + 1) / (resamples + 1)


def did_interval(
    rows_a: Sequence[dict[str, Any]],
    rows_b: Sequence[dict[str, Any]],
    *,
    resamples: int = 1000,
    seed: int = 0,
) -> dict[str, Any]:
    """Difference in differences of S@10, causal minus random, of query set A minus B.

    Args:
        rows_a: Output of :func:`evaluate` for the focus language.
        rows_b: Output of :func:`evaluate` for the control language.
        resamples: Bootstrap resamples, drawn independently within each query set.
        seed: Bootstrap seed.

    Returns:
        ``estimate`` and the 95% percentile interval ``ci``.
    """
    penalties = [
        np.array([float(r["causal"] > 0) - float(r["random"] > 0) for r in rows])
        for rows in (rows_a, rows_b)
    ]
    rng = np.random.default_rng(seed)
    boot = [
        p[rng.integers(0, len(p), (resamples, len(p)))].mean(axis=1) for p in penalties
    ]
    return {
        "estimate": float(penalties[0].mean() - penalties[1].mean()),
        "ci": [float(x) for x in np.percentile(boot[0] - boot[1], [2.5, 97.5])],
    }


def summarise(
    rows: Sequence[dict[str, Any]],
    *,
    resamples: int = 1000,
    permutations: int = 10_000,
    seed: int = 0,
) -> dict[str, Any]:
    """Mean S@10 and MRR@10 per protocol with paired bootstrap 95% intervals.

    Args:
        rows: Output of :func:`evaluate`.
        resamples: Bootstrap resamples over queries, shared by all protocols.
        permutations: Sign flips of the paired permutation tests.
        seed: Bootstrap and permutation seed.

    Returns:
        ``n``, ``n_answerable`` and, per protocol, ``all`` and ``answerable`` entries
        with ``s10``, ``mrr`` and their intervals ``s10_ci`` and ``mrr_ci``; ``tests``
        holds the paired permutation p-values of S@10 for each of the random and
        size-matched pools against the causal pool.
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
    out["tests"] = {}
    for label, keep in (
        ("all", np.ones(len(rows), bool)),
        ("answerable", answerable > 0),
    ):
        hit = {n: np.array([r[n] > 0 for r in rows], float)[keep] for n in PROTOCOLS}
        out["tests"][label] = {
            f"{n}_vs_causal": paired_permutation_p(
                hit[n], hit["causal"], resamples=permutations, seed=seed
            )
            for n in ("random", "size_matched")
        }
    return out
