---
title: "Olmo 3"
aliases: ["Olmo 3"]
authors: ["Team Olmo", "Allyson Ettinger", "Amanda Bertsch", "Bailey Kuehl", "David Graham"]
year: 2025
venue: "arXiv technical report 2512.13961; Hugging Face model card allenai/Olmo-3-1125-32B (base model)"
arxiv: "2512.13961"
url: "https://arxiv.org/abs/2512.13961"
citekey: olmo2025olmo
verified: 2026-10-27
theme: "[[Evaluated LLMs]]"
related: ["[[2026-10-27-temporal-retrieval-eval]]", "[[LLM selection]]", "[[Qwen3 Embedding]]", "[[AMC-16K]]", "[[Language and Retrieval Bias]]", "[[Apertus]]", "[[Gemma 3]]", "[[Simulated Ignorance Fails]]"]
tags: [type/paper, theme/llm-evaluated, topic/english, topic/llm, topic/reranking, topic/leakage]
---
# Olmo 3

> [!info] TL;DR
> Olmo 3 is a fully open family of 7B and 32B models: the report releases every stage, checkpoint and dataset, from the 5.5T-token Dolma 3 pretraining mix to the Think and Instruct models. The base model's card gives an English-only scope, Apache 2.0 licence and a "Dec 2024" date cutoff. Its corpus can be searched for a gold fact-check, but it offers no Polish.

## Motivation

- Releasing only weights hides the data and recipes that decide what a model knows, so the authors release the whole "model flow".
- Fully open models at 32B trailed open-weight peers such as Qwen 3 32B, so the report aims at a stronger open recipe.
- Open data allow tracing model outputs back to training documents, which closed models cannot offer.
- Related notes: [[Apertus]] is the other open-data model in our set, at 70B and with 1,811 languages.

## Method

Notation: query post $q$, candidate fact-check $f$; the model is used as a reranker that scores the pair $(q, f)$.

**Pretraining data.** Dolma 3 Mix has 5.93T tokens (the card says 5.50T for the 32B run). Common Crawl supplies 76.1%, from 104 dumps with a cutoff of 31 December 2024, kept only if the language classifier says English. Further sources are olmOCR-processed science PDFs (13.6%, crawl cutoff December 2024), Stack-Edu code, arXiv, FineMath and Wikipedia.

**Staged training.** Stage 1 is the pretraining mix. Stage 2 is mid-training on two 100B-token mixes of web, code, mathematics, question answering and instruction data, with decontamination against benchmark sets. Stage 3 extends context to 65,536 tokens with 100B tokens. The 32B final checkpoint merges four checkpoints.

**Mid-training crawl.** A separate high-quality STEM-heavy crawl ran from 12 September 2024 to 3 June 2025, so mid-training data extend past the December 2024 cutoff on the card.

**Post-training.** Think models use supervised fine-tuning, preference tuning and reinforcement learning with verifiable rewards; Instruct models follow a similar pipeline; Olmo 3.1 32B Instruct is a later checkpoint reported in the same document.

**Size and licence.** The 32B base has 32.23B bf16 parameters, about 64.5 GB of weights. The card states Apache 2.0, English as the only language and a date cutoff of December 2024.

## Key numbers

- The 32B base scores 78.3 on MMLU Humanities and 70.8 on MMLU STEM, against 80.5 and 74.9 for Gemma 3 27B (card, base models).
- Olmo 3-Eval Math is 61.6 and Code 40.0 for the 32B base, against 39.7 and 23.3 for Apertus-70B and 53.9 and 20.5 for OLMo 2-32B (card).
- Olmo 3.1 32B Instruct scores 80.9 on MMLU and 88.8 on IFEval, against 74.6 and 85.4 for Gemma 3 27B and 70.2 and 70.4 for Apertus 70B (report).
- AlpacaEval 2 length-controlled: 59.8 for Olmo 3.1 32B Instruct, below Gemma 3 27B at 65.5.

## Experiments

- **Base-model evaluation:** a suite of maths, code, multiple-choice and generative question-answering tasks; the card compares the 32B base with open-weight and fully open bases of similar size.
- **Decontamination:** matches of benchmark items are searched in mid-training sources and removed; the report finds decontaminated mixes perform better, not worse.
- **Think and Instruct post-training:** each stage (supervised, preference, reinforcement) adds gains; the report calls Olmo 3.1 Think 32B and Instruct 32B the best fully open models at 32B.
- **Data tracing:** because all data are public, reasoning chains can be traced back to training documents.

## Data

- Dolma 3 Mix: 5.93T tokens in the report, mostly English web, with PDFs, code, arXiv, mathematics and Wikipedia.
- Dolma 3 Dolmino mix and Longmino mix: 100B-token mid-training and long-context mixes.
- Post-training: Dolci instruction, thinking and preference data, including a multilingual Aya subset for basic multilinguality.

> [!failure] Limitations
> - English only: non-English documents are filtered out, so Polish and cross-lingual claim matching are out of scope.
> - The card describes the base model; instruction-tuned 32B checkpoints have separate cards and a later 3.1 release.
> - The December 2024 cutoff does not cover the mid-training crawl that runs to June 2025.
> - Instruct and Think training adds synthetic data from other models, whose own cutoffs are not controlled.
> - Base models are not instruction-tuned, so a reranker prompt may need few-shot examples or an instruct checkpoint.

## Relation to our project

- Reranker 4 for RQ4, the English slice with auditable data: for each English gold fact-check we search Dolma 3 for its URL and long claim n-grams and record exposure, as for [[Apertus]]. See ([[2026-10-27-temporal-retrieval-eval]], [[LLM selection]]).
- The cutoff for date strata should be treated as uncertain between December 2024 and mid-2025; per-query exposure from the corpus is the safer variable ([[Simulated Ignorance Fails]]).
- At 32B it fits one 80 GB GPU for bf16 weights; we pin a specific checkpoint (base or Olmo 3.1 Instruct) before any run.
- English only, so Polish rows use [[Apertus]], [[Gemma 3]] and Polish models; relevance validation uses English [[AMC-16K]] pairs ([[Language and Retrieval Bias]]).

## Future work

- **Open:** the report hopes to find optimal hyperparameters per base model, and stopped Olmo 3.1 Think reinforcement learning for compute reasons while performance was still rising (searched 2026-10).
- **Open:** a retrieval, reranking or fact-check result for Olmo 3 with corpus-exposure analysis (searched 2026-10).
