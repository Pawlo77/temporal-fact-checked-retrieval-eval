---
title: "LLM Relevance Judgments Can Be Gamed"
aliases: ["LLM-based relevance assessment still can't replace human relevance assessment"]
authors: ["Charles L. A. Clarke", "Laura Dietz"]
year: 2024
venue: "arXiv preprint (v3, January 2026)"
arxiv: "2412.17156"
url: "https://arxiv.org/abs/2412.17156"
citekey: clarke2024llm
verified: 2026-10-27
theme: "[[Judging and Reliability]]"
related: ["[[2026-10-27-temporal-retrieval-eval]]", "[[LLM selection]]", "[[LLM Judges Favour LLM Rankers]]", "[[Self-Preference Bias]]"]
tags: [type/paper, theme/llm-judging, topic/judge-bias, topic/evaluation, topic/reranking, topic/english]
---
# LLM Relevance Judgments Can Be Gamed

> [!info] TL;DR
> The paper argues that an LLM relevance assessor is a ranking method, not a gold standard. On TREC RAG 2024, agreement between the Umbrela judge and humans drops from 0.89 over all systems to 0.51 among the top 20. A run built from LLM judgments ranks fifth under the judge and 28th under humans, and reranking every system with the judge gives near-perfect judged scores that humans do not share.

## Motivation

- [Upadhyay et al., 2024](https://arxiv.org/abs/2411.08275) report Kendall's $\tau$ of 0.89 on TREC RAG 2024 and conclude LLM judgments can replace manual ones.
- Earlier cautions about circularity (LLMs judging LLM outputs) and that "LLMs are not people" were not answered by that study.
- Test collections are reused to compare future systems, which will increasingly contain LLM relevance components.
- Related findings on bias towards LLM rankers ([[LLM Judges Favour LLM Rankers]]) and narcissistic evaluators ([[Self-Preference Bias]]) suggest the judge favours systems that resemble it.

## Method

Notation: the paper's judge Umbrela assigns relevance grades to passages, and system quality is NDCG computed with those grades (automatic) or with human grades (manual).

**Top-of-leaderboard agreement.** $\tau$ is recomputed after removing weak systems, because poor systems are easy to separate and inflate the correlation.

**Subversion.** A run is built to exploit the judge: pool the top 20 of 15 preliminary runs, label them with GPT-4o, run pairwise LLM preference judgments on top-graded passages, and sort by those preferences.

**Circularity simulation.** Every submitted run is reranked by the track's Umbrela grades, then scored again with the same grades.

Intuition: a measuring tool that anyone may also use as a reranker will be optimised against, and then it stops measuring.

## Key numbers

- Kendall's $\tau$ between manual and Umbrela: 0.89 over 75 systems, 0.84 over the top 60 (about 8% swapped pairs), 0.51 over the top 20 (24%), 0.56 over the top 15 (21%).
- The subversion run uwc1 is fifth under automatic and 28th under manual evaluation.
- After Umbrela reranking of all runs, $\tau$ falls to 0.63 over the top 60, 0.44 (top 20), 0.38 (top 10) and -0.40 (top 5).
- Twelve reranked systems exceed 0.95 NDCG under the judge but score 0.68 to 0.72 under humans.

## Experiments

- **Reproduction:** Umbrela results broadly reproduced, with outliers such as one system scoring 0.81 automatically and 0.63 manually.
- **Top-system differences:** the best automatic system would be fifth by manual labels, and the best manual system sixth by automatic labels.
- **uwc1 versus uwc2:** uwc1 pools many runs and judges them with an LLM; uwc2 reranks the baseline with an LLM prompt, rising from ninth to fourth under manual and seventh to third under automatic assessment.
- **Circular evaluation:** reranking with the judge raises human-scored quality for every system, so the tool is a strong ranker, and judging the result with it inflates scores.

## Data

- TREC 2024 RAG track retrieval task: 301 queries, MS MARCO Segment V2.1, 75 submitted runs of 100 passages each.
- Only 27 queries had manual judgments in the original comparison, and the Upadhyay data was shared with the authors in limited form.

> [!failure] Limitations
> - One judge (Umbrela), one collection and one simulation using organiser labels, so the size of the effect elsewhere is untested.
> - No error bars on the original comparison, so part of the top-system disagreement may be noise.
> - The central argument about gold standards is conceptual and not an experiment.
> - The predicted decay as developers tune to LLM metrics is a forecast.

## Relation to our project

- It is the reason expanded qrels are only a bound: labels for sibling fact-checks come from pooling our own systems and judging them with an LLM panel ([[LLM selection]]; [[2026-10-27-temporal-retrieval-eval|Project plan]]).
- We report every system on fact-checker-only qrels and on expanded qrels, and stratify humans' labels per pooled system.
- Agreement is reported on the top systems as well as overall, since the all-system value hides the loss.
- The judge model is never used as a reranker, and judge families stay disjoint from systems ([[LLM Judges Favour LLM Rankers]]).

## Future work

- **Open:** safeguards against feedback loops in reusable collections, such as hidden judge prompts or held-out judges (searched 2026-10).
- **Open:** a measure of the gap between judged and human scores for systems that contain a judge component (searched 2026-10).
- **Partly done:** measuring how much LLM judges agree on top systems with panels; [Verga et al., 2024](https://arxiv.org/abs/2404.18796) test panels on QA and chat ([[Panel of LLM Evaluators]]).
