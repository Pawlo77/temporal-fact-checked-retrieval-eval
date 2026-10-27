---
title: "Data Leakage in Recommender Evaluation"
aliases: ["A Critical Study on Data Leakage in Recommender System Offline Evaluation"]
authors: ["Yitong Ji", "Aixin Sun", "Jie Zhang", "Chenliang Li"]
year: 2023
venue: "ACM Transactions on Information Systems 41(3), Article 75, pages 1-27"
arxiv: "2010.11060"
doi: "10.1145/3569930"
url: "https://dl.acm.org/doi/10.1145/3569930"
citekey: ji2023critical
verified: 2026-10-27
theme: "[[Chronological Evaluation]]"
tags: [type/paper, theme/chronological, topic/leakage, topic/recsys, topic/evaluation, topic/temporal]
---
# Data Leakage in Recommender Evaluation

> [!info] TL;DR
> Offline recommender evaluation usually ignores the global timeline, so collaborative filtering learns from other users' interactions that happen after the test moment. Adding one year of such future data at a time to four models on four datasets, the authors show that models recommend items that did not yet exist, that top-20 lists drift away from the leak-free lists, and that accuracy and model order change unpredictably. They propose a timeline scheme in which a model only sees interactions before each test instance.

## Motivation

- Most recommender papers split data without regard to time: of 85 papers from 2017-2019 surveyed by Sun et al. (2020), 53.7% used random splits, 28% leave-one-out and 12.3% split-by-timepoint.
- Leave-one-out respects each user's own timeline, so it looks safe, but collaborative filtering transfers information between users whose activity periods do not overlap.
- Prior work noted leakage in passing ([Campos et al., 2013](https://doi.org/10.1007/s11257-012-9136-x)) or compared splits ([Meng et al., 2020](https://doi.org/10.1145/3383313.3418479)); no study measured the effect of leakage itself.

## Method

The paper is about recommendation; its terms are kept. A "future item" is one first seen after the test instance's timestamp.

**Global vs local timeline.** A split observes the local timeline if each user's test interaction is after their training interactions, and the global timeline if every test interaction is after every training interaction. Only split-by-timepoint observes the global timeline.

**Graded leakage.** Interactions over ten years are cut into one-year windows. Test instances are users' last interactions inside one test year. Training first holds all earlier years plus non-test interactions of the test year, then adds the following years one at a time, so leakage grows run by run.

Intuition: the test set stays fixed and only the amount of future data changes, so any change in output is caused by leakage.

**Measures.** Count of future items in top-20 lists; Jaccard overlap of top-20 lists between leak-free and leaky runs, compared with the overlap between random seeds of the same run; HR@20 and NDCG@20 over the full item set (not sampled).

**Timeline scheme.** Interactions are replayed in time order; at each test instance the model predicts from what it has learned so far and from the items available then. Prequential evaluation is the extreme case; a sliding window is a relaxed version.

## Key numbers

- All four models recommend future items on all four datasets, and the count grows as more future years enter training.
- Accuracy under leakage moves in both directions relative to the leak-free run, with no consistent pattern across models or datasets.
- The order of the four models by HR@20 changes with the amount of future data on all four datasets; on Yelp only the best and worst models stay fixed.

## Experiments

- **Future items in top-20:** BPR, NeuMF, SASRec and LightGCN, two test years; future items appear and increase with leakage.
- **List drift:** Jaccard similarity to leak-free lists falls as future years are added and moves away from seed-to-seed similarity, so the change is not training noise; MovieLens-25M is affected more than Amazon-electronic.
- **Accuracy:** HR@20 and NDCG@20 fluctuate, rise or fall with added future data depending on model and dataset.
- **Model order:** ranking of the four models by HR@20 swaps across leakage levels.

## Data

- MovieLens-25M (2009-2019, no filtering), Yelp (2009-2019, 10-core), Amazon-music (2008-2018, 5-core), Amazon-electronic (2008-2018, 10-core); ten years each, users whose history starts before the window removed.

> [!failure] Limitations
> - Leakage is simulated at year granularity; leakage within the test year is not controlled.
> - Only leave-one-out is studied; the timeline scheme is proposed but not evaluated.
> - MovieLens timestamps are unreliable (many users rate everything in one day), as the authors note.
> - Four classic baselines; no text or content-based models.

## Relation to our project

- The "future item" finding is the recommender form of index leakage in PFCR: a fact-check published after the post can be retrieved only because the pool ignores the global timeline ([[2026-10-27-temporal-retrieval-eval|Project plan]]).
- The timeline scheme is our causal protocol in recommender terms: each post is scored against the pool available at its time ([[2026-10-27-topic-research|Topic research]]).
- Unpredictable model order supports reporting rank changes between random and causal protocols, not only score changes ([[Chronological Evaluation]]).
- Its leakage is in training data; [[Dont Get Ahead of Yourself]] later shows that in standard settings the net effect is a large inflation, not a random one.

## Future work

- **Partly done:** quantify leakage under the dominant sequential protocol with a leak-free counterpart; [[Dont Get Ahead of Yourself]] finds drops of 21.7% to 73.4% in sampled nDCG@10.
- **Partly done:** validation and tuning under global temporal splits; [Gusak et al., 2025](https://doi.org/10.1145/3705328.3748164).
- **Open:** a full evaluation of the timeline scheme with incremental models against batch retraining (searched 2026-10).
