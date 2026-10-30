---
title: "Dated Data"
aliases: ["Dated Data: Tracing Knowledge Cutoffs in Large Language Models"]
authors: ["Jeffrey Cheng", "Marc Marone", "Orion Weller", "Dawn Lawrie", "Daniel Khashabi", "Benjamin Van Durme"]
year: 2024
venue: "First Conference on Language Modeling (COLM 2024)"
arxiv: "2403.12958"
url: "https://arxiv.org/abs/2403.12958"
citekey: cheng2024dated
verified: 2026-10-27
theme: "[[LLM Temporal Leakage]]"
tags: [type/paper, theme/llm-leakage, topic/temporal, topic/leakage, topic/llm, topic/evaluation]
---
# Dated Data

> [!info] TL;DR
> A model's reported training cutoff is not the date its knowledge of a given resource stops. The paper estimates a resource-level effective cutoff from the minimum of perplexity over dated versions of the text, without access to the training data. For newer open models the effective cutoff is often years earlier than the reported one, because old data hides in recent web crawls and deduplication misses near copies.

## Motivation

- Developers publish one cutoff date per model, but a model may hold several versions of a resource, some outdated or conflicting with newer ones.
- Documentation and membership-inference work ask whether a text was in the training set, not which version of it was.
- Users of a model for up-to-date answers can be misled: the paper's example is tax advice built on a 2022 rule although the reported cutoff is 2023.
- For leakage-aware evaluation, a stratum defined by the reported date is only as good as that date, so the boundary itself needs checking.

## Method

Notation: we write a model's reported cutoff as $K(m)$ and its effective cutoff for resource $r$ as $K_{eff}(m, r)$; the paper does not use our query notation.

**Time-spanning probes.** WikiSpan holds the 5,000 most-edited English Wikipedia pages, one version per month from April 2016 to April 2023; it stands for a resource that is updated in place. NewsSpan holds New York Times articles from CommonCrawl, 500 per month from January 2016 to July 2020; it stands for a resource that grows over time.

**Effective cutoff.** For every month, take perplexity on the first 512 tokens of each Wikipedia page (256 for news), average after dropping the lowest and highest 2.5%, and min-max scale across months to get relative perplexity. $K_{eff}(m, r)$ is the month where relative perplexity is lowest.

Intuition: a model has seen text from the months it knows best, so its surprise on that month's version of the resource is smallest.

**Ground truth from open data.** For models with released pretraining data, the authors index about 4T tokens with BM25 and query with the first 512 words of each page. Among the top ten hits, a document counts as a version of the page if its normalised edit distance to some monthly version is below 0.2, and it is assigned to the closest month. The resulting histogram of versions should mirror the perplexity curve upside down.

## Key numbers

- Pile-trained models (Pythia, GPT-Neo, GPT-J) reach minimum perplexity at March 2020, exactly their Wikipedia dump date; the dump is upsampled three times.
- RedPajama has a minimum around mid-2019, although its Wikipedia dump is from January 2023; over 80% of its Wikipedia-like documents are pre-2023 versions.
- On NewsSpan every Pile-trained model's perplexity rises in early 2020, the date of the last CommonCrawl dump in the Pile, so the news cutoff matches the reported one.
- Perplexity curves keep the same minimum with only 50 or more documents per month, and across Pythia 460M to 12B and LLaMA 7B to 65B.

## Experiments

- **NewsSpan:** perplexity of the Pile-trained models rises in early 2020, matching the last CommonCrawl dump they saw.
- **WikiSpan, Pile models:** a sharp minimum at March 2020 for GPT-Neo, GPT-J and Pythia; the effective cutoff equals the reported Wikipedia date.
- **WikiSpan, FalconRW:** a low band from late 2019 to early 2021 with a minimum near January 2020, although RefinedWeb excludes the wikipedia.org domain; copies on other domains remain.
- **WikiSpan, C4-derived models:** LLaMA falls within its 2017 to 2020 dumps, RedPajama a few months later, OLMo (20 dumps from 2019 to 2023) latest; all are biased towards the April 2019 C4 dump.
- **Deduplication audit:** near and exact duplicates of Wikipedia pages survive in FalconRW, C4 and RedPajama despite their filters.
- **Pythia against deduplicated Pythia:** removing the upsampled Wikipedia dump erases the sharp minimum and moves the effective cutoff earlier.
- **Closed-data models (appendix):** Mistral and LLaMA-2 show much earlier effective Wikipedia cutoffs; Gemma shows a much later one, roughly 2021 by the authors' reading. These are unverifiable speculation.

## Data

- WikiSpan: 5,000 most-edited Wikipedia pages (100 pages absent in 2016 filtered out), monthly versions, April 2016 to April 2023.
- NewsSpan: nytimes.com articles from 20 recent CommonCrawl dumps, 500 per month, January 2016 to July 2020.
- Open pretraining sets searched: C4, the Pile, RefinedWeb and RedPajama, indexed for the ground-truth analysis.

> [!failure] Limitations
> - Only Wikipedia and one news outlet are probed; no fact-check sites or claim text.
> - Needs token probabilities, so closed API models cannot be tested directly.
> - Most models are older open models; the newest results (Gemma, Mistral) are appendix speculation without data to confirm them.
> - Minima are not always sharp, so the effective cutoff is a distribution over months, not a date.
> - NewsSpan stops in mid-2020 because CommonCrawl removed the outlet, so recent models are not tested on news.

## Relation to our project

- It supports stratifying RQ4 by each model's own effective cutoff and not by a reported date, and it argues against Qwen3 treated as having a known boundary ([[2026-10-27-temporal-retrieval-eval|Project plan]], [[LLM selection]]).
- We could run the same perplexity-over-time probe on fact-check articles published by the sources in [[MultiClaim]] for the open models in the plan, as a check of when exposure ends; the paper does not do this.
- Treat a band around the reported cutoff as ambiguous and report it separately, because old copies and late additions blur the boundary in both directions.
- Complements [[Simulated Ignorance Fails]], which shows prompts cannot enforce a cutoff, and [[All Leaks Count]], which audits what the model says rather than what it holds.

## Future work

- **Open:** effective cutoffs for fact-check text and other claim-level resources instead of Wikipedia and news (searched 2026-10).
- **Open:** a probe that works for models without exposed token probabilities, such as API-only systems (searched 2026-10).
- **Open:** effective-cutoff estimates for the models released after 2023, with their training data inspected (searched 2026-10).
