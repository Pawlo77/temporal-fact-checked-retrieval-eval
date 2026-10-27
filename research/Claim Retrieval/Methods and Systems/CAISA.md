---
title: "CAISA"
aliases: ["CAISA at SemEval-2025 Task 7: Multilingual and Cross-lingual Fact-Checked Claim Retrieval"]
authors: ["Muqaddas Haroon", "Shaina Ashraf", "Ipek Baris Schlicht", "Lucie Flek"]
year: 2025
venue: "Proceedings of the 19th International Workshop on Semantic Evaluation (SemEval-2025), pages 1377-1382"
url: "https://aclanthology.org/2025.semeval-1.183/"
citekey: haroon2025caisa
verified: 2026-10-27
theme: "[[Methods and Systems]]"
tags: [type/paper, theme/methods, topic/multilingual, topic/shared-task, topic/dense-retrieval, topic/reranking, topic/llm]
---
# CAISA

> [!info] TL;DR
> A SemEval-2025 Task 7 system for the crosslingual track: an embedding model keeps 500 candidate fact-checks per post, and Llama-3 8B-Instruct, prompted zero-shot to say whether each is relevant, ranks the top 10. The best configuration, Jina embeddings plus Llama with a task description, reaches Success@10 of 57.7% in the results table. The paper reports three different headline values.

## Motivation

- [[SemEval-2025 Task 7]] asks for previously fact-checked claims for posts in many languages, scored by Success@10 on [[MultiClaim]] data.
- The authors want to know how far an LLM can act as a relevance filter in retrieval-based fact-checking, without fine-tuning.
- The paper cites [[MultiClaim]] for the finding that supervised fine-tuning beats unsupervised methods; it does not fine-tune.

## Method

We write a post as $q$, a fact-check as $f$ and Success@10 as in the glossary.

**Preprocessing.** Posts and fact-checks are cleaned; missing post text is replaced by OCR text, claim titles and summaries are added, and LSA summaries and URL-derived names serve as extra fields.

**Candidate generation.** Three embedders each select the 500 fact-checks with highest cosine similarity: Jina embeddings v2 (English only, used on English translations and mapped back to the original text), paraphrase-multilingual-mpnet-base-v2 and multilingual-e5-large-instruct on original-language text.

**LLM relevance filter.** Llama-3 8B-Instruct is prompted zero-shot, with or without a task description, to label each candidate relevant or not and give a score from 0 to 1. The list is sorted by that score and the top 10 returned.

Intuition: a cheap embedder narrows the pool, and the LLM reads each candidate against the post to judge relevance.

## Key numbers

- Llama with task description over Jina candidates: Success@10 57.7%; Jina alone 55.2%.
- With e5-large: Llama with description 54.3%, e5-large alone 54.3%, so no gain; with MPNet: 38.6% against 22% alone.
- Llama zero-shot without a task description: 11%.
- The abstract says 0.57 on the crosslingual track and the conclusion says 55.7%; the table value is 57.7%.

## Experiments

- **Embedders alone:** Jina 55.2%, e5-large 54.3%, MPNet 22%; the authors say embedder choice matters.
- **Llama over each candidate list:** a task description raises accuracy over the bare prompt; the gain is largest where the embedder is weakest (MPNet).
- **Prompt detail:** a detailed instruction beats a bare zero-shot prompt; no few-shot or fine-tuned variants are tried.

## Data

- [[SemEval-2025 Task 7]] data built on [[MultiClaim]]: 28,092 posts in 27 languages, 205,751 fact-checks in 39 languages and 31,305 post-claim links, with machine translations, plus new Turkish and Polish data from the organisers.
- Train, validation and test splits are made from the given post-claim pairs; the paper does not describe the split rule.

> [!failure] Limitations
> - The three headline values (0.57, 55.7%, 57.7%) disagree, and the evaluation split is not stated.
> - The model is cited as LLaMA with a 2023 reference while named Llama-3 8B-Instruct; the exact release is unclear.
> - The Llama-with-e5-large result equals e5-large alone (54.3%), suggesting little added value outside the Jina setting.
> - Authors note overgeneralisation and hallucinated relations between claims; no ablation or error analysis supports this.
> - No temporal analysis, no mention of the model's training cutoff or of fact-check exposure.

## Relation to our project

- It is the SemEval LLM filtering step our risk register cites: a small LLM used as relevance filter after a dense candidate list, on the full pool ([[LLM selection]], [[2026-10-27-temporal-retrieval-eval|Project plan]]).
- The filter sees the fact-check text and ranks it with parametric knowledge, so for RQ5 its gain should be reported by cutoff stratum and under a causal pool; the paper has neither.
- Its gains depend on the embedder, as in [[TIFIN India]], where reranking added 1.7%; report reranking against the first-stage ranking alone.
- Weak and inconsistent numbers make it a design reference, not a baseline to reproduce.

## Future work

- **Open:** the authors call for further refinement to improve accuracy and reliability across languages, without a concrete plan (searched 2026-10).
- **Open:** the same filter under a time-respecting split and date-restricted pool (searched 2026-10).
