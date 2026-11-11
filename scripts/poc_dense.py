"""Run a dense encoder through the three-pool proof of concept on MultiClaim v2.

Usage: uv run --extra dense python scripts/poc_dense.py MODEL [data/raw] [lang[:n] ...]
MODEL is ``e5`` (intfloat/multilingual-e5-large) or ``mmlw``
(sdadas/mmlw-retrieval-roberta-large, Polish). Same query sets as ``poc_bm25.py``;
prints scores, wall time and peak memory as JSON. Post text is never printed.
"""

import json
import platform
import resource
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np
from poc_bm25 import _texts
from sentence_transformers import SentenceTransformer

from temporal_fact_checked_retrieval_eval.dataset import DatedCorpus
from temporal_fact_checked_retrieval_eval.dataset.multiclaim import load_multiclaim
from temporal_fact_checked_retrieval_eval.poc import (
    did_interval,
    evaluate_scores,
    summarise,
)

MODELS = {
    "e5": ("intfloat/multilingual-e5-large", "query: ", "passage: "),
    "mmlw": ("sdadas/mmlw-retrieval-roberta-large", "zapytanie: ", ""),
}
SEEDS = (0, 1, 2)


def main(model_key: str, root: Path, languages: list[str]) -> None:
    """Encode each language slice once and score it under three seeds."""
    name, query_prefix, passage_prefix = MODELS[model_key]
    model = SentenceTransformer(name)
    folder = root / "multiclaim_v2"
    corpus = load_multiclaim(
        fact_checks_csv=folder / "fact_checks.csv",
        posts_csv=folder / "posts.csv",
        mapping_csv=folder / "fact_check_post_mapping.csv",
    )
    fc_texts = _texts(folder / "fact_checks.csv", "fact_check_id", ("claim", "title"))
    post_texts = _texts(folder / "posts.csv", "post_id", ("post_body",))
    out: dict[str, Any] = {"model": name, "hardware": platform.platform()}
    by_lang: dict[str, list[dict[str, Any]]] = {}
    for spec in languages:
        lang, _, size = spec.partition(":")
        posts = {k: p for k, p in corpus.posts.items() if p.language == lang}
        fcs = {k: f for k, f in corpus.fact_checks.items() if f.language == lang}
        pairs = tuple(
            p for p in corpus.pairs if p.post_id in posts and p.fact_check_id in fcs
        )
        sub = DatedCorpus(posts=posts, fact_checks=fcs, pairs=pairs)
        queries = sorted({p.post_id for p in pairs})
        if size:
            pick = np.random.default_rng(0).choice(len(queries), int(size), False)
            queries = [queries[i] for i in sorted(pick)]
        start = time.perf_counter()
        fc_emb = model.encode(
            [passage_prefix + fc_texts[f] for f in fcs],
            batch_size=128,
            normalize_embeddings=True,
            show_progress_bar=False,
        )
        q_emb = model.encode(
            [query_prefix + post_texts[q] for q in queries],
            batch_size=128,
            normalize_embeddings=True,
            show_progress_bar=False,
        )
        row = {q: i for i, q in enumerate(queries)}
        rows = {
            seed: evaluate_scores(
                sub, lambda q, e=fc_emb, m=q_emb, r=row: e @ m[r[q]], queries, seed=seed
            )
            for seed in SEEDS
        }
        by_lang[lang] = rows[SEEDS[0]]
        out[spec] = {
            "queries": len(queries),
            "pool": len(fcs),
            "seconds": round(time.perf_counter() - start, 1),
            "runs": [summarise(rows[seed]) for seed in SEEDS],
        }
    if {"pol", "eng"} <= by_lang.keys():
        out["did_pol_vs_eng"] = did_interval(by_lang["pol"], by_lang["eng"])
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    out["peak_rss_mb"] = round(
        peak / (1 if sys.platform == "linux" else 1024) / 1024, 1
    )
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    args = sys.argv[1:]
    main(
        args[0],
        Path(args[1] if len(args) > 1 else "data/raw"),
        args[2:] or ["pol", "eng"],
    )
