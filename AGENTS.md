# AGENTS.md

## Exit criteria

```bash
make check
```

Experiments: edit `configs/experiment.yaml`; local MLflow: `make mlflow`.

## Agent-only

- Chat in caveman ultra (rule `.cursor/rules/caveman.mdc`); files, code, commits and PR bodies stay normal prose.
- Delivery goes through skill `ship`; outside it no commit, push, tag or PR; never force push, amend, draft PRs or push to `main`.
- No new markdown or doc expansion unless asked.
- No runtime dependency without a justification in `pyproject.toml`.
- Use `prek`, never the `pre-commit` CLI; change dependencies in `pyproject.toml` plus `uv lock`.
- Never edit generated files: `.claude/rules/` (edit `.cursor/rules/*.mdc`, then `uv run python scripts/sync_rules.py`), `.codex/agents/` and the tool configs (`make configs`).

## Load order

1. This file and the exit criteria above.
2. Always-apply rules (`.claude/rules/always.md`).
3. Skills are chosen by their descriptions; scoped rules load by file path.
