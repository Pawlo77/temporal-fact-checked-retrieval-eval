---
title: Research
tags: [type/hub]
created: 2026-01-01
parent: "[[temporal-fact-checked-retrieval-eval]]"
---
# Research

Literature on one question: **how much of the reported performance of previously fact-checked claim retrieval (PFCR) survives when a system may search only fact-checks published before the post, and is the penalty larger for Polish than for English?**

A naive "index only earlier fact-checks" filter mixes four effects: the gold fact-check not existing yet, a smaller pool, training-time leakage and missing labels for earlier fact-checks of the same claim. The project separates them with a causal index, answerability-aware metrics and a gap decomposition; see [[Proposed Task]]. State of the art per area is in the `## Summary` of each area note; novelty position below.

## Areas

Each area is a folder with a note of its own name that lists its themes and papers.

| Area | Scope | Notes |
|------|-------|-------|
| [[Claim Retrieval]] | PFCR datasets, shared tasks, methods and systems, language and retrieval bias | 16 |
| [[Temporal Evaluation]] | Chronological splits, query-time retrieval, leakage in claim verification, LLM temporal leakage | 12 |
| [[Evaluation Methodology]] | How data is split and what random and standard splits hide | 3 |
| [[Retrieval Models]] | Embedding models, retrievers and rerankers used as systems | 8 |

Search protocols and outcomes: `protocols/`. Writing standard: `research/AGENTS.md`.

## Novelty position

| Claim | Closest prior work | What remains new |
|---|---|---|
| Per-query causal (date-restricted) PFCR index | [[TREC 2011 Microblog]]; [[Role of Context in PFCR]]; [[MultiClaim]] | First date-restricted fact-check pool per query for PFCR |
| Answerability separate from ranking | [[Missing Counter-Evidence]] | Answerable rate with conditional and unconditional scores |
| Pool-size-matched control | [[MultiClaim]] random pool sweep | Per-query size matched to the causal pool |
| Statistics leakage | [[TREC 2011 Microblog]] | Measured for PFCR (BM25 full vs causal statistics) |
| Training-time leakage | [[Role of Context in PFCR]]; [[Chronological Splits Rumor Detection]] | Multilingual social-media PFCR, separated from index effects |
| Cluster-expanded qrels for earlier siblings | [[AVeriTeC]]; [[MultiClaimNet]]; [[AMC-16K]] | Sibling relevance as a causal-protocol label set |
| Time-to-findability metric | [[StreamingQA]]; [[LongEval 2023]] | Days until a debunk ranks in the top 10 |
| Additive gap decomposition | none found | Random-to-causal chain with paired-bootstrap deltas |
| Parametric leakage of LLM rerankers | [[Simulated Ignorance Fails]] | Pre- vs post-cutoff query strata on PFCR |
| Polish-English DiD with archive density | [[SemEval-2025 Task 7]]; [[AMC-16K]]; [[Language and Retrieval Bias]] | Within-language causal penalty vs archive density |

## Not claimable

- Time-respecting evaluation as an idea ([[TREC 2011 Microblog]]) or rolling evaluation ([[StreamingQA]], [[LongEval 2023]]).
- First chronological PFCR evaluation ([[Role of Context in PFCR]]) or out-of-time test set ([[SemEval-2025 Task 7]]).
- First pool-size control ([[MultiClaim]]); any language-bias finding ([[Language and Retrieval Bias]]).
- The method of PINGAN AI (undocumented) or a Polish-to-English score of [[mmlw-retrieval-roberta-large]] (unreported).
