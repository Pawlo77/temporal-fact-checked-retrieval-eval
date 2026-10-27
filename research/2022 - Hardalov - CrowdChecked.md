# 2022 - Hardalov - CrowdChecked

## Citation

- Authors: Momchil Hardalov, Anton Chernyavskiy, Ivan Koychev, Dmitry Ilvovsky, Preslav Nakov
- Title: CrowdChecked: Detecting Previously Fact-Checked Claims in Social Media
- Venue: Proceedings of AACL-IJCNLP 2022 (Volume 1: Long Papers), online, pages 266-285
- Year: 2022
- URL: https://aclanthology.org/2022.aacl-main.22/ (abstract page and PDF read)
- Verified on: 2026-10-27

## What it does

- Mines "crowd fact-checking": tweets whose replies link a Snopes fact-checking article, giving distantly supervised tweet-article pairs.
- Filters noisy pairs with Jaccard or cosine thresholds and trains SBERT with modified self-adaptive training and a weighted MNR loss; final system re-ranks with LambdaMART over TF.IDF and SBERT scores.
- Evaluates on the CheckThat! 2021 Task 2A English splits (train 999 / dev 199 / test 202), preserving the original splits.
- Removes all CheckThat '21 tweets from the mined data.

## Key numbers

- Collection October 2017 to October 2021; 482,736 hits; 332,660 unique tweet-article pairs, 316,564 unique tweets, 10,340 Snopes articles (published 1995-2021).
- 8,898 articles overlap with CheckThat '21's 13,835; CheckThat '21 articles peak at 2016/2017.
- Table 6/7: best ensemble MAP@5 90.3 on the CheckThat '21 test vs Aschern 88.2.

## Relation to our project

- Not novel for us: large-scale distant supervision for PFCR, and training on newer data (to Oct 2021) than the test set's collection period.
- Shows the training-time leakage scenario our H5 targets: training pairs collected up to 2021 used to evaluate on an earlier test set, with only exact-tweet de-duplication; the paper does not analyse this temporally.
- No date-restricted pool.

## Verification

- Status: OK.
- Only in the reference list (line 215); citation correct.
