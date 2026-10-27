---
title: "Llama 3.3"
aliases: ["meta-llama/Llama-3.3-70B-Instruct (Hugging Face model card)"]
authors: ["Meta AI, Llama team"]
year: 2024
venue: "Hugging Face model card (release 6 December 2024 per the licence); context: Llama 3 herd paper, arXiv 2407.21783"
url: "https://huggingface.co/meta-llama/Llama-3.3-70B-Instruct"
citekey: meta2024llama
verified: 2026-10-27
theme: "[[Evaluated LLMs]]"
related: ["[[2026-10-27-temporal-retrieval-eval]]", "[[LLM selection]]", "[[Qwen3 Embedding]]", "[[AMC-16K]]", "[[Language and Retrieval Bias]]", "[[Gemma 3]]", "[[Apertus]]", "[[Command A]]", "[[Mistral Large 2411]]", "[[Simulated Ignorance Fails]]"]
tags: [type/paper, theme/llm-evaluated, topic/multilingual, topic/llm, topic/reranking, topic/leakage]
---
# Llama 3.3

> [!info] TL;DR
> The source is a Hugging Face model card, read in full, with the [Llama 3 herd paper](https://arxiv.org/abs/2407.21783) for context. Llama 3.3 is a text-only 70B instruction-tuned model with 128K context, pre-training data up to December 2023 and eight supported languages, none of them Polish. It is the earliest stated cutoff in our set, which gives the widest split between exposed and unexposed queries.

## Motivation

- The card positions Llama 3.3 as a 70B model optimised for multilingual dialogue that outperforms many open and closed chat models on common benchmarks.
- The Llama 3 paper shows the group's data recipe: knowledge until the end of 2023 and only a small share of multilingual text.
- For us the model matters as a cutoff control, because its December 2023 date is stated and early.
- Related notes: [[Gemma 3]] and [[Apertus]] state later cutoffs.

## Method

Notation: query post $q$, candidate fact-check $f$; the model scores the pair $(q, f)$ as a reranker.

**Architecture.** An optimised decoder-only transformer with grouped-query attention, 70.55B bf16 parameters and 128K context, so about 141 GB of weights. Instruction tuning uses supervised fine-tuning and reinforcement learning from human feedback.

**Data.** Pre-training uses about 15T tokens from publicly available sources, described only as "a new mix". Fine-tuning data are public instruction sets and over 25M synthetic examples. The card states a pre-training data cutoff of December 2023.

**Languages.** Supported: English, German, French, Italian, Portuguese, Hindi, Spanish and Thai. The card says the model saw more languages than these eight, and calls use in other languages out of scope unless developers fine-tune and take responsibility for safety.

**Licence.** The Llama 3.3 Community License is a custom licence that allows commercial and research use, with attribution and a separate licence for products above 700 million monthly users.

**Herd paper context.** The Llama 3 data mix is roughly 50% general knowledge, 25% mathematics and reasoning, 17% code and 8% multilingual tokens, and the tokenizer adds 28K tokens for non-English languages. Polish appears in that paper only in the list of speech-interface languages.

## Key numbers

- MMLU (chain of thought) 86.0 and MMLU-Pro 68.9, identical or higher than Llama 3.1 70B at 86.0 and 66.4 (card).
- IFEval 92.1 and MGSM 91.1, against 87.5 and 86.9 for Llama 3.1 70B (card); MGSM covers languages that do not include Polish.
- Polish tasks in the [[Bielik 11B v3]] report: 66.40 on the Open PL LLM Leaderboard (Bielik 65.93, Mistral-Large-Instruct-2411 69.84) and 70.73 on Polish EQ-Bench (Bielik 71.20).
- Command A wins 79.9% of Polish mArenaHard comparisons against Llama 3.3 70B, an LLM-judged score from the [[Command A]] report.
- INCLUDE cultural knowledge 71.9 and 69.6 on the cultural average, above Gemma 3 27B at 67.9 and 67.7 (from the [[Apertus]] report).

## Experiments

- **Card benchmarks:** instruction-tuned model on knowledge, steerability, reasoning, code, maths, tool use (BFCL 77.3) and multilingual maths; all English-centred except MGSM.
- **Safety:** the card describes red teaming, child-safety assessments and a warning that use outside supported languages is discouraged without safeguards.
- **Third-party Polish results:** Polish leaderboards place it close to the 11B Polish-specialised [[Bielik 11B v3]], so size alone does not buy Polish quality.

## Data

- Pre-training: about 15T tokens of public web and other data, cutoff December 2023; sources not itemised.
- Fine-tuning: public instruction data and over 25M synthetic examples.
- Evaluation: MMLU, MMLU-Pro, IFEval, GPQA Diamond, HumanEval, MBPP EvalPlus, MATH, BFCL v2 and MGSM.

> [!failure] Limitations
> - Polish is not a supported language, and the card advises against use outside the eight.
> - Data sources are not listed, so exposure to a given fact-check cannot be checked.
> - The earlier cutoff means any post-2023 claim is unknown to the model, which suits our design but limits ranking quality on recent topics.
> - The licence adds attribution and naming obligations, and the card is gated behind an agreement.
> - The card gives no retrieval, reranking or judging evaluation.

## Relation to our project

- Reranker 6, the cutoff control: December 2023 is the earliest stated date among the evaluated models, so the same queries split differently than for [[Gemma 3]] (August 2024) and [[Apertus]] (March 2024). See ([[2026-10-27-temporal-retrieval-eval]], [[LLM selection]]).
- Two 80 GB GPUs hold bf16 weights; the Llama 3.3 Community License is recorded in the results table.
- Language caveat: Polish is outside the supported set, so we run English first and treat Polish rows as a stress test. [[AMC-16K]] reports that Llama 3.1 70B answers in a non-English language in 28% of chain-of-thought outputs.
- It already served as the filter model in the tool of [[Generative-AI Claim Retrieval]], so reranking and filtering precedents exist ([[Language and Retrieval Bias]]).
- Gain jumps near December 2023 would be the leakage signature we test for ([[Simulated Ignorance Fails]]).

## Future work

- **Open:** the card says the model is static and that future tuned versions will follow as safety improves; no evaluation plan is stated (searched 2026-10).
- **Open:** a Polish retrieval or reranking result for Llama 3.3 70B on fact-check data (searched 2026-10).
