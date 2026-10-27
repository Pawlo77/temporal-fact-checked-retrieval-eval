---
title: "Expansion options"
type: plan-note
domain: vault
parent: "[[2026-10-27-temporal-retrieval-eval]]"
tags: [expansion, novelty, methodology, answerability, recency, leakage, cross-lingual, conformal, effort]
created: 2026-10-27
updated: 2026-10-27
related:
  - "[[2026-10-27-temporal-retrieval-eval]]"
  - "[[Topic research]]"
  - "[[Language scope]]"
  - "[[LLM selection]]"
  - "[[Risk register]]"
  - "[[Research]]"
  - "[[Course grading and report]]"
---
# Expansion options

Scope decision, agreed: keep the temporal PFCR idea and expand it to make it more interesting for a reader. No second paper, no pivot to narrative-drift modelling, no new retrieval architecture. Tier 3 from the earlier sweep (a narrative-drift annotation paper) is dropped; Tier 1 and Tier 2 below are candidate expansions of this one project.

## How to read this

Each direction answers the same questions: what it is, what it builds on, what we must build, new model training (yes or no), new data or preparation, effort (engineer-days and GPU), main risk, and a verdict. Effort is an estimate, not a measurement, in the spirit of [[compute]] ([V] verified, [U] estimate).

## Decision criteria (shared)

- Adds a measured, publishable result, not a promise of one.
- No new retrieval model training (the fine-tuned retriever in the plan is the only planned training and is orthogonal).
- Reuses the shared split, the one results schema, and the stored run files.
- Priced in engineer-days and GPU-hours against a 3-4 person team with about ten supervisor Wednesdays.

## What already exists in the plan (to avoid double-counting)

- The strict causal pool and the answerability flag are core, not an expansion.
- The size-matched random control is core.
- RQ5 (LLM reranker parametric leakage) is planned; Direction E sharpens it, it does not add it.
- The dataset-agnostic protocol module is planned (Task 2 steps 3-4); the datasets section below makes it concrete.

## Tier 1 — strengthen the core

### A. Continuous time-decay ablation

**What it is.** Replace the binary "causal vs random" comparison with a single family of time weights over the full pool, swept over a strength parameter. A weight `w(t_f, t_q)` that is 1 for `t_f < t_q` and 0 otherwise is the causal index; a soft exponential decay over age interpolates to "no temporal signal" at one end. Report Survived Success@10 and MRR as a curve over decay strength, per system and language, instead of one number per protocol.

**What it builds on.** [Efron & Golovchinsky, SIGIR 2011](https://doi.org/10.1145/2009916.2009984) (time as a document prior with graceful degradation); [Grofsky 2025](https://arxiv.org/abs/2509.19376) (freshness must enter candidate selection, not only re-ranking); [TempRetriever, SIGIR 2025](https://arxiv.org/abs/2502.21024) (learned temporal fusion, the strongest learned baseline); [ColDeR, ACL 2025](https://aclanthology.org/2025.acl-long.447/) (dense-retriever brevity/position bias to control for).

**What we must build.** A `temporal_decay.py` re-scorer over stored run files: apply `score * exp(-lambda * age)` (or a rank-based equivalent) to existing BM25 and dense scores, sweep a lambda grid, emit one curve per cell. No re-encoding.

**New models to train.** None.

**New data or preparation.** None; publication dates are already required for the causal split.

**Effort.** About 1 engineer-day, no GPU. Low risk; the only care is keeping the soft-decay and hard-cutoff families reported separately so the curve is honest.

**Verdict.** Adopt. Near-free, and it turns the headline into a curve that a reviewer reads as a finding rather than an audit.

### B. Answerability as a first-class axis

**What it is.** Report conditional and unconditional Success@10/MRR separately (unanswerable queries counted as misses vs excluded), and add a selective-retrieval view: a system can abstain, and we plot (coverage, Success@10) by sweeping an abstention threshold on a confidence signal. This decomposes the causal drop into answerability loss (the gold does not exist yet, the system should abstain) and ranking loss (the gold exists but ranks low).

**What it builds on.** [Geifman & El-Yaniv 2017](https://arxiv.org/abs/1705.08500) (selective prediction and risk-coverage curves); [Kamath et al., ACL 2020](https://aclanthology.org/2020.acl-main.503/) (selective QA under distribution shift); [UAEval4RAG, ACL 2025](https://aclanthology.org/2025.acl-long.415/) (unanswered/acceptable-ratio metrics); [SQuAD 2.0, ACL 2018](https://aclanthology.org/P18-2124/) (answerability as a first-class label).

**What we must build.** The answerability flag already exists. Add a threshold sweep over a per-query confidence signal (top retrieval score or the BM25 max score) to produce risk-coverage curves, plus the conditional/unconditional table. No learned abstainer; a logistic re-scoring on retrieval features is possible later but not required.

**New models to train.** None (threshold-based abstention).

**New data or preparation.** None.

**Effort.** About 1 engineer-day, no GPU. Low risk.

**Verdict.** Adopt. This is the single cheapest rebuttal to "the idea is too simple": it replaces one number with a two-way decomposition and a curve.

### C. A rigorous statistical frame

**What it is.** Three parts: (1) state the gap as a paired off-policy difference between two index regimes and estimate it with the paired/cluster bootstrap we already run, leading with effect sizes rather than p-values; (2) replace the plain Polish-English difference-in-differences with synthetic difference-in-differences; (3) report Holm-corrected intervals and effect sizes for every headline comparison.

**What it builds on.** [Joachims & Swaminathan, SIGIR 2016](https://doi.org/10.1145/2911451.2914803) (counterfactual evaluation of rankers); [Delta-OPE, RecSys 2024](https://doi.org/10.1145/3640457.3688162) (estimate the pairwise policy difference directly); [Arkhangelsky et al., AER 2021](https://doi.org/10.1257/aer.20190159) (synthetic difference-in-differences); [Urbano et al., SIGIR 2019](https://doi.org/10.1145/3331184.3331259) (which IR significance tests actually work); [Ihemelandu & Ekstrand, SIGIR 2023](https://doi.org/10.1145/3539618.3592004) (effect size, not p-value, at scale).

**What we must build.** Parts 1 and 3 are mostly re-labelling plus a variance-reduced paired estimator (the paired bootstrap already estimates the same quantity); effectively writing, not code. Part 2 is a small implementation of synthetic difference-in-differences (statsmodels gives DiD; synthetic controls need a manual or `synthdid`-style port).

**New models to train.** None.

**New data or preparation.** None.

**Effort.** Parts 1 and 3: about 0.5 engineer-day. Part 2: about 2-3 engineer-days, and it is weak here because we have two units (Polish, English); synthetic-DiD pays off only if the extended language set is added. Split the verdict.

**Verdict.** Adopt parts 1 and 3 now; defer part 2 (synthetic-DiD) unless the extended language set is unlocked, otherwise it is under-powered and not worth the days.

## Tier 2 — add a niche axis

### D. Conformal time-respecting retrieval

**What it is.** Wrap the causal retriever in split-conformal risk control so it emits a candidate set with a stated probability of containing the gold fact-check, and abstains when no set meets the threshold. A time-conditional variant calibrates the guarantee per fact-check-lag bucket so the coverage claim holds where the index is weakest.

**What it builds on.** [Bates et al., JACM 2021](https://arxiv.org/abs/2101.02703) (risk-controlling prediction sets); [Angelopoulos et al., ICLR 2024](https://arxiv.org/abs/2208.02814) (conformal risk control); [C-RAG, ICML 2024](https://arxiv.org/abs/2402.03181) (conformal RAG under distribution shift); [Conformal-RAG, SIGIR 2025](https://arxiv.org/abs/2506.20978) (group-conditional coverage); [Two-stage risk control 2024](https://arxiv.org/abs/2404.17769) (retrieval and ranking risk controlled separately).

**What we must build.** A calibration split (chronological, held out from test), a nonconformity score (one minus the normalised score of the gold, or rank-based), set construction with abstention, and the time-conditional calibration. All post-hoc over stored scores; no new encoding.

**New models to train.** None.

**New data or preparation.** Yes, one protocol change: a chronological calibration split disjoint from the test set.

**Effort.** About 3-5 engineer-days, CPU only. The guarantee is easy to get subtly wrong, so it needs careful tests.

**Main risk.** Conformal guarantees assume exchangeability; temporal data violates it, so on a growing archive the guarantee is not exact. We would report empirical coverage, not a hard guarantee, which weakens the headline. This is the highest-value, highest-effort, most correctness-sensitive option.

**Verdict.** Maybe. Decide only after A, B, C land and we see the measured answerability rate; the risk is that the "guarantee" claim becomes "empirical coverage", which is less of a differentiator.

### E. Parametric leakage, measured properly (sharpen RQ5)

**What it is.** Four refinements to the planned RQ5: (1) estimate per-source effective knowledge cutoffs (Polish vs English fact-check sites differ) instead of assuming one cutoff; (2) classify each leaked pair as direct (the fact-check states the answer) vs causally-related (the reranker must infer it), which is where parametric leakage is hardest; (3) a prompted-cutoff ablation ("ignore anything after YYYY-MM-DD") on the LLM rerankers; (4) a cutoff-stratified control using the models already listed with different documented cutoffs.

**What it builds on.** [Dated Data 2024](https://arxiv.org/abs/2403.12958) (effective cutoffs diverge from reported); [Gao et al., EMNLP 2025](https://arxiv.org/abs/2510.02340) (prompted cutoffs fail on causally-related knowledge); [TiMaGPT, Findings NAACL 2024](https://aclanthology.org/2024.findings-naacl.208/) (dated point-in-time models); [FreshBench, NAACL 2025](https://aclanthology.org/2025.naacl-long.381/) (temporal-generalisation bias vocabulary); [Test of Time, ACL 2026](https://aclanthology.org/2026.acl-long.1693/) (post-cutoff decay is probe-sensitive).

**What we must build.** An effective-cutoff probe harness (dated fact questions per source, reusing the Dated Data method); a leakage-taxonomy prompt over (post, claim) pairs (reuses the judge-panel infrastructure); the prompted-cutoff reruns; and the cutoff-stratified model comparison.

**New models to train.** None for the cheap version. The expensive version (training TiMaGPT-style dated checkpoints) is explicitly skipped; cutoff-stratified existing models replace it.

**New data or preparation.** None beyond running the LLM rerankers the plan already budgets for.

**Effort.** Cheap version about 2-3 engineer-days plus the reranker GPU time already planned. Low-to-medium risk (the probe must hold phrasing fixed, per Test of Time).

**Verdict.** Adopt the cheap version. It converts RQ5 from a single decay number into a controlled experiment, without new training.

### F. Cross-lingual-only debunk lag

**What it is.** Add a cross-lingual causal protocol: a Polish post may match an English fact-check published before the post. Measure how much answerability recovers and the Success@10/MRR delta against the monolingual causal index, then attribute the miss rate to "an English debunk existed at query time but a Polish one did not". A language-family-distance ablation (Slavic vs Germanic) is the mechanism test but requires the extended language set.

**What it builds on.** [Quelle et al., EPJ Data Science 2025](https://doi.org/10.1140/epjds/s13688-025-00520-6) (multilingual fact-check lag and cross-lingual drift); [MMTweets 2023](https://arxiv.org/abs/2308.05680) (cross-lingual debunk retrieval); [Claim2Vec 2026](https://arxiv.org/abs/2604.09812) (defers multilingual PFCR as open); [MIRACL, TACL 2023](https://doi.org/10.1162/tacl_a_00595) (multilingual retrieval reference).

**What we must build.** A cross-lingual pool variant (all fact-checks before `t_q`, in Polish and English, or all languages), reusing the cross-lingual encoders already in the core (LaBSE, multilingual-e5, mmlw). No new models.

**New models to train.** None.

**New data or preparation.** None for the Polish-English version; the family ablation needs the extended language set.

**Effort.** Cross-lingual pool about 1-2 engineer-days. Family ablation is gated on the extended set. Low risk.

**Verdict.** Adopt the cross-lingual pool; it is self-contained with Polish and English and gives a concrete "thin archive" mechanism. Leave the family ablation to the extended tier.

## Datasets and dataset-independence

The question: can the project be more independent of MultiClaim, catch more datasets, and be a more general protocol.

**What "dataset-agnostic" means here, and what it does not.** The planned protocol module (Task 2 steps 3-4) reads a small adapter: posts, fact-checks, gold pairs, timestamps with instance intervals. Any dated claim-to-fact-check corpus is processed by re-running the module with a new cutoff and no code change. This makes the protocol independent of MultiClaim's format, but not independent of the requirement that the corpus has dated queries and dated documents with relevance labels. It generalises to other fact-checking corpora, not to arbitrary retrieval corpora.

**Dataset decision criteria.** A corpus is worth adding only if it passes all of: (1) per-item publication timestamps for both the query post and the fact-check (non-negotiable for causal evaluation); (2) gold relevance labels with dates; (3) access terms that allow our use and, ideally, id-list release; (4) it adds a genuinely new axis rather than more of the same.

**Candidate datasets.**

| Dataset | What it is | Timestamps | Labels | Languages | Adds | Fit |
|---|---|---|---|---|---|---|
| [[MultiClaim]] v1/v2 | 206k/435k fact-checks, post-to-fact-check pairs | yes | yes | 39 / more | core | primary |
| [[SemEval-2025 Task 7]] | test posts to 2024, fact-checks to mid-2024 | yes | yes | 8 + Polish/Turkish | out-of-time test | core |
| [[AMC-16K]] | 16k manually annotated pairs | yes | manual | 20 | human quality | secondary |
| [[MultiClaimNet]] | claim clusters | yes | cluster | 78 | sibling relevance | secondary |
| MMTweets | cross-lingual debunk pairs + images | yes | yes | cross-lingual | cross-lingual-only debunks | Direction F |
| CrowdChecked | claim-matching pairs | partial [unverified] | yes | EN | second dated dataset | generalisation |
| CheckThat! 2021/2022 Task 2 | Snopes/PolitiFact claim matching | partial [unverified] | yes | EN/AR | second dated dataset | generalisation |
| X-Fact | multilingual veracity | yes | veracity labels | 25 | not retrieval | skip |
| MIRACL / Mr. TyDi | multilingual retrieval | no | relevance | 18 / 11 | no timestamps | skip |
| LiveFact / ChronoQA / StreamingQA | temporal QA/evidence | yes | yes | mostly EN | generality demo, not PFCR | optional |

**Recommendation.** Keep MultiClaim v1/v2, SemEval-2025, AMC-16K and MultiClaimNet as the core. Add MMTweets if Direction F is adopted. Pick one of CrowdChecked or CheckThat! as the second dated dataset for the generalisation claim (access terms first). Do not add MIRACL, Mr. TyDi, X-Fact: they either lack timestamps or are a different task. LiveFact, ChronoQA and StreamingQA are optional demonstrations that the protocol applies beyond PFCR, not core results.

## Summary recommendation

- Adopt A + B + C(parts 1 and 3) now: about 2.5 engineer-days, no GPU, no new models, no new data.
- Adopt E (cheap) and F (cross-lingual pool) if compute allows: about 4 engineer-days more, reusing the rerankers and cross-lingual encoders already planned.
- Defer: C(part 2, synthetic-DiD) and F(family ablation) until the extended language set is unlocked; D (conformal) until A-C land and we see the answerability rate.
- Explicitly skip: TiMaGPT-style training, MIRACL/X-Fact datasets, and the Tier 3 narrative-drift paper.
