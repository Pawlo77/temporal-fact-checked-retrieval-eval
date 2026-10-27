---
title: "LLM Temporal Leakage"
tags: [type/theme, theme/llm-leakage]
parent: "[[Temporal Evaluation]]"
---
# LLM Temporal Leakage

How post-cutoff information reaches an evaluation through an LLM's parametric knowledge or through date-filtered web search, and how to measure and block it. Part of [[Temporal Evaluation]].

| Paper | Year | Takeaway |
|-------|------|----------|
| [[Temporal Leakage in Date-Filtered Web Retrieval]] | 2026 | Google and DuckDuckGo date filters return a page with major post-cutoff information for 71% and 81% of questions; leaky pages cut Brier from 0.24 to 0.11. |
| [[Simulated Ignorance Fails]] | 2026 | A prompted cutoff closes only 48% of the gap between simulated and true ignorance; reasoning models leak more behind cleaner traces. |
| [[All Leaks Count]] | 2026 | Claim-level Shapley-weighted leakage shows date-filtered RAG amplifies leakage 2.5 to 4.7 times; claim supervision removes most of it. |
