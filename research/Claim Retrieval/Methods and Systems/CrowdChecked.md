---
title: "CrowdChecked"
aliases: ["CrowdChecked: Detecting Previously Fact-Checked Claims in Social Media"]
authors: ["Momchil Hardalov", "Anton Chernyavskiy", "Ivan Koychev", "Dmitry Ilvovsky", "Preslav Nakov"]
year: 2022
venue: "Proceedings of the 2nd Conference of the Asia-Pacific Chapter of the ACL and the 12th IJCNLP (AACL-IJCNLP 2022), Volume 1: Long Papers, pages 266-285"
arxiv: "2210.04447"
doi: "10.18653/v1/2022.aacl-main.22"
url: "https://aclanthology.org/2022.aacl-main.22/"
citekey: hardalov2022crowdchecked
verified: 2026-10-27
theme: "[[Methods and Systems]]"
tags: [type/paper, theme/methods, topic/english, topic/dense-retrieval, topic/reranking, topic/leakage]
---
# CrowdChecked

> [!info] TL;DR
> The paper mines 332,660 tweet-article pairs in which a Twitter user replies to a tweet with a Snopes link, labels them by distant supervision, and trains sentence-BERT on them with a noise-aware loss. With LambdaMART reranking it reaches MAP@5 90.3 on the CheckThat! 2021 English test, 2.1 points above the best shared-task system. Training data run to October 2021, later than the test set's collection.

## Motivation

- PFCR datasets had about 1,000 post-fact-check pairs ([[That is a Known Lie]], [[CheckThat 2021 Task 2]]); [Vo and Lee, 2020](https://aclanthology.org/2020.emnlp-main.621/) had 19K image tweets but checked each pair by hand.
- Users who reply with a fact-check link act as crowd fact-checkers and give pairs for free, but many links do not match the claim in the tweet they answer.
- Self-adaptive training for noisy labels existed for cross-entropy classification, not for the in-batch ranking loss used by retrievers.

## Method

We write the tweet as post $q$ and the Snopes article as fact-check $f$.

**Collection.** Twitter search for replies or quotes linking `snopes.com/fact-check/`, October 2017 to October 2021. For each hit, the root of the conversation and the tweet replied to are kept as candidate posts. Non-English, empty, self-linking and broken-link items and all CheckThat! 2021 tweets are removed.

**Distant labels.** A pair is kept if (i) the Jaccard similarity of normalised tokens between $q$ and the article title and subtitle exceeds a threshold, or (ii) the cosine of a sentence-BERT model trained on CheckThat! 2021 exceeds one. Thresholds give 3.5K to 49K training pairs.

**Loss.** Multiple-negatives ranking (MNR) with trainable temperature $\tau$. Each pair carries a refurbished label $y^r_i \leftarrow \alpha y^r_i + (1-\alpha)\hat{y}_i$ with $\alpha = 0.9$, updated from the model's predictions after an early epoch. The loss is $-\frac{1}{m}\sum_i y^r_i \left(c_i^\top v_i/\tau - \log \sum_j \exp(c_i^\top v_j/\tau)\right)$, and weighting by $y^r_i$ again makes the effective weight its square.

Intuition: pairs the model keeps disbelieving lose influence, so noisy crowd links matter less.

**Reranking.** LambdaMART over TF.IDF and sentence-BERT scores and reciprocal ranks for three field combinations (claim; claim and title; claim, title and subtitle), following the Aschern CheckThat! 2021 system.

## Key numbers

- CheckThat! 2021 English test, MAP@5: full system 90.3 vs Aschern 88.2 and NLytics 79.9.
- Sentence-BERT trained only on crowd pairs (Jaccard > 0.30): MAP@5 80.84 vs 79.20 when trained on the CheckThat! 2021 training set; pretraining on crowd pairs then fine-tuning gives 83.11.
- Self-adaptive training adds 1.0 MAP@5 on test and loss weights a further 0.7.
- Manual annotation estimates about 27% of all mined pairs (about 90,170) are correct matches by the cosine bins, and nearly 61,500 by the Jaccard bins.

## Experiments

- **Label strategy and threshold:** Jaccard-selected data help more than cosine-selected data, which the authors attribute to cosine pairs being easy for a similar model; more data generally helps.
- **Mixing vs sequential training:** both beat single-source training; sequential is best.
- **Noise handling ablation:** shuffling with trainable temperature, self-adaptive labels and weights each add on the test set, though dev gains shrink on its 199 queries.
- **Feasibility annotation:** 150 conversation-reply-tweet triples sampled across ten similarity bins, three annotators, Fleiss kappa 0.745 to 0.750; precision exceeds 90% for Jaccard 0.4 and above.

## Data

- CrowdChecked: 332,660 unique tweet-article pairs, 316,564 unique tweets and 10,340 Snopes articles published 1995-2021, peaking in 2020-2021.
- CheckThat! 2021 Task 2A English: 999 train, 199 dev and 202 test tweets against 13,835 Snopes articles, peaking in 2016-2017; 8,898 articles appear in both collections.

> [!failure] Limitations
> - De-duplication against the test set is by tweet only; the same claims and the same 8,898 articles can appear in training and test.
> - Crowd pairs collected up to October 2021 train a model evaluated on an earlier-collected test set, and no temporal analysis is given.
> - Most mined pairs are wrong matches; labels are filtered by similarity to titles, which favours lexically easy pairs.
> - English and Snopes only.

## Relation to our project

- It is a concrete instance of training-time leakage that our chronological training regime targets: later supervision, shared fact-checks, and a test set that is older than the training data ([[2026-10-27-temporal-retrieval-eval|Project plan]], [[2026-10-27-topic-research|Topic research]]).
- Its 8,898-article overlap shows why we keep fact-checks in the training pool separate by date, not only posts.
- The reply-link mechanism yields pairs where the post precedes the reply but not necessarily the fact-check, so it is not a source of post-first labels for us ([[Methods and Systems]]).
- We do not use its English-only data; our language contrast is Polish vs English ([[2026-10-27-language-scope|Language scope analysis]]).

## Future work

- **Partly done:** more languages; multilingual PFCR training data came from fact-checker links instead of crowd replies ([[MultiClaim]], [Pikuliak et al., 2023](https://aclanthology.org/2023.emnlp-main.1027/)).
- **Open:** further distant-supervision sources such as ensemble predictions (searched 2026-10).
- **Open:** measuring how much of the gain comes from claims and fact-checks shared across the training and test periods (searched 2026-10).
