# 2026 - El Lahib - Temporal Leakage in Date-Filtered Web Retrieval

## Citation

- Authors: Ali El Lahib, Ying-Jieh Xia, Zehan Li, Yuxuan Wang, Xinyu Pi
- Title: Temporal Leakage in Search-Engine Date-Filtered Web Retrieval: A Retrospective Forecasting Case Study
- Venue: Proceedings of ACL 2026 (Volume 2: Short Papers), San Diego, pages 787-795, DOI 10.18653/v1/2026.acl-short.65
- Year: 2026
- URL: https://aclanthology.org/2026.acl-short.65/
- Verified on: 2026-10-27 (Anthology page read; the paper exists with this title and venue)

## What it does

- Audits Google Search's `before:` filter and DuckDuckGo's date-range filter, used to enforce pre-cutoff retrieval in retrospective forecasting evaluations.
- Measures how often retrieved pages contain post-cutoff information and how often the answer is directly revealed.
- Forecasts with gpt-oss-120b on leaky vs leak-free documents to show inflated accuracy.
- Characterises leakage mechanisms: updated articles, related-content modules, unreliable metadata, absence-based signals.
- Recommends stronger safeguards or evaluation on frozen, time-stamped web snapshots.

## Key numbers

- Abstract: at least one retrieved page has major post-cutoff leakage for 71% of questions (Google) and 81% (DuckDuckGo); the answer is directly revealed for 41% and 55%.
- Abstract: Brier score 0.10 with leaky documents vs 0.24 leak-free.

## Relation to our project

- Supports our "timestamp leakage" category: publication-date metadata and page updates move documents across a cutoff. Fact-check pages are frequently updated, so `t_fc` from crawl or last-modified dates may be wrong.
- Supports using a frozen archive with stored timestamps and a date-audit sample.
- Does NOT cover: claim matching, fact-checking archives, ranking metrics.

## Verification

- OK. The paper exists at the cited URL; note line "date-filtered web search still leaks post-cutoff information (ACL 2026 short)" is correct. Reference list entry should add authors (El Lahib et al.).
