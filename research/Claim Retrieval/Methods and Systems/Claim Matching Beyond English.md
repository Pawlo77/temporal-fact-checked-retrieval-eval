---
title: "Claim Matching Beyond English"
aliases: ["Claim Matching Beyond English to Scale Global Fact-Checking"]
authors: ["Ashkan Kazemi", "Kiran Garimella", "Devin Gaffney", "Scott A. Hale"]
year: 2021
venue: "Proceedings of the 59th Annual Meeting of the ACL and the 11th IJCNLP (ACL-IJCNLP 2021), Volume 1: Long Papers, pages 4504-4517"
arxiv: "2106.00853"
doi: "10.18653/v1/2021.acl-long.347"
url: "https://aclanthology.org/2021.acl-long.347/"
citekey: kazemi2021claim
verified: 2026-10-27
theme: "[[Methods and Systems]]"
tags: [type/paper, theme/methods, topic/multilingual, topic/embedding, topic/bm25]
---
# Claim Matching Beyond English

> [!info] TL;DR
> The paper frames claim matching as finding message pairs that one fact-check can serve, and builds annotated data from WhatsApp tiplines and public groups in English, Hindi, Bengali, Malayalam and Tamil. A distilled XLM-R encoder (I-XLM-R) beats LASER and LaBSE as a reranker over BM25 and as a match classifier. The model is deployed in tiplines run by over 12 fact-checking organisations.

## Motivation

- PFCR work such as [[That is a Known Lie]] was English-only, centred on US politics, and always paired a post with a fact-check.
- Labels built from one fact-check report miss other occurrences of the same claim, which the authors say inflates false negatives.
- Off-the-shelf multilingual encoders such as [[LaBSE]] and LASER are weaker for lower-resource Indian languages.
- Grouping messages with the same claim measures prevalence, which fact-checkers use to choose what to check.

## Method

We write a tipline or group message as post $q$ and a fact-check headline as $f$; the paper also matches posts to posts.

**Claim-like statement detection.** Annotators label about 1,000 items per language for whether they contain a claim-like statement (Yes, Probably, No, wrong language).

**Claim similarity.** Pairs are rated on a four-point scale; "Very Similar" means one fact-check serves both, "Somewhat Similar" means it serves them partly. Candidate pairs are sampled by cosine similarity under LASER, LaBSE and I-XLM-R, with sampling weights from a Gaussian centred at 0.825, plus 100 random pairs per language except Tamil.

**I-XLM-R.** Knowledge distillation trains an XLM-R student to place both an English sentence $s_i$ and its translation $t_i$ near the English SBERT teacher's embedding of $s_i$, minimising $\frac{1}{|B|}\sum_{i \in B} [(M_T(s_i) - M_S(s_i))^2 + (M_T(s_i) - M_S(t_i))^2]$ on OPUS parallel data.

Intuition: the student inherits the teacher's English similarity space and maps each Indian language onto it.

**Use.** For retrieval, Elasticsearch BM25 retrieves candidates and embedding cosine reranks them, scored by MRR. For matching, a cosine threshold or an AdaBoost classifier over lengths, embeddings and cosine decides whether two items match.

## Key numbers

- BM25 plus I-XLM-R reranking reaches MRR 0.5281 in Bengali vs 0.4247 for BM25 alone; in English (0.4221 vs 0.4286) and Tamil (0.4634 vs 0.4747) it is on par with BM25.
- LASER and LaBSE rerankers fall below BM25 in every language, LaBSE by 0.085 in Hindi.
- AdaBoost with I-XLM-R features reaches accuracy 0.883 and positive-class F1 0.885 in 10-fold cross-validation (LaBSE 0.797 and 0.791).
- A cosine threshold with I-XLM-R gives F1 0.73 over all languages (LaBSE 0.58, LASER 0.55).

## Experiments

- **Retrieval reranking:** MRR per language for BM25 and three rerankers; I-XLM-R leads in Bengali, Hindi and Malayalam. Mean First Relevant and HasPositive@k showed no useful pattern.
- **Threshold classifier:** I-XLM-R wins in every language; Tamil is hardest (F1 0.57). Matching fact-check pairs is easier than matching social media pairs (F1 0.76 vs 0.72).
- **Error analysis:** 65 of 89 threshold errors are false negatives; 16 of 24 false positives are "Somewhat Similar" pairs that share some claims.
- **Clustering:** single-link clustering of 37,823 election-tipline messages at threshold 0.90 gives 1,305 clusters of two or more items, the largest with 213. In 132 of 137 multilingual clusters shown, a journalist found the same claim across languages.

## Data

- Claim detection set: 5,066 messages in five languages, triple-annotated; Randolph's kappa 0.30 (Bengali) to 0.63.
- Claim similarity set: 2,343 pairs; 261 (11%) Very Similar and 121 Somewhat Similar by majority.
- Sources: an Indian election tipline (March-May 2019), other tiplines (February-August 2020), public WhatsApp groups, and about 150,000 fact-checks from aggregators and IFCN signatories.

> [!failure] Limitations
> - Evaluation is within each language; crosslingual matching is shown only through the clustering demonstration.
> - Too few fact-checks matched a social media item to evaluate that setting, the one PFCR targets.
> - Pairs are sampled by the very encoders being compared, so the test pool favours what those models find.
> - Submission times exist for tipline messages, but no evaluation respects them; the fact-check pool is not restricted by date.

## Relation to our project

- We cite it for the observation that claims recur across messages and languages, which motivates our sibling qrels: an earlier fact-check of the same claim also answers a post ([[Proposed Task]], [[Enhanced topic research]]).
- Its argument that single-report labels miss matches is the missing-label problem our sibling labels address for MultiClaim ([[MultiClaim]]).
- It does not bear on Polish, which is outside its five languages ([[Language scope analysis]]).
- No temporal protocol: the paper is evidence that PFCR evaluation without dates was the norm in 2021 ([[Research summary]]).

## Future work

- **Done:** crosslingual matching at scale; [[MultiClaim]] evaluates crosslingual PFCR and [Ramponi et al., 2025](https://aclanthology.org/2025.emnlp-main.1480/) separate multilingual from crosslingual retrieval ([[Multilingual vs Crosslingual Retrieval]]).
- **Partly done:** matching social media posts to fact-checks in Indian languages; the MultiClaim v2 subset of Ramponi et al. has Hindi, Bengali and Malayalam posts paired with fact-checks, but no tipline messages.
- **Open:** using tipline submission times to evaluate matching against only earlier fact-checks (searched 2026-10).
