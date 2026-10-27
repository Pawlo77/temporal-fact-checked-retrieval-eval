---
title: "Methods and Systems"
tags: [type/theme, theme/methods]
parent: "[[Claim Retrieval]]"
---
# Methods and Systems

PFCR and claim-matching methods, systems and evaluation studies: how posts are matched to earlier fact-checks, and under which splits those systems were scored. Part of [[Claim Retrieval]].

## Summary

- [[That is a Known Lie]] defines PFCR and sets BM25 plus a reranker as the first strong baseline on a random split.
- [[Claim Matching Beyond English]] shows multilingual claim matching without a temporal protocol.
- [[Role of Context in PFCR]] already compares chronological and random splits: reranker MAP 0.602 (sentence random) down to 0.429 (debate chronological).
- That split restricts training data only; no date-restricted verified-claim pool is described.
- [[Multilingual vs Crosslingual Retrieval]] finds LLM reranking best on a 47-language v2 subset, with random stratified splits.
- [[TIFIN India]] (translate, fine-tune with hard negatives, rerank the top 50) is a leakage-testable recipe: Success@10 0.938.
- [[Generative-AI Claim Retrieval]] offers date filtering as a user feature, not as an evaluation protocol.
- Open: rerankers add little over a fine-tuned retriever, so gains must be reported separately under full and causal pools.

| Paper | Year | Takeaway |
|-------|------|----------|
| [[That is a Known Lie]] | 2020 | Defines PFCR; BM25 plus a rankSVM reranker over sentence-BERT scores is the first strong baseline, evaluated on a random split. |
| [[Claim Matching Beyond English]] | 2021 | Distilled XLM-R matches WhatsApp tipline claims in five Indian languages and English better than LaBSE or LASER. |
| [[CrowdChecked]] | 2022 | 332K crowd reply-link pairs with noise-aware training reach MAP@5 90.3 on CheckThat! 2021, trained on data newer than the test set. |
| [[Role of Context in PFCR]] | 2022 | Debate context lifts MAP to 0.532; a chronological split drops the earlier model from 0.602 to 0.429, without a date-restricted pool. |
| [[Multilingual vs Crosslingual Retrieval]] | 2025 | On 47 languages of MultiClaim v2, LLM reranking and similarity-mined negatives win; crosslingual retrieval behaves differently. |
| [[TIFIN India]] | 2025 | Translate to English, fine-tune Stella with hard negatives, rerank with Qwen2.5-72B: Success@10 0.938 at SemEval-2025 Task 7. |
| [[Generative-AI Claim Retrieval]] | 2025 | Retrieval, LLM filtering, summaries and verdicts for fact-checkers; date filtering through embeddings fails. |
