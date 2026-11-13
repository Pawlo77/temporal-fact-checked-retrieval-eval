---
title: "Fenced Case Law Retrieval"
aliases: ["Fenced Citation-Context Retrieval for Case Law: Temporal Leakage and Degree Control Across Two Jurisdictions"]
authors: ["Yao Liu", "Tien-Ping Tan", "Zhilan Liu"]
year: 2026
venue: "arXiv preprint (v3)"
arxiv: "2607.17142"
url: "https://arxiv.org/abs/2607.17142"
citekey: liu2026fenced
verified: 2026-11-11
theme: "[[Chronological Evaluation]]"
tags: [type/paper, theme/chronological, topic/leakage, topic/temporal, topic/bm25, topic/evaluation, topic/english]
---
# Fenced Case Law Retrieval

> [!info] TL;DR
> In prior case retrieval, the text later cases use when citing a candidate (incoming citation context) is a strong signal, but it is usually used without a date limit. The paper adds this signal to BM25 with a temporal fence that admits only citing cases dated before the query, and decomposes what an unfenced evaluation over-credits. On ECtHR-PCR, 14.9% of the unfenced gain over BM25 comes from citations on or after the query date. Even fenced, the channel adds +16.1 R@1000 on CLERC and +8.68 over a BM25 plus citation-degree control on ECtHR-PCR, with no learned parameters.

## Motivation

- Citation anchor text improves legal precedent retrieval ([Patil et al., 2024](https://doi.org/10.3233/FAIA241241)), but its contexts are collected regardless of date, so a retriever is credited with citations a deployed system could not have seen.
- IL-PCR states that it puts no temporal constraint on scraped documents; COLIEE suppresses citations corpus-wide.
- ECtHR-PCR ([Santosh et al., 2024](https://arxiv.org/abs/2404.00596)) already restricts each query's candidate pool to cases dated before it and splits chronologically, but its baselines ignore the citation network.
- When relevance labels are citations, raw citation count predicts relevance, so a citation-context gain may be popularity, not content.
- Neither the size of the temporal over-credit nor its separation from popularity had been measured for legal case retrieval.

## Method

Notation: query case $q$ with date $t_q$; candidate case $d$; citing case $c$ with date $t_c$; window $w = (d, c, i)$ is the $i$-th passage where $c$ cites $d$; fence threshold $T$.

**Fenced anchor channel.**

$$
W_T(d) = \{(d,c,i) : t_c < T\}, \qquad s_{\text{anc}}(q,d) = \sum_{w \in W_T(d)} \omega(w)\,\text{BM25}(q,w),
$$

$$
s(q,d) = \frac{1}{\kappa + r_{\text{body}}(d)} + \frac{1}{\kappa + r_{\text{anc}}(d)} .
$$

$T$ is the query date (per-query fence) or the split start (split-static fence). $\omega$ is 1 on ECtHR-PCR and recency-decayed on CLERC; $r$ are within-channel ranks and $\kappa$ the RRF constant.

Intuition: a candidate is scored by its own text and by how earlier cases described it, never by how later cases did.

**Temporal-admission decomposition (ECtHR-PCR, day dates).** Four arms differ only in which citers are admitted: $a$ split-static fence (deployed), $a'$ split-static on the full-artifact index, $b$ per-query fence $t_c < t_q$, $c$ unrestricted. Then

$$
c - a = \underbrace{(c-b)}_{\text{non-prior-date premium}} + \underbrace{(b-a')}_{\text{admission cost}} + \underbrace{(a'-a)}_{\text{index effect}} .
$$

Only $c-b$ is leakage; $b-a'$ is legitimate pre-query evidence that a split-level fence excludes.

**Phantom fraction.**

$$
\phi = \frac{c-b}{c-\text{body}} ,
$$

with numerator and denominator resampled jointly. Intuition: the share of the whole unfenced citation-context gain over BM25 that comes from citers dated on or after the query.

**Dose-response (CLERC, year dates).** Arms admit citers with year $< Y(q) + k$ for $k \in \{0,1,2,5,10,\infty\}$ under frozen time-blind scoring; premium$(k) = \text{R@1000}(k) - \text{R@1000}(0)$. $k=1$ already admits same-year citers, some of them legitimate.

**Controls.** On ECtHR-PCR the channel must beat degree-only, BM25 plus degree (primary), window-count-only and BM25 plus window-count. A score-permutation placebo shuffles window scores among candidates matched on fenced degree and window count. On CLERC a family and time-matched placebo reattaches each context to a wrong target, and a degree control gets its own 51-configuration dev grid.

## Implementation

- **Code:** supplied as supplementary material, public release promised.
- **Software:** Anserini/Lucene disk-based BM25; RRF fusion; no GPU at index or query time.
- **CLERC:** BM25 $k_1=1.2$, $b=0.75$ (dev); about 300-word windows from CAP citation metadata in 179 per-year indexes, 16.57M anchor edges; per-query year fence; same-source skip and citation-family closure; RRF $\kappa=60$.
- **ECtHR-PCR:** BM25 $k_1=2.0$, $b=0.9$ from a pre-registered 25-point grid; ±250-word windows around application-number mentions in the citer's law section; split-static fence (test citers before 2018-01-01) enforced by hash-identical rebuilds from a corpus with test citations blanked; sum aggregation; RRF $\kappa=30$.
- **Statistics:** paired cluster bootstrap, $B = 10{,}000$, clusters by application root and exact-duplicate facts; sup-$t$ simultaneous bands for the dose-response.

## Data

- CLERC: 1.84M US federal opinions; queries are citing passages with the central citation removed; 2,000 dev and 2,851 official test queries. A label-free source mapping covers 2,058 of 2,850 eligible test queries; unmapped queries fall back to BM25.
- ECtHR-PCR: 15,729 English ECtHR judgments (1960–2022) with per-case ISO dates; facts-only queries; each query's candidate pool holds only cases dated before it. Validation 2015–2017 (2,186 queries), test 2018–2022 (3,231 queries, 38,759 gold pairs); macro-averaged recall.
- COLIEE 2026 Task 1: probed only; suppressed citation fragments outnumber surviving citations 314:1 on test, so the method cannot apply.

## Experiments

- **CLERC dev placebo:** the matched placebo falls below BM25 while real contexts hold, so the gain is target-specific content.
- **CLERC dev dose-response:** relaxing the year fence raises the over-credit monotonically in aggregate point estimates.
- **CLERC test:** audited post-exposure replication of the fenced policy against BM25, zero-shot bge-large-en-v1.5 and a dev-tuned degree control.
- **ECtHR-PCR test:** single-shot run after pre-registered byte-equality gates, against four popularity controls and published trained systems.
- **ECtHR-PCR validation decomposition:** the four admission arms at retrieval caps of 5,000 and 20,000.
- **Audits:** 20,921 contributing windows re-verified for temporal, self and family violations; 100-window manual precision check.

## Results

- CLERC test: policy R@1000 70.21 vs BM25 54.11, +16.11 (95% CI +14.28 to +17.95); +22.30 on the 2,058 mapped queries. The dev-optimal degree-fusion weight is zero, so the degree control equals BM25.
- CLERC zero-shot dense (bge-large-en-v1.5) reaches 0.5227 and a BM25 plus dense hybrid 0.5965, against fenced 0.7726 on the earlier 2,493-query alignment.
- CLERC dev: fenced 88.35 vs BM25 84.35; unfenced reaches 93.30, a non-prior-year premium of +4.95 (+2.95 under decay scoring); the clearly-later-year part ($k=\infty$ minus $k=1$) is +3.55.
- ECtHR-PCR test macro R@1000: fenced 79.56, BM25 plus window count 71.15, BM25 plus degree 70.89, BM25 62.31, degree only 39.19. The primary gain is +8.68 (cluster LB95 +7.62) and +15.45 at R@100.
- The published trained LeCoPCR-HT reaches R@1000 79.39 and MAP 13.68 against fenced 79.56 and 15.82, an unpaired comparison.
- ECtHR-PCR validation at cap 5,000: fenced 82.47, unrestricted 87.44, a naive effect of +4.97 = +2.70 premium + 3.29 admission cost − 1.02 index effect. The premium is +2.49 at cap 20,000.
- Phantom fraction 14.9% (CI 12.9% to 17.1%) of an 18.06-point unfenced gain over BM25.
- The ECtHR-PCR placebo keeps about 96% of the gain, which bounds score magnitude only. Audits find zero fence violations and 98 of 100 windows are true citation contexts.

## Limitations

- The anchor-text idea is borrowed from PAT; the contribution is the fenced measurement and controls (authors).
- The CLERC test set was first read through a label-assisted alignment, so the CLERC result is a post-exposure estimate (authors).
- Decomposition arms saturate the retrieval cap; only $c-b$ is stable across caps (authors).
- CLERC year dates make its premium include legitimate same-year citers (authors).
- The split-static fence cuts ECtHR-PCR pair coverage from 94.9% to 80.0%; a per-query fence would recover +2.28 (authors).
- Relevance labels are judicial citations, not adjudicated relevance (authors).
- Leakage numbers are for the authors' own unfenced variants, not measurements of prior systems (authors).
- The fence applies to evidence about candidates; the ECtHR-PCR candidate pool was already causal, so the paper does not measure what a non-causal pool costs (ours).

## Relation to our project

- **Novelty claim not contradicted, but narrowed.** Per-query pre-query candidate pools already exist in legal case retrieval: ECtHR-PCR restricts each query to cases dated before it, and this paper fences citation evidence per query. Neither is PFCR.
- So "first causal index in retrieval" is not claimable; our claim must stay "first in PFCR" ([[Chronological Evaluation]]).
- It does not match posts to fact-checks, and it does not compare a causal against a full candidate pool; it fences side evidence attached to candidates.
- Its premium versus admission-cost split separates leakage from legitimate pre-query evidence a coarse fence drops, which matches our per-query pool versus split-level cutoff choice ([[2026-10-27-temporal-retrieval-eval|Project plan]]).
- Its degree control is a model for a popularity control when gold fact-checks are popular ([[Language and Retrieval Bias]]).
- Its hash-identical rebuild with test data blanked is a cheap leak test we can reuse for BM25 statistics computed on the causal pool ([[TREC 2011 Microblog]]).

## Future work

- **Open:** a byte-verifiable per-query fence, which the authors leave as engineering work (searched 2026-11).
- **Open:** an exposure-matched control to explain why each year shell adds over-credit (searched 2026-11).
- **Open:** a fresh blind CLERC test evaluation on held-out queries (searched 2026-11).
