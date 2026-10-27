# 2023 - Schlichtkrull - AVeriTeC

## Citation

- Authors: Michael Schlichtkrull, Zhijiang Guo, Andreas Vlachos
- Title: AVeriTeC: A Dataset for Real-world Claim Verification with Evidence from the Web
- Venue: NeurIPS 2023 Datasets and Benchmarks Track (per arXiv comment "Accepted to NeurIPS 2023 Datasets & Benchmarks Track"); arXiv:2305.13117 v3
- Year: 2023
- URL: https://arxiv.org/abs/2305.13117 (HTML v3 read)
- Verified on: 2026-10-27

## What it does

- Releases 4,568 real-world claims from fact-checks by 50 organisations, each annotated with question-answer pairs, evidence from the web, and a textual justification.
- Avoids temporal leakage by restricting annotators' custom Google search to documents published before the claim date, and by ordering train/dev/test splits temporally.
- States that temporal ordering also prevents pretraining leakage if a language model's training data is cut off before the test period.
- Acknowledges the guarantee is approximate: Google's estimated dates are noisy (Section 8), and about 6% of dev answers come from a fact-checking domain, mostly an earlier fact-check of the same claim by a different organisation.
- Provides a baseline (Google Search limited to pre-claim documents, BM25, BLOOM question generation, BERT stance) and an evaluation that only credits verdicts when evidence matches gold.

## Key numbers

- Abstract: 4,568 claims, 50 organisations, inter-annotator kappa 0.619 on verdicts.
- Table 2: train 3,068 claims (end date 25-08-2020), dev 500 (end 31-10-2020), test 1,000 (end 22-12-2021).
- Table 4 (macro F1 veracity): no evidence .17, gold evidence .49, AVeriTeC baseline .23, gpt-3.5-turbo .39.
- Section 7.2: Google results contained useful evidence in 9/20 manually analysed dev examples.

## Relation to our project

- Direct precedent for a causal (pre-claim) evidence constraint and temporally ordered splits; supports our training-regime (random vs chronological) arm and our parametric-leakage stratum.
- Its finding that an earlier fact-check of the same claim by another outlet counts as legitimate pre-claim evidence is the same mechanism as our "earlier sibling" cluster-expanded qrels.
- Its date-noise caveat supports our timestamp-leakage category and margin sensitivity.
- Does NOT cover: matching posts to a fact-check archive, ranking metrics, answerability rates, pool-size effects, multilingual/Polish data.

## Verification

- OK. Note line "AVeriTeC, NeurIPS 2023 (evidence must predate the claim)" is correct. Suggested addition (not an error): AVeriTeC also orders its splits temporally and admits the pre-claim guarantee is approximate (about 6% of dev answers from fact-checking domains).
