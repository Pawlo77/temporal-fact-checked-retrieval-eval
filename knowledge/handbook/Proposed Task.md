---
title: "Proposed Task"
type: handbook
domain: vault
parent: "[[temporal-fact-checked-retrieval-eval]]"
tags: [handbook, task, proposal]
created: 2026-10-27
updated: 2026-10-27
---
# Proposed Task

Enhanced version of [[Original Task]], derived from [[Enhanced topic research]] (evidence, references, power analysis); literature state and verified novelty in [[Research summary]]. The assigned scope stays intact (temporal split, 4+ systems, Polish vs English, gap decomposition, 50 failing queries); the additions raise novelty and publication chances.

## Title

Retrieval that cannot see the future: a causal evaluation protocol for previously fact-checked claim retrieval, with answerability-aware metrics and a Polish-English contrast.

## Core idea

A naive "index only earlier fact-checks" filter conflates four effects: the gold debunk not existing yet, a smaller pool, supervised-training leakage, and missing labels for earlier debunks of the same claim. The project separates them instead of reporting one number.

## Novelty position

- Not new: time-respecting retrieval evaluation (TREC 2011 Microblog), chronological train/test splits for PFCR (Shaar et al., Findings NAACL 2022, English debates), out-of-time PFCR test posts (SemEval-2025 Task 7), MultiClaim's post-newer/older and random pool-size analyses, and language-bias analysis (Vykopal et al., EACL 2026).
- New: a per-query date-restricted fact-check index for PFCR evaluation, answerability separated from ranking, a pool-size control matched to the time-restricted pool, statistics leakage measured for PFCR, sibling qrels, time-to-findability, and the additive gap decomposition.
- Training-time leakage is an extension: random vs chronological training on multilingual social-media PFCR, separated from index and answerability effects.
- Cite Shaar et al. 2022, TREC 2011 Microblog and MultiClaim's three temporal analyses as precedents.

## Research questions

- RQ1: How much Success@10 and MRR survive a causal index, on answerable queries, with pool size controlled?
- RQ2: What share of the random-vs-causal gap is answerability loss, pool composition, training leakage, or missing sibling labels?
- RQ3: Is the penalty larger for Polish than English (difference-in-differences), and does archive density at query time explain it?
- RQ4: How many days after a post does the first relevant fact-check become retrievable (time-to-findability)?
- RQ5: Do LLM rerankers benefit from parametric knowledge of later debunks?

## What is added over the original

- Strict causal protocol plus a per-query size-matched random control, a cluster-expanded causal protocol (earlier same-claim debunks via MultiClaimNet clusters), rolling-origin and delayed-query variants.
- Statistics leakage: BM25 IDF and length statistics computed from the causal pool only (cumulative document frequencies by fact-check date), with full-pool statistics as a sensitivity row.
- Answerable rate reported next to conditional and unconditional Success@10 and MRR.
- Time-to-findability curve per language and system.
- Chronological vs random training split for one fine-tuned retriever, extending Shaar et al. 2022 to multilingual social-media data.
- Additive gap chain: random, size-matched random, cluster-expanded causal, strict causal answerable, strict causal all queries, with paired-bootstrap intervals and order-shuffling robustness.
- Sibling qrels: LLM-proposed judgments, human-validated on 200 Polish and 200 English items.
- Power statement: with about 450 Polish queries, a Polish-English difference under roughly 4-6 points of Success@10 is not detectable (assumed discordance, to re-state after the first run). Pool MultiClaim v1, v2 and the SemEval-2025 test to raise Polish counts.

## Language scope

- [[Language scope analysis]] recommends Polish as the headline, English as the high-archive anchor, plus Spanish, German, Turkish, Czech and Slovak chosen to span archive size.
- The mechanism is tested as a dose-response: causal penalty against archive density (log causal same-language pool size, earlier-sibling count, post-to-debunk lag), mainly within languages, with the seven-language spread as corroboration.
- The brief's deliverables stay unchanged: Polish-English difference-in-differences as the central number, 50 manual queries (25 Polish, 25 English); the LLM reranker and full gap chain stay on Polish and English.
- Reporting rules keep it out of language-bias scope: only within-language deltas and slopes, no ranking of languages by absolute score.
- Requires supervisor sign-off before committing, since the brief names Polish and English only; without MultiClaim v2 access it degrades towards Polish-English only.

## Systems

- BM25 (original text and provided translation), with causal-pool statistics.
- Multilingual dense: multilingual-e5-large and BGE-M3.
- Polish or cross-lingual encoder: mmlw-retrieval-roberta-large, LaBSE.
- Cross-encoder reranker: bge-reranker-v2-m3, polish-reranker-roberta-v3.
- LLM scale: Qwen3-Embedding-8B and a Qwen3 reranker (parametric-leakage strata).
- Fine-tuned multilingual-e5 under random and chronological training regimes.

## Data

- MultiClaim v1 (Zenodo 7737983), MultiClaim v2 (Zenodo 15413169), SemEval-2025 Task 7 (Zenodo 14989176), MultiClaimNet clusters; AMC-16K as secondary set. Access request must go out now.
- Timestamps: earliest instance as publication time; day resolution with margin sensitivity (0, 1, 7 days); sample-check 100 dates per language against live URLs.

## Deliverables

- Released split definitions as id lists plus code rebuilding them from the official files; no post text.
- Cluster-expanded qrels for earlier debunks (judged ids only).
- Results table (4+ systems, both protocols, Polish and English, significance tests) with the Polish-English contrast as the headline number.
- Gap decomposition and a coded analysis of 50 newly failing queries (25 Polish, 25 English, two annotators, kappa), codebook: answerability, lexical leakage, narrative drift, cross-lingual-only debunk, missing label, timestamp error, multimodal-only.

## Out of scope

New retrieval architecture, veracity judging, language-bias analysis. Aggregate error reporting only; no ranked list of outlets or authors; MultiClaim access terms respected in any release.

## Venues

ACL Rolling Review (Findings or main) as evaluation-methodology plus resource paper; SIGIR short or resource track; FEVER and NLP4PI workshops; candidate temporal PFCR task for CLEF 2028 at the earliest (CLEF 2027 proposals closed on 17 July 2026). Fallback if the penalty is small: the leakage is answerability, not ranking.

## Main risks

- Date reliability and missing post dates.
- Small answerable Polish set.
- Overlap with the dataset authors' group: cite their post-newer/older analysis, pool-size sweep and date-filter system, and frame this as a complement.
- Overlap with Shaar et al. 2022: claim only the index restriction, decomposition and multilingual setting.
- Details in [[Enhanced topic research]].
