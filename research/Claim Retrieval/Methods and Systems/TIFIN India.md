---
title: "TIFIN India"
aliases: ["TIFIN India at SemEval-2025: Harnessing Translation to Overcome Multilingual IR Challenges in Fact-Checked Claim Retrieval"]
authors: ["Prasanna Devadiga", "Arya Suneesh", "Pawan Rajpoot", "Bharatdeep Hazarika", "Aditya Baliga"]
year: 2025
venue: "Proceedings of the 19th International Workshop on Semantic Evaluation (SemEval-2025), pages 2297-2304"
arxiv: "2504.16627"
url: "https://aclanthology.org/2025.semeval-1.299/"
citekey: devadiga2025tifin
verified: 2026-10-27
theme: "[[Methods and Systems]]"
tags: [type/paper, theme/methods, topic/multilingual, topic/polish, topic/shared-task, topic/dense-retrieval, topic/llm]
---
# TIFIN India

> [!info] TL;DR
> A SemEval-2025 Task 7 system that translates every post into English with an LLM, retrieves with a fine-tuned English embedder (Stella 400M) trained with mined hard negatives, and reranks the top 50 with Qwen2.5-72B-Instruct fused by reciprocal rank fusion. It scores Success@10 0.938 monolingual and 0.81025 crosslingual. Translation and fine-tuning give most of the gain; LLM reranking adds 1.7%.

## Motivation

- [[SemEval-2025 Task 7]] asks for fact-checks for posts in many languages, monolingually and crosslingually, scored by Success@10 on [[MultiClaim]] data.
- Language-specific or large multilingual models are costly; the team aimed for a pipeline whose main parts run on one consumer GPU.
- In [[MultiClaim]], English embedders such as GTR-T5 and MPNet were among the top models, and BM25 produced more false positives as the pool grew; the team cites both as reasons for dense English retrieval.

## Method

We write a post as $q$, a fact-check as $f$, and Success@10 as defined in our glossary.

**Embedder choice.** The top-10 MTEB English v2 models under 1B parameters plus MPNet, GTR-T5 and MiniLM are compared on Google-translated English text; Stella 400M (stella_en_400M_v5) is chosen.

**LLM translation.** All posts are translated into English with Aya Expanse 8B, using a prompt that asks for a faithful, cleaned translation that keeps entities and hashtags.

**Hard-negative fine-tuning.** Stella is fine-tuned on translated training pairs with negatives mined by Sentence Transformers; gains plateau near 40 negatives per query, and 20 are used.

**LLM reranking and fusion.** Qwen2.5-72B-Instruct receives the post and the top-50 candidates and returns the 10 most relevant IDs. Reciprocal rank fusion merges this list with the fine-tuned retriever's ranking.

Intuition: translation puts every language into the space where the strongest small embedders were trained, and the LLM only reorders a short list.

## Key numbers

- Monolingual test ablation: Stella 0.8159, with its s2p prompt 0.8305, with translated posts 0.8837, fine-tuned 0.9217, with reranking and fusion 0.938.
- Final per-language Success@10: Polish 0.886, English 0.880, Turkish 0.904, Malay 1.0; crosslingual 0.81025.
- Conventional rerankers lower Success@10 by 0.032 to 0.127; the Qwen reranker adds 0.025.
- Translating test posts takes 61 minutes and fine-tuning 35 minutes on one RTX 4090.

## Experiments

- **Base embedders:** 15 models on translated posts; Stella leads (0.815 average), multilingual-e5-large reaches 0.802. German and Portuguese are hardest, Malay and Thai easiest.
- **Rerankers:** ColBERTv2, two mxbai rerankers and InRanker hurt both MiniLM and Stella; a Cohere reranker helped at first, but its gain was matched by hard-negative fine-tuning.
- **Hybrid search:** adding BM25 helps MiniLM but hurts Stella, so only dense rankings are fused.
- **LLM rerankers:** Gemini 1.5 Pro, Llama 3.1 70B, Llama 3.3 70B and Qwen2.5 72B were tried; Qwen was best. The reranker table names Qwen2-72B-Instruct while the text says Qwen2.5-72B-Instruct.

## Data

- SemEval-2025 Task 7 data, a MultiClaim subset with original text, OCR text and Google translations; posts in 27 languages and fact-checks in 39 in the full dataset.
- Monolingual test languages reported: English, French, German, Portuguese, Spanish, Thai, Malay, Arabic, Turkish and Polish.

> [!failure] Limitations
> - No temporal analysis: fine-tuning uses the task's training pairs and the full fact-check pool is searchable for every post.
> - The 72B reranker and the translation LLM have unknown training cutoffs and could have seen the fact-checks.
> - Embedder search was limited to models under 1B parameters by hardware.
> - Crosslingual results are given only as one number, with no ablation.

## Relation to our project

- It is a ready recipe for our strongest system family: translate, fine-tune with hard negatives, rerank with an LLM ([[Proposed Task]]).
- Each stage carries a leakage route our protocol separates: supervised pairs from a random split, and LLM parametric knowledge of fact-checks published after the post ([[Enhanced topic research]]).
- Its Polish score (0.886) slightly above English (0.880) is evidence against assuming Polish is the weaker language under random evaluation ([[Language scope analysis]]).
- Its finding that rerankers add little when the retriever is fine-tuned tells us to report reranking gains separately under causal and full pools ([[Research summary]]).

## Future work

- **Open:** testing the pipeline on other datasets (searched 2026-10).
- **Open:** quantised embedding vectors for efficiency (searched 2026-10).
- **Open:** LLM translation for low-resource languages in PFCR (searched 2026-10).
- **Open:** the same pipeline under a time-respecting split and date-restricted pool (searched 2026-10).
