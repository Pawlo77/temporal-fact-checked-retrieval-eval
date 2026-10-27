---
title: "mmlw-retrieval-roberta-large"
aliases: ["sdadas/mmlw-retrieval-roberta-large (Hugging Face model card)"]
authors: ["Sławomir Dadas"]
year: 2023
venue: "Hugging Face model card (model version of 2023-12-26)"
url: "https://huggingface.co/sdadas/mmlw-retrieval-roberta-large"
citekey: dadas2023mmlw
verified: 2026-10-27
theme: "[[Retrieval Models]]"
tags: [type/paper, theme/models, topic/polish, topic/dense-retrieval, topic/embedding]
---
# mmlw-retrieval-roberta-large

> [!info] TL;DR
> The source is a Hugging Face model card, read in full; the card has no DOI or arXiv id and asks users to cite [[PIRB]] instead. The model is a Polish dense retriever (1024-dimensional vectors) built from a Polish RoBERTa by distilling an English BGE teacher on 60 million Polish-English pairs, then fine-tuning on Polish MS MARCO. The card reports an NDCG@10 of 58.46 on PIRB.

## Motivation

- Polish had few strong retrievers; [[Multilingual E5]] was the best off-the-shelf option, and the card's family (MMLW, "muszę mieć lepszą wiadomość") targets Polish specifically.
- A Polish encoder should keep the retrieval quality of English models, which the card pursues by distilling English FlagEmbeddings (BGE) into Polish ([[BGE-M3]] is the multilingual relative of that family).

## Method

Notation: query post $q$, fact-check $f$ in the pool $P$; encoder $E$ with unit-length output vectors.

**Step 1, multilingual knowledge distillation.** The model starts from a Polish RoBERTa checkpoint and learns, with the distillation method of [Reimers and Gurevych, 2020](https://aclanthology.org/2020.emnlp-main.365/), to place a Polish sentence where the English teacher (bge-large-en) places its English source. The corpus has 60 million Polish-English text pairs.

Intuition: the Polish student inherits the teacher's English retrieval space, so Polish and English text should land near each other.

**Step 2, contrastive fine-tuning.** The distilled model is fine-tuned with a contrastive loss on the Polish MS MARCO training split. Batch sizes are large to make training efficient: 1152 (small), 768 (base) and 288 (large). Training ran on 12 A100 GPUs.

**Scoring.** Queries need the prefix "zapytanie: "; passages take no prefix. Relevance is cosine similarity of the vectors.

The card dates a model update to 2023-12-26 ("improved results"); the earlier weights remain under revision tag v1.

## Key numbers

- NDCG@10 of 58.46 on PIRB, the value the card gives for the current version (leaderboard value).
- The PIRB paper reports 58.06 for the same recipe on Polish RoBERTa-large, against 57.29 for multilingual-e5-large; the card's 58.46 postdates that paper's table ([[PIRB]]).

## Experiments

- **PIRB evaluation:** 41 Polish retrieval tasks scored by NDCG@10; the card gives only the average and points to the leaderboard for per-task results.

## Data

- Distillation corpus: 60 million Polish-English text pairs; source mix not listed on the card (the PIRB note lists OPUS, PELCRA, DGT, Wikipedia and others).
- Fine-tuning: Polish MS MARCO training split (`clarin-knext/msmarco-pl`), a machine-translated MS MARCO.
- Evaluation: PIRB, 41 tasks.

> [!failure] Limitations
> - The card reports one number; no per-task, per-length or per-domain breakdown.
> - Results are Polish-only; the card gives no cross-lingual (Polish to English) figure.
> - Fine-tuning data is machine-translated, so noise in the translation is inherited.
> - The prefix is mandatory; omitting it silently degrades the embeddings.
> - The card states no data or training cutoff date.

## Relation to our project

- Our Polish-specialised encoder: apply "zapytanie: " to posts and nothing to fact-checks ([[2026-10-27-temporal-retrieval-eval|Project plan]], [[2026-10-27-topic-research|Topic research]]).
- Distillation from an English teacher makes Polish post to English fact-check retrieval plausible, but the card shows only Polish results, so we measure it ([[2026-10-27-language-scope|Language scope analysis]]) and compare against [[Multilingual E5]] and [[BGE-M3]].
- It is the retriever that [[polish-reranker-roberta-v3]] is scored with (average 65.17 on PIRB), a natural first-stage and reranker pair.

## Future work

- **Done:** a Polish reranker on top of this retriever; [[polish-reranker-roberta-v3]].
- **Open:** Polish-to-English retrieval quality of this model (searched 2026-10).
- **Open:** a claim-matching or fact-check task for Polish encoders (searched 2026-10).
