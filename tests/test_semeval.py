"""Tests for the SemEval-2025 Task 7 loader."""

import csv
import io
import json
from datetime import datetime
from pathlib import Path

from temporal_fact_checked_retrieval_eval.dataset import GoldPair
from temporal_fact_checked_retrieval_eval.dataset.semeval import load_semeval


def _write_csv(path: Path, header: list[str], rows: list[list[str]]) -> None:
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(header)
    writer.writerows(rows)
    path.write_text(buffer.getvalue(), encoding="utf-8")


def _write_reference(path: Path, qrels: dict[str, list[str | int]]) -> None:
    path.write_text(json.dumps(qrels), encoding="utf-8")


def test_load_semeval_merges_references_and_drops_undated(tmp_path: Path) -> None:
    _write_csv(
        tmp_path / "fact_checks.csv",
        ["fact_check_id", "claim", "instances", "title"],
        [
            ["fc_a", "claim a", repr([(1686787200.0, "https://x/a")]), "title a"],
            ["fc_b", "claim b", repr([(1704067200.0, "https://x/b")]), "title b"],
        ],
    )
    _write_csv(
        tmp_path / "posts.csv",
        ["post_id", "instances", "ocr", "verdicts", "text"],
        [
            ["post_1", repr([(1704067200.0, "fb")]), "", "", "hello"],
            ["post_2", repr([]), "", "", "undated"],
            ["post_3", repr([(1686787200.0, "fb")]), "", "", "world"],
        ],
    )
    _write_reference(
        tmp_path / "mono.json",
        {"post_1": ["fc_a"], "post_2": ["fc_b"], "post_3": ["fc_a"]},
    )
    _write_reference(
        tmp_path / "cross.json",
        {"post_1": ["fc_b"], "post_3": [9999]},
    )

    corpus = load_semeval(
        fact_checks_csv=tmp_path / "fact_checks.csv",
        posts_csv=tmp_path / "posts.csv",
        reference_jsons=(tmp_path / "mono.json", tmp_path / "cross.json"),
    )

    assert set(corpus.posts) == {"post_1", "post_3"}
    assert set(corpus.fact_checks) == {"fc_a", "fc_b"}
    assert corpus.fact_checks["fc_a"].language is None
    assert corpus.posts["post_1"].instances == (datetime(2024, 1, 1),)

    assert corpus.pairs == (
        GoldPair("post_1", "fc_a", None),
        GoldPair("post_3", "fc_a", None),
        GoldPair("post_1", "fc_b", None),
        GoldPair("post_3", "9999", None),
    )


def test_load_semeval_parses_string_and_nan_timestamps(tmp_path: Path) -> None:
    _write_csv(
        tmp_path / "fact_checks.csv",
        ["fact_check_id", "claim", "instances", "title"],
        [
            [
                "fc_s",
                "claim",
                repr([("2022-10-25 02:00:00+02", "https://x"), ("nan", "https://y")]),
                "title",
            ]
        ],
    )
    _write_csv(
        tmp_path / "posts.csv",
        ["post_id", "instances", "ocr", "verdicts", "text"],
        [
            [
                "post_1",
                repr([("2023-02-23 12:00:13.851+01", "fb")]),
                "",
                "",
                "hi",
            ]
        ],
    )
    _write_reference(tmp_path / "mono.json", {"post_1": ["fc_s"]})

    corpus = load_semeval(
        fact_checks_csv=tmp_path / "fact_checks.csv",
        posts_csv=tmp_path / "posts.csv",
        reference_jsons=(tmp_path / "mono.json",),
    )

    assert corpus.fact_checks["fc_s"].instances == (datetime(2022, 10, 25),)
    assert corpus.posts["post_1"].instances == (
        datetime(2023, 2, 23, 11, 0, 13, 851000),
    )
