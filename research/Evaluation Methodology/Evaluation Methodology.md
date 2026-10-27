---
title: "Evaluation Methodology"
tags: [type/hub]
created: 2026-10-27
parent: "[[Research]]"
---
# Evaluation Methodology

General evaluation practice that the temporal protocol builds on: how data is split, and what random and standard splits hide. Each theme is a folder with a note of its own name that lists its papers.

## Summary

- [[We Need to Talk about Standard Splits]] argues for random over standard splits; [[We Need to Talk about Random Splits]] rebuts it.
- Random splits over-estimate performance on new samples, often by over 20 points of error reduction.
- Prefer independent new samples, else biased or adversarial splits.
- [[Mind the Gap]]: a model trained only on text before the test period has up to 16% higher perplexity, and the gap grows with time.
- Open for our project: whether system order under Success@10 and MRR survives the switch to a causal index.
- Open: a control that holds training or pool size fixed and varies only the time of the data.

| Theme | Question it answers |
|-------|---------------------|
| [[Data Splits]] | How should data be split, and how much do random, standard and time-blind splits overestimate performance? |
