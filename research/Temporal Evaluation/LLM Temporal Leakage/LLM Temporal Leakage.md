---
title: "LLM Temporal Leakage"
tags: [type/theme, theme/llm-leakage]
parent: "[[Temporal Evaluation]]"
---
# LLM Temporal Leakage

How post-cutoff information reaches an evaluation through an LLM's parametric knowledge or through date-filtered web search, and how to measure and block it.

## Summary

- [[Temporal Leakage in Date-Filtered Web Retrieval]]: date filters return a page with major post-cutoff information for 71% and 81% of questions.
- [[Simulated Ignorance Fails]]: a prompted cutoff closes only 48% of the gap to true ignorance; reasoning models leak more.
- [[All Leaks Count]]: date-filtered RAG amplifies claim-level leakage 2.5 to 4.7 times.
- [[Dated Data]]: effective cutoffs differ from reported ones, by years for some open models.
- [[TripleFact]] and [[Fact-Check Claims Stay Easy]]: fact-check-site claims stay easy after cutoffs; contamination injected into one model lifts a score by 0.23.
- A hard date filter is insufficient, so the causal pool must be built from stored timestamps.
- Open: parametric leakage of LLM rerankers on PFCR, measured on pre- vs post-cutoff query strata.
- Open: high-salience topics are the most exposed, so strata should be reported per topic.
- Open: training cutoffs of the embedders are mostly unstated; stratify rather than claim them away.

| Paper | Year | Takeaway |
|-------|------|----------|
| [[Temporal Leakage in Date-Filtered Web Retrieval]] | 2026 | Google and DuckDuckGo date filters return a page with major post-cutoff information for 71% and 81% of questions; leaky pages cut Brier from 0.24 to 0.11. |
| [[Simulated Ignorance Fails]] | 2026 | A prompted cutoff closes only 48% of the gap between simulated and true ignorance; reasoning models leak more behind cleaner traces. |
| [[All Leaks Count]] | 2026 | Claim-level Shapley-weighted leakage shows date-filtered RAG amplifies leakage 2.5 to 4.7 times; claim supervision removes most of it. |
| [[Dated Data]] | 2024 | Perplexity over dated Wikipedia and news versions gives an effective cutoff, often years before the reported one (RedPajama: 2019 against a 2023 dump). |
| [[TripleFact]] | 2025 | Human-adversarial, live-then-labelled and entity-swapped tests; label contamination in one fine-tuned model lifts a component score 0.62 to 0.85, composite stays 0.49 to 0.57. |
| [[Fact-Check Claims Stay Easy]] | 2025 | PolitiFact and Snopes claims stay easy after cutoffs; iterated RAG-feedback rewrites cut GPT-4o AUC by 17.5 points. |
