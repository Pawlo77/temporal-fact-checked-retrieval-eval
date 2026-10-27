---
title: "TripleFact"
aliases: ["TripleFact: Defending Data Contamination in the Evaluation of LLM-driven Fake News Detection"]
authors: ["Cheng Xu", "Nan Yan"]
year: 2025
venue: "Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pages 8808-8823"
doi: "10.18653/v1/2025.acl-long.431"
url: "https://aclanthology.org/2025.acl-long.431/"
citekey: xu2025triplefact
verified: 2026-10-27
theme: "[[LLM Temporal Leakage]]"
tags: [type/paper, theme/llm-leakage, topic/temporal, topic/leakage, topic/llm, topic/evaluation]
---
# TripleFact

> [!info] TL;DR
> TripleFact is an evaluation framework for LLM fake news detection that tries to resist benchmark contamination. It combines human-written adversarial claims, claims collected live and labelled days later, and a test with real entities swapped for fictional ones. In a controlled injection of contamination into one model, a component score rose by 0.23 while the composite score stayed within 0.49 to 0.57.

## Motivation

- LLMs are pretrained on trillions of tokens, so test claims, labels or related text may already be known; zero-shot evaluation then rewards memory.
- Fake news is called especially exposed because claims are time-sensitive and models store false claims as well as true ones; the paper's example is a debunked conspiracy theory recognised from training text.
- Static sets such as LIAR assume test data is unseen. The paper cites fresh-question benchmarks (LatestEval) and post-hoc correction as partial answers, both with costs.
- Our concern is the same one on the retrieval side: a pool of fact-check articles is public text a model may have read ([[Simulated Ignorance Fails]], [[Dated Data]]).

## Method

Notation: the paper's own symbols are kept (no query or pool objects appear in this classification task).

**HAPT (human-adversarial preference testing).** People write real and fake stories; the target LLM classifies each zero-shot and the F1 is the component output $O_{HAPT}$.

**RTW-AV (real-time web agent with asynchronous validation).** An agent collects claims from live social media topics and retrieves web pages as context. Ground truth is attached days later from fact-checking consensus such as Snopes or PolitiFact. Time-Delayed Accuracy (TDA) is the share of correct classifications after validation; Context Utilization Score (CUS) is the share of answers citing at least three sources. $O_{RTW\text{-}AV} = \text{CUS} \times \text{TDA}$.

**ECVE (entity-controlled virtual environment).** Named entities in an existing benchmark are replaced by fictional ones, for example a real vaccine maker by an invented name. Entity-Independent Accuracy (EIA) is accuracy on modified claims; the Bias Reduction Ratio is $\text{BRR} = \text{EIA} - \text{OAUC}$, with OAUC the accuracy on original claims.

**Score.** $\text{TFS} = (1 + \text{BRR}) \cdot \frac{O_{HAPT} + O_{RTW\text{-}AV}}{2}$.

Intuition: a model that answers differently once a famous name is replaced was using memory of the name, so its score is scaled down.

## Key numbers

- o1-preview scores highest, TFS 0.788 (17 models, three families); gpt-3.5-turbo-0125 is 0.516 and Llama-3.2-1B 0.258.
- Injecting label-level contamination (test items with labels added to fine-tuning) into gpt-4o-mini raises $O_{RTW\text{-}AV}$ from 0.62 to 0.85 and $O_{HAPT}$ from 0.40 to 0.52 at full intensity.
- Under that injection BRR falls to -0.18 and TFS stays between 0.49 and 0.57 against a 0.53 baseline.
- The abstract's "up to 23%" is this 0.62 to 0.85 rise in one fine-tuned model, not a measured inflation of the 17 evaluated models.

## Experiments

- **Evaluation of 17 LLMs:** GPT, Llama and DeepSeek models evaluated with all three components; larger and newer models score higher, and most models have negative BRR, read by the authors as entity reliance.
- **Contamination injection:** gpt-4o-mini is fine-tuned on four kinds of contamination (semantic, information, data, label) at 10%, 30%, 50% and 100% intensity; label-level contamination inflates the first two components most, and BRR penalises it.
- **Cost:** the paper lists API cost per experiment; o1-preview is the most expensive, at about $278 for RTW-AV and $407 for ECVE.

## Data

- HAPT: 100 real and 100 fake stories written by the authors in the style of PolitiFact, standing in for crowdsourcing.
- RTW-AV: tweets captured every 6 hours for 7 days via the X API, 100 each from Top and Latest per topic; gpt-4o-mini turned them into 157 statements, matched with 1,570 retrieved pages.
- ECVE: the LIAR2 test set, with entities replaced by gpt-4o-mini.
- Models: 17 GPT, Llama and DeepSeek models; stated cutoffs are 09/2021 for gpt-3.5-turbo, 03/2023 for Llama-3-8B and 10/2023 to 12/2023 for most others; DeepSeek states none.

> [!failure] Limitations
> - Human-written claims were produced by the authors, not crowdsourced; scale and cultural consistency are untested.
> - Entity replacement can change claim meaning, and RTW-AV labels depend on fact-check consensus that may lag.
> - English only; low-resource languages are untested, and the live X and PolitiFact data cannot be redistributed.
> - Contamination is simulated by fine-tuning one small model, not found in real pretraining data; the stability claim rests on that one setting.
> - The composite mixes quantities (F1, accuracy, a ratio), so a stable total can hide components that move in opposite directions.

## Relation to our project

- It states the risk in the register: contamination can inflate LLM fact-checking scores, so pretrained models may know fact-check sites ([[LLM selection]], [[2026-10-27-temporal-retrieval-eval|Project plan]]).
- Cite the "up to 23%" figure only with its setting: fine-tuning injection into one model, not the 17 evaluated LLMs.
- We take the live-then-label idea: queries newer than a model's cutoff are contamination-free for that model, which is the post-cutoff stratum of RQ5.
- ECVE-style entity swaps give a cheap test on a sample of our posts: if a reranker's ranking changes when named entities are masked, memory is involved. We would have to design it.
- Pairs with [[Dated Data]] for the cutoff boundary and [[Simulated Ignorance Fails]] for prompting limits.

## Future work

- **Open:** multilingual and multimodal extensions, named by the paper (searched 2026-10).
- **Open:** validation on contamination found in real pretraining corpora instead of injected by fine-tuning (searched 2026-10).
- **Open:** applying contamination-aware evaluation to retrieval and reranking of fact-checks (searched 2026-10).
