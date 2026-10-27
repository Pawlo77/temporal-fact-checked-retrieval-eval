---
title: "LongEval 2023"
aliases: ["Overview of the CLEF-2023 LongEval Lab on Longitudinal Evaluation of Model Performance", "Extended Overview of the CLEF-2023 LongEval Lab on Longitudinal Evaluation of Model Performance"]
authors: ["Rabab Alkhalifa", "Iman Bilal", "Hsuvas Borkakoty", "Jose Camacho-Collados", "Romain Deveaud", "Alaa El-Ebshihy", "Luis Espinosa-Anke", "Gabriela Gonzalez-Saez", "Petra Galuščáková", "Lorraine Goeuriot", "Elena Kochkina", "Maria Liakata", "Daniel Loureiro", "Philippe Mulhem", "Florina Piroi", "Martin Popel", "Christophe Servan", "Harish Tayyar Madabushi", "Arkaitz Zubiaga"]
year: 2023
venue: "Experimental IR Meets Multilinguality, Multimodality, and Interaction (CLEF 2023), Lecture Notes in Computer Science, pages 440-458; extended overview in CEUR Workshop Proceedings Vol-3497"
doi: "10.1007/978-3-031-42448-9_28"
url: "https://doi.org/10.1007/978-3-031-42448-9_28"
citekey: alkhalifa2023overview
verified: 2026-10-27
theme: "[[Chronological Evaluation]]"
tags: [type/paper, theme/chronological, topic/temporal, topic/shared-task, topic/evaluation, topic/bm25, topic/dense-retrieval]
---
# LongEval 2023

> [!info] TL;DR
> The first LongEval lab at CLEF asks how retrieval systems and sentiment classifiers hold up as data moves away from the training period. For retrieval, systems trained on June 2022 Qwant web search data are run on a same-time collection and on July and September 2022 collections. Contrary to the lab's expectation, average NDCG did not drop on the later collections, and the most stable systems were not the most effective ones.

## Motivation

- Retrieval experiments usually use static collections, while web documents, queries and relevance change continuously.
- Models trained on one period lose quality on test data distant in time; whether this holds for retrieval, and over what horizon, had no shared benchmark.
- Neural rankers were suspected to be less stable over time than statistical ones, and depend strongly on their training data.

## Method

The lab's terms are kept; queries $q$ and documents are dated by collection month, not individually.

**Collections.** Within-time (WT): held-out queries on the training corpus (June 2022). Short-term (ST): a new snapshot from July 2022. Long-term (LT): a snapshot from September 2022. Each snapshot is a full collection; documents and queries overlap partly between snapshots.

**Relevance.** From a click model on Qwant logs; manual judgments of pooled runs for 150 sampled queries were in progress.

**Persistence measure.** For a run $r$, the relative change $(\mathrm{NDCG}_{WT}(r) - \mathrm{NDCG}_{ST}(r)) / \mathrm{NDCG}_{WT}(r)$, and likewise for LT. Negative values mean the run did better on the later collection.

Intuition: robustness is the change of a system's score between collections, read separately from how good it is.

**Ranking views.** Runs are ranked by NDCG and by change, and the two Borda counts are summed.

**Task 2.** Binary sentiment on tweets: train 2016, test within-time, 2018 (short) and 2021 (long), scored by F1 and relative performance drop.

## Key numbers

- 14 teams in the retrieval task; 73 runs on WT and ST, 63 on LT, including 4 organiser baselines.
- Average NDCG across runs: 0.3226 (WT), 0.3273 (ST), 0.3359 (LT) for the runs in the change table; on average runs improved slightly.
- Ranking correlation by NDCG: 0.95 between WT and ST, 0.71 between WT and LT.
- Initial quality and change are negatively correlated: -0.65 (WT rank vs ST change) and -0.51 (vs LT change).

## Experiments

- **Absolute effectiveness:** best runs used BM25 with query expansion (often with GPT 3.5 or word embeddings) and BERT-style reranking; original French data beat the provided English translations for every baseline pair.
- **Persistence:** the runs that improved most on later collections (for example NEON_3b, from 0.2017 to 0.2387 NDCG) were near the bottom in absolute terms; top runs were stable or slightly worse.
- **Unexpected direction:** runs changed less from WT to ST than from WT to LT, even though LT differs more; the organisers left this for further analysis.
- **Query difficulty:** the hardest queries were short and generic ("taxes", "the police"); two had no relevant documents.
- **Task 2:** 4 teams; the run with the smallest long-term drop had low absolute F1, so low drop alone does not mean a good model.

## Data

- Training: 672 queries, 9,656 click-model assessments, 1,570,734 French web pages, plus 98 held-out WT queries (June 2022).
- ST: 882 queries, 1,593,376 documents (July 2022). LT: 923 queries, 1,081,334 documents (September 2022). Automatic English translations provided.
- Manual judgments: 150 queries, 19,678 documents sampled from pools, about 14,953 judgments recorded at writing.

> [!failure] Limitations
> - The time span is three months, and LT shares 65% of its documents with the training snapshot, so drift is mild.
> - Click-model relevance may change with the engine itself; manual judgments were unfinished.
> - Snapshots are whole collections: within a snapshot, nothing restricts a query to documents that existed before it.
> - One FADERIC run scored zero on LT, probably a submission error, which distorts change rankings.

## Relation to our project

- The precedent for reporting effectiveness and robustness as separate rankings; we report the causal score and the random-to-causal change per system for the same reason ([[Proposed Task]]).
- Its result is a caution: temporal drop is not guaranteed and can even reverse, so our causal penalty must be measured, not assumed ([[Enhanced topic research]]).
- LongEval tests whether systems persist across later snapshots; our causal index restricts each query to fact-checks published before it, a per-query cut-off LongEval does not impose ([[Research summary]]).
- A possible venue model: a temporal PFCR task in the LongEval style is the CLEF route named in our plan.

## Future work

- **Partly done:** continued longitudinal evaluation in later editions of the lab ([Alkhalifa et al., 2024](https://doi.org/10.1007/978-3-031-71908-0_10)); their findings were not read for this note.
- **Open:** explaining why later snapshots scored higher than the training-time collection (searched 2026-10).
- **Open:** longitudinal retrieval evaluation with per-query time cut-offs inside each snapshot (searched 2026-10).
