---
title: "Chronological Evaluation"
tags: [type/theme, theme/chronological]
parent: "[[Temporal Evaluation]]"
---
# Chronological Evaluation

Chronological splits, time-respecting retrieval evaluation, temporal persistence and leakage in recommender evaluation: how scores change when a system sees only what existed at query time.

## Summary

- [[TREC 2011 Microblog]] is the origin of the causal idea and of statistics leakage: runs may not use future evidence or IDF from later tweets.
- [[StreamingQA]] evaluates dated questions against a growing time-stamped corpus.
- [[LongEval 2023]] evaluates on successive snapshots; the 2023 change in NDCG was system-dependent.
- [[Chronological Splits Rumor Detection]]: chronological splits lower every model (Twitter 16 logistic regression 89.3 to 48.7 macro-F1).
- [[Data Leakage in Recommender Evaluation]] and [[Dont Get Ahead of Yourself]] show timeline leakage reorders models (nDCG@10 cut by 21.7% to 73.4%).
- Not claimable: time-respecting evaluation as an idea, or rolling evaluation over a growing corpus.
- Open: a per-query date-restricted pool for PFCR, and BM25 statistics computed from the causal pool only.
- Open: report rank stability of systems between random and causal protocols, not only score drops.

| Paper | Year | Takeaway |
|-------|------|----------|
| [[TREC 2011 Microblog]] | 2011 | Defines query-time search; the compulsory run bans future evidence, including IDF computed on later tweets. |
| [[StreamingQA]] | 2022 | Dated questions against a growing dated news index; adding articles adapts open-book models with almost no forgetting. |
| [[Chronological Splits Rumor Detection]] | 2023 | Chronological instead of random splits significantly lower every model on four rumor benchmarks (Twitter 16 logistic regression: 89.3 to 48.7 macro-F1). |
| [[Data Leakage in Recommender Evaluation]] | 2023 | Training on interactions after the test moment makes models recommend items that did not yet exist; the proposed timeline scheme removes this. |
| [[LongEval 2023]] | 2023 | Retrieval systems on later Qwant snapshots did not drop on average NDCG; the most stable systems were not the most effective. |
| [[Dont Get Ahead of Yourself]] | 2025 | Removing future leakage from sequential recommender evaluation cuts sampled nDCG@10 by 21.7% to 73.4% and changes the best model in 7 of 8 settings. |
