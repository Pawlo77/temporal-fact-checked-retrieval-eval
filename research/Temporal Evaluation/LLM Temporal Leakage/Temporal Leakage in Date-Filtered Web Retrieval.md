---
title: "Temporal Leakage in Date-Filtered Web Retrieval"
aliases: ["Temporal Leakage in Search-Engine Date-Filtered Web Retrieval: A Retrospective Forecasting Case Study"]
authors: ["Ali El Lahib", "Ying-Jieh Xia", "Zehan Li", "Yuxuan Wang", "Xinyu Pi"]
year: 2026
venue: "Proceedings of the 64th Annual Meeting of the Association for Computational Linguistics (Volume 2: Short Papers), pages 787-795"
arxiv: "2602.00758"
doi: "10.18653/v1/2026.acl-short.65"
url: "https://aclanthology.org/2026.acl-short.65/"
citekey: ellahib2026temporal
verified: 2026-10-27
theme: "[[LLM Temporal Leakage]]"
tags: [type/paper, theme/llm-leakage, topic/temporal, topic/leakage, topic/evaluation, topic/english]
---
# Temporal Leakage in Date-Filtered Web Retrieval

> [!info] TL;DR
> The paper audits Google's `before:` filter and DuckDuckGo's date-range filter, the usual way to keep retrieval before a cutoff in retrospective forecasting. For about 390 resolved questions, 71% (Google) and 81% (DuckDuckGo) have at least one retrieved page with major post-cutoff information, and 41% and 55% have a page that reveals the answer. A model given such pages reaches Brier 0.11 against 0.24 with leak-free pages.

## Motivation

- Retrospective forecasting scores a system on questions whose outcome is known, so the evidence it retrieves must predate the question. Most pipelines enforce this with a search-engine date filter or a scraped publication date (Halawi et al., 2024, and others), and the same assumption is used in claim verification and timeline retrieval.
- Earlier warnings that such filters leak rested on a few hand-picked examples (Paleka et al., 2026; FutureSearch et al., 2025). It was unclear whether leakage is rare or systematic.
- Fixed historical corpora give strong temporal control but their questions fall inside the knowledge of current models. Prospective benchmarks avoid leakage but must wait for outcomes.
- The failure is general: any retrieval evaluation that trusts a date filter, including a fact-check pool, can inherit it ([[Missing Counter-Evidence]] studies the same problem for verification evidence).

## Method

Notation: this paper's cutoff is the question's opening date; we call the retrieved page the document and keep the paper's "leakage" for information from after that cutoff.

**Audit.** For each Metaculus question an LLM writes 10 to 20 search queries from the title and background. About 100 unique URLs per question are retrieved through Google `before:` or DuckDuckGo with a date range from 2000-01-01 to the cutoff, and each page is fetched. Pages over 7,680 tokens are cut to 30 passages of 256 tokens chosen by maximal marginal relevance.

**Leakage severity.** An LLM judge (gpt-oss-120b, temperature 0.5) sees the question, resolution criteria, resolved answer, cutoff and page, and scores 0 (no relevant post-cutoff content) to 4 (directly reveals the answer). Absence-based signals are capped at 3.

Intuition: the question-level rate asks "could a forecaster find a decisive page", which is what matters because one page is enough to turn forecasting into lookup.

**Downstream test.** gpt-oss-120b forecasts 2025 binary questions with documents grouped by leakage level, compared by Brier score.

## Key numbers

- Major leakage (score 3 or more) in at least one page: 71.0% of Google questions, 81.2% of DuckDuckGo questions (393 and 389 questions).
- Answer directly revealed (score 4): 41.0% (Google) and 54.8% (DuckDuckGo).
- About a third of all retrieved pages carry some post-cutoff information: 33.2% of 38,879 (Google) and 34.5% of 34,454 (DuckDuckGo).
- Mean Brier on 93 questions: 0.244 with no retrieval and 0.242 with score-0 pages, against 0.108 with score 3-4 pages and 0.129 with score-4 pages only (0.25 is the 50% guess).

## Experiments

- **Leakage audit:** both engines on Metaculus questions resolving 2021 to 2025; almost every question (about 98%) has at least one topical post-cutoff page, and severe leakage is the majority case.
- **Impact on forecasting:** leak-free pages leave the model at its no-retrieval baseline; pages with strong leakage halve the Brier score. Several score-3 pages plus one score-4 page beat a score-4 page alone, because corroboration reduces misreads.
- **Mechanisms:** four recurring pathways, each with a worked example: pages updated after publication (a missile database first published in 2017 listing launches through 2023); related-article sidebars on an old article announcing a 2023 launch; absence of an event in a comprehensive timeline (no US-Iran war in a 1951 to 2025 timeline); and wrong self-reported timestamps (a page "last updated 2020" stating that Finland joined NATO in 2023). The last one defeats pipelines that re-check scraped dates.
- **Cutoff year:** the share of leaky URLs is above 46% for 2021 and 2022 cutoffs and 27% to 35% for 2023 and 2025. Older pages have had longer to be edited.

## Data

- 393 resolved Metaculus questions (2021 to 2025, none opened in 2024); 389 usable on DuckDuckGo.
- 38,879 Google URLs and 34,454 DuckDuckGo URLs, from queries generated per question.
- 134 documents double-annotated for judge validation: 76.1% exact agreement (scores 0 and 1 merged), quadratic weighted kappa 0.85, F1 0.82 for score 4.
- Questions, queries, URLs and audit period are released by the authors.

> [!failure] Limitations
> - Two engines and one platform; other retrievers may leak differently.
> - Judge and forecaster are the same model, so shared misreadings are possible.
> - Passage selection by maximal marginal relevance can drop scattered leakage, so rates may be underestimated.
> - Mitigation (Wayback retrieval, frozen snapshots) is recommended but not measured.
> - Questions concern world events, not fact-check retrieval; no ranking metric is studied.

## Relation to our project

- Supports our timestamp-leakage category: a publication or crawl date is not the date the content last changed, and fact-check pages are routinely edited after publication, so the fact-check time $t_f$ may be wrong. We keep a frozen archive with stored dates and audit a sample of dates by hand ([[Proposed Task]], [[Enhanced topic research]]).
- Related-content sidebars on a fact-check page can mention later claims; our text cleaning should strip them before indexing.
- The causal pool $P(q)$ must be built from stored timestamps, never from a live engine's date filter ([[LLM Temporal Leakage]]).
- Not covered: claim matching, fact-check archives and ranking metrics.

## Future work

- **Partly done:** evaluate mitigation by frozen snapshots; a Wayback-snapshot retrieval arm is statistically indistinguishable from date-filtered live retrieval on matched questions, and claim-level supervision reduces leakage further ([[All Leaks Count]]).
- **Open:** judges from a model family different from the forecaster, and full-page rather than passage-sampled audits (searched 2026-10).
- **Open:** the same audit on fact-checking and claim-retrieval pipelines (searched 2026-10).
