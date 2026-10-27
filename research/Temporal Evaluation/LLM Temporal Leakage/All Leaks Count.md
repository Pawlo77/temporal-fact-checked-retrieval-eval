---
title: "All Leaks Count"
aliases: ["All Leaks Count, Some Count More: Interpretable Temporal Contamination Detection and Mitigation in LLM Backtesting"]
authors: ["Zeyu Zhang", "Bradly C. Stadie"]
year: 2026
venue: "Findings of the Association for Computational Linguistics: EMNLP 2026, pages 36100-36127"
url: "https://aclanthology.org/2026.findings-emnlp.1690/"
citekey: zhang2026all
verified: 2026-10-27
theme: "[[LLM Temporal Leakage]]"
tags: [type/paper, theme/llm-leakage, topic/temporal, topic/leakage, topic/llm, topic/evaluation]
---
# All Leaks Count

> [!info] TL;DR
> The paper measures how much of an LLM's stated reasoning depends on post-cutoff knowledge, by splitting the rationale into atomic claims, dating each claim and weighting it by its influence on the prediction. The resulting metric, Shapley-DCLR, shows that date-filtered retrieval raises accuracy but also leakage by 2.5 to 4.7 times. A supervised pipeline, TimeSPEC, removes most of that leakage at a small accuracy cost.

## Motivation

- Backtesting an LLM on resolved events assumes it reasons only from knowledge available at a reference date, but pretrained models encode later events ("lookahead bias", Sarkar and Vafa, 2025).
- Retrieval adds a second channel: date filters admit post-cutoff content through unreliable metadata ([[Temporal Leakage in Date-Filtered Web Retrieval]]).
- Instructing the model to ignore later knowledge does not work ([[Simulated Ignorance Fails]]).
- Existing remedies are coarse: temporally partitioned pretraining needs one model per cutoff, contamination audits flag whole items, and memorisation tests do not say which information moved the answer.

## Method

Notation: reference date $t_{ref}$ (the paper's), claim $c$, rationale $R$ as a set of claims; this is the only place the paper's symbols are used.

**Leakage of a claim.** The grounding function $\tau(c)$ is the earliest time at which $c$ is publicly knowable ($-\infty$ for timeless facts). A claim leaks iff $\tau(c) > t_{ref}$, giving indicator $\ell(c)$.

**Decision weight.** The Shapley value $\phi_i$ of claim $i$ is its average marginal contribution to the prediction score over all orders in which claims could be shown to the model. Exact values cost $2^n$ model runs, so Leverage SHAP estimates them with $O(n \log n)$ coalitions.

**Shapley-DCLR.** $\sum_i |\phi_i|\,\ell(c_i) \,/\, \sum_i |\phi_i|$.

Intuition: the share of the evidence that actually drives the prediction which comes from after the cutoff; a leaked aside counts little, a leaked key fact counts a lot.

**Claim taxonomy.** Nine classes: C0-C1 are safe without checking, C2-C6 need a date check by external search, C7-C8 are leaked by definition.

**TimeSPEC.** A generator issues date-filtered queries and drafts a rationale; a supervisor extracts and classifies claims; violations trigger regeneration with deliberately different queries; a closed-world aggregator answers from the task input and validated claims only.

## Key numbers

- Treatment questions, Qwen3.5-35B: Temporal RAG reaches DCLR 13.1% and accuracy (1 minus Brier) 85.4%; TimeSPEC 1.8% and 83.9%; a bare date hint 5.2% and 80.5%.
- Control questions, which resolve after every model's cutoff so only retrieval can leak: Temporal RAG still has DCLR of 16.7%, 17.0% and 18.5% (three models), against 0.2% to 0.6% for no-retrieval baselines.
- Adding supervision to Temporal RAG cuts DCLR by 83% to 89% at accuracy costs of 0.3 to 1.5 points.
- Frozen-snapshot arm on 159 matched questions: DCLR 3.6% (Wayback snapshots) against 3.3% (live date-filtered) and 1.8% (TimeSPEC).

## Experiments

- **Ablation over (search, supervision):** four systems on three LLMs (Qwen3.5-35B, Kimi-K2.5, Claude Sonnet 4); retrieval alone helps accuracy and amplifies leakage, supervision alone removes leakage but loses evidence, and only the combination keeps both.
- **Metric validity:** the Control group gives a near-zero floor and Treatment raises DCLR 5.0 to 8.7 times for the bare hint; a 90-claim audit gives 97.8% category agreement with humans (kappa 0.975) and two annotators agree on 97.5% of 120 claims.
- **Shapley versus counting:** the unweighted leaked-claim rate tracks DCLR in aggregate (Pearson 0.91 to 0.96) but hides severity on individual instances; leave-one-out influence is off by up to 13 points when claims interact.
- **Leakage-sensitivity probe:** on Qwen3.5-35B, suppressing leakage costs most where the task depends on later knowledge. Stock ranking drops 0.091 and Temporal RAG sits at DCLR 73.3%; NBA salary prediction improves from 0.635 to 0.695 because verified comparables replace memorised contracts; legal outcomes are unchanged (0.818 against 0.815).
- **Frozen snapshots:** archived pages are no better than live date-filtered retrieval; the paired DCLR difference is +0.4 points with an interval spanning zero. Supervision, not the retrieval source, drives the gain.

## Data

- Treatment: 1,942 binary Autocast questions, all resolved before each model's cutoff.
- Control: 827 ForecastBench questions resolving after every cutoff.
- Probe: 100 stock-ranking instances (COVID period), 137 NBA free-agent contracts (2019 to 2025), 100 Supreme Court cases.
- Cost: about $0.051 per question end to end, of which supervision is about $0.006.

> [!failure] Limitations
> - The audit sees only stated evidence; knowledge used silently is missed, so DCLR can underestimate contamination.
> - Leakage is blocked, not removed: the aggregator is still a pretrained LLM.
> - Covers binary, ranking, numeric and classification forecasting; open-ended generation and long chains are untested.
> - The human audits are focused challenge sets, not population estimates.
> - No retrieval ranking metric or fact-check setting.

## Relation to our project

- If an LLM reranker returns rationales, claim-level dating gives a way to measure parametric and retrieved leakage per claim, complementing our knowledge-cutoff strata (RQ5 in [[2026-10-27-temporal-retrieval-eval|Project plan]], [[2026-10-27-topic-research|Topic research]]).
- Its Control/Treatment design (questions after every cutoff versus before) is the model for separating parametric from retrieval leakage in our own pool.
- Confirms that a hard date filter is insufficient, so the causal pool $P(q)$ needs stored timestamps ([[Temporal Leakage in Date-Filtered Web Retrieval]], [[LLM Temporal Leakage]]).
- Avoid: treating output-level audits as proof of no leakage; stratification by cutoff is still needed.

## Future work

- **Open:** auditing latent reasoning rather than stated evidence, and removing leakage at the source through time-partitioned pretraining or temporal-discipline training (searched 2026-10).
- **Open:** open-ended generation, long reasoning chains and multi-step temporal dependencies (searched 2026-10).
- **Open:** applying claim-level temporal auditing to retrieval and fact-checking pipelines (searched 2026-10).
