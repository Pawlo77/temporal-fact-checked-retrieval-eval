---
title: "Complex Claim Verification in the Wild"
aliases: ["Complex Claim Verification with Evidence Retrieved in the Wild"]
authors: ["Jifan Chen", "Grace Kim", "Aniruddh Sriram", "Greg Durrett", "Eunsol Choi"]
year: 2024
venue: "Proceedings of the 2024 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers), pages 3569-3587"
arxiv: "2305.11859"
doi: "10.18653/v1/2024.naacl-long.196"
url: "https://aclanthology.org/2024.naacl-long.196/"
citekey: chen2024complex
verified: 2026-10-27
theme: "[[Leakage in Verification]]"
tags: [type/paper, theme/verification-leakage, topic/leakage, topic/temporal, topic/evaluation, topic/english]
---
# Complex Claim Verification in the Wild

> [!info] TL;DR
> A five-stage pipeline checks complex political claims with raw web evidence that was published before the claim and does not come from fact-checking sites. Dropping either restriction raises test accuracy from 33 to 49, so apparent success of unconstrained web retrieval comes largely from post-claim fact-checks. Under the realistic setting evidence still beats claim-only input (33.0 vs 25.5), and the summaries are mostly faithful but rarely cover every aspect of a claim.

## Motivation

- Prior work on real claims either uses evidence curated by the fact-checker, uses no evidence, or retrieves without restriction ([Augenstein et al., 2019](https://aclanthology.org/D19-1475/)), which returns fact-check pages ([[Missing Counter-Evidence]]).
- Systems that only see the claim learn surface patterns, not factual errors.
- Question-driven retrieval with live search had only been evaluated with humans filtering results ([Fan et al., 2020](https://doi.org/10.18653/v1/2020.emnlp-main.580)); the concurrent [[AVeriTeC]] builds a dataset with the same pre-claim restriction but wh-questions.

## Method

Notation: the claim date plays the role of $t_q$; a retrieved page with date $t_d$ is allowed only if $t_d < t_q$ (the causal condition) and, in the site-constrained setting, its site is not on a fact-checking list.

**Pipeline.** (1) text-davinci-003 decomposes the claim into 10 yes/no subquestions from four in-context examples. (2) Each subquestion goes to the Bing Search API, 10 pages after the constraints; about a third of URLs cannot be scraped. (3) Pages are cut into 30-word spans; BM25 picks the top 10 spans, expands each by 150 words, and the top 4 merged passages are kept. (4) The language model writes a claim-focused summary per document without judging the stance. (5) A DeBERTa-large classifier labels claim plus summaries with one of six PolitiFact labels.

Intuition: the temporal and site constraints remove exactly the documents a real checker would not have when the claim first appears.

**Constraints.** Temporal (pages before the claim date), site (no fact-checking domains), both, or neither; PolitiFact itself is excluded in every setting to avoid label leakage.

## Key numbers

- Test accuracy by retrieval constraint: none 49.0, site only 33.5, temporal only 33.5, both 33.0, claim only 25.5; dev 50.5, 37.5, 42.5, 40.5, 37.0.
- Claim plus human justification (oracle): 57.5 test accuracy.
- 82.7% of MultiFC claims (12,721 of 15,379) have at least one page from the excluded list; 24.4% of retrieved pages are from fact-checking sites.
- Same queries two months apart: only 30% of result URLs overlap (Jaccard 0.30); veracity accuracy changes insignificantly (33.0 to 29.5).

## Experiments

- **Constraint comparison:** all four constraint settings against claim-only and oracle; every retrieval setting beats claim-only on most metrics, but either constraint costs 15 to 16 points of test accuracy against unconstrained.
- **Stage ablations:** original claim instead of subquestions in the first stage drops accuracy to 24.5, so decomposition matters; second-stage queries (claim, gold subquestions, justification) change little; no summarisation gives 29.0.
- **Temporal filter effect:** with and without the date filter, retrieved URL sets have Jaccard 0.12, so the filter changes the evidence substantially.
- **Retrieval stability:** repeated Bing queries after one week (overlap 0.48) and two months (0.30); the authors advise a released, fixed document set.
- **Faithfulness (200 summaries, MTurk):** few-shot prompting gives 82.5% faithful against 66.0% zero-shot; kappa 0.30.
- **Comprehensiveness (161 subquestions, 50 claims):** few-shot summaries answer 42.9% fully and 21.1% partly; 36 of 50 claims have at least one unanswerable subquestion.

## Data

- ClaimDecomp: 1,200 PolitiFact claims (train 800, dev 200, test 200), six veracity labels, justifications and about three gold subquestions per claim.
- MultiFC: 15,379 claims with Google results, used only to measure fact-check contamination.

> [!failure] Limitations
> - Performance is bottlenecked by first-stage retrieval; 36.0% of questions stay unanswerable even from faithful summaries.
> - Some claims need contact with people and are not checkable from the web.
> - Commercial search is not reproducible over time, and about a third of pages cannot be scraped.
> - English political claims only; social-media claims and other languages are untested.
> - Faithfulness and comprehensiveness agreement is low (kappa 0.30 and 0.32), and the date constraint relies on engine-reported dates.

## Relation to our project

- It quantifies how much apparent performance comes from post-claim fact-checks, the closest verification analogue of our random-versus-causal gap ([[2026-10-27-temporal-retrieval-eval|Project plan]]; [[2026-10-27-topic-research|Topic research]]).
- Its search non-stationarity finding argues for a frozen, timestamped archive such as [[MultiClaim]] over live search ([[Leakage in Verification]]).
- In PFCR a fact-check for the post is the goal, not a leak, so its site constraint does not transfer; only the time constraint does ([[2026-10-27-language-scope|Language scope analysis]]).
- It does not cover ranking metrics, pool size or multilingual data.

## Future work

- **Done:** a realistic benchmark with pre-claim web evidence, released as a dataset so retrieval can be compared; [Schlichtkrull et al., 2023](https://arxiv.org/abs/2305.13117) ([[AVeriTeC]]) is concurrent.
- **Open:** human-in-the-loop checking where fact-checkers rerun searches and the system learns which questions matter (searched 2026-10).
- **Open:** claim triage for claims that cannot be checked from the web, and extension to social-media claims and other languages (searched 2026-10).
