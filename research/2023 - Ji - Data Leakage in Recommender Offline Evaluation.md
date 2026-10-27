# 2023 - Ji - Data Leakage in Recommender Offline Evaluation

## Citation

- Authors: Yitong Ji, Aixin Sun, Jie Zhang, Chenliang Li
- Title: A Critical Study on Data Leakage in Recommender System Offline Evaluation
- Venue: ACM Transactions on Information Systems 41(3), Article 75, 27 pages (February 2023); preprint arXiv:2010.11060
- Year: 2023
- URL: https://dl.acm.org/doi/10.1145/3569930
- Verified on: 2026-10-27 (ACM DL page read)

## What it does

- Defines data leakage in recommender evaluation as not observing the global timeline, so models learn from interactions not available at prediction time.
- Experiments with BPR, NeuMF, SASRec, LightGCN on MovieLens-25M, Yelp, Amazon-music, Amazon-electronic, using leave-last-one-out and varying amounts of "future" training data per test year.
- Finding 1: models recommend future items (items only available after the test instance's timestamp).
- Finding 2: top-N lists and relative model orders change unpredictably with the amount of leaked future data.
- Argues only split-by-timepoint observes the global timeline, while noting it alone is not automatically realistic.

## Key numbers

- Section 2.2 (citing a prior survey): of 85 recsys papers from 2017-2019, 53.7% used random split, 28% leave-one-out, 12.3% split-by-timepoint.
- Table of future items in BPR top-N lists, e.g. Yelp test year Y5 with Y9 training data: 3,162 future items.

## Relation to our project

- Cross-field precedent that leaking future items into the candidate set produces recommendations impossible at query time, the same structure as future fact-checks in a PFCR pool ("index leakage").
- Supports reporting system-ranking stability (Kendall tau) across protocols, since leakage reorders models.
- Does NOT cover: text retrieval, answerability, relevance labels, pool-size controls.

## Verification

- OK. Note line "Ji et al., TOIS 2023 (data leakage from ignoring the global timeline)" is correct. Reference list omits authors; add "Ji, Sun, Zhang, Li".
