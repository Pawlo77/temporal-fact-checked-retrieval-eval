# 2022 - Liska - StreamingQA

## Citation

- Authors: Adam Liska, Tomas Kocisky, Elena Gribovskaya, Tayfun Terzi, Eren Sezener, Devang Agrawal, Cyprien de Masson d'Autume, Tim Scholtes, Manzil Zaheer, Susannah Young, Ellen Gilsenan-McMahon, Sophia Austin, Phil Blunsom, Angeliki Lazaridou
- Title: StreamingQA: A Benchmark for Adaptation to New Knowledge over Time in Question Answering Models
- Venue: Proceedings of the 39th International Conference on Machine Learning (ICML 2022), PMLR 162:13604-13622
- Year: 2022
- URL: https://proceedings.mlr.press/v162/liska22a.html
- Verified on: 2026-10-27 (PMLR abstract page read). Not cited in the Enhanced topic research note; added as missed prior work.

## What it does

- Builds a QA dataset with human-written and generated questions, each asked on a given date, answerable from 14 years of time-stamped news articles.
- Evaluates models quarterly as they read new articles not seen in pre-training (a streaming, rolling-origin setup).
- Compares parametric updating (no full retraining) and semi-parametric models whose search space grows with new articles.
- Finds adding new articles to the retrieval space allows rapid adaptation, but models with an outdated underlying LM underperform those with a retrained LM.

## Key numbers

- 14 years of news articles; quarterly evaluation (abstract). No other numbers read.

## Relation to our project

- Precedent for dated queries against a time-stamped, growing retrieval corpus, i.e. our rolling-origin protocol; also for separating retrieval-index freshness from parametric (LM) freshness, which maps onto our index vs parametric leakage split.
- Does NOT cover: fact-checking, claim matching, leakage auditing, multilingual data.

## Verification

- Not in the note (missed). Recommend citing next to Lazaridou et al. 2021 for the rolling-origin protocol.
