---
title: "That is a Known Lie"
aliases: ["That is a Known Lie: Detecting Previously Fact-Checked Claims"]
authors: ["Shaden Shaar", "Nikolay Babulkov", "Giovanni Da San Martino", "Preslav Nakov"]
year: 2020
venue: "Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics (ACL 2020), pages 3607-3618"
arxiv: "2005.06058"
doi: "10.18653/v1/2020.acl-main.332"
url: "https://aclanthology.org/2020.acl-main.332/"
citekey: shaar2020that
verified: 2026-10-27
theme: "[[Methods and Systems]]"
tags: [type/paper, theme/methods, topic/english, topic/bm25, topic/reranking, topic/benchmark]
---
# That is a Known Lie

> [!info] TL;DR
> The paper defines PFCR as a ranking task and releases its first two datasets: PolitiFact (debate and speech sentences) and Snopes (tweets). BM25 over fact-check text is a strong baseline. A rankSVM reranker that adds sentence-BERT similarities to BM25 scores improves MRR by about 0.04 on PolitiFact and by about 0.12 on Snopes.

## Motivation

- Checking a claim against earlier fact-checks was named as a pipeline step by [Hassan et al., 2017](https://doi.org/10.14778/3137765.3137815) (ClaimBuster), but never specified or evaluated.
- Existing fact-checking datasets, such as [MultiFC](https://aclanthology.org/D19-1475/), used normalised claims written by fact-checkers, not claims as they occur in debates or social media.
- Google Fact Check Explorer and the ClaimsKG graph support keyword search, not semantic matching of long, naturally phrased claims.
- Viral claims return and politicians repeat statements, so an archive of verdicts can answer many new claims quickly.

## Method

We write the input claim as post $q$, a verified claim with its article as fact-check $f$, and the archive as pool $P$; the paper calls these Input claim, VerClaim and the verified-claims database.

**Task.** Given a check-worthy $q$ and $P$, rank $P$ so that every $f$ that helps verify $q$, or a sub-claim of it, is above every $f$ that does not. Relevance is taken from fact-checkers' own links, not defined formally.

**Representations of $f$.** Each fact-check has a normalised claim, a title and the article body. BM25 is run against each field and their concatenation.

**Semantic matching.** BERT, RoBERTa and sentence-BERT encode $q$ and $f$; cosine similarity ranks $P$. A full-article variant scores $q$ against every body sentence, keeps the top-$n$ sentence scores plus claim and title scores, and trains a small classifier on them.

**Reranking.** A pairwise rankSVM with RBF kernel reranks the BM25 top-$N$ using BM25 scores per field, sentence-BERT scores and the reciprocal ranks each score induces.

Intuition: BM25 catches pairs with shared words, embeddings catch paraphrases, and the reranker learns when to trust which.

**Metrics.** MRR, MAP, MAP@k and HasPositive@k, which is Success@k in our glossary.

## Key numbers

- PolitiFact test: BM25 on the article body reaches MRR 0.565; reranking the BM25 top-100 reaches 0.608 (best single sentence-BERT model 0.395).
- Snopes test: BM25 on claim plus title reaches MRR 0.664; reranking the top-50 reaches 0.788 and Success@10 0.915.
- Only 27% of PolitiFact pairs and 50% of Snopes pairs have TF.IDF cosine above 0.25, so PolitiFact is the lexically harder set.
- In a manual sample of 100 PolitiFact pairs, 48% could not be matched by approximate string matching.

## Experiments

- **BM25 fields:** title, claim, body and their union on PolitiFact; the body is best, beating the claim field by 0.09 MRR, and the union is slightly worse than the body alone.
- **Sentence encoders:** sentence-BERT beats BERT and RoBERTa by at least 13 points absolute on all measures, but stays below BM25 on both datasets.
- **Full-article matching:** top-4 body sentences plus claim and title give MRR 0.517 on PolitiFact, close to but below BM25.
- **Reranking depth:** gains grow with list length up to 100 on PolitiFact and peak at 50 on Snopes, where the first-stage retriever is stronger.
- **Body leakage on Snopes:** tweets were extracted from the article bodies, so body matching was dropped; removing the tweet text from the body still gave "unrealistically high" scores.

## Data

- PolitiFact: 768 post-fact-check pairs from PolitiFact reports on 78 events (2012-2019), split 614 train and 154 test; pool of 16,636 verified claims.
- Snopes: 1,000 tweets found inside Snopes articles and manually filtered, split 800 train and 200 test; pool of 10,396 Snopes claims from ClaimsKG.

> [!failure] Limitations
> - The train-test split is random at the sentence level; nothing is said about dates of posts or fact-checks, and the full pool is searchable for every query.
> - Snopes posts are quoted inside their gold fact-check, so the gold article is a copy of the query and body matching is unusable.
> - Gold labels come from one report or article per post, so earlier fact-checks of the same claim are unlabelled.
> - English only, with small test sets (154 and 200 posts).

## Relation to our project

- We take the task definition and the field choices (claim, title, body) as the base case for our PFCR systems ([[Proposed Task]]).
- The Snopes construction, a tweet cited inside its fact-check, is the same mechanism as MultiClaim backlinks ([[MultiClaim]]). Such pairs imply the post existed before $t_f$, which supports our premise that gold fact-checks often postdate the post; the paper itself gives no dates ([[Enhanced topic research]]).
- Its random sentence-level split is the protocol later shown to overstate scores by the same group's chronological split ([[Role of Context in PFCR]]).
- We avoid body-text fields that quote the post when measuring leakage; the paper's own Snopes result shows how such text inflates scores ([[Methods and Systems]]).

## Future work

- **Done:** more languages and datasets; CheckThat! 2021 added Arabic tweets ([[CheckThat 2021 Task 2]]) and [Pikuliak et al., 2023](https://aclanthology.org/2023.emnlp-main.1027/) built a 27-language post set ([[MultiClaim]]).
- **Partly done:** claim-image and claim-video inputs; MultiClaim adds OCR text from post images, but video remains unaddressed in the PFCR notes we hold (searched 2026-10).
- **Partly done:** time-respecting evaluation; [Shaar et al., 2022](https://aclanthology.org/2022.findings-naacl.122/) split the PolitiFact debates chronologically ([[Role of Context in PFCR]]).
- **Open:** a per-query causal index $P(q)$ for this data, with gold fact-checks dated against posts (searched 2026-10).
