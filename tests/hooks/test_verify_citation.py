"""Skill paper-notes: the citation checker compares notes with Crossref and arXiv.

No network: ``fetch`` is replaced by canned responses.

@see [[.agents/skills/paper-notes/scripts/verify_citation.py]]
"""

import importlib.util
import json
from pathlib import Path
from types import ModuleType

import pytest

from tests.hooks._hookrun import ROOT

SCRIPT = ROOT / ".agents" / "skills" / "paper-notes" / "scripts" / "verify_citation.py"

CROSSREF = {
    "message": {
        "title": ["Attention Is All You Need"],
        "author": [{"family": "Vaswani"}, {"family": "Shazeer"}],
        "issued": {"date-parts": [[2017]]},
    }
}
ARXIV = """<feed xmlns="http://www.w3.org/2005/Atom"><entry>
<title>Attention Is All
  You Need</title><published>2017-06-12T00:00:00Z</published>
<author><name>Ashish Vaswani</name></author><author><name>Noam Shazeer</name></author>
</entry></feed>"""
EMPTY_FEED = '<feed xmlns="http://www.w3.org/2005/Atom"></feed>'

NOTE = """---
title: "Transformer"
aliases: ["Attention Is All You Need"]
authors: ["Ashish Vaswani", "Noam Shazeer"]
year: {year}
{ids}
tags: [type/paper, theme/models]
---
# Transformer
"""


@pytest.fixture
def module(monkeypatch: pytest.MonkeyPatch) -> ModuleType:
    """Load the checker with ``fetch`` answering from canned records."""
    spec = importlib.util.spec_from_file_location("verify_citation_under_test", SCRIPT)
    assert spec is not None
    assert spec.loader is not None
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    responses = {"crossref": json.dumps(CROSSREF).encode(), "arxiv": ARXIV.encode()}

    def fake_fetch(url: str) -> bytes:
        if "id_list=0000.00000" in url:
            return EMPTY_FEED.encode()
        if "error" in url:
            raise OSError("offline")
        return responses["crossref" if "crossref" in url else "arxiv"]

    monkeypatch.setattr(loaded, "fetch", fake_fetch)
    return loaded


def _note(tmp_path: Path, ids: str, year: int = 2017, name: str = "T.md") -> Path:
    path = tmp_path / "research" / "Models" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(NOTE.format(year=year, ids=ids), encoding="utf-8")
    return path


def test_matching_doi_and_arxiv_pass(module: ModuleType, tmp_path: Path) -> None:
    note = _note(tmp_path, 'doi: "10.5555/1"\narxiv: "1706.03762"')
    assert module.check(note) == []


def test_wrong_year_is_reported(module: ModuleType, tmp_path: Path) -> None:
    problems = module.check(_note(tmp_path, 'doi: "10.5555/1"', year=2018))
    assert len(problems) == 1
    assert "year 2017 != 2018" in problems[0]


def test_title_and_author_mismatch(module: ModuleType, tmp_path: Path) -> None:
    note = _note(tmp_path, 'arxiv: "1706.03762"')
    note.write_text(
        note
        .read_text(encoding="utf-8")
        .replace("Attention Is All You Need", "Other")
        .replace("Noam Shazeer", "Someone Else"),
        encoding="utf-8",
    )
    problems = module.check(note)
    assert any("title" in p for p in problems)
    assert any("authors" in p for p in problems)


def test_missing_record_and_ids(module: ModuleType, tmp_path: Path) -> None:
    assert module.check(_note(tmp_path, "")) == ["no doi or arxiv id"]
    missing = module.check(_note(tmp_path, 'arxiv: "0000.00000"'))
    assert "lookup failed" in missing[0]
    assert "lookup failed" in module.check(_note(tmp_path, 'doi: "10.1/error"'))[0]


def test_arxiv_doi_is_skipped(module: ModuleType, tmp_path: Path) -> None:
    note = _note(tmp_path, 'doi: "10.48550/arXiv.1706.03762"\narxiv: "1706.03762"')
    assert module.check(note) == []


def test_main_checks_paper_notes_only(
    module: ModuleType, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    _note(tmp_path, 'arxiv: "1706.03762"')
    hub = tmp_path / "research" / "Research.md"
    hub.write_text("---\ntitle: Research\ntags: [type/hub]\n---\n", encoding="utf-8")
    module.ROOT = tmp_path
    assert module.paper_notes(tmp_path / "research") == [
        tmp_path / "research" / "Models" / "T.md"
    ]
    assert module.main([]) == 0
    assert capsys.readouterr().out == "OK T.md\n"
    bad = _note(tmp_path, "", name="Bad.md")
    assert module.main([str(bad)]) == 1


def test_user_agent_names_project(
    module: ModuleType, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    (tmp_path / "pyproject.toml").write_text(
        '[tool.agent-kit]\nname = "demo"\n', encoding="utf-8"
    )
    monkeypatch.delenv("LITERATURE_MAILTO", raising=False)
    assert module.user_agent(tmp_path) == "demo citation check"
    monkeypatch.setenv("LITERATURE_MAILTO", "me@example.com")
    assert module.user_agent(tmp_path).endswith("(mailto:me@example.com)")
