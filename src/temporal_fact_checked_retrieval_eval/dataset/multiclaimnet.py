"""MultiClaimNet claim-to-cluster loader."""

import csv
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def load_multiclaimnet(*, path: Path) -> dict[str, str]:
    """Load the NID-to-cluster mapping from MultiClaimNet's ``MultiClaim.csv``.

    Args:
        path: CSV with columns ``Claim, ClusterID, Translation, Language, NID,
            Timstamp, URL`` (the timestamp column is misspelled ``Timstamp`` and
            often empty).

    Returns:
        A mapping from NID (fact-check id) to ClusterID for every row with a
        non-empty NID.
    """
    mapping: dict[str, str] = {}
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            nid = (row.get("NID") or "").strip()
            if not nid:
                continue
            mapping[nid] = row["ClusterID"]
    return mapping
