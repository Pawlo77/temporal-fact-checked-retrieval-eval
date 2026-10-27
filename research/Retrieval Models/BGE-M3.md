---
title: "BGE-M3"
aliases: ["M3-Embedding: Multi-Linguality, Multi-Functionality, Multi-Granularity Text Embeddings Through Self-Knowledge Distillation"]
authors: ["Jianlv Chen", "Shitao Xiao", "Peitian Zhang", "Kun Luo", "Defu Lian", "Zheng Liu"]
year: 2024
venue: "Findings of the Association for Computational Linguistics: ACL 2024, pages 2318-2335"
arxiv: "2402.03216"
doi: "10.18653/v1/2024.findings-acl.137"
url: "https://aclanthology.org/2024.findings-acl.137/"
citekey: chen2024m3
verified: 2026-10-27
theme: "[[Retrieval Models]]"
tags: [type/paper, theme/models, topic/multilingual, topic/dense-retrieval, topic/embedding]
---
# BGE-M3

> [!info] TL;DR
> One XLM-RoBERTa-based encoder (released as BGE-M3) produces a dense vector, sparse term weights and multi-vector token embeddings at once. It covers more than 100 languages and inputs up to 8,192 tokens. Training uses self-knowledge distillation: the combined score of the three modes is the teacher for each mode. Dense alone reaches 69.2 nDCG@10 on MIRACL (mE5-large 66.6), and the three modes together reach 71.5.

## Motivation

- Most embedding models were English-only, and multilingual ones such as mDPR, mContriever and [[Multilingual E5]] still lagged on many languages.
- Each model offered one retrieval function, while practical systems combine dense, lexical and multi-vector retrieval ([ColBERT, Khattab and Zaharia, 2020](https://doi.org/10.1145/3397271.3401075)).
- Long-document retrievers were costly to train, so most encoders accepted only 512 tokens.

## Method

Notation: post $q$, fact-check $f$ (the paper's passage $p$), $H$ the encoder's hidden states, $\tau$ a temperature.

**Three scores from one encoder.**
- Dense: $s_{dense} = \langle e_q, e_f \rangle$ with $e = \mathrm{norm}(H[0])$, the [CLS] vector.
- Sparse: each token gets weight $w_t = \mathrm{ReLU}(W_{lex}^\top H[i])$, and $s_{lex} = \sum_{t \in q \cap f} w_{qt} w_{ft}$.
- Multi-vector: ColBERT-style late interaction, $s_{mul} = \frac{1}{N}\sum_{i} \max_j E_q[i] \cdot E_f[j]$.

Hybrid ranking uses $s_{rank} = w_1 s_{dense} + w_2 s_{lex} + w_3 s_{mul}$ with task-dependent weights.

**Self-knowledge distillation.** Each mode is trained with InfoNCE, $-\log \frac{\exp(s(q,f^*)/\tau)}{\sum_{f} \exp(s(q,f)/\tau)}$. The weighted sum $s_{inter}$ of the three scores is then used as a soft teacher for each mode, $-p(s_{inter}) \log p(s_*)$.

Intuition: the ensemble of three views ranks better than any one view, so each view learns from the ensemble instead of fighting the others.

**Training stages.** XLM-RoBERTa adapted with RetroMAE, then dense-only contrastive pre-training on unsupervised pairs, then fine-tuning of all three modes with distillation and ANCE hard negatives ($w_1 = 1$, $w_2 = 0.3$, $w_3 = 1$).

**Efficient batching.** Batches are grouped by length, long batches split into gradient-checkpointed sub-batches, and embeddings shared across GPUs. At 8,192 tokens this raises the batch size more than 20 times.

**MCLS.** Without long-document fine-tuning, inserting several [CLS] tokens and averaging them improves long-document retrieval at inference.

## Key numbers

- MIRACL dev, 18 languages, nDCG@10: BM25 31.9, mE5-large 66.6, E5-mistral-7b 63.4, M3 dense 69.2, sparse 53.9, multi-vector 70.5, all three 71.5.
- MKQA cross-lingual (25 non-English query languages against English Wikipedia), Recall@100: mE5-large 70.9, M3 dense 75.1, all three 75.5. For Polish queries: BM25 40.8, mE5-large 76.7, M3 dense 76.3, all three 76.6.
- MLDR long-document test, nDCG@10: mE5-large (512 tokens) 34.2, M3 dense 52.5, sparse 62.2, all three 65.0.

## Experiments

- **Multilingual retrieval (MIRACL):** dense beats all baselines on average and in most languages. Adding sparse and multi-vector scores gives further gains.
- **Cross-lingual retrieval (MKQA):** gaps are smaller than on MIRACL and E5-mistral-7b matches or beats M3 on some languages. M3 stays stable on low-resource languages (Arabic, Khmer, Hebrew), while sparse is weak because few terms are shared across languages.
- **Long documents (MLDR, NarrativeQA):** sparse beats dense by about 10 points on MLDR; on NarrativeQA all three reach 61.7 vs 51.6 for OpenAI text-embedding-3-large.
- **Ablation, distillation:** without it, sparse drops from 53.9 to 36.7 on MIRACL and dense from 69.2 to 68.7.
- **Ablation, stages:** direct fine-tuning of XLM-RoBERTa gives 60.5, adding RetroMAE 66.1, adding unsupervised pre-training 69.2.
- **Ablation, long data:** without long-document fine-tuning, dense drops to 41.2 on MLDR; MCLS raises it to 45.0 with no training.

## Data

- Unsupervised pairs: 1.2 billion pairs in 194 languages and 2,655 cross-lingual correspondences. Sources are Wikipedia, S2ORC, xP3, mC4, CC-News, curated MTP data, plus NLLB and CCMatrix translations.
- Labelled fine-tuning data: 8 English sets (including MS MARCO, NQ, HotpotQA, NLI), 7 Chinese sets, plus Mr. TyDi and MIRACL for other languages.
- MultiLongDoc: synthetic questions generated by GPT-3.5 for long Wikipedia, Wudao and mC4 articles; MLDR is built from these sources.

> [!failure] Limitations
> - The authors note generalisation to other datasets and real-world settings is untested, and per-language variation is not analysed.
> - Very long or over-limit documents are not studied for cost or quality.
> - MIRACL and Mr. TyDi training data are in fine-tuning, so MIRACL dev is not zero-shot.
> - The time span of the pre-training crawl (CC-News, mC4) is not stated.

## Relation to our project

- BGE-M3 is our second multilingual dense baseline; its sparse and multi-vector modes give a hybrid run from the same model, a cheap contrast with BM25 under the causal index ([[2026-10-27-temporal-retrieval-eval|Project plan]], [[2026-10-27-topic-research|Topic research]]).
- The MKQA Polish row is the one published Polish-to-English retrieval number for these encoders, and it is close for mE5-large and BGE-M3. Our Polish posts against English fact-checks test whether that parity holds for claims ([[2026-10-27-language-scope|Language scope analysis]]).
- Its sparse weights depend on learned term importance, not on corpus statistics, so unlike BM25 they leak no future document frequencies; the dense index can be masked to $P(q)$ at search time.
- It is the base model of [[bge-reranker-v2-m3]], so reranker and retriever share pre-training exposure; we treat that as one parametric-leakage source ([[Retrieval Models]]).

## Future work

- **Partly done:** wider evaluation across languages and real-world tasks; [Enevoldsen et al., 2025](https://arxiv.org/abs/2502.13595) (MMTEB) and [[Qwen3 Embedding]] report BGE-M3 as a baseline on MTEB Multilingual (59.56 mean task score).
- **Partly done:** Polish retrieval for multilingual encoders; [[PIRB]] benchmarks Polish models, while the published Polish cross-lingual figure remains the MKQA row.
- **Open:** behaviour of the learned sparse and hybrid modes when the index is restricted by date (searched 2026-10).
