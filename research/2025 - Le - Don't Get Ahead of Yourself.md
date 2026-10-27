# 2025 - Le - Don't Get Ahead of Yourself

## Citation

- Authors: Huy Hoang Le, Yang Liu, Alan Medlar, Dorota Glowacka
- Title: Don't Get Ahead of Yourself: A Critical Study on Data Leakage in Offline Evaluation of Sequential Recommenders
- Venue: RecSys '25, Proceedings of the Nineteenth ACM Conference on Recommender Systems, pages 1164-1168 (labelled "extended-abstract" on ACM DL)
- Year: 2025
- URL: https://dl.acm.org/doi/10.1145/3705328.3759329
- Verified on: 2026-10-27 (ACM DL page read)

## What it does

- Compares temporal leave-one-out (LOO), the dominant split for sequential recommenders and known to leak, with split-by-timepoint LOO that prevents leakage.
- Four datasets (including Steam and ML-1m); models include SASRec and LightSANs.
- Splits temporal-LOO results into active and inactive users to show evidence of leakage.
- Controls for training-set size between the two strategies and finds similar drops, attributing the drop primarily to leakage.
- Reports that the impact of leakage on model rankings is unpredictable.

## Key numbers

- Abstract / Section 4.1: sampled nDCG@10 drops by 21.7% (Steam) to 73.4% (ML-1m) under split-by-timepoint LOO.

## Relation to our project

- Its training-set-size control is the recsys analogue of our size-matched random control: it separates "less data" from "no future data".
- Supports reporting rank stability across protocols.
- Does NOT cover: text retrieval, fact-checking, relevance labels, answerability.

## Verification

- OK. Note line "RecSys 2025 study comparing temporal leave-one-out with split-by-timepoint" is correct. Reference list entry omits authors; add "Le, Liu, Medlar, Glowacka", and note it is a short extended-abstract paper (5 pages).
