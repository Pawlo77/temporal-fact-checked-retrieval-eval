---
title: "Self-Preference Bias"
aliases: ["LLM Evaluators Recognize and Favor Their Own Generations"]
authors: ["Arjun Panickssery", "Samuel R. Bowman", "Shi Feng"]
year: 2024
venue: "Advances in Neural Information Processing Systems 37 (NeurIPS 2024), pages 68772-68802"
arxiv: "2404.13076"
url: "https://proceedings.neurips.cc/paper_files/paper/2024/hash/7f1f0218e45f5414c79c0679633e47bc-Abstract-Conference.html"
citekey: panickssery2024self
verified: 2026-10-27
theme: "[[Judging and Reliability]]"
related: ["[[2026-10-27-temporal-retrieval-eval]]", "[[LLM selection]]", "[[Panel of LLM Evaluators]]", "[[Rubric Self-Preference]]", "[[LLM Judges Favour LLM Rankers]]"]
tags: [type/paper, theme/llm-judging, topic/judge-bias, topic/evaluation, topic/llm, topic/english]
---
# Self-Preference Bias

> [!info] TL;DR
> LLM evaluators give higher scores to their own summaries than to those of other LLMs or humans. GPT-4 distinguishes its own text from two other LLMs and humans with 73.5% accuracy out of the box, and fine-tuning pushes GPT-3.5 and Llama 2 above 90%. The strength of self-preference rises linearly with self-recognition, which suggests recognition causes the bias.

## Motivation

- Self-evaluation is used in model-based benchmarks, reward modeling and self-refinement, so the same model often acts as evaluator and evaluatee.
- Self-preference had been seen in dialogue benchmarks and summarisation ([Liu et al., 2023](https://arxiv.org/abs/2311.09766)), but nobody explained it or tried to change its strength.
- If a judge prefers text because it recognises it as its own, bias can be reduced by hiding the author, otherwise not.

## Method

Notation: an evaluator model is asked a quality question (self-preference) or an authorship question (self-recognition) about a pair of texts or a single text.

**Self-preference.** The evaluator sees its own summary and one from another source and picks the better one. Order bias is handled by asking twice with swapped order and averaging the confidences from output token probabilities.

**Self-recognition.** The same pair is shown, and the evaluator picks the text it wrote. An individual variant shows one text and asks yes or no, or a 1 to 5 rating.

**Causal test.** The authors fine-tune evaluators on 500 articles to raise or lower self-recognition, then plot self-preference against self-recognition. Control fine-tunings on unrelated tasks check for confounders.

Intuition: if training a model to spot its own writing also makes it favour that writing, spotting is plausibly the mechanism.

## Key numbers

- GPT-4 reaches 73.5% accuracy telling its summaries from those of two other LLMs and humans; all three models exceed 50% out of the box.
- After fine-tuning on 500 examples, GPT-3.5 and Llama 2 exceed 90% self-recognition accuracy.
- Pairwise preference reverses when the option order is swapped in 25% (GPT-4), 58% (GPT-3.5) and 89% (Llama 2) of cases.
- The example-level Kendall correlation between recognising and preferring one's own summary is 0.41 on XSUM and 0.37 on CNN/DailyMail for GPT-3.5 before fine-tuning.

## Experiments

- **Out of the box:** GPT-4, GPT-3.5 and Llama 2 summaries compared; the self-preference scores of each model pair sum to more than one, so both prefer themselves, and weaker models cannot tell themselves from stronger ones.
- **Fine-tuning for recognition:** self-recognition and self-preference follow a linear trend across models, and training on one dataset transfers to the other.
- **Inverse causality:** evaluators do not favour generations of fine-tuned models over the originals (average preference 0.46, and only 22% of evaluator-domain pairs above 0.51), so higher quality is not the cause.
- **Confounders:** fine-tuning on length, vowel count, Flesch-Kincaid readability, constant output "1" and random output lands on the same line.
- **Source labels:** swapping the source labels reverses the preference for GPT-4 and GPT-3.5 on XSUM, but not on CNN/DailyMail or for Llama.

## Data

- XSUM and CNN/DailyMail: 1,000 news articles each with human summaries; 500 for fine-tuning and 500 for evaluation.
- Generators and evaluators: Llama-2-7b-chat, GPT-3.5 and GPT-4, summaries sampled at temperature zero.

> [!failure] Limitations
> - Only summarisation with three models, and the paper shows other studies reach opposite model rankings on other tasks.
> - Quality is not controlled against ground truth, so self-preference is not proved to be disproportionate.
> - Causality is shown at the capability level only, not for individual examples, and the fine-tuning controls cannot rule out every confounder.
> - Prompts were a single simple design, and the label-swap effect is not seen on all datasets or models.

## Relation to our project

- It is the second pillar for disjoint judge families: no judge family may also supply an evaluated or pooled system ([[LLM selection]]; [[2026-10-27-temporal-retrieval-eval|Project plan]]).
- Our relevance labels mostly judge human-written fact-checks, which weakens the recognition channel, but judging model-written rationales, drift narratives or failure codes brings it back, so the panel avoids all family overlap.
- Pairwise sibling judgments are run in both orders and averaged, since order flips are common and strongest for weaker models.
- Hiding the author of outputs is a free mitigation, which the authors suggest as a standard practice.
- It does not show that a panel removes the bias ([[Panel of LLM Evaluators]]; [[Rubric Self-Preference]]).

## Future work

- **Partly done:** self-preference in other evaluation formats; [Pombal et al., 2026](https://arxiv.org/abs/2604.06996) study rubric-based judging and find it persists ([[Rubric Self-Preference]]).
- **Done:** judge panels as a counter-measure; [Verga et al., 2024](https://arxiv.org/abs/2404.18796) report lower intra-model bias ([[Panel of LLM Evaluators]]).
- **Open:** paraphrasing outputs to block recognition and testing the example-level hypothesis (searched 2026-10).
- **Open:** controlling for true quality with ground-truth annotation to measure disproportionate preference (searched 2026-10).
