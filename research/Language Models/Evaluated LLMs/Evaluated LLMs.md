---
title: "Evaluated LLMs"
tags: [type/theme, theme/llm-evaluated]
parent: "[[Language Models]]"
---
# Evaluated LLMs

LLMs we evaluate as rerankers of the shared first-stage candidates. They differ in stated cutoff, data openness and Polish coverage, so the RQ4 effect (gain on queries whose gold fact-check predates the cutoff) can be tested across families.

## Summary

- Stated cutoffs span December 2023 ([[Llama 3.3]]) to December 2024 ([[Olmo 3]]), with [[Apertus]] at March 2024 and [[Gemma 3]] at August 2024.
- Auditable pretraining data exist only for [[Apertus]] (70B, 1,811 languages, Goldfish loss) and [[Olmo 3]] (32B, English).
- Stated cutoffs are weak: [[Gemma 3]] states it on a separate page, [[Olmo 3]] adds a mid-training crawl to June 2025, and [[Apertus]] gives its cutoff only in a prompt template.
- [[Bielik 11B v3]] (22 GB) and [[PLLuM]] are Polish-specialised and state no cutoff.
- Polish coverage is not measured for reranking in any source; [[Llama 3.3]] lists eight languages without Polish.
- Open: none of the six reports retrieval or relevance judging on fact-check data, so each is validated first on [[AMC-16K]] pairs.

| Paper | Year | Takeaway |
|-------|------|----------|
| [[Gemma 3]] | 2025 | 27B, 14T tokens distilled from an unnamed teacher; cutoff August 2024 (Google page), over 140 languages, closed data, Gemma terms. |
| [[Apertus]] | 2026 | Fully open 8B and 70B; 15T tokens in 1,811 languages, Polish 3% of web documents; March 2024 cutoff; Apache 2.0. |
| [[Olmo 3]] | 2025 | Open 7B and 32B; English-only Dolma 3 corpus; card cutoff December 2024, mid-training crawl to June 2025. |
| [[Llama 3.3]] | 2024 | 70B, cutoff December 2023, eight supported languages without Polish; earliest cutoff, widest pre/post split. |
| [[Bielik 11B v3]] | 2026 | 11B Polish-optimised model from Mistral 7B; 65.93 on Open PL LLM Leaderboard; no cutoff stated; Apache 2.0. |
| [[PLLuM]] | 2025 | Polish family from Llama and Mistral bases on a 140B-token corpus; no cutoff; mixed licences; Polish retrieval table with rerankers. |
