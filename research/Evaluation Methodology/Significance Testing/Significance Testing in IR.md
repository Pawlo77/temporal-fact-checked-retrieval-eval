---
title: "Significance Testing in IR"
aliases: ["Statistical Significance Testing in Information Retrieval", "Statistical Significance Testing in Information Retrieval: An Empirical Analysis of Type I, Type II and Type III Errors"]
authors: ["Julián Urbano", "Harlley Lima", "Alan Hanjalic"]
year: 2019
venue: "Proceedings of the 42nd International ACM SIGIR Conference on Research and Development in Information Retrieval (SIGIR 2019), pages 505-514"
doi: "10.1145/3331184.3331259"
url: "https://doi.org/10.1145/3331184.3331259"
code: "https://github.com/julian-urbano/sigir2019-statistical"
citekey: urbano2019statistical
verified: 2026-11-11
reviewed: 2026-11-11
theme: "[[Significance Testing]]"
tags: [type/paper, theme/significance-testing, topic/significance, topic/evaluation, topic/reproducibility]
---
# Significance Testing in IR

> [!info] TL;DR
> Earlier comparisons of paired significance tests in IR could not count true errors, because the null hypothesis of real TREC data is unknown. The authors simulate new topics for pairs of TREC systems from fitted copula models, so the true means are known. Over about 500 million p-values, the paired t-test and permutation test hold the Type I error at the nominal $\alpha$; the bootstrap-shift, Wilcoxon and sign tests reject too often. They recommend the t-test for mean effectiveness, the permutation test for other statistics, and discontinuing the bootstrap-shift, Wilcoxon and sign tests.

## Motivation

- Surveys of SIGIR, TOIS, CIKM and ECIR papers find about 65% use the t-test and 25% Wilcoxon; sign, bootstrap and permutation tests are rarer ([Sakai, 2016](https://doi.org/10.1145/2911451.2911492); [Carterette, 2017](https://doi.org/10.1145/3077136.3080738)).
- Past empirical studies split 50 TREC topics into 25–25 halves and counted discordant conclusions; without the true null, discordance is not a Type I error.
- Theoretical studies object that IR scores violate normality, symmetry and interval-scale assumptions, but cannot say how much that costs in practice.
- [Smucker et al., 2007](https://doi.org/10.1145/1321440.1321528) used the permutation test as reference and found high t and bootstrap agreement with it; a test can disagree case by case yet keep the same long-run Type I rate.
- [Parapar et al., 2019](https://doi.org/10.1002/asi.24203) simulate new runs for the same topic, whereas testing concerns new topics for the same systems.

## Method

Notation: the paper's topics are our queries $q$, $n = |Q|$; baseline and experimental scores $B_q, E_q$; difference $D_q = E_q - B_q$ with mean $\bar D$ and standard deviation $s_D$; $T$ Monte Carlo replicas. All five tests are paired, over per-topic score differences.

**Hypotheses.** Two-tailed: $H_0: \mu_B = \mu_E$. One-tailed: $H_0: \mu_B \ge \mu_E$ against $\mu_B < \mu_E$. The formulas assume $\bar D > 0$; a one-tailed $p_1$ gives $p_2 = 2p_1$ for the symmetric tests.

**Paired t-test** (R `t.test`).

$$
t = \frac{\bar D}{s_D/\sqrt{n}}, \qquad p_1 = 1 - F_t(t;\, n-1).
$$

Intuition: the mean difference in units of its standard error; the Central Limit Theorem covers non-normal scores when $n$ is not too small.

**Wilcoxon signed-rank** (R `wilcox.test`). Zero differences are dropped, leaving $n_0$; the rest are ranked by $|D_q|$ keeping the sign. $W = \sum_{R_q>0} R_q$ and $p_1 = 1 - F_{WSR}(W; n_0)$.

**Sign test** (own counting, then R `binom.test`). $S = \sum_q \mathbb 1[D_q > 0]$, with ties when $|D_q| \le h = 0.01$, and $p_1 = 1 - F_{\text{Binom}}(S-1;\, n_0, 0.5)$.

**Permutation test** (randomisation, exchangeability under $H_0$). Each replica $j$ flips the sign of every $D_q$ with probability 0.5 and records the mean $\bar D^*_j$:

$$
p_1 = \frac{1}{T}\sum_j \mathbb 1[\bar D^*_j \ge \bar D], \qquad p_2 = \frac{1}{T}\sum_j \mathbb 1[|\bar D^*_j| \ge |\bar D|].
$$

**Bootstrap-shift test.** Each replica resamples $n$ differences with replacement, giving mean $\bar D^*_j$; the replicas are centred on their grand mean $\bar D^{**}$:

$$
p_1 = \frac{1}{T}\sum_j \mathbb 1[\bar D^*_j - \bar D^{**} \ge \bar D], \qquad p_2 = \frac{1}{T}\sum_j \mathbb 1[|\bar D^*_j - \bar D^{**}| \ge |\bar D|].
$$

Intuition: the null distribution is estimated from the sample itself, which is poor for small $n$; hence the bias towards small p-values, which shrinks as $n$ grows.

**Monte Carlo precision.** $T\hat p_1$ is binomial, so the standard error of $\hat p_1$ and the $T$ for a relative error $\varepsilon$ are

$$
\sqrt{\hat p_1(1-\hat p_1)/T}, \qquad T = \frac{1-p_1}{\varepsilon^2 p_1}.
$$

Intuition: a 1% relative error at $p_1 = 0.05$ needs 190,000 replicas. The paper uses $T = 10^6$ for both resampling tests: errors of 0.00014 at $p_2 = 0.01$ and 0.0003 at $p_2 = 0.05$. Earlier IR work used 1,000 (Wilbur, Sakai), 2,000, up to 5,000 and 100,000.

**Simulation.** A bivariate model per system pair: margins $F_B, F_E$ and a copula $c$ for their dependence on the same topic. Fitting: margins on $\{B_q\}, \{E_q\}$, pseudo-observations $U_q = F_B(B_q)$, $V_q = F_E(E_q)$, then $c$ on $(U_q, V_q)$. Simulating: draw $(U, V) \sim c$, return $(F_B^{-1}(U), F_E^{-1}(V))$. Model selection rewards fit over simplicity (log-likelihood rather than BIC).

- Type I: set $F_E \leftarrow F_B$, so $\mu_B = \mu_E$ by construction; every rejection is an error.
- Type II: transform $F_E$ so $\mu_E = \mu_B + \delta$ while keeping its support; every non-rejection is an error.
- Type III: with $\delta > 0$, count $\bar D < 0$ with $p_2 \le \alpha$, a correct rejection with the wrong direction (a Type S error).

## Implementation

- **Code:** [julian-urbano/sigir2019-statistical](https://github.com/julian-urbano/sigir2019-statistical), with the data; preprint arXiv 1905.11096.
- **Software:** R, `simIReff` 1.0 (6 margin families, 12 copula families plus rotations; mean tolerance $10^{-5}$); permutation and bootstrap in C++11, the permutation test with the Mersenne Twister.
- **Hardware:** Dutch national e-infrastructure (SURF); no further detail.
- **Budget:** about 250 million p-values for Type I and 250 million for Type II and III; $T = 10^6$ replicas per resampling test.

## Data

- TREC 5–8 Ad hoc runs: top 90% kept, 326 runs, about 14,000 pairs; AP, P@10 and RR.
- TREC 2010–13 Web runs: top 90% kept, 193 runs, about 5,000 pairs; nDCG@20 and ERR@20.
- Simulated topic sets of $n = 25, 50, 100$; no simulation beyond 100 topics.

## Experiments

- **Type I:** random same-collection pair, same margins, simulate $n$ topics, five tests, one- and two-tailed, $\alpha \in [0.001, 0.1]$; 1,667,000 trials per measure and $n$.
- **Type II (power):** baseline from the bottom 75% of runs, partner among the 10 runs closest to $\mu_B + \delta$, $\delta = 0.01, \dots, 0.1$; 167,000 trials per $\delta$; reported at $\alpha = 0.05$, plus power against $\alpha$ at $\delta = 0.01, 0.03$ with 50 topics.
- **Type III:** same data as Type II, wrong-sign rejections at $\alpha = 0.05$.

## Results

- At $n = 50$ and $\alpha = 0.05$, the t and permutation tests err at 0.05; bootstrap-shift at 0.059 two-tailed and 0.054 one-tailed. At $\alpha = 0.01$: 0.01 against 0.014.
- The t-test tracks the nominal rate almost exactly even at 25 topics; it is slightly conservative at low $\alpha$ with small samples for ERR@20 and RR.
- The permutation test approaches the nominal rate as $n$ grows and is nearly ideal for RR and P@10.
- Bootstrap-shift over-rejects but approaches the nominal rate as $n$ grows, as the sampling distribution is better estimated.
- Wilcoxon and sign over-reject, and get worse as $n$ grows; Wilcoxon does better on P@10, whose differences are nearly symmetric.
- Measure instability does not raise the t and permutation Type I rates, and the tests are not too conservative, contrary to discordance studies.
- Power rises with $n$ and $\delta$ and falls with variance; P@10 and RR differences have 2–4 times the standard deviation of the other measures.
- Bootstrap-shift is nearly always the most powerful, most clearly at small $n$; Wilcoxon, t and permutation follow closely; sign is weakest. At large $n$ all but the sign test have nearly equal power; one-tailed power is higher with the same pattern.
- Type III: t and permutation lowest, bootstrap between, Wilcoxon and sign worst. With more topics, Wilcoxon and sign get worse while bootstrap catches up with t and permutation; RR is worst and ERR@20 best.
- With AP, 50 topics and $\delta = 0.01$, the t-test Type III rate is 0.0069 at 9.47% power, so 7.3% of significant results could have the wrong sign. P@10 gives 0.0064 at 8.9% power, 7.2%.
- The paper states the Type III rate "can be as high as 2%" for P@10, RR or small topic sets; its plotted rates over all cases stay below 0.012, so the base of that 2% is unclear.

## Limitations

- Only 25, 50 and 100 topics; behaviour at thousands of queries is extrapolated from trends (ours).
- Only test p-values for $H_0$ on the mean; confidence-interval coverage, percentile or BCa bootstrap intervals are not studied (ours).
- Topics are simulated independently; clustered or dependent queries are not modelled (ours).
- One pair of systems at a time; multiple comparisons are not addressed (ours).
- Simulated systems are hypothetical systems that behave like TREC runs, not the runs themselves (authors).
- Other ways of handling zero differences in Wilcoxon are out of scope (authors).
- Only ad hoc and Web measures over TREC runs (ours).
- Type III rates over significant results are estimated roughly from two plots, not reported in full (authors).

## Relation to our project

The report (checkpoint 2, Methods) gives intervals by a paired bootstrap over queries, with 1,000 resamples in the BM25 proof of concept. It gives p-values by a paired permutation test, citing this paper.

- **Supports:** the paired permutation test for p-values. Its top recommendation for mean effectiveness such as S@10 and MRR is the t-test; the two behave almost identically (Section 1.2, p. 506; Section 5, p. 513).
- **Against bootstrap testing:** it proposes discontinuing the bootstrap-shift test, which is biased towards small p-values (Sections 1.2 and 4.1, pp. 506 and 510–511; Section 5, p. 513).
- **Partly for bootstrap:** the bias shrinks with sample size; "the only situation favorable to the bootstrap" is "(very) large test collections" (Section 5, p. 513).
- **Not studied:** bootstrap confidence intervals, interval coverage and cluster resampling. Cite it for the permutation test only; the checkpoint 1 plan's paired cluster bootstrap has no support here.
- **Scale:** we score 1,367 Polish and 22,600 English queries, 152 and 2,364 of them answerable; the paper never tests beyond 100 topics.
- [Ihemelandu and Ekstrand, 2023](https://doi.org/10.1145/3539618.3592004) fill that gap: at thousands of topics, bootstrap, randomisation and t-tests hold the expected Type I rate, while Wilcoxon and sign do not.
- **Resample count:** it uses $10^6$ replicas and lists 1,000 only as what Wilbur and Sakai used (Section 3.1, p. 508).
- By its binomial bound, 1,000 permutations give a p-value error of about 0.007 at $p = 0.05$ (14% relative); 10,000 give 0.0022 (4.4%) (ours).
- A 95% percentile interval from 1,000 bootstrap resamples rests on 25 values per tail (ours); justify the intervals with other sources.
- **Takeaway:** keep the paired permutation test (or t-test) over per-query differences, with at least 10,000 permutations for p-values near 0.05.
- The binary Success@k per query is discrete like P@10, where the t and permutation tests behaved well. The paper credits that to symmetric differences, which binary differences need not have (ours).

## Future work

- **Partly done:** how metric score distributions change Type I rates; [Urbano et al., 2021](https://doi.org/10.1145/3471158.3472242).
- **Partly done:** simulating rankings instead of scores to compare tests; [Parapar et al., 2021](https://doi.org/10.1145/3412841.3441945).
- **Partly done:** error rates of paired tests at thousands of queries; [Ihemelandu and Ekstrand, 2023](https://doi.org/10.1145/3539618.3592004).
- **Partly done:** Type I error and power under multiple comparisons across many systems; [Otero et al., 2025](https://doi.org/10.1007/978-3-031-88711-6_27) find Wilcoxon with Benjamini-Hochberg holds $\alpha$ at typical sample sizes.
- **Open:** error rates of paired tests with clustered or dependent queries (searched 2026-11).
- **Open:** coverage of bootstrap confidence intervals for IR metric differences under known nulls (searched 2026-11).
