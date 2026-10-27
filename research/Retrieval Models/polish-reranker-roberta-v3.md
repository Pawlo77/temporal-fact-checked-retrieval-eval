---
title: "polish-reranker-roberta-v3"
aliases: ["sdadas/polish-reranker-roberta-v3 (Hugging Face model card)"]
authors: ["Sławomir Dadas"]
year: 2025
venue: "Hugging Face model card (undated; compares Qwen3-Reranker, so 2025 or later)"
url: "https://huggingface.co/sdadas/polish-reranker-roberta-v3"
citekey: dadas2025polish
verified: 2026-10-27
theme: "[[Retrieval Models]]"
tags: [type/paper, theme/models, topic/polish, topic/reranking]
---
# polish-reranker-roberta-v3

> [!info] TL;DR
> The source is a Hugging Face model card, read in full, and the paper it cites (Dadas and Grębowiec, arXiv 2402.14318, Springer DOI 10.1007/978-3-031-84353-2_4). The model is a 443M-parameter Polish cross-encoder with 8192-token context, distilled from an LLM reranker. The card has no DOI or arXiv id of its own. It reports NDCG@10 of 66.21 in the PIRB reranker category.

## Motivation

- RAG pipelines need a reranker that handles long documents; the predecessor, polish-reranker-roberta-v2, reads only 512 tokens.
- LLM rerankers such as Qwen3-Reranker-8B ([[Qwen3 Embedding]]) are strong but large; the card shows a small Polish model can match them on many Polish tasks.
- The earlier reranker line is described in [Dadas and Grębowiec, 2024](https://arxiv.org/abs/2402.14318), which evaluates Polish rerankers on the 41 PIRB tasks and finds most models generalise poorly out of domain.

## Method

Notation: query post $q$, candidate fact-check $f$; the reranker outputs a score $s(q,f)$ for each candidate in a first-stage list.

**Backbone.** A new long-context Polish RoBERTa (`PKOBP/polish-roberta-8k`) supporting 8192 tokens (v2: 512, a 16x increase). The input is the query and passage joined by separator tokens, and the output is a single logit.

**Training.** Knowledge distillation: the teacher is the LLM reranker BAAI/bge-reranker-v2.5-gemma2-lightweight, and the student learns its ranking with the RankNet pairwise loss. The corpus is largely that of v2, plus about 40,000 public-administration passages from Polish government and municipal sites, with questions generated synthetically by DeepSeek-V3-0324.

Intuition: the student copies the ordering of a much larger LLM judge, so it can run cheaply on every query.

## Key numbers

- NDCG@10 of 66.21 in the PIRB Rerankers category (card), with BAAI/bge-multilingual-gemma2 as retriever; v2 scored 65.30 under the same retriever.
- Average PIRB score rises from 64.49 (v2) to 65.17 (v3) with [[mmlw-retrieval-roberta-large]] as retriever.
- It beats Qwen3-Reranker-8B on 18 of 41 PIRB tasks with about 5% of its parameters.
- Public administration, BGE-M3 retriever, NDCG@10 (opi-urzedowe / ezd-qa / ezd-ir-chunked): v3 86.3 / 80.1 / 86.7; [[bge-reranker-v2-m3]] 78.8 / 74.3 / 85.4; Qwen3-Reranker-8B 84.1 / 79.9 / 84.8.

## Experiments

- **Long-context gain:** v2 against v3 on PIRB tasks with long documents. Gains are largest on eprawnik (+5.73 and +9.12 NDCG@10 for the two retrievers), quora (+5.65, +8.25) and abczdrowie (+4.70, +6.25).
- **Short texts:** v3 matches v2 on short and medium texts and is slightly worse on very short ones (onet, czy-wiesz-v2).
- **Public administration:** three Polish administration sets reranked from [[BGE-M3]] candidates, compared with five other rerankers.

## Data

- Distillation corpus: largely that of v2, not itemised on the card.
- Public-administration addition: about 40,000 passages with DeepSeek-V3-generated questions.
- Evaluation: PIRB (41 tasks, see [[PIRB]]), and opi-urzedowe, ezd-qa (manual Q&A) and ezd-ir-chunked (passages up to several thousand tokens).

> [!failure] Limitations
> - The licence on the card is "gemma", not Apache-2.0, inherited from the teacher; check it before redistributing derived artefacts.
> - Polish only; the card has no cross-lingual reranking result.
> - Numbers come from the author's own benchmark, with no significance tests.
> - The card gives no training date or data cutoff.
> - A drop on very short texts.

## Relation to our project

- Our Polish reranker over a Polish candidate list; the 8K context lets it read full fact-check articles, not only claims and titles ([[2026-10-27-temporal-retrieval-eval|Project plan]], [[Topic research]]).
- It cannot score Polish posts against English fact-checks reliably, so [[bge-reranker-v2-m3]] covers the cross-lingual case ([[Language scope]]).
- Teacher and student are LLM-derived, so parametric knowledge of dated events may enter the ranking; we report the retriever alone next to every reranked run.

## Future work

- **Partly done:** wider comparison with LLM rerankers; the card compares Qwen3-Reranker-4B and 8B ([[Qwen3 Embedding]]).
- **Open:** cross-lingual (Polish to English) reranking with a Polish-trained cross-encoder (searched 2026-10).
- **Open:** a dated or claim-matching reranking task for Polish (searched 2026-10).
