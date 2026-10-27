---
title: "Language and Retrieval Bias"
aliases: ["Investigating Language and Retrieval Bias in Multilingual Previously Fact-Checked Claim Detection"]
authors: ["Ivan Vykopal", "Antonia Karamolegkou", "Jaroslav Kopčan", "Qiwei Peng", "Tomáš Javůrek", "Michal Gregor", "Marian Simko"]
year: 2026
venue: "Proceedings of the 19th Conference of the European Chapter of the ACL (EACL 2026), Volume 1: Long Papers, pages 5195-5221"
arxiv: "2509.25138"
doi: "10.18653/v1/2026.eacl-long.240"
url: "https://aclanthology.org/2026.eacl-long.240/"
citekey: vykopal2026investigating
verified: 2026-10-27
theme: "[[Bias]]"
tags: [type/paper, theme/bias, topic/multilingual, topic/polish, topic/llm, topic/dense-retrieval, topic/evaluation]
---
# Language and Retrieval Bias

> [!info] TL;DR
> The paper measures two biases in multilingual PFCR. Language bias: six open LLMs judging post-fact-check relevance on AMC-16K mostly do worse when instructed in the target language instead of English, especially zero-shot; task descriptions and few-shot examples narrow the gap. Retrieval bias: dense retrievers return some fact-checks, including malformed ones and COVID-19 claims, far more often than the post distribution warrants.

## Motivation

- [[AMC-16K]] evaluated LLMs for PFCR with English instructions only, so the effect of the instruction language was unknown.
- Multilingual LLMs are known to favour high-resource languages, which matters for fair access to fact-checking.
- No PFCR work had defined a tendency of retrievers to over-return certain fact-checks; the analogue in recommender systems is popularity bias ([Abdollahpouri et al., 2021](https://doi.org/10.1145/3450613.3456821) is cited for its metrics).

## Method

We write a post as $q$, a fact-checked claim as $f$, and Success@k and MRR as in our glossary.

**Language bias.** Six LLMs (Qwen3 8B and 14B, Llama 3.1 8B and 70B, Gemma 3 12B and 27B) label each AMC-16K pair as relevant or not. Prompting strategies are zero-shot, zero-shot with task description, few-shot (10 examples) with task description, and chain-of-thought. Prompts are translated by GPT-4.1 into the 19 non-English dataset languages and Chinese, then reviewed by native or proficient speakers. Bias is the macro F1 difference between target-language and English instructions; crosslingual pairs use either the post's or the claim's language.

**Retrieval bias.** It is defined as retrieving certain $f$ more often than others regardless of relevance. A T5 dual encoder (Ni et al., 2022) and Multilingual E5 rank all claims for 1,239 test pairs of MultiClaim, keeping the top 20. The authors count how often each $f$ appears and model topics of posts and retrieved claims with Semantic Signal Separation (30 topics).

Intuition: if a fact-check appears in many unrelated top lists, its retrieval reflects the retriever and the corpus, not the post.

**Mitigation probe.** Three LLMs classify the top candidates zero-shot; the top-scoring relevant one gives a top-1 accuracy.

## Key numbers

- Monolingual, averaged over models: target-language instructions change macro F1 by -4.00 zero-shot and +2.03 with task description; Gemma 3 27B gains in every strategy.
- Language families: Slavic languages, Polish included, gain about 2.5 to 3.5 macro F1 points from target-language instructions; Burmese loses up to 14.
- Retrieval: Multilingual E5 Success@1 38.8%, Success@10 82.9%, Success@20 88.5%, MRR 53.98; Qwen3 8B filtering raises top-1 accuracy to 63.12%.
- COVID-19 and vaccine topics are 23.0% of posts but 49.5% of retrieved claims and 44.8% of false top-1 results; a JavaScript snippet appears in 159 top-20 lists.

## Experiments

- **Monolingual instruction language:** zero-shot is English-biased for most models; adding context reduces the bias; Latin-script languages benefit more from target-language prompts than non-Latin scripts.
- **Crosslingual instruction language:** post-language prompts with few-shot examples help most models; claim-language prompts help less; related pairs such as Polish and Serbo-Croatian benefit.
- **Thinking mode:** Qwen3 8B reasoning shrinks the zero-shot gap (-6 to -2.5) and the crosslingual gaps.
- **Chinese vs English instructions:** most models drop with Chinese, Llama 3.1 8B by 12 points on average; Gemma 3 27B gains 2.75.
- **Similarity scores:** true and false top-1 results overlap heavily in cosine (0.8 to 1.0 for E5), so similarity alone cannot separate them.
- **Topic concentration:** posts in low-resource languages concentrate on fewer topics (top topic 21.1% vs 12.1% for high-resource), a proposed link between the two biases.

## Data

- AMC-16K: 16,000 annotated post-claim pairs from MultiClaim, 8K monolingual over 20 languages and 8K crosslingual over 20 language pairs; 16% relevant. Polish has 61 posts and 808 claims; crosslingual pairs include pol-hbs, ces-pol and hun-pol.
- MultiClaim test split for retrieval: 1,239 post-claim pairs, 13,861 retrieved claims.

> [!failure] Limitations
> - Retrieval bias is measured by frequency and topic counts on one test split, without a formal metric controlled for gold relevance or claim popularity in the pool.
> - The mitigation probe reports top-1 accuracy for LLM labels, not a ranked metric comparable with Success@k.
> - Only six open models; no code-switching; AMC-16K covers few scripts.
> - No temporal dimension: frequently retrieved claims could simply be older and more numerous in the pool.

## Relation to our project

- Language bias is already covered here, so our Polish-English contrast must be framed as a difference in temporal penalty, not as language bias ([[Proposed Task]], [[Language scope analysis]]).
- Retrieval bias toward popular claims interacts with sibling qrels: popular claims have more earlier fact-checks, so we stratify the causal penalty by claim-cluster size ([[Enhanced topic research]]).
- Malformed fact-checks recurring in top lists argue for cleaning the pool before indexing, applied equally to full and causal pools ([[Bias]]).
- A causal pool changes which popular claims exist at $t_q$; whether retrieval bias shrinks under $P(q)$ is a question our data can answer.

## Future work

- **Open:** mitigation methods for language and retrieval bias in PFCR beyond LLM reranking (searched 2026-10).
- **Open:** fairness-aware retrieval objectives and frequency-normalised success metrics for PFCR (searched 2026-10).
- **Partly done:** reducing cross-language disparity in LLM fact-checking with prompting and fine-tuning, outside PFCR ([Information Processing and Management, 2026](https://www.sciencedirect.com/science/article/pii/S0306457326000087)).
- **Open:** whether retrieval bias changes when the pool is restricted to fact-checks published before each post (searched 2026-10).
