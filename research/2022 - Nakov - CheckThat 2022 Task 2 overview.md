# 2022 - Nakov - CheckThat 2022 Task 2 overview

## Citation

- Authors: Preslav Nakov, Giovanni Da San Martino, Firoj Alam, Shaden Shaar, Hamdy Mubarak, Nikolay Babulkov (as cited in Shaar et al. 2022 and Hardalov et al. 2022)
- Title: Overview of the CLEF-2022 CheckThat! Lab Task 2 on Detecting Previously Fact-Checked Claims
- Venue: CLEF 2022 Working Notes, CEUR-WS Vol-3180
- Year: 2022
- URL: https://ceur-ws.org/Vol-3180/paper-29.pdf (PDF read)
- Verified on: 2026-10-27

## What it does

- Same two subtasks as 2021: 2A tweets (Arabic, English) and 2B political debates (English, PolitiFact).
- Reuses the 2021 train/dev data, renames the 2021 test as "dev-test", and adds a new test set.
- Official measure MAP@5; baseline is a random baseline in 2022.
- English verified-claim collection is again 13,835 Snopes claims.

## Key numbers

- Table 1: 2A-English 1,610 input claims (999 train / 200 dev / 202 dev-test / 209 test), 13,835 verified claims; 2A-Arabic 908 (512/85/261/50), 30,379 verified (text also says 30,329); 2B-English 752 (472/119/78/83), 869 pairs, 20,771 verified claims.
- Table 3: 2A English best RIET Lab MAP@5 0.956; 2B SimBa MAP@5 0.459.
- Arabic results not reported: random baseline and the only system scored 0.0.

## Relation to our project

- Not novel for us: shared-task PFCR with a newly added test set on top of older training data, which resembles an out-of-time test but is not described as time-based in the excerpt read.
- No date restriction of the verified-claim pool described.

## Verification

- Status: OK.
- Line 54's "CheckThat! 2020-2022 Task 2 (verified claim retrieval, English tweets vs Snopes; Arabic)" holds for 2022, with the omission of 2B (debates) noted in CORRECTIONS-A.
