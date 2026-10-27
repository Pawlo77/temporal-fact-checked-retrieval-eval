---
title: "bge-reranker-v2-m3"
aliases: ["BAAI/bge-reranker-v2-m3 (Hugging Face model card)"]
authors: ["Beijing Academy of Artificial Intelligence (BAAI), FlagEmbedding team"]
year: 2024
venue: "Hugging Face model card (undated; evaluation images carry 2024-03-17 names)"
url: "https://huggingface.co/BAAI/bge-reranker-v2-m3"
citekey: baai2024reranker
verified: 2026-10-27
theme: "[[Retrieval Models]]"
tags: [type/paper, theme/models, topic/multilingual, topic/reranking]
---
# bge-reranker-v2-m3

> [!info] TL;DR
> The source is a Hugging Face model card, read in full, with its two linked papers: arXiv 2312.15503 (Llama2Vec, cited by the card as "Making Large Language Models A Better Foundation For Dense Retrieval") and [[BGE-M3]]. Neither describes this reranker, and the card has no DOI. It is a multilingual cross-encoder initialised from bge-m3 that outputs a relevance score for a query-passage pair. The card gives its evaluation only as images, so we report no numbers from it.

## Motivation

- Embedding models score a query and a passage separately; a reranker reads both together and outputs a relevance score directly, which is more precise but slower.
- The BGE reranker family covers Chinese and English (base, large) and multilingual use (v2-m3, v2-gemma); v2-m3 is the lightweight, easy-to-deploy multilingual option.
- Its backbone is [[BGE-M3]], a multilingual retriever; the card reranks the top 100 candidates of bge-m3 on MIRACL.

## Method

Notation: query post $q$, candidate fact-check $f$; the model returns a raw score $s(q,f)$.

**Architecture.** A cross-encoder with bge-m3 as base model. Input is the query and passage as one pair; the output is a single logit. Higher is more relevant, and a sigmoid maps it to $[0,1]$ (the card's `normalize=True`).

Intuition: the model reads the post and the fact-check together, so word-level interaction decides the score.

**Training.** The card states that the LLM-based rerankers of the family (gemma-2b, MiniCPM-2B) are trained on bge-m3-data, Quora and FEVER training data. It does not list training data for v2-m3 itself.

**Use.** The card's example truncates to 512 tokens; the context length of 8192 comes from a secondary source, the [[polish-reranker-roberta-v3]] card.

## Key numbers

- None read as text on the card: the MIRACL, BEIR, C-MTEB and llama-index results are images.
- Secondary figures from other sources: 568M parameters and 8192 context ([[polish-reranker-roberta-v3]] card); 58.36 on the multilingual retrieval subset when reranking the top 100 of Qwen3-Embedding-0.6B, below the embedder alone at 64.64 ([[Qwen3 Embedding]]).
- Polish administration sets with a BGE-M3 retriever, NDCG@10: 78.8 (opi-urzedowe), 74.3 (ezd-qa), 85.4 (ezd-ir-chunked), under polish-reranker-roberta-v3 on all three.

## Experiments

- **Card evaluation:** reranking top-100 candidates from bge-en-v1.5 and e5-mistral-7b-instruct (BEIR), bge-zh-v1.5 (C-MTEB retrieval) and bge-m3 (MIRACL, multilingual), plus a llama-index test; all shown as images.
- **Independent comparisons:** [[Qwen3 Embedding]] and [[polish-reranker-roberta-v3]] include it as a baseline.

## Data

- Evaluation sets named on the card: BEIR, C-MTEB retrieval, MIRACL, llama-index; sizes not stated.
- Training data for v2-m3: not stated.

> [!failure] Limitations
> - Results are only images; the card has no numeric tables, significance tests or per-language breakdown.
> - Reranking can lower quality: it falls below the embedder alone on several suites in the Qwen3 report.
> - Training data and cutoff for v2-m3 are not stated.
> - The example truncates inputs at 512 tokens.

## Relation to our project

- Our multilingual reranker; it can score Polish posts against English fact-checks, unlike the Polish-only [[polish-reranker-roberta-v3]] ([[2026-10-27-temporal-retrieval-eval|Project plan]], [[Language scope]]).
- Sharing a base with [[BGE-M3]] means reranker and retriever share pre-training exposure; we treat it as one parametric-leakage source and report the retriever alone next to every reranked run ([[Topic research]]).

## Future work

- **Partly done:** independent multilingual evaluation; [[Qwen3 Embedding]] and the [[polish-reranker-roberta-v3]] card compare it, but only on retrieval, not on fact-check data.
- **Open:** a published per-language or Polish-to-English result for this reranker (searched 2026-10).
