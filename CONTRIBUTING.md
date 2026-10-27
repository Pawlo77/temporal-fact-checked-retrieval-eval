# Contributing to temporal-fact-checked-retrieval-eval

## Security

Report a vulnerability through GitHub's private reporting or by email to the maintainer.
Never commit secrets, tokens or personal data.

## What to contribute

- **Bug reports and fixes**, ideally with the smallest input that reproduces the problem.
- **Features**: open an issue first to agree on scope and design.
- **Documentation and tests.**

## Development setup

Prerequisites: Python 3.12 and [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/Pawlo77/temporal-fact-checked-retrieval-eval.git
cd temporal-fact-checked-retrieval-eval
make install
```

`make install` syncs the dependencies into `.venv` and installs the [prek](https://github.com/j178/prek)
hooks once, from the main checkout: the hooks are shared by all git worktrees and call the main
checkout's `.venv`. Change dependencies with `uv add` and `uv lock`, never `pip install`.


## Obsidian vault setup

Obsidian rewrites its settings on every open, so the live files under `.obsidian/` are not committed. The committed `*.example.json` files hold the community plugin list and the default settings. On a fresh clone, copy them once (existing files are kept):

```bash
find .obsidian -name '*.example.json' -exec sh -c 'cp -n "$1" "${1%.example.json}.json"' _ {} \;
```

Then open the folder as a vault and run `make obsidian-plugins`. To share a setting with the team, edit its `.example.json` by hand; never commit a live `.json` file.


## Quality gates

| Command | When |
|---------|------|
| `make check` | Always, before a pull request: pytest, all prek hooks and `make vault-check`. CI runs the same checks. |
| `make vault-check` | After editing notes under `knowledge/` or `plans/`: properties, links and brevity budgets. |

Write the test first for new behaviour and bug fixes.

## Project rules

- **Brevity:** one home per fact, link instead of restating; file budgets are enforced by `scripts/check_brevity.py`.
- **Generated files:** never edit `.claude/rules/`, `.codex/agents/` or `knowledge/generated/`; change the source and rerun `scripts/sync_rules.py`, `scripts/sync_agents.py` or `make knowledge`.
- **Template files:** files that come from [python-kit-template](https://github.com/Pawlo77/python-kit-template) change there, not here.

## Branches, commits and pull requests

- Branch from `main` with a type prefix (`feat/`, `fix/`, `docs/`, `test/`, `refactor/`, `chore/`, `ci/`, `perf/`); `main` is protected.
- Commit subjects are `type: summary` (`feat`, `fix`, `docs`, `test`, `refactor`, `chore`, `ci`, `build`, `perf`): imperative, no trailing period, at most 72 characters, one concern per commit. A `commit-msg` hook enforces it; never bypass hooks with `--no-verify` or force-push shared branches.
- The PR title uses the same format (workflow `pr-title`). Fill in the pull request template; open it ready for review (no draft or WIP) and keep it focused.
- The `assign-author.yaml` workflow assigns the author and labels the PR from the title type (`fix` is `bug`, `docs` is `documentation`, the rest `enhancement`).
- Required checks: `prek`, `tests-passed`, `title`; CodeQL also runs on every PR. Resolve every review thread before asking for a merge. The maintainer merges with a merge commit.

## AI-assisted contributions

AI tools are welcome. The contributor is responsible for the change: a human reviews every AI-written change, runs the quality gates and can explain the diff. Instructions for coding agents live in `AGENTS.md`.

## Questions

Open a GitHub [issue](https://github.com/Pawlo77/temporal-fact-checked-retrieval-eval/issues) for usage questions, ideas and bugs.
