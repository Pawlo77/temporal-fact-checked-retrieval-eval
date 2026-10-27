---
title: "Claim Retrieval"
tags: [type/hub]
created: 2026-10-27
parent: "[[Research]]"
---
# Claim Retrieval

Previously fact-checked claim retrieval (PFCR): finding earlier fact-checks for a social media post. Each theme is a folder with a note of its own name that lists its papers.

## Summary

- Task defined by [[That is a Known Lie]]; shared tasks [[CheckThat 2021 Task 2]] and [[CheckThat 2022 Task 2]] used fixed splits and no date-restricted pool.
- [[CheckThat 2026]] has no PFCR task, so no live shared task overlaps a temporal PFCR evaluation.
- [[MultiClaim]] (205,751 fact-checks, 39 languages) is the reference multilingual dataset; [[SemEval-2025 Task 7]] added out-of-time test posts.
- Strong recipes combine translation, fine-tuned embedders with hard negatives and LLM reranking ([[TIFIN India]], [[Multilingual vs Crosslingual Retrieval]]).
- Chronological PFCR splits exist only for training ([[Role of Context in PFCR]]: MAP 0.602 down to 0.429).
- Language and retrieval bias is already published ([[Language and Retrieval Bias]]), so it is not our contribution.
- Open for our project: no PFCR evaluation restricts the fact-check index per query to documents published before the post.
- Open: answerability and ranking quality are never reported separately, and earlier sibling fact-checks lack labels.

| Theme | Question it answers |
|-------|---------------------|
| [[Datasets and Benchmarks]] | Which PFCR datasets and shared tasks exist, and how were they built, split and scored? |
| [[Methods and Systems]] | Which retrieval, reranking and LLM methods work for PFCR, and how were they evaluated? |
| [[Bias]] | Which language, popularity and retrieval biases distort PFCR results? |
