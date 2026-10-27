---
title: "Mind the Gap"
aliases: ["Mind the Gap: Assessing Temporal Generalization in Neural Language Models"]
authors: ["Angeliki Lazaridou", "Adhiguna Kuncoro", "Elena Gribovskaya", "Devang Agrawal", "Adam Liska", "Tayfun Terzi", "Mai Gimenez", "Cyprien de Masson d'Autume", "Tomas Kocisky", "Sebastian Ruder", "Dani Yogatama", "Kris Cao", "Susannah Young", "Phil Blunsom"]
year: 2021
venue: "Advances in Neural Information Processing Systems 34 (NeurIPS 2021), pages 29348-29363"
arxiv: "2102.01951"
url: "https://proceedings.neurips.cc/paper/2021/hash/f5bf0ba0a17ef18f9607774722f5698c-Abstract.html"
citekey: lazaridou2021mind
verified: 2026-10-27
theme: "[[Data Splits]]"
tags: [type/paper, theme/splits, topic/temporal, topic/evaluation, topic/llm, topic/english]
---
# Mind the Gap

> [!info] TL;DR
> Language models are usually trained and tested on text from overlapping periods. Holding training size fixed, a Transformer-XL trained only on text before the test period has up to 16% higher perplexity than one that has seen the test period, and the gap grows month by month. A larger model does not slow the decay; continually updating on the new stream (dynamic evaluation) does.

## Motivation

- Standard practice partitions a pretraining crawl at random and evaluates on benchmarks that overlap it in time; GPT-3's crawl (2016-2019) overlaps tasks introduced in 2014-2017.
- Such evaluation neither measures generalisation to future text nor rules out test data contamination.
- Temporal splits were used for single tasks (machine translation, sentiment, named entities, and [[We Need to Talk about Random Splits]]) but not for language model pretraining itself.
- Deployed systems, including fake-news flagging about recent events, run on text produced after training.

## Method

The paper is about language modelling, not retrieval; its symbols are not renamed. "Time-stratified" means training only on documents dated before the evaluation period.

**Evaluation period.** 2018-2019, with a test set of 24k documents (1k per month).

**TIME-STRATIFIED setup.** Train on all documents up to September 2017, validate on October-December 2017, test on 2018-2019.

**CONTROL setup.** Same test set and the same training size, but training data include documents from 2018-2019 (excluding the test documents), filled backwards in time until the size matches.

Intuition: the two setups differ only in when their training text was written, so any gap is the cost of being out of date.

**Relative perplexity.** Degradation is measured as the relative perplexity increase of TIME-STRATIFIED over CONTROL on the same test month, because absolute perplexity varies with document length.

**Model.** Transformer-XL, 18 layers, 287M parameters; a 448M variant for the size study.

**Dynamic evaluation.** A few gradient steps on the chronologically ordered test stream, updating all parameters, only bias terms, or only embeddings.

## Key numbers

- Perplexity CONTROL vs TIME-STRATIFIED: WMT 21.11 vs 22.45 (+6.34%), CustomNews 18.38 vs 21.33 (+16.04%), arXiv 21.38 vs 23.07 (+7.90%).
- Emerging new words (frequent in test, unseen or 5x rarer in training; 287 types) have perplexity about 110 vs 22 overall on WMT. Dynamic evaluation lowers them from 109.73 to 66.26.
- The 448M time-stratified model has 5.5% lower perplexity but the same slope of decay ($p > 0.05$). By late 2019 the up-to-date 287M CONTROL model beats it.
- Updating only the bias terms (198K parameters) gives WMT perplexity 22.16, almost the full-update 22.17 (no update: 22.45).

## Experiments

- **Two years stale:** three corpora, matched training size; the stale model is worse everywhere and the gap widens with distance from the training period. The pattern holds for other test years, longer gaps and German WMT (appendix).
- **Error breakdown:** degradation is driven by common nouns and is fastest on proper nouns and numbers (for example politicians whose role changed); politics and sports decay faster than lifestyle.
- **Second occurrences:** a new word is cheap to predict the second time only when its first occurrence is still in the Transformer memory; otherwise perplexity exceeds 2,700.
- **Model size:** 287M vs 448M; size does not change the decay slope.
- **Closed-book QA:** 438 synthetic questions on 22 government roles in 11 countries for 2019. Accuracy falls as the pretraining end year moves further from 2019.
- **Reading comprehension:** time-stratified NewsQA, 10,000 questions from 2009; models trained to end-2008 and end-2009 both reach 0.47 F1, since answers are in the passage.
- **Dynamic evaluation:** slows decay, significantly on arXiv and WMT; on arXiv about one week of new data is enough to overtake CONTROL. It also causes forgetting of past data.

## Data

- WMT News Crawl: English news 2007-2019, 22.65 GB of training text.
- CustomNews: crawled English news 1969-2019, 395.59 GB, deduplicated with MinHash.
- arXiv abstracts: 1986-2019, 0.72 GB.
- Share of CONTROL training data from the test period: 6.3% (WMT), 34.8% (CustomNews), 14.5% (arXiv).

> [!failure] Limitations
> - Only autoregressive Transformer-XL language models and two QA tasks; the authors say a broader set of downstream tasks is needed.
> - Perplexity is the main measure; effects on retrieval or ranking are not tested.
> - The closed-book QA set is small and template-based, and the authors report dataset noise in its 2019 point.
> - Dynamic evaluation trades future gains for catastrophic forgetting and leaves residual decay.

## Relation to our project

- Our encoders and LLM rerankers face the same gap from both sides. A model trained before a post's period may represent new narratives poorly. A model trained after it may already know the later debunk, the parametric leakage behind our RQ5 ([[2026-10-27-temporal-retrieval-eval|Project plan]], [[2026-10-27-topic-research|Topic research]]).
- We take its control design: hold training size fixed and vary only the time of the data. Our pool-size-matched control and chronological training regime follow the same logic ([[Data Splits]]).
- The proper-noun and emerging-word finding suggests causal-index losses will concentrate on posts about new events and names. Breaking results down by event novelty and language is a cheap check ([[2026-10-27-language-scope|Language scope analysis]]).
- Its follow-up benchmark for question answering over a news stream is [[StreamingQA]].

## Future work

- **Done:** time-stratified question answering over a news stream with retrieval; [Liska et al., 2022](https://proceedings.mlr.press/v162/liska22a.html) ([[StreamingQA]]).
- **Done:** jointly modelling text with its timestamp so models can be refreshed without full retraining; [Dhingra et al., 2022](https://aclanthology.org/2022.tacl-1.15/).
- **Partly done:** benchmarks that are not static and track knowledge updates over time; [Jang et al., 2022](https://aclanthology.org/2022.emnlp-main.418/) build TemporalWiki from Wikipedia snapshot differences.
- **Open:** temporal degradation of dense retrievers and rerankers in claim matching, separated from index composition (searched 2026-10).
