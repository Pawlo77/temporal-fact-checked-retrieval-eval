# 2021 - Shaar - CheckThat 2021 Task 2 overview

## Citation

- Authors: Shaden Shaar, Fatima Haouari, Watheq Mansour, Maram Hasanain, Nikolay Babulkov, Firoj Alam, Giovanni Da San Martino, Tamer Elsayed, Preslav Nakov (author list as cited in Hardalov et al. 2022)
- Title: Overview of the CLEF-2021 CheckThat! Lab Task 2 on Detecting Previously Fact-Checked Claims in Tweets and Political Debates
- Venue: CLEF 2021 Working Notes, CEUR-WS Vol-2936
- Year: 2021
- URL: https://ceur-ws.org/Vol-2936/paper-29.pdf (PDF read)
- Verified on: 2026-10-27

## What it does

- Subtask 2A: tweets vs a collection of fact-checked claims, Arabic and English; ranking, top-n.
- Subtask 2B: claims from political debates/speeches vs PolitiFact verified claims, English.
- English 2A: 13,835 Snopes verified claims; 1,401 tweets cited in Snopes articles.
- Arabic 2A: 5,921 AraFacts claims plus 24,408 ClaimsKG English claims translated to Arabic.
- Official measure MAP@5; Elastic Search (BM25) baseline.

## Key numbers

- Table 2: 2A-Arabic 858 input claims (512/85/261), 1,039 pairs, 30,329 verified claims; 2A-English 1,401 (999/200/202), 1,401 pairs, 13,835 verified; 2B-English 669 (472/119/78), 804 pairs, 19,250 verified.
- Split text: Arabic "randomly split" 512/85/261; English "split the data into 70%, 15% and 15%" (the word "random" is not used for English).
- Table 3: English best Aschern MAP@5 0.883 vs ES baseline 0.749; Arabic bigIR 0.908 vs 0.794.
- Table 5 (2B): no team beat the ES baseline (MAP@5 0.346).

## Relation to our project

- Not novel for us: shared-task PFCR on tweets and debates with fixed splits.
- The DIPS participant paper (CEUR Vol-2936 paper-45, seen only in a search excerpt) lists a `Date` field "on which the claim was fact-checked" and used it in BM25 features; so the CheckThat '21 English data carried fact-check dates, yet no causal pool restriction is described in the overview.
- Gap left: no date-restricted index, no temporal split described.

## Verification

- Status: CORRECTED.
- Line 54: "random 70/15/15 splits for English in 2021" overstates the source: the overview gives 70/15/15 for English without saying random (only Arabic is "randomly split"). The line also omits Subtask 2B (PolitiFact debates, English). CheckThat! 2020 was not checked in this pass.
- "No causal index constraint" is consistent with the overview (none described).
