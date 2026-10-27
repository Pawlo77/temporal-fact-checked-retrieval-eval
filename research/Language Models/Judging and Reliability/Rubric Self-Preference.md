---
title: "Rubric Self-Preference"
aliases: ["Self-Preference Bias in Rubric-Based Evaluation of Large Language Models"]
authors: ["José Pombal", "Ricardo Rei", "André F. T. Martins"]
year: 2026
venue: "Conference on Language Modeling (COLM 2026); arXiv v3, August 2026"
arxiv: "2604.06996"
url: "https://arxiv.org/abs/2604.06996"
citekey: pombal2026self
verified: 2026-10-27
theme: "[[Judging and Reliability]]"
related: ["[[2026-10-27-temporal-retrieval-eval]]", "[[LLM selection]]", "[[Self-Preference Bias]]", "[[Panel of LLM Evaluators]]", "[[AMC-16K]]"]
tags: [type/paper, theme/llm-judging, topic/judge-bias, topic/evaluation, topic/llm, topic/english]
---
# Rubric Self-Preference

> [!info] TL;DR
> Self-preference bias persists when judges give binary verdicts on individual criteria, even for objective, programmatically checkable rubrics. Among criteria a generator fails, judges can be more than 50% more likely to pass them when the output is their own. Ensembling judges reduces the bias without removing it, and on a medical chat benchmark it moves model scores by up to 10 points.

## Motivation

- Judges favour their own outputs or their family's in pairwise and direct-scoring settings ([[Self-Preference Bias]]; [[Panel of LLM Evaluators]]).
- Rubric-based evaluation, with a binary verdict per criterion, is spreading in benchmarks and reward modeling, and might be less exposed because it avoids ordering and score calibration issues.
- Nobody had measured it, and real rubrics are subjective, which confounds bias with disagreement.

## Method

Notation: judge $J$, generator $G$, and overestimation rate $O(J,G)$, the share of ground-truth failures that $J$ wrongly marks as passed for outputs of $G$.

**HSPP ratio.** The Harmful Self-Preference Propensity ratio is $O(J,J)$ divided by the mean of $O(J,G)$ over generators that are neither $J$ nor in its family. A value of 1 means no self-preference.

Intuition: the ratio compares how lenient a judge is to itself with how lenient it is to unrelated models, so general leniency cancels.

**Family variant.** The same ratio for same-family generators other than $J$ isolates family effects.

**Paradigms.** Single-rubric, all-rubrics, direct assessment and pairwise comparison are compared with instance-level and rubric-level accuracy, and 95% bootstrap intervals with 1000 resamples.

## Key numbers

- On LiveCodeBench the rubric-level self ratio is 20.15 for GPT-5 and 5.97 for GPT-oss-120B, against Qwen 235B at 0.83.
- On IFEval nearly all judges have ratios above 1, but only two are significant.
- On HealthBench, GPT-5 gives itself a bonus of about 4 points on a 100-point scale, and Gemma 4B overestimates itself by 10.90 points.
- Within difficulty bins GPT-5's ratio stays at 13.74 and 14.66 in the two hardest bins, so capability does not explain it.

## Experiments

- **Objective rubrics:** IFEval and LiveCodeBench, converted to binary rubrics with exact ground truth; judges favour themselves and their family, more strongly in pairwise comparison than in rubric or direct scoring.
- **Ensembling:** a majority vote of the five largest family judges has equal or higher accuracy and lower bias, but not zero; judge quality matters most and family diversity less.
- **Agreement filter:** dropping rubrics where judges disagree lowers the measured bias.
- **Capability control:** stratifying by how hard an output is to judge keeps the ratio high for GPT-5, GPT-oss-120B and Claude Sonnet; reasoning effort does not reduce it.
- **Subjective rubrics:** a mixed-effects logistic regression on HealthBench finds negative rubrics and communication, global health and emergency referral themes amplify self-preference, while instruction-following rubrics do not.

## Data

- IFEval: 541 prompts with verifiable instructions.
- LiveCodeBench: 177 problems after 2025-01-04, with 5,685 unit tests used as rubrics.
- HealthBench: 5,000 instances and 48,562 unique rubrics, with a majority vote of five judges as the reference.
- Twelve models as judges and generators: Gemma 3, Llama 4, Qwen 3, GPT-5, GPT-oss-120B and two Claude 4.5 models.

> [!failure] Limitations
> - HealthBench has no ground truth, so the reference is an ensemble; the authors note this underestimates the bias.
> - Closed models are run only in the single-rubric setting for cost.
> - Relatedness beyond a named family, such as distillation, is not measured.
> - It tests detection and mitigation by ensembling and filtering only, with no debiasing method.

## Relation to our project

- A relevance label is a binary verdict on a criterion, so the findings apply directly: judge families must be disjoint from every evaluated and pooled system, and "relatives" count ([[LLM selection]]).
- Distillation and shared data blur family lines, so we state each panel member's lineage and rerun with each judge left out ([[2026-10-27-temporal-retrieval-eval|Project plan]]).
- The panel cuts bias but does not remove it, which is why expanded qrels stay a bound and humans label a stratified sample.
- The overestimation it measures is a false positive on failed criteria, the same error as topic-only false relevance in [[AMC-16K]]; we report judge precision on same-topic negatives.
- Inter-judge disagreement is used to flag pairs for human audit; panel members must be strong judges, not just diverse ones.

## Future work

- **Open:** extension to reward modeling pipelines, where the authors expect faster reward hacking (searched 2026-10).
- **Open:** a definition and measure of relatedness between models, which the authors call open (searched 2026-10).
- **Open:** inference-time debiasing or training-time corrections that remove the bias, which ensembling does not (searched 2026-10).
