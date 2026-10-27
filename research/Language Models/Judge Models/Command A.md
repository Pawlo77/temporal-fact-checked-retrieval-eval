---
title: "Command A"
aliases: ["Command A: An Enterprise-Ready Large Language Model"]
authors: ["Team Cohere", "Aakanksha", "Arash Ahmadian", "Marwan Ahmed"]
year: 2025
venue: "arXiv technical report 2504.00698; Hugging Face model card CohereLabs/c4ai-command-a-03-2025"
arxiv: "2504.00698"
url: "https://arxiv.org/abs/2504.00698"
citekey: cohere2025command
verified: 2026-10-27
theme: "[[Judge Models]]"
related: ["[[2026-10-27-temporal-retrieval-eval]]", "[[LLM selection]]", "[[Qwen3 Embedding]]", "[[AMC-16K]]", "[[Language and Retrieval Bias]]", "[[gpt-oss-120b]]", "[[Mistral Large 2411]]", "[[Panel of LLM Evaluators]]", "[[Llama 3.3]]", "[[PLLuM]]"]
tags: [type/paper, theme/llm-judge-model, topic/multilingual, topic/polish, topic/llm, topic/evaluation]
---
# Command A

> [!info] TL;DR
> Command A is Cohere's 111B model for enterprise use, with retrieval-augmented generation, tools and 23 languages including Polish. It has 256K context, a hybrid sliding-window and global attention design and open weights for research under CC-BY-NC. The report gives no training cutoff, and Polish appears only in a language-by-language head-to-head against other chat models.

## Motivation

- Enterprises need agentic, retrieval-grounded and multilingual models that run on modest hardware, but leading models need large clusters.
- Cohere targets 23 "key languages of global business" and reports a serving footprint of two A100 or H100 GPUs.
- Models should answer from supplied documents and decline when the context lacks the answer, which matters for any judge that reads evidence.
- Related notes: its predecessor Command R+ was an LLM labeller in [[AMC-16K]] and the judge in [[PLLuM]], and a Command model sat in the [[Panel of LLM Evaluators]].

## Method

Notation: query post $q$, candidate fact-check $f$; the judge returns a label for the pair $(q, f)$.

**Architecture.** A decoder-only transformer with SwiGLU, grouped-query attention, no bias terms, parallel blocks and a 255,000-token multilingual tokenizer. Layers interleave sliding-window attention with rotary positions and full attention without positions at a 3:1 ratio. The card gives a window of 4096 and 256K context, configured as 128K on Hugging Face.

**Data.** Web text, code, synthetic data, human-written instruction data and vendor data; web text is filtered for quality and educational content. The report lists no sources by name and no cutoff.

**Post-training.** Six expert models (code, safety, retrieval-augmented generation, mathematics, multilingual and general) are trained by supervised fine-tuning and preference tuning, then merged by weight averaging. A "polishing" phase uses best-of-N sampling and preference optimisation to improve style. Intuition: merging combines separate skills without retraining one model on everything.

**Languages.** English, French, Spanish, Italian, German, Portuguese, Japanese, Korean, Arabic, Chinese, Russian, Polish, Turkish, Vietnamese, Dutch, Czech, Indonesian, Ukrainian, Romanian, Greek, Hindi, Hebrew and Persian.

**Size and licence.** 111.06B bf16 parameters, about 222 GB of weights; CC-BY-NC-4.0 with an acceptable-use addendum, so non-commercial research only.

## Key numbers

- Academic: MMLU 85.5, MATH 80.0, IFEval 90.9, GPQA 50.8; Llama 3.3 70B scores 86.0, 77.0, 92.1 and 50.5.
- Standard retrieval-augmented tasks: ChatRAGBench 72.9, HotPotQA 92.1, DROP 91.1; enterprise answerability accuracy 96% on answerable and 91% on unanswerable questions, against 95% and 87% for Llama 3.3 70B.
- Polish mArenaHard (500 translated hard prompts, LLM-judged): Command A wins 79.9% against Llama 3.3 70B and 64.9% against Mistral Large 2.
- Tool use: BFCL 63.8 and Taubench 51.7.

## Experiments

- **Academic and agentic suites:** MMLU, MATH, IFEval, GPQA, BFCL, Taubench, code and SQL benchmarks against GPT-4o, DeepSeek V3 and Llama models.
- **Multilingual:** NTREX translation (COMET-20 68.8 average), MGSM, INCLUDE-44 and mArenaHard in 23 languages; it is preferred over Llama 3.3 70B, Llama 3.1 405B and DeepSeek V3 in all 23.
- **Human evaluation:** blind head-to-head comparisons in nine priority languages and an enterprise benchmark where it passes 94.2% of generative tasks.
- **Retrieval-augmented generation:** correctness with a judge panel in the style of Verga et al., plus answerability.
- **Long context and safety:** RULER and LongBench-V2, and multilingual safety with LLM judges.

## Data

- Pre-training and post-training sources are described by type only, with no sizes or dates.
- Evaluation: mArenaHard in 23 languages, NTREX-128, FLORES-200, MGSM, INCLUDE (44 languages), ChatRAGBench, HotPotQA, DROP, Bamboogle and internal enterprise sets.

> [!failure] Limitations
> - No training cutoff and no data sources, so exposure to a given fact-check is unknown.
> - Weights are non-commercial research only; derived labels must be checked against the licence.
> - Polish results are an LLM-judged win rate, not a measurement of relevance judging.
> - Most evaluations were run by Cohere with internal sets and, for several multilingual comparisons, LLM judges.
> - On the Polish cultural and language benchmark of the [[Bielik 11B v3]] report, Command-A-03-2025 scores 56.17, below Polish-specialised models near 70.
> - Hosting 111B weights needs several GPUs or quantisation.

## Relation to our project

- Judge 2, from a family disjoint from the evaluated models, with Polish listed among 23 languages ([[2026-10-27-temporal-retrieval-eval]], [[LLM selection]]); the answerable and unanswerable accuracy figures show it can decline when context lacks the answer.
- A predecessor, Command R+, was the judge in the [[PLLuM]] RAG test because it was the open model with the best Polish at that time.
- Serve on two 80 GB GPUs in 8-bit or on larger nodes in bf16; record the CC-BY-NC licence in the results table.
- We validate it per language on the Polish and English [[AMC-16K]] pairs, with English instructions as the default ([[Language and Retrieval Bias]]).
- Agreement between this judge and the other two is checked with Fleiss' kappa, and leave-one-judge-out runs show whether any one family dominates the panel.

## Future work

- **Open:** the conclusion states no future directions; it only restates the enterprise focus on agentic workflows, multilingual use and low serving cost (searched 2026-10).
- **Open:** a Polish relevance-judging evaluation of Command A on fact-check pairs (searched 2026-10).
