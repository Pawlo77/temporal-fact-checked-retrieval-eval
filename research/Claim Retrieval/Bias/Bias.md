---
title: "Bias"
tags: [type/theme, theme/bias]
parent: "[[Claim Retrieval]]"
---
# Bias

Language, popularity and other systematic biases in PFCR: which languages and which fact-checks systems favour, and how that distorts aggregate scores. Part of [[Claim Retrieval]].

## Summary

- [[Language and Retrieval Bias]] already publishes language and popularity bias in PFCR (EACL 2026).
- LLM relevance judgements favour English instructions; dense retrievers over-return popular COVID-19 claims and malformed fact-checks.
- Not claimable: any language-bias finding or ranking of languages by absolute score.
- Open for our project: the Polish-English comparison must be a within-language causal penalty, not a language ranking.
- Open: clean malformed fact-checks before indexing, equally for full and causal pools.

| Paper | Year | Takeaway |
|-------|------|----------|
| [[Language and Retrieval Bias]] | 2026 | LLM relevance judgements favour English instructions, mostly zero-shot; dense retrievers over-return popular COVID-19 claims and malformed fact-checks. |
