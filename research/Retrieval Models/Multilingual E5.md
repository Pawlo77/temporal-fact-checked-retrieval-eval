---
title: "Multilingual E5"
aliases: ["Multilingual E5 Text Embeddings: A Technical Report"]
authors: ["Liang Wang", "Nan Yang", "Xiaolong Huang", "Linjun Yang", "Rangan Majumder", "Furu Wei"]
year: 2024
venue: "arXiv technical report 2402.05672 (models released mid-2023)"
arxiv: "2402.05672"
url: "https://arxiv.org/abs/2402.05672"
citekey: wang2024multilingual
verified: 2026-10-27
theme: "[[Retrieval Models]]"
tags: [type/paper, theme/models, topic/multilingual, topic/dense-retrieval, topic/embedding]
---
# Multilingual E5

> [!info] TL;DR
> A short technical report on the multilingual E5 embedders (small, base, large), released in mid-2023, and a new instruction-tuned large variant. They follow the English E5 recipe: contrastive pre-training on about 1 billion multilingual text pairs, then supervised fine-tuning on about 1.6M labelled pairs. mE5-large reaches 66.5 nDCG@10 averaged over 16 MIRACL languages, against 39.3 for BM25; the instruct variant beats LaBSE on 112-language bitext mining.

## Motivation

- Most strong embedding models were English-only (Sentence-BERT, GTR, Sentence-T5), limiting multilingual retrieval.
- The English E5 recipe of weakly supervised pre-training followed by labelled fine-tuning had not been released for many languages.
- Translation-trained encoders such as [[LaBSE]] align languages but are weak on asymmetric retrieval tasks.

## Method

Notation: a post $q$ and a fact-check $f$ are embedded separately, and $f$ is ranked by the cosine similarity of the two vectors (a bi-encoder).

**Initialisation.** mE5-small from multilingual MiniLM, mE5-base from xlm-roberta-base, mE5-large from xlm-roberta-large.

**Stage 1, contrastive pre-training.** InfoNCE loss with in-batch negatives only, batch size 32k, 30k steps, about 1B pairs. Pairs are (title, body) or similar from Wikipedia, mC4, multilingual CC News, Reddit, S2ORC, Stack Exchange, xP3 and SBERT data, plus NLLB translation pairs.

Intuition: naturally co-occurring text pairs teach the encoder that a title and its body, or a question and its answer, belong together across languages.

**Stage 2, supervised fine-tuning.** About 1.6M labelled pairs with mined hard negatives and distillation from a cross-encoder; 2 epochs, batch size 512. The mix includes MS MARCO, NQ, TriviaQA, SQuAD, NLI, ELI5, NLLB, DuReader, FEVER, HotpotQA, Quora, Mr. TyDi and MIRACL.

**Instruct variant.** mE5-large-instruct is fine-tuned on a mixture that adds about 500k GPT-3.5/4 synthetic examples with 150k instructions in 93 languages; an instruction describing the task is prepended at training and evaluation.

## Key numbers

- MIRACL dev, 16 languages, nDCG@10: BM25 39.3, mDPR 41.5, mE5-large 66.5, mE5-large-instruct 65.7. Recall@100 is 94.3 for mE5-large vs 78.7 for BM25.
- English MTEB (56 datasets): mE5-large 61.5, mE5-large-instruct 64.4, LaBSE 45.2, BGE-large-en-v1.5 64.2.
- Tatoeba bitext mining (112 languages): LaBSE 81.1, mE5-large 75.7, mE5-large-instruct 83.8.

## Experiments

- **English MTEB:** the instruct model is above the previous best multilingual model (Cohere multilingual-v3, 64.0) and the English-only BGE-large-en-v1.5; smaller models trade quality for speed.
- **Multilingual retrieval (MIRACL dev):** all mE5 sizes beat mDPR, which was fine-tuned on MIRACL; per-language nDCG@10 for mE5-large ranges from 52.9 (English, Spanish, Indonesian) to 84.6 (Telugu).
- **Bitext mining (BUCC 2018, Tatoeba):** mE5 is competitive on BUCC (up to 99.0) and on Tatoeba is beaten by LaBSE except for the instruct model, credited to the wider language coverage of synthetic data.

## Data

- Pre-training mixture: about 1B pairs (Wikipedia 150M; mC4, CC News, NLLB, Reddit 160M each; xP3 80M; S2ORC and Stack Exchange 50M each; SBERT data 10M).
- Fine-tuning mixture: about 1.6M pairs, largest parts MS MARCO passage (500k) and NLI (275k); FEVER contributes 70k.
- MIRACL dev (16 languages), English MTEB (56 datasets), BUCC 2018 (4 languages), Tatoeba (112 languages).

> [!failure] Limitations
> - No peer-reviewed venue, no ablations, and no statement of the time span of the pre-training crawl.
> - MIRACL has no Polish, so the report gives no Polish retrieval number.
> - Cross-lingual retrieval is measured only through bitext mining of near-translations, not query-document retrieval across languages.
> - MIRACL training data is in the fine-tuning mix, so MIRACL dev is not a zero-shot test.

## Relation to our project

- mE5-large and mE5-large-instruct are our main multilingual dense baselines and the base for the fine-tuned system trained under random and chronological regimes ([[2026-10-27-temporal-retrieval-eval|Project plan]], [[2026-10-27-topic-research|Topic research]]).
- The pre-training crawl includes CC News and Reddit with no stated end date, so exposure to fact-check-era text cannot be ruled out. We treat it as possible parametric leakage and compare query strata rather than claiming it away ([[Retrieval Models]]).
- Polish evidence comes from [[PIRB]], where mE5-large is the strongest off-the-shelf model (57.29 NDCG@10); the cross-lingual Polish-English case is untested ([[2026-10-27-language-scope|Language scope analysis]]).
- Encoding the pool once and masking by $t_f < t_q$ at search time makes the causal pool $P(q)$ cheap for a bi-encoder like this one.

## Future work

- **Done:** Polish retrieval evaluation of mE5 across 41 tasks; [Dadas et al., 2024](https://aclanthology.org/2024.lrec-main.1117/) ([[PIRB]]).
- **Partly done:** a broader multilingual benchmark than MIRACL for embedders; on MTEB Multilingual from [Enevoldsen et al., 2025](https://arxiv.org/abs/2502.13595), [[Qwen3 Embedding]] reports mE5-large-instruct at 63.22 (mean task score), above [[BGE-M3]] at 59.56.
- **Open:** disclosure or measurement of the pre-training crawl's time span, needed to date parametric exposure of the model (searched 2026-10).
