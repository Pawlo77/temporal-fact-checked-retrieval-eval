# 2019 - Gorman - We Need to Talk about Standard Splits

## Citation

- Authors: Kyle Gorman, Steven Bedrick
- Title: We Need to Talk about Standard Splits
- Venue: Proceedings of ACL 2019 (57th Annual Meeting), Florence, pages 2786-2791, DOI 10.18653/v1/P19-1267
- Year: 2019
- URL: https://aclanthology.org/P19-1267/
- Verified on: 2026-10-27 (Anthology page read)

## What it does

- Replicates and reproduces nine POS taggers (2000-2018) that each claimed state of the art on a "standard split".
- Replicates results on the standard split but fails to reliably reproduce some system rankings across randomly generated train-test splits.
- Notes few researchers apply significance tests or examine ranking stability across splits.
- Argues randomly generated splits should be used in system evaluation.

## Key numbers

- Nine POS taggers published between 2000 and 2018 (abstract). No other numbers taken.

## Relation to our project

- Supports our statistical plan (significance testing, ranking stability across protocols/resamples).
- Its recommendation runs in the opposite direction to ours: it favours random splits over standard splits and does not discuss time; it should be cited as the position Søgaard et al. 2021 rebut, not as support for time-based splits.
- Does NOT cover: temporal splits, retrieval, leakage.

## Verification

- CORRECTED. The note groups it under "Split methodology: Gorman and Bedrick, ACL 2019; Søgaard et al., EACL 2021 (random splits overestimate; prefer biased or time-based splits)". Bibliographic data are right, but Gorman and Bedrick argue for random splits; citing them next to "random splits overestimate" without saying so misrepresents them. Fix: "Gorman and Bedrick (ACL 2019) argue for random over standard splits and for significance testing; Søgaard et al. (EACL 2021) rebut them."
