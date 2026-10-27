# 2023 - Pikuliak - MultiClaim

## Citation

- Authors: Matúš Pikuliak, Ivan Srba, Robert Moro, Timo Hromadka, Timotej Smoleň, Martin Melišek, Ivan Vykopal, Jakub Simko, Juraj Podroužek, Maria Bielikova (author list as given in the BibTeX on the MultiClaimNet Zenodo record)
- Title: Multilingual Previously Fact-Checked Claim Retrieval
- Venue: Proceedings of EMNLP 2023, pages 16477-16500
- Year: 2023
- URL: https://aclanthology.org/2023.emnlp-main.1027/ ; read via https://arxiv.org/html/2305.07991v2 and https://aclanthology.org/2023.emnlp-main.1027.pdf
- Verified on: 2026-10-27

## What it does

- Releases MultiClaim: fact-checks collected mostly via Google Fact Check Explorer plus missing major sources (e.g. Snopes), and social-media posts (Facebook, Instagram, Twitter) linked by fact-checkers through ClaimReview links and through Facebook/Instagram fact-check warnings (Section 3).
- Publishes claim, title, publication date and URL for each fact-check, not the article body.
- Evaluates unsupervised retrieval (BM25 on original/English text, English and multilingual text-embedding models) with Success@10; monolingual = pool restricted to the post's language; crosslingual = full pool (Section 4.1).
- Section 4.2 "Time": performance over 20 post-date quantiles, a COVID-19 drop, and a leak test comparing pairs where the post is newer vs older than the fact-check.
- Measures how pool size affects BM25 vs TEMs by adding random fact-checks to 100 pairs from 100 to 2,100 (Section 4.1, Figure 4).
- Supervised fine-tuning on a random 80:10:10 split of posts (Section 5); post-hoc manual annotation of top-10 outputs shows many unlabeled valid pairs (Section 6).

## Key numbers

- Section 1/3: 205,751 fact-checks, 39 languages, 142 organisations; 28,092 posts, 27 languages; 31,305 pairs; 26,774 monolingual and 4,212 crosslingual pairs (these two sum to 30,986, not 31,305; the paper does not reconcile this).
- Section 4.2: dates available for N = 26,337 posts; drop "at the start of 2020", attributed to COVID-19; correlation of quantile time with GTR-T5 minus BM25-English: Pearson ρ = -0.33, P = 0.17.
- Section 4.2: post-newer vs post-older groups "virtually the same performance (e.g., 80.02 vs 80.04 monolingual S@10 for GTR-T5)"; "If there is an information leak happening, we were not able to measure it."
- Section 9.1 Selection bias: "we know that there are at least few samples with this problem" (fact-check containing the post verbatim).
- Section 3 noise: 87 of 100 manually checked pairs correct; Section 9.1: about 13% of posts carry the claim only visually.
- Section 6: 87 test posts, 3,390 unique predictions, 719 correct pairs, 96 already in the dataset, "roughly 7x more pairs"; 247 monolingual, 136 crosslingual-English, 336 crosslingual non-English.
- Table 3: COVID-related monolingual N = 4,159, GTR-T5 0.72 vs otherwise 0.83.
- Table 5 (Appendix C): Polish 6,912 fact-checks, 453 posts; English 85,814 fact-checks, 7,307 posts; Turkish 6,676 fact-checks, 7 posts.
- Table 6: snopes.com 18,376; politifact.com 9,029; demagog.org.pl 4,292; oko.press 1,872; sprawdzam.afp.com 458; fakenews.pl 320.
- Table 10: Pearson correlation of S@10 with MRR 0.986, MAP 0.986, NDCG 0.993, MAP@10 1.000.
- Section 4.1: without the language filter BM25-Original vs MPNet S@10 51.9 vs 38.5.

## Relation to our project

- Not novel for us: a temporal analysis of MultiClaim already exists in three forms: post-date quantiles, the post-newer vs post-older leak test, and a pool-size sweep with random fact-checks. We must cite all three.
- The leak test keeps the full index and compares two subsets of gold pairs; it neither removes future fact-checks from the pool nor separates answerability from ranking, so it does not answer our RQ1.
- The pool-size sweep is a random-addition control (100 to 2,100), not a per-query size match to a causal pool; our size-matched control is an extension, not a first.
- The random 80:10:10 supervised split is the training-leakage baseline we contrast with (H5).
- Gap left: no causal (date-restricted) index, no answerable-only scoring, no time-to-findability.

## Verification

- Status: CORRECTED (counts and the 80.02 vs 80.04 claim are right; two framing claims need fixing).
- Line 56: counts 205,751 / 39 / 28,092 / 27 / 31,305 and "80.02 vs 80.04 S@10 for GTR-T5" are correct; the paper's figure is monolingual S@10. The note's statement that the analysis "keeps the full index" is consistent with the method described.
- Line 57: "COVID-19 drop at start of 2020" and "about 7x more valid pairs" correct.
- Line 76 and line 43: "MultiClaim itself shows performance falls as pool size grows" is not what was read: Figure 4 reports relative performance between BM25 and TEMs as the pool grows (BM25 gets relatively better), and Section 7 says COVID results are hurt by "the sheer amount" of similar fact-checks. Correct statement: MultiClaim ran a pool-size sweep (random fact-checks added, 100 to 2,100) showing pool size changes the BM25-vs-TEM gap; it did not report a per-query pool-matched control. "No prior PFCR evaluation has used" a pool-size control should be softened to "no prior PFCR evaluation matched pool size to a time-restricted pool".
- Line 88: Polish sources: add fakenews.pl 320 (Table 6). Konkret24 was not seen in the Table 6 rows read.
- Line 91/150: 26,337 dated posts, hence 1,755 undated, correct.
- Line 127: correlation above 0.98 correct (minimum 0.986).
- Line 144: "13 of 100 checked pairs" is close; the paper says 87/100 pairs were correct and extrapolates "~13% of posts" lack a textual claim.
