---
title: "Data Splits"
tags: [type/theme, theme/splits]
parent: "[[Evaluation Methodology]]"
---
# Data Splits

How to split data for training and testing, and what random, standard and time-blind splits hide. Part of [[Evaluation Methodology]].

| Paper | Year | Takeaway |
|-------|------|----------|
| [[We Need to Talk about Standard Splits]] | 2019 | The fixed WSJ split replicates the published tagger ranking, but one claimed gain is not significant on random splits; test over many splits with Bonferroni correction. |
| [[We Need to Talk about Random Splits]] | 2021 | Random and standard splits overestimate performance on new samples, often by over 20 points of error reduction; prefer independent samples or biased splits. |
| [[Mind the Gap]] | 2021 | A language model trained only on text before the test period has up to 16% higher perplexity, and the gap grows with time. |
