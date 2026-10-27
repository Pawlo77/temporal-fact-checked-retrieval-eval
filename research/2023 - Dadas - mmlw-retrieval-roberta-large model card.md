# 2023 - Dadas - mmlw-retrieval-roberta-large model card

## Citation

- Author: Sławomir Dadas (Hugging Face user sdadas); the card asks users to cite the PIRB paper (Dadas, Perełkiewicz, Poświata, LREC-COLING 2024)
- Title: sdadas/mmlw-retrieval-roberta-large (model card)
- Venue: Hugging Face model card; card states the model was updated to a new version on 2023-12-26 (older weights under revision tag "v1")
- Year: 2023 (date of the current model version per the card)
- URL: https://huggingface.co/sdadas/mmlw-retrieval-roberta-large
- Verified on: 2026-10-27 (card read)

## What it does

- Polish dense retriever producing 1024-dimensional vectors; about 0.4B parameters; Apache-2.0 licence.
- Step 1: initialised from Polish RoBERTa and trained by multilingual knowledge distillation on 60 million Polish-English pairs with English BGE (bge-large-en) as teacher.
- Step 2: contrastive fine-tuning on the Polish MS MARCO training split (batch size 288 for large), on 12 A100 GPUs.
- Requires the query prefix "zapytanie: " (no passage prefix).

## Key numbers

- Card: "NDCG@10 of 58.46 on the Polish Information Retrieval Benchmark" (PIRB leaderboard).

## Relation to our project

- S3 Polish-specialised encoder; must apply the "zapytanie: " prefix to posts and no prefix to fact-checks.
- Distilled on Polish-English pairs from an English teacher, so Polish and English inputs should land in a shared space; Polish-to-English retrieval is plausible but the card reports only Polish (PIRB) results, so cross-lingual quality must be measured, not assumed.
- Does NOT cover: temporal evaluation, claim matching.

## Verification

- CORRECTED (attribution). Note S3 says "sdadas/mmlw-retrieval-roberta-large (PIRB NDCG@10 58.46)". The number 58.46 is on the model card (leaderboard value for the current version), but the PIRB paper's Table 3 reports 58.06 for the distilled + fine-tuned polish-roberta-v2 (large) retriever. Fix: "PIRB NDCG@10 58.46 per the model card / leaderboard (paper Table 3: 58.06; multilingual-e5-large 57.29)".
