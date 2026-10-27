---
title: "Data Splits"
tags: [type/theme, theme/splits]
parent: "[[Evaluation Methodology]]"
---
# Data Splits

How to split data for training and testing, and what random, standard and time-blind splits hide. Part of [[Evaluation Methodology]].

## Summary

- [[We Need to Talk about Standard Splits]] (ACL 2019): the fixed split replicates the published ranking, but one claimed gain is not significant on random splits.
- [[We Need to Talk about Random Splits]] (EACL 2021): random and standard splits over-estimate; the ranking can flip on a new sample.
- [[Mind the Gap]] (NeurIPS 2021): time-blind training costs up to 16% perplexity.
- Not claimable: that [[We Need to Talk about Standard Splits]] show random splits overestimate; they argue the opposite.
- Open: test whether PFCR system ordering flips between random and causal protocols.
- Open: a pool-size-matched control, with the time of the data as the only varying factor.

| Paper | Year | Takeaway |
|-------|------|----------|
| [[We Need to Talk about Standard Splits]] | 2019 | The fixed WSJ split replicates the published tagger ranking, but one claimed gain is not significant on random splits; test over many splits with Bonferroni correction. |
| [[We Need to Talk about Random Splits]] | 2021 | Random and standard splits overestimate performance on new samples, often by over 20 points of error reduction; prefer independent samples or biased splits. |
| [[Mind the Gap]] | 2021 | A language model trained only on text before the test period has up to 16% higher perplexity, and the gap grows with time. |
