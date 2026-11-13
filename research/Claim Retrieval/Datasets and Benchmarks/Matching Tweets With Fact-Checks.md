---
title: "Matching Tweets With Fact-Checks"
aliases: ["Matching Tweets With Applicable Fact-Checks Across Languages"]
authors: ["Ashkan Kazemi", "Zehua Li", "Verónica Pérez-Rosas", "Scott A. Hale", "Rada Mihalcea"]
year: 2022
venue: "Proceedings of the Workshop on Multi-Modal Fake News and Hate-Speech Detection (DE-FACTIFY 2022), CEUR Workshop Proceedings 3199, paper 1"
arxiv: "2202.07094"
url: "https://ceur-ws.org/Vol-3199/paper1.pdf"
citekey: kazemi2022matching
verified: 2026-11-11
theme: "[[Datasets and Benchmarks]]"
tags: [type/paper, theme/datasets, topic/multilingual, topic/bm25, topic/dense-retrieval, topic/benchmark]
---
# Matching Tweets With Fact-Checks

> [!info] TL;DR
> The paper releases 6,533 tweet and fact-check pairs in English, Spanish, Portuguese and Hindi-English, built from social media links inside fact-check articles. It frames PFCR both as binary matching with XLM-R and as ranking full fact-check articles with BM25, LaBSE and multilingual MPNet-SBERT. XLM-R trained on all languages classifies pairs at 86.28% mean accuracy. Full-article BM25 beats both embedding models in every monolingual setting (English MAP@1 64.85% vs 53.56%), while LaBSE wins cross-lingually (55.48% vs 47.95%).

## Motivation

- Fact-checkers in a survey of 24 organisations asked for tools that find existing fact-checks ([Nakov et al., 2021](https://arxiv.org/abs/2103.07769)).
- Earlier claim matching paired short claims with short verified claims ([[That is a Known Lie]]; [[Claim Matching Beyond English]]), not posts with article-length fact-checks.
- PFCR data was mostly English; [[CheckThat 2021 Task 2]] added Arabic.
- Multilingual sentence encoders such as [[LaBSE]] had not been compared with BM25 for matching posts to long fact-check articles across languages.

## Method

Notation: post $q$ (a tweet, with link preview text appended when it holds a link); fact-check $f$ (claim plus justification article); gold set $G(q)$, usually one fact-check.

**Pair construction.** Social media links cited in fact-checks, and the original news sources where available, are resolved to tweets, giving $(q, f)$ pairs. Several tweets can share one fact-check.

**Matching.** A binary XLM-R classifier labels $(q, f)$ as match or not. Random negatives generalised poorly, so hard negatives are mined: all non-matching pairs in the same language setting are ranked by LaBSE cosine similarity, and the most similar pairs below 0.7 are kept to limit false negatives.

Intuition: negatives that look similar teach the classifier what "applicable" means.

**Retrieval.** For each post, fact-checks are ranked by:

- Full-length BM25 (Elasticsearch) over whole articles;
- Paragraph BM25 over article paragraphs, for a fair comparison with encoders;
- LaBSE or MPNet-SBERT cosine similarity between the post and article paragraphs, because encoders take at most 512 tokens.

Hindi posts are translated to English with Google Translate for BM25 only. Retrieval is scored with MAP@K for $K \in \{1,5,10,20,50\}$ and MRR. With one gold fact-check, MAP@1 equals Success@1.

## Implementation

- **Code:** not released; the dataset is announced at `lit.eecs.umich.edu`.
- **Software:** Hugging Face Transformers, Sentence-Transformers, Elasticsearch BM25; a GPU server.
- **Models:** XLM-RoBERTa classifier; LaBSE; paraphrase-mpnet-base-v2 for English and paraphrase-multilingual-mpnet-base-v2 otherwise.
- **Training:** classification uses 5-fold cross-validation; no optimiser, learning rate or epoch counts are reported.

## Data

- Source pool: about 150,000 fact-checks from IFCN signatories and aggregators (Google Fact Check Explorer, GESIS ClaimsKG, Data Commons), with publication date, verdict and links to the checked content.
- Pairs: English-English 4,850; Hindi tweets with English fact-checks 664; Spanish 617; Portuguese 402.
- Quality: two annotators checked 100 random English pairs with 87% agreement; 89% of tweets matched their fact-check.
- No train/test split for retrieval is described, and the size of the ranked fact-check pool is not stated; no temporal filtering is applied.

## Experiments

- **Matching:** XLM-R per language pair and trained on all pairs together; accuracy and F1 per class.
- **Hard negatives:** similarity-mined against random negatives.
- **Monolingual retrieval:** English, Spanish and Portuguese, two BM25 variants against two encoders.
- **Cross-lingual retrieval:** Hindi posts against English fact-checks.

## Results

- Hard negatives raise classification accuracy by 15 points absolute over random negatives.
- XLM-R accuracy, separate vs joint training: English 88.46% vs 88.61%, Hindi-English 80.27% vs 80.50%, Spanish 85.82% vs 88.57%, Portuguese 84.08% vs 87.44%; mean 84.66% vs 86.28%.
- English retrieval MAP@1 and MRR: full BM25 64.85% and 71.51%, paragraph BM25 62.03% and 67.61%, MPNet-SBERT 53.56% and 61.84%, LaBSE 44.98% and 53.00%.
- Spanish MAP@1: full BM25 73.41%, multilingual MPNet-SBERT 59.52%, paragraph BM25 58.33%, LaBSE 57.14%.
- Portuguese MAP@1: both BM25 variants 69.62%, LaBSE 59.49%, multilingual MPNet-SBERT 54.43%.
- Hindi-English MAP@1: LaBSE 55.48%, full BM25 on translated posts 47.95%, paragraph BM25 45.89%, multilingual MPNet-SBERT 43.15%.
- Joint XLM-R F1 for the match and no-match classes: English 88.66% and 88.54%, Hindi-English 81.60% and 78.90%; the joint model mostly gains on the no-match class in English.
- MAP grows little beyond $K=5$: English full BM25 70.82% at $K=5$ and 71.39% at $K=50$; MPNet-SBERT 60.58% and 61.68%. Most posts that are found at all are found in the top five.
- Paragraph BM25 still beats the encoders by at least 10 MAP@1 points in Portuguese and matches them in Spanish, so the 512-token limit explains only part of the gap.
- LaBSE trails MPNet-SBERT by more than 8 MAP@1 points in English, which the authors attribute to covering over 100 languages.
- The XLM-R classifier does not rerank paragraph pairs well, because there are no paragraph-level labels.

## Limitations

- Encoders see paragraphs, not whole articles, which costs them part of the gap to BM25 (authors).
- Pairs come from links and are noisy; only 100 English pairs were checked (authors).
- No paragraph-level labels for training a reranker (authors).
- Pool size, query split and negatives in the retrieval pool are unspecified, so scores cannot be compared with later benchmarks (ours).
- Fact-checks are not filtered by date; a fact-check can be ranked for a tweet posted before it (ours).
- Small non-English sets (402 to 664 pairs) and no significance tests (ours).

## Relation to our project

- **Novelty claim not contradicted.** This is a PFCR dataset and evaluation, and it never restricts the fact-check pool per post by date; time is not discussed at all.
- It records fact-check publication dates in its source pool, so a causal index could have been built, but it was not.
- Tweets are found through links inside the fact-check, so most posts predate their gold fact-check by construction; a causal index would keep each gold item only when it precedes the post, the same tension as in [[MultiClaim]].
- Its finding that BM25 beats 2022 multilingual encoders monolingually supports keeping BM25 as a baseline ([[2026-10-27-temporal-retrieval-eval|Project plan]]; [[Retrieval Models]]).
- Its pairing method is a precursor of [[MultiClaim]], which scales the same link-based construction to 27 languages.
- Its paragraph-vs-article gap shows that the indexed fact-check text field changes scores, so that choice must be identical for full and causal pools.

## Future work

- **Partly done:** long-document multilingual embeddings, which the authors propose; [[BGE-M3]] takes inputs up to 8,192 tokens.
- **Partly done:** specialised multilingual embeddings for fact-check search, through fine-tuned retrievers in [[SemEval-2025 Task 7]].
- **Partly done:** a larger multilingual PFCR dataset built from fact-check links ([[MultiClaim]]).
- **Open:** a time-ordered split or per-post causal pool on this dataset (searched 2026-11).
