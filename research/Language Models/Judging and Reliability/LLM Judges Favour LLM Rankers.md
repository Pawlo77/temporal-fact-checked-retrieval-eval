---
title: "LLM Judges Favour LLM Rankers"
aliases: ["Rankers, Judges, and Assistants: Towards Understanding the Interplay of LLMs in Information Retrieval Evaluation"]
authors: ["Krisztian Balog", "Donald Metzler", "Zhen Qin"]
year: 2025
venue: "Proceedings of the 48th International ACM SIGIR Conference on Research and Development in Information Retrieval (SIGIR 2025), pages 3865-3875"
arxiv: "2503.19092"
doi: "10.1145/3726302.3730348"
url: "https://doi.org/10.1145/3726302.3730348"
citekey: balog2025rankers
verified: 2026-10-27
theme: "[[Judging and Reliability]]"
related: ["[[2026-10-27-temporal-retrieval-eval]]", "[[LLM selection]]", "[[LLM Relevance Judgments Can Be Gamed]]", "[[Self-Preference Bias]]", "[[Panel of LLM Evaluators]]"]
tags: [type/paper, theme/llm-judging, topic/judge-bias, topic/evaluation, topic/reranking, topic/english]
---
# LLM Judges Favour LLM Rankers

> [!info] TL;DR
> The paper tests whether LLM relevance judges favour systems that are themselves built on LLMs. On TREC Deep Learning, the strongest Gemini judges score every LLM reranker above oracle rankings that humans rate higher, so the bias is large enough to reverse the order. The judges also fail to separate close systems, and no bias towards LLM-rewritten text appears.

## Motivation

- LLMs now rank, judge and help write documents, and nobody had measured how an LLM ranker influences an LLM judge.
- Agreement of LLM labels with human labels is the usual evidence of validity, but it says little about systems unlike the judge ([Upadhyay et al., 2024](https://arxiv.org/abs/2411.08275)).
- Earlier work found LLMs favour their own generations ([Liu et al., 2023](https://arxiv.org/abs/2311.09766); [[Self-Preference Bias]]), and the question here is whether the effect carries over from text to ranking systems.

## Method

Notation: a judge assigns a relevance grade to each passage in a system's top 10, and system quality is NDCG@10 computed from those grades instead of human grades.

**Reranking setup.** Every ranker reorders the top 100 BM25 passages. Passages without a TREC judgment are dropped rather than counted as non-relevant, so humans and LLMs score the same pairs.

**Oracle rankers.** The Perfect oracle sorts the BM25 candidates by human grade. Swap[i] exchanges the top i results with the bottom i, and Swap[i,i+1] degrades the list further. All pairs of oracles differ significantly under human labels, so they test judge sensitivity without any LLM ranker present.

**Judges.** Four Gemini models (v1 Nano, v1 Pro, v1.5 Flash, v1.5 Pro) use the UMBRELA prompt on a 4-point scale, with temperature 0 and top-p 1.

Intuition: because oracles contain no LLM, any judge that ranks LLM rankers above a better oracle is rewarding the system type rather than relevance.

## Key numbers

- On DL19 with the v1.5 Pro judge, PRP with Gemini v1.5 Flash scores 0.947 and RankT5 0.916, while the Perfect oracle scores 0.864; human judges give 0.747, 0.731 and 0.892.
- Agreement with humans on grades (Cohen's $\kappa$): v1 Nano is near 0 (-0.002 graded, DL19), v1.5 Flash reaches 0.268 graded and 0.461 binary, v1.5 Pro 0.204 and 0.462.
- Kendall's $\tau$ with human system order over all systems is only 0.077 (DL19) and 0.143 (DL20) for v1.5 Pro, yet 0.600 and 0.867 on the oracles alone.
- Perfect oracle with LLM-rewritten passages: NDCG@10 of 0.868 against 0.883 on DL19 and 0.825 against 0.818 on DL20, not significant.

## Experiments

- **Choice of judge:** four Gemini variants compared with TREC assessors; the three largest agree on system order, v1 Nano is unusable, and the larger v1.5 Pro is not clearly better than v1.5 Flash.
- **Discriminative ability:** the v1.5 Pro judge misses the difference between RankT5 and RG with FLAN-T5-XXL on DL19, which humans find at $p<0.001$, and reports a significant gap between two PRP systems where humans find none.
- **Bias towards LLM rankers:** human labels place the selected oracles above all LLM rankers; the LLM judges invert that order completely, and BM25 is rated 0.712 against 0.506 by humans.
- **Bias towards LLM text:** 4,000 balanced query-passage pairs are rewritten by Gemini v1.5 Flash and rejudged; rewrites do not receive higher grades, and a RankT5 ranker scores original and rewritten text almost identically.

## Data

- TREC Deep Learning 2019 and 2020: 43 and 54 queries with TREC assessor labels over the MS MARCO v1 passage corpus of 8.8 million passages.
- Rewrite sample: 500 query-passage pairs per relevance level and year, 4,000 in total.

> [!failure] Limitations
> - All judges are Gemini models, and the only LLM ranker from the same family is one PRP configuration, so family effects are not separated from "any LLM" effects.
> - The paper calls the study preliminary: one task, passage-level pointwise judging and reranking of BM25 candidates only.
> - The no-bias result for LLM-written text holds for one rewriter and one judge from the same family.
> - Correlations over many systems are shown to depend on which systems are included, so no single $\tau$ summarises judge quality.

## Relation to our project

- This is the main evidence behind judge families that are disjoint from every evaluated and pooled system ([[LLM selection]]); an LLM reranker in the pool would otherwise be rewarded for being an LLM.
- Cluster-expanded relevance sets built from pooled system outputs are exactly this setting, so every system is also scored against fact-checker-only qrels and the expanded ones are reported as a bound ([[2026-10-27-temporal-retrieval-eval|Project plan]]).
- We adopt its guidance: one judge configuration for all systems, no selective filling of unjudged items, stated model versions, and human validation on a sample.
- Agreement statistics must be reported among top systems, not only over all of them, because the paper shows that all-system correlation hides weak discrimination ([[LLM Relevance Judgments Can Be Gamed]]).
- The panel idea follows [[Panel of LLM Evaluators]]; per-language validity is checked on [[AMC-16K]].

## Future work

- **Partly done:** circularity and gaming of LLM judges, which the authors flag as adversarial robustness; [Clarke and Dietz](https://arxiv.org/abs/2412.17156) simulate it on TREC RAG 2024 ([[LLM Relevance Judgments Can Be Gamed]]).
- **Partly done:** judging with several model families to dilute family favouritism; [Pombal et al., 2026](https://arxiv.org/abs/2604.06996) show ensembling helps without removing the bias ([[Rubric Self-Preference]]).
- **Open:** a test with judges from several families against rankers from each family, which would separate same-family from LLM-versus-non-LLM bias (searched 2026-10).
- **Open:** judging longer documents and non-English text, which the paper lists as untested (searched 2026-10).
