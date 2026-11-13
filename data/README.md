# Data

Raw datasets are access-restricted and research-only (MultiClaim v1/v2, SemEval-2025
Task 7) — never commit them. This `data/` tree is gitignored; only this README is
tracked.

## Layout

| Path | Contents |
|---|---|
| `raw/multiclaim_v1/` | MultiClaim v1: `fact_checks.csv`, `posts.csv`, `fact_check_post_mapping (1).csv` |
| `raw/multiclaim_v2/` | MultiClaim v2: same files plus `relationship` column |
| `raw/multiclaimnet/` | MultiClaimNet claim clusters: `ClaimCheck.csv`, `ClaimMatch.csv`, `MultiClaim.csv` |
| `raw/semeval2025_task7/` | SemEval-2025 Task 7 (unzipped): `train_dev_sets/`, `test_set/`, `baselines/`, `scripts/` |
| `processed/` | Derived artifacts (dedup merge, frozen split, results) — never committed |

Loaders live in `src/temporal_fact_checked_retrieval_eval/dataset/`; `multiclaim.py`
reads v1/v2, `synthetic.py` builds a synthetic fixture for tests. No post text is
ever committed anywhere in the repository.
