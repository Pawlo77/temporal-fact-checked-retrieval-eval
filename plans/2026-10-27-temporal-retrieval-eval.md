---
title: "Temporal retrieval evaluation plan"
type: plan
domain: vault
parent: "[[temporal-fact-checked-retrieval-eval]]"
status: draft
created: 2026-10-27
updated: 2026-10-27
tags: [plan, task, proposal]
related:
  - "[[Original Task]]"
  - "[[2026-10-27-topic-research|Topic research]]"
  - "[[2026-10-27-language-scope|Language scope analysis]]"
  - "[[2026-10-27-literature-corrections|Literature corrections log]]"
  - "[[Research]]"
---
# Temporal Retrieval Evaluation Plan

**Status:** draft

**Goal:** Measure how much of the reported performance of previously fact-checked claim retrieval (PFCR) survives an index that cannot see the future, and release the protocol, split and code so others can reuse them. One project that covers the whole of [[Original Task]]: both team slots of the brief (sparse and dense baselines; reranking and gap decomposition) are workstreams of a single study with one split, one results table and one paper.

**Architecture:** A dated MultiClaim corpus feeds one protocol module that builds the random, strict causal, size-matched and cluster-expanded pools. Retrieval systems (BM25, dense, cross-lingual, rerankers, LLM-scale) run under every protocol and write rows to one shared results table. Analysis reads that table: paired bootstrap per system, difference-in-differences for Polish vs English, dose-response mixed model across languages, additive gap decomposition, 50 hand-coded failures.

**Tech Stack:** Python 3.12, uv, `bm25s` or Pyserini, sentence-transformers and transformers, MLflow, statsmodels, EDEN cluster with GPU nodes ([[compute]]).

---

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

- **Languages:** Polish is the focus and headline, English the high-archive anchor. [[2026-10-27-language-scope|Language scope analysis]] recommends adding Spanish, German, Turkish, Czech and Slovak, chosen to span archive size, so that the mechanism is tested as a dose-response instead of a two-point contrast.
- **Fallback:** Polish and English only is the brief's scope and a strict subset of this plan; every deliverable holds in that case, and only the mechanism test (RQ3 dose-response) weakens.
- **Gate:** the wider language set needs the supervisor's sign-off and MultiClaim v2 access; it is an additive robustness layer, not a change of the brief's deliverables.
- **Reporting rules:** within-language deltas and slopes only, no ranking of languages by absolute score, so the study stays clear of the published language-bias work.
- **Out of scope:** new retrieval architecture, veracity judging, language-bias analysis; aggregate error reporting only, no ranked list of outlets or authors; [[MultiClaim]] access terms respected in any release.

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
- LLM scale: [[Qwen3 Embedding|Qwen3-Embedding-8B]] and a Qwen3 reranker, with pre- and post-cutoff query strata; the single-family risk is handled in the LLM selection plan once written.
- Fine-tuned multilingual-e5 under random and chronological training.

## Metrics and statistics

- Success@10 and MRR, answerable rate, conditional and unconditional scores; time-to-findability curve per language and system.
- Paired bootstrap over queries for random-vs-causal deltas; independent bootstrap per language for the Polish-English difference-in-differences; Holm across systems.
- Dose-response: mixed-effects model of per-query hit on protocol × log causal same-language pool size, with sibling count, signed lag and calendar-time spline; pre-registered tests H-PL and H-DOSE.
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

- MultiClaim v1 (Zenodo 7737983), v2 (Zenodo 15413169), [[SemEval-2025 Task 7]] data (Zenodo 14989176), [[MultiClaimNet]] clusters; [[AMC-16K]] as secondary set.
- Timestamps: earliest instance as publication time, day resolution with margin sensitivity (0, 1, 7 days), 100 dates per language checked against live URLs.

## Tasks

### Task 1: Data access and dated corpus (W1)

**Files:**
- Create: `src/temporal_fact_checked_retrieval_eval/dataset/` loaders, `configs/` dataset config
- Test: `tests/` loader and date-parsing tests on a synthetic fixture

- [ ] **Step 1:** Send the Zenodo access requests for v1, v2 and the SemEval data (institutional address) and log the dates.
- [ ] **Step 2:** Write loaders for posts, fact-checks and pairs; earliest-instance timestamps; drop and report posts without dates.
- [ ] **Step 3:** Sample-check 100 dates per language against live URLs; record the margin-sensitivity result.
- [ ] **Step 4:** Measure per-language counts, answerable rates and archive sizes; restate the power analysis with measured numbers.

### Task 2: Protocols and shared split (W1)

**Files:**
- Create: protocol module for random, strict causal, size-matched, cluster-expanded and rolling-origin pools
- Test: property tests (a pool never contains a fact-checked item dated after the post; size-matched pool has the same size)

- [ ] **Step 1:** Implement the strict causal pool and the answerability flag.
- [ ] **Step 2:** Implement the size-matched control and the cluster-expanded relevance via [[MultiClaimNet]].
- [ ] **Step 3:** Implement the delayed-query variant for time-to-findability and the chronological training split.
- [ ] **Step 4:** Freeze the split ids and publish the id lists plus the rebuild code (no post text).

### Task 3: Sparse and dense baselines (W2)

**Files:**
- Create: BM25 with causal-pool statistics, dense encoders, shared results writer
- Test: scoring tests on a toy corpus

- [ ] **Step 1:** BM25 with full-pool and causal-pool IDF; index once, mask by time at search time.
- [ ] **Step 2:** Encode the pool once with each dense model; apply time masks at search time.
- [ ] **Step 3:** Run all protocols and languages in scope on EDEN ([[compute]]) and write rows to the shared results table.

### Task 4: Reranking and LLM scale (W3)

**Files:**
- Create: cross-encoder reranking, LLM reranker with pre- and post-cutoff strata, fine-tuned retriever
- Test: rerank determinism and caching tests

- [ ] **Step 1:** Cross-encoder rerankers on top-100 for all languages in scope.
- [ ] **Step 2:** Fine-tune one multilingual-e5 retriever under random and chronological training.
- [ ] **Step 3:** LLM reranker on Polish and English with query strata around the model's training cutoff (RQ5).

### Task 5: Analysis and gap decomposition (W4)

**Files:**
- Create: bootstrap and difference-in-differences code, mixed model, gap chain, annotation sheets
- Test: statistics tests on simulated data with known effects

- [ ] **Step 1:** Paired and per-language bootstrap with Holm across systems.
- [ ] **Step 2:** Additive gap chain with order-shuffling robustness; covariate regression.
- [ ] **Step 3:** Dose-response mixed model with the pre-registered tests; restate minimum detectable effects.
- [ ] **Step 4:** Code 50 newly failing queries (25 Polish, 25 English), two annotators, report kappa.
- [ ] **Step 5:** Validate LLM sibling qrels and narrative-drift labels on a human sample.

### Task 6: Release and paper (W5)

**Files:**
- Create: release package of ids, qrels and code; `report/` write-up

- [ ] **Step 1:** Check the release against the MultiClaim access terms; ids and code only.
- [ ] **Step 2:** One results table: at least four systems under both protocols for Polish and English (and the added languages), with significance tests; headline: how much more the temporal split costs Polish.
- [ ] **Step 3:** Write the paper from the shared table and the released code; target venues below.

## Deliverables

- Split definitions as id lists plus code that rebuilds them from the official files; no post text.
- Cluster-expanded qrels for earlier debunks (judged ids only).
- The shared results table, the gap decomposition, the dose-response analysis and the coded analysis of 50 failing queries.
- The paper.

## Venues

ACL Rolling Review (Findings or main) as an evaluation-methodology paper with a resource; SIGIR short or resource track; FEVER and NLP4PI workshops; a CLEF temporal PFCR task proposal for 2028 at the earliest. Fallback if the penalty is small: the leakage is answerability, not ranking.

## Risks

- Date reliability and missing post dates; small answerable Polish set; v2 access.
- Overlap with the dataset authors' group and with [[Role of Context in PFCR]]: claim only the index restriction, the decomposition and the multilingual mechanism test.
- Scope perception of the wider language set: the reporting rules and the sign-off gate address it.
- The full register is written separately once the risk scan finishes.
