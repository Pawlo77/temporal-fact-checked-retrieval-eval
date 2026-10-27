---
title: "Leakage in Verification"
tags: [type/theme, theme/verification-leakage]
parent: "[[Temporal Evaluation]]"
---
# Leakage in Verification

Evidence or answer leakage in claim verification: retrieved evidence that was written after the claim, or that is itself a fact-check of it, inflates scores. Part of [[Temporal Evaluation]].

## Summary

- [[Missing Counter-Evidence]]: in MultiFC, 69.7% of misinformation claims have evidence from or repeating a fact-check of the same claim.
- [[AVeriTeC]] requires evidence to predate the claim and uses temporal splits; about 6% of dev answers still come from fact-checking domains.
- [[Complex Claim Verification in the Wild]]: a temporal or fact-check-site constraint cuts accuracy from 49.0 to 33.5.
- Earlier fact-checks of the same claim count as evidence in [[AVeriTeC]], which supports sibling relevance for PFCR.
- Open: separate answerability (does the gold fact-check exist yet) from ranking quality, with conditional and unconditional scores.
- Open: fact-checks of the same claim by other organisations are leaks for verification but legitimate siblings for PFCR.
- Open: a frozen, timestamped archive is preferable to live search, which is non-stationary.

| Paper | Year | Takeaway |
|-------|------|----------|
| [[Missing Counter-Evidence]] | 2022 | In MultiFC, 69.7% of misinformation claims have evidence from or repeating a fact-check of the same claim; models exploit it. |
| [[AVeriTeC]] | 2023 | A claim dataset whose web evidence is restricted to pre-claim documents and whose splits are temporal; the guarantee stays approximate (about 6% of dev answers from fact-checking domains). |
| [[Complex Claim Verification in the Wild]] | 2024 | Adding a temporal or fact-check-site constraint cuts test accuracy from 49.0 to 33.5, so unconstrained web retrieval works largely through post-claim fact-checks. |
