---
paths:
  - "src/**/*.py"
---

<!-- Generated from .cursor/rules/performance.mdc by scripts/sync_rules.py; do not edit. -->

# Performance

Prefer the **fastest correct implementation** with the **lowest practical memory footprint**.

## Design defaults

- Stream large workloads — generators or batched iteration; avoid materializing huge lists upfront
- Bound concurrency memory — do not create one async task per item when inputs can be large
- Reuse precomputed tables and packed encodings in hot loops
- Keep caches sized to real reuse patterns

## End-of-task performance review

After implementation and before hand-off:

1. Identify hot paths touched
2. Estimate memory and time scaling; flag accidental O(n²) or bulk materialization
3. Run `make check`; add `tests/benchmarks/` coverage when changing hot paths (`benchmarks.mdc` / `make bench`)
4. Fix regressions found during review
