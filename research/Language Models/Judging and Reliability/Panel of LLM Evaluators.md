---
title: "Panel of LLM Evaluators"
aliases: ["Replacing Judges with Juries: Evaluating LLM Generations with a Panel of Diverse Models"]
authors: ["Pat Verga", "Sebastian Hofstätter", "Sophia Althammer", "Yixuan Su", "Aleksandra Piktus", "Arkady Arkhangorodsky", "Minjie Xu", "Naomi White", "Patrick Lewis"]
year: 2024
venue: "arXiv preprint"
arxiv: "2404.18796"
url: "https://arxiv.org/abs/2404.18796"
citekey: verga2024replacing
verified: 2026-10-27
theme: "[[Judging and Reliability]]"
related: ["[[2026-10-27-temporal-retrieval-eval]]", "[[LLM selection]]", "[[Self-Preference Bias]]", "[[Rubric Self-Preference]]", "[[LLM Judges Favour LLM Rankers]]"]
tags: [type/paper, theme/llm-judging, topic/judge-bias, topic/evaluation, topic/llm, topic/english]
---
# Panel of LLM Evaluators

> [!info] TL;DR
> Instead of one large judge such as GPT-4, the paper pools verdicts from three smaller models of three different families (Command R, Claude 3 Haiku, GPT-3.5). This panel (PoLL) agrees better with human labels on QA and with Chatbot Arena rankings, shows less spread between judged models, and costs seven to eight times less than a GPT-4 Turbo judge.

## Motivation

- Evaluating free-form generation is hard, and string matching misses valid answers such as other date formats.
- Single-model judges show intra-model bias and prefer their own outputs ([Panickssery et al., 2024](https://arxiv.org/abs/2404.13076); [[Self-Preference Bias]]).
- The most capable judge is usually chosen, which is slow and costly, and it is unclear that size is needed.

## Method

Notation: judge $j$ scores an answer $a$, with a reference $r$ in QA or a rival output in pairwise settings, and a panel $P$ pools the scores with a voting function $f$.

**Panel score.** Each member scores independently and the final score is $f(\{j(a) : j \in P\})$. QA uses max voting over binary verdicts, and Arena Hard uses average pooling over 1 to 5 scores because three judges often lack a majority.

**Composition.** One model per family: Command R (35B), Claude 3 Haiku and GPT-3.5. Mistral Large and Mistral Medium outputs are judged as unaffiliated generators.

Intuition: biases of different families point in different directions, so pooling cancels part of them, as pooling human annotators does.

## Key numbers

- Cohen's $\kappa$ with humans on Natural Questions: PoLL 0.763 against GPT-4 0.627; on TriviaQA 0.906 against 0.841; on HotpotQA 0.867 against 0.830 (Haiku alone 0.873).
- Chatbot Arena Hard: PoLL has Pearson 0.917 and Kendall $\tau$ 0.778 with the Arena ranking, GPT-4 0.817 and 0.667.
- On multi-hop QA, the spread of judge-minus-human accuracy has standard deviation 2.2 for PoLL and 6.1 for GPT-3.5.
- Cost per million tokens: PoLL $1.25 input and $4.25 output against $10 and $30 for GPT-4 Turbo, 7 to 8 times cheaper.

## Experiments

- **Agreement with humans:** single-hop QA on KILT with a Cohere annotator workforce as reference; PoLL is best or near best, and GPT-4 is among the weakest in this reference-based setup.
- **Arena ranking:** the GPT-4 judge ranks another GPT-4 variant second against a true position of four; PoLL tracks the top of the ranking better.
- **Prompt sensitivity:** GPT-4 kappa on NQ moves from 0.518 zero-shot to 0.627 few-shot and 0.725 with a "do not overthink" line, still below PoLL.
- **Bias and consistency:** on HotpotQA and Bamboogle, the largest positive deviation from human accuracy for each model occurs when it judges itself.

## Data

- KILT Natural Questions, TriviaQA and HotpotQA for single-hop QA; HotpotQA and Bamboogle for multi-hop QA.
- Chatbot Arena Hard: 500 hard prompts, with Chatbot Arena crowd ratings as ground truth.
- Human labels: Cohere annotators judged whether the reference answer is contained in the generated answer.

> [!failure] Limitations
> - Only three settings, three judges and one panel composition; math and reasoning evaluation are not tested.
> - Panel selection, meaning which models to include for quality and cost, is left to future work.
> - Prices are those at the time of writing, and GPT-4 judge weakness in QA partly reflects prompt choice.
> - Later work finds ensembling lowers self-preference without removing it ([[Rubric Self-Preference]]).

## Relation to our project

- It is the template for the three-family judge panel in [[LLM selection]], where the panel must also be disjoint from all evaluated and pooled systems ([[2026-10-27-temporal-retrieval-eval|Project plan]]).
- Judgments are binary, so we pre-register the vote rule and report both majority and any-judge aggregation, plus a leave-one-judge-out rerun.
- Prompt sensitivity of a single judge supports fixing and releasing prompts before labelling.
- The cost result supports small open-weight judges over one large model on local GPUs.
- Panel agreement is validated against humans per language, using [[AMC-16K]] for Polish; bias in a panel shared with evaluated systems is still possible ([[LLM Judges Favour LLM Rankers]]).

## Future work

- **Partly done:** panel selection and the remaining bias; [Pombal et al., 2026](https://arxiv.org/abs/2604.06996) find committee members' quality matters more than family diversity ([[Rubric Self-Preference]]).
- **Open:** panels for math and reasoning evaluation, as the authors note (searched 2026-10).
- **Open:** a relevance-judging evaluation of panels in a language such as Polish against human labels (searched 2026-10).
