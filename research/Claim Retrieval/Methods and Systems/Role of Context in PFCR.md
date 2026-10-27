---
title: "Role of Context in PFCR"
aliases: ["The Role of Context in Detecting Previously Fact-Checked Claims"]
authors: ["Shaden Shaar", "Firoj Alam", "Giovanni Da San Martino", "Preslav Nakov"]
year: 2022
venue: "Findings of the Association for Computational Linguistics: NAACL 2022, pages 1619-1631"
arxiv: "2104.07423"
doi: "10.18653/v1/2022.findings-naacl.122"
url: "https://aclanthology.org/2022.findings-naacl.122/"
citekey: shaar2022role
verified: 2026-10-27
theme: "[[Methods and Systems]]"
tags: [type/paper, theme/methods, topic/english, topic/temporal, topic/evaluation, topic/reranking]
---
# Role of Context in PFCR

> [!info] TL;DR
> On PolitiFact debate claims, the paper adds context from the surrounding transcript and from the fact-check article to a learning-to-rank PFCR model. Source-side context (neighbouring sentences and co-reference) helps most, raising MAP from 0.429 to 0.532. It also introduces a chronological debate-level split, under which the earlier state-of-the-art model drops from MAP 0.602 (random sentence split) to 0.429.

## Motivation

- [[That is a Known Lie]] matched each debate sentence on its own, but spoken claims often span sentences or rely on pronouns and earlier turns.
- Its random sentence-level split could put parts of one claim, or repeated claims on one topic, in both training and test.
- Multi-hop reasoning over evidence sentences helped FEVER-style verification ([Zhao et al., 2020](https://openreview.net/forum?id=r1eIiCNYwS), Transformer-XH), but had not been tried for PFCR.

## Method

We write a debate sentence as post $q$ and a PolitiFact verified claim with its article as fact-check $f$; the paper calls them InputClaim and VerClaim.

**Pair types.** Three fact-checking experts label each pair as clean ($q$ self-contained and directly verified), clean-hard (self-contained, indirectly verified), part-of ($q$ needs neighbouring sentences to form a claim) or context-dep ($q$ needs co-reference).

**Baseline.** BM25 over article text retrieves the top 100; a rankSVM reranks with 9 similarity scores (BM25 on claim, title, text and their union; sentence-BERT on claim, title and top-4 sentences) and their reciprocal ranks, an 18-dimensional vector.

**Local context.** Feature vectors of the $k$ previous and $l$ following transcript sentences are concatenated to the vector of $q$: $FC(k, l) = S_{i-k} \oplus \dots \oplus S_i \oplus \dots \oplus S_{i+l}$, with $FC(3,1)$ chosen by cross-validation (90 features).

Intuition: a pronoun-heavy sentence borrows the matching signal of the sentences around it.

**Co-reference.** NeuralCoref on the whole transcript (source side) and e2e-coref on article text concatenated with the claim (target side).

**Global context.** Transformer-XH, pretrained on FEVER, reads a graph of claim, title and top-3 article sentences for each of the top-100 candidates and adds three support, refute and not-enough-information scores.

**Splits.** Debate-Level Chrono trains on the first 50 events (2012-2018) and tests on the last 20 (2019). Semi-Chrono splits each year's transcripts 80/20. Debate-Level Random puts 80% of debates in training. Sentence-Level Random is the 2020 setup.

## Key numbers

- Reranker MAP by split: Debate-Level Chrono 0.429, Semi-Chrono 0.539, Debate-Level Random 0.590, Sentence-Level Random 0.602.
- Chronological test with context: source co-reference plus $FC(3,1)$ reaches MAP 0.532 vs baseline 0.429.
- Part-of pairs gain most from source context: MAP 0.161 to 0.385.
- Transformer-XH alone raises clean-hard pairs from 0.365 to 0.441.

## Experiments

- **Split comparison:** the same reranker under four splits; scores fall as the split becomes more realistic. The authors attribute the chronological drop to politicians discussing different topics across years, and the random-debate gain to politicians repeating themselves in consecutive events.
- **Source side:** local context adds 8 MAP points, source co-reference 5, both together 10.
- **Target side:** co-reference and Transformer-XH help less; combining them is worse than Transformer-XH alone.
- **All components:** best for clean pairs (0.749) but overall 0.517, below source-side context alone.
- **Hyper-parameters:** tuned on debates from 2018 after training on 2012-2017, so model selection also respects time.

## Data

- PolitiFact part of That is a Known Lie, cleaned of a few false matches: 695 pairs (291 clean, 210 clean-hard, 68 part-of, 126 context-dep); pool of 16,636 verified claims.
- Chronological split: 554 training and 141 test pairs.

> [!failure] Limitations
> - Only the training split respects time; the pool is the same 16,636 claims for every query, so fact-checks published after a 2019 debate remain retrievable.
> - The chronological drop mixes topic drift, fewer similar training debates and any change in answerability; the paper does not separate them.
> - Pair-type agreement is moderate (Fleiss kappa 0.5) and the test set has 141 pairs, with no significance tests.
> - English US political debates only; the context methods do not transfer directly to single social media posts.

## Relation to our project

- It is the closest precedent for chronological PFCR evaluation, and our novelty claims cite it: chronological training splits exist; a per-query causal index $P(q)$ does not ([[Proposed Task]], [[Research summary]]).
- Its random-to-chronological MAP drop of 0.17 is the effect size our training-regime comparison extends to multilingual social media posts ([[Enhanced topic research]]).
- We adopt its practice of tuning on the latest training period, so hyper-parameters never see the test period.
- Its uncontrolled pool is what our gap decomposition separates: index leakage, answerability and pool size, alongside training leakage.

## Future work

- **Open:** other multi-hop reasoning frameworks for context modelling in PFCR (searched 2026-10).
- **Partly done:** other conversation types and languages; multilingual social media PFCR exists ([[MultiClaim]]), but without conversational context modelling.
- **Open:** pairing the chronological split with a date-restricted pool and an answerability filter (searched 2026-10).
