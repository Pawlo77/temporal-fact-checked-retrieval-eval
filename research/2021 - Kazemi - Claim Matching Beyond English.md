# 2021 - Kazemi - Claim Matching Beyond English

## Citation

- Authors: Ashkan Kazemi, Kiran Garimella, Devin Gaffney, Scott A. Hale
- Title: Claim Matching Beyond English to Scale Global Fact-Checking
- Venue: Proceedings of ACL-IJCNLP 2021 (Volume 1: Long Papers), pages 4504-4517
- Year: 2021
- URL: https://aclanthology.org/2021.acl-long.347/ (abstract page and PDF read)
- Verified on: 2026-10-27

## What it does

- Defines claim matching as identifying pairs of messages containing claims that one fact-check can serve.
- Builds data from WhatsApp tiplines (Indian election tipline, March-May 2019; other tiplines February-August 2020) and public WhatsApp groups, plus fact-check headlines, in English, Hindi, Bengali, Malayalam, Tamil.
- Two annotated sets: claim-like statement detection and claim-similarity pairs (pairs sampled with LASER, LaBSE and their model, plus random pairs).
- Trains I-XLM-R by knowledge distillation (English SBERT teacher, XLM-R student) and compares with LASER and LaBSE.
- Demonstrates clustering of 37,823 tipline messages.

## Key numbers

- 5,066 messages annotated for claim-like statements; 2,343 message/fact-check pairs annotated for similarity (Section 3).
- Table 8: 261 "Very Similar" pairs overall (11%).
- Table 4 (MRR, BM25 + reranker): Bengali I-XLM-R 0.5281 vs BM25 0.4247.
- Table 6: I-XLM-R accuracy 0.883, F1(+) 0.885.
- Section 6: 1,305 clusters with 2 or more items at threshold 0.90; largest 213.

## Relation to our project

- Not novel for us: multilingual claim matching and the cluster view of repeated claims.
- The data has message submission times but the evaluation is not temporal; no date-restricted fact-check pool.
- Useful as a citation for "claims recur", which motivates earlier-sibling relevance.

## Verification

- Status: OK.
- Only in the reference list (line 214); citation correct. MultiClaim's Table 1 lists it as 150,000 fact-checks, 258 pairs, 5 languages; the paper's own Table 8 gives 261 Very Similar pairs (the small difference is MultiClaim's count, not checked further).
