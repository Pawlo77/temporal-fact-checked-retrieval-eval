---
title: "No Hindsight for LLM Fact-Checkers"
aliases: ["No Hindsight for LLM Fact-Checkers: Measuring Leakage Channels in Misinformation Detection"]
authors: ["Kuan-Hua Wu Lu", "Yohanes Andre Setiawan"]
year: 2026
venue: "arXiv preprint"
arxiv: "2610.04888"
url: "https://arxiv.org/abs/2610.04888"
citekey: lu2026no
verified: 2026-11-11
theme: "[[Leakage in Verification]]"
tags: [type/paper, theme/verification-leakage, topic/leakage, topic/temporal, topic/llm, topic/english]
---
# No Hindsight for LLM Fact-Checkers

> [!info] TL;DR
> The paper separates two hindsight channels in LLM claim verification: outcomes memorised in pretraining (parametric) and retrieved evidence published after the claim (temporal). It dates every evidence answer of AVeriTeC and QuanTemp++ and builds a point-in-time view with pre-claim evidence only. Masking named entities drops Qwen3-14B Supported recall from 0.421 to 0.131 while accuracy moves 0.032, and a pre-2018 control model moves the other way. Post-claim evidence lifts zero-shot AVeriTeC accuracy by 6.3 points, of which at most 3.1 is strict hindsight; on QuanTemp++ the gap is flat.

## Motivation

- Verification benchmarks score models on labelled claims, so a model can reach a verdict by recalling how the story ended instead of reasoning from what was knowable at claim time.
- Evidence leakage was studied as content overlap: fact-check text copied into evidence ([[Missing Counter-Evidence]]) or filtered by overlap ([Chrysidis et al., 2024](https://arxiv.org/abs/2404.18971)), not by publication date.
- [[AVeriTeC]] and QuanTemp++ design cleaner evidence pools, but neither records a publication date for every evidence page.
- Live search date filters still return post-cutoff pages ([[Temporal Leakage in Date-Filtered Web Retrieval]]).
- Temporal LLM work evaluates only on post-cutoff text or trains date-bounded models; no study measures both channels on the same claims.

## Method

Notation: claim $X$ with date $t_q$; evidence answer $e$ with recovered date $t_e$; label $Y$; representation $R \in \mathbb{R}^{d_R}$; realised outcome embedding $K$; selected evidence embedding $E$.

**Date recovery.** For each AVeriTeC answer the live URL is fetched, else its Wayback capture (gzip decoded). Signals in trust order: URL slug date, JSON-LD `datePublished` or `article:published_time`, generic meta or `<time>` tags; the archive timestamp is kept only as an upper bound. The earliest date in the most trusted tier wins.

**Two evidence views.** The leaked view is the cleaned pool without a date filter. The point-in-time view keeps $e$ only if $t_e$ exists and $t_e \le t_q$; a post-claim archive bound is dropped because it proves nothing about publication. Claims without qualifying evidence keep an empty set. In both views answers are ranked by all-mpnet-base-v2 similarity to the claim and the top $k$ kept; nothing is retrieved from the open web.

Intuition: the point-in-time view is a lower bound on pre-claim evidence, so its gap to the leaked view mixes missing evidence with strict hindsight.

**Parametric probe.** Qwen3-14B answers True or False from its own knowledge; $P(\text{true})$ is the next-token mass on "True" against "False". The probe is repeated with spaCy named entities replaced by typed placeholders. A collapse concentrated on memorable outcomes signals recall rather than reasoning. GPT-2-XL, trained on WebText collected to December 2017 (before 97.5% of claims), estimates the pure information-loss effect of masking; the difference-in-differences is the memorisation component.

**Training objective.** A trainable head on frozen backbone features maximises utility and penalises outcome dependence beyond the evidence:

$$
\max_f \; I(R;Y \mid X) - \lambda\, I(R;K \mid E), \qquad \lambda > 0 .
$$

Intuition: $R$ should predict the verdict without encoding how events unfolded, except what the selected evidence already supports.

The leakage term is bounded by conditional CLUB:

$$
I(R;K \mid E) \le \mathbb{E}_{p(r,k,e)}[\log q_\phi(k \mid r,e)] - \mathbb{E}_{p(e)}\mathbb{E}_{p(r\mid e)p(k\mid e)}[\log q_\phi(k \mid r,e)] .
$$

Training alternates: fit the critic $q_\phi$ by maximum likelihood with the head frozen, then update head and classifier on $\text{CE}(Y,\hat Y) + \lambda \hat I_{\text{CLUB}}$ with the critic frozen.

**Outcome statements $K$.** Qwen3-4B writes a short neutral statement of how events unfolded from the fact-check article (never the label), with verdict and negation words banned. QuanTemp++ has no article URLs, so $K$ comes from the justification text.

**Leakage measurement.** Two ridge regressions predict $K$ from $(R,E)$ and from $E$ alone, fit on train and scored on validation; leakage is the held-out $R^2$ gain.

## Implementation

- **Code:** not released; date cache, split indices, $K$ text and code are promised at camera-ready.
- **Backbone:** Qwen3-14B in non-thinking mode, frozen, 4-bit; final-layer states mean-pooled to 5,120 dimensions and cached.
- **Head:** PCA to 16 dimensions (59–61% variance), then a linear map (AVeriTeC) or shallow MLP (QuanTemp++) to $d_R$, and a linear classifier. $K$ and $E$ use all-MiniLM-L6-v2, each PCA-reduced to 8 dimensions.
- **Critic:** a 2-layer MLP $q_\phi(k \mid R, e)$.
- **Grid:** $\lambda \in \{0, 0.01, 0.02, 0.04, 0.06, 0.1, 0.5\}$ against $d_R \in \{8, 2, 1\}$, five seeds; promising cells rerun with 20 paired seeds. Head chosen at $\lambda=0$, $d_R=32$ for the smallest train-validation gap that keeps validation F1.

## Data

- AVeriTeC: binary subset of 2,795 official claims; 5,565 evidence answers, of which 2,232 have a trusted on-page date and 419 of those (18.8%) postdate the claim. 19.4% of answers have no date signal and 40.5% only an archive bound.
- Processing: Not Enough Evidence dropped, fact-check-site evidence removed, URL and near-text duplicates (Jaccard ≥ 0.8) dropped, duplicate claim IDs collapsed to the earliest date. A chronological 80/10/10 split removes validation or test records whose verdict text appears in train, leaving 2,248 train and 265 validation binary claims.
- QuanTemp++: 4,827 train and 710 validation binary claims, dated mainly from URL slugs and search snippets; only 4.1% of answers postdate the claim; validation is 5.5% Supported.

## Experiments

- **Entity masking:** 2,554 entity-bearing AVeriTeC claims, no evidence, Qwen3-14B, phi-4 and GPT-2-XL; in-window models collapse toward "False", the control does not.
- **Label-conditioned check:** confidence change split by gold label rules out a label-blind drift toward each model's prior.
- **Width vs penalty:** the $\lambda \times d_R$ grid with claim-only and top-5 point-in-time evidence; narrowing $d_R$, not raising $\lambda$, removes leakage.
- **Zero-shot temporal gap:** Qwen3-14B with top-5 leaked vs point-in-time evidence on all 2,513 chronological train and validation claims; McNemar and bootstrap tests.
- **Trained-head sensitivity:** the leaked minus point-in-time Supported-recall gap as $\lambda$ grows and $d_R$ shrinks.

## Results

- Qwen3-14B masking: Supported recall 0.421 to 0.131, macro-F1 0.640 to 0.502, accuracy 0.710 to 0.678 against an always-Refuted majority of 0.679.
- phi-4 Supported recall falls 0.277 to 0.039; GPT-2-XL rises 0.394 to 0.686. The difference-in-differences against the control is +0.582 (95% CI +0.533 to +0.630).
- Confidence loss on gold-True minus gold-False claims is +0.190 for Qwen3-14B and +0.175 for phi-4, against +0.009 for GPT-2-XL.
- At $\lambda=0$ on AVeriTeC with evidence, leakage falls from 0.168 to 0.029 as $d_R$ shrinks from 8 to 1, while F1 falls from 0.607 to 0.512. About 0.03 $R^2$ survives every width and penalty.
- A penalty helps only in QuanTemp++ claim-only at $d_R=8$: leakage −0.088 for −0.007 F1 over 20 seeds.
- Zero-shot AVeriTeC: accuracy 0.782 point-in-time vs 0.844 leaked (+6.3, CI 4.9 to 7.8), macro-F1 +7.9, Supported recall +10.4; McNemar $p < 0.001$.
- The gap is +9.0 for the 1,361 claims with no pre-claim evidence and +3.1 for the 1,152 with some; the 3.1 is an upper bound on strict hindsight.
- Without evidence the model reaches 75.3% accuracy; an evidence-only prompt raises macro-F1 inflation from 7.9 to 9.0.
- QuanTemp++ accuracy gap is 0.05% ($p = 0.87$): 91% of leaked top-5 evidence would pass the date filter and 70% of claims get the same top 5.
- The trained head barely reacts to the evidence view at $\lambda=0$ (−1.0 accuracy points on AVeriTeC); pushing it off the parametric shortcut raises the Supported-recall gap from 1.5% to 9.7%.

## Limitations

- 54% of binary AVeriTeC claims have no dated pre-claim evidence, so part of the inflation is missing evidence, not hindsight (authors).
- Recovered dates were not hand-audited; social-media and paywalled pages stay undated (authors).
- The two datasets use different dating instruments, so cross-dataset comparisons are indicative only (authors).
- QuanTemp++ $K$ comes from justification text, so the penalty partly regularises verdict wording; 41% of AVeriTeC $K$ statements carry a banned-word flag (authors).
- One backbone; PCA-compressed features may explain why the head ignores evidence (authors).
- The evidence pool is the benchmark's annotated answers ranked by similarity, not a retrieval system over an archive (ours).
- Claims with an empty point-in-time set are scored with no evidence, so the headline 6.3 conflates answerability with ranking (ours).

## Relation to our project

- **Novelty claim not contradicted.** The paper restricts per-claim evidence to documents dated on or before the claim, but in claim verification, not PFCR. There are no posts, no fact-check archive and no ranking metric.
- It does not build a per-query index of fact-checks published before the post; it removes fact-check sites from evidence altogether.
- Its split of the gap into "no pre-claim evidence" (+9.0) and "has some" (+3.1) mirrors our need to report conditional and unconditional Success@k, separating answerability from ranking ([[Leakage in Verification]]).
- Its date-recovery tiers and the rule that an archive bound after $t_q$ proves nothing support our timestamp-leakage category ([[2026-10-27-temporal-retrieval-eval|Project plan]]).
- The parametric probe supports keeping a parametric-leakage stratum for LLM rerankers ([[LLM Temporal Leakage]]; [[Simulated Ignorance Fails]]).

## Future work

- **Open:** a debiased detector on claims after the backbone's training cutoff with dated evidence, which the authors say needs a new dataset (searched 2026-11).
- **Open:** whether good pre-claim evidence exists at all across corpora, the ceiling every point-in-time system faces (searched 2026-11).
- **Open:** a hand-audited sample of recovered evidence dates to bound date error (searched 2026-11).
