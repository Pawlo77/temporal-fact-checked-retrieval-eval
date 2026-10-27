---
title: "Chronological Splits Rumor Detection"
aliases: ["It's about Time: Rethinking Evaluation on Rumor Detection Benchmarks using Chronological Splits"]
authors: ["Yida Mu", "Kalina Bontcheva", "Nikolaos Aletras"]
year: 2023
venue: "Findings of the Association for Computational Linguistics: EACL 2023, pages 736-743"
arxiv: "2302.03147"
doi: "10.18653/v1/2023.findings-eacl.55"
url: "https://aclanthology.org/2023.findings-eacl.55/"
citekey: mu2023its
verified: 2026-10-27
theme: "[[Chronological Evaluation]]"
tags: [type/paper, theme/chronological, topic/temporal, topic/evaluation, topic/english]
---
# Chronological Splits Rumor Detection

> [!info] TL;DR
> Four standard rumor detection benchmarks are re-evaluated with chronological instead of random train/dev/test splits. Every model on every dataset scores significantly lower when the test posts are the latest ones; on Twitter 16, logistic regression falls from 89.3 to 48.7 macro-F1. Random splits put near-identical posts about the same event in training and test, so they mostly measure recognition of known rumors, not detection of new ones.

## Motivation

- Recent rumor detection papers almost all evaluate on Twitter 15, Twitter 16, PHEME or Weibo with random splits.
- Topics of rumors are driven by events, so random splits mix posts about the same event across training and test; some pairs differ by a few characters.
- Chronological splits had already lowered classifier scores in hate speech, legal, political and biomedical text ([Huang and Paul, 2018](https://aclanthology.org/P18-2110/); [Agarwal and Nenkova, 2022](https://doi.org/10.1162/tacl_a_00497)), but not been tested on rumor benchmarks.
- Leave-one-event-out splits remove topic overlap but need event labels, which only PHEME has.

## Method

The paper is about classification; its terms are kept.

**Standard chronological split.** Sort posts by time: earliest 70% train, next 10% dev, latest 20% test, no temporal overlap. Possible only for Twitter 15 and PHEME, since in Twitter 16 and Weibo rumors and non-rumors do not overlap in time.

**Stratified chronological split.** Split rumors and non-rumors separately in time order (70/10/20) and merge, so class ratios match the random split and there is no temporal overlap within each class.

**Random split.** Stratified 5-fold cross-validation with the same 70/10/20 proportions.

Intuition: holding proportions and class balance fixed, the only change is whether test posts come after all training posts.

**Models.** TF-IDF logistic regression (5,000 n-grams), fine-tuned BERT, and a social-media model (BERTweet for English, ERNIE for Chinese). Binary rumor vs non-rumor; macro precision, recall and F1 over five seeds; random vs chronological compared with a t-test.

## Key numbers

- Twitter 16 macro-F1, random vs stratified chronological: LR 89.3 vs 48.7, BERT 91.5 vs 47.2, BERTweet 89.3 vs 45.1.
- Twitter 15 LR: 85.0 random vs 56.4 standard chronological.
- Weibo, random vs stratified chronological: LR 90.1 vs 77.9, BERT 91.2 vs 87.5.
- PHEME leave-one-event-out F1: LR 63.2, BERT 70.7, BERTweet 71.4.

## Experiments

- **Random vs chronological:** all three models on all four datasets; random splits are significantly higher everywhere ($p < 0.05$). The gap is about 50% on the small Twitter sets and about 10% on PHEME and Weibo.
- **Standard vs stratified chronological:** on Twitter 15 and PHEME, both give similar scores, so class balance does not explain the drop.
- **Error analysis:** with a Levenshtein threshold of 20 characters, 14% to 30% of random-split test posts have a near-duplicate in training, against 2% to 7% under chronological splits; most such posts are classified correctly, while errors cluster on emerging topics.
- **Model comparison:** under chronological splits BERT-style models beat LR significantly; the authors note these models were pretrained after the benchmarks were built, which may itself leak information.

## Data

- Twitter 15 and Twitter 16: 1,490 and 818 tweets, recast as binary rumor vs non-rumor.
- PHEME: 5,802 tweets from 9 breaking-news events (1,972 rumor, 3,830 non-rumor).
- Weibo: 4,664 Chinese posts (2,313 rumors from the Weibo debunking platform, 2,351 non-rumors).

> [!failure] Limitations
> - Only two languages and two platforms; Twitter 15 and 16 are small, so their gaps have large variance.
> - Rumors and non-rumors were collected at different times in Twitter 16 and Weibo, so time and label are confounded.
> - Pretraining of the models post-dates the data, a second leakage channel that is noted but not measured.
> - Classification only: no retrieval, no candidate pool.

## Relation to our project

- Evidence for our training-regime arm: a fine-tuned model trained and tested on random splits of misinformation data can look far better than it is on new events ([[Proposed Task]]).
- Its near-duplicate analysis has a PFCR counterpart: under a random protocol, posts of a recurring claim and their fact-checks from the future sit in the pool. Our coded failure analysis should count lexical near-duplicates in the same way ([[Enhanced topic research]]).
- For PFCR itself the chronological training split already exists in [[Role of Context in PFCR]]; this paper is supporting evidence from a neighbouring task, not a precedent for the causal index ([[Chronological Evaluation]]).
- Its caveat that pretraining post-dates the data maps to our parametric-leakage strata for LLM rerankers.

## Future work

- **Done:** temporal drift in other social-media tasks; stance towards COVID-19 vaccination drops under chronological splits ([Mu et al., 2024](https://aclanthology.org/2024.lrec-main.594/)).
- **Done:** whether context-based rumor models generalise to unseen rumors under forward and backward chronological splits ([Mu et al., 2024](https://aclanthology.org/2024.lrec-main.595/)).
- **Open:** rumor and claim benchmarks in more languages with chronological splits and dated collection of both classes (searched 2026-10).
