---
title: "Datasets and Benchmarks"
tags: [type/theme]
created: 2026-10-27
parent: "[[Claim Retrieval]]"
---
# Datasets and Benchmarks

PFCR datasets, shared tasks and dataset releases: what posts, fact-checks and links exist, and how they were split and scored.

## Summary

- [[MultiClaim]] has 205,751 fact-checks, 28,092 posts and 31,305 pairs; v2 ([[MultiClaim Zenodo Records]]) grows to 435k fact-checks, 89k posts and 105k pairs.
- [[MultiClaim]] ran three temporal analyses over the full index, including a random pool-size sweep (100 to 2,100) and post-newer vs post-older pairs (80.02 vs 80.04 S@10).
- [[SemEval-2025 Task 7]] tested on out-of-time posts against a pool reaching May 2024; Polish and Turkish were unseen languages.
- Its best system, PINGAN AI, reached mono average S@10 0.9601 with no system description, so its method cannot be cited.
- [[AMC-16K]] adds 16K human-labelled pairs in 20 languages, including 400 Polish monolingual pairs.
- [[MultiClaimNet]] clusters 85.3K fact-checks into 30.9K clusters, an enabler for sibling relevance labels.
- [[CheckThat 2021 Task 2]] and [[CheckThat 2022 Task 2]] fixed splits without a date-restricted pool; [[CheckThat 2026]] has no PFCR task.
- Open: v1 and v2 timestamp semantics, the `backlink` relation and the pair-count mismatch stay undefined.

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
