---
title: "Significance Testing"
tags: [type/theme, theme/significance-testing]
parent: "[[Evaluation Methodology]]"
---
# Significance Testing

Which paired significance test or interval to use when comparing retrieval systems over the same queries.

## Summary

- [[Significance Testing in IR]] (SIGIR 2019): t and permutation tests hold Type I error at $\alpha$ for 25–100 topics; bootstrap-shift, Wilcoxon and sign over-reject.
- Claimable: a paired permutation test (or t-test) for p-values. Not claimable: support for bootstrap intervals, cluster resampling or 1,000 resamples; it drops the bootstrap-shift test.
- Open: error rates with clustered queries, and bootstrap interval coverage; thousands of queries are partly covered by later work.

| Paper | Year | Takeaway |
|-------|------|----------|
| [[Significance Testing in IR]] | 2019 | Over 500 million simulated p-values, the paired t and permutation tests keep Type I error at $\alpha$; use the t-test for means and discontinue bootstrap-shift, Wilcoxon and sign tests. |
