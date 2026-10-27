# 2021 - Lazaridou - Mind the Gap

## Citation

- Authors: Angeliki Lazaridou, Adhi Kuncoro, Elena Gribovskaya, Devang Agrawal, Adam Liska, Tayfun Terzi, Mai Gimenez, Cyprien de Masson d'Autume, Tomas Kocisky, Sebastian Ruder, Dani Yogatama, Kris Cao, Susannah Young, Phil Blunsom
- Title: Mind the Gap: Assessing Temporal Generalization in Neural Language Models
- Venue: Advances in Neural Information Processing Systems 34 (NeurIPS 2021)
- Year: 2021
- URL: https://proceedings.neurips.cc/paper/2021/hash/f5bf0ba0a17ef18f9607774722f5698c-Abstract.html
- Verified on: 2026-10-27 (proceedings abstract page read)

## What it does

- Contrasts the static LM paradigm (train and evaluate on overlapping periods) with predicting utterances from beyond the training period.
- Shows Transformer-XL LMs perform worse on future data and degrade increasingly with time.
- Finds increasing model size alone does not solve the problem.
- Finds continual updating with new information mitigates the degradation.

## Key numbers

- None quoted: only the abstract page was read (no numbers in the abstract).

## Relation to our project

- Background for parametric temporal effects: encoders and LLM rerankers trained before a query period may handle later narratives worse, and conversely models trained after it may know later debunks (our RQ5 parametric leakage is the flip side).
- Does NOT cover: retrieval, fact-checking, leakage of future information into evaluation.

## Verification

- OK. Note line "Lazaridou et al., NeurIPS 2021 (temporal generalization)" is correct.
