---
title: "Plan summary"
type: plan-note
domain: vault
parent: "[[2026-10-27-temporal-retrieval-eval]]"
tags: [summary, changes]
created: 2026-10-28
updated: 2026-10-28
related:
  - "[[Risk register]]"
---
## Project

We evaluate previously fact-checked claim retrieval (given a social media post, find the fact-check that already debunks it) on MultiClaim, with Polish as the focus and English as the control. The usual benchmark searches all fact-checks, including ones published after the post. We search only fact-checks that existed on the day of the post, as a real fact-checker would, and measure how much performance survives. Metrics: Success@10 (the right fact-check is in the top 10) and MRR (how high the first right result ranks).

- **Systems (4):** BM25, two dense encoders (multilingual-e5-large and a Polish or cross-lingual one) and a cross-encoder reranker.
- **Setups (3):** random (the usual benchmark), strict causal (only earlier fact-checks) and size-matched random (a random pool of the same size, to separate the effect of a smaller pool from the effect of time).
- **Tiers:** core is committed; core+ runs right after the core; conditional runs only if a stated condition holds; extended is the original stretch work.

## Research questions

| ID | Question | Status |
|---|---|---|
| RQ1 | How much performance survives when the index cannot see the future? | original |
| RQ2 | How much of the drop is a missing fact-check, a smaller pool, training leakage or missing labels? | original |
| RQ3 | Is the drop larger for Polish than for English? | original |
| RQ4 | How many days after a post does the first relevant fact-check appear? | original |
| RQ6 | Does the ranking of systems change between the normal and the time-respecting setup? | original |
| RQ7 | If a system may abstain on low-confidence posts, what is the trade-off between coverage and accuracy? | new, core |
| RQ8 | For Polish posts, how much do earlier English fact-checks recover? | new, core |
| RQ5 | Do LLM rerankers do better on facts they may have seen in training? | was a stretch goal, now core+ |

## What changed and why

| Change | Why |
|---|---|
| RQ7 added (core) | Many posts have no earlier fact-check, so the right answer is "don't know". Abstention curves split the drop into missing fact-check versus bad ranking. |
| RQ8 added (core) | It tests whether a thin Polish archive explains the Polish drop. It reuses the encoders we already plan to use. |
| Time-decay figure and effect sizes (core) | One extra figure from stored scores, and effect sizes (how big the drop is, not only whether it is significant) next to the significance tests. Almost no extra work. |
| RQ5 moved to core+ | We have the compute, so it runs right after the core. We added checks of what each model knows and when its knowledge ends. |
| Conformal retrieval (conditional) | It returns a set of candidates with a stated chance of containing the right fact-check. Interesting, but its guarantee is weak on time-ordered data. We do it only if abstention turns out to matter, and report measured coverage. |
| Dropped: synthetic difference-in-differences (a statistical comparison method), training our own dated models, a separate narrative-drift paper | Two languages are too few for the first, and the other two are too big for the time we have. |

Unchanged: the four systems, the three setups, the 50 hand-coded failures and the extended tier (sibling labels, more languages, a second dataset, a fine-tuned retriever).

The core only measured the drop. The additions explain it, and they reuse stored scores and models, so they add little work. The risky parts stay conditional.

## Timeline

| When | What |
|---|---|
| 18 Nov | Data access gate: without it we deliver the protocol and code on whatever data arrived. |
| 25 Nov | Split and results format frozen. |
| 16 Dec | Core done: 4 systems, 3 setups, 2 languages, plus the Polish run with earlier English fact-checks (RQ8). |
| 7 Jan | Core+ stops. Unfinished work is reported as exploratory. |
| 13 Jan | Final report. |

## Risks

- We do not know how many Polish posts have an earlier fact-check; we measure this first. Below 150 such posts, the Polish-English comparison becomes descriptive.
- MultiClaim access is restricted. We name every team member in one request and release only id lists and code, never post text.

## Open points

1. Approval of the new scope.
2. Will you co-sign the data access requests from a university address?
3. How is the project graded: how much weight does the manual analysis of 50 failed queries carry compared with the results table?
