---
title: "Multilingual vs Crosslingual Retrieval"
aliases: ["Multilingual vs Crosslingual Retrieval of Fact-Checked Claims: A Tale of Two Approaches"]
authors: ["Alan Ramponi", "Marco Rovera", "Robert Moro", "Sara Tonelli"]
year: 2025
venue: "Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing (EMNLP 2025), pages 29057-29076"
arxiv: "2505.22118"
doi: "10.18653/v1/2025.emnlp-main.1480"
url: "https://aclanthology.org/2025.emnlp-main.1480/"
citekey: ramponi2025multilingual
verified: 2026-10-27
theme: "[[Methods and Systems]]"
tags: [type/paper, theme/methods, topic/multilingual, topic/polish, topic/dense-retrieval, topic/reranking, topic/llm]
---
# Multilingual vs Crosslingual Retrieval

> [!info] TL;DR
> On a curated MultiClaim v2 subset in 47 languages, the paper compares 16 embedding models, cross-encoder and LLM reranking, and fine-tuning with three negative-sampling strategies. LLM reranking of the top 30 is best (multilingual MRR@10 0.8042, crosslingual 0.6140 with multilingual-e5-large). Fine-tuning with similarity-mined negatives is second. Crosslingual retrieval behaves differently from multilingual retrieval: reranking and hard negatives help it far more.

## Motivation

- Most PFCR work was monolingual English ([[That is a Known Lie]], [[CrowdChecked]]); crosslingual PFCR had been studied only by [[MultiClaim]] and [[AMC-16K]], both of which showed the potential of translation into English.
- Newer multilingual embedders and LLMs might remove the need for translation.
- Fine-tuning with random negatives saturates quickly; task-specific hard-negative strategies for crosslingual retrieval were untested.
- Earlier MultiClaim splits separated posts but not fact-checks, so the same fact-check could sit in training and test pools.

## Method

We write a social media post as $q$, a fact-checked claim as $f$, and the paired claim as the gold set $G(q)$.

**Data curation.** From MultiClaim v2 the authors keep post text without OCR, original-language claims, and pairs whose relationship is `claim_review` or `backlink`. Languages are re-detected with fastText, gCLD3, langdetect and polyglot. Languages with fewer than 200 posts are dropped, as are claims without a paired post.

**Split.** Posts, fact-checks and pairs are split 80/10/10, stratified by language. No fact-check appears in more than one split, so each split has its own pool $P$.

**Settings.** Multilingual: all pairs. Crosslingual: only pairs where $q$ and $f$ differ in language, also reported without English.

**Unsupervised.** Dense retrieval with 16 embedders (278M to 7B parameters), then reranking of the top 30 by bge-reranker-v2-m3 (cross-encoder) or RankGPT (LLM, on the three best embedders). Pools are the test split (about 6,100 claims) or all 52,911 claims.

**Supervised.** multilingual-e5-large and paraphrase-multilingual-mpnet-base-v2 trained with multiple-negatives ranking loss and $k$ negatives per post. Negatives are random; topic (same BERTopic cluster); or similarity (the $k$ most similar non-gold claims).

Intuition: a negative that shares words and topic with the post forces the model to learn which claim the post actually makes.

**Metrics.** Success@10 and MRR@10.

## Key numbers

- multilingual-e5-large, test MRR@10: retrieval 0.7475 multilingual and 0.4323 crosslingual; LLM reranking 0.8042 and 0.6140.
- Similarity negatives beat random by 1.45 and 5.31 MRR@10 (multilingual and crosslingual); the fine-tuned model reaches multilingual MRR@10 0.7768 and Success@10 0.8228.
- Cross-encoder reranking adds on average 8.11 MRR@10 in the crosslingual test setting but only 0.60 in the multilingual one, and lowers the scores of strong retrievers there.
- LLM reranking adds on average 4.54, 13.80 and 6.93 MRR@10 in multilingual, crosslingual, and crosslingual without English.

## Experiments

- **Embedder comparison:** text-embedding-3-large leads multilingually; bge-multilingual-gemma2 leads crosslingually on the test pool and gte-multilingual-base on the full pool. Model size and embedding dimension do not correlate with performance.
- **Reranking:** cross-encoders help weak models and the crosslingual setting; RankGPT is best everywhere but costs about 50 dollars per test run.
- **Negatives and $k$:** $k = 10$ is best on development data for all strategies; topic negatives help most at small $k$, similarity negatives at larger $k$.
- **English and Hindi:** supervised similarity negatives are best monolingually; reranking is best crosslingually.
- **Small model:** for paraphrase-multilingual-mpnet-base-v2, fine-tuning does not beat its own unsupervised retrieval.

## Data

- Multilingual subset: 55,421 posts, 52,911 fact-checks and 63,913 pairs; 6,375 test pairs.
- Crosslingual subset: 7,975 posts, 7,869 fact-checks and 9,066 pairs; 929 test pairs, 118 without English.
- 47 languages (30 in posts, 46 in claims) and 283 language combinations; Polish-Polish has 1,309 pairs.

> [!failure] Limitations
> - Splits are random within language; post and fact-check dates play no role, so a test post can be matched to a fact-check published after it.
> - Unlabelled positives are likely across fact-checker databases, especially crosslingually, which also contaminates mined negatives.
> - English dominates crosslingual pairs; conclusions may change with another language mix.
> - Automatic language identification remains noisy despite four detectors.

## Relation to our project

- It defines the strongest random-split recipe we compare against: e5 with similarity negatives, plus an LLM reranker ([[Proposed Task]]).
- Its fact-check-disjoint split addresses one training leak, a fact-check seen in training; it leaves index leakage and answerability untouched, which our causal index $P(q)$ adds ([[Enhanced topic research]]).
- Polish is one of its 30 post languages with 1,309 monolingual pairs, a usable size reference for our Polish slice ([[Language scope analysis]]).
- Dropping the identical-claim relationship matches our plan to report such pairs separately ([[MultiClaim Zenodo Records]]).
- We take [[Multilingual E5]], [[BGE-M3]] and [[bge-reranker-v2-m3]] as in its comparison, so our scores can be compared with its random-split numbers ([[Research summary]]).

## Future work

- **Open:** what makes the crosslingual setting different, which the authors leave for further study (searched 2026-10).
- **Open:** checking the conclusions under a chronological split with a date-restricted pool (searched 2026-10).
- **Open:** recovering unlabelled crosslingual positives before mining negatives (searched 2026-10).
