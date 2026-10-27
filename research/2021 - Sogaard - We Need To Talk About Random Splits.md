# 2021 - Sogaard - We Need To Talk About Random Splits

## Citation

- Authors: Anders Søgaard, Sebastian Ebert, Jasmijn Bastings, Katja Filippova
- Title: We Need To Talk About Random Splits
- Venue: Proceedings of EACL 2021 (Main Volume), Online, pages 1823-1832, DOI 10.18653/v1/2021.eacl-main.156
- Year: 2021
- URL: https://aclanthology.org/2021.eacl-main.156/
- Verified on: 2026-10-27 (Anthology page and PDF read)

## What it does

- Responds to Gorman and Bedrick (2019): random splits, like standard splits, give overly optimistic performance estimates.
- Compares standard, random, heuristic (sentence-length threshold), adversarial (approximate Wasserstein maximisation) splits and new samples across seven NLP tasks; some new samples are later time slices (e.g. headlines one year later, tweets the next day).
- Finds even worst-case splits often under-estimate error on new in-domain samples, invalidating the covariate-shift assumption.
- Recommends multiple independent test sets (new samples); if infeasible, multiple biased splits rather than multiple random splits.
- Appendix A.5 documents temporal drift: shifting headline training data five years into the past causes a large drop.

## Key numbers

- Table 2: PROBING-BSHIFT BERT error reduction 0.808 (random) vs 0.450 (new samples); POS tagging 0.962 (random) vs 0.927 (new sample).
- Section 4: absolute differences between random-split and new-sample error reductions are often above 20%.

## Relation to our project

- Supports the claim that random evaluation is optimistic, and that a later, independent sample (our causal/rolling-origin queries) is the better estimator of deployment performance.
- Does NOT cover: retrieval, index composition, answerability; its recommended biased splits are length/adversarial, not explicitly time-based.

## Verification

- CORRECTED (partial). Note says "(random splits overestimate; prefer biased or time-based splits)". "Random splits overestimate" is right. The paper's stated recommendation is multiple independent new samples, else biased (heuristic/adversarial) splits; it does not name time-based splits as its recommendation (it cites Karimi et al. 2015 for temporal splits and studies temporal drift only in an appendix). Fix: "prefer new independent samples, else biased or adversarial splits; temporal drift shown in appendix".
