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
  - "[[Topic research]]"
  - "[[Language scope]]"
  - "[[LLM selection]]"
  - "[[Risk register]]"
  - "[[Literature corrections]]"
  - "[[Research]]"
  - "[[Qwen3 Embedding]]"
  - "[[Gemma 3]]"
  - "[[Apertus]]"
  - "[[Olmo 3]]"
  - "[[Bielik 11B v3]]"
  - "[[Llama 3.3]]"
  - "[[gpt-oss-120b]]"
  - "[[Command A]]"
  - "[[Mistral Large 2411]]"
  - "[[LLM Judges Favour LLM Rankers]]"
  - "[[Self-Preference Bias]]"
  - "[[Panel of LLM Evaluators]]"
---
# Temporal Retrieval Evaluation Plan

**Status:** draft, for the supervisor's approval

**Goal:** Measure how much of the reported performance of previously fact-checked claim retrieval (PFCR) survives an index that cannot see the future, separate the reasons for the drop, and release the protocol, split definitions and code so others can reuse them. This is the whole of project 2 ("Retrieval that cannot see the future: temporal evaluation of fact-checked claim retrieval") as one study: both team slots of the brief (sparse and dense baselines; reranking and gap decomposition) are workstreams of a single plan with one split, one results table and one paper.

**Architecture:** A dated MultiClaim corpus, read through a dataset-agnostic adapter, feeds one protocol module that builds the random, strict causal, size-matched and cluster-expanded pools. Retrieval systems run under every protocol and write rows to one shared results table. Analysis reads that table: cluster bootstrap per system, Polish-English difference-in-differences, an additive gap decomposition, and 50 hand-coded failures. Everything beyond the brief's scope is a stretch tier that unlocks only after the core is complete.

**Tech Stack:** Python 3.12, uv, bm25s (custom causal statistics), sentence-transformers, transformers and vLLM, MLflow, statsmodels; EDEN cluster with A100-class GPUs; open-weight models only for any text taken from MultiClaim.

---

## 1. Title

Retrieval that cannot see the future: a causal evaluation protocol for previously fact-checked claim retrieval, with answerability-aware metrics and a Polish focus.

## 2. Problem and motivation

PFCR benchmarks (MultiClaim, SemEval-2025 Task 7) score systems against a search pool that also contains fact-checks published after the query post. A fact-checker searching on the day of the post only has the earlier archive. A naive "index only earlier fact-checks" filter conflates four effects: the gold fact-check not existing yet, a smaller pool, supervised-training leakage, and missing labels for earlier fact-checks of the same claim. The project separates these effects instead of reporting one number, and tests whether the thin Polish fact-check ecosystem makes the penalty larger than for English.

## 3. Research questions and hypotheses

- **RQ1:** How much Success@10 and MRR survive a causal index, reported unconditionally (unanswerable queries count as misses) and on answerable queries, with pool size controlled?
- **RQ2:** What share of the random-vs-causal gap is answerability loss, pool composition, training leakage, or missing sibling labels?
- **RQ3:** Is the penalty larger for Polish than for English (difference-in-differences)? With the extended languages: does archive density at query time explain it?
- **RQ4:** How many days after a post does the first relevant fact-check become retrievable (time-to-findability among debunked posts)?
- **RQ5 (stretch):** Do LLM rerankers gain more on queries whose gold fact-check predates the model's training cutoff, and does that gain track each model's own cutoff?
- **RQ6:** Does the ranking of retrieval systems change between the random and the causal protocol (rank reversals, rank correlation with intervals, significance of the reversals), and does the effect appear on a second dated dataset?
- **H-answerability:** most gold pairs are post-first, so many queries are unanswerable under a causal index by definition; the share is measured first, not assumed.
- **H-distractors (restated after the risk review):** on queries whose gold is unchanged between protocols, the causal pool only removes later distractors, so the conditional score may rise; the hypothesis is that time-local distractors are harder than the same number of random ones (causal vs size-matched random). A null or positive conditional delta is reported as a finding.
- **H-PL and H-DOSE (extended tier):** pre-registered tests of the Polish-English difference and of the dose-response on log causal same-language pool size.

## 4. Scope

**Core tier (committed, equals the brief):**
- Languages: Polish (focus) and English (control).
- Systems: BM25 with causal-pool statistics, multilingual-e5-large, a cross-lingual or Polish encoder (mmlw-retrieval-roberta-large or LaBSE), and bge-reranker-v2-m3 as cross-encoder.
- Protocols: random, strict causal, size-matched random.
- Analysis: Success@10 and MRR with cluster-bootstrap significance, gap decomposition, 50 hand-coded newly failing queries (25 Polish, 25 English).

**Extended tier (stretch, unlocked in this order once the core is complete and at least four supervisor Wednesdays remain):**
1. Sibling qrels for Polish: cluster-expanded causal protocol with a validated three-family LLM judge panel.
2. More languages, once MultiClaim v2 access is granted: Spanish, German, Turkish, Czech, Slovak, chosen to span archive size so that the Polish-English contrast becomes a dose-response (see section 6).
3. A second dated dataset to show that the effect generalises beyond MultiClaim (see Task 5).
4. Fine-tuned retriever under random and chronological training.
5. LLM-scale systems and RQ5, only with models whose training cutoff is documented (section 7).

**Out of scope:** a new retrieval architecture, judging claim veracity, language-bias analysis (already published on this dataset). Errors are reported in aggregate; there is no ranked list of outlets or authors.

## 5. Protocols and methods

- **Random protocol:** the published setup.
- **Strict causal protocol:** per-query pool of fact-checks published before the post; a query is answerable only if a gold fact-check is in the pool.
- **Size-matched random control:** the same pool size per query, drawn from the full pool, gold kept.
- **Cluster-expanded causal protocol (extended):** relevance extended to earlier same-claim fact-checks via MultiClaimNet clusters and judge-panel labels; every system is also reported on fact-checker-only qrels, so the expanded numbers are a bound, not the primary result.
- **Statistics leakage:** BM25 IDF and length statistics from the causal pool only (cumulative document frequencies by date), full-pool statistics as a sensitivity row.
- **Time-to-findability:** delayed-query variant (re-query at post date plus 0, 1, 3, 7, 30, 90 days); right-censored at the dataset end; named "among debunked posts" because every post in the data has a fact-check by construction.
- **Timestamps:** a fact-check or post can carry several dated instances (republications, other outlets or platforms), so its time is an interval, not a point. Primary rule: earliest instance as publication time, day resolution. Sensitivity runs: margins of 0, 1 and 7 days; first-listed and median instance; and bounds, a conservative pool (fact-check counts as published only at its latest instance, post at its earliest) against a liberal pool (earliest instance for the fact-check, latest for the post). Report, per language, the answerable rate and every headline score under both bounds, the share of queries whose pool membership flips between them, and a clean subset restricted to single-instance fact-checks. 100 dates per language are checked against live URLs; posts without dates are dropped and reported.
- **Metrics and statistics:** Success@10, MRR, answerable rate, conditional and unconditional scores; cluster bootstrap by gold fact-check or MultiClaimNet cluster (posts sharing a fact-check are not independent); Holm correction across systems; difference-in-differences with an independent bootstrap per language.
- **Gap decomposition:** additive chain random, size-matched random, cluster-expanded causal, strict causal answerable, strict causal all queries, every step scored unconditionally on one fixed query set, with order-shuffling (Shapley-style averaging); the core chain omits the cluster-expanded step, which belongs to the extended tier; covariates: signed post-to-debunk lag, lexical overlap, cross-lingual gold flag, relationship type, earlier-sibling count, topic, platform.
- **Failure analysis:** 50 newly failing queries, two annotators, Cohen's kappa; codebook: answerability, lexical leakage, narrative drift, cross-lingual-only debunk, missing label, timestamp error, multimodal-only. Failure coding stays human; LLMs may only pre-sort.

## 6. Languages

- **Core:** Polish (focus, headline) and English (high-archive control).
- **Why widen (extended tier):** with two languages the contrast has zero degrees of freedom for a mechanism claim, and Polish is not extreme (6,912 Polish fact-checks in MultiClaim v1, close to Turkish 6,676 and German 4,996; English has 85,814). A dose-response of the penalty against archive density turns the "thin archive" claim into a testable prediction.
- **Extended set:** Spanish, German, Turkish, Czech, Slovak plus Polish and English (seven languages); the mechanism is identified mainly from within-language variation (the causal pool grows over time in every language), with the between-language spread as corroboration.
- **Reporting rules that keep it out of the language-bias study:** only within-language deltas and slopes, no ranking of languages by absolute score, language as a random effect.
- **Gate:** MultiClaim v2 access; without v2 the plan degrades to Polish and English only, which is the brief.
- **Power:** with v2, Polish has roughly 1,190 to 1,690 queries; the minimum detectable Polish-English difference is about 6 points of Success@10 on answerable queries if 30% of queries are answerable, and larger if fewer are (assumed numbers, restated after the first data load).

## 7. Models

**Core systems (all open weights):** BM25 (bm25s with custom causal statistics), multilingual-e5-large, mmlw-retrieval-roberta-large or LaBSE, bge-reranker-v2-m3.

**Extended systems:** BGE-M3 and polish-reranker-roberta-v3 as additional encoder and cross-encoder.

**LLM-scale systems and why more than one family.** Relying on a single LLM family would be a research risk: parametric leakage is a property of one model's pretraining data and cutoff, Qwen3 states no cutoff, and LLM judges are documented to favour LLM rankers and their own outputs. The LLM tier therefore uses several families, over one shared first-stage candidate list (top 30 to 50):

| Role | Model | Stated cutoff | Why |
|---|---|---|---|
| Retriever | [[Qwen3 Embedding\|Qwen3-Embedding-8B]] | none stated | strongest multilingual embedder; "cutoff unknown" stratum |
| Reranker | [[Qwen3 Embedding\|Qwen3-Reranker-8B]] | none stated | continuity; "cutoff unknown" |
| Reranker | [[Gemma 3\|Gemma 3 27B-it]] | August 2024 | cutoff inside the query period |
| Reranker (auditable) | [[Apertus\|Apertus-70B-Instruct]] (and 8B for a size axis) | March 2024 | open pretraining data: each gold fact-check can be searched for |
| Reranker (auditable, English) | [[Olmo 3\|Olmo 3 32B]] | December 2024 | second open-data cutoff |
| Reranker (Polish) | [[Bielik 11B v3\|Bielik-11B-v3.0-Instruct]] | none stated | Polish-specialised |
| Reranker (control) | [[Llama 3.3\|Llama-3.3-70B-Instruct]] | December 2023 | earliest cutoff, widest split |
| Judge | [[gpt-oss-120b]], [[Command A\|Command A (03-2025)]], [[Mistral Large 2411\|Mistral-Large-Instruct-2411]] | n/a | three families disjoint from every evaluated system; majority vote |

- **RQ5 design:** per model with a stated cutoff, stratify queries by gold fact-check date before or after that cutoff and estimate the reranker gain over the shared first stage; control with difference-in-differences against the cross-encoders; a gain jump at each model's own cutoff, not at a common date, is the leakage signature. Qwen3 and Bielik are reported as "cutoff unknown". For Apertus and Olmo, exposure is checked directly in the released pretraining data.
- **Narrative-drift labels (validity gate):** the drift prompt and judge-panel model versions are frozen before validation; two humans label a stratified calibration sample of 100 items (50 Polish, 50 English); drift enters the analysis as a covariate only when the panel-vs-human Cohen's kappa is at least 0.6 on each language, otherwise it is reported as exploratory and the human-coded 50 failing queries carry the drift finding; every drift result is shown with and without the covariate, and a 5% sample is rerun three times for label flip rate.
- **Judge protocol:** binary sibling relevance and three-way narrative drift; independent labels with one released prompt; majority label; Fleiss' kappa across judges, Cohen's kappa against humans per language, each judge validated on the 400 Polish pairs of AMC-16K before use; humans label 200 Polish and 200 English items.
- **Controls:** models pinned by repository and commit hash; temperature 0 and fixed seed; prompts, parsing rules and a response cache released (ids and labels, never post text); a 5% sample rerun three times to report label flip rate; candidate order randomised.
- **Data terms:** post text is sent only to local open-weight models; no API call carries MultiClaim text unless the access terms are confirmed to allow it.
- **Licences to record:** Command A is CC-BY-NC and Mistral Large 2411 is under the Mistral Research License (research use only).

## 8. Data and access

- MultiClaim v1 (Zenodo 7737983), v2 (Zenodo 15413169), SemEval-2025 Task 7 data (Zenodo 14989176), MultiClaimNet clusters; AMC-16K as secondary set.
- The Zenodo records are access-restricted and research-only: request from an institutional (pw.edu.pl) address, **name every team member in one request**, which is what allows sharing among them; the data stays in a restricted directory on EDEN readable only by the named members, is never sent to an LLM API and never shared with anyone not named. Data is deleted at project end. The project has one team; no second team receives the data.
- **Privacy of posts:** posts are real people's text, so no verbatim post text appears in the paper, the repository or the release; examples are paraphrased; errors are reported in aggregate, never per outlet or author.
- **Licences:** MultiClaim's code (GPL-3.0) is not copied into this repository (the protocol is reimplemented from the paper); the licence of every dataset, model and tool used is recorded in a table in the repository and the paper.
- Release: id lists, cutoffs, judged ids and code that rebuilds the split from the official files; no post text. Whether id lists may be released is to be confirmed with the dataset authors in writing.
- The brief's "reproduces from public data" is read as "reproduces for anyone granted MultiClaim access".

## 9. Tasks

### Task 0: Approvals and access (week 1)

- [ ] **Step 1:** Send the v1, v2 and SemEval access requests from pw.edu.pl addresses naming all team members (target 28 October); supervisor co-signs.
- [ ] **Step 2:** On the existing EDEN account, check partitions, time limits, quotas and compute-node internet; pre-download models on the login node.
- [ ] **Step 3:** Write to the dataset authors: may id-list and qrel releases and EDEN storage be used; what do the timestamps mean.
- [ ] **Step 4:** Obtain the supervisor's answers to the questions in section 12 (co-signing, ethics statement, grading weights).

### Task 1: Dated corpus and first checks (W1)

**Files:** loaders under `src/temporal_fact_checked_retrieval_eval/dataset/`, dataset config, tests on a synthetic fixture.

- [ ] **Step 1:** Loaders for posts, fact-checks and pairs; earliest-instance timestamps with the interval bounds of section 5; drop and report undated posts.
- [ ] **Step 1b:** Merge MultiClaim v1, v2 and SemEval data: map ids across the releases, deduplicate posts and fact-checks by normalised text (Unicode normalisation, lowercase, whitespace and URL stripping, hash), keep a provenance column, prefer v2 records, reconcile language labels, report the count lost per language, and keep SemEval test posts out of any training data.
- [ ] **Step 2:** Answerable rate per language and relationship type at margins 0, 1 and 7 days, **before any model run**.
- [ ] **Step 3:** Check 30 Polish and 30 English dates against live URLs, then 100 per language; share of mixed earlier-and-later gold; posts per gold fact-check (design effect for the bootstrap); Polish pair mix by outlet and relationship type.
- [ ] **Step 4:** Restate power and minimum detectable effects with measured numbers.

### Task 2: Protocols and shared split (W1)

- [ ] **Step 1:** Strict causal pool and answerability flag; property tests (no pool item dated after the post).
- [ ] **Step 2:** Size-matched control; delayed-query variant; chronological training split.
- [ ] **Step 3:** Dataset-agnostic protocol module: all protocols read a small adapter (posts, fact-checks, gold pairs, timestamps with instance intervals), so any dated corpus, a second dataset or a newer fact-check dump, is processed by re-running the module with a new cutoff and no code changes; test it with a synthetic corpus and with MultiClaim.
- [ ] **Step 4:** Write the formal definition of causal evaluation for retrieval over a growing archive (pool P(q), answerability, the protocols as operators on the pool) and its properties, each with a proof sketch and a test: pools are monotone in the cutoff; the unconditional strict-causal Success@k is bounded by the answerable rate; the size-matched control has the same pool size as the causal pool; the additive chain telescopes to the total gap.
- [ ] **Step 5:** Freeze the split format (ids, cutoffs, qrels) and the one results schema by 25 November.

### Task 3: Core systems (W2, W3)

- [ ] **Step 1:** BM25 with per-query causal statistics, prototype on 1,000 queries; fall back to monthly rolling statistics if exact per-query statistics are too slow.
- [ ] **Step 2:** multilingual-e5-large and the Polish or cross-lingual encoder: encode the pool once, apply time masks at search time.
- [ ] **Step 3:** bge-reranker-v2-m3 on the top 100.
- [ ] **Step 4:** Run all protocols for Polish and English on EDEN; write rows to the shared table.

### Task 4: Core analysis (W4)

- [ ] **Step 1:** Cluster bootstrap, Holm, difference-in-differences; unconditional and conditional tables separately.
- [ ] **Step 1b:** Ranking-reversal check (RQ6): rank the systems under the random and the causal protocol, report Kendall tau with a bootstrap interval, every pairwise reversal with its significance, and whether the best system changes; this result decides the publication target (section 10).
- [ ] **Step 2:** Additive gap chain with order shuffling; covariate regression.
- [ ] **Step 3:** Code the 50 failing queries with two annotators; report kappa.

### Task 5: Extended tier (only after the core is complete)

- [ ] **Step 1:** Polish sibling qrels with the validated judge panel; fact-checker-only qrels reported next to expanded ones.
- [ ] **Step 2:** Added languages and the dose-response mixed model (with v2).
- [ ] **Step 3:** Second dated dataset: identify a corpus with dated posts and fact-checks whose terms allow our use (candidates to check: the Snopes-based CheckThat! claim-matching data and CrowdChecked), build its causal split with the same protocol module and repeat the ranking-reversal check.
- [ ] **Step 4:** Recovery analysis: on MultiClaim (and the second dataset if built), test whether time-aware negatives or a recency-aware rerank recovers the lost performance; reported as an analysis, not a new method.
- [ ] **Step 5:** Fine-tuned retriever under random and chronological training with the same test set.
- [ ] **Step 6:** LLM-scale systems and RQ5 with the model set of section 7.

### Task 6: Release and paper (W5)

- [ ] **Step 1:** Check the release against the access terms; ids, judged ids, prompts and code only; write the licence table (datasets, models, tools).
- [ ] **Step 2:** Write the paper from the shared table and the released code.

## 10. Timeline and decision gates

About 10 usable supervisor Wednesdays remain (estimate) to the end of January 2027 (11 November and 6 January are public holidays; 23 and 30 December are likely breaks).

| Gate | When | Rule |
|---|---|---|
| Data access | 18 Nov | no data access by then: switch to a protocol-and-code deliverable on whatever record arrived and tell the supervisor |
| Split and schema frozen | 25 Nov | ids, cutoffs, qrels format, one results schema |
| Answerability check | first data week | Polish strict-causal answerable at least 150: keep the Polish-English difference-in-differences as headline; 50 to 149: report it as descriptive with intervals; below 50: the headline becomes answerability and time-to-findability, Polish as a case study |
| Core complete | 16 Dec | 4 systems x 3 protocols x 2 languages in one table with cluster-bootstrap intervals; otherwise all extended work stops |
| Extended unlock | after core | at least 4 Wednesdays left; order as in section 4 |
| Venue decision | after the ranking-reversal check | significant reversals or a changed best system: aim at an A* main track and unlock the second dataset first; otherwise target ARR Findings or SIGIR short (section 15) |

## 11. Deliverables

- Split definitions as id lists plus code that rebuilds them from the official files; no post text.
- The shared results table: at least four systems under the random and the temporal protocol, Polish and English, with significance tests; the central number is how much more the temporal split costs Polish.
- The ranking-reversal analysis (RQ6), the gap decomposition and the coded analysis of 50 newly failing queries.
- Extended tier, if unlocked: judged sibling ids, released prompts, model hashes and response-cache index, dose-response analysis.
- A paper written from the shared table.

## 12. Decisions requested from the supervisor

1. Will you co-sign the Zenodo access requests from a pw.edu.pl address?
2. Does the faculty need an ethics statement or data-management note for restricted social-media data?
3. How will the project be graded: how much weight falls on the manual analysis of 50 failing queries compared with the results table, so that we can plan our effort accordingly?

## 13. Main risks and mitigations

The full register has 26 risks with checks and stop/go gates (Risk register). The ones that can reshape the project:
- **Answerability unknown:** no source reports how many MultiClaim pairs have the fact-check before the post; measured first (Task 1), headline adapts (section 10).
- **Near-tautological headline:** on queries with the same gold under both protocols only distractors are removed; the plan reports answerability and ranking separately and scores the chain unconditionally on one query set.
- **Access terms:** the Zenodo terms forbid sharing beyond named requesters; handled by naming everyone in one request, local open-weight models only, and written confirmation of what may be released.
- **Scope:** the plan exceeds a course project; the core tier equals the brief and everything else is gated.
- **Confounded Polish result:** the larger Polish penalty may reflect how pairs were collected (ClaimReview links, Meta warnings, backlinks), not a thin archive; the answerable rate and penalty are reported by relationship type and outlet group, aggregate only, and the Polish result is descriptive unless the within-language slope supports a mechanism.
- **Single-LLM dependence:** several families with stated cutoffs, open-data models, a disjoint judge panel and human validation (section 7).
- **Novelty:** time-respecting evaluation (TREC 2011 Microblog), chronological PFCR splits (Shaar et al., Findings NAACL 2022), out-of-time PFCR test posts (SemEval-2025 Task 7) and the dataset authors' post-newer/older analysis exist; the claim is limited to the per-query date-restricted index, the answerability vs ranking separation, the size-matched control, statistics leakage, sibling qrels, time-to-findability and the decomposition. No published date-restricted PFCR evaluation was found in searches on 27 October 2026; searches repeat monthly.

## 14. Novelty position

- **Not new:** time-respecting retrieval evaluation (TREC 2011 Microblog), chronological train/test splits for PFCR (Shaar et al. 2022, English debates), out-of-time PFCR test posts (SemEval-2025 Task 7), MultiClaim's post-newer/older and pool-size analyses, language-bias analysis (Vykopal et al., EACL 2026).
- **New:** a per-query date-restricted fact-check index for PFCR, answerability separated from ranking, a pool-size control matched to the time-restricted pool, statistics leakage for PFCR, sibling qrels, time-to-findability, the additive gap decomposition and, in the extended tier, the archive-density mechanism test.
- **Venues:** see section 15; a CLEF temporal PFCR task proposal for 2028 at the earliest.

## 15. Publication strategy

- **Target:** an A* main track (ACL, EMNLP or NAACL through ACL Rolling Review, or SIGIR full paper). No workshops. Fallbacks if the result is smaller: ARR Findings, SIGIR short paper or ECIR.
- **Assessment:** as a single-dataset audit the paper is a solid Findings or SIGIR-short candidate; reviewers may call "index only earlier fact-checks" obvious, and on queries with unchanged gold the filter only removes distractors. An A* attempt needs a consequence, which the plan builds in as follows.
- **What the paper needs and where the plan provides it:**
  1. System rankings change: RQ6 and the ranking-reversal check (Task 4, core, costs almost nothing extra).
  2. The effect generalises: a formal, dataset-agnostic protocol (Task 2 steps 3 and 4) plus a second dated dataset (Task 5 step 3), framed as a general causal-evaluation protocol for retrieval over a growing archive.
  3. A mechanism: the archive-density dose-response across seven languages (extended tier).
  4. A consequence for practice: the recovery analysis (Task 5 step 4).
  5. A resource: the time-masked split released as id lists and code, rebuildable for a newer fact-check dump or another dated corpus by re-running the dataset-agnostic module (Task 2 step 3).
- **Decision rule:** after the core and the ranking-reversal check, aim at an A* venue only if reversals are significant or the best system changes and the answerable-rate gate holds; then unlock the second dataset before other extended work. Otherwise target Findings or SIGIR short.
- **Timing:** ARR 4 January 2027 and SIGIR 21 January 2027 are not realistic for an A* attempt with about ten supervisor Wednesdays left; aim at the next ARR cycle after the course, with the deadline checked at that time.
- **Claims to avoid:** anything the novelty position lists as not new; no claim that leakage is removed or that Polish is special without the within-language evidence.
