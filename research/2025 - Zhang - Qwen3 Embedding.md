# 2025 - Zhang - Qwen3 Embedding

## Citation

- Authors: Yanzhao Zhang, Mingxin Li, Dingkun Long, Xin Zhang, Huan Lin, Baosong Yang, Pengjun Xie, An Yang, Dayiheng Liu, Junyang Lin, Fei Huang, Jingren Zhou
- Title: Qwen3 Embedding: Advancing Text Embedding and Reranking Through Foundation Models
- Venue: arXiv:2506.05176 (v3, 11 Jun 2025); technical report
- Year: 2025
- URL: https://arxiv.org/abs/2506.05176
- Verified on: 2026-10-27 (arXiv abstract and HTML v3 read)

## What it does

- Releases Qwen3-Embedding and Qwen3-Reranker models at 0.6B, 4B and 8B, initialised from dense Qwen3 foundation models, 32K context, Apache 2.0.
- Uses large-scale synthetic training data, then supervised fine-tuning and model merging (ablated in Table 5).
- Evaluates embedders on MMTEB (216 tasks: MTEB Multilingual 131, English v2 41, CMTEB 32, Code 12) and rerankers on MTEB-R, CMTEB-R, MMTEB-R, MLDR, MTEB-Code, FollowIR.

## Key numbers

- Section 1 / Table 2: Qwen3-Embedding-8B 70.58 on MTEB Multilingual (mean task); 4B 69.45; 0.6B 64.33; multilingual-e5-large-instruct 63.22; BGE-M3 59.56 (baselines taken from the MTEB leaderboard on 4 June 2025).
- Table 3: Qwen3-Embedding-8B 75.22 MTEB English v2; 80.68 MTEB Code.
- Reranking table: BGE-reranker-v2-m3 MMTEB-R 58.36 (as a baseline).
- Table 5: Qwen3-Embedding-0.6B drops to 61.21 MMTEB without synthetic data.

## Relation to our project

- S5 LLM-scale retriever/reranker; Qwen3-Reranker-8B exists at the size the note names.
- Released in June 2025 on Qwen3 foundation models, i.e. after MultiClaim v1 and the SemEval-2025 test period; the report does not state a training-data cutoff, so treat it as the system most likely exposed to parametric leakage and use it in the pre/post-cutoff strata.
- Does NOT cover: temporal evaluation, Polish-specific results (not read), claim matching.

## Verification

- OK. Reference list "Zhang et al. 2025, Qwen3 Embedding" with arXiv URL is correct.
