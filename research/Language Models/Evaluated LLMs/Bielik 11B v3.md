---
title: "Bielik 11B v3"
aliases: ["Bielik 11B v3: Multilingual Large Language Model for European Languages"]
authors: ["Krzysztof Ociepa", "Łukasz Flis", "Remigiusz Kinas", "Krzysztof Wróbel", "Adrian Gwoździej"]
year: 2026
venue: "arXiv preprint 2601.11579 (v1, preliminary version); Hugging Face model card speakleash/Bielik-11B-v3.0-Instruct"
arxiv: "2601.11579"
url: "https://arxiv.org/abs/2601.11579"
citekey: ociepa2026bielik
verified: 2026-10-27
theme: "[[Evaluated LLMs]]"
related: ["[[2026-10-27-temporal-retrieval-eval]]", "[[LLM selection]]", "[[Qwen3 Embedding]]", "[[AMC-16K]]", "[[Language and Retrieval Bias]]", "[[polish-reranker-roberta-v3]]", "[[PLLuM]]", "[[Mistral Large 2411]]", "[[Llama 3.3]]", "[[Apertus]]"]
tags: [type/paper, theme/llm-evaluated, topic/polish, topic/multilingual, topic/llm, topic/reranking]
---
# Bielik 11B v3

> [!info] TL;DR
> Bielik 11B v3 is an 11B model for Polish and 31 other European languages, made by depth up-scaling Mistral 7B v0.2 and continuing pre-training on 1.1T tokens. After supervised fine-tuning, DPO-Positive and reinforcement learning it scores 65.93 on the Open PL LLM Leaderboard, close to Llama 3.3 70B at 66.40. It has Apache 2.0 weights, no stated data cutoff and about 22 GB of bf16 weights.

## Motivation

- General multilingual models handle Polish poorly: the Mistral 7B v0.2 tokenizer needs 747 tokens for a Polish passage that Polish-trained APT tokenizers encode in 344 to 375.
- High-quality Polish instruction data are scarce, so SpeakLeash annotators write and correct instructions by hand.
- The report names [[PLLuM]] (Polish models) and [[Apertus]] (broad multilingual) as related work.
- The aim is a model that runs on consumer GPUs with up to 24 GB of VRAM.

## Method

Notation: query post $q$, candidate fact-check $f$; the model scores the pair $(q, f)$ as a reranker.

**Depth up-scaling.** Start from the 32-layer Mistral 7B v0.2, duplicate layers, then cut eight layers at the junction from each copy, giving 50 layers and 11.17B parameters. Intuition: stacking trimmed copies of a trained network gives a deeper starting point than random initialisation.

**Tokenizer.** The Mistral tokenizer is kept (32,000 tokens plus chat tokens, 32,128 total) for balance across the 32 languages. Polish text costs about 3.2 tokens per word with it.

**Pre-training.** Three stages: over 1T tokens at 8,192 context; about 50B tokens at 32,768; over 1B tokens at 65,536 with YaRN. The mixture has 32 languages, with Polish 54.25% and English 20.5% of documents, from CulturaX, HPLT v2.0, FineWeb, FineWeb-Edu, SlimPajama, Common Crawl, legal texts, parliamentary proceedings and journals.

**Post-training.** Supervised fine-tuning on 20M instructions and dialogues for three epochs; DPO-Positive on 114,000 preference examples; reinforcement learning with GRPO and Dr. GRPO on 143k problems with verifiable rewards.

**Data rights, cutoff, size.** Collection began in November 2022 and is ongoing, with `robots.txt` and text-and-data-mining reservations excluded retroactively; no cutoff date is stated. The card names Apache 2.0, ChatML format and 32 European languages "optimized for Polish". The weights are 11.17B bf16 parameters, about 22 GB.

## Key numbers

- Open PL LLM Leaderboard 65.93 for the instruct model against 55.16 for the base, above Llama 3.1 70B Instruct (65.49) and Mixtral 8x22B (65.23), below Llama 3.3 70B (66.40) and Mistral-Large-Instruct-2411 (69.84).
- Polish Linguistic and Cultural Competency Benchmark 71.83%, first among open models listed; Llama-3.3-70B scores 48.83, Gemma-3-27B 47.33 and Command-A-03-2025 56.17 in the same table.
- INCLUDE-base-44 Polish 69.0, against 58.9 for Qwen2.5-14B-Instruct and 49.6 for Apertus-8B-Instruct.
- Belebele across 28 European languages 82.98, below Qwen2.5-14B-Instruct at 85.91.

## Experiments

- **Polish benchmark suite:** Open PL LLM Leaderboard (sentiment, NER, topic, reading comprehension, QA, similarity, summarisation, RAG-style QA), Polish EQ-Bench (71.20), CPTUB (3.73) and a Polish medical exam leaderboard (50.21%).
- **English and multilingual checks:** Open LLM Leaderboard average 72.45, GSM8K 85.60, FLORES translation 19.22 BLEU (from Polish 19.91).
- **Version comparison:** v3 improves over v2.6 on Belebele (82.98 against 68.67) and FLORES (19.22 against 13.58), and slightly drops on EQ-Bench (71.20 against 73.8).
- **Pre-training monitoring:** checkpoints are tracked on the Polish and English leaderboards to catch degradation.

## Data

- Pre-training corpus: 32 languages, over 1T tokens (the report also states 1.1T total), roughly 428.6M Polish and 162.0M English documents.
- Post-training: human-written and synthetic Polish instructions, a 114,000-example preference set and 143k verifiable problems.
- Evaluation: Open PL LLM Leaderboard (an SpeakLeash/Cyfronet project), CPTUB, PLCC (600 questions), PES medical exams, INCLUDE-base-44, Belebele and FLORES.

> [!failure] Limitations
> - The report is a preliminary version and says results may change.
> - Several leaderboards are run by the authors' own project, and an author maintains the Open PL LLM Leaderboard.
> - The training-data cutoff and the base model's own data are not stated, so a pre/post-cutoff split is not possible.
> - The report does not describe the pre-training data of the Mistral 7B v0.2 base, which Bielik inherits.
> - No retrieval, reranking or relevance-judging result is reported.
> - The 32,000-token vocabulary is inefficient for Polish, which raises input cost for long fact-checks.

## Relation to our project

- Reranker 5, the Polish-specialised one, against the Polish cross-encoder [[polish-reranker-roberta-v3]]; at about 22 GB it fits one GPU ([[2026-10-27-temporal-retrieval-eval]], [[LLM selection]]).
- It states no cutoff, so it stays in the "cutoff unknown" group and out of the cutoff regression. Collection began in November 2022 and is ongoing, so later Polish fact-checks may also be in the data.
- It shares ancestry with [[Mistral Large 2411]], the judge, so Bielik rows also get a leave-Mistral-out score.
- Polish ability is measured on knowledge and language tasks, not on relevance; we validate it on the 400 Polish [[AMC-16K]] pairs before using its rankings ([[Language and Retrieval Bias]]).

## Future work

- **Open:** the authors plan larger variants, more European and global languages, domain adaptation (legal, medical, scientific), multimodal extensions and more ablations of each training stage (searched 2026-10).
- **Open:** a published retrieval, reranking or relevance-judging result for Bielik 11B v3 on Polish fact-check data (searched 2026-10).
