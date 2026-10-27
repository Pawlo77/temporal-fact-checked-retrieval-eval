---
title: "Temporal Evaluation"
tags: [type/hub]
created: 2026-10-27
parent: "[[Research]]"
---
# Temporal Evaluation

How evaluation changes when time is respected: what a system may see at query time, and where information from the future leaks in. Each theme is a folder with a note of its own name that lists its papers.

## Summary

- Time-respecting retrieval evaluation is old: [[TREC 2011 Microblog]] banned future evidence, including IDF from later tweets.
- [[StreamingQA]] and [[LongEval 2023]] evaluate over a growing or snapshotted corpus; the LongEval change was system-dependent, not a uniform drop.
- Verification benchmarks restrict evidence by date, yet the guarantee is approximate ([[AVeriTeC]]: about 6% of dev answers from fact-checking domains).
- Random splits overestimate in neighbouring tasks ([[Chronological Splits Rumor Detection]], [[Dont Get Ahead of Yourself]]).
- LLMs add a second leak: date filters and prompted ignorance fail ([[Temporal Leakage in Date-Filtered Web Retrieval]], [[Simulated Ignorance Fails]]).
- Open: no PFCR evaluation restricts the fact-check index to documents published before each query.
- Open: statistics leakage for BM25, answerability, sibling labels and parametric leakage of rerankers have not been measured for PFCR.
- Full claim-by-claim position: [[Research#Novelty position]].

| Theme | Question it answers |
|-------|---------------------|
| [[Chronological Evaluation]] | How are chronological splits, query-time retrieval and leakage-free timelines defined, and how much do scores drop? |
| [[Leakage in Verification]] | How do evidence and answers from after the claim leak into claim verification benchmarks? |
| [[LLM Temporal Leakage]] | How do LLM parametric knowledge and date-filtered web search leak post-cutoff information? |
