# Paper notes: writing standard

This project's half of skill `paper-notes`; edit it freely. Every note has the same
sections, words and symbols.

## Layout

```text
research/
  Research.md                  hub: the question and a table of areas
  AGENTS.md                    agent context (tooling, project use)
  protocols/<domain>.yaml      literature-search protocols and outcomes
  <Area>/
    <Area>.md                  folder note: table of its themes or papers
    <Short title>.md           paper note, citekey in frontmatter
    <Theme>/
      <Theme>.md               folder note of the theme
      <Short title>.md
```

File names are the paper's short name (method or system name), never `Year - Author - Title`.

## Placement

| Paper changes | Folder | Tag |
|---------------|--------|-----|
| (what a paper must change to belong here) | `research/<Area>/[<Theme>/]` | `theme/<slug>` |

## Sections (exact order, no others)

| Section | Contract |
|---------|----------|
| `> [!info] TL;DR` | What the paper changes and the result, 2–4 plain sentences |
| `## Motivation` | The gap before the paper, 3–5 bullets; prior work linked (vault note or verified URL) |
| `## Method` | Notation sentence, definitions, the method; an `Intuition:` sentence next to each key equation |
| `## Key numbers` | 2–5 headline results, each with its setting and baseline |
| `## Experiments` | One bullet per experiment: `**Name:** what was tested; what was found` |
| `## Data` | One bullet per dataset: name, what it is, size |
| `> [!failure] Limitations` | One bullet per failure mode |
| `## Relation to our project` | What we take, test or avoid; links to project notes |
| `## Future work` | Bullets led by `**Done:**` or `**Partly done:**` (with a verified link) or `**Open:**` ending `(searched YYYY-MM)` |
| `## Verification` | Sources checked and `Verified on YYYY-MM-DD` |

Whole note: 500–1500 words.

## Never

- References to figures, tables or equation numbers: state the finding.
- Copied result tables; abstract paraphrase; "this paper proposes"; TODOs.
- Facts not in the paper or a verified source; citations from memory.
- The same point in two sections.

## Glossary

| Use | Not | Meaning |
|-----|-----|---------|
| (term) | (synonyms to avoid) | (meaning) |

## Notation

(The project's symbols. Rename a paper's symbols to these and say so once.)

## Tags (vocabulary)

Paper notes carry `type/paper`, one `theme/` and one or more `topic/`:

- `theme/`: (one slug per row of Placement).
- `topic/`: (add values here before using them).

Other notes: `type/hub`, `type/theme`.

## Citation fields

`title` (short name = filename = heading), `aliases` (official title first), `authors`
(full names, published order), `year`, `venue` (with volume and pages), `arxiv` and/or
`doi`, `url` (published version, else arXiv), `citekey`
(`<firstauthor><year><firstword>`), `theme`, `tags`. `scripts/verify_citation.py` must
print `OK` for the note.
