# 2024 - Chen - Complex Claim Verification in the Wild

## Citation

- Authors: Jifan Chen, Grace Kim, Aniruddh Sriram, Greg Durrett, Eunsol Choi
- Title: Complex Claim Verification with Evidence Retrieved in the Wild
- Venue: Proceedings of NAACL 2024 (Volume 1: Long Papers), Mexico City, pages 3569-3587, DOI 10.18653/v1/2024.naacl-long.196
- Year: 2024
- URL: https://aclanthology.org/2024.naacl-long.196/
- Verified on: 2026-10-27 (Anthology page and PDF read)

## What it does

- Builds a five-stage pipeline (claim decomposition, raw document retrieval via Bing, fine-grained retrieval, claim-focused summarisation, veracity judgment) for complex political claims.
- Applies a temporal constraint (only pages published before the claim) and a site constraint (no fact-checking websites; list in Appendix A.1), and compares against unconstrained retrieval.
- Uses ClaimDecomp: 1,200 PolitiFact claims (train 800, dev 200, test 200), six veracity labels.
- Shows MultiFC-style unconstrained retrieval is heavily contaminated with fact-check pages.
- Concludes that adding either constraint "dramatically reduces the performance", implying web retrieval works largely because it retrieves fact-checks published after the claim.

## Key numbers

- Table 2 (test accuracy): no constraint 49.0; site constraint only 33.5; temporal constraint only 33.5; both 33.0; claim only 25.5. Dev: 50.5 / 37.5 / 42.5 / 40.5 / 37.0.
- Section 4: in MultiFC, 12,721 of 15,379 claims (82.7%) contain at least one page from the excluded list; 24.4% of retrieved pages are from fact-checking sites.
- Section 5.3: only 30% of search URLs overlap when the same queries are issued two months apart.
- Section 6: 36.0% of questions unanswerable from the most faithful summaries.

## Relation to our project

- Quantifies how much of apparent performance comes from post-claim fact-checks: the closest analogue to our random-vs-causal gap, but for verification, not retrieval.
- Its search-engine non-stationarity finding (30% URL overlap) argues for a frozen, timestamped archive like MultiClaim rather than live search.
- Does NOT cover: PFCR (matching a post to an existing fact-check is the goal in our task, not a leak), ranking metrics, pool-size control, multilingual data.

## Verification

- OK. Note line "Chen et al., NAACL 2024 (temporal and fact-check-site constraints sharply reduce veracity accuracy, showing web retrieval works largely because it finds later fact-checks)" matches Table 2 and the paper's own wording.
