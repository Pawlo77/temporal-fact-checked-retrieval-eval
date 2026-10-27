# 2025 - Ramponi - Multilingual vs Crosslingual Retrieval of Fact-Checked Claims

## Citation

- Authors: Alan Ramponi, Marco Rovera, Robert Moro, Sara Tonelli
- Title: Multilingual vs Crosslingual Retrieval of Fact-Checked Claims: A Tale of Two Approaches
- Venue: Proceedings of EMNLP 2025 (main), Suzhou, pages 29045-29064
- Year: 2025
- URL: https://aclanthology.org/2025.emnlp-main.1480/ (abstract page and PDF read)
- Verified on: 2026-10-27

## What it does

- Builds a subset of MultiClaim v2: post text only (no OCR), original languages, languages with at least 200 posts, claims with at least one paired post.
- Keeps only pairs with relationship claim_review or backlink ("only these relationships were present in the original version of MultiClaim").
- Re-detects languages with four detectors (fastText, gCLD3, langdetect, polyglot) instead of Google Translate labels.
- Splits pairs into train/dev/test stratified by language, withholding 10% for dev and 10% for test.
- Compares unsupervised retrieval (16 embedding models), cross-encoder and LLM re-ranking, and supervised fine-tuning with random, topic or similarity negative sampling; metrics S@10 and MRR@10.
- Reports a multilingual setting (all pairs) and a crosslingual setting (pairs in different languages only).

## Key numbers

- Abstract/Section 3: 47 languages (30 in posts, 46 in claims), 283 language combinations; Polish (pl) is in the list.
- Data table: multilingual 55,421 posts (train 44,553 / dev 5,185 / test 5,683) and 52,911 fact-checks; crosslingual 7,975 posts and 7,869 fact-checks.
- Table 2 (multilingual-e5-large, test MRR@10): LLM re-rank 0.8042 multilingual, 0.6140 crosslingual, 0.5797 crosslingual without English.
- Section 5.2: similarity negatives improve over random by 1.45 / 5.31 MRR@10 and 0.94 / 4.96 S@10 (multilingual / crosslingual).

## Relation to our project

- Not novel for us: multilingual vs crosslingual PFCR on MultiClaim v2, LLM reranking as the strongest method, and hard-negative fine-tuning.
- Their split is random stratified by language, not chronological, and the pool is not date-restricted; this is a direct example of the random protocol whose gap we want to measure, and a natural S6 recipe.
- Their choice to drop similarity:identical pairs supports our plan to report those pairs separately.
- They release only IDs, splits and code, the same pattern our release must follow.

## Verification

- Status: OK.
- Line 61 ("multilingual vs crosslingual PFCR on a MultiClaim v2 subset, 47 languages, best results from LLM reranking and similarity-sampled negatives; no temporal protocol") is correct. Precisely: LLM reranking is best, "followed by fine-tuning with negative examples sampled using a sentence similarity-based strategy"; splits are random stratified by language.
- Reference line 210 correct; the note names no co-authors (Rovera, Moro, Tonelli); Moro is also a MultiClaim and SemEval author.
