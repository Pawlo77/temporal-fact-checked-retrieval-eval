# 2024 - Dadas - PIRB

## Citation

- Authors: Sławomir Dadas, Michał Perełkiewicz, Rafał Poświata
- Title: PIRB: A Comprehensive Benchmark of Polish Dense and Hybrid Text Retrieval Methods
- Venue: Proceedings of LREC-COLING 2024, Torino, pages 12761-12774 (ELRA and ICCL)
- Year: 2024
- URL: https://aclanthology.org/2024.lrec-main.1117/
- Verified on: 2026-10-27 (Anthology page and PDF read)

## What it does

- Introduces the Polish Information Retrieval Benchmark: 41 tasks, including 10 new unpublished datasets (medicine, law, business, physics, linguistics), plus MAUPQA, BEIR-PL, PolEval-2022.
- Evaluates more than 20 dense and sparse retrievers, reporting only those above BM25.
- Proposes a three-step recipe: multilingual knowledge distillation from English BGE (FlagEmbedding) teachers into Polish RoBERTa or mE5 students, supervised fine-tuning, and sparse-dense hybrids with a lightweight rescoring model.
- Finds multilingual-e5-large the strongest existing model; distilled Polish RoBERTa-large and mE5-large reach the top scores.

## Key numbers

- Table 2 (avg NDCG@10, 41 tasks): multilingual-e5 small 50.65, base 53.12, large 57.29.
- Table 3 (avg NDCG@10): distilled + fine-tuned polish-roberta-v2 (large) 58.06; hybrid BM25 58.82; hybrid SPLADE 59.23. Distilled + fine-tuned mE5-large 58.03. mE5-large fine-tuned only 57.44; with SPLADE hybrid 58.66.
- Appendix: distilled Polish RoBERTa-large beats mE5-large on 53% of short-query, 50% of medium and 83% of long-query datasets; mE5 is clearly better only on PolEval-2022.

## Relation to our project

- Grounds the S3 choice: a Polish-specialised encoder is only about 1 NDCG@10 point above mE5-large on PIRB averages, so a large Polish-vs-multilingual gap on PFCR would be informative.
- PIRB has no fact-check or social-media claim-matching task, so PIRB rankings may not transfer to PFCR.
- Does NOT cover: temporal evaluation, cross-lingual Polish-English retrieval.

## Verification

- OK for the reference entry ("Dadas et al. 2024, PIRB, LREC-COLING"). See the mmlw model-card note for the 58.46 figure: the paper's Table 3 reports 58.06 for the distilled + fine-tuned Polish RoBERTa-large retriever, not 58.46.
