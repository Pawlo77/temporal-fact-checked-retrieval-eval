---
paths:
  - "src/**/*.py"
---

<!-- Generated from .cursor/rules/python-quality.mdc by scripts/sync_rules.py; do not edit. -->

# Python quality

Match the tooling in `pyproject.toml`; do not fight ruff or mypy.

## Types

- Imports at module top; no inline imports unless a cycle is documented.
- Annotate every public function, method and module-level name in `src/temporal_fact_checked_retrieval_eval`.
- Prefer `pathlib.Path`, explicit returns and `X | Y` over `Optional`.
- No bare `except:`; no `# type: ignore` without a comment.
- Exhaustive `match` on unions: `never` in the default branch.

## Docstrings (Google style)

- Every file starts with a one-line module docstring, `__init__.py` included; a module-level constant gets a one-line docstring below it.
- Types live in annotations: never repeat them in `Args` or `Returns`.
- One line when the name and signature say enough; add `Args`, `Returns` or `Raises` only for what the code does not show (side effects, ranges, invariants, errors).
- `_private` and tests: docstring only when the logic is not obvious.
- Comments say why, never what.

## Logging

- Stdlib `logging` only; one `logger = logging.getLogger(__name__)` per module; no `print` for diagnostics.
- Lazy formatting (`logger.info("done %s", item_id)`); no `INFO` or above inside tight loops.
- Log an event once, at the layer that owns the decision; never log and re-raise.
