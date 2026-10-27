---
title: "MultiClaim Zenodo Records"
aliases: ["MultiClaim Dataset v2", "MultiClaim: Multilingual Previously Fact-Checked Claim Retrieval"]
authors: ["Robert Moro", "Ivan Srba", "Matúš Pikuliak", "Martin Melišek", "Juraj Podroužek", "Matúš Mesarčík", "Natália Slosiarová", "Jakub Simko", "Maria Bielikova"]
year: 2025
venue: "Zenodo, restricted-access dataset records (v1.0 published 2023-05-12; v2 published 2025-05-19)"
doi: "10.5281/zenodo.15413169"
url: "https://zenodo.org/records/15413169"
citekey: moro2025multiclaim
verified: 2026-10-27
theme: "[[Datasets and Benchmarks]]"
tags: [type/paper, theme/datasets, topic/multilingual, topic/benchmark, topic/temporal]
---
# MultiClaim Zenodo Records

> [!info] TL;DR
> Source type: two Zenodo dataset records, not papers. The v1 record distributes the [[MultiClaim]] data (206k fact-checks, 28k posts); the v2 record extends it to 435k fact-checks, 89k posts and 105k pairs, all posts published before April 2025. Both give timestamps per fact-check and per post instance, which is what a date-restricted pool needs; v2 adds a pair-provenance field and Google-Translate fields.

## Motivation

- The [[MultiClaim]] paper describes the data but the files, field formats and access terms live only on the records.
- Platforms remove flagged posts, so the records keep anonymised post text instead of URLs to prevent decay.
- v2 enlarges the data under new EU rules: the record argues that Article 40(12) of the Digital Services Act permits research on systemic risks such as disinformation.

## Method

We write a post as $q$ with time $t_q$ and a fact-check as $f$ with time $t_f$.

**v1 files.** `fact_check_post_mapping.csv` (fact-check id, post id); `fact_checks.csv` (claim, title, instances); `posts.csv` (text, OCR, Meta verdicts, instances). Text fields are tuples of original text, English translation and detected languages.

**Instances.** For fact-checks, "a list of timestamps and URLs"; for posts, timestamps and platforms. v2 states these are unix timestamps "following the MultiClaim v1 format".

Intuition: one fact-check may have several instances, so $t_f$ is a choice, not a given.

**v2 additions.** The mapping gains `relationship` with values `claimreview_schema`, `backlink` or `similarity:identical` ("for identical claims"). Fact-checks gain `claim_en`, `title_en`, detected languages in BCP 47 and ISO 639, `ratings` aggregated over instances, and v1-format copies. Posts gain an anonymised `post_body`, its translation and v1-format text; a small number of Telegram posts from public channels are included.

**Sources.** Fact-checks come from Google Fact Check Explorer and "a limited number of custom scrapers"; full fact-check texts are not published.

**Access.** Restricted: research use only, request from an institutional e-mail, no re-identification or contact of post authors, no re-sharing, cite the paper (and, for v2, the record).

## Key numbers

- v1 description: "206k claims" and "28k social media posts".
- v2 description: "435k claims", "89k social media posts" published before April 2025, "105k pairs".
- Files are not listed publicly on either record (restricted access).

## Experiments

- **None:** dataset records report no experiments; results on v1 are in [[MultiClaim]] and on v2 in [[Multilingual vs Crosslingual Retrieval]].

## Data

- MultiClaim v1.0 (record 7737983): fact-checks, posts and pairs of the EMNLP 2023 paper.
- MultiClaim v2 (record 15413169): 435k fact-checks, 89k posts, 105k pairs with provenance labels.

> [!failure] Limitations
> - Neither record defines what a timestamp means (publication, crawl or update time), its time zone, or which instance is canonical.
> - `backlink` is not defined, and the record does not say where v1's platform-warning pairs went in v2.
> - The "before April 2025" bound is stated for posts; whether it also bounds fact-checks is not said.
> - Translations and language labels are machine-made (Google Translate, Google Vision OCR).

## Relation to our project

- The timestamps are the basis of our causal pool $P(q) = \{f \in P : t_f < t_q\}$; we must fix a rule for $t_f$ (earliest instance) and report sensitivity to it ([[2026-10-27-temporal-retrieval-eval|Project plan]]).
- The `relationship` field lets us report results separately for fact-checker links and text-identity links ([[2026-10-27-topic-research|Topic research]]).
- v2 raises the Polish query count, which our power statement depends on ([[2026-10-27-language-scope|Language scope analysis]]).
- No re-sharing: our release can hold only ids, cutoffs and code ([[Datasets and Benchmarks]]).

## Future work

- **Partly done:** v2 used for multilingual vs crosslingual evaluation; [[Multilingual vs Crosslingual Retrieval]] (Ramponi et al., 2025) uses the claimreview and backlink pairs.
- **Open:** documented timestamp semantics and an official dated split of v2 (searched 2026-10).
