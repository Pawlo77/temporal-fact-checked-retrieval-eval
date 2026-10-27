---
title: "Datasets and Benchmarks"
tags: [type/theme]
created: 2026-10-27
parent: "[[Claim Retrieval]]"
---
# Datasets and Benchmarks

PFCR datasets, shared tasks and dataset releases: what posts, fact-checks and links exist, and how they were split and scored.

| Paper | Year | Takeaway |
|-------|------|----------|
| [[CheckThat 2021 Task 2]] | 2021 | Tweet (Arabic, English) and debate PFCR shared task; BM25 plus reranking wins on tweets, nothing beats BM25 on debates. |
| [[CheckThat 2022 Task 2]] | 2022 | Reruns 2021 with a small new test set; sentence-T5 plus GPT-Neo reranking reaches MAP@5 0.956 on English tweets. |
| [[MultiClaim]] | 2023 | 28k posts, 206k fact-checks, 27/39 languages; translation helps, and its post-newer vs older leak test finds no leak. |
| [[SemEval-2025 Task 7]] | 2025 | Monolingual and crosslingual PFCR on MultiClaim with out-of-time test posts and unseen Polish and Turkish. |
| [[AMC-16K]] | 2025 | 16k human-labelled post-fact-check pairs in 20 languages; LLMs judge relevance well but worse on Slavic languages. |
| [[MultiClaimNet]] | 2025 | 85.3K MultiClaim fact-checks in 30.9K LLM-built same-claim clusters, with timestamps. |
| [[MultiClaim Zenodo Records]] | 2025 | Dataset records of MultiClaim v1 and v2 (435k fact-checks, 89k posts), with per-instance timestamps and pair provenance. |
| [[CheckThat 2026]] | 2026 | 2026 lab tasks: scientific source retrieval, numerical claims, article generation; no PFCR task. |
