---
title: "Apertus"
aliases: ["Apertus: Democratizing Open and Compliant LLMs for Global Language Environments"]
authors: ["Alejandro Hernández-Cano", "Alexander Hägele", "Allen Hao Huang", "Angelika Romanou"]
year: 2026
venue: "Proceedings of the 64th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pages 46877-46955; read as arXiv 2509.14233; Hugging Face card swiss-ai/Apertus-70B-Instruct-2509"
doi: "10.18653/v1/2026.acl-long.2172"
url: "https://aclanthology.org/2026.acl-long.2172/"
citekey: hernandezcano2026apertus
verified: 2026-10-27
theme: "[[Evaluated LLMs]]"
related: ["[[2026-10-27-temporal-retrieval-eval]]", "[[LLM selection]]", "[[Qwen3 Embedding]]", "[[AMC-16K]]", "[[Language and Retrieval Bias]]", "[[Olmo 3]]", "[[Gemma 3]]", "[[Llama 3.3]]", "[[Simulated Ignorance Fails]]"]
tags: [type/paper, theme/llm-evaluated, topic/multilingual, topic/llm, topic/reranking, topic/leakage]
---
# Apertus

> [!info] TL;DR
> Apertus is a fully open 8B and 70B model suite from the Swiss AI Initiative, pre-trained on 15T tokens from 1,811 languages. Data are filtered for opt-outs applied retroactively and for personal data, and a Goldfish loss suppresses verbatim recall. Weights, code, checkpoints and data-reconstruction scripts are released under Apache 2.0, with a stated March 2024 knowledge cutoff.

## Motivation

- Open-weight models rarely release their data, and some allegedly contain material that site owners opted out of through `robots.txt`.
- Most open models cover a handful of languages; Apertus aims at over 1,800 and puts about 40% of its text mixture into non-English data.
- Verbatim regurgitation of training text raises copyright and privacy risks, so the authors train against memorization.
- For our study the point is auditability: Apertus is the first fully open model at 70B scale, so its pretraining corpus can be searched for a given fact-check; compare [[Olmo 3]] at 32B.

## Method

Notation: query post $q$, candidate fact-check $f$; the model scores the pair $(q, f)$ as a reranker.

**Data.** The web part comes from FineWeb-2, with a quality-filtered FineWeb-2-HQ for 20 high-resource languages, which include Polish. Polish is 3.03% of FineWeb-2 documents (138M). English uses FineWeb-Edu, DCLM and FineWeb-HQ, plus code, mathematics and parallel data. Crawls cover 2013 to 2024.

**Compliance.** The `robots.txt` files of January 2025 were applied retroactively to all earlier crawl dumps, removing about 8% of English and 4% of multilingual tokens. Personal data are masked, and toxicity classifiers cover nine languages, Polish among them.

**Goldfish loss.** The causal language-modelling loss is computed on only a hashed subset of tokens (about 0.3T of 15T were masked). Intuition: the model never learns long continuous spans, so it cannot recite them.

**Training.** A decoder-only transformer with the xIELU activation and the AdEMAMix optimizer, trained in five stages on 4096 GH200 GPUs, then extended to 65,536 tokens of context. Post-training uses 3.8M supervised examples, 149 languages and QRPO alignment.

**Cutoff, licence, size.** The report's system-prompt template states "Knowledge cutoff: March 2024". The 70B model has 70.6B bf16 parameters (about 141 GB of weights), the licence is Apache 2.0, and the card gates access behind an acceptable-use policy.

## Key numbers

- Apertus-70B-Instruct scores 61.5 on the cultural-knowledge average, below gemma-3-27b-it at 67.7 and Llama-3.3-70B-Instruct at 69.6 (post-training evaluation).
- Pretrained 70B averages 67.5 on the card's general-understanding tasks, against 67.3 for Llama 3.1 70B and 69.8 for Qwen2.5-72B.
- Instruction following: 75.2 on IFEval, against 90.8 for Llama 3.3 and 81.3 for Gemma 3 27B.
- Memorization probe: Rouge-L of 0.188 after 128 exposures against 0.178 for unseen text, which is close to baseline.

## Experiments

- **Pretraining benchmarks:** general understanding, XNLI, XCOPA and INCLUDE across 44 and 45 languages; the 70B model leads fully open models on INCLUDE.
- **Post-training evaluation:** knowledge, cultural, maths, code and instruction-following suites in 94 languages; weakest in maths, code and reasoning because no verifiable-reward RL was applied.
- **Long context:** RULER at 4K to 64K tokens for both instruct models.
- **Memorization:** book sequences injected at 1 to 128 exposures; Goldfish keeps recall near baseline, though near-duplicate canonical works (poems, plays, constitutions, the Bible) are still memorized.

## Data

- Pretraining corpus: 15T tokens, 1,811 languages, reconstructable with released scripts, not hosted as a dump.
- Post-training: a 3.8M-example supervised mixture on Hugging Face, plus preference data.
- Evaluation: INCLUDE V1 and V2, BLEnD, CulturalBench, Switzerland QA, Global-MMLU, MGSM, IFEval and RULER.

> [!failure] Limitations
> - Instruction following and reasoning trail Llama 3.3 and Gemma 3 at similar scale, which can lower reranking quality.
> - The cutoff of March 2024 comes from a prompt template, and web dumps contain older and newer text than any single date.
> - Retroactive opt-outs remove data, so the corpus is not what a crawler saw at the time.
> - Goldfish loss is fragile to near-duplicates, so memorization suppression is partial.
> - No Polish-specific retrieval or reranking result is reported.

## Relation to our project

- Reranker 3 for RQ4, the auditable one: for each gold fact-check we can search the reconstructed corpus for its URL and long claim n-grams and use per-query exposure instead of date strata. See ([[2026-10-27-temporal-retrieval-eval]], [[LLM selection]]).
- Goldfish loss makes it a low-memorization contrast: an exposure effect may be weaker here than for [[Gemma 3]] or [[Llama 3.3]], which is itself informative.
- The 70B model needs two 80 GB GPUs for bf16 weights; the 8B model supplies the size axis at about 16 GB.
- Polish is a high-resource language in its data, but no Polish judge or reranker validation exists, so we use the 400 Polish [[AMC-16K]] pairs first ([[Language and Retrieval Bias]]).
- Retroactive opt-out removal means fact-check sites that blocked crawlers may be absent, so absence from the corpus is not proof of absence from the web.

## Future work

- **Open:** the report notes that reinforcement learning with verifiable rewards was not yet applied, and releases its artifacts to enable independent audit (searched 2026-10).
- **Open:** a Polish retrieval, reranking or relevance-judging result for Apertus (searched 2026-10).
- **Open:** a per-query exposure measurement of a retrieval benchmark against the Apertus corpus (searched 2026-10).
