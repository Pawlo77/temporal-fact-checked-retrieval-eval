# 2024 - Chen - M3-Embedding BGE-M3

## Citation

- Authors: Jianlv Chen, Shitao Xiao, Peitian Zhang, Kun Luo, Defu Lian, Zheng Liu
- Title: M3-Embedding: Multi-Linguality, Multi-Functionality, Multi-Granularity Text Embeddings Through Self-Knowledge Distillation
- Venue: Findings of the ACL: ACL 2024, pages 2318-2335, DOI 10.18653/v1/2024.findings-acl.137; preprint arXiv:2402.03216
- Year: 2024
- URL: https://aclanthology.org/2024.findings-acl.137/
- Verified on: 2026-10-27 (Anthology page and arXiv abstract read)

## What it does

- Introduces M3-Embedding (released as BGE-M3), supporting retrieval in more than 100 working languages.
- Supports dense, multi-vector and sparse retrieval from one model.
- Handles inputs from short sentences to documents of up to 8,192 tokens.
- Trains with self-knowledge distillation, using combined relevance scores from the three retrieval modes as the teacher signal, plus an optimised batching strategy.
- Reports state-of-the-art results on multilingual, cross-lingual and long-document retrieval benchmarks.

## Key numbers

- From the abstract: more than 100 languages, up to 8,192 tokens. No benchmark tables were read; I quote no scores from the paper.
- Secondary (Qwen3 Embedding report, Table 2, MTEB Multilingual): BGE-M3 0.6B mean (task) 59.56.

## Relation to our project

- S2 dense baseline; its sparse and multi-vector modes allow a hybrid run without a second model, as the note proposes.
- Base model for BAAI/bge-reranker-v2-m3 (S4).
- Does NOT cover: temporal evaluation, claim matching; training-data cutoff is not stated in the abstract.

## Verification

- OK. Reference list "Chen et al. 2024, M3-Embedding (BGE-M3), Findings ACL" is correct.
