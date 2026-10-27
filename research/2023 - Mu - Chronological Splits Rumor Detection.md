# 2023 - Mu - Chronological Splits Rumor Detection

## Citation

- Authors: Yida Mu, Kalina Bontcheva, Nikolaos Aletras
- Title: It's about Time: Rethinking Evaluation on Rumor Detection Benchmarks using Chronological Splits
- Venue: Findings of the ACL: EACL 2023, Dubrovnik, pages 736-743, DOI 10.18653/v1/2023.findings-eacl.55
- Year: 2023
- URL: https://aclanthology.org/2023.findings-eacl.55/
- Verified on: 2026-10-27 (Anthology page and PDF read)

## What it does

- Re-evaluates rumour classifiers (LR, BERT, BERT+) on four benchmarks (Twitter15, Twitter16, PHEME, Weibo) with chronological instead of random splits.
- Uses the same 70/10/20 proportions and label ratios for random (5-fold) and (stratified) chronological splits.
- Finds random splits significantly overestimate performance across all datasets and models (t-test, p < 0.05).
- Attributes the gap to topical overlap / temporal concept drift; recommends chronological splits; releases splits on GitHub.

## Key numbers

- Table 4, Twitter16 macro-F1: LR random 89.3 vs stratified chronological 48.7; BERT 91.5 vs 47.2; BERT+ 89.3 vs 45.1.
- Table 4, Twitter15 LR macro-F1: random 85.0 vs standard chronological 56.4.
- Table 4, Weibo LR: random 90.1 vs stratified chronological 77.9.
- Table 5: PHEME leave-one-event-out F1 LR 63.2, BERT 70.7, BERT+ 71.4.

## Relation to our project

- Motivates hypothesis H5 (fine-tuned models trained on random splits lose more under chronological evaluation) and our chronological training regime.
- Shows the gap can be very large in misinformation data where topics are event-driven.
- Does NOT cover: retrieval, index composition, answerability, ranking metrics, multilingual or Polish data; it concerns training/test splits for classification only.

## Verification

- OK. Note line "Mu et al., Findings EACL 2023 (rumour detection overestimated under random splits)" is correct.
