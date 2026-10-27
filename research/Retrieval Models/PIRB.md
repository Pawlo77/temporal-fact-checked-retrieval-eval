---
title: "PIRB"
aliases: ["PIRB: A Comprehensive Benchmark of Polish Dense and Hybrid Text Retrieval Methods"]
authors: ["Sławomir Dadas", "Michał Perełkiewicz", "Rafał Poświata"]
year: 2024
venue: "Proceedings of the 2024 Joint International Conference on Computational Linguistics, Language Resources and Evaluation (LREC-COLING 2024), pages 12761-12774"
arxiv: "2402.13350"
url: "https://aclanthology.org/2024.lrec-main.1117/"
citekey: dadas2024pirb
verified: 2026-10-27
theme: "[[Retrieval Models]]"
tags: [type/paper, theme/models, topic/polish, topic/dense-retrieval, topic/bm25, topic/benchmark, topic/evaluation]
---
# PIRB

> [!info] TL;DR
> PIRB is a Polish retrieval benchmark of 41 tasks, 10 of them new, scored by NDCG@10. Among existing models, multilingual-e5-large is clearly best (57.29 average) and BM25 reaches 41.85. The authors' three-step recipe distils an English BGE teacher into a Polish student on 60M Polish-English pairs, fine-tunes on Polish MS MARCO and adds a learned sparse-dense hybrid. It lifts Polish RoBERTa-large to 58.06 as a dense model and 59.23 as a hybrid.

## Motivation

- Polish is absent from multilingual retrieval sets such as mMARCO, Mr. TyDi and MIRACL, so multilingual models had no Polish evaluation.
- Existing Polish resources (PolQA, BEIR-PL, MAUPQA, PolEval-2022) are mostly machine-translated or generated, with few human-annotated queries.
- Few Polish retrievers existed (Silver Retriever, PolEval-2022 models), and [Multilingual E5](https://arxiv.org/abs/2402.05672) was the first strong multilingual option ([[Multilingual E5]]).

## Method

Notation: query $q$, document $f$ (a fact-check in our setting), positive $f^+$, negative $f^-$; $s$ is the teacher score and $\hat s$ the student score.

**Benchmark.** 41 tasks in five groups: PolEval-2022 (7), web datasets (9), BEIR-PL (11, machine-translated), MAUPQA (12) and two others (MFAQ, GPT-exams). The main metric is average NDCG@10; only models above BM25 are reported.

**Step 1, multilingual distillation.** The student (Polish RoBERTa or mE5) learns to map a Polish translation to the vector an English BGE teacher gives the English source, with MSE loss. Training uses 60M+ Polish-English pairs, filtered with [[LaBSE]] at similarity 0.7.

Intuition: the student inherits the teacher's English retrieval space while learning to read Polish.

**Step 2, fine-tuning.** Contrastive loss with in-batch and hard negatives on the Polish MS MARCO training split, temperature 0.01, 50,000 steps.

**Step 3, hybrid.** A LambdaMART rescorer (XGBoost, 100 trees) takes four features per index for each document: its score, the list's max and min scores, and a presence flag. It merges a dense and a sparse (BM25 or SPLADE) top-100 at about 1,500 queries per second, against 2-5 for a Transformer reranker.

## Key numbers

- Existing models, average NDCG@10 over 41 tasks: BM25 41.85, Polish SPLADE++ 52.93, multilingual-e5 small 50.65, base 53.12, large 57.29.
- Distilled and fine-tuned polish-roberta-v2 large: 58.06 dense, 58.82 with BM25 hybrid, 59.23 with SPLADE hybrid. The same recipe on mE5-large gives 58.03, 58.84 and 59.22.
- Fine-tuning mE5-large without distillation adds only 0.15 (57.44); distilled models gain 2.0-4.6 points from fine-tuning.

## Experiments

- **Baseline sweep:** more than 20 Polish and multilingual encoders. mE5-large leads every task group; SPLADE++ (82M parameters) comes close to mE5-base.
- **Recipe ablation:** distillation alone leaves most students below the original mE5. Fine-tuning then helps distilled students far more than undistilled mE5. Hybrids help small models most, and SPLADE beats BM25 as the sparse side.
- **Error analysis (appendix):** the best Polish model beats mE5-large on 53% of short-query, 50% of medium and 83% of long-query datasets. mE5 is clearly better only on PolEval-2022 (short queries and passages) and on trivia-like data.
- **Hybrid analysis:** sparse matching mainly helps queries with named entities or specialised terms.

## Data

- PolEval-2022 passage retrieval: 7 subsets (Wikipedia, legal questions, e-commerce FAQ).
- BEIR-PL: 11 BEIR datasets machine-translated to Polish.
- MAUPQA: 12 automatically built question-passage sets.
- Web datasets (new): 9 Polish Q&A sites in medicine, law, business, trivia, linguistics and physics, from 272 to 224,533 queries.
- GPT-exams (new): 8,131 exam-style question-answer pairs from 409 university courses, generated with gpt-3.5-turbo.
- MFAQ Polish: more than 60,000 FAQ pairs from Common Crawl.
- Training: Polish MS MARCO train split; the 60M-pair Polish-English corpus from OPUS, PELCRA, DGT, Wikipedia, abstracts and machine-translated questions.

> [!failure] Limitations
> - No social-media, claim or fact-checking task; queries are questions, not posts.
> - No cross-lingual task: all queries and documents are Polish.
> - Many tasks are machine-translated or LLM-generated, which the authors flag as possibly noisy.
> - Gains of the Polish models over mE5-large are about one NDCG@10 point on average, with no significance testing reported.
> - Silver Retriever trained on MAUPQA, so it cannot be scored fairly on that group.

## Relation to our project

- PIRB is our evidence for choosing Polish encoders: mE5-large is the strongest off-the-shelf model and the distilled Polish RoBERTa ([[mmlw-retrieval-roberta-large]]) adds about a point ([[Proposed Task]], [[Enhanced topic research]]).
- A large Polish-vs-multilingual gap on PFCR would therefore be informative, since PIRB averages predict a small one ([[Language scope analysis]]).
- Its distillation from English teachers on Polish-English pairs suggests Polish posts and English fact-checks share a space. PIRB never tests that cross-lingual case, so we measure it.
- Its hybrid recipe and SPLADE results support running BM25 alongside dense models. Under a causal index, BM25 statistics must come from $P(q)$ only, which a learned rescorer trained on full-pool scores would not respect ([[Research summary]]).

## Future work

- **Done:** a Polish reranker evaluated on PIRB; [[polish-reranker-roberta-v3]] reports 66.21 NDCG@10 in the reranker category.
- **Partly done:** Polish evaluation beyond retrieval for the same encoders; [Poświata et al., 2024](https://arxiv.org/abs/2405.10138) (PL-MTEB) is a Polish embedding benchmark over several task types.
- **Open:** a Polish claim-matching or fact-check retrieval task in PIRB, and any Polish-English cross-lingual retrieval task (searched 2026-10).
