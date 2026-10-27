# 2026 - Li - Simulated Ignorance Fails

## Citation

- Authors: Zehan Li, Yuxuan Wang, Ali El Lahib, Ying-Jieh Xia, Xinyu Pi
- Title: Simulated Ignorance Fails: A Systematic Study of LLM Behaviors on Forecasting Problems Before Model Knowledge Cutoff
- Venue: Proceedings of IJCAI-26 (Main Track), pages 5837-5845, DOI 10.24963/ijcai.2026/650; preprint arXiv:2601.13717 (v1, 20 Jan 2026)
- Year: 2026
- URLs: https://ijcai.org/proceedings/2026/650 ; https://arxiv.org/abs/2601.13717
- Verified on: 2026-10-27 (arXiv abstract page and IJCAI proceedings listing read)

## What it does

- Tests whether Simulated Ignorance (prompting a model to ignore knowledge after a stated cutoff) approximates True Ignorance on retrospective forecasting.
- Uses competition-level forecasting questions and 9 models.
- Finds cutoff instructions leave a large gap between simulated and true ignorance.
- Finds chain-of-thought does not suppress prior knowledge even when traces contain no explicit post-cutoff references; reasoning-optimised models show worse SI fidelity.
- Concludes SI-based retrospective forecasting evaluation is methodologically flawed.

## Key numbers

- arXiv abstract: 477 questions, 9 models, 52% performance gap between SI and TI.
- IJCAI abstract: 470 questions (the published version reports 470, not 477).
- IJCAI PDF Figure 1 caption: control-group Brier 0.11.

## Relation to our project

- Argues against prompting an LLM reranker to "pretend it is date t"; parametric leakage must be handled by stratifying queries by model knowledge cutoff (our RQ5 design), not by instructions.
- Does NOT cover: retrieval, fact-checking, ranking metrics.

## Verification

- CORRECTED. Note cites it only as "arXiv 2601.13717" and the reference list as "Simulated Ignorance Fails (pre-cutoff forecasting)" with no authors. It is published at IJCAI 2026 (Li et al.); cite the IJCAI version. The claim "simulated ignorance does not replicate true ignorance" is correct.
