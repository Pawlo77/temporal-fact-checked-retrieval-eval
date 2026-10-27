---
title: "Proposed Task"
type: handbook
domain: vault
parent: "[[temporal-fact-checked-retrieval-eval]]"
tags: [handbook, task, proposal]
created: 2026-10-27
updated: 2026-10-27
related:
  - "[[Original Task]]"
  - "[[Enhanced topic research]]"
  - "[[Language scope analysis]]"
  - "[[Research]]"
---
# Proposed Task

One project that covers the whole of [[Original Task]]: both team slots of the brief (sparse and dense baselines; reranking and gap decomposition) are workstreams of a single study with one split, one results table and one paper. Evidence, references and the full protocol definitions are in [[Enhanced topic research]]; the literature position is in [[Research]].

## Title

Retrieval that cannot see the future: a causal evaluation protocol for previously fact-checked claim retrieval, with answerability-aware metrics, a Polish focus and an archive-density mechanism test.

## Core idea

A naive "index only earlier fact-checks" filter conflates four effects: the gold debunk not existing yet, a smaller pool, supervised-training leakage, and missing labels for earlier debunks of the same claim. The project separates them instead of reporting one number, and asks whether the thin Polish archive explains a larger penalty.

## Research questions

- RQ1: How much Success@10 and MRR survive a causal index, on answerable queries, with pool size controlled?
- RQ2: What share of the random-vs-causal gap is answerability loss, pool composition, training leakage, or missing sibling labels?
- RQ3: Is the penalty larger for Polish than for English (difference-in-differences), and does archive density at query time explain it (dose-response across and within languages)?
- RQ4: How many days after a post does the first relevant fact-check become retrievable (time-to-findability)?
- RQ5: Do LLM rerankers benefit from parametric knowledge of later debunks?

## Scope

- **Languages:** Polish is the focus and headline, English the high-archive anchor. [[Language scope analysis]] recommends adding Spanish, German, Turkish, Czech and Slovak, chosen to span archive size, so that the mechanism is tested as a dose-response instead of a two-point contrast.
- **Fallback:** Polish and English only is the brief's scope and a strict subset of this plan; every deliverable below holds in that case, and only the mechanism test (RQ3 dose-response) weakens.
- **Gate:** the wider language set needs the supervisor's sign-off and MultiClaim v2 access; it is an additive robustness layer, not a change of the brief's deliverables.
- **Reporting rules:** within-language deltas and slopes only, no ranking of languages by absolute score, so the study stays clear of the published language-bias work.

## Workstreams

- **W1 Data and protocol:** dated corpus from MultiClaim v1, v2 and SemEval-2025 data; the shared split and its release.
- **W2 Sparse and dense baselines:** BM25 with causal-pool statistics, multilingual dense retrievers, a bilingual or cross-lingual encoder, all languages in scope.
- **W3 Reranking and LLM scale:** cross-encoder rerankers on all languages; the LLM reranker (RQ5) and the fine-tuned retriever on Polish and English.
- **W4 Gap decomposition and analysis:** the additive gap chain, the dose-response model, 50 hand-coded newly failing queries.
- **W5 Release and paper:** split ids, qrels, code, results table, write-up.
- W1 feeds W2 and W3; W2 and W3 fill one shared results table; W4 reads it.

## Protocols

- Random protocol: the published setup.
- Strict causal protocol: per-query pool of fact-checks published before the post; a query is answerable only if a gold fact-check is in it.
- Size-matched random control: same pool size per query, drawn from the full pool, gold kept.
- Cluster-expanded causal protocol: relevance extended to earlier same-claim fact-checks via [[MultiClaimNet]] clusters and LLM-proposed, human-validated judgments.
- Rolling-origin and delayed-query variants for time-to-findability.
- Statistics leakage: BM25 IDF and length statistics from the causal pool only, full-pool statistics as a sensitivity row.
- Chronological vs random training split for one fine-tuned retriever.

## Systems

- BM25 on original text and provided translation.
- Multilingual dense: [[Multilingual E5|multilingual-e5-large]], [[BGE-M3]].
- Polish or cross-lingual encoder: [[mmlw-retrieval-roberta-large]], [[LaBSE]].
- Cross-encoder rerankers: [[bge-reranker-v2-m3]], [[polish-reranker-roberta-v3]].
- LLM scale: [[Qwen3 Embedding|Qwen3-Embedding-8B]] and a Qwen3 reranker, with pre- and post-cutoff query strata.
- Fine-tuned multilingual-e5 under random and chronological training.

## Metrics and statistics

- Success@10 and MRR, answerable rate, conditional and unconditional scores; time-to-findability curve per language and system.
- Paired bootstrap over queries for random-vs-causal deltas; independent bootstrap per language for the Polish-English difference-in-differences; Holm across systems.
- Dose-response: mixed-effects model of per-query hit on protocol × log causal same-language pool size, with sibling count, signed lag and calendar-time spline; pre-registered tests H-PL and H-DOSE ([[Language scope analysis]]).
- Power: with MultiClaim v2, Polish has roughly 1,190 to 1,690 queries and detects a Polish-English difference of about 6 points of Success@10 on answerable queries (assumed discordance and answerable rate, restated after the first run); without v2 only about 450 Polish queries remain and the minimum detectable difference is larger.

## Gap decomposition and analysis

- Additive chain: random, size-matched random, cluster-expanded causal, strict causal answerable, strict causal all queries, with bootstrap intervals and order-shuffling robustness.
- Covariates: signed post-to-debunk lag, lexical overlap, cross-lingual gold flag, relationship type, earlier-sibling count, topic, platform.
- Narrative drift judged by an LLM and validated on a human sample.
- 50 newly failing queries (25 Polish, 25 English), two annotators, kappa; codebook: answerability, lexical leakage, narrative drift, cross-lingual-only debunk, missing label, timestamp error, multimodal-only.

## Novelty position

- Not new: time-respecting retrieval evaluation ([[TREC 2011 Microblog]]), chronological train/test splits for PFCR ([[Role of Context in PFCR]], English debates), out-of-time PFCR test posts ([[SemEval-2025 Task 7]]), [[MultiClaim]]'s post-newer/older and pool-size analyses, language-bias analysis ([[Language and Retrieval Bias]]).
- New: a per-query date-restricted fact-check index for PFCR, answerability separated from ranking, a pool-size control matched to the time-restricted pool, statistics leakage for PFCR, sibling qrels, time-to-findability, the additive gap decomposition, and the archive-density mechanism test.
- Training-time leakage is an extension of [[Role of Context in PFCR]] to multilingual social-media data.

## Data

- MultiClaim v1 (Zenodo 7737983), v2 (Zenodo 15413169), [[SemEval-2025 Task 7]] data (Zenodo 14989176), [[MultiClaimNet]] clusters; [[AMC-16K]] as secondary set. The access request must go out now.
- Timestamps: earliest instance as publication time, day resolution with margin sensitivity (0, 1, 7 days), 100 dates per language checked against live URLs.

## Deliverables

- Released split definitions as id lists plus code that rebuilds them from the official files; no post text.
- Cluster-expanded qrels for earlier debunks (judged ids only).
- One results table: at least four systems under both protocols, Polish and English (and the added languages), with significance tests; the headline number is how much more the temporal split costs Polish.
- Gap decomposition, dose-response analysis and the coded analysis of 50 failing queries.
- The paper, written from the shared table and the released code.

## Out of scope

New retrieval architecture, veracity judging, language-bias analysis. Aggregate error reporting only; no ranked list of outlets or authors; [[MultiClaim]] access terms respected in any release.

## Venues

ACL Rolling Review (Findings or main) as an evaluation-methodology paper with a resource; SIGIR short or resource track; FEVER and NLP4PI workshops; a CLEF temporal PFCR task proposal for 2028 at the earliest. Fallback if the penalty is small: the leakage is answerability, not ranking.

## Main risks

- Date reliability and missing post dates; small answerable Polish set; v2 access.
- Overlap with the dataset authors' group and with [[Role of Context in PFCR]]: claim only the index restriction, the decomposition and the multilingual mechanism test.
- Scope perception of the wider language set: the reporting rules and the sign-off gate address it.
- Details in [[Enhanced topic research]] and [[Language scope analysis]].
