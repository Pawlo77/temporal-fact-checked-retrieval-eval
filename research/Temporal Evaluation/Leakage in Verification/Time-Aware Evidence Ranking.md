---
title: "Time-Aware Evidence Ranking"
aliases: ["Time-aware evidence ranking for fact-checking"]
authors: ["Liesbeth Allein", "Isabelle Augenstein", "Marie-Francine Moens"]
year: 2021
venue: "Journal of Web Semantics 71, 100663"
arxiv: "2009.06402"
doi: "10.1016/j.websem.2021.100663"
url: "https://doi.org/10.1016/j.websem.2021.100663"
citekey: allein2021time
verified: 2026-11-11
theme: "[[Leakage in Verification]]"
tags: [type/paper, theme/verification-leakage, topic/temporal, topic/reranking, topic/english]
---
# Time-Aware Evidence Ranking

> [!info] TL;DR
> The paper trains the evidence-ranking module of a claim verification model against rankings derived only from evidence timestamps, through a listwise learning-to-rank loss. Four hypotheses define the target ranking: newest first, newest first among evidence up to the claim date, closest to the claim date, and closest to the evidence medoid date. On MultiFC, picking the best hypothesis per fact-checking domain raises Micro F1 by 7.44% (BiLSTM), 8.46% (RNN) and 3.63% (DistilBERT) over models with implicit ranking. Search-engine order as the target hurts every model.

## Motivation

- Claim veracity and meaning can change over time, so evidence relevance depends on when the claim and the evidence were published.
- Prior verification models weigh evidence equally, by search rank, by source popularity or by semantic similarity to the claim; none uses timestamps.
- Earlier temporal work in fact-checking studied temporal factuality via search-result frequency, adversarial date edits or pattern-based temporal fact extraction, not evidence ranking.
- MultiFC ([Augenstein et al., 2019](https://arxiv.org/abs/1909.03242)) ships claim dates and evidence snippets that often begin with a date, which makes timestamp-derived ranking targets possible.

## Method

Notation: claim $c_i$ with date $t(c_i)$, here $t_q$; evidence set $E_i = \{e_{i1},\dots,e_{iK}\}$, $K \le 10$, with dates $t(e_{ij})$; offset $\Delta t(e_{ij}) = t(e_{ij}) - t(c_i)$ in days, positive for evidence after the claim; target score $r(e_{ij})$, higher is more relevant.

**Base models.** Each model encodes the claim, each snippet and metadata into a joint vector $f_{ij}$, computes domain-masked label scores $l_{ij}$ and a ranking score $r(f_{ij})$, and predicts

$$
p_i = \text{softmax}\Big(\sum_j r(f_{ij})\, l_{ij}\Big) .
$$

For the BiLSTM (the MultiFC joint model), $f_{ij} = [h_{c_i}; h_{e_{ij}}; h_{c_i} - h_{e_{ij}}; h_{c_i} \circ h_{e_{ij}}; h_{m_i}]$. The RNN concatenates $[h_{c_i}; h_{e_{ij}}; h_{m_i}]$; DistilBERT uses the joint [CLS] vector.

Intuition: evidence the ranker scores high dominates the verdict, so constraining the ranker changes the prediction.

**ListMLE loss.**

$$
\mathcal{L} = -\sum_{i=1}^{N} \log P(R_i \mid E_i; r), \qquad P(R_i \mid E_i; r) = \prod_{u=1}^{K} \frac{\exp r(E_{R_{iu}})}{\sum_{v=u}^{K} \exp r(E_{R_{iv}})} .
$$

Snippets without a timestamp or outside the target ranking are masked. Cross-entropy updates all parameters except the ranker; ListMLE updates only the ranker.

**Four target rankings** (ties get equal scores):

| Method | Hypothesis | Constraint |
|--------|-----------|------------|
| Evidence-based date | newer evidence is more relevant | $\Delta t(e_j) \le \Delta t(e_k) \Rightarrow r(e_j) \le r(e_k)$ |
| Claim-based date | newer is better, but only evidence available at claim time counts | same, only for $\Delta t \le 0$; later evidence gets $r=0$ |
| Claim-centred distance | evidence near the claim date is more relevant | $\lvert\Delta t(e_j)\rvert \ge \lvert\Delta t(e_k)\rvert \Rightarrow r(e_j) \le r(e_k)$ |
| Evidence-centred distance | relevant evidence clusters in time | distance to the medoid of $\{\Delta t\}$ in the set, ascending |

Intuition: claim-based date ranking is a causal evidence restriction applied as a training target, not as a filter at test time.

**Time-aware evidence ranking.** For each domain, the method with the best development score is chosen and test results are averaged over domains.

## Implementation

- **Code:** not released.
- **Software:** Hugging Face DistilBertForSequenceClassification (distilbert-base-uncased); ListMLE from allRank; Python `datetime` for parsing.
- **BiLSTM:** 2 layers, hidden 128, skip connections, 300-d word embeddings; CNN metadata encoder (32 channels, kernel 32); label embeddings 16-d; batch 32, 150 epochs; RMSProp 0.0002 for classification, Adam 0.001 for ranking.
- **RNN:** 2-layer unidirectional, hidden 128, dropout 0.1; one ranking layer; same optimisers and epochs.
- **DistilBERT:** batch 32, 10 epochs; AdamW 0.0005 for classification, Adam 0.01 for ranking.
- **Training:** pre-training on all 26 domains with alternating batches capped by the smallest domain, then per-domain fine-tuning from the best development checkpoint. Applying the ranking constraint in both phases worked best.

## Data

- MultiFC: 34,924 real claims from 26 fact-checking websites, each with speaker, tags, categories and up to ten Google Search snippets retrieved with the verbatim claim as query.
- Evidence dates: the text before the first ellipsis is parsed as a date; unparseable ones are dropped. A manual check of 150 parsed timestamps found no errors. The share of dated snippets varies widely by domain.
- Split: label-stratified random split into 27,940 train, 3,493 development and 3,491 test claims; labels per domain range from 2 to 40.

## Experiments

- **Main comparison:** three architectures, each with implicit ranking (base), random evidence, search-engine order as target, the four temporal targets and per-domain best; Micro and Macro F1 averaged over domains.
- **Training phase:** constraint in pre-training only, fine-tuning only, or both.
- **Ranking change:** Spearman correlation between base and time-aware rankings.
- **Domain analysis:** whether the share of dated snippets, topic time-sensitivity or evidence date dispersion explains which domains gain.

## Results

- Base Micro/Macro F1: BiLSTM .5521/.3185, RNN .5053/.2691, DistilBERT .5558/.2909.
- Per-domain best temporal target: BiLSTM .6265/.3673 (+7.44%/+4.88%), RNN .5899/.3453 (+8.46%/+7.62%), DistilBERT .5921/.3135 (+3.63%/+2.26%).
- Search-engine order as target lowers Micro F1 for all models (−0.53%, −2.71%, −7.65%).
- Evidence-based date ranking helps BiLSTM (+2.73%) and RNN (+3.06%) more than claim-based date ranking (+1.47%, +2.18%). For DistilBERT both date targets hurt (−1.34%, −7.67%); only evidence-centred distance helps (+2.01%).
- Constraint in both phases beats either phase alone, for example BiLSTM .6265 vs .5998 and .6072 Micro F1.
- Spearman correlation with base rankings is .17 to .24 (BiLSTM), .54 to .61 (RNN) and −.35 to −.02 (DistilBERT).
- Time-sensitive domains (politics, economy, climate, entertainment) gain more than mixed domains; the dated-snippet share does not explain the gains, and Kruskal-Wallis and Mann-Whitney tests reject evidence date dispersion as the cause.

## Limitations

- Snippets come from a single Google query per claim and are often uninformative, so ranking cannot help (authors).
- One target method per domain; claim-specific temporal semantics are not modelled (authors).
- The best method is selected per domain on development data, so the headline "time-aware" row is an oracle-style selection over five runs (ours).
- Evidence-based date ranking, which prefers post-claim evidence, beats the causal claim-based variant; the gain may partly reward hindsight evidence, including fact-checks themselves (ours; [[Missing Counter-Evidence]]).
- Random label-stratified split, no temporal split; English only; no significance tests on the F1 gains (ours).

## Relation to our project

- **Novelty claim not contradicted.** The paper is claim verification, not PFCR: it ranks a claim's own ten search snippets to predict a label, with no fact-check archive and no post queries.
- Its claim-based date ranking excludes evidence after the claim, but only as a training target; post-claim snippets still reach the model at test time.
- It does not restrict any retrieval index per query, and its split is random.
- Its finding that newest-first targets beat the causal variant is a warning that unrestricted evaluation favours post-claim evidence, the inflation a causal index removes ([[Leakage in Verification]]).
- Recency as a ranking prior is a cheap baseline we could test inside the causal pool, where it cannot exploit future fact-checks ([[2026-10-27-temporal-retrieval-eval|Project plan]]).

## Future work

- **Partly done:** time-awareness beyond ranking, with shared timelines of claim and evidence from dates and time expressions fed to the classifier on MultiFC ([Allein et al., 2023](https://arxiv.org/abs/2302.12569)).
- **Partly done:** time constraints at the document retrieval stage, through evidence search limited to pre-claim documents ([[AVeriTeC]]).
- **Open:** choosing a temporal ranking method per claim from its temporal semantics, as the authors propose (searched 2026-11).
- **Open:** space-aware evidence ranking by analogy with temporal ranking (searched 2026-11).
