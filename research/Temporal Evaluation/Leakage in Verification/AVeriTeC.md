---
title: "AVeriTeC"
aliases: ["AVeriTeC: A Dataset for Real-world Claim Verification with Evidence from the Web"]
authors: ["Michael Schlichtkrull", "Zhijiang Guo", "Andreas Vlachos"]
year: 2023
venue: "Advances in Neural Information Processing Systems 36 (NeurIPS 2023), Datasets and Benchmarks Track"
arxiv: "2305.13117"
url: "https://arxiv.org/abs/2305.13117"
citekey: schlichtkrull2023averitec
verified: 2026-10-27
theme: "[[Leakage in Verification]]"
tags: [type/paper, theme/verification-leakage, topic/leakage, topic/temporal, topic/benchmark, topic/english]
---
# AVeriTeC

> [!info] TL;DR
> AVeriTeC releases 4,568 real-world claims from 50 fact-checking organisations, each with question-answer evidence from the open web and a written justification. Annotators may only use documents published before the claim, and train, dev and test are ordered in time, so evidence from the future cannot leak in. The guarantee is approximate, and a simple web-search baseline reaches only 0.23 macro-F1 on verdicts.

## Motivation

- Many verification datasets use synthetic claims built from Wikipedia, unlike claims journalists check.
- Datasets with real claims often lack evidence annotation or add it automatically, which in MultiFC can include evidence published days or weeks after the claim ([Glockner et al., 2022](https://aclanthology.org/2022.emnlp-main.397/); [[Missing Counter-Evidence]]).
- Labels in some datasets do not follow from the annotated evidence, and some claims cannot be understood without the source article.
- Leaks also cross splits: evidence for a 2021 training claim can pertain to a 2020 test claim.

## Method

Notation: the paper's claim date plays the role of the query time $t_q$; evidence documents must satisfy $t_d < t_q$, the causal-pool condition applied to web documents.

**Annotation in three phases.** Claims are taken from ClaimReview via the Google Fact Check API and normalised (context added, split into single claims). Annotators then write question-answer pairs, each answer backed by a source URL, and give a verdict; the fact-check itself and other fact-checking articles are forbidden as evidence. A second annotator, blind to the article and label, sees only the pairs and gives a verdict and justification; disagreement triggers a repeat with new annotators (up to five annotators per claim).

**Temporal guard.** Annotators use documents linked from the article, or a custom Google search restricted to documents published before the claim date (the article date if the claim date is unknown). Splits are ordered in time.

Intuition: evidence the claim's author could not yet have seen is the only evidence a real-time checker could use.

**Evaluation.** Generated question-answer pairs are matched to gold ones with the Hungarian algorithm over METEOR; veracity and justification count only when the evidence score reaches 0.25.

## Key numbers

- 4,568 claims, 50 organisations, 2.60 questions per claim; $\kappa = 0.619$ on verdicts over 100 re-annotated claims (free-marginal).
- Verdict macro-F1: no evidence 0.17, baseline pipeline 0.23, gpt-3.5-turbo 0.39, gold evidence 0.49.
- About 6% of dev answers come from a fact-checking domain, mostly an earlier fact-check of the same claim by another outlet.
- Google results held useful evidence in 9 of 20 manually inspected dev claims, 16 of 20 when gold questions were the queries.

## Experiments

- **Baseline pipeline:** claim keywords and generated questions as Google queries limited to pre-claim documents, BM25 to the top 100 sentences, a BLOOM-7b generated question per sentence, BERT reranking and stance classification, BART justifications; evidence recall is close to human-annotator agreement but veracity stays low, mostly from wrong evidence.
- **Gold vs no evidence:** gold question-answer pairs lift veracity to 0.49 against 0.17 without evidence, so evidence helps and retrieval is the bottleneck.
- **gpt-3.5-turbo:** better at question generation and verdicts (0.39) but scores lower under the evidence-conditioned metric because answers are unsourced and often hallucinated.
- **Stance detection:** paraphrasing claims with ChatGPT as augmentation did not help (0.46 vs 0.49 with gold evidence); conflicting-evidence claims are rarely recognised even with gold evidence.

## Data

- Train 3,068, dev 500, test 1,000 claims, with end dates 25-08-2020, 31-10-2020 and 22-12-2021; the train set has no start date.
- Labels (train/dev/test, percent): supported 27.6/24.4/25.5, refuted 56.8/61.0/62.0, conflicting 6.4/7.6/6.3, not enough evidence 9.2/7.0/6.2.
- Answers: 53% extractive, 26% abstractive, 17% boolean, 4% unanswerable; 24 to 28% of claims were re-annotated.

> [!failure] Limitations
> - The temporal guarantee is approximate: Google's publication dates are estimates, and news about a claim can appear during the days a fact-check takes.
> - Fact-checks by other organisations of the same claim still enter as evidence (about 6% of dev answers).
> - The metric cannot detect answers unsupported by their source, and penalises valid alternative evidence paths.
> - English only; claims inherit selection bias from fact-checkers and are skewed to refuted.
> - The full text read here is the arXiv version; the NeurIPS proceedings page carries no DOI, so only the arXiv id is verified.

## Relation to our project

- Direct precedent for a causal evidence constraint plus temporally ordered splits, which supports our training-regime arm and the parametric-leakage stratum ([[2026-10-27-temporal-retrieval-eval|Project plan]]; [[Topic research]]).
- Its finding that an earlier fact-check of the same claim by another outlet counts as legitimate pre-claim evidence matches our earlier-sibling cluster-expanded relevance sets.
- Its date-noise caveat supports our timestamp-leakage category and margin sensitivity ([[Leakage in Verification]]).
- It does not cover matching posts to a fact-check archive, ranking metrics, pool size or non-English data ([[Language scope]]).

## Future work

- **Partly done:** the shared tasks built on the dataset evaluate open-system pipelines on the same test protocol ([Schlichtkrull et al., 2024](https://doi.org/10.18653/v1/2024.fever-1.1)); [Schlichtkrull et al., 2025](https://doi.org/10.18653/v1/2025.fever-1.15) adds open-weights, reproducible systems.
- **Open:** an evaluation that checks answers against their sources and credits alternative evidence paths, as the authors request, was not found (searched 2026-10).
- **Open:** a version with languages other than English and a pool of dated fact-checks to match posts against (searched 2026-10).
