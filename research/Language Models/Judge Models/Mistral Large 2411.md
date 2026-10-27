---
title: "Mistral Large 2411"
aliases: ["mistralai/Mistral-Large-Instruct-2411 (Hugging Face model card)"]
authors: ["Mistral AI"]
year: 2024
venue: "Hugging Face model card (undated; the version tag 2411 denotes November 2024)"
url: "https://huggingface.co/mistralai/Mistral-Large-Instruct-2411"
citekey: mistralai2024mistral
verified: 2026-10-27
theme: "[[Judge Models]]"
related: ["[[2026-10-27-temporal-retrieval-eval]]", "[[LLM selection]]", "[[Qwen3 Embedding]]", "[[AMC-16K]]", "[[Language and Retrieval Bias]]", "[[Generative-AI Claim Retrieval]]", "[[gpt-oss-120b]]", "[[Command A]]", "[[Bielik 11B v3]]", "[[Self-Preference Bias]]"]
tags: [type/paper, theme/llm-judge-model, topic/multilingual, topic/polish, topic/llm, topic/evaluation]
---
# Mistral Large 2411

> [!info] TL;DR
> The source is a Hugging Face model card, read in full; it has no technical report, benchmark table, training-data statement or cutoff. Mistral-Large-Instruct-2411 is a dense 123B model with 128K context, an improved system-prompt, function-calling and long-context update of the 2407 release, and a research-only licence. The card names Polish among its languages, and independent Polish evaluations put it at the top of the open models they compare.

## Motivation

- The card says the 2411 release extends Mistral-Large-Instruct-2407 with better long context, function calling and system-prompt handling.
- It describes the model as multilingual by design, proficient in 80 coding languages, agent-centric and strong on retrieval-augmented and long-context applications.
- For us the draw is evidence from other papers: a Mistral Large 123B model was the best labeller of relevance in [[AMC-16K]] and the best filter in [[Generative-AI Claim Retrieval]].
- Related notes: [[gpt-oss-120b]] and [[Command A]] are the other two judges.

## Method

Notation: query post $q$, candidate fact-check $f$; the judge returns a label for the pair $(q, f)$.

**Model.** A dense decoder-only LLM of 122.6B bf16 parameters (the card says 123B), so about 245 GB of weights. The card says running it on GPUs requires over 300 GB of GPU memory and recommends vLLM with tensor parallelism 8 and Mistral's own tokenizer mode.

**Prompting.** The chat format has a dedicated system-prompt block, and the card recommends always including a system prompt that states the bot's purpose. Function calling and JSON output are native.

**Languages.** The card text names English, French, German, Spanish, Italian, Chinese, Japanese, Korean, Portuguese, Dutch and Polish. The metadata list omits Polish and Dutch, so the card is internally inconsistent on Polish.

**Training and cutoff.** The card gives no training data, token count, procedure or knowledge cutoff.

**Licence.** The Mistral AI Research License permits use, modification and distribution for research purposes only. Research purposes cover use of the model, derivatives or outputs solely for personal, scientific or academic, non-profit and non-commercial work. Commercial entities need a separate licence, and redistribution must carry the licence.

## Key numbers

- The card reports no benchmark numbers.
- Third-party, Polish: 69.84 on the Open PL LLM Leaderboard, highest of the models listed, against Llama 3.3 70B at 66.40 and Bielik 11B v3 at 65.93 (from the [[Bielik 11B v3]] report). Polish EQ-Bench is 77.29.
- Third-party, relevance: a Mistral Large 123B reaches the best macro F1 in [[AMC-16K]], 82.46 monolingual and 80.54 crosslingual with few-shot prompts (model release not named in our note of that paper).
- Third-party, filtering: a Mistral Large filter lowers Success@10 from 0.76 to 0.70 but removes most irrelevant candidates in [[Generative-AI Claim Retrieval]].

## Experiments

- **None on the card:** the card runs no evaluation of its own and links no paper.
- **Judge-like use elsewhere:** [[AMC-16K]] (relevance labelling in 20 languages), [[Generative-AI Claim Retrieval]] (filtering and veracity) and Polish leaderboards in the [[Bielik 11B v3]] report.
- **Cross-vendor comparison:** Command A wins 64.9% of Polish mArenaHard comparisons against Mistral Large 2, per the [[Command A]] report.

## Data

- Training data: not described.
- Evaluation data: none on the card; we rely on the third-party evaluations above.

> [!failure] Limitations
> - No documentation of data, benchmarks or cutoff, so we cannot place it on the exposure timeline or check its Polish training share.
> - The Polish claim rests on one sentence of the card and on a leaderboard run by the Bielik authors.
> - The research licence bars commercial use and restricts distribution; labels are "Outputs" and must stay within research purposes.
> - At 245 GB of bf16 weights it needs several GPUs, and 8-bit or 4-bit loading changes its behaviour.
> - Mistral-family models appear in the evaluated set through Bielik's Mistral 7B base, which could produce affinity between judge and judged.

## Relation to our project

- Judge 3, the family that did best in [[AMC-16K]] and in [[Generative-AI Claim Retrieval]]; it forms a disjoint three-family panel with [[gpt-oss-120b]] and [[Command A]] ([[2026-10-27-temporal-retrieval-eval]], [[LLM selection]]).
- Because [[Bielik 11B v3]] derives from Mistral 7B v0.2, Bielik rows also get a leave-Mistral-out score to expose self-preference ([[Self-Preference Bias]]).
- We pin the exact checkpoint (the 2411 revision; AMC-16K does not name its Mistral Large release) and record the Mistral Research License in the results table.
- We release prompts, ids and labels but never post text; because labels are outputs under a research-only licence, we confirm the release terms before publication.
- Validation on the 400 Polish and the English [[AMC-16K]] pairs comes first, with English instructions as the default ([[Language and Retrieval Bias]]).

## Future work

- **Open:** the card states no future work or report; it gives no evaluation to extend (searched 2026-10).
- **Open:** a documented Polish relevance-judging evaluation of the 2411 release, separate from 2407 (searched 2026-10).
