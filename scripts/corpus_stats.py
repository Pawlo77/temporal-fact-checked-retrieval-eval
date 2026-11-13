"""Print Table 2 statistics (counts, balance, order, answerability) as JSON.

Usage: uv run python scripts/corpus_stats.py [data/raw]
Reads MultiClaim v1/v2 and the SemEval-2025 Task 7 monolingual test set from the
gitignored raw tree; prints counts only, no text. v1 has no post language column,
so its pl/en slices are empty; use the paper counts.
"""

import json
import sys
from pathlib import Path

from temporal_fact_checked_retrieval_eval.dataset import DatedCorpus
from temporal_fact_checked_retrieval_eval.dataset.multiclaim import load_multiclaim
from temporal_fact_checked_retrieval_eval.dataset.semeval import load_semeval
from temporal_fact_checked_retrieval_eval.stats import corpus_summary

VERSIONS = {
    "v1": ("multiclaim_v1", "fact_check_post_mapping (1).csv"),
    "v2": ("multiclaim_v2", "fact_check_post_mapping.csv"),
}


def _semeval_test(root: Path) -> dict[str, dict[str, float]]:
    """Summarise the SemEval monolingual test set, whole and per language pool."""
    test = root / "semeval2025_task7" / "test_set"
    corpus = load_semeval(
        fact_checks_csv=test / "fact_checks.csv",
        posts_csv=test / "posts.csv",
        reference_jsons=(test / "monolingual_reference.json",),
    )
    tasks = json.loads((test / "tasks.json").read_text(encoding="utf-8"))["monolingual"]
    out = {"all": corpus_summary(corpus)}
    for lang in ("pol", "eng"):
        posts = {str(i) for i in tasks[lang]["posts_test"]}
        fcs = {str(i) for i in tasks[lang]["fact_checks"]}
        sub = DatedCorpus(
            posts={k: v for k, v in corpus.posts.items() if k in posts},
            fact_checks={k: v for k, v in corpus.fact_checks.items() if k in fcs},
            pairs=tuple(p for p in corpus.pairs if p.post_id in posts),
        )
        out[lang] = corpus_summary(sub)
    return out


def main(root: Path) -> None:
    """Print the summary of each version, overall and for Polish and English."""
    out = {}
    for name, (folder, mapping) in VERSIONS.items():
        corpus = load_multiclaim(
            fact_checks_csv=root / folder / "fact_checks.csv",
            posts_csv=root / folder / "posts.csv",
            mapping_csv=root / folder / mapping,
        )
        out[name] = {
            lang or "all": corpus_summary(corpus, language=lang)
            for lang in (None, "pol", "eng")
        }
    out["semeval_test"] = _semeval_test(root)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main(Path(sys.argv[1] if len(sys.argv) > 1 else "data/raw"))
