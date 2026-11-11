"""Print Table 2 statistics (counts, balance, order, answerability) as JSON.

Usage: uv run python scripts/corpus_stats.py [data/raw]
Reads MultiClaim v1/v2 from the gitignored raw tree; prints counts only, no text.
v1 has no post language column, so its pl/en slices are empty; use the paper counts.
"""

import json
import sys
from pathlib import Path

from temporal_fact_checked_retrieval_eval.dataset.multiclaim import load_multiclaim
from temporal_fact_checked_retrieval_eval.stats import corpus_summary

VERSIONS = {
    "v1": ("multiclaim_v1", "fact_check_post_mapping (1).csv"),
    "v2": ("multiclaim_v2", "fact_check_post_mapping.csv"),
}


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
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main(Path(sys.argv[1] if len(sys.argv) > 1 else "data/raw"))
