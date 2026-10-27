---
title: "gpt-oss-120b"
aliases: ["gpt-oss-120b & gpt-oss-20b Model Card"]
authors: ["OpenAI", "Sandhini Agarwal", "Lama Ahmad"]
year: 2025
venue: "arXiv model card 2508.10925; Hugging Face model card openai/gpt-oss-120b"
arxiv: "2508.10925"
url: "https://arxiv.org/abs/2508.10925"
citekey: openai2025gptoss
verified: 2026-10-27
theme: "[[Judge Models]]"
related: ["[[2026-10-27-temporal-retrieval-eval]]", "[[LLM selection]]", "[[Qwen3 Embedding]]", "[[AMC-16K]]", "[[Language and Retrieval Bias]]", "[[Temporal Leakage in Date-Filtered Web Retrieval]]", "[[Command A]]", "[[Mistral Large 2411]]", "[[Panel of LLM Evaluators]]", "[[Self-Preference Bias]]"]
tags: [type/paper, theme/llm-judge-model, topic/llm, topic/multilingual, topic/evaluation, topic/judge-bias]
---
# gpt-oss-120b

> [!info] TL;DR
> gpt-oss-120b is OpenAI's open-weight reasoning model: a mixture-of-experts transformer with 116.8B total and 5.1B active parameters, shipped in 4-bit form so that it fits one 80 GB GPU. The model card paper states a knowledge cutoff of June 2024, an Apache 2.0 licence and reasoning levels that change accuracy. It tests 14 languages for multilingual knowledge, and Polish is not one of them.

## Motivation

- The release targets reasoning and agentic workflows with open weights under Apache 2.0, an adjustable reasoning effort and full access to the chain of thought.
- The release is called a model card because the models will be used in many systems built by others.
- For us, a judge needs open weights (pinned and rerunnable), a family disjoint from the evaluated models, and enough reasoning to label relevance.
- Related notes: [[Command A]] and [[Mistral Large 2411]] are the other two judges.

## Method

Notation: query post $q$, candidate fact-check $f$; the judge returns a label for the pair $(q, f)$, such as relevant or not.

**Architecture.** An autoregressive mixture-of-experts transformer with 36 layers and 128 experts, of which 4 are chosen per token. Attention alternates banded and dense layers, with grouped-query attention and a context extended to 131,072 tokens by YaRN. Total parameters are 116.83B, active parameters 5.13B per token.

**Quantisation.** The expert weights, over 90% of parameters, are post-trained in MXFP4 at 4.25 bits per parameter. The checkpoint is 60.8 GiB and runs on one 80 GB GPU; all evaluations used this form. A bf16 copy would need about 234 GB, by 2-bytes-per-parameter arithmetic.

**Training.** Text-only data of trillions of tokens, focused on STEM, coding and general knowledge, with hazardous-biology content filtered out. The knowledge cutoff is June 2024. Training took 2.1M H100-hours. Post-training uses chain-of-thought reinforcement learning like OpenAI o3.

**Interface.** The harmony chat format has system, developer, user, assistant and tool roles, and the model emits reasoning ("analysis") before the final answer. Three reasoning levels (low, medium, high) are set in the system prompt, and longer reasoning raises accuracy at higher latency.

**Licence.** Apache 2.0 with a usage policy. The card warns that raw chain of thought is not for end users and may hallucinate.

## Key numbers

- At high reasoning: MMLU 90.0 and GPQA Diamond 80.1 without tools, against 85.9 and 67.1 at low reasoning.
- Multilingual MMLU (14 languages, professionally translated) averages 81.3 at high reasoning and 74.1 at low, against 85.2 for OpenAI o4-mini; Italian 85.0, German 83.0, Swahili 72.3, Yoruba 62.4.
- SimpleQA accuracy 0.168 with hallucination rate 0.782, below o4-mini at 0.234 and 0.750 (no browsing).
- PersonQA accuracy 0.298 against 0.356 for o4-mini.

## Experiments

- **Reasoning and tools:** AIME, GPQA, HLE, MMLU, coding (Codeforces, SWE-Bench) and tool-use (tau-bench) at three reasoning levels; the model comes close to o4-mini.
- **Multilingual:** MMMLU in Arabic, Bengali, Chinese, French, German, Hindi, Indonesian, Italian, Japanese, Korean, Portuguese, Spanish, Swahili and Yoruba; accuracy falls with language resource level.
- **Health:** HealthBench 57.6 and Hard 30.0 at high reasoning, close to o3.
- **Hallucination, bias, safety:** SimpleQA and PersonQA, BBQ (0.87 ambiguous, 0.90 disambiguated), instruction hierarchy and jailbreak tests.

## Data

- Pre-training: trillions of text tokens, STEM-heavy, cutoff June 2024; sources not listed.
- Evaluation: AIME 2024 and 2025, GPQA Diamond, HLE, MMLU, MMMLU, SWE-Bench Verified, HealthBench, SimpleQA, PersonQA and BBQ.

> [!failure] Limitations
> - No Polish evaluation: MMMLU omits Polish, so Polish judging quality is unmeasured.
> - Factual recall without browsing is weak, so verdicts must rest on the supplied text of the post and fact-check.
> - Reasoning level changes results by several points, so the level must be fixed and reported.
> - The raw chain of thought is unconstrained and may hallucinate; only the final verdict should be used.
> - Data sources are closed and the model is OpenAI's, so judge-side leakage of well-known fact-checks cannot be excluded.

## Relation to our project

- Judge 1, in a three-family panel with [[Command A]] and [[Mistral Large 2411]], disjoint from every evaluated family ([[2026-10-27-temporal-retrieval-eval]], [[LLM selection]]). The panel idea follows [[Panel of LLM Evaluators]] and self-preference risk motivates the disjointness ([[Self-Preference Bias]]).
- Precedent: it served as leakage judge in [[Temporal Leakage in Date-Filtered Web Retrieval]], agreeing with humans at quadratic weighted kappa 0.85 on 134 documents; that work was in English.
- One 80 GB GPU holds the released weights, so it is the cheapest judge to serve.
- Before use we validate it on the 400 Polish and the English [[AMC-16K]] pairs, report precision on same-topic negatives and fix the reasoning level ([[Language and Retrieval Bias]]).
- Its June 2024 cutoff sits inside our query period, so a judge may have seen some fact-checks; judge prompts therefore carry the full texts and no instruction to recall facts.

## Future work

- **Open:** the card paper notes that no direct optimisation pressure was placed on the chain of thought, to let the community study monitorability; it names no other direction (searched 2026-10).
- **Open:** a Polish or cross-lingual relevance-judging evaluation of gpt-oss-120b (searched 2026-10).
