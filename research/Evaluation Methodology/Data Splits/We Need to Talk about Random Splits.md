---
title: "We Need to Talk about Random Splits"
aliases: ["We Need To Talk About Random Splits"]
authors: ["Anders Søgaard", "Sebastian Ebert", "Jasmijn Bastings", "Katja Filippova"]
year: 2021
venue: "Proceedings of the 16th Conference of the European Chapter of the Association for Computational Linguistics: Main Volume (EACL 2021), pages 1823-1832"
arxiv: "2005.00636"
doi: "10.18653/v1/2021.eacl-main.156"
url: "https://aclanthology.org/2021.eacl-main.156/"
citekey: sogaard2021we
verified: 2026-10-27
theme: "[[Data Splits]]"
tags: [type/paper, theme/splits, topic/evaluation, topic/temporal, topic/english]
---
# We Need to Talk about Random Splits

> [!info] TL;DR
> Across seven NLP tasks, random splits (and standard splits) consistently overestimate performance on new in-domain samples, often by more than 20 points of error reduction. Biased splits by sentence length and adversarial splits that maximise train-test distance come closer but are still optimistic in most tasks. The authors recommend multiple independent test samples, or failing that, multiple biased splits instead of multiple random ones.

## Motivation

- [[We Need to Talk about Standard Splits]] argued for random over standard splits; that relies on test data being an i.i.d. sample of the data users care about.
- The quantity that matters is the system difference on data users will send, not on the annotated corpus.
- Domain adaptation simulates drift with biased sampling under the covariate shift assumption; whether such splits predict error on genuinely new data had not been tested across tasks.
- Temporal and neighbour-based splits had been proposed before ([Karimi et al., 2015](https://doi.org/10.1162/coli_a_00230) is cited for them), but not compared against fresh samples.

## Method

The paper's setting is not retrieval; it compares how well five evaluation splits predict performance on a later or separate sample of the same domain.

**Split types.** Standard (the dataset's own split, where one exists); random (resampled 3-10 times, cross-validation). Heuristic: sentences above a length threshold, about 10% of data, go to test. Also adversarial, and new samples: separately collected in-domain data, for time-stamped datasets the most recent period.

**Adversarial split.** Build a ball tree over pairwise Wasserstein distances, pick a random centroid, and put its $k$ nearest neighbours in test; the rest is training. Exact worst-case selection is NP-hard, so this is an approximation averaged over five runs.

**Comparable score.** Results come from different samples, so each is an error reduction over a baseline, $r = (p_s - p_b)/(1 - p_b)$. Here $p_s$ is the system and $p_b$ a random (for headlines, identity) baseline.

Intuition: a split is a good evaluation if its $r$ is close to $r$ on new samples; the mean squared error to new samples ranks the split types.

## Key numbers

- Mean squared error to new-sample results: standard 0.179, random 0.030, heuristic 0.015, adversarial 0.011, so adversarial splits estimate new-sample error best.
- BERT on the bigram-shift probing task: error reduction 0.808 on random splits vs 0.450 on new Gutenberg samples.
- POS tagging (NCRF++): 0.962 random vs 0.927 on the Xinhua new sample; removing the CRF layer lowers the random-split score (0.952) but raises the new-sample score (0.930), so the ranking flips.
- Headline generation trained on 1994-1998 instead of 1999-2003 (same size) drops ROUGE-2 on 2004 data from 0.208 to 0.161, losing about half the gain over copying the input.

## Experiments

- **Seven tasks, five split types:** POS tagging, two SentEval probing tasks, translation quality estimation, headline generation, emoji prediction, news classification; random and standard splits overestimate on every task. Heuristic splits are more optimistic than new samples in 5 of 7 tasks, adversarial splits in 4 of 7.
- **Alternative heuristics (appendix):** splits by rare words lower scores, but less than the length threshold; bootstrap resampling gives slightly lower error reduction than cross-validation.
- **Temporal drift, headlines (appendix):** three equal-size models trained on a random half, the earlier half or the later half of 1994-2003, tested on 2004. The earlier-half model is clearly worse, partly from vocabulary change such as "US" replacing "U.S.".
- **Temporal drift, emojis (appendix):** training on single days before a fixed test day; the correlation between temporal gap and performance is significant ($p < 0.05$).

## Data

- Penn Treebank WSJ with OntoNotes Xinhua as new sample (POS tagging).
- SentEval word-content and bigram-shift probing on Toronto BookCorpus, new samples from the 2018 Gutenberg corpus.
- WMT 2014 Spanish-English quality estimation, with its unofficial second test set as new sample.
- Gigaword headlines 1998-2003 for training, 20,000 pairs each from the two halves of 2004 for validation and test.
- Sentiment140 emoji tweets; 67,980 tweets from June 16 as new sample.
- UCI news headlines, five genres; last year as new sample, 100,000 earlier headlines sampled for training.

> [!failure] Limitations
> - New samples are defined differently per task (other newspaper, later day, later year, other book corpus), so "in-domain" is a judgement call.
> - Time-based splits appear only as one way to build new samples and in an appendix; they are not evaluated as a split strategy of their own.
> - Models are small task-specific ones (LASER plus MLP, LSTMs, NCRF++, BERT probes), not modern pretrained retrievers.
> - No retrieval task, so pool composition and answerability, which change scores in PFCR, are outside its scope.

## Relation to our project

- We take its central claim: random splits overstate deployment performance, and a later independent sample is the better estimate. Our causal protocol evaluates each post $q$ against $P(q)$, the fact-checks published before $t_q$, which is that later-sample principle applied to the retrieval pool ([[Proposed Task]], [[Enhanced topic research]]).
- The ranking flip under a new sample (POS tagger with and without CRF) is what we test for retrieval families. Does system order under Success@10 and MRR survive the switch to a causal index ([[Data Splits]])?
- Its headline-drift appendix motivates our chronological training regime for fine-tuned retrievers, together with [[Mind the Gap]] and [[Role of Context in PFCR]].
- We avoid citing it as recommending time-based splits: its stated recommendation is new samples, else biased or adversarial splits.

## Future work

- **Done:** more benchmarks with multiple independent test sets, and adoption of chronological splits where data are dated; [Mu et al., 2023](https://aclanthology.org/2023.findings-eacl.55/) ([[Chronological Splits Rumor Detection]]) show random splits overestimate rumour detection.
- **Partly done:** the problem of tuning on the test set under any split; [van der Goot, 2021](https://aclanthology.org/2021.emnlp-main.368/) proposes tune-and-test protocols but keeps the split question open.
- **Open:** adversarial or biased splits for retrieval with a dated pool, compared against a later sample of queries (searched 2026-10).
