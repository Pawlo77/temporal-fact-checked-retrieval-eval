---
title: "Gemma 3"
aliases: ["Gemma 3 Technical Report"]
authors: ["Gemma Team", "Aishwarya Kamath", "Johan Ferret", "Shreya Pathak"]
year: 2025
venue: "arXiv technical report 2503.19786; Hugging Face model card google/gemma-3-27b-it; Google AI model card (knowledge cutoff)"
arxiv: "2503.19786"
url: "https://arxiv.org/abs/2503.19786"
citekey: gemmateam2025gemma
verified: 2026-10-27
theme: "[[Evaluated LLMs]]"
related: ["[[2026-10-27-temporal-retrieval-eval]]", "[[LLM selection]]", "[[Qwen3 Embedding]]", "[[AMC-16K]]", "[[Language and Retrieval Bias]]", "[[Llama 3.3]]", "[[Apertus]]", "[[Simulated Ignorance Fails]]"]
tags: [type/paper, theme/llm-evaluated, topic/multilingual, topic/llm, topic/reranking, topic/leakage]
---
# Gemma 3

> [!info] TL;DR
> Gemma 3 is Google's open multilingual model family from 1B to 27B parameters, with 128K context and image input. The 27B model was trained on 14T tokens with knowledge distillation and a stated knowledge cutoff of August 2024. Weights are open under the Gemma terms, but the training data are not, and neither the report nor the cards give a Polish result.

## Motivation

- Long context makes the key-value cache explode: a global-only design adds about 60% memory overhead at 32K tokens, against under 15% for the Gemma 3 layout.
- The new version adds image input, 128K context and a wider language coverage while keeping consumer-grade hardware in reach.
- Distillation from a larger teacher gives small models more quality at a fixed token budget.
- Related notes: [[Llama 3.3]] is the older English-leaning open baseline, and [[Apertus]] publishes its data.

## Method

Notation: query post $q$, candidate fact-check $f$; the model is used as a reranker that scores the pair $(q, f)$.

**Architecture.** A decoder-only transformer with five local sliding-window attention layers (span 1024 tokens) for every global layer. Pre-training uses 32K sequences, and 128K is added at the end by rescaling RoPE. The 27B model has 25.6B non-embedding, 1.4B embedding and 0.4B vision-encoder parameters, and the Hugging Face metadata counts 27.43B in bf16.

**Pre-training.** 14T tokens for 27B, 12T for 12B, 4T for 4B and 2T for 1B, with all models distilled from a larger teacher that the report does not name. The mixture adds monolingual and parallel data, balanced across languages with a strategy borrowed from earlier multilingual work. The tokenizer is the Gemini 2.0 SentencePiece tokenizer with 262k entries. Evaluation sets are decontaminated from the training mix.

**Post-training.** Distillation from a large instruction-tuned teacher, then reinforcement learning with weight-averaged reward models, code-execution feedback and ground-truth maths rewards.

**Data and cutoff.** The Hugging Face card lists web documents in over 140 languages, code, mathematics and images, with no sources or per-language sizes. The knowledge cutoff of August 2024 appears only on the Google AI model card, not in the report.

**Weights and memory.** The report gives 54.0 GB for bf16 weights of the 27B model, and 72.7 GB with a key-value cache at 32,768 tokens. The Hugging Face card sets the licence to "gemma" with a terms-of-use gate.

## Key numbers

- Instruction-tuned 27B scores 75.1 on Global MMLU-Lite, against 68.6 for Gemma 2 27B (report, zero-shot).
- The pre-trained 27B scores 76.8 on XQuAD across languages, 55.7 ChrF on WMT24++ and 24.4 on ECLeKTic cross-lingual knowledge transfer (card).
- Chatbot Arena Elo 1338 for the 27B instruction-tuned model, preliminary as of March 2025, above Llama 3.3 70B at 1257.
- Cultural knowledge: 67.9 on INCLUDE for gemma-3-27b-it, below Llama-3.3-70B-Instruct at 71.9 (from the [[Apertus]] report).
- Polish tasks: the [[Bielik 11B v3]] report lists gemma-3-27b-it at 55.92 on the Open PL LLM Leaderboard, below its 12B sibling at 62.20.

## Experiments

- **Pre-training probes:** general-ability probes show gains over Gemma 2 in most categories; the authors warn that decontamination may leave probes contaminated.
- **Ablations:** moving from 1:1 to 5:1 local-to-global layers has minimal impact on perplexity, and the sliding window can shrink a lot without hurting it.
- **Memorization:** Gemma 3 models memorize long-form text at a much lower rate than earlier Gemma and Gemini models, with little difference between 4B and 27B.
- **Safety:** evaluations include child safety, content safety and representational harms, and use English prompts only.

## Data

- Pre-training corpus: not released; 14T tokens for 27B, over 140 languages, categories only.
- Benchmarks on the card: HellaSwag, BoolQ, TriviaQA, MMLU, MGSM, Global-MMLU-Lite, WMT24++, FloRes, XQuAD and ECLeKTic, among others.

> [!failure] Limitations
> - Training data and sources are closed, so exposure of a given fact-check cannot be audited.
> - The cutoff comes from a separate Google page; the report is silent, and effective cutoffs often differ from stated ones.
> - The unnamed teacher may carry knowledge from later data than the stated cutoff.
> - No Polish-specific result appears in the report or card, and the safety evaluation is English only.
> - Reported Polish leaderboard scores of the 27B model are lower than for its 12B sibling, which we cannot explain from the sources.

## Relation to our project

- Reranker 2 for RQ5, with a stated August 2024 cutoff inside the query period; a 27B bf16 model fits one 80 GB GPU for weights, with the cache on top ([[2026-10-27-temporal-retrieval-eval]], [[LLM selection]]).
- Already used as a relevance judge in [[Language and Retrieval Bias]], where it gained in every prompting strategy, so its behaviour on the PFCR domain has precedent; compare [[AMC-16K]].
- Language caveat: "over 140 languages" is a coverage claim, not a Polish measurement, so we validate on the 400 Polish [[AMC-16K]] pairs first.
- The distillation teacher is unknown, so we treat the August 2024 cutoff as a lower bound on exposure, not as a clean boundary ([[Simulated Ignorance Fails]]).
- Gemma terms of use apply to outputs we release; we have not checked how they treat derived qrels.

## Future work

- **Open:** the report names no future directions beyond safety release policy; it states only that it focused on images, long context, multilinguality and STEM.
- **Open:** a published Polish retrieval or reranking result for Gemma 3 27B (searched 2026-10).
- **Open:** the identity of the distillation teacher and its data cutoff (searched 2026-10).
