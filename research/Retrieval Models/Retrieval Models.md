---
title: "Retrieval Models"
tags: [type/theme]
created: 2026-10-27
parent: "[[Research]]"
---
# Retrieval Models

Embedding models, retrievers and rerankers used as systems in our experiments. Each note records what the model is, what its source reports and how we use it.

## Summary

- [[Multilingual E5]] and [[BGE-M3]] are the multilingual dense baselines; mE5 is an arXiv technical report.
- [[mmlw-retrieval-roberta-large]] scores NDCG@10 58.46 on the [[PIRB]] card (58.06 in the paper), about 1 point above mE5-large (57.29).
- Rerankers: [[bge-reranker-v2-m3]] (Apache-2.0) and [[polish-reranker-roberta-v3]] (licence "gemma", [[PIRB]] 66.21).
- [[Qwen3 Embedding]] is the LLM-scale option, with no stated training cutoff.
- [[LaBSE]] has a documented 2019-2020 crawl, so it serves as the low-exposure control for parametric leakage.
- Open: training cutoffs of the other models are unstated, so parametric strata compare query periods.
- Open: BM25 statistics must come from the causal pool only, and a learned rescorer trained on full-pool scores would not respect that.
- Open: whether the gemma licence permits releasing derived qrels.

| Note | Role | What it is |
|------|------|------------|
| [[BGE-M3]] | dense retriever | Multilingual dense, sparse and multi-vector retriever |
| [[Multilingual E5]] | dense retriever | Multilingual contrastive text embedder |
| [[Qwen3 Embedding]] | dense retriever | LLM-based embedding and reranking family |
| [[PIRB]] | dense retriever | Polish retrieval benchmark with its Polish models |
| [[mmlw-retrieval-roberta-large]] | dense retriever | Polish encoder distilled from English BGE |
| [[LaBSE]] | cross-lingual encoder | Language-agnostic sentence encoder |
| [[polish-reranker-roberta-v3]] | reranker | Polish long-context cross-encoder |
| [[bge-reranker-v2-m3]] | reranker | Multilingual cross-encoder on a BGE-M3 base |
