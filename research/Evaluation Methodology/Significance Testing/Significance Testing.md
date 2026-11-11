---
title: "Significance Testing"
tags: [type/theme, theme/significance-testing]
parent: "[[Evaluation Methodology]]"
---
# Significance Testing

Which paired significance test or interval to use when comparing retrieval systems over the same queries.

## Summary

- [[Significance Testing in IR]] (SIGIR 2019): t and permutation tests hold Type I error at $\alpha$ for 25–100 topics; bootstrap-shift, Wilcoxon and sign over-reject.
- Not claimable: that it justifies a cluster bootstrap with 1,000 resamples; it recommends the t-test and drops the bootstrap-shift test.
- Open: error rates at thousands of queries, with clustered queries, and bootstrap interval coverage.

| Paper | Year | Takeaway |
|-------|------|----------|
| [[Significance Testing in IR]] | 2019 | Over 500 million simulated p-values, the paired t and permutation tests keep Type I error at $\alpha$; use the t-test for means and discontinue bootstrap-shift, Wilcoxon and sign tests. |
