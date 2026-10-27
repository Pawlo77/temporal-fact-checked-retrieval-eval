---
title: "LaBSE"
aliases: ["Language-agnostic BERT Sentence Embedding"]
authors: ["Fangxiaoyu Feng", "Yinfei Yang", "Daniel Cer", "Naveen Arivazhagan", "Wei Wang"]
year: 2022
venue: "Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pages 878-891"
arxiv: "2007.01852"
doi: "10.18653/v1/2022.acl-long.62"
url: "https://aclanthology.org/2022.acl-long.62/"
citekey: feng2022language
verified: 2026-10-27
theme: "[[Retrieval Models]]"
tags: [type/paper, theme/models, topic/multilingual, topic/embedding, topic/dense-retrieval]
---
# LaBSE

> [!info] TL;DR
> LaBSE is a BERT-base dual encoder for 109 languages, pre-trained with masked and translation language modelling and fine-tuned to rank true translations above in-batch alternatives with an additive margin. It reaches 83.7% average accuracy on 112-language Tatoeba translation retrieval, against 65.5% for LASER. Pre-training cuts the parallel data needed by about 80%, but the model is weaker than monolingual models on graded English sentence similarity.

## Motivation

- Earlier cross-lingual sentence encoders (LASER, m-USE, the bilingual dual encoders of [Yang et al., 2019](https://doi.org/10.24963/ijcai.2019/746)) were trained from scratch on translation pairs.
- Pre-trained multilingual language models such as mBERT and XLM-R align languages but give poor sentence embeddings without a sentence-level objective; XLM-R Large scores 57.3% on 37 Tatoeba languages vs 84.4% for LASER.
- Low-resource languages were poorly covered, and m-USE handled only 16 languages.

## Method

The paper embeds a source sentence $x$ and its translation $y$; in our terms these play the roles of a post $q$ and a fact-check $f$.

**Translation ranking loss.** With $\phi(x, y) = x y^\top$ on normalised [CLS] vectors and a batch of $N$ pairs, $\mathcal{L} = -\frac{1}{N}\sum_i \log \frac{e^{\phi(x_i,y_i)}}{e^{\phi(x_i,y_i)} + \sum_{n \ne i} e^{\phi(x_i,y_n)}}$, summed over both directions.

**Additive margin softmax.** The positive score is replaced by $\phi(x_i, y_i) - m$ with $m = 0.3$.

Intuition: the margin forces each true translation to beat every non-translation by a fixed gap, which separates near-translations.

**Cross-accelerator negatives.** Embeddings from all 32 TPU cores are shared as negatives, so each pair sees the global batch of 4,096 instead of the 128 on its own core.

**Pre-training.** BERT-base encoder (12 layers, 768 hidden), custom 501,153-token vocabulary. Pre-training uses MLM on monolingual text and TLM on translation pairs, grown by 3-stage progressive stacking. Fine-tuning uses maximum sequence length 128.

## Key numbers

- Tatoeba, all 112 languages: LaBSE 83.7%, LASER 65.5%; on the 36 XTREME languages, 95.0% vs 84.4%.
- UN translation retrieval (P@1, average of es, fr, ru, zh): 89.5, vs 88.1 for the best bilingual models of Yang et al.
- STS Benchmark test (Pearson $r$): LaBSE 72.8, below m-USE 82.5 and SentenceBERT 79.2.

## Experiments

- **Ablation, vocabulary and objectives:** additive margin gives the largest gain (UN average 66.7 to 86.9 with mBERT vocabulary). The custom vocabulary helps, and pre-training helps on UN, and on Tatoeba only with the custom vocabulary.
- **Margin size:** UN P@1 rises from about 60 at $m = 0$ to its best at $m = 0.3$.
- **Pre-training effect:** with pre-training, 50k steps (200M pairs) suffice; without it, 500k steps (1B pairs) are needed and the result is still slightly worse.
- **BUCC 2018 mining:** LaBSE beats prior work in all four pairs, forward F1 up to 92.5 (de-en), with one model instead of four bilingual ones.
- **Unseen languages:** 30+ Tatoeba languages without explicit training data average 60.5% accuracy, likely through related languages.
- **SentEval transfer:** competitive with English-only encoders on seven classification tasks.
- **Mining CommonCrawl:** LaBSE-mined en-zh and en-de pairs train NMT models close to models trained on official WMT data.

## Data

- Monolingual text: CommonCrawl 2019-35 snapshot and a Wikipedia dump of 21 May 2020; 17B sentences after filtering.
- Translation pairs: 6B web-mined pairs, capped at 100M per language; experiments show 200M pairs overall suffice.
- Evaluation: UN corpus (86,000 document pairs, five language pairs), Tatoeba (up to 1,000 sentences per language, 112 languages), BUCC 2018 (four pairs), SentEval, STS Benchmark.

> [!failure] Limitations
> - Trained on translation equivalence, it is weak on graded similarity, which the authors attribute to the training objective.
> - Sequences are capped at 128 tokens in fine-tuning, so long documents are truncated.
> - No query-document retrieval is evaluated; it ranks 45.2 on English MTEB in [[Multilingual E5]], far below retrieval-trained encoders.
> - Zero-shot language results may be inflated by language-detection noise in training data, as the authors note.

## Relation to our project

- LaBSE is our classic cross-lingual baseline. It suits Polish posts that are close translations of an English fact-check's claim and should fail when the post only paraphrases or alludes to it ([[Proposed Task]], [[Enhanced topic research]]).
- Its training crawl ends in 2019-2020 (CommonCrawl 2019-35, Wikipedia May 2020). It is the one model in our set with a documented cutoff before most MultiClaim fact-checks, which makes it the low-exposure control for parametric leakage ([[Research summary]]).
- We expect it to trail [[Multilingual E5]] and [[BGE-M3]] on Success@10; a small gap on Polish-English pairs would suggest that cross-lingual PFCR there is mostly translation matching ([[Language scope analysis]]).

## Future work

- **Partly done:** combining LaBSE-style alignment with distillation from a monolingual teacher, which the authors call complementary to [Reimers and Gurevych, 2020](https://aclanthology.org/2020.emnlp-main.365/); [[PIRB]] distils English teachers into Polish retrievers, though not with LaBSE.
- **Done:** a multilingual encoder trained for asymmetric retrieval rather than translation; [[Multilingual E5]] and [[BGE-M3]].
- **Open:** LaBSE evaluated on claim matching between posts and fact-checks across languages under a date-restricted pool (searched 2026-10).
