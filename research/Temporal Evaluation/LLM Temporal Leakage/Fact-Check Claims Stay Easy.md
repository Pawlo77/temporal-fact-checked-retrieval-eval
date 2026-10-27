---
title: "Fact-Check Claims Stay Easy"
aliases: ["Real-time Factuality Assessment from Adversarial Feedback"]
authors: ["Sanxing Chen", "Yukun Huang", "Bhuwan Dhingra"]
year: 2025
venue: "arXiv preprint arXiv:2410.14651 (v3, 27 July 2025)"
arxiv: "2410.14651"
url: "https://arxiv.org/abs/2410.14651"
citekey: chen2025real
verified: 2026-10-27
theme: "[[LLM Temporal Leakage]]"
tags: [type/paper, theme/llm-leakage, topic/temporal, topic/leakage, topic/llm, topic/evaluation]
---
# Fact-Check Claims Stay Easy

> [!info] TL;DR
> Claims from PolitiFact and Snopes stay easy for LLM detectors even after the models' knowledge cutoffs: PolitiFact through shallow patterns, Snopes because search retrieval restores near-perfect scores. The authors build a harder real-time set by rewriting fresh news into fake variants, iterating against a retrieval-augmented GPT-4o detector. That cuts its ROC-AUC by 17.5 points.

## Motivation

- Fake news benchmarks usually come from fact-checking sites such as PolitiFact and Snopes (the LIAR dataset is the paper's example); their popular claims are likely in pretraining and retrieval corpora.
- Fresh fact-checks avoid pretraining contamination but can leak the label through retrieval, since a model may copy a retrieved verdict, and publishers pick which claims to check.
- Earlier LLM-written fake news is not hard for strong detectors, and one-round generation does not use detector feedback.
- This note's concern is the first point: whether a fact-check-site claim after a cutoff is a clean test.

## Method

Notation: a news item $x$, plausibility score $g(x \mid c)$ from a detector given retrieved context $c$; the paper's symbols are kept.

**Detector.** An LLM scores plausibility from 1 to 10 zero-shot, with the prompt stating the date as March 26, 2024 and that the item is unseen; scores are averaged over samples and rescaled. The metric is ROC-AUC. Retrieval is either an in-house corpus of 811k March 2024 articles with a DPR retriever or Google search, five documents each.

**Adversarial rewrite.** For each true story, GPT-4o writes eight fake candidates; an LLM contradiction check and an edit limit (over 60% token overlap) filter them. The detector ranks the rest, and the most plausible candidate plus the detector's rationale feeds the next round, for six rounds after a direct-rewrite round 0.

$\hat f_i = \arg\max_{f_{ij}} g(f_{ij} \mid c)$.

Intuition: the generator learns from the explanations a fact-checker would give, so it keeps the errors the detector fails to notice.

## Key numbers

- Final-round GPT-4o with the news retriever: AUC falls from 82.4 to 64.9, a 17.5-point drop; with no retrieval it is 58.5 first round and 48.8 last, below chance.
- Retrieval-free detectors on the new set sit at 48.8 to 54.0 in the last round; on earlier LLM fake news they scored 64.5 to 91.3.
- Google retrieval restores last-round GPT-4o to 86.1 and Llama 3.1 405B to 86.6.
- Dataset: 402 true and 402 fake items; humans with Google reached 99% on 100 checked pairs.

## Experiments

- **PolitiFact over time:** 9,244 items from June 2015 to August 2024; retrieval-free GPT-4o and Gemini Pro get better in recent years, including after their end-2023 cutoffs. Fine-tuned RoBERTa shows the same trend, and removing the speaker, publish time or paraphrasing does not change it; the authors read recent fake claims as more sensational.
- **Snopes over time:** 3,212 items from January 2016 to October 2024; GPT-4o is near perfect on old items, drops on recent ones, and search retrieval brings back near-perfect performance.
- **Iterative generation:** deception grows with every round across five detectors and two retrieval sources; GPT-3.5 is most vulnerable and Llama 3.1 the most robust.
- **Feedback type:** rationale from a retrieval-augmented detector beats a retrieval-free rationale or scores alone; by round six the gap is 6.5 AUC points (64.9 against 71.4).
- **Chain-of-thought:** helps only with retrieved context; without it, detectors stay below random.

## Data

- PolitiFact: 9,244 claims, 2015 to 2024. Snopes: 3,212 articles, 2016 to 2024.
- NBC News: 431 stories from 1 to 13 March 2024 as seeds; 29 invalid pairs removed to leave 402 true and 402 fake.
- Retrieval corpus: 811k March 2024 articles, plus live Google results.

> [!failure] Limitations
> - The AUC trend on PolitiFact is shown in figures with no per-year numbers in the text, and cause is attributed from sampled examples.
> - Fake items are made by GPT-4o and tested against GPT-4o-based feedback, so the set may favour that family.
> - Detectors get the plausibility prompt and a stated date, which may not match deployment.
> - Seed news is two weeks of one outlet in English.
> - The paper is a preprint, revised three times.

## Relation to our project

- It is the evidence behind the risk-register entry on contamination with fact-check sites: gold fact-checks and posts both sit on the same sites, so "after the cutoff" does not mean "unseen" ([[LLM selection]], [[2026-10-27-temporal-retrieval-eval|Project plan]]).
- For RQ5, do not treat date alone as the clean stratum: the PolitiFact trend shows post-cutoff items can be easier through surface patterns, so we should compare to non-LLM baselines ([[bge-reranker-v2-m3]]) on the same strata.
- Retrieval restoring accuracy on Snopes warns that an LLM reranker given the fact-check text can be right through the text, not through knowledge; our protocol separates the two by pool design ([[Dated Data]], [[TripleFact]]).
- The task here is verification, not PFCR, so the numbers do not transfer; only the mechanism does.

## Future work

- **Open:** a similar check for retrieval of fact-checks, comparing post-cutoff and pre-cutoff fact-check pools (searched 2026-10).
- **Open:** the authors suggest better reasoning and inference-time scaling for retrieval-grounded detection (searched 2026-10).
