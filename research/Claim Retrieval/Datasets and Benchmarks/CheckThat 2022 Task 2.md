---
title: "CheckThat 2022 Task 2"
aliases: ["Overview of the CLEF-2022 CheckThat! Lab Task 2 on Detecting Previously Fact-Checked Claims"]
authors: ["Preslav Nakov", "Giovanni Da San Martino", "Firoj Alam", "Shaden Shaar", "Hamdy Mubarak", "Nikolay Babulkov"]
year: 2022
venue: "Working Notes of CLEF 2022, CEUR Workshop Proceedings Vol-3180, pages 393-403"
url: "https://ceur-ws.org/Vol-3180/paper-29.pdf"
citekey: nakov2022overview
verified: 2026-10-27
theme: "[[Datasets and Benchmarks]]"
tags: [type/paper, theme/datasets, topic/shared-task, topic/english, topic/reranking, topic/benchmark]
---
# CheckThat 2022 Task 2

> [!info] TL;DR
> The CLEF-2022 edition reruns the PFCR shared task of [[CheckThat 2021 Task 2]]: the 2021 data become training, development and "dev-test" sets, and a small new test set is added (209 English tweets, 50 Arabic tweets, 83 debate sentences). Six teams took part; the best English tweet system, sentence-T5 retrieval plus GPT-Neo reranking, reached MAP@5 0.956, and the single debate team reached 0.459. The baseline is now random.

## Motivation

- PFCR remained a key aid for fact-checkers, and the 2021 edition had few teams and small test sets.
- Recent matching methods (memory-enhanced transformers, generative models, reinforcement learning) needed a common benchmark.
- Reusing the 2021 data gives continuity across editions.

## Method

We write a tweet or debate sentence as post $q$, a verified claim as fact-check $f$ and the collection as pool $P$.

**Task.** As in 2021: rank $P$ by usefulness for fact-checking $q$. Subtask 2A covers tweets in Arabic and English; Subtask 2B covers political debates and speeches in English against PolitiFact.

**Partitions.** The 2021 train and dev sets are kept, the 2021 test set becomes dev-test, and a new test set is added. Pools: 13,835 Snopes claims (English 2A), 30,379 claims from AraFacts plus translated ClaimsKG (Arabic 2A; the text also says 30,329), 20,771 PolitiFact claims (2B).

Intuition: new test queries against an unchanged archive check whether 2021 systems generalise to later tweets.

**Evaluation.** MAP@5 official, with MRR and Precision@k; random baseline.

## Key numbers

- English 2A: RIET Lab MAP@5 0.956; AI Rational 0.922; BigIR 0.921 with a model fine-tuned only on 2021 data.
- 2B: SimBa MAP@5 0.459, the only team; the random baseline scores zero.
- Arabic 2A: the one submitted system and the random baseline both scored 0.0, so no Arabic results are reported.

## Experiments

- **RIET Lab:** sentence-T5 candidate retrieval fine-tuned with BM25 hard negatives, then a GPT-Neo reranker trained with a mutual-information objective.
- **AI Rational:** sentence-BERT, Elasticsearch and an SVM; it finds that for MAP@k and P@k, reranking reduces to classification.
- **BigIR:** query expansion from URLs, images and videos, BM25 retrieval, BERT-based reranking (MPNet for English).
- **SimBa:** unsupervised averaging of Sentence-BERT and SimCSE similarities plus token overlap for 2A; for 2B, blocking with four encoders and a linear SVM over similarity features.
- **Fraunhofer SIT:** sentence-transformer ensemble with back-translation augmentation; lowest English score (0.610).

## Data

- 2A English: 1,610 tweets (999 train, 200 dev, 202 dev-test, 209 test), one gold claim each, 13,835 Snopes claims.
- 2A Arabic: 908 tweets (512, 85, 261, 50), 1,089 pairs, 30,379 claims.
- 2B English: 752 sentences (472, 119, 78, 83), 869 pairs, 20,771 PolitiFact claims.

> [!failure] Limitations
> - The new test sets are tiny (209, 50 and 83 queries) and Arabic produced no usable result.
> - A random baseline replaces 2021's BM25 baseline, so gains over the baseline are not comparable across editions.
> - The overview does not say when the new test tweets were posted or whether they follow the training data in time; no date restriction of $P$ is described.
> - English tweets are again cited by their own Snopes article.

## Relation to our project

- A test set added after training data resembles an out-of-time test, but without stated dates we cannot treat it as one; [[SemEval-2025 Task 7]] is the clearer precedent ([[Datasets and Benchmarks]]).
- BigIR's 2021-trained model staying near the top suggests little drift on this English Snopes data, a contrast to measure on multilingual posts ([[Enhanced topic research]]).
- The hard-negative plus reranker recipe of the winner matches the system families we evaluate ([[Proposed Task]]).

## Future work

- **Done:** moving beyond Snopes and PolitiFact to many languages; [[MultiClaim]] (Pikuliak et al., 2023) and [[SemEval-2025 Task 7]].
- **Done:** the organisers' plan to shift CheckThat! to other tasks; the 2026 edition has source retrieval, numerical-claim verification and article generation, with no PFCR task ([[CheckThat 2026]]).
- **Open:** a dated re-split of the CheckThat! tweet data with a causal pool (searched 2026-10).
