---
title: "Retrieval Models"
tags: [type/theme]
created: 2026-10-27
parent: "[[Research]]"
---
# Retrieval Models

Embedding models, retrievers and rerankers used as systems in our experiments. Each note records what the model is, what its source reports and how we use it.

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
