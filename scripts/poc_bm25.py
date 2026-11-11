"""Run the BM25 proof of concept on MultiClaim v2; print JSON (scores only).

Usage: uv run python scripts/poc_bm25.py [data/raw] [language[:n] ...]
Monolingual slices (default pol eng); ``eng:3000`` samples 3000 queries. The query
set is the dated posts with a gold fact-check, scored under the random,
size-matched and causal pools. Reports wall time and peak memory too. Post text
is read locally and never printed.
"""

import csv
import json
import platform
import resource
import sys
import time
from pathlib import Path

import numpy as np

from temporal_fact_checked_retrieval_eval.dataset import DatedCorpus
from temporal_fact_checked_retrieval_eval.dataset.multiclaim import load_multiclaim
from temporal_fact_checked_retrieval_eval.poc import evaluate, summarise

SEEDS = (0, 1, 2)


def _texts(path: Path, key: str, columns: tuple[str, ...]) -> dict[str, str]:
    """Map an id column to the joined text of ``columns``."""
    csv.field_size_limit(sys.maxsize)
    with path.open(newline="", encoding="utf-8") as handle:
        return {
            row[key]: " ".join(row[c] for c in columns)
            for row in csv.DictReader(handle)
        }


def main(root: Path, languages: list[str]) -> None:
    """Print the summary of each language, one run per size-matched seed."""
    folder = root / "multiclaim_v2"
    corpus = load_multiclaim(
        fact_checks_csv=folder / "fact_checks.csv",
        posts_csv=folder / "posts.csv",
        mapping_csv=folder / "fact_check_post_mapping.csv",
    )
    fc_texts = _texts(folder / "fact_checks.csv", "fact_check_id", ("claim", "title"))
    post_texts = _texts(folder / "posts.csv", "post_id", ("post_body",))
    out: dict = {"hardware": platform.platform(), "bm25": "bm25s default, \\w+ tokens"}
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
            pick = np.random.default_rng(0).choice(
                len(queries), int(size), replace=False
            )
            queries = [queries[i] for i in sorted(pick)]
        start = time.perf_counter()
        runs = [
            summarise(evaluate(sub, fc_texts, post_texts, queries, seed=s))
            for s in SEEDS
        ]
        out[spec] = {
            "queries": len(queries),
            "pool": len(fcs),
            "seconds": round(time.perf_counter() - start, 1),
            "runs": runs,
        }
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    out["peak_rss_mb"] = round(
        peak / (1 if sys.platform == "linux" else 1024) / 1024, 1
    )
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main(
        Path(sys.argv[1] if len(sys.argv) > 1 else "data/raw"),
        sys.argv[2:] or ["pol", "eng"],
    )
