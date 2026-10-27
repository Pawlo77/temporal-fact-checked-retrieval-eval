---
title: "Judging and Reliability"
tags: [type/theme, theme/llm-judging]
parent: "[[Language Models]]"
---
# Judging and Reliability

Reliability, bias and non-determinism of LLM judges and hosted LLM APIs: when a judge shares a family with a judged system, when labels can be gamed, and when "deterministic" calls differ. It constrains the judge design in [[LLM selection]] and the [[2026-10-27-temporal-retrieval-eval|project plan]].

## Summary

- [[LLM Judges Favour LLM Rankers]]: Gemini judges score every LLM reranker above human-preferred oracle rankings, so judge families must be disjoint from evaluated systems.
- [[Self-Preference Bias]]: judges recognise and favour their own text; recognition and preference rise together linearly.
- [[Panel of LLM Evaluators]]: a three-family panel of small judges beats GPT-4 in agreement with humans and costs 7 to 8 times less.
- [[Rubric Self-Preference]]: self-preference survives objective binary rubrics, and ensembling reduces it without removing it.
- [[LLM Relevance Judgments Can Be Gamed]]: LLM relevance labels are a ranking method; agreement falls to 0.51 among the top 20 systems, so expanded qrels are a bound.
- [[ChatGPT Behavior Drift]]: hosted snapshots change within months, so judges are pinned open weights.
- [[LLM Non-Determinism]]: temperature 0 still gives run-to-run accuracy swings of up to 15%, so flip rates are reported.

| Paper | Year | Takeaway |
|-------|------|----------|
| [[LLM Judges Favour LLM Rankers]] | 2025 | LLM judges invert the human order of oracle versus LLM rankers on TREC DL and cannot separate close systems. |
| [[Self-Preference Bias]] | 2024 | GPT-4 recognises its own summaries with 73.5% accuracy; self-preference grows linearly with self-recognition. |
| [[Panel of LLM Evaluators]] | 2024 | Three smaller judges from three families agree better with humans than GPT-4 and show less self-bias. |
| [[LLM Relevance Judgments Can Be Gamed]] | 2024 | Judge-based reranking inflates judged scores while human scores stay at 0.68 to 0.72; top-20 Kendall tau is 0.51. |
| [[Rubric Self-Preference]] | 2026 | Rubric judging keeps self-preference, up to a 20-fold ratio on code, mitigated but not removed by ensembling. |
| [[ChatGPT Behavior Drift]] | 2024 | GPT-4 prime accuracy fell from 84.0% to 51.1% between March and June 2023. |
| [[LLM Non-Determinism]] | 2024 | At temperature 0, accuracy varies up to 15% across ten runs and raw outputs rarely repeat. |
