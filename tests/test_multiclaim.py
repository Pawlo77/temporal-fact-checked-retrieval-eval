"""Tests for the MultiClaim CSV loader."""

import csv
import io
from datetime import datetime
from pathlib import Path

from temporal_fact_checked_retrieval_eval.dataset import GoldPair
from temporal_fact_checked_retrieval_eval.dataset.multiclaim import load_multiclaim


def _write_csv(path: Path, header: list[str], rows: list[list[str]]) -> None:
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(header)
    writer.writerows(rows)
    path.write_text(buffer.getvalue(), encoding="utf-8")


def test_load_multiclaim_drops_undated_post(tmp_path: Path) -> None:
    _write_csv(
        tmp_path / "fact_checks.csv",
        ["fact_check_id", "claim", "title", "instances", "claim_detected_language_iso"],
        [
            [
                "fc_a",
                "claim a",
                "title a",
                repr([(1686787200.0, "https://x/a")]),
                "en",
            ],
            [
                "fc_b",
                "claim b",
                "title b",
                repr([(1704067200.0, "https://x/b")]),
                "pl",
            ],
        ],
    )
    _write_csv(
        tmp_path / "posts.csv",
        ["post_id", "post_body", "post_detected_language_iso", "instances"],
        [
            ["post_1", "hello", "en", repr([(1704067200.0, "fb")])],
            ["post_2", "undated", "pl", repr([])],
            ["post_3", "world", "pl", repr([(1686787200.0, "fb")])],
        ],
    )
    _write_csv(
        tmp_path / "fact_check_post_mapping.csv",
        ["fact_check_id", "post_id", "relationship"],
        [
            ["fc_a", "post_1", "claimreview_schema"],
            ["fc_b", "post_2", "claimreview_schema"],
            ["fc_b", "post_3", ""],
        ],
    )

    corpus = load_multiclaim(
        fact_checks_csv=tmp_path / "fact_checks.csv",
        posts_csv=tmp_path / "posts.csv",
        mapping_csv=tmp_path / "fact_check_post_mapping.csv",
    )

    assert set(corpus.posts) == {"post_1", "post_3"}
    assert "post_2" not in corpus.posts
    assert set(corpus.fact_checks) == {"fc_a", "fc_b"}

    assert corpus.posts["post_1"].instances == (datetime(2024, 1, 1),)
    assert corpus.posts["post_1"].language == "en"
    assert corpus.posts["post_3"].instances == (datetime(2023, 6, 15),)
    assert corpus.posts["post_3"].language == "pl"

    assert corpus.fact_checks["fc_a"].instances == (datetime(2023, 6, 15),)
    assert corpus.fact_checks["fc_a"].language == "en"
    assert corpus.fact_checks["fc_b"].instances == (datetime(2024, 1, 1),)
    assert corpus.fact_checks["fc_b"].language == "pl"

    assert corpus.pairs == (
        GoldPair("post_1", "fc_a", "claimreview_schema"),
        GoldPair("post_3", "fc_b", None),
    )
