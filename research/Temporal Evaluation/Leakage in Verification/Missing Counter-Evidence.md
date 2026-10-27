---
title: "Missing Counter-Evidence"
aliases: ["Missing Counter-Evidence Renders NLP Fact-Checking Unrealistic for Misinformation"]
authors: ["Max Glockner", "Yufang Hou", "Iryna Gurevych"]
year: 2022
venue: "Proceedings of the 2022 Conference on Empirical Methods in Natural Language Processing (EMNLP 2022), pages 5916-5936"
arxiv: "2210.13865"
doi: "10.18653/v1/2022.emnlp-main.397"
url: "https://aclanthology.org/2022.emnlp-main.397/"
citekey: glockner2022missing
verified: 2026-10-27
theme: "[[Leakage in Verification]]"
tags: [type/paper, theme/verification-leakage, topic/leakage, topic/temporal, topic/evaluation, topic/english]
---
# Missing Counter-Evidence

> [!info] TL;DR
> Evidence-based fact-checking in NLP assumes that counter-evidence to a false claim exists before the claim is checked; for most real misinformation it does not, and professional fact-checkers create it. In MultiFC, 69.7% of misinformation claims have evidence snippets that come from or repeat a fact-check of the same claim, and models trained on it exploit this leaked evidence. Realistic datasets need evidence that is both sufficient and unleaked.

## Motivation

- Standard NLP fact-checking retrieves evidence for a claim and predicts a verdict ([Guo et al., 2022](https://doi.org/10.1162/tacl_a_00454)), presuming that refuting evidence can be found from the claim's content alone.
- Misinformation spreads exactly where credible information is missing, so evidence refuting a new claim often only appears in the fact-check written about it.
- Models on MultiFC could predict verdicts from evidence snippets without the claim ([Hansen et al., 2021](https://doi.org/10.1145/3404835.3463067)); why was unclear.
- Leaked evidence was noted at the same time by [Khan et al., 2022](https://aclanthology.org/2022.findings-acl.282/), without dataset analysis or model experiments.

## Method

Vocabulary of this vault: a fact-check is an article from a fact-checking organisation; leakage is information from after the claim's verification reaching the evaluation.

**Verification strategies.** 100 misinformation claims (50 PolitiFact, 50 Snopes; half from the MultiFC era before 2019, half from 2020/2021) are coded by how fact-checkers refuted them. Global counter-evidence contradicts the claim regardless of its source. Local counter-evidence, non-credible source and no-evidence assertion all need a source guarantee: knowing which source the claimant relied on.

Intuition: a system that sees only the claim text can only use global counter-evidence, since it cannot establish what the claim was based on.

**Evidence criteria.** Sufficient: evidence lets a human justify the verdict. Unleaked: evidence contains no information that existed only after the claim was verified.

**Leak detection.** A snippet is leaked if it comes from a fact-checking site (URL patterns) or discusses the claim's veracity (phrase patterns), which also catches fact-checks republished on other sites.

**Exploitation test.** BERT predicts the verdict from snippets only (title, text, both) or claim plus snippets, on Snopes and PolitiFact claims from MultiFC; test claims are split by whether leaks were detected.

## Key numbers

- Fact-checkers used global counter-evidence for 20 of 75 applicable claims (26.7%); about two-thirds were refuted via a source guarantee.
- Leaked evidence detected automatically for 69.7% of 16,244 MultiFC misinformation claims.
- Of 230 automatically flagged snippets in 100 claims, 83.9% were confirmed leaked; 97 of those 100 claims had at least one leaked snippet.
- Of 100 claims with no automatic detection, about a third still had leaked evidence on manual inspection.

## Experiments

- **Human verification strategies:** two-round coding of 100 claims, 25 excluded as multimodal or scam; pilot agreement 9 of 10.
- **Dataset survey:** sixteen datasets with natural claims; none with real misinformation meets both criteria. Fact-check-based evidence is sufficient but leaked; Wikipedia or science evidence is insufficient; search-engine evidence leaks even after removing the claim's own fact-check, since other organisations check the same claims.
- **Leak analysis in MultiFC:** among 100 claims without detected leaks, 15 had unleaked refuting evidence, but in 10 it was outweighed by leaked evidence; 40 had supporting evidence, mostly from misinformation itself.
- **Model reliance:** snippet-only BERT matches the earlier specialised model; scores differ between leaked and unleaked subsets, and a comparison on the same claims with leaked vs unleaked evidence confirms the dependence.

## Data

- 20,274 crawled PolitiFact claims, used for verdict trends: after 2016 fact-checkers chose more false claims; in 2021 under 10% were true.
- 100 manually analysed misinformation claims from PolitiFact and Snopes.
- MultiFC: 16,244 misinformation claims with search-engine evidence snippets.

> [!failure] Limitations
> - English claims from two US organisations; strategies may differ elsewhere.
> - Leak detection relies on hand-written patterns and misses about a third of leaks.
> - The leak criterion is relative to the verification date, which MultiFC does not always record precisely.
> - No method is proposed for finding source guarantees automatically.

## Relation to our project

- It frames our question from the other side: for verification a later fact-check is leakage, while in PFCR retrieving the existing fact-check is the task. The leak is a fact-check published after the post, which is what our causal index removes ([[Proposed Task]]).
- Its finding that most new misinformation lacks prior counter-evidence predicts low answerability under a causal pool for genuinely new claims; we report the answerable rate separately ([[Enhanced topic research]]).
- Fact-checks of the same claim by other organisations are leaks for verification but legitimate earlier siblings for PFCR, which our cluster-expanded qrels exploit ([[Research summary]]).
- The paper itself names claim matching ([[That is a Known Lie]]) as related but different and does not evaluate retrieval.

## Future work

- **Done:** a real-world verification dataset with evidence restricted to before the claim date and leaks from fact-checks audited; [[AVeriTeC]].
- **Done:** measuring how much web-retrieval verification depends on fact-check sites and post-claim pages; [[Complex Claim Verification in the Wild]].
- **Partly done:** reconstructing the claimant's flawed reasoning from its source, the source-guarantee path the authors propose, for misrepresented science; [Glockner et al., 2024](https://aclanthology.org/2024.acl-long.240/).
- **Open:** automatic provenance detection that traces a claim to its source across platforms (searched 2026-10).
