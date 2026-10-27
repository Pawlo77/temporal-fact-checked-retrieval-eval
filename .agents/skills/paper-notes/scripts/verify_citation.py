"""Check that each paper note cites a paper that exists, with matching metadata.

Usage: ``uv run python <this script> [NOTE ...]`` (default: every note under
``research/`` tagged ``type/paper``). Looks up ``doi`` on Crossref and ``arxiv`` on the
arXiv API, then compares the official title (first alias, else ``title``), the author
surnames and, for a DOI, the year. Prints ``OK`` or ``FAIL`` per note; exits 1 on any
missing record or mismatch. Needs network.
"""

import json
import os
import re
import sys
import tomllib
import unicodedata
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET  # nosec B405 - parses the arXiv API response only
from collections.abc import Callable
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[4]
"""Repository root, four levels above this script."""

ATOM = {"a": "http://www.w3.org/2005/Atom"}
PAPER_TAG = "type/paper"
"""Tag that marks a paper note; hubs and folder notes carry other ``type/`` tags."""

Lookup = Callable[[str], tuple[str, list[str], int]]


def user_agent(root: Path = ROOT) -> str:
    """Return the HTTP user agent: project name, plus ``LITERATURE_MAILTO`` if set."""
    name = root.name
    pyproject = root / "pyproject.toml"
    if pyproject.is_file():
        data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
        name = data.get("tool", {}).get("agent-kit", {}).get("name", name)
    mailto = os.environ.get("LITERATURE_MAILTO", "")
    return f"{name} citation check" + (f" (mailto:{mailto})" if mailto else "")


def fetch(url: str) -> bytes:
    """Return the body of ``url`` (one attempt, 60 s timeout)."""
    request = urllib.request.Request(url, headers={"User-Agent": user_agent()})
    with urllib.request.urlopen(request, timeout=60) as response:  # nosec B310
        return bytes(response.read())


def norm(text: str) -> str:
    """Fold accents and case; keep letters and digits separated by single spaces."""
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def surname(name: str) -> str:
    """Return the normalised last word of a person's name."""
    words = norm(name).split()
    return words[-1] if words else ""


def crossref(doi: str) -> tuple[str, list[str], int]:
    """Return title, author surnames and year of a DOI from Crossref."""
    url = f"https://api.crossref.org/works/{urllib.parse.quote(doi)}"
    message = json.loads(fetch(url))["message"]
    authors = [a.get("family", a.get("name", "")) for a in message.get("author", [])]
    year = message["issued"]["date-parts"][0][0]
    return message["title"][0], authors, int(year)


def arxiv(arxiv_id: str) -> tuple[str, list[str], int]:
    """Return title, author names and first-version year of an arXiv id."""
    url = f"https://export.arxiv.org/api/query?id_list={urllib.parse.quote(arxiv_id)}"
    root = ET.fromstring(fetch(url))  # nosec B314 - arXiv API response
    entry = root.find("a:entry", ATOM)
    title = entry.findtext("a:title", "", ATOM) if entry is not None else ""
    if entry is None or not title.strip():
        msg = f"arXiv has no record {arxiv_id}"
        raise LookupError(msg)
    names = [a.findtext("a:name", "", ATOM) for a in entry.findall("a:author", ATOM)]
    year = int(entry.findtext("a:published", "0000", ATOM)[:4])
    return " ".join(title.split()), names, year


SOURCES: dict[str, Lookup] = {"doi": crossref, "arxiv": arxiv}
"""Frontmatter key and the registry that resolves it."""


def frontmatter(path: Path) -> dict[str, Any]:
    """Return a note's YAML frontmatter, or an empty mapping when it has none."""
    parts = path.read_text(encoding="utf-8").split("---", 2)
    if len(parts) < 3 or parts[0].strip():
        return {}
    meta = yaml.safe_load(parts[1])
    return meta if isinstance(meta, dict) else {}


def _compare(key: str, ident: str, meta: dict[str, Any], found: tuple) -> list[str]:
    title, authors, year = found
    official = str((meta.get("aliases") or [meta.get("title", "")])[0])
    mine = sorted(surname(str(a)) for a in meta.get("authors") or [])
    problems = []
    if norm(title) != norm(official):
        problems.append(f"{key} {ident}: title {title!r} != {official!r}")
    if sorted(surname(a) for a in authors) != mine:
        problems.append(f"{key} {ident}: authors {authors} != {meta.get('authors')}")
    if key == "doi" and year != meta.get("year"):
        problems.append(f"{key} {ident}: year {year} != {meta.get('year')}")
    return problems


def check(path: Path) -> list[str]:
    """Return the problems with one note's citation (empty when it checks out)."""
    meta = frontmatter(path)
    if not any(meta.get(key) for key in SOURCES):
        return ["no doi or arxiv id"]
    problems: list[str] = []
    for key, lookup in SOURCES.items():
        ident = str(meta.get(key) or "")
        if not ident or ident.lower().startswith("10.48550/"):
            continue  # arXiv DOIs are checked through the arxiv id
        try:
            found = lookup(ident)
        except (OSError, LookupError, ValueError, KeyError, ET.ParseError) as exc:
            problems.append(f"{key} {ident}: lookup failed ({exc})")
            continue
        problems += _compare(key, ident, meta, found)
    return problems


def paper_notes(research: Path) -> list[Path]:
    """Return the notes under ``research`` tagged ``type/paper``."""
    return [
        path
        for path in sorted(research.rglob("*.md"))
        if PAPER_TAG in (frontmatter(path).get("tags") or [])
    ]


def main(argv: list[str] | None = None) -> int:
    """Check the given notes (default: all paper notes); print one line per note."""
    args = sys.argv[1:] if argv is None else argv
    notes = [Path(a) for a in args] or paper_notes(ROOT / "research")
    failed = 0
    for note in notes:
        problems = check(note)
        failed += bool(problems)
        print(f"{'FAIL' if problems else 'OK'} {note.name}")
        for problem in problems:
            print(f"  - {problem}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
