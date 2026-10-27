---
title: "Simulated Ignorance Fails"
aliases: ["Simulated Ignorance Fails: A Systematic Study of LLM Behaviors on Forecasting Problems Before Model Knowledge Cutoff"]
authors: ["Zehan Li", "Yuxuan Wang", "Ali El Lahib", "Ying-Jieh Xia", "Xinyu Pi"]
year: 2026
venue: "Proceedings of the Thirty-Fifth International Joint Conference on Artificial Intelligence (IJCAI-26), Main Track, pages 5837-5845"
arxiv: "2601.13717"
doi: "10.24963/ijcai.2026/650"
url: "https://ijcai.org/proceedings/2026/650"
citekey: li2026simulated
verified: 2026-10-27
theme: "[[LLM Temporal Leakage]]"
tags: [type/paper, theme/llm-leakage, topic/temporal, topic/leakage, topic/llm, topic/evaluation]
---
# Simulated Ignorance Fails

> [!info] TL;DR
> Telling an LLM to use only knowledge from before a date does not make it forecast like a model that truly lacks that knowledge. On resolved Metaculus questions, the cutoff instruction closes only 48% of the gap between pre-cutoff and post-cutoff Brier scores, chain-of-thought does not close the rest, and reasoning-optimised models leak more while producing cleaner reasoning traces. The authors conclude that prompt-based retrospective forecasting on pre-cutoff events is flawed.

## Motivation

- Prospective evaluation is rigorous but slow; retrospective forecasting on resolved events is fast but needs outcomes the model has not seen. Frontier models now have cutoffs in late 2024 or 2025, leaving few clean questions (Paleka et al., 2025 is the cited source).
- Simulated Ignorance (SI) would solve this by prompting the model to forget what it knows; True Ignorance (TI) is a model that genuinely predates the outcome. No earlier work tested whether SI approximates TI.
- Recent benchmarks have quietly moved to prospective-only questions (ForecastBench, FutureSearch's pastcasting benchmark) without justifying it.
- It matters for retrieval evaluation too: retrieval-side leakage is covered in [[Temporal Leakage in Date-Filtered Web Retrieval]], this paper covers the parametric side.

## Method

Notation: model cutoff $K(m)$, question resolution date $R(q)$; the paper's Brier score $B$ is used as is.

**Question partition.** Let $K_{min}$ and $K_{max}$ be the earliest and latest model cutoffs. A question is pre-cutoff if $R(q) < K_{min}$ (every model has seen the outcome) and post-cutoff if $R(q) > K_{max}$ (none has). With a cutoff instruction fixed at 2023-01-01, pre-cutoff questions are the SI condition and post-cutoff ones the TI condition.

**SI-TI gap.** The mean Brier score on post-cutoff questions minus the mean on pre-cutoff questions, per prompting condition.

Intuition: if prompting really hid the outcome, a model would be equally good (or bad) on both sets; any advantage on questions it was told to forget is leaked knowledge.

**Interventions.** A 2x2 design crosses direct answer or chain-of-thought with no cutoff or the cutoff instruction; a third test compares reasoning-optimised models with standard ones. Each model-question pair is run three times and averaged.

## Key numbers

- The cutoff instruction closes 48% of the SI-TI gap and leaves 52% (nine models, direct prompting).
- Gap by domain: instructions close 91% in business questions but 33% in politics and geopolitics.
- Reasoning-optimised models have a larger gap than standard ones: 0.086 against 0.064 (direct, with cutoff) and 0.097 against 0.067 (chain-of-thought, with cutoff).
- Natural experiment on Q4 2024 questions: Brier 0.136 for DeepSeek-V3.2 (SI, cutoff January 2025) against 0.204 for GPT-5.1 (TI, cutoff September 2024).
- Metaculus community forecasters differ by only 0.011 Brier between the two question sets, models by about 0.13.

## Experiments

- **Cutoff instructions:** all nine models still do better on questions they were told to ignore; leakage is largest for high-coverage events such as elections.
- **Chain-of-thought:** without a cutoff instruction it narrows the gap from both sides (worse on pre-cutoff, better on post-cutoff); with the instruction it changes little. Traces become cleaner, reaching about 99% cutoff compliance, yet the gap remains, so clean reasoning does not show clean knowledge.
- **Reasoning-optimised models:** GPT-5.1, Gemini-2.5-Pro and DeepSeek-R1 give the cleanest traces (logic 99.4%, cutoff-clean 98.8%) and the largest gaps; the authors suggest training rewards compliant-looking reasoning that leads to a memorised answer.
- **Difficulty controls:** each model's Brier score jumps at its own cutoff, not at a common calendar date; the cross-model Q4 2024 comparison holds the questions fixed, and the human baseline shows the two sets are equally hard.
- **Trace audit:** an automated audit agrees with humans on 36 traces (94%; kappa 0.86 for cutoff compliance, 0.64 for logic).
- **Case studies:** the same Fermi-style reasoning on a pre-cutoff NATO question gives a perfect score by recalling ratification dates, but fails on a structurally identical post-cutoff question.

## Data

- 470 resolved binary Metaculus questions from 2023 to 2025 across six domains (the arXiv abstract says 477, the setup section and the IJCAI abstract say 470); 201 pre-cutoff and about 274 post-cutoff per model.
- Nine models: six standard (Claude 3.5 Sonnet, Gemini-2.5-Flash, Llama 4 Maverick, DeepSeek-V3.2-Exp, two gpt-oss sizes) and three reasoning-optimised, with cutoffs from April 2024 to January 2025.

> [!failure] Limitations
> - Residual difficulty differences between the two question sets cannot be fully excluded, though the controls argue against them.
> - Trace audits miss subtle leakage in wording or framing.
> - Only prompt-based interventions; machine unlearning or time-partitioned models are not tested.
> - Metaculus questions only; no retrieval, fact-checking or ranking metrics.
> - Read from the arXiv v1 full text; the published IJCAI text was not compared line by line.

## Relation to our project

- Rules out prompting an LLM reranker to "pretend it is date $t$": parametric leakage is handled by stratifying queries by model cutoff (RQ5 in [[Proposed Task]]), as in the post-cutoff versus pre-cutoff split here ([[Enhanced topic research]]).
- The domain finding suggests high-salience claims (elections, wars) are the most exposed to memorised verdicts, so our strata should be reported per topic ([[LLM Temporal Leakage]]).
- Pair with [[All Leaks Count]], which measures leakage in stated reasoning but also cannot see silent use of knowledge.

## Future work

- **Open:** parameter-level approaches such as unlearning as a way to reach True Ignorance (searched 2026-10).
- **Open:** domains beyond forecasting, including retrieval and reranking with LLMs (searched 2026-10).
- **Partly done:** claim-level auditing of what drives a prediction; [Zhang and Stadie, 2026](https://aclanthology.org/2026.findings-emnlp.1690/) ([[All Leaks Count]]).
