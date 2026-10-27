---
title: "Original Task"
type: handbook
domain: vault
parent: "[[temporal-fact-checked-retrieval-eval]]"
tags: [handbook, task]
created: 2026-10-27
updated: 2026-10-27
related:
  - "[[Proposed Task]]"
  - "[[compute]]"
---
# Original Task

Course project 2 of the NLP course (Warsaw University of Technology): **Retrieval that cannot see the future: temporal evaluation of fact-checked claim retrieval**. Supervisor: Soveatin Kuntur (M.Sc. Eng.). Difficulty: Hard (16/25). Availability: Wednesdays only, during NLP course hours. Max 2 teams: one on sparse and dense retrieval baselines, one on reranking and gap decomposition; one shared split, one shared results table.

## Research question

How much of the reported performance of previously fact-checked claim retrieval survives a temporal split, where the index contains only fact-checks published before the query post?

## Why it matters

The task is evaluated on random splits, so a system can be rewarded for matching a post against a debunk written days later about the same wording. Fact-checkers work strictly forward in time, so published scores may overstate what the tools deliver in practice.

## Data (status: READY, one access request must go out in October)

- [[MultiClaim]] ([[MultiClaim|Pikuliak et al.]], EMNLP 2023): 206k fact-checks in 39 languages, 28k social media posts, 31k post-to-fact-check pairs, all carrying publication dates. Repository `github.com/kinit-sk/multiclaim`; the Zenodo record is access-restricted, so request access in October rather than November.
- [[AMC-16K]] (Vykopal et al.): curated 16k-pair subset across 20 languages. [[SemEval-2025 Task 7]] release, derived from [[MultiClaim]]. Both usable as secondary evaluation sets.
- Polish is the focus, English the control. Poland has a small fact-check ecosystem (Demagog, Konkret24, AFP Sprawdzam, Fakehunter), so a thin national index should make the temporal penalty worse for Polish queries than for English ones. That contrast is the result; without the control there is no claim.

## What we will do

- Implement the temporal split: index only fact-checks published before each query post's date, everything else identical to the standard protocol. Release the split.
- Rerun at least four standard systems (BM25, a multilingual dense retriever, a bilingual or cross-lingual encoder, a cross-encoder reranker) under the random and the temporal protocol, on Polish and English. Report Success@10 and MRR with significance tests over query bootstraps.
- Decompose the gap: time lag between post and debunk, lexical overlap, narrative drift. Inspect 50 newly-failing queries by hand.

## Success criteria

- Released temporal-split protocol and code that reproduces both evaluations from public data.
- Results table of at least four systems under both protocols for Polish and English, with significance tests. Central number: how much more the temporal split costs Polish.
- Gap decomposition plus a qualitative analysis of 50 newly-failing queries.

## Out of scope

Proposing a new retrieval architecture, judging claim veracity, and language-bias analysis (already published on this dataset).

## Starting point

[[That is a Known Lie|Shaar et al. 2020]] introduced the task, [[MultiClaim]] scaled it to 39 languages, [[SemEval-2025 Task 7]] ran on it. Retrieval on Polish is not new and must not be claimed as such. New this year: the temporal evaluation protocol and the size of the gap it exposes.

## Data and ethics

Public texts and published fact-checks. A retrieval system can make a named journalist or outlet look like a disinformation source: report errors in aggregate, publish no ranked list of suspect outlets or authors. Respect the [[MultiClaim]] access terms in any release.

## Skills

Python, information retrieval (BM25, dense retrievers, cross-encoder reranking), evaluation with bootstrap significance tests.

## Difficulty dimensions

| Dimension | Value (1-5) | Basis |
|---|---|---|
| D1 Data work | 2 | [[MultiClaim]] as released; one access request (Zenodo) and a temporal split of existing data |
| D2 Compute and infrastructure | 3 | BM25, multilingual dense, cross-lingual encoder and cross-encoder over 206k fact-checks, Polish and English |
| D3 Technical depth | 3 | Four retrieval systems including reranking |
| D4 Methodological demands | 5 | Protocol design, bootstrap significance tests, 4+ systems, manual analysis of 50 failures, gap decomposition |
| D5 External dependencies and risks | 3 | Restricted Zenodo record, [[MultiClaim]] access terms, risk of exposing named outlets or journalists |
| Total | 16 | Hard |
