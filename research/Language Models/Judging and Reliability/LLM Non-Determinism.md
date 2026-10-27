---
title: "LLM Non-Determinism"
aliases: ["Non-Determinism of \"Deterministic\" LLM Settings"]
authors: ["Berk Atil", "Sarp Aykent", "Alexa Chittams", "Lisheng Fu", "Rebecca J. Passonneau", "Evan Radcliffe", "Guru Rajan Rajagopal", "Adam Sloan", "Tomasz Tudrej", "Ferhan Ture", "Zhe Wu", "Lixinyu Xu", "Breck Baldwin"]
year: 2024
venue: "arXiv preprint (v5, April 2025); workshop version at EVAL4NLP 2025, pages 135-148"
arxiv: "2408.04667"
url: "https://arxiv.org/abs/2408.04667"
citekey: atil2024non
verified: 2026-10-27
theme: "[[Judging and Reliability]]"
related: ["[[2026-10-27-temporal-retrieval-eval]]", "[[LLM selection]]", "[[ChatGPT Behavior Drift]]"]
tags: [type/paper, theme/llm-judging, topic/reproducibility, topic/evaluation, topic/llm, topic/english]
---
# LLM Non-Determinism

> [!info] TL;DR
> Setting temperature to 0, top-p to 1 and a fixed seed does not make hosted LLMs repeatable. Across five models, eight tasks and ten runs, accuracy varies by up to 15% between runs, and the gap between best-case and worst-case accuracy reaches 70%. Raw outputs rarely match exactly, and parsed answers are more stable but still not identical.

## Motivation

- Benchmarks report one number per model, which assumes repeated runs give the same result.
- Practitioners notice variation at "deterministic" settings, but it had not been quantified across models, tasks and prompting modes.
- Earlier studies of sampling variance use temperature 1 and so do not isolate the setting that evaluations rely on.
- For judges, a label that changes between identical calls adds noise to every downstream metric ([[ChatGPT Behavior Drift]]).

## Method

Notation: for each condition (model, task, prompting mode), N identical runs are made and compared question by question.

**Total agreement rate.** TARr@N is the share of questions whose raw output strings are identical in all N runs. TARa@N is the same for parsed answers.

**Best and worst accuracy.** BestAcc counts a question correct if any run answers it correctly, and WorstAcc counts it correct only if every run does.

Intuition: the gap between BestAcc and WorstAcc is the range of scores one could report by choosing a run.

The authors also report median accuracy and the maximum-minimum accuracy over runs, because accuracy is not normally distributed.

## Key numbers

- Accuracy varies by up to 15% across natural runs, and BestAcc minus WorstAcc reaches 70% in some conditions.
- Mixtral-8x7B on college math: best 75.0%, worst 3.0%, a 72-point range.
- GPT-4o few-shot on college math: TARr@10 is 0.0% and TARa@10 50.0%.
- Longer outputs are less stable; in few-shot settings higher median accuracy goes with higher TARa@10.

## Experiments

- **Main grid:** five models, eight tasks and two prompting modes give 80 conditions of ten runs each; no model is repeatable across all tasks.
- **Raw versus parsed:** string agreement is much lower than answer agreement, which affects any downstream parser.
- **Normality:** 20 runs of GPT-4o and Llama-3-70B on college math are non-normal (Kolmogorov-Smirnov $p<10^{-9}$), so means and standard deviations mislead.
- **Local control:** Llama-3-8B on local GPUs without serving optimisations gave deterministic results, pointing to batching and serving, not the weights.
- **Correlations:** output length correlates negatively with agreement, and fine-tuning GPT-3.5 reduced instability in a two-fold test.

## Data

- Four BIG-Bench Hard tasks (navigation, ruin names, geometric shapes, logical deduction) with 250 questions each.
- Four MMLU tasks: high-school European history (165), college mathematics (100), professional accounting (282), public relations (110).
- Models: GPT-3.5 Turbo, GPT-4o, Llama-3-70B-Instruct, Llama-3-8B-Instruct and Mixtral-8x7B-Instruct.

> [!failure] Limitations
> - Multiple-choice tasks only, with hand-built answer extraction that limits generality.
> - Closed APIs prevent identifying the cause, so batching or hardware explanations remain speculative.
> - Ten runs per condition and a zero-shot or few-shot prompt, without chain-of-thought.
> - Does not test relevance judging or ranking tasks.

## Relation to our project

- It sets the reporting rule for judges and rerankers: temperature 0, a fixed seed, pinned open weights and cached outputs, plus a repeat on a sample ([[LLM selection]]; [[2026-10-27-temporal-retrieval-eval|Project plan]]).
- We report a flip rate, the share of items whose label changes across repeated calls, alongside TARa-style agreement and the max-minus-min metric per judge.
- Judge outputs are limited to a single label token, since shorter outputs were more stable and parsing brittleness disappears.
- Serving settings (batch size, engine version) are recorded because the local no-optimisation run was deterministic, and drift between snapshots is treated separately ([[ChatGPT Behavior Drift]]).

## Future work

- **Done:** an extension to hosted environments and system settings; the same authors' workshop version at [EVAL4NLP 2025](https://aclanthology.org/2025.eval4nlp-1.12/).
- **Open:** methods that reduce instability at training or inference time, such as constrained single-letter answers (searched 2026-10).
- **Open:** whether instability correlates with specific error types such as false positives and false negatives in judging (searched 2026-10).
