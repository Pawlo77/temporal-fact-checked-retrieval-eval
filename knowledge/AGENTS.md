# Knowledge agents

The repository root is the Obsidian vault `temporal-fact-checked-retrieval-eval` (map: `temporal-fact-checked-retrieval-eval.md`); notes live in
`knowledge/`, plus `plans/` and `.remember/*.md`. Create notes from `knowledge/_templates/`
(Templater); vault machinery: skill `obsidian`. `make vault-check` passes before hand-off.

## Where things live

| Path | Contents |
|---|---|
| `temporal-fact-checked-retrieval-eval.md`, `Dashboard.md` | map of the vault; Dataview tables |
| `architecture/` | one module note per package of `src/temporal_fact_checked_retrieval_eval`; a change under `src/temporal_fact_checked_retrieval_eval/<pkg>/` updates it (bump `updated`) in the same change |
| `decisions/` | one log per domain, `<Domain> decisions.md`: a dated section per design choice, newest first |
| `issues/` | one note per open bug, `<id> - <title>.md`; fixed bugs become rows of `Fixed issues.md` |
| `concepts/` | one note per term |
| `handbook/` | how-to notes for people; `Solutions/<date> - <title>.md` for solved problems |
| `generated/`, `_templates/` | rebuilt by `make knowledge`, never edited; Templater templates, not notes |

## Frontmatter

- `title`, `type` (`map`, `dashboard`, `module`, `decision-log`, `issue`, `concept`, `handbook`, `solution`, `plan`, `generated`), `domain` (a package or `index`, `vault`), `parent` (the wikilink of the note one level up, `"[[temporal-fact-checked-retrieval-eval]]"`; none on the map), `tags` (a YAML list without `#`), `created` (`YYYY-MM-DD`), `updated` when the content changes.
- `status`: required on issues (`open`, `fixed`, `wontfix`, `deferred`) and plans (`draft`, `ready`, `in progress`, `done`, `superseded`).
- `related`: wikilinks to related notes (no "Related" sections in bodies). `related-code`: wikilinks to code by vault path with extension, for example `"[[src/temporal_fact_checked_retrieval_eval/core.py]]"`. `aliases`: other names.
- These rules are the schema in `[tool.agent-kit.vault.schema]` of `pyproject.toml`; `scripts/check_vault.py` enforces it.

## Writing rules

- Link notes by file name without `.md` (`[[Run archive]]`), code and other files by vault path with extension; the parent is metadata, never a "Part of" sentence.
- One idea per bullet; content only, no narration of what the note is about.
- Numbers come from executed output, never from memory.
- No secrets, tokens, private hostnames or personal data beyond the maintainer's public identity; a prek hook rejects them.
- A design choice appends a section to its log; a bug found or fixed adds or updates its issue note.
