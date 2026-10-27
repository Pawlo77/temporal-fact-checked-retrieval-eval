---
title: "CheckThat 2021 Task 2"
aliases: ["Overview of the CLEF-2021 CheckThat! Lab Task 2 on Detecting Previously Fact-Checked Claims in Tweets and Political Debates"]
authors: ["Shaden Shaar", "Fatima Haouari", "Watheq Mansour", "Maram Hasanain", "Nikolay Babulkov", "Firoj Alam", "Giovanni Da San Martino", "Tamer Elsayed", "Preslav Nakov"]
year: 2021
venue: "Working Notes of CLEF 2021, CEUR Workshop Proceedings Vol-2936, pages 393-405"
url: "https://ceur-ws.org/Vol-2936/paper-29.pdf"
citekey: shaar2021overview
verified: 2026-10-27
theme: "[[Datasets and Benchmarks]]"
tags: [type/paper, theme/datasets, topic/shared-task, topic/english, topic/bm25, topic/reranking, topic/benchmark]
---
# CheckThat 2021 Task 2

> [!info] TL;DR
> The CLEF-2021 CheckThat! lab ran PFCR as a ranking shared task: Subtask 2A matches tweets to fact-checked claims in Arabic and English, Subtask 2B matches political-debate sentences to PolitiFact claims. Four teams took part; on tweets, BM25 retrieval plus a fine-tuned BERT-style reranker beat the BM25 baseline by large margins (English MAP@5 0.883 vs 0.749), while on debates no team beat BM25.

## Motivation

- Fully automatic fact-checking lacks credibility with journalists, so tools that find earlier fact-checks are a safer aid.
- The task had only one dedicated dataset and model before ([[That is a Known Lie]]); pipelines named the step but did not evaluate it.
- Google Fact Check Explorer and ClaimsKG support keyword search, not semantic matching of long claims.

## Method

We write the input tweet or debate sentence as post $q$, a verified claim as fact-check $f$ and the collection as pool $P$; the paper calls them input claim and VerClaim.

**Task.** Given a check-worthy $q$ and $P$, rank $P$ by usefulness for fact-checking $q$; systems return a top-$n$ list.

**Arabic 2A.** $P$ joins 5,921 AraFacts claims with 24,408 English ClaimsKG claims machine-translated to Arabic. Annotators picked one tweet per AraFacts claim from tweets quoted in its article, avoiding image or video claims, near-verbatim copies and multi-claim tweets, and cross-checked each other. Extra gold pairs came from Jaccard-similar duplicate claims and from manual review of the BM25 top 25 per tweet.

Intuition: the same rumour checked by several Arabic outlets should count as several correct answers.

**English 2A.** $P$ is 13,835 Snopes claims; the 1,401 tweets are those Snopes articles cite.

**2B.** 669 debate and speech sentences against 19,250 PolitiFact claims, reusing the [[That is a Known Lie]] setup.

**Evaluation.** MAP@5 is official; MRR, MAP@k and Precision@k are also reported. Baseline: Elasticsearch BM25.

## Key numbers

- English 2A: Aschern (TF.IDF, fine-tuned sentence-BERT, LambdaMART reranking) MAP@5 0.883 vs BM25 baseline 0.749.
- Arabic 2A: bigIR (BM25 top 20 reranked by fine-tuned AraBERT) MAP@5 0.908 vs 0.794.
- 2B: BM25 baseline MAP@5 0.346; the best team (DIPS) reached 0.328, and no team beat the baseline.

## Experiments

- **Subtask 2A English:** three teams, ten runs; all beat BM25, the second team (RoBERTa regression) by 5 points.
- **Subtask 2A Arabic:** one team; reranking with negatives mined from BM25 top results gave the gain.
- **Subtask 2B:** three teams with sentence-BERT similarities, triplet-loss fine-tuning with rankSVM, or RoBERTa regression; all below BM25.

## Data

- 2A Arabic: 858 tweets (512 train, 85 dev, 261 test, "randomly split"), 1,039 pairs, 30,329 verified claims.
- 2A English: 1,401 tweets (999, 200, 202; a 70/15/15 split, not stated as random), 1,401 pairs, 13,835 verified claims.
- 2B English: 669 sentences (472, 119, 78), 804 pairs, 19,250 verified claims.

> [!failure] Limitations
> - English tweets are those cited inside their own Snopes article, so the gold fact-check cites the post and was written after it.
> - Splits are random or unspecified; no dates of tweets or fact-checks enter the task, and the full pool is searchable for every query.
> - English pairs are one-to-one, so other relevant Snopes claims are unlabelled.
> - Small test sets (202 English, 261 Arabic, 78 debate queries) and few teams.

## Relation to our project

- Shared-task PFCR with fixed splits is not new; we cite this edition as the English and Arabic precedent ([[Datasets and Benchmarks]]).
- The Snopes construction is the same "post cited in its fact-check" mechanism as MultiClaim's links ([[MultiClaim]]), which is why gold fact-checks tend to postdate posts in our data ([[Enhanced topic research]]).
- No causal pool or temporal split is described, so the 2021 results say nothing about our RQ1 ([[Proposed Task]]).

## Future work

- **Done:** larger training data and more languages, which the organisers planned; [[CheckThat 2022 Task 2]] added test data, and [[MultiClaim]] (Pikuliak et al., 2023) covered 27 post languages.
- **Partly done:** chronological evaluation of the debate data; [[Role of Context in PFCR]] (Shaar et al., 2022) split PolitiFact debates by time.
- **Open:** date-restricted pools for the tweet subtask (searched 2026-10).
