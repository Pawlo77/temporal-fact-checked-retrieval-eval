---
title: "AMC-16K"
aliases: ["Large Language Models for Multilingual Previously Fact-Checked Claim Detection"]
authors: ["Ivan Vykopal", "Matúš Pikuliak", "Simon Ostermann", "Tatiana Anikina", "Michal Gregor", "Marian Simko"]
year: 2025
venue: "Findings of the Association for Computational Linguistics: EMNLP 2025, Suzhou, pages 15741-15765"
arxiv: "2503.02737"
doi: "10.18653/v1/2025.findings-emnlp.852"
url: "https://aclanthology.org/2025.findings-emnlp.852/"
citekey: vykopal2025large
verified: 2026-10-27
theme: "[[Datasets and Benchmarks]]"
tags: [type/paper, theme/datasets, topic/llm, topic/multilingual, topic/polish, topic/benchmark, topic/evaluation]
---
# AMC-16K

> [!info] TL;DR
> The paper frames PFCR as binary relevance classification of retrieved post-fact-check pairs and releases AMC-16K: 16,000 human-labelled pairs from [[MultiClaim]] in 20 languages and 20 language pairs. Seven open LLMs (7B to 123B) with five prompting strategies reach Macro F1 above 80% at best; they do worse on low-resource, Slavic and non-Latin-script languages, and English translation helps most models.

## Motivation

- [[MultiClaim]] labels are not exhaustive, so only precision-style evaluation is sound and recall cannot be measured.
- Prior LLM work on PFCR was single-language and used entailment labels or generative reranking ([Choi and Ferrara, 2024](https://doi.org/10.1145/3589335.3651504)), which do not match a fact-checker's broader notion of relevance.
- Fact-checkers in smaller languages need crosslingual matches, where embedding similarity alone gives many false positives.

## Method

We write a post as $q$ and a fact-checked claim as $f$.

**Relevance.** $f$ is relevant to $q$ if it can help verify $q$, whether it supports or refutes it; this covers entailment, contradiction, partial overlap and generalisation.

Intuition: a fact-check is useful if a fact-checker would open it, not only if it paraphrases the post.

**Pipeline.** A retriever ([[Multilingual E5]] Large) returns the top $N$ claims; an LLM labels each $(q, f)$ relevant or not, filtering false positives.

**Sampling.** Monolingual: 40 posts per language, top 10 same-language claims each, giving 400 pairs per language. Crosslingual: top 100 claims in other languages per post, 400 pairs per language combination. Posts with visual content via links or embedded media were skipped.

**Annotation.** Six annotators label Yes, No or Cannot tell, one label per pair; an author resolves Cannot tell. Fleiss' kappa is 0.60 on a pre-annotation test and 0.62 on a post-annotation test.

**Models and prompts.** Mistral Large 123B, Command R+ 104B, Qwen2.5 72B, Llama3.1 70B and 8B, Qwen2.5 7B, Mistral 7B; zero-shot, zero-shot with task description, few-shot (5 relevant, 5 irrelevant demonstrations chosen by similarity), chain-of-thought, cross-lingual-thought. Baselines: E5 and GTR-T5 with thresholds set by Youden's index, and two DeBERTa NLI models. Metrics: Macro F1, true negative rate, false negative rate.

## Key numbers

- Best Macro F1: Mistral Large few-shot 82.46 monolingual and 80.54 crosslingual on original text, vs the best baseline E5 on translations at 77.53 and 68.45.
- Crosslingual Macro F1 is on average about 4.5% lower than monolingual.
- English translation raises Llama3.1 few-shot Macro F1 by about 16%; it lowers Command R+, which covers more languages in training.
- 16% of pairs are relevant overall; above 30% for English, Malay, Portuguese and German; Polish monolingual 20.25%.
- Retrieval on the same posts: E5 Large Success@10 0.74 on MultiClaim labels vs 0.87 on AMC-16K labels, the gap coming from added human-found pairs.

## Experiments

- **Model size:** 70B+ models beat smaller ones significantly; Qwen2.5 7B with chain-of-thought is the best small model.
- **Prompting:** few-shot is best for Mistral Large and Qwen2.5 72B; chain-of-thought is best for small models and narrows the crosslingual gap by 5% relative to cross-lingual-thought.
- **Languages:** monolingual scores are lowest for Slavic languages, Hungarian and Burmese; differences persist after translation, so data difficulty also matters.
- **Output errors:** Llama3.1 answered in a non-English language in 37% (8B) and 28% (70B) of chain-of-thought outputs; Polish caused the most such errors (568).
- **Reasoning errors:** in 420 reviewed misclassifications, about 65% were false relevance from shared topic only, often COVID-19 or vaccination.

## Data

- AMC-16K: 8,000 monolingual pairs (20 languages, including Polish with 400 pairs) and 8,000 crosslingual pairs (20 combinations, including pol-hbs, ces-pol and hun-pol), drawn from [[MultiClaim]] v1.
- Polish posts in AMC-16K: 71, with 808 distinct fact-checked claims.
- Seed set from [[MultiClaim]]'s post-hoc annotation (3,390 pairs) used for few-shot demonstrations and model selection.

> [!failure] Limitations
> - Pairs are sampled from one retriever's top ranks, so labels are biased toward that retriever and recall stays approximate.
> - One annotator per pair; agreement is moderate to substantial.
> - Only open models released before July 2024; 70B+ models were quantised.
> - Pairs carry no date constraint: a labelled-relevant fact-check may postdate its post.

## Relation to our project

- Human relevance labels beyond fact-checker links are not new; AMC-16K is the precedent for our sibling qrels ([[Datasets and Benchmarks]]).
- The 400 Polish pairs can validate our LLM relevance judge on Polish before we trust it on sibling fact-checks ([[2026-10-27-temporal-retrieval-eval|Project plan]]).
- The topic-similarity false positives warn that an LLM judge may over-label same-topic earlier fact-checks as relevant ([[Topic research]]).
- Lower Slavic scores support treating Polish as a hard language rather than assuming parity with English ([[Language scope]]).

## Future work

- **Done:** language and retrieval bias analysis on AMC-16K; [[Language and Retrieval Bias]] (Vykopal et al., 2026).
- **Open:** closed-source and newer LLMs as relevance judges for multilingual PFCR (searched 2026-10).
- **Open:** date-aware relevance labels, marking whether the relevant fact-check existed at post time (searched 2026-10).
