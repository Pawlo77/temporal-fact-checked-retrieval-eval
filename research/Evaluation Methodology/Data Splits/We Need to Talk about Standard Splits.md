---
title: "We Need to Talk about Standard Splits"
aliases: ["We Need to Talk about Standard Splits"]
authors: ["Kyle Gorman", "Steven Bedrick"]
year: 2019
venue: "Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics (ACL 2019), pages 2786-2791"
doi: "10.18653/v1/P19-1267"
url: "https://aclanthology.org/P19-1267/"
citekey: gorman2019we
verified: 2026-10-27
theme: "[[Data Splits]]"
tags: [type/paper, theme/splits, topic/evaluation, topic/significance, topic/english]
---
# We Need to Talk about Standard Splits

> [!info] TL;DR
> Six English part-of-speech taggers that each claimed state of the art on the fixed Wall Street Journal split are re-run on that split and on twenty random splits. The published ranking replicates on the standard split, but one claimed improvement (Stanford over LAPOS) is not significant on almost any random split and is reversed on some. The authors recommend Bonferroni-corrected significance testing over multiple random splits for system comparison.

## Motivation

- NLP ranks systems by a single score on one held-out "standard split" and rarely tests whether a difference could arise by chance; a survey of ACL 2017 and TACL 2017 found most papers lacked appropriate tests ([Dror et al., 2018](https://aclanthology.org/P18-1128/)).
- A fixed split invites the whole field to overfit to its quirks, and publication bias rewards only gains on that split.
- The risk is largest on saturated tasks near ceiling, where true differences are small.

## Method

The paper is about classification, not retrieval, so its own notation is kept: data $G$ split into $G_{train}$, $G_{dev}$, $G_{test}$; systems $S_1, S_2$; metric $M$.

**Standard-split comparison.** $S_1$ is preferred if $M(G_{test}, S_1) > M(G_{test}, S_2)$. The paper treats the observed difference $\hat\delta$ as an estimate of a latent true difference $\delta$.

**McNemar's test.** Let $n_{1>2}$ count test items $S_1$ gets right and $S_2$ gets wrong, and $n_{2>1}$ the reverse. Under $\delta = 0$, $n_{1>2} \sim \mathrm{Bin}(n_{1>2}+n_{2>1}, 0.5)$; the paper uses the two-sided mid-p variant and 95% Wilson confidence intervals for accuracy.

Intuition: if two systems are equally good, their disagreements should split evenly between them.

**Replication.** Train and tune each tagger on the standard Collins split (sections 00-18 train, 19-21 dev, 22-24 test, about 80/10/10).

**Reproduction.** Repeat on twenty random 80/10/10 splits at sentence level and count the splits where the second system is significantly better after Bonferroni correction for the family of trials.

## Key numbers

- Replicated token accuracy on the Penn Treebank standard split ranges from 0.9646 (TnT) to 0.9774 (Flair). TnT and LAPOS replicate exactly; the other four are close to their published numbers.
- Stanford beats LAPOS significantly in 1 of 20 random Penn Treebank splits and 0 of 20 OntoNotes splits. It is worse than LAPOS in 2 and 14 of those splits respectively.
- Two decades of tagger research reduced token error by 1.28 points absolute, while the best tagger stays 1.16 points below an oracle ensemble of the six.

## Experiments

- **Replication (standard split):** six taggers on Penn Treebank and an OntoNotes re-annotation; same ranking under token, out-of-vocabulary and sentence accuracy. All Penn Treebank pairs are significant; on OntoNotes, LAPOS vs Stanford is not ($p = .1366$).
- **Reproduction (random splits):** most adjacent pairs stay stable across twenty random splits, but Collins vs LAPOS holds in only 7 of 20 OntoNotes splits and Stanford vs LAPOS almost never holds.
- **Error analysis:** per-sentence Krippendorff's $\alpha$ across taggers; most disagreement is on headline-like capitalised sentences and local syntactic ambiguity.
- **Split effect:** accuracy is slightly higher on random splits than on the standard split, which the authors attribute to sentence-level randomisation spreading rare words across train and test.

## Data

- Penn Treebank-3, Wall Street Journal portion: 38,219 / 5,527 / 5,462 sentences (train/dev/test).
- OntoNotes 5 WSJ subset, re-annotated by one annotator: 28,905 / 4,051 / 4,059 sentences.

> [!failure] Limitations
> - One task and one language (English POS tagging); three of nine candidate taggers could not be run.
> - Random sentence-level splits mix near-duplicate text across train and test, which inflates scores; the paper itself observes higher accuracy on random splits.
> - Time and deployment are not considered: random splits assume test data are i.i.d. with training data, which [[We Need to Talk about Random Splits]] later shows is optimistic.
> - Repeated training of the neural tagger needed substantial grid compute.

## Relation to our project

- We take the statistical practice: paired significance tests between systems, multiple-comparison correction, and checking whether rankings survive a change of protocol. In our setting the protocol change is random vs causal index, not standard vs random split ([[2026-10-27-temporal-retrieval-eval|Project plan]], [[Topic research]]).
- We avoid its recommendation itself. For PFCR, a random split of posts lets near-duplicate claims from the future sit in training and in the pool, the leakage our causal protocol removes. We cite it as the position that [[We Need to Talk about Random Splits]] rebuts, not as support for time-based evaluation.
- Its observation that random splits score higher because rare items spread across splits mirrors our expectation that random PFCR protocols overstate Success@k ([[Data Splits]]).

## Future work

- **Done:** apply random-split testing beyond English tagging and replace point estimates with Bayesian comparison over k-fold cross-validation on several datasets; [Szymański and Gorman, 2020](https://aclanthology.org/2020.emnlp-main.172/).
- **Done:** test whether random splits estimate performance on new samples; they do not, and biased or adversarial splits do better: [[We Need to Talk about Random Splits]].
- **Open:** a significance protocol for comparing systems under time-respecting splits with a changing retrieval pool, as PFCR needs (searched 2026-10).
