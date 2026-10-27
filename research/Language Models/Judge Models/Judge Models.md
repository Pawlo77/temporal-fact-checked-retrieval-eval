---
title: "Judge Models"
tags: [type/theme, theme/llm-judge-model]
parent: "[[Language Models]]"
---
# Judge Models

Open-weight LLMs that label sibling relevance and narrative drift. They come from families disjoint from every evaluated and pooled system, and are combined as a three-family panel validated against human labels.

## Summary

- [[gpt-oss-120b]]: 116.8B mixture-of-experts, 5.1B active, one 80 GB GPU, cutoff June 2024, Apache 2.0; its multilingual test omits Polish.
- [[Command A]]: 111B, 23 languages including Polish, 256K context, CC-BY-NC; answers when context supports it and declines otherwise (96% and 91% accuracy on answerable and unanswerable questions).
- [[Mistral Large 2411]]: 123B, research licence, card without benchmarks or report; its family led relevance labelling in [[AMC-16K]] and the Open PL LLM Leaderboard.
- None of the three states a Polish relevance-judging result; each is validated on the 400 Polish [[AMC-16K]] pairs first.
- Open: bias and reliability of the judges themselves are covered in [[Judging and Reliability]].

| Paper | Year | Takeaway |
|-------|------|----------|
| [[gpt-oss-120b]] | 2025 | Open reasoning MoE at 4-bit; MMMLU 81.3 at high reasoning across 14 languages without Polish; precedent as leakage judge. |
| [[Command A]] | 2025 | Enterprise 111B with RAG and 23 languages; wins 79.9% of Polish prompts against Llama 3.3 70B in an LLM-judged arena; non-commercial weights. |
| [[Mistral Large 2411]] | 2024 | Dense 123B with research-only licence; no cutoff or data statement; leads the open models in the Bielik report's Polish leaderboard. |
