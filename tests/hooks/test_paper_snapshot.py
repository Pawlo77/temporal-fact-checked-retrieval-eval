"""Skill paper-notes: full-text snapshots mirror research/ under fulltext/.

No network: ``fetch`` is replaced by canned responses.

@see [[.agents/skills/paper-notes/scripts/snapshot.py]]
"""

import importlib.util
from pathlib import Path
from types import ModuleType

import pytest

from tests.hooks._hookrun import ROOT

SCRIPT = ROOT / ".agents" / "skills" / "paper-notes" / "scripts" / "snapshot.py"

NOTE = """---
title: "Transformer"
arxiv: "1706.03762"
url: "https://example.org/transformer"
tags: [type/paper, theme/models]
---
# Transformer
"""

PAGE = "<html><body><script>x()</script>" + "<p>word</p>" * 2000 + "</body></html>"


@pytest.fixture
def snap(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> ModuleType:
    """Load the script with research/ and fulltext/ under a temporary root."""
    spec = importlib.util.spec_from_file_location("paper_snapshot", SCRIPT)
    assert spec
    assert spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    monkeypatch.setattr(module, "ROOT", tmp_path)
    monkeypatch.setattr(module, "RESEARCH", tmp_path / "research")
    monkeypatch.setattr(module, "FULLTEXT", tmp_path / "fulltext")
    return module


def write_note(root: Path, rel: str) -> Path:
    """Create a paper note at ``research/<rel>``."""
    path = root / "research" / rel
    path.parent.mkdir(parents=True)
    path.write_text(NOTE, encoding="utf-8")
    return path


def test_snapshot_mirrors_note_path_and_falls_back_to_url(
    snap: ModuleType, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A failed arXiv download falls back to the HTML url at the mirror path."""
    note = write_note(tmp_path, "Models/Attention/Transformer.md")

    def fake(url: str) -> tuple[bytes, str]:
        if "arxiv" in url:
            raise OSError("down")
        return PAGE.encode(), "text/html"

    monkeypatch.setattr(snap, "fetch", fake)
    assert snap.snapshot(note, None, False).startswith("wrote")
    out = tmp_path / "fulltext" / "Models" / "Attention" / "Transformer.txt"
    text = out.read_text(encoding="utf-8")
    assert "# source: https://example.org/transformer" in text
    assert "x()" not in text
    assert snap.snapshot(note, None, False).startswith("exists")


def test_short_text_is_rejected(
    snap: ModuleType, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """An abstract-only page is not a full text."""
    note = write_note(tmp_path, "Models/Transformer.md")
    monkeypatch.setattr(snap, "fetch", lambda url: (b"<p>abstract</p>", "text/html"))
    assert snap.snapshot(note, None, False).startswith("FAIL")


def test_sync_moves_snapshot_after_note_moves(snap: ModuleType, tmp_path: Path) -> None:
    """A note moved to another theme takes its snapshot along."""
    write_note(tmp_path, "New theme/Transformer.md")
    old = tmp_path / "fulltext" / "Old theme" / "Transformer.txt"
    old.parent.mkdir(parents=True)
    old.write_text("text", encoding="utf-8")
    snap.sync()
    assert not old.exists()
    assert (tmp_path / "fulltext" / "New theme" / "Transformer.txt").exists()
