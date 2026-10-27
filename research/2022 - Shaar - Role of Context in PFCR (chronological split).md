# 2022 - Shaar - Role of Context in PFCR (chronological split)

Found while searching for prior time-aware PFCR evaluation; not cited in the Enhanced topic research note.

## Citation

- Authors: Shaden Shaar, Firoj Alam, Giovanni Da San Martino, Preslav Nakov
- Title: The Role of Context in Detecting Previously Fact-Checked Claims
- Venue: Findings of the ACL: NAACL 2022, Seattle, pages 1619-1631
- Year: 2022
- URL: https://aclanthology.org/2022.findings-naacl.122/ ; read via https://arxiv.org/pdf/2104.07423.pdf (v2, 9 May 2022)
- Verified on: 2026-10-27

## What it does

- Works on the PolitiFact part of Shaar et al. 2020: debate/speech sentences matched to PolitiFact verified claims; studies source-side context (the debate) and target-side context (the fact-check article).
- Annotates pair types: clean, clean-hard, part-of, context-dep.
- Compares four data splits: Debate-Level Chrono (train on the first 50 debates, 2012-2018; test on the last 20, 2019), Debate-Level Semi-Chrono (80/20 within each year), Debate-Level Random, and Sentence-Level Random (the 2020 setup).
- Calls the chronological split "a more realistic scenario, where we would only have access to earlier debates", and uses it for all main experiments.
- The excerpt read reports one verified-claim collection (16,636 claims) and does not describe restricting it to claims fact-checked before each debate.

## Key numbers

- 695 pairs (clean 291, clean-hard 210, part-of 68, context-dep 126); 16,636 verified claims.
- Chrono split: 554 train pairs, 141 test pairs.
- Table 3 (reranker MAP): Debate-Level Chrono 0.429; Semi-chrono 0.539; Debate-Level Random 0.590; Sentence-Level Random 0.602.
- Fleiss kappa 0.5 for pair-type annotation.

## Relation to our project

- Directly relevant prior work: a chronological train/test split for PFCR already exists and shows a large drop from random to chronological (MAP 0.602 to 0.429). The "random vs chronological training" idea (our H5, S6 regimes) is therefore not new for PFCR in general; it is new for multilingual social-media PFCR on MultiClaim/SemEval.
- The drop mixes topic drift between years and training-set leakage; the paper attributes it to different topics across time frames. It does not separate index leakage, answerability or pool size.
- No evidence in what was read of a causal (date-restricted) verified-claim pool, so our causal-index claim still stands, but must cite this paper as the closest precedent.

## Verification

- Status: OK (new paper; verified from arXiv v2 and ACL Anthology search result).
- Impact on the Enhanced topic research note: line 79 ("Training-time leakage for fine-tuned PFCR models (random vs chronological training data), absent from SemEval system papers") is literally true for SemEval papers but implies novelty that this paper weakens; line 43's "no prior PFCR evaluation" framing must cite it. Line 66 lists chronological splits only for rumour detection (Mu et al.); this PFCR-specific precedent is missing.
