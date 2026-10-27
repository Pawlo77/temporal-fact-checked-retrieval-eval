# 2025 - Vykopal - Generative-AI-Driven Claim Retrieval System

Found while searching for prior time-aware PFCR work; not cited in the Enhanced topic research note.

## Citation

- Authors: Ivan Vykopal, Martin Hyben, Robert Moro, Michal Gregor, Jakub Simko
- Title: A Generative-AI-Driven Claim Retrieval System Capable of Detecting and Retrieving Claims from Social Media Platforms in Multiple Languages
- Venue: arXiv preprint 2504.20668 (submitted 29 Apr 2025); no peer-reviewed venue found in this pass
- Year: 2025
- URL: https://arxiv.org/abs/2504.20668 (HTML read)
- Verified on: 2026-10-27

## What it does

- Pipeline: embedding retrieval (Multilingual E5 Large best) on MultiClaim over 20 languages, LLM filtering of the top 50, LLM summaries of fact-check articles (AFP-Sum, about 19K AFP articles in 23 languages, up to September 2023), veracity explanation; a web tool with a Milvus store of fact-checks in over 80 languages.
- "Criteria-based retrieval": fact-checks embedded with a metadata template (claim, language, publication date, organisation); a natural-language criterion (language, date range, domain, named entity) retrieves items with similarity above 0.8, then the post re-ranks them. Ground truth is E5 ranking over a subset filtered by a manual (exact) filter.
- Finds that filtering by language, domain and date range lowered agreement with the reference ranking, date range worst, because embeddings only contained the exact date.

## Key numbers

- The text read gives no date-range scores in numbers (Table 3 values not extracted); only the ordering "date range performing the worst".

## Relation to our project

- Not a causal evaluation: date is a user-supplied filter applied through embeddings, and the reference ranking already uses an exact date filter; there is no comparison of time-restricted vs full pools as an evaluation protocol.
- Relevant engineering point: date filtering must be done as an exact metadata filter, not through embeddings (our protocol already does this).
- It shows the KInIT group thinks about date-filtered retrieval; our overlap risk note (line 158) should mention it.

## Verification

- Status: OK (new paper).
- Supports, with caveat, the Enhanced note's claim that no prior PFCR work uses a causal index: this is the closest found, and it is a retrieval feature, not an evaluation protocol.
