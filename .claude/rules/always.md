<!-- Generated from .cursor/rules/brevity.mdc by scripts/sync_rules.py; do not edit. -->

# Brevity

Every line is read again by people and agents. Write the fewest lines that keep the meaning.

- Code: comments say why, never restate the next line. One-line docstrings; add `Args`/`Returns` only for a parameter that name and type do not explain. Functions ≤ 50 statements; module docstring ≤ 12 lines.
- Reuse before writing: a block that appears twice becomes a helper or a fixture.
- One home per fact. Link (`[[note]]`, path) instead of restating it in another file.
- Reference material as tables or lists, not paragraphs. No "Overview", "Introduction" or "Summary" sections. No sentence over 35 words.
- Delete obsolete code and text; do not deprecate, archive or keep it "for history" (git has it).
- Budgets (`scripts/check_brevity.py`, run by `make vault-check`; `--list` prints them all): root AGENTS.md ≤ 500 words and 80 lines; README ≤ 900 words; skill ≤ 100 lines and 500 words; rule ≤ 60 lines and 400 words; agent ≤ 40 lines; command ≤ 15 lines. This repository's own: `brevity-local.mdc`.
- A file at or over budget must not grow: cut or split before adding. Files already over budget when the rule came in are capped at that size (`existing` in `[tool.agent-kit.brevity]`).
- Reports and PR bodies: findings first; no recap of the task or of code you only read.

<!-- Generated from .cursor/rules/experiment-boundaries.mdc by scripts/sync_rules.py; do not edit. -->

# Experiment boundaries

- Runnable code in `src/temporal_fact_checked_retrieval_eval/` — notebooks in `notebooks/`, paper in `report/`, configs in `configs/`
- YAML experiment configs in `configs/`; load via `load_experiment_config` in `config.py`
- Add modules only with real implementation, never empty package trees
- Heavy optional dependencies → `[project.optional-dependencies]` extras when introduced
- MLflow artifacts (`mlruns/`, `mlruns.db`) stay gitignored — log via tracking helpers only

<!-- Generated from .cursor/rules/git-commits.mdc by scripts/sync_rules.py; do not edit. -->

# Git commits and pull requests

- Commits, pushes and PRs happen inside skill `ship` (it classifies the branch and merges routine changes itself); outside it, never without the user's explicit permission.
- One logical change per commit; when a change spans unrelated concerns, propose a numbered commit plan.
- Message: `type: summary` (`feat`, `fix`, `docs`, `test`, `refactor`, `chore`, `ci`, `build`, `perf`), imperative, no period, ≤ 72 characters; an optional body says what changed and why.
- Before committing: the exit criteria in `AGENTS.md`, then `git status`, `git diff` and `git log -5`; stage only that commit's files.
- No AI attribution (`Co-Authored-By: Claude`, `Generated with …`) anywhere; `scripts/strip_watermarks.py` and `pr-title.yaml` enforce it.
- Never `--no-verify`, amend or force-push; push a feature branch, never `main`; never draft or WIP PRs (the shell guard denies them).
- After pushing, run `uv run python scripts/pr_follow.py` until it exits 0 (desktop app: `ccd_pr` `get_status` while checks run). It lists red checks, a stale branch, open threads and every comment (Codecov, Copilot): fix red checks in new commits, merge `origin/main` when behind, fix or answer each comment; never hand off on red.
- PRs open ready for review, titled in commit style, with the body of `.github/pull_request_template.md`.
- After `gh pr create`: `gh pr edit <n> --add-assignee Pawlo77 --add-label <label>`, with `bug` for `fix`, `documentation` for `docs` and `enhancement` otherwise.

<!-- Generated from .cursor/rules/minimal-diff.mdc by scripts/sync_rules.py; do not edit. -->

# Minimal diff

- Read the surrounding code first; match its naming, types and patterns.
- Solve the requested task only; no drive-by refactors.
- Reuse existing functions before adding abstractions; no one-line helpers; no handling for impossible cases.
- New behaviour needs tests first (`tdd.mdc`); no tests of the obvious.
- No new markdown files unless requested.
- If two approaches work, pick the simpler one that matches the repository.
- When porting from another repository, bring over only the slice the task needs.
