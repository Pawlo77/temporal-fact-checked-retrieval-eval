# 2025 - Devadiga - TIFIN India at SemEval-2025 Task 7

## Citation

- Authors: Prasanna Jagadeesh Devadiga, Arya Suneesh, Pawan Kumar Rajpoot, Bharatdeep Hazarika, Aditya U. Baliga (full list as cited in the task overview)
- Title: TIFIN India at SemEval-2025: Harnessing Translation to Overcome Multilingual IR Challenges in Fact-Checked Claim Retrieval
- Venue: Proceedings of SemEval-2025, pages 2297-2304
- Year: 2025
- URL: https://aclanthology.org/2025.semeval-1.299/ (PDF read); arXiv 2504.16627
- Verified on: 2026-10-27

## Why this paper

- PINGAN AI (rank 1 in both tracks) has no system paper: it carries no reference in Tables 8/9 of the overview and is absent from Table 7. TIFIN India is the highest-ranked team with a paper in the monolingual track (rank 3 mono, 4 cross). RACAI (rank 4 mono, 3 cross; SemEval-2025 best system paper for Task 7) is summarised from the overview only.

## What it does

- Translates posts to English with Aya Expanse 8B.
- Retrieval with Stella 400M, fine-tuned with mined hard negatives (gains plateau near 40 negatives per query).
- LLM reranking of the top 50 with Qwen2.5-72B-Instruct, fused with the base retrieval by Reciprocal Rank Fusion.
- Reports that conventional cross-encoder rerankers hurt, and recommends translation plus a fine-tuned embedder as capturing most of the gain.
- RACAI (from the overview): single-stage BGE-Multilingual-Gemma2-9B embeddings, original languages, parameter-efficient fine-tuning, no reranking.

## Key numbers

- Final monolingual S@10 0.938; crosslingual 0.81025 (abstract; overview Table 8 shows avg 0.9383, pol 0.8860, tur 0.9040, eng 0.8800).
- Table 1/5 path: Stella base 0.8159 -> s2p prompt 0.8305 -> translated posts 0.8837 -> fine-tuned 0.9217 -> + rerank + RRF 0.938 (rerank + RRF +1.7%).
- Table 4: cross-encoder rerankers deltas -0.127 to -0.032; Qwen reranker +0.025 (Table 4 labels it Qwen/Qwen2-72B-Instruct while the text says Qwen2.5-72B-Instruct; the paper is inconsistent).

## Relation to our project

- Gives a concrete S5/S6 recipe (translate, fine-tune with hard negatives, LLM rerank top 50) whose leakage we can test: fine-tuning uses MultiClaim train pairs (random split) and the reranker is a 72B LLM with unknown cutoff.
- No temporal analysis in what was read.

## Verification

- Status: OK.
- Supports the "LLM reranking" part of line 59, but for TIFIN India, not PINGAN AI.
