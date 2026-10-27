# 2025 - KInIT - MultiClaim v1 and v2 Zenodo records

## Citation

- Records: "MultiClaim: Multilingual Previously Fact-Checked Claim Retrieval" (v1.0) and "MultiClaim Dataset v2" (v2)
- Creators: not read from the record pages (the extract did not show the creator list); the v1 record links the EMNLP 2023 paper by Pikuliak et al. (KInIT); attribution of v2 to KInIT is inferred from the v1 "newer version" link and Ramponi et al. 2025 footnote 3, not from the v2 creator field.
- Venue: Zenodo, restricted access
- Year: v1 published 12 May 2023 (modified 6 Jun 2024); v2 published 19 May 2025
- URLs: https://zenodo.org/records/7737983 (v1), https://zenodo.org/records/15413169 (v2)
- Verified on: 2026-10-27

## What it does

- v1 files: `fact_check_post_mapping.csv` (fact_check_id, post_id); `fact_checks.csv` (fact_check_id, claim, instances, title); `posts.csv` (post_id, instances, ocr, verdicts, text).
- v1 text fields are "translated text" tuples: (original, English translation, detected-language list).
- v1 `instances`: fact-checks "a list of timestamps and URLs"; posts "a list of timestamps and what were the social media platforms" (the v1 page does not say "unix").
- v2 adds `relationship` in the mapping (claimreview_schema, backlink, or similarity:identical "for identical claims"), Google-Translate fields (`claim_en`, `title_en`, `post_body_en`, detected languages in BCP 47 and ISO 639), `ratings`, `claim_v1`/`title_v1`/`text_v1`, and anonymised `post_body`; `instances` described as "a list of unix timestamps and URLs following the MultiClaim v1 format".
- v2 fact-checks come from Google Fact Check Explorer and "a limited number of custom scrapers"; full fact-check texts are not published.
- Access terms (both): research purposes only; request from an official institutional e-mail; no attempt to identify, deanonymise or contact post authors; no re-sharing; cite the papers; accept that annotations may be wrong.

## Key numbers

- v1 description: "206k claims" and "28k social media posts".
- v2 description: "435k claims", "89k social media posts", "which were all published before April 2025", "105k pairs".
- Zenodo stats at read time: v1 all-version views 4,438 and downloads 788; v2 version views 1,693, downloads 321 (not relevant to research, listed only as read).

## Relation to our project

- Both records carry per-instance timestamps for posts and fact-checks, which is what a causal index needs; one fact-check can have several instances (several URLs), so `t_fc` must be defined (earliest vs other).
- The v2 relationship field lets us separate fact-checker links (claimreview_schema, backlink) from text-identity links (similarity:identical); Ramponi et al. 2025 used only the first two.
- Gap: neither record documents timestamp semantics (publication vs crawl vs update), time zone, or which instance is canonical; this is a real risk for our date filter.
- Access terms forbid re-sharing, so our release must be id lists, cutoffs and code.

## Verification

- Status: OK.
- Line 60: "435k fact-checks, 89k posts, 105k pairs, all published before April 2025; relationship types claimreview_schema, backlink, similarity:identical" matches v2. The page phrase "which were all published before April 2025" grammatically follows the posts clause; whether it also bounds fact-checks is not stated.
- Line 87: record ids 7737983 and 15413169 correct.
- Line 91-92: field descriptions correct for v2; for v1 the page says "timestamps" without "unix".
- Line 94: "similarity:identical pairs ... added by text identity, not by a fact-checker" is a reasonable reading of "(for identical claims)" but the record does not say who/what created them; mark as interpretation.
- Line 156: access terms correct.
- H3 (line 36): the record does not define `backlink` or say where Meta-warning pairs went; the claim "`backlink` pairs (fact-check body links the post)" and the mapping of Meta-warning pairs to `claimreview_schema` are unverified. The v1 paper (Section 3) describes two collection routes: ClaimReview links, and Facebook/Instagram URLs in fact-check bodies plus platform warnings.
