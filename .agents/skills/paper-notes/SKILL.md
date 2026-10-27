---
name: paper-notes
description: >-
  Use when adding, summarizing or updating a literature note in research/, citing a
  paper from the vault, or finding a few papers on a topic for the project.
---

# Paper notes

One note per paper at `research/<Area>/[<Theme>/]<Short title>.md`, hub `research/Research.md`;
every folder has a note named after it that lists its papers. No PDFs are kept. The
project's half of this skill is [reference.md](reference.md) (layout and placement,
section contracts, tags, glossary, notation); every note starts from [template.md](template.md). No `research/`
here: the project enables it with `copier update --data vault=true --data research=true`.

## 1. Verify the paper exists (gate)

- Find the record yourself: arXiv API (`https://export.arxiv.org/api/query?id_list=<id>`),
  Crossref (`https://api.crossref.org/works/<doi>`), the proceedings page, Semantic
  Scholar for the published venue. Never cite from memory.
- Prefer the published version: its title, author order, venue with volume and pages, DOI.
- Fill the frontmatter, then run the checker; continue only on `OK`:
  ```bash
  uv run python .agents/skills/paper-notes/scripts/verify_citation.py "research/<Area>/<Short title>.md"
  ```
- Every prior work linked in Motivation is checked the same way; unverifiable ones are not
  linked.
- Finding candidates for the user: agent `paper-scout`, then a table of citation,
  verified URL, one-line relevance and theme; the user picks. A whole area: skill
  `literature-search`.

## 2. Place

Pick the area and theme from the placement table in [reference.md](reference.md). None
fits: propose one to the user, then add its row and tag slug there, create the folder with
its folder note and add it to the parent's table (`Research.md` for an area).

## 3. Read

Read from the URL: arXiv HTML (`https://arxiv.org/html/<id>`) first. Otherwise download
the PDF to a temp dir, extract it and delete it; never save a PDF in the repository:

```bash
d=$(mktemp -d) && curl -sL "<pdf url>" -o "$d/p.pdf" && uv run --with pypdf python -c "import sys; from pypdf import PdfReader; [print(f'=== p{i}', p.extract_text() or '') for i, p in enumerate(PdfReader(sys.argv[1]).pages, 1)]" "$d/p.pdf" > "$d/p.txt"; rm "$d/p.pdf"
```

A paper without readable full text is recorded as unread, never written from the abstract.

## 4. Write

1. Fill every section of the template in order, following the contracts, glossary and
   notation in [reference.md](reference.md).
2. Write for human readers: no tooling, plans or config keys in the note; project usage
   goes to `Relation to our project`, tooling to `research/AGENTS.md`.
3. Future work: the paper's own directions, then its main gaps; search citations and arXiv
   for each and mark it `Done`, `Partly done` (link the verified later paper) or
   `Open (searched YYYY-MM)`.
4. Re-read the source for every number, dataset and claim you wrote; delete what you
   cannot find. Then fill `Verification` with today's date.
5. Read the note once as a newcomer: each idea once, no section repeating another.

## 5. Link

- Add the paper to the table of its folder note (an unlinked note fails `vault-check`).
- Link related vault notes from Motivation or Relation to our project, not a "See also".

## 6. Check

```bash
uv run python .agents/skills/paper-notes/scripts/verify_citation.py
make vault-check
```

Report the note, its theme and anything left out as unverifiable.
