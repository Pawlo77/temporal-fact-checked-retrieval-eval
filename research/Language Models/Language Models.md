---
title: "Language Models"
tags: [type/theme]
created: 2026-10-27
parent: "[[Research]]"
---
# Language Models

Open-weight LLMs used in our experiments, either as rerankers whose gain may depend on what they saw in pretraining, or as judges that label sibling relevance and narrative drift. Each theme is a folder with a note of its own name that lists its papers.

## Summary

- Six LLMs are evaluated as rerankers because their stated cutoffs differ: [[Llama 3.3]] December 2023, [[Apertus]] March 2024, [[Gemma 3]] August 2024 and [[Olmo 3]] December 2024.
- Only [[Apertus]] and [[Olmo 3]] release their pretraining data, so exposure of a gold fact-check can be measured per query instead of inferred from dates.
- [[Bielik 11B v3]] and [[PLLuM]] are the Polish-specialised models; neither states a training cutoff, so both stay out of the cutoff regression.
- Language coverage differs: [[Llama 3.3]] does not list Polish, [[Olmo 3]] is English only, and none of the nine sources reports a Polish reranking or relevance-judging result.
- The judge panel uses three disjoint families: [[gpt-oss-120b]] (cutoff June 2024, Apache 2.0), [[Command A]] (CC-BY-NC, Polish among 23 languages) and [[Mistral Large 2411]] (research licence, no technical report).
- Bf16 weights run from about 22 GB ([[Bielik 11B v3]]) to 245 GB ([[Mistral Large 2411]]); [[gpt-oss-120b]] ships in 4-bit form at 60.8 GiB.
- Four licences restrict use or release (Gemma terms, Llama 3.3 Community, CC-BY-NC, Mistral Research); whether derived labels may be released stays to confirm per model.
- Open: reliability of LLM judges (self-preference, non-determinism, drift) is covered in [[Judging and Reliability]].

| Theme | Question it answers |
|-------|---------------------|
| [[Evaluated LLMs]] | Which open LLMs serve as rerankers, and what do their cutoffs, data openness, licences and languages allow us to conclude? |
| [[Judge Models]] | Which open LLMs label relevance and drift, and what do their sources say about languages, licence and size? |
| [[Judging and Reliability]] | How reliable, biased or non-deterministic are LLM judges and APIs? |
