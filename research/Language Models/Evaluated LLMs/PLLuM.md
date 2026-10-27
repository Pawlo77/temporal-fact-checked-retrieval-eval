---
title: "PLLuM"
aliases: ["PLLuM: A Family of Polish Large Language Models"]
authors: ["Jan Kocoń", "Maciej Piasecki", "Arkadiusz Janz", "Teddy Ferdinan"]
year: 2025
venue: "arXiv preprint 2511.03823 (v1, 83 pages)"
arxiv: "2511.03823"
url: "https://arxiv.org/abs/2511.03823"
citekey: kocon2025pllum
verified: 2026-10-27
theme: "[[Evaluated LLMs]]"
related: ["[[2026-10-27-temporal-retrieval-eval]]", "[[LLM selection]]", "[[Qwen3 Embedding]]", "[[AMC-16K]]", "[[Language and Retrieval Bias]]", "[[Bielik 11B v3]]", "[[polish-reranker-roberta-v3]]", "[[bge-reranker-v2-m3]]", "[[PIRB]]", "[[Command A]]"]
tags: [type/paper, theme/llm-evaluated, topic/polish, topic/multilingual, topic/llm, topic/reranking]
---
# PLLuM

> [!info] TL;DR
> PLLuM is a family of Polish-focused models (8B to 70B) adapted from Llama 3.1 and Mistral models, built by a consortium of Polish institutions on a 140B-token Polish corpus. The paper also describes 77k organic instructions, 100k preference pairs, a safety filter and a public-administration assistant. It names no training cutoff and reports no reranker test of PLLuM itself, but includes a Polish retrieval and reranker comparison that we reuse.

## Motivation

- English-centred models give limited support to Polish, and commercial models offer little transparency about data.
- Polish institutional text (law, administration, science) was not available in one governed, legally vetted corpus.
- A national assistant for public services needs safe, culturally correct Polish output and retrieval-augmented answers.
- Peer effort: [[Bielik 11B v3]] is the other Polish model family, built by SpeakLeash.

## Method

Notation: query post $q$, candidate fact-check $f$; a model would score the pair $(q, f)$ as a reranker.

**Corpus.** The research corpus has 390M documents and 139.9B tokens of Polish text after cleaning and deduplication; an open-model subset has 5.0B tokens and an open subset 3.9B. About 3B tokens are institutional and official text, and 921M tokens were cleaned by hand. English and Baltic or other Slavic corpora are added for transfer.

**Base models and training.** Continual pre-training of existing models rather than training from scratch: Llama 3.1 8B and 70B, Mistral-Nemo-Base-2407 (12B) and Mixtral 8x7B. Pre-training used up to 180B tokens (full corpus) or 8B tokens (open-licence corpus). Training from scratch was tried and found inferior at this data scale.

**Instructions and alignment.** PLLuMIC contains 77k instructions (organic, synthetic and converted), followed by a two-stage preference optimisation on 100k preference examples with human annotation. A hybrid filter and correction module screens outputs.

**Released models.** The 8B and 70B Llama-PLLuM models carry the Llama 3.1 licence; the 12B and 8x7B models come under Apache 2.0 and as non-commercial CC-BY-NC-4.0 variants. Bielik's report lists Llama-PLLuM-70B at 70.6B parameters, about 141 GB of bf16 weights; a 12B model needs about 24 GB.

**Cutoff.** The paper states no training cutoff. It mentions only that evaluation texts from 2024 were published after the data-collection cut-off point.

## Key numbers

- Llama-PLLuM-70B-instruct scores 87.6 in the LLM-as-judge RAG evaluation, above Llama-3.3-70B at 84.5 and Bielik 2.2 at 85.5, below Llama-3.1-70B at 90.3 (judge: Command R+).
- Llama-PLLuM-70B scores 89.7 on RAG-IFEval, third among large models; Llama-PLLuM-8B at 85.8 leads models below 12B.
- In the paper's Polish administration retrieval test with a BGE-M3 first stage, Qwen3-Reranker-8B reaches NDCG@10 of 84.8 on EZD-IR, bge-reranker-v2-m3 85.4 and polish-reranker-roberta-v2 83.0.
- BM25 scores 75.3 on EZD-IR, above bge-m3 at 74.1, so lexical retrieval stays competitive on long documents.

## Experiments

- **Base-model comparison:** perplexity on 5,000 Polish texts from 2024 ranks candidates; a scratch-trained model wrote fluent Polish but hallucinated, and vocabulary extension did worse than plain continual pre-training.
- **Instruction ablations:** example packing and repeated data change results; annealing before instruction tuning helps.
- **Alignment evaluation:** an LLM judge scored seven dimensions, but human annotators corrected it because it overestimated linguistic correctness, factuality and conciseness.
- **Human arena and essays:** Polish speakers compared models in an arena adapted from Chatbot Arena and found negative transfer from English, such as English email conventions inside Polish text.
- **RAG and retrieval:** rule-based RAG-IFEval, a judge-based RAG test on 110 questions, and retrieval over three public-administration sets (OPI-GOV 910 questions, EZD-QA and EZD-IR 1,000 questions each).

## Data

- Polish research corpus: 390M documents, 139.9B tokens, in 18 topic domains.
- PLLuMIC: 77k instructions; preference corpus: 100k examples; 59 organic evaluation task sets.
- Retrieval sets: OPI-GOV, EZD-QA and EZD-IR on Polish government information.

> [!failure] Limitations
> - No pre-training cutoff and no data release for the full corpus, so exposure cannot be audited.
> - Several PLLuM variants are non-commercial, and the 8B and 70B models inherit the Llama licence.
> - Leaderboard and judge scores come from the authors' own pipeline, and the judge was shown to overrate some dimensions.
> - The paper reports no reranking or relevance-judging result for PLLuM models themselves.
> - Chat models carry fine-tuned behaviours such as safety refusals that may not suit raw relevance scoring.

## Relation to our project

- A Polish-specialised candidate beside [[Bielik 11B v3]]; the 12B Apache 2.0 model is the cheapest, and the 70B model shares its base with the Llama family ([[2026-10-27-temporal-retrieval-eval]], [[LLM selection]]).
- The paper's retrieval table is the source for the Polish administration numbers in [[bge-reranker-v2-m3]] and shows that Qwen3-Reranker-8B and polish rerankers are the bar for an LLM reranker on Polish ([[Qwen3 Embedding]], [[polish-reranker-roberta-v3]], [[PIRB]]).
- Its observation that an LLM judge overrates factuality and fluency supports validating every judge against human labels, using the 400 Polish [[AMC-16K]] pairs ([[Language and Retrieval Bias]]).
- The paper used Command R+ as the Polish judge because it was the open model with the best Polish at that time, which motivates [[Command A]] as a judge.
- Cutoff unknown, so PLLuM stays out of the cutoff regression.

## Future work

- **Open:** the paper keeps training a tokenizer and model from scratch as a prospective option once more Polish data exist (searched 2026-10).
- **Open:** a relevance or reranking evaluation of PLLuM chat models on Polish fact-check data (searched 2026-10).
