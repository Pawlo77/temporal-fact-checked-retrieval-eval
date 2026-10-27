---
title: "ChatGPT Behavior Drift"
aliases: ["How Is ChatGPT’s Behavior Changing Over Time?"]
authors: ["Lingjiao Chen", "Matei Zaharia", "James Zou"]
year: 2024
venue: "Harvard Data Science Review 6(2)"
doi: "10.1162/99608f92.5317da47"
url: "https://doi.org/10.1162/99608f92.5317da47"
citekey: chen2024chatgpt
verified: 2026-10-27
theme: "[[Judging and Reliability]]"
related: ["[[2026-10-27-temporal-retrieval-eval]]", "[[LLM selection]]", "[[LLM Non-Determinism]]"]
tags: [type/paper, theme/llm-judging, topic/reproducibility, topic/evaluation, topic/llm, topic/english]
---
# ChatGPT Behavior Drift

> [!info] TL;DR
> The paper compares the March 2023 and June 2023 snapshots of GPT-3.5 and GPT-4 on eight tasks and finds large changes in the same named service. GPT-4 prime identification falls from 84.0% to 51.1% accuracy, while GPT-3.5 rises from 49.6% to 76.2%. Much of the decline traces to GPT-4 following user instructions less, so a pipeline can break without warning.

## Motivation

- Providers update hosted models without saying when or how, which makes results from the "same" model hard to reproduce.
- Earlier monitoring reported small shifts, mostly below 5% on common benchmarks, and focused on simple classification services.
- Updates that improve one skill may harm another, so whether a service improves uniformly is an open question.

## Method

Notation: the paper compares two snapshots of a service on the same prompts, with a main metric per task plus verbosity and answer mismatch.

**Mismatch.** For each prompt, the share of cases where the extracted answers of the two snapshots differ; reasoning text may differ without counting.

Intuition: mismatch measures changed behaviour even when accuracy stays level because new errors replace old ones.

**Instruction-following probe.** A task-agnostic set of instructions (answer in brackets, no apologies, writing constraints, formatting, and composites of two) separates fidelity to instructions from task skill.

Queries use only the user prompt, with the default system prompt and temperature 0.1.

## Key numbers

- Prime vs composite (1,000 questions): GPT-4 accuracy 84.0% to 51.1%; GPT-3.5 49.6% to 76.2%.
- Happy numbers: GPT-4 83.6% to 35.2%; chain-of-thought gain for GPT-4 falls from 56.6 to 3.2 points.
- OpinionQA response rate of GPT-4 falls from 97.6% to 22.1%; directly executable code from 52% to 10%.
- GPT-4 follows the answer-extraction instruction in 99.5% of cases in March and 0.5% in June.

## Experiments

- **Math:** the June GPT-4 skips the requested step-by-step reasoning and answers "composite" almost always; GPT-3.5 improves.
- **Sensitive questions:** GPT-4 answers 21.0% in March and 5.0% in June, with shorter refusals; a jailbreak prompt succeeds 78.0% then 31.0%.
- **Opinion survey:** 27% of GPT-3.5 opinions change between snapshots, against 2.8% and 7.0% when the same snapshot is run twice.
- **Code:** June outputs add markdown fences, so fewer are directly executable; removing them restores GPT-4 to 70%.
- **Multi-hop agent, USMLE, visual reasoning:** GPT-4 exact match on HotpotQA rises from 1.2% to 37.8%; USMLE accuracy moves from 86.6% to 82.4%; ARC exact match changes by about 2 points.

## Data

- Prime and composite numbers, 500 happy-number queries, 100 sensitive questions, OpinionQA with 1,506 questions.
- A LangChain HotpotQA agent, 50 recent LeetCode easy problems, USMLE questions, and 467 ARC samples.
- 200 recent arXiv abstracts and further sets for instruction-following checks.

> [!failure] Limitations
> - Two snapshots and tasks that the authors call non-exhaustive, so drift is demonstrated but not characterised over time.
> - The cause is not identified; the instruction-following explanation is partial and GPT-3.5 shows no consistent trend.
> - Sensitive-question answers were labelled by hand, and the temperature of 0.1 leaves some randomness.
> - Closed models only, so internal changes are unobservable.

## Relation to our project

- It is why judges and rerankers are pinned open weights with commit hashes, and API models appear only as a dated ceiling row ([[LLM selection]]; [[2026-10-27-temporal-retrieval-eval|Project plan]]).
- The same-snapshot rerun baseline in the opinion experiment is our template: separate drift from run-to-run noise before blaming the model.
- Format compliance is checked on every judge output, since June GPT-4 broke code and parsing without a change in the prompt.
- Cached responses and released prompts let a later reader reproduce each label ([[LLM Non-Determinism]]).

## Future work

- **Open:** a long-running study of drift across more tasks and providers, which the authors announce as ongoing (searched 2026-10).
- **Open:** drift of LLM judges specifically, meaning whether relevance labels from a hosted judge change across snapshots (searched 2026-10).
