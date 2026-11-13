"""Tests for the MultiClaimNet claim-to-cluster loader."""

import csv
import io
from pathlib import Path

from temporal_fact_checked_retrieval_eval.dataset.multiclaimnet import (
    load_multiclaimnet,
)


def _write_csv(path: Path, header: list[str], rows: list[list[str]]) -> None:
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(header)
    writer.writerows(rows)
    path.write_text(buffer.getvalue(), encoding="utf-8")


def test_load_multiclaimnet_maps_nid_to_cluster(tmp_path: Path) -> None:
    _write_csv(
        tmp_path / "MultiClaim.csv",
        ["Claim", "ClusterID", "Translation", "Language", "NID", "Timstamp", "URL"],
        [
            ["claim a", "0", "", "en", "164477", "", ""],
            ["claim b", "0", "", "pl", "164478", "1627369680.0", "https://x/"],
            ["claim c", "1", "", "", "", "1641427140.0", "https://y/"],
            ["claim d", "1", "", "en", "68301", "", ""],
        ],
    )

    mapping = load_multiclaimnet(path=tmp_path / "MultiClaim.csv")

    assert mapping == {
        "164477": "0",
        "164478": "0",
        "68301": "1",
    }
