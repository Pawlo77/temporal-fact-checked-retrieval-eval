# 2022 - Feng - LaBSE

## Citation

- Authors: Fangxiaoyu Feng, Yinfei Yang, Daniel Cer, Naveen Arivazhagan, Wei Wang
- Title: Language-agnostic BERT Sentence Embedding
- Venue: Proceedings of ACL 2022 (Volume 1: Long Papers), Dublin
- Year: 2022
- URL: https://aclanthology.org/2022.acl-long.62/
- Verified on: 2026-10-27 (Anthology page read)

## What it does

- Studies multilingual sentence embeddings combining MLM, translation language modelling, dual-encoder translation ranking and additive margin softmax.
- Shows a pre-trained multilingual LM reduces the parallel data needed for good performance by 80%.
- Produces LaBSE for bitext retrieval; the abstract reports results over 112 Tatoeba languages (the number of training languages was not in the parts I read).

## Key numbers

- Abstract: 83.7% bi-text retrieval accuracy over 112 languages on Tatoeba, vs 65.5% for LASER.
- Secondary (mE5 report, Table 3): LaBSE 45.2 on English MTEB, far below retrieval-trained encoders.

## Relation to our project

- Reasonable "classic cross-lingual" baseline (S3) for translation-like post/fact-check pairs; trained on translation pairs, so weak on asymmetric retrieval (mE5 report Table 3).
- Does NOT cover: retrieval-trained objectives, temporal evaluation.

## Verification

- OK. Reference list "Feng et al. 2022, LaBSE, ACL" is correct.
