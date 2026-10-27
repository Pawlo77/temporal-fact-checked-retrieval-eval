---
title: "Generative-AI Claim Retrieval"
aliases: ["A Generative-AI-Driven Claim Retrieval System Capable of Detecting and Retrieving Claims from Social Media Platforms in Multiple Languages"]
authors: ["Ivan Vykopal", "Martin Hyben", "Robert Moro", "Michal Gregor", "Jakub Simko"]
year: 2025
venue: "arXiv preprint arXiv:2504.20668"
arxiv: "2504.20668"
url: "https://arxiv.org/abs/2504.20668"
citekey: vykopal2025generative
verified: 2026-10-27
theme: "[[Methods and Systems]]"
tags: [type/paper, theme/methods, topic/multilingual, topic/polish, topic/dense-retrieval, topic/llm]
---
# Generative-AI Claim Retrieval

> [!info] TL;DR
> The paper builds a four-step PFCR assistant: embedding retrieval, LLM filtering of irrelevant fact-checks, LLM summaries of fact-check articles, and LLM veracity prediction. Multilingual E5 Large is the best retriever (average Success@10 0.84 over 20 MultiClaim languages). LLM filtering removes about 90% of irrelevant fact-checks but also drops relevant ones. A test of date-range filtering through embeddings performs worst among four criteria.

## Motivation

- Fact-checkers lose time re-verifying recurring claims, and retrieved lists contain loosely related fact-checks.
- Earlier multilingual PFCR evaluated rankings only ([[MultiClaim]]); filtering, summaries and verdict explanations for fact-checkers were not evaluated together.
- Fact-checkers want to restrict results by language, date, outlet or named entity, which embedding search does not support directly.

## Method

We write a post as $q$, a fact-check as $f$ and the archive as pool $P$.

**Direct retrieval.** English embedders on Google-translated text and multilingual embedders on original text rank all of $P$ by cosine for 20 MultiClaim languages with at least 100 posts, monolingual pairs only.

**Criteria-based retrieval.** Each $f$ is embedded from a template holding claim, language, publication date and organisation. A natural-language criterion (language, date range, domain or named entity) first retrieves fact-checks with similarity above 0.8, which are then ranked by $q$. The reference ranking is Multilingual E5 Large applied to a pool filtered exactly by metadata.

Intuition: if embeddings encoded metadata well, the criterion query would select the same subset as an exact filter.

**Filtration.** An LLM reads the top 50 from Multilingual E5 Large and keeps only directly relevant fact-checks, with an explanation.

**Summaries and verdicts.** LLMs summarise AFP articles in English, then predict True, False or Unverifiable from retrieved claims, ratings and summaries.

**Tool.** A web application stores fact-checks in over 80 languages in a Milvus vector database and uses Llama 3.3 70B.

## Key numbers

- Average Success@10 over 20 languages: Multilingual E5 Large 0.84, GTR-T5-Large on English translations 0.83, BGE-M3 0.82, BM25 0.62; Polish 0.77 and English 0.75 for Multilingual E5 Large.
- Criteria filtering vs exact filtering, average Spearman correlation: named entities -0.31, languages -0.58, domains -0.66, dates -0.82; only 2% of fact-checks are shared under the date criterion.
- Filtration on 1,000 posts in 10 languages: Multilingual E5 Large alone Success@10 0.76; Mistral Large filtering 0.70 with true negative rate 90.23% and false negative rate 15.38%.
- Veracity: Mistral Large with retrieved fact-checks reaches macro F1 63.05 vs 26.53 without them.

## Experiments

- **Retrieval:** six English and eight multilingual embedders; Multilingual E5 Large is best except in Thai, where a smaller E5 wins.
- **Criteria-based retrieval:** all four criteria give negative rank correlations with the exact-filter reference; dates are worst because embeddings held exact dates while queries named ranges.
- **Filtration:** nine LLMs; all lower Success@10 and MRR compared with no filtering, but remove most irrelevant candidates; Mistral Large has the best trade-off.
- **Summarisation:** 14 LLMs on 100 AFP articles per language; small Llama models often answer in the source language; putting the article first helps.
- **Human study:** six participants (five journalism students, one academic) rate most features 3.5 to 4 out of 5.

## Data

- MultiClaim: 206K fact-checks in 39 languages, 28K posts in 27 languages, 31K pairs.
- Filtration and veracity subset: 100 posts each in Czech, English, French, German, Hindi, Hungarian, Polish, Portuguese, Spanish and Slovak (55 true, 65 unverifiable, 880 false).
- AFP-Sum: about 19K AFP fact-checking articles with fact-checker summaries in 23 languages, published up to September 2023; 386 from the Polish AFP service.

> [!failure] Limitations
> - The date experiment tests filtering through embeddings, not a time-respecting evaluation; no comparison of date-restricted and full pools is made.
> - Retrieval evaluation ignores post and fact-check dates, and LLM filters may know fact-checks from pretraining.
> - The class balance of the veracity set is extreme (88% false).
> - The user study has six non-professional participants; the paper is a preprint without peer review found.

## Relation to our project

- It is the closest prior PFCR work that mentions date filtering. Its date feature is a user filter applied through embeddings, not an evaluation protocol, so our causal-index claim stands; we cite it in the overlap discussion ([[Topic research]], [[Methods and Systems]]).
- Its failure with dates confirms our design choice: the causal pool $P(q)$ is built by an exact metadata filter on $t_f < t_q$, never by embedding text ([[2026-10-27-temporal-retrieval-eval|Project plan]]).
- Its Polish monolingual Success@10 (0.77, above English 0.75) is a reference for our Polish slice ([[Language scope]]).
- LLM filtering is a candidate final stage whose parametric leakage we would need to measure separately.

## Future work

- **Open:** evaluation with professional fact-checkers (searched 2026-10).
- **Open:** criteria filtering by date ranges inside embedding search, beyond exact dates (searched 2026-10).
- **Partly done:** language bias of LLM relevance judgements across 20 languages; [Vykopal et al., 2026](https://aclanthology.org/2026.eacl-long.240/) ([[Language and Retrieval Bias]]).
