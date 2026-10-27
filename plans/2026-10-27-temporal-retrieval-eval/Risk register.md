---
title: "Risk register"
type: plan-note
domain: vault
parent: "[[2026-10-27-temporal-retrieval-eval]]"
created: 2026-10-27
updated: 2026-10-27
tags: [risks, methodology, data-access, ethics, timeline]
related:
  - "[[Original Task]]"
  - "[[2026-10-27-temporal-retrieval-eval|Project plan]]"
  - "[[Topic research]]"
  - "[[Language scope]]"
  - "[[Literature corrections]]"
  - "[[Research]]"
  - "[[MultiClaim]]"
  - "[[MultiClaim Zenodo Records]]"
  - "[[SemEval-2025 Task 7]]"
  - "[[MultiClaimNet]]"
  - "[[Role of Context in PFCR]]"
  - "[[Language and Retrieval Bias]]"
  - "[[Qwen3 Embedding]]"
  - "[[polish-reranker-roberta-v3]]"
  - "[[compute]]"
  - "[[EDEN access and networking]]"
---
# Risk register

Status: draft

**Goal:** list every risk that can kill, shrink or invalidate the project in [[2026-10-27-temporal-retrieval-eval|Project plan]], with the cheapest test for each and the point at which to cut scope.

**Architecture:** register of risks scored by judgment (likelihood and impact are the author's estimates, not measurements), then ordered checks, stop/go gates and supervisor questions.

**Tech Stack:** none; web checks done on 2026-10-27 (sources under References), no data access yet, so every dataset number below is from papers or records.

## Summary

- **R1 Answerability may be tiny and unknown.** No source reports the share of [[MultiClaim]] pairs where the fact-check predates the post; the paper's leak test gives only scores (80.02 vs 80.04), not group sizes. The plan's answerable rates (0.3, 0.5) are guesses; if the real rate is about 0.1, Polish keeps roughly 45 (v1) to 130 (v2) answerable queries and the headline Polish-English contrast is unpowered.
- **R2 The headline number risks being near-tautological, and H2 is logically weak.** On queries answerable under both protocols the gold is the same earlier fact-check; the causal pool only removes later distractors, so conditional scores should rise, not fall. Most of the "random vs causal" gap is then the definition of answerability, which reviewers may call trivial; the real ranking effect sits only in queries with mixed earlier and later gold and in time-local distractor composition.
- **R3 Access terms bind the whole design.** Zenodo terms (v1, v2, SemEval-2025) require an institutional e-mail, research use only, and no re-sharing "with anyone else not included in this request". That covers the second team, EDEN group members, any commercial LLM API used for sibling judgments, and possibly the released id lists. The brief's success criterion "reproduces both evaluations from public data" cannot hold literally, since the data is not public.
- **R4 Scope far exceeds a Hard (16/25) course project with about 10 supervisor Wednesdays.** The plan has 5 RQs, 7 languages, 6 protocols, 6 system families (including an 8B LLM reranker and two fine-tuning regimes), a mixed-effects dose-response model, 400 human sibling judgments, and 50 double-annotated queries. The brief requires 4 systems × 2 protocols × 2 languages, decomposition and 50 queries.
- **R5 The Polish-vs-English DiD is confounded by collection route, not archive density.** Pairs come from ClaimReview "reviewed item" links (post first by construction) and Meta-warning or backlink pairs (either order). The mix of routes per outlet (Demagog, AFP, Snopes) sets the answerable rate per language, so a larger Polish penalty may reflect how Polish pairs were collected. Demagog and oko.press also check politicians' statements more than social posts.

## Register

Likelihood (L) and impact (I): H/M/L, author's judgment. Plan status: whether the current plan note already contains the mitigation (addressed), only part of it (partly), or not (open). Owner: the team member named at kickoff for the workstream; trigger: the event that activates the mitigation.

| id | risk | category | L | I | evidence or source | mitigation | owner/trigger | plan status |
|---|---|---|---|---|---|---|---|---|
| R1 | Strict-causal answerable rate far below the assumed 0.3-0.5 | statistics, validity | H | H | MultiClaim reports no share of post-newer pairs (arXiv 2305.07991v2, leak test); H1 of [[Topic research]] itself predicts most pairs are post-first | Compute answerable rate per language and per relationship type on day 1 of access, before any model run; restate MDE; if Polish answerable < 150, make answerability (not ranking) the headline | W1; trigger: first data load | addressed: Task 1 step 2 and answerability gate |
| R2 | Conditional causal score rises (fewer distractors), so "penalty on answerable queries" is absent or reversed; H2 unsupported | research validity | H | H | Gold set unchanged for all-earlier-gold queries; only distractors removed; MultiClaim pool sweep shows pool size changes scores | Re-state H2 as "time-local distractors are harder than random ones" (causal vs size-matched random); split answerable queries into all-earlier-gold vs mixed-gold; pre-register that a null or positive conditional delta is a finding | W4; trigger: protocol spec review | addressed: restated hypothesis, unconditional chain |
| R3 | Re-sharing clause: second team, EDEN group, LLM APIs, id-list release | legal, access | H | H | Zenodo records 7737983, 15413169, 14989176, term 3; term 1 (institutional e-mail) | Name every team member in one request from pw.edu.pl addresses; store data in a directory readable only by named people; local open-weight LLMs only (no API); ask KInIT in writing whether id lists and qrels may be released | Team lead; trigger: before the request is sent | partly: Task 0 and section 8; waits for the dataset authors' answer |
| R4 | Effort exceeds a course project; deliverables slip | scope, timeline | H | H | Brief vs plan (see Summary R4); 10 usable Wednesdays to 27 Jan 2027 (11 Nov and 6 Jan are public holidays, 23 and 30 Dec likely break) | Freeze a core: brief scope only (pl, en; BM25, mE5, mmlw or LaBSE, bge-reranker-v2-m3; random, strict causal, size-matched; chain; 50 queries). Everything else is a stretch tier unlocked only by the gates below | Team; trigger: kickoff | addressed: core and extended tiers, gates |
| R5 | DiD confounded by collection route, outlet practice, topic and platform mix | methodology | H | M | [[MultiClaim]] collection routes; v2 `relationship` undefined ([[MultiClaim Zenodo Records]]); [[Language scope]] admits n = 2 has zero df | Report answerable rate and penalty by relationship type and outlet group (aggregate only); stratify or reweight DiD by route; phrase the Polish result as descriptive unless the within-language slope supports a mechanism | W4; trigger: R1 numbers | addressed: reported by relationship type; descriptive unless slope supports it |
| R6 | Data access delayed or refused (no reply, non-institutional address, v2 refused) | access | M | H | Requests are manual; brief marks data "READY" although no request has gone out; maintainer's contact address is not institutional | Send v1, v2 and SemEval requests on 28 Oct from pw.edu.pl addresses; supervisor co-signs; fallback plan for a protocol-only demo on SemEval data if only one record arrives | Team lead; trigger: no reply by 11 Nov | addressed: Task 0 step 1 and 18 Nov gate |
| R7 | Timestamps are crawl, update or ClaimReview dates, not publication; time zone unknown | data, validity | M | H | Neither record defines timestamp semantics; MultiClaim paper does not say how post dates were obtained; 1,755 of 28,092 v1 posts lack dates | 100 URL checks per language (plan); report lag-sign flips at 0, ±1, ±7 days; drop same-day pairs as a sensitivity run; ask KInIT | W1; trigger: > 10% of checked dates off by > 1 day | addressed: Task 1 step 3, margins 0, 1, 7 |
| R8 | "Earliest instance" for a fact-check picks a republication in another outlet or language | data | M | M | v1/v2 `instances` is a list per fact-check | Report earliest-instance vs first-listed-instance runs; flag multi-outlet fact-checks | W1; trigger: share of multi-instance fact-checks > 5% | open |
| R9 | Sibling qrels biased: judged pool comes from the evaluated systems, labels added only for the causal protocol, LLM judge has parametric knowledge | methodology | H | H | MultiClaim found 719 valid pairs where data had 96 (7x incompleteness affects both protocols); pooling bias is standard IR knowledge | Expand labels symmetrically for both protocols or report expanded results as a bound only; pool includes BM25; 200+200 human checks give a kappa interval about ±0.1, so report it; keep strict qrels as primary | W3/W4; trigger: before any expanded number is reported | addressed: expanded qrels reported as a bound only |
| R10 | Additive chain not additive: steps switch between conditional (answerable) and unconditional query sets | statistics | H | M | Chain in [[2026-10-27-temporal-retrieval-eval\|Project plan]] mixes "strict causal answerable" and "all queries" | Score every step unconditionally on one fixed query set (unanswerable = miss); give conditional scores in a separate table; Shapley averaging over orders as planned | W4; trigger: protocol spec review | addressed: chain scored unconditionally on one query set |
| R11 | Bootstrap over queries ignores clustering (many posts share one fact-check or [[MultiClaimNet]] cluster), so CIs are too narrow | statistics | H | M | MultiClaim: COVID near-duplicates; posts per claim > 1 by design | Cluster bootstrap by gold fact-check or cluster id; report effective n; recompute power with the design effect | W4; trigger: first CI computation | addressed: cluster bootstrap |
| R12 | Power analysis rests on assumed d and a, and conflates pairs with posts (v2 n = 1,309 is Ramponi et al. subset mono pairs) | statistics | H | M | [[Language scope]] power table assumptions | Recompute with real n, a, d and clustering after first run; at a = 0.1 and n = 450 the paired MDE is about 0.09-0.13 (n = 100-150, d = 0.1-0.2) | W4; trigger: R1 numbers | addressed: power restated after the first data load |
| R13 | Prior or concurrent date-restricted PFCR evaluation (scooping) | novelty | M | H | Searches on 2026-10-27 (arXiv, ACL Anthology, web) found none; closest remain [[Role of Context in PFCR]] and [[Generative-AI Claim Retrieval]] date filter; KInIT holds v2, timestamps and an active PFCR line ([[Language and Retrieval Bias]], EACL 2026) | Re-search monthly (arXiv cs.CL/cs.IR, ACL Anthology, SIGIR/ECIR); contact KInIT early, framed as a complement; claim only the decomposition and protocol | W5; trigger: monthly search | partly: monthly re-search in section 13 |
| R14 | Novelty judged thin ("filtering by date is obvious", TREC 2011 Microblog precedent) | publication | M | M | [[Research]] "Not claimable" list | Lead with the decomposition and the answerability vs ranking split; venue target workshop (FEVER, NLP4PI) first, ARR only if R2 shows a ranking effect | W5; trigger: results of R2 | addressed: novelty claim narrowed, workshop first |
| R15 | Parametric leakage RQ5 not identifiable: Qwen3 training cutoff unstated, v2 posts end before April 2025, Qwen3 released 2025 | methodology | H | M | [[Qwen3 Embedding]] note; Qwen3 cards give no cutoff; [[Simulated Ignorance Fails]] | Drop RQ5 from the core; keep as exploratory only if a model with a documented cutoff before most posts is used | W3; trigger: kickoff | addressed: RQ5 is stretch, documented cutoffs only |
| R16 | Time-to-findability conditioned on eventually-debunked posts (every post has a fact-check by construction); not a deployment estimate | validity | H | M | MultiClaim collects only posts linked to fact-checks | Name it "time-to-findability among debunked posts"; right-censor at dataset end; no deployment claims | W4; trigger: write-up | addressed: named time-to-findability among debunked posts |
| R17 | Chronological fine-tuning confounds training leakage with topic drift; test period concentrates in late data | methodology | M | M | [[Role of Context in PFCR]] did not separate drift from leakage | Same test set for both regimes; random regime excludes test-period pairs and near-duplicates; stretch tier only | W3; trigger: stretch gate | addressed: same test set for both regimes |
| R18 | Merging v1, v2 and SemEval: id spaces, duplicates, different language labels | data | M | M | v2 carries v1-format copies; SemEval test posts to March 2024, pool to May 2024; overlap unknown | Dedupe by normalised text plus id mapping; report counts lost; start with one source if mapping is unclear | W1; trigger: first merge | open |
| R19 | GDPR and re-identification: anonymised post text is still personal data if searchable; named outlets and journalists | ethics, legal | M | M | v2 record: users can request removal; Zenodo term 2; brief's ethics rule | No verbatim post quotes; paraphrase examples; aggregate errors; delete data at project end; ask supervisor whether the faculty needs an ethics statement | Team lead; trigger: before annotation | partly: data deleted at project end; ethics question to lecturer |
| R20 | Licences: MultiClaim code is GPL-3.0 while the repo is Apache-2.0; polish-reranker-roberta-v3 under the gemma licence | software, legal | M | L | GitHub kinit-sk/multiclaim (GPL-3.0); HF cards: bge-m3 and multilingual-e5-large MIT, Qwen3-Embedding-8B, Qwen3-Reranker-8B, bge-reranker-v2-m3, mmlw-retrieval-roberta-large, LaBSE Apache-2.0, polish-reranker-roberta-v3 gemma | Do not copy MultiClaim code (reimplement or keep it outside the repo); do not redistribute weights; cite licences in the paper | W5; trigger: first code import | open |
| R21 | EDEN partition limits, compute-node internet and quotas unknown | compute | M | M | [[EDEN access and networking]]: partition limits and quotas unpublished; offline compute nodes unverified; the account already exists | Check limits on the login node; pre-download models there; keep the core runnable on one A100 40 GB (8B models need bf16 and batch care) | Team lead; trigger: first job fails on limits | reduced: account exists; limits still to check (Task 0 step 2) |
| R22 | BM25 with per-query causal statistics needs custom code; no library supports per-query IDF | software | M | M | Plan's cumulative-df design; Pyserini needs Java and fixed index statistics | Implement on a sparse term-doc matrix with cumulative df by date; unit-test against bm25s on a full pool; fall back to monthly rolling indices | W2; trigger: week 1 of W2 | addressed: Task 3 step 1 prototype and fallback |
| R23 | Repo not ready: no retrieval dependencies, empty dataset/models packages, README points to a missing `knowledge/handbook/Proposed Task.md`, report template is `Interspeech.cls` | reproducibility, process | H | L | `pyproject.toml`, `src/`, `README.md`, `report/` as of 2026-10-27; the plan file carries title "Proposed Task" and type handbook | Fix links and template before writing; add torch, sentence-transformers, bm25s with justifications; seed and log every run in MLflow | W5; trigger: first PR | partly: README link fixed; dependencies and report template open |
| R24 | Two-team split: the plan absorbs both brief slots; if a second team is assigned, interfaces and shared split must be agreed | team, process | M | M | [[Original Task]]: max 2 teams, one shared split and one results table | Agree at the first Wednesday who owns what; freeze split format (ids, cutoffs, qrels) by 25 Nov; one results schema | Team; trigger: 28 Oct meeting | addressed: one plan, freeze on 25 Nov |
| R25 | Supervisor bottleneck: Wednesday-only access; decisions (language scope, scope cuts, access terms) wait a week each | process | H | M | [[Original Task]] availability | Batch questions (below) into each Wednesday; default decisions written down in advance and applied if no answer | Team lead; trigger: weekly | partly: questions batched in section 12 |
| R26 | Language-scope expansion read as the out-of-scope language-bias study | scope | M | M | [[Language and Retrieval Bias]]; brief excludes language-bias analysis | Keep option B as stretch only, gated on v2 access; within-language deltas only | Team; trigger: v2 access | addressed: extended tier and reporting rules |
| R27 | Narrative-drift LLM labels unvalidated or drifting with prompt changes | methodology | M | L | Plan validates on "a human sample" of unstated size | Fix prompt and model version; validate on ≥ 100 items; treat as covariate only | W4; trigger: stretch gate | partly: judge validation against humans |
| R28 | Multimodal-only posts (13 of 100 in MultiClaim audit) inflate failures | data | M | L | [[MultiClaim]] noise audit | Code them in the 50-query analysis; sensitivity run excluding OCR-only posts | W4; trigger: failure analysis | addressed: multimodal-only in the failure codebook |

## Assumptions to test first

Ordered by cost; each can kill or reshape the project.

1. **Access terms permit the design** (cost: one e-mail, 28 Oct). Ask KInIT whether a second team, id-list and qrel releases, and EDEN storage are allowed. A "no" on releases turns the "released split" deliverable into "code that rebuilds the split".
2. **Answerable rate per language** (cost: one hour after data arrives). Count pairs with t_fc < t_post at margins 0, 1 and 7 days, by language and relationship type. If Polish answerable < 150, drop the DiD as headline and lead with answerability.
3. **Timestamp sanity** (cost: half a day). Check 30 Polish and 30 English dates against live URLs before the planned 100. More than 10% off by over a day makes day-level causal pools unreliable.
4. **Same gold under both protocols** (cost: one hour). Share of answerable queries with mixed earlier and later gold. If near zero, conditional ranking effects come only from distractors (R2).
5. **Clustering** (cost: one hour). Posts per gold fact-check and per [[MultiClaimNet]] cluster; design effect for the bootstrap.
6. **Polish source mix** (cost: one hour). Share of Polish pairs by outlet and relationship type vs English (R5).
7. **BM25 per-query statistics** (cost: one day). Prototype on 1,000 queries; time per query decides between exact per-query and monthly statistics.

## Stop/go criteria

- **Go/no-go 1 (18 Nov):** no data access → switch to a protocol-and-code deliverable on whatever record arrived, and tell the supervisor.
- **Go/no-go 2 (first data week):** Polish strict-causal answerable ≥ 150 → keep the DiD headline; 50-149 → report DiD with CIs as descriptive; < 50 → headline becomes answerability and time-to-findability, Polish as a case study.
- **Core complete (16 Dec):** 4 systems × 3 protocols × 2 languages in one table with cluster-bootstrap CIs. If not done, all stretch work stops.
- **Stretch unlock:** core complete and ≥ 4 Wednesdays left → add in this order: sibling qrels (Polish), more languages (with v2 access), fine-tuning regimes. LLM reranker and RQ5 only with a documented model cutoff.
- **Publication go (mid-January):** pursue ARR (4 Jan 2027 deadline is not realistic) or SIGIR short (21 Jan 2027) only if R2 shows a non-trivial ranking effect; otherwise target a 2027 workshop.

## Open questions for the supervisor

- Will you co-sign the Zenodo access requests from a pw.edu.pl address?
- Does the faculty need an ethics statement or data-management note for restricted social-media data?
- Is a paper submission expected, and does a course deadline in late January conflict with ARR or SIGIR timing?
- Which grading weight falls on the 50-query manual analysis vs the results table?

## References

- MultiClaim v1 record and access terms: https://zenodo.org/records/7737983
- MultiClaim v2 record, terms, removal procedure: https://zenodo.org/records/15413169
- SemEval-2025 Task 7 data record and terms: https://zenodo.org/records/14989176
- MultiClaim code (GPL-3.0): https://github.com/kinit-sk/multiclaim
- MultiClaim paper (leak test, dated posts N = 26,337): https://arxiv.org/html/2305.07991v2
- Model licences: https://huggingface.co/BAAI/bge-m3 ; https://huggingface.co/intfloat/multilingual-e5-large ; https://huggingface.co/Qwen/Qwen3-Embedding-8B ; https://huggingface.co/Qwen/Qwen3-Reranker-8B ; https://huggingface.co/BAAI/bge-reranker-v2-m3 ; https://huggingface.co/sdadas/mmlw-retrieval-roberta-large ; https://huggingface.co/sdadas/polish-reranker-roberta-v3 ; https://huggingface.co/sentence-transformers/LaBSE
- Prior-work search, closest temporal-leakage work: https://aclanthology.org/2026.acl-short.65/ ; https://arxiv.org/abs/2504.20668 ; https://aclanthology.org/2026.eacl-long.240/
- CheckThat! 2026 (no PFCR task): https://arxiv.org/abs/2602.09516
- Meta ended US third-party fact-checking on 7 April 2025 (affects posts collected via Meta warnings after that date): https://www.fox5atlanta.com/news/meta-ends-us-fact-checking-2025
- ACL 2027 call (ARR 4 January 2027): https://2027.aclweb.org/calls/main/ ; SIGIR 2027: https://sigir2027.org/
