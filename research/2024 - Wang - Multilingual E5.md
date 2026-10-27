# 2024 - Wang - Multilingual E5

## Citation

- Authors: Liang Wang, Nan Yang, Xiaolong Huang, Linjun Yang, Rangan Majumder, Furu Wei (Microsoft)
- Title: Multilingual E5 Text Embeddings: A Technical Report
- Venue: arXiv technical report, arXiv:2402.05672 (no peer-reviewed venue found)
- Year: 2024 (models released mid-2023)
- URL: https://arxiv.org/abs/2402.05672
- Verified on: 2026-10-27 (arXiv abstract and HTML read)

## What it does

- Describes mE5 small/base/large (initialised from multilingual MiniLM, xlm-roberta-base, xlm-roberta-large) and mE5-large-instruct.
- Training: contrastive pre-training on about 1 billion multilingual text pairs, then supervised fine-tuning on about 1.6M labelled pairs (MS MARCO, NQ, TriviaQA, SQuAD, NLI, ELI5, NLLB, DuReader, FEVER, HotpotQA, Quora, Mr. TyDi, MIRACL).
- The instruct model adds about 500k GPT-3.5/4 synthetic examples (150k instructions, 93 languages).
- Evaluates on English MTEB, MIRACL (16 languages) and bitext mining (BUCC, Tatoeba).

## Key numbers

- Table 3 (English MTEB, 56 datasets): mE5-large 61.5, mE5-large-instruct 64.4, LaBSE 45.2.
- Table 4 (MIRACL dev, nDCG@10 avg over 16 languages): BM25 39.3, mDPR 41.5, mE5-large 66.5, mE5-large-instruct 65.7.
- Bitext Tatoeba (112 langs): LaBSE 81.1, mE5-large 75.7, mE5-large-instruct 83.8.

## Relation to our project

- Main multilingual dense baseline (S2) and the fine-tuning base for S6. Input prefixes were not read in this report; take them from the model card before running.
- Its fine-tuning mix includes FEVER (Wikipedia claim verification), not fact-check archives; parametric exposure to MultiClaim-era fact-check articles through the 1B-pair web pre-training corpus cannot be ruled out from the report.
- Does NOT cover: temporal evaluation, claim matching; no Polish row in the MIRACL per-language tables I read (Polish evidence for mE5 comes from PIRB).

## Verification

- OK. Reference list "Wang et al. 2024, Multilingual E5 Text Embeddings" with the arXiv URL is correct; it is a technical report, not a peer-reviewed paper.
