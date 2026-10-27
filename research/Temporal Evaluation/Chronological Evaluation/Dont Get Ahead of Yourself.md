---
title: "Dont Get Ahead of Yourself"
aliases: ["Don't Get Ahead of Yourself: A Critical Study on Data Leakage in Offline Evaluation of Sequential Recommenders"]
authors: ["Huy Hoang Le", "Yang Liu", "Alan Medlar", "Dorota Glowacka"]
year: 2025
venue: "Proceedings of the Nineteenth ACM Conference on Recommender Systems (RecSys '25), pages 1164-1168"
doi: "10.1145/3705328.3759329"
url: "https://dl.acm.org/doi/10.1145/3705328.3759329"
citekey: le2025dont
verified: 2026-10-27
theme: "[[Chronological Evaluation]]"
tags: [type/paper, theme/chronological, topic/leakage, topic/recsys, topic/evaluation, topic/temporal]
---
# Dont Get Ahead of Yourself

> [!info] TL;DR
> Sequential recommenders are almost always evaluated with temporal leave-one-out, which lets training contain other users' interactions from after the test moment. Comparing it with a leakage-free split-by-timepoint variant on four datasets and nine models, sampled nDCG@10 falls by 21.7% to 73.4% once leakage is removed. In most settings, subsampling the leaky training set to the same size removes only a few points of that drop, and the best model changes in 7 of 8 dataset-metric combinations.

## Motivation

- Leakage in recommender evaluation was already documented ([[Data Leakage in Recommender Evaluation]]), but practice did not change: 7 of 9 full RecSys 2024 papers on sequential recommendation still used temporal leave-one-out.
- Earlier split comparisons mixed leakage with other differences: temporal leave-one-out and split-by-timepoint have different test-set and training-set sizes, so their gap cannot be attributed to leakage alone.
- [[Data Leakage in Recommender Evaluation]] varied the amount of leaked future data but did not compare leaky and leak-free protocols as used in practice.

## Method

The paper is about recommendation, not retrieval; its terms are kept and mapped where useful.

**Temporal leave-one-out (T-LOO).** For each user, the last interaction is the test item and the second-to-last the validation item; everything else trains. Other users' interactions after the test moment stay in training.

**Split-by-timepoint leave-one-out (ST-LOO).** One global cut-off date. Active users (with interactions after the cut-off) contribute the first interaction after it as the test item and the one before it as validation; later interactions are discarded. Inactive users are dropped.

Intuition: ST-LOO is T-LOO with a global clock, so the only systematic difference is whether training can see the future.

**Size control.** T-LOO training sets are 1.2 times (ML-1m) to 2.3 times (Steam) larger, so a third arm subsamples whole users from T-LOO until training size matches ST-LOO.

**Leakage measured as utility gap.** Leakage is the relative drop from T-LOO to ST-LOO. Leakage between training and validation is deliberately kept in both arms so that model selection does not bias the estimate.

## Key numbers

- Sampled nDCG@10 drops 21.7% (Steam) to 73.4% (ML-1m) from T-LOO to ST-LOO; unsampled nDCG@10 drops 16.5% to 90.0%.
- With matched training size the drop remains large: on ML-1m sampled nDCG@10 still falls 72.2% (vs 73.4% unmatched); on Beauty 41.6% (vs 62.7%).
- Under T-LOO, users who leave before the cut-off (and so have more future data from others) score higher than active users: SASRec on ML-1m sampled nDCG@10 0.5271 vs 0.2600.

## Experiments

- **Leakage gap:** nine models (FPMC, GRU4Rec, Caser, SASRec, BERT4Rec, S3-Rec, LightSANs, SINE, FEARec) under T-LOO and ST-LOO with sampled and unsampled nDCG@10 and recall@10; all lose substantially without leakage.
- **Training-size control:** subsampled T-LOO vs ST-LOO; most of the gap remains, so leakage, not training volume, drives it, though on Yelp and Steam unsampled metrics size explains more.
- **Active vs inactive users:** splitting T-LOO results by the ST-LOO cut-off; inactive users score higher for both models on all datasets, which is the signature of leakage.
- **Model rankings:** the top model differs between protocols in 7 of 8 dataset-metric pairs; on Steam unsampled the worst T-LOO model becomes the best.

## Data

- ML-1m, Beauty, Steam and Yelp with implicit feedback and 5-core filtering; T-LOO training sets range from 131,413 (Beauty) to 4,214,699 (Yelp) interactions.

> [!failure] Limitations
> - Leakage is measured indirectly, as the gap between two splits that still differ in test-set size and user population.
> - Leakage during model selection (training vs validation) is kept on purpose and not quantified.
> - Extended abstract: per-model results are only in online supplementary material.
> - Absolute effects rely partly on sampled metrics, which the authors note can disagree with unsampled ones.

## Relation to our project

- The size-matched control is the closest design analogue to our per-query size-matched random pool: it separates "less data" from "no future data" ([[Proposed Task]]).
- The active vs inactive split suggests a diagnostic for PFCR: under the random protocol, posts whose gold fact-check appears long after them should gain most, which we can test by stratifying on post-to-fact-check lag ([[Enhanced topic research]]).
- Ranking reversals support reporting rank stability of our systems between random and causal protocols, not only score drops ([[Chronological Evaluation]]).
- Leakage here is in training data, not in the candidate pool, so it maps to our training-regime arm rather than to the causal index.

## Future work

- **Partly done:** leakage between training and validation in model selection; global temporal splits with several validation schemes are compared by [Gusak et al., 2025](https://doi.org/10.1145/3705328.3748164).
- **Open:** a direct per-instance measure of leakage instead of a split-vs-split gap (searched 2026-10).
- **Open:** time-respecting evaluation with a candidate set that also grows over time, as in a fact-check archive (searched 2026-10).
