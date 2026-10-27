---
title: "Enhanced topic research"
type: handbook
domain: vault
parent: "[[temporal-fact-checked-retrieval-eval]]"
tags: [handbook, research, novelty, venues, temporal-evaluation]
created: 2026-10-27
updated: 2026-10-27
---
# Enhanced topic research

Builds on [[Original Task]]. Sources checked on 2026-10-27; every claim below carries a URL in the reference list. Counts quoted from papers are the papers' numbers, not ours; our own counts come only after the data request is granted.

## Recommended enhanced topic

### Title

**Retrieval that cannot see the future: a causal evaluation protocol for previously fact-checked claim retrieval, with answerability-aware metrics and a Polish-English contrast**

### Pitch

Previously fact-checked claim retrieval (PFCR) is scored on MultiClaim and SemEval-2025 Task 7 against a search pool that contains fact-checks published after the query post, while a fact-checker querying at post time only has the archive up to that moment. We define a causal (time-respecting) protocol, show that a naive "index only earlier fact-checks" filter conflates four effects (gold disappearing, pool shrinkage, supervised-training leakage, missing relevance labels for earlier sibling debunks), and decompose the random-vs-causal gap into those components across at least four retrieval families on Polish (thin national fact-check ecosystem) and English (control). The release is a split, cluster-expanded relevance labels for earlier debunks, and a time-to-findability metric for the deployment question "if I search for this post on day t, will the debunk be there, and how many days after posting does it become findable?".

### Research questions

- RQ1: How much of the Success@10 and MRR reported under the standard protocol survives a causal index, on answerable queries only, after controlling for pool size?
- RQ2: Which share of the random-vs-causal gap comes from (a) answerability loss, (b) pool composition, (c) training-set leakage in fine-tuned models, (d) missing labels for earlier same-claim fact-checks?
- RQ3: Is the causal penalty larger for Polish than for English, and does a thin national archive explain it (fewer earlier siblings, longer post-to-debunk lags, more cross-lingual-only earlier debunks)?
- RQ4: How long after a post does the first relevant fact-check become retrievable (time-to-findability), and how does it differ by language and system?
- RQ5: Do LLM rerankers gain from parametric knowledge of debunks published after the query (parametric temporal leakage), measured on queries before vs after model knowledge cutoffs?

### Hypotheses

- H1: Most gold pairs are post-before-fact-check, because the dataset is built from fact-checkers linking the posts they debunked; a causal index makes these queries unanswerable by their own gold.
- H2: On the answerable subset, the causal score falls below the random score once pool size is matched, because later fact-checks restate the post wording (lexical leakage) more than earlier ones do.
- H3: Pair relationship type predicts lag sign: `backlink` pairs (fact-check body links the post) are post-first by construction; `claimreview_schema` and Meta-warning pairs contain more recurring claims where the debunk is older.
- H4: The Polish causal penalty (difference-in-differences vs English) is positive and larger for lexical BM25 than for multilingual dense retrievers, because cross-lingual earlier debunks exist for viral international claims.
- H5: Fine-tuned retrievers trained on a random split lose more under causal evaluation than zero-shot retrievers, because training pairs include near-duplicates of future test claims.
- H6: Cluster-expanded labels recover a measurable share of "unanswerable" queries, so the strict causal score under-states deployable value; the true number lies between the strict and expanded scores.

### Contributions claimed

- A formal causal protocol for PFCR and a leakage taxonomy (index, answerability, training, label, parametric, timestamp leakage), with a pool-size-matched control that no prior PFCR evaluation has used.
- The first measurement of the random-vs-causal gap on MultiClaim / SemEval-2025 Task 7 data, decomposed into additive components with paired-bootstrap intervals, for 4+ systems from BM25 to LLM reranking.
- A Polish-vs-English difference-in-differences estimate of the causal penalty, with a power analysis that states the minimum detectable effect.
- Released split definitions, cluster-expanded qrels for earlier same-claim debunks (LLM-proposed, human-validated on Polish), and a time-to-findability curve per language.
- A coded analysis of 50 newly failing queries with a shared failure codebook (narrative drift, lexical leakage, cross-lingual-only debunk, missing label, timestamp error).

## Novelty map

### What already exists (not novel)

- PFCR task definition: Shaar et al., ACL 2020, "That is a Known Lie" (Snopes, PolitiFact).
- CheckThat! 2020-2022 Task 2 (verified claim retrieval, English tweets vs Snopes; Arabic): random 70/15/15 splits for English in 2021; no causal index constraint.
- CheckThat! 2025 and 2026 dropped PFCR; 2026 tasks are scientific-claim source retrieval, numerical/temporal claim verification, and fact-check article generation. No open PFCR lab task to collide with.
- MultiClaim (Pikuliak et al., EMNLP 2023): 205,751 fact-checks in 39 languages, 28,092 posts in 27 languages, 31,305 pairs; the paper already compares pairs where the post is newer vs older and reports "virtually the same performance" (80.02 vs 80.04 S@10 for GTR-T5), concluding no measurable leak. That analysis keeps the full index; it does not remove future fact-checks or control pool size, so it does not answer our RQ1.
- MultiClaim also reports performance over post-date quantiles (a COVID-19 drop at start of 2020) and an annotation showing about 7x more valid pairs than labelled; both are inputs for us, not competitors.
- SemEval-2025 Task 7 (Peng et al.): train/dev from MultiClaim (8 monolingual languages), test posts newly collected up to March 2024 with Polish and Turkish as unannounced languages; the test pool contains fact-checks up to May 2024, so test posts can still be matched to later fact-checks. Out-of-time test posts, not a causal index.
- SemEval-2025 Task 7 top systems: ensembles of multilingual embedders plus per-language fine-tuned rerankers and LLM reranking (PINGAN AI first monolingual average S@10 0.9601 and crosslingual 0.85875); Polish and Turkish were the weakest languages for most teams.
- MultiClaim v2 (Zenodo 2025): 435k fact-checks, 89k posts, 105k pairs, all published before April 2025; relationship types `claimreview_schema`, `backlink`, `similarity:identical`.
- Ramponi et al., EMNLP 2025: multilingual vs crosslingual PFCR on a MultiClaim v2 subset, 47 languages, best results from LLM reranking and similarity-sampled negatives; no temporal protocol.
- Vykopal et al., Findings EMNLP 2025: AMC-16K, 16,000 manually annotated post-claim pairs over 20 languages, LLMs as PFCR detectors.
- Vykopal et al., EACL 2026: language bias and retrieval bias (popular claims retrieved disproportionately) on AMC-16K. This is the "language-bias analysis already published"; do not claim it.
- MultiClaimNet (Findings EMNLP 2025): 85.3K MultiClaim claims grouped into 30.9K clusters across 78 languages, with timestamps and URLs. Enabler for sibling relevance, not a temporal evaluation.
- Temporal leakage in evidence retrieval for verification: Glockner et al., EMNLP 2022 (evidence leaked from fact-check articles); AVeriTeC, NeurIPS 2023 (evidence must predate the claim); Chen et al., NAACL 2024 (temporal and fact-check-site constraints sharply reduce veracity accuracy, showing web retrieval works largely because it finds later fact-checks). These target verification with web evidence, not matching posts to a fact-check archive.
- Chronological splits in misinformation classification: Mu et al., Findings EACL 2023 (rumour detection overestimated under random splits).
- Recommender systems: Ji et al., TOIS 2023 (data leakage from ignoring the global timeline); RecSys 2025 study comparing temporal leave-one-out with split-by-timepoint.
- IR temporal persistence: LongEval at CLEF 2023 onward (performance drop as test data moves away from training time).
- LLM temporal contamination: date-filtered web search still leaks post-cutoff information (ACL 2026 short); claim-level temporal leakage auditing in LLM backtesting (Findings EMNLP 2026); simulated ignorance does not replicate true ignorance (arXiv 2601.13717).
- Split methodology: Gorman and Bedrick, ACL 2019; Søgaard et al., EACL 2021 (random splits overestimate; prefer biased or time-based splits); Lazaridou et al., NeurIPS 2021 (temporal generalization).

### What is new here

- Causal index for PFCR, as distinct from out-of-time test posts (SemEval) or a post-newer/older comparison over a full index (MultiClaim).
- Separating answerability from ranking quality: the strict causal score mixes "gold does not exist yet" with "system fails"; no PFCR paper reports both.
- Pool-size-matched control: a causal pool is smaller, which raises scores (MultiClaim itself shows performance falls as pool size grows), so an uncontrolled comparison can understate the penalty.
- Cluster-expanded qrels for earlier debunks of the same claim, turning "unanswerable by gold" into "answerable by an earlier sibling".
- Time-to-findability as a deployment metric (days from post until a relevant fact-check is retrievable in the top 10).
- Training-time leakage for fine-tuned PFCR models (random vs chronological training data), absent from SemEval system papers.
- Parametric temporal leakage of LLM rerankers on PFCR, measured with pre- and post-cutoff query strata.
- Polish-English difference-in-differences with an explicit power statement; prior Polish PFCR evidence is the 500-post SemEval test slice and MultiClaim per-language tables.

## Method outline

### Data and timestamps

- Corpora: MultiClaim v1 (Zenodo 7737983), MultiClaim v2 (Zenodo 15413169), SemEval-2025 Task 7 (Zenodo 14989176); AMC-16K as a manually checked secondary set.
- Polish in v1 (paper Table 5): 6,912 fact-checks, 453 posts. Polish sources with at least 50 fact-checks visible in Table 6 include demagog.org.pl 4,292, oko.press 1,872, sprawdzam.afp.com 458; Konkret24 coverage to verify after access.
- Polish in the SemEval-2025 test: 500 posts, 8,796 claims, 564 pairs.
- English is the largest monolingual block (Snopes 18,376 and PolitiFact 9,029 fact-checks in v1).
- Post time: `instances` is a list of (unix timestamp, platform); define `t_post` as the earliest instance; the v1 paper had dates for 26,337 of 28,092 posts, so missing dates must be dropped and reported.
- Fact-check time: `instances` is a list of (unix timestamp, URL); one fact-check can have several instances (several outlets or republications); define `t_fc` as the earliest instance and keep the per-instance list for a sensitivity run.
- Timestamp granularity and time zone are unknown until access; compare at day resolution with a configurable margin (0, ±1, ±7 days) and report sensitivity.
- `similarity:identical` pairs in v2 are added by text identity, not by a fact-checker; report them separately.

### Protocol definitions

- Random protocol: the published setup; full language pool (monolingual) or full pool (crosslingual); all gold pairs.
- Strict causal protocol: for query post q, pool P(q) = {f : t_fc(f) < t_post(q) − margin}; query is answerable iff at least one gold fact-check is in P(q).
- Size-matched random control: for each q, sample |P(q)| fact-checks from the full pool, always keeping gold, to isolate pool-size effects from time effects.
- Cluster-expanded causal protocol: relevance extended to earlier fact-checks in the same MultiClaimNet cluster or judged relevant by the annotation step below.
- Rolling-origin protocol: monthly cutoffs T; index grows to all fact-checks before T; queries are posts in [T, T+1 month); report the series and its mean; this is the streaming deployment view.
- Delayed-query protocol: re-query q at t_post + Δ for Δ in {0, 1, 3, 7, 30, 90} days; yields the time-to-findability curve.
- Training regimes for fine-tuned systems: random training split vs chronological training split (train strictly before the earliest test post); same hyperparameters and steps.

### Leakage taxonomy

- Index leakage: future fact-checks in the pool.
- Answerability leakage: queries counted as answerable only because their debunk was written later.
- Training leakage: supervised pairs from the future, or near-duplicate claims of test queries, in training data.
- Label leakage: relevance labels exist only because a fact-checker later linked post and debunk; earlier siblings are unlabelled.
- Parametric leakage: LLM or embedder pretraining corpora contain post-query fact-checks.
- Timestamp leakage: wrong or updated dates (republication, last-modified dates, time zones) moving documents across the cutoff.

### Systems

- S1 BM25 on original text and on the provided English translation (Pyserini or bm25s); Polish via a Polish analyzer or the provided translation.
- S2 multilingual dense: multilingual-e5-large(-instruct) and BGE-M3 (dense; optionally its sparse and multi-vector modes as a hybrid).
- S3 bilingual or Polish-specialised encoder: sdadas/mmlw-retrieval-roberta-large (PIRB NDCG@10 58.46) and LaBSE as the classic cross-lingual baseline.
- S4 cross-encoder reranker over the S2 top-100: BAAI/bge-reranker-v2-m3 and sdadas/polish-reranker-roberta-v3.
- S5 LLM-scale: Qwen3-Embedding-8B as a retriever and Qwen3-Reranker-8B or an open instruction LLM as a listwise reranker; used for the parametric-leakage strata.
- S6 fine-tuned: multilingual-e5 fine-tuned on MultiClaim pairs under the random and chronological training regimes (H5).
- Hold encoder, translation, text fields (claim plus title) and top-k fixed across protocols; only the pool and the training data change.

### Metrics and statistics

- Success@10 and MRR@10 (task convention); MAP and nDCG@10 in the appendix, as MultiClaim shows they correlate above 0.98 with S@10.
- Answerable rate per protocol and language; conditional S@10 on answerable queries; unconditional S@10 over all queries.
- Time-to-findability: median days from t_post to the first retrievable relevant fact-check; Kaplan-Meier style curve with never-found queries right-censored at the dataset end.
- Paired bootstrap over queries (10,000 resamples) for random-vs-causal differences within a system and language; percentile CIs.
- Polish-English contrast as difference-in-differences with an independent bootstrap per language; Holm correction across systems.
- Optional: randomization (permutation) test for system rankings and Kendall tau of system rankings across protocols.

### Gap decomposition

- Additive chain on one query set: Random → size-matched random (pool size) → causal with cluster-expanded labels (time composition, siblings available) → strict causal answerable (label loss) → strict causal all queries (answerability).
- Report each step's delta with paired-bootstrap CIs; shuffle the step order as a robustness check (Shapley-style averaging over orders).
- Per-query covariates for regression on the per-query delta: post-to-debunk lag (log days, signed), lexical overlap (token Jaccard and BM25 score between post and gold), cross-lingual gold flag, relationship type, cluster size, earlier-sibling count, topic (BERTopic or LLM label), platform, OCR-only text flag.
- Narrative drift: LLM judge rates whether the earliest relevant fact-check and the post express the same claim, a variant, or an updated narrative; validated on a human-labelled sample.

### Annotation plan

- 50 newly failing queries (correct under random, wrong under causal) per the brief, stratified by language (25 Polish, 25 English) and system family; two annotators, Cohen's kappa reported.
- Codebook: answerability (no earlier relevant fact-check exists), lexical leakage (later debunk quotes the post), narrative drift, cross-lingual-only earlier debunk, missing label (an earlier relevant fact-check exists but is unlabelled), timestamp error, multimodal-only claim (image or video needed; MultiClaim attributes 13 of 100 checked pairs to this).
- Sibling qrels: for strict-causal-unanswerable Polish queries, pool the top-10 earlier fact-checks from S2, S4 and S5 and have an LLM judge relevance; humans relabel a random 200 Polish and 200 English judgments to report LLM-human agreement; release only judged ids, never raw post text.

## Risks and mitigations

- Date reliability: unix timestamps may be crawl or update times, not publication times; check a 100-item sample per language against the live URL date; run margin sensitivity; report the share of pairs whose lag sign flips within ±7 days.
- Post dates missing for some posts (1,755 of 28,092 in v1 by the paper's own count): exclude and report; test whether exclusion correlates with language.
- Small Polish answerable set: a strict causal filter may leave only a fraction of Polish queries answerable; pool v1, v2 and the SemEval test (deduplicated by post id and text) and use cluster-expanded labels to raise the answerable count.
- Statistical power (sketch below): pre-register the minimum detectable effect and report CIs, not only p-values.
- Translated duplicates and near-duplicate fact-checks: deduplicate by normalised claim text and MultiClaimNet clusters before counting siblings; keep cross-outlet duplicates in the pool because they exist in deployment.
- Pool-size confound: always report the size-matched control alongside the strict causal score.
- Fine-tuning leakage via pretrained encoders: multilingual-e5, BGE-M3 and Qwen3 may have seen MultiClaim-era fact-checks; flag as parametric leakage, compare pre- and post-release query strata, do not claim it is removed.
- Access terms: data is research-only, request from an institutional e-mail, no re-sharing, no deanonymisation; release split definitions as id lists, timestamps cutoffs and code that rebuilds splits from the official files, never post text.
- Ethics on named outlets and journalists: report errors per language and per system, not per outlet or author; no ranked list of outlets; quote no full posts in the paper; paraphrase failure examples.
- Overlap with the KInIT group (dataset authors, very active): cite MultiClaim's post-newer/older analysis explicitly and frame the protocol as a complement; consider contacting them for v2 access and timestamp semantics.
- Scope creep: the novelty is the protocol and decomposition; no new architecture, no veracity prediction, no language-bias claims.

### Power sketch

- Paired Success@10 difference on n queries with discordance rate d (share of queries whose hit/miss flips between protocols): SE ≈ sqrt(d / n); MDE at alpha 0.05 and 80% power ≈ 2.80 × SE.
- Difference-in-differences with English n = 5,000: SE_DiD = sqrt(d/n_pl + d/5000).
- Values computed for this note (assumed d, not measured):

| Polish n | d | 95% CI half-width | MDE paired | MDE DiD |
|---|---|---|---|---|
| 300 | 0.10 | 0.036 | 0.051 | 0.053 |
| 300 | 0.20 | 0.051 | 0.072 | 0.074 |
| 450 | 0.10 | 0.029 | 0.042 | 0.044 |
| 450 | 0.20 | 0.041 | 0.059 | 0.062 |
| 564 | 0.10 | 0.026 | 0.037 | 0.039 |
| 564 | 0.20 | 0.037 | 0.053 | 0.056 |
| 1000 | 0.10 | 0.020 | 0.028 | 0.031 |
| 1000 | 0.20 | 0.028 | 0.040 | 0.043 |

- Reading: with about 450 Polish queries, a Polish-English penalty difference below roughly 4-6 points of S@10 is not detectable; with only about 150 answerable Polish queries the MDE grows to roughly 7-10 points, so pooling sources is necessary.
- Replace assumed d with the measured discordance after the first run and re-state the MDE in the paper.

## Venue strategy

- Primary: ACL Rolling Review targeting ACL 2027 Findings or main (ARR deadline 4 Jan 2027 per ccfddl); framing as an evaluation-methodology paper with a resource.
- IR alternative: SIGIR 2027 short or resource track (full-paper deadline 21 Jan 2027; short and resource dates TBA); ECIR 2027 resource track deadline 2 Nov 2026 is too close for results.
- Workshops: FEVER (ACL-co-located; check 2027 CFP), NLP4PI (2026 edition held 28 Oct 2026 at EMNLP; target 2027), and a findings-style short if the gap is small but well-measured.
- CheckThat!: no PFCR task in 2025-2026; the protocol and split are a candidate task proposal for a future CLEF lab (temporal PFCR with a Polish track), or a LongEval-style temporal persistence track.
- Negative-result fallback: if the causal penalty is small, the paper still stands as "the leakage is answerability, not ranking", plus the time-to-findability resource.

## Alternative directions considered

- Streaming / rolling-origin evaluation only: high feasibility, moderate novelty; kept as a protocol variant rather than the headline.
- Recency and age priors in ranking: a model change, borderline "new architecture"; keep as a diagnostic re-scoring baseline at most.
- Abstention and calibration for unanswerable posts (no fact-check exists yet): high practical value and novel for PFCR; second paper or a section if time allows (score threshold selective-retrieval curve on causal unanswerable queries).
- Narrative-drift annotation with LLMs as the main contribution: novel but hard to validate at scale; kept as a decomposition covariate.
- Near-duplicate vs same-claim debunk retrieval benchmark: overlaps MultiClaimNet clustering; kept as the sibling-qrel step.
- Cross-lingual temporal effects (earlier debunk exists only in another language): included as a covariate and a code in the failure analysis, not a separate study, to avoid language-bias framing.
- Reranking robustness under causal pools: subsumed by S4 and S5 rows.
- Parametric leakage of LLM rerankers as a standalone paper: novel, but needs clean post-cutoff queries (MultiClaim v2 up to April 2025 helps); kept as RQ5.
- Veracity of retrieved claims, new retrievers, language-bias study: out of scope by the brief.

## Reference list

- Shaar et al. 2020, That is a Known Lie, ACL: https://aclanthology.org/2020.acl-main.332/
- Pikuliak et al. 2023, Multilingual Previously Fact-Checked Claim Retrieval (MultiClaim), EMNLP: https://aclanthology.org/2023.emnlp-main.1027/ ; arXiv HTML with tables: https://arxiv.org/html/2305.07991v2
- MultiClaim v1 Zenodo record: https://zenodo.org/records/7737983
- MultiClaim v2 Zenodo record: https://zenodo.org/records/15413169
- MultiClaim code: https://github.com/kinit-sk/multiclaim
- Peng et al. 2025, SemEval-2025 Task 7 overview: https://aclanthology.org/2025.semeval-1.323/
- SemEval-2025 Task 7 data on Zenodo: https://zenodo.org/records/14989176
- Ramponi et al. 2025, Multilingual vs Crosslingual Retrieval of Fact-Checked Claims, EMNLP: https://aclanthology.org/2025.emnlp-main.1480/
- Vykopal et al. 2025, LLMs for Multilingual Previously Fact-Checked Claim Detection (AMC-16K), Findings EMNLP: https://aclanthology.org/2025.findings-emnlp.852/
- Vykopal et al. 2026, Investigating Language and Retrieval Bias in Multilingual PFCD, EACL: https://aclanthology.org/2026.eacl-long.240/
- MultiClaimNet 2025, Findings EMNLP: https://aclanthology.org/2025.findings-emnlp.599/ ; data: https://zenodo.org/records/15100352
- Kazemi et al. 2021, Claim Matching Beyond English, ACL: https://aclanthology.org/2021.acl-long.347/
- Hardalov et al. 2022, CrowdChecked, AACL: https://aclanthology.org/2022.aacl-main.22/
- CheckThat! 2021 Task 2 overview: https://ceur-ws.org/Vol-2936/paper-29.pdf
- CheckThat! 2022 Task 2 overview: https://ceur-ws.org/Vol-3180/paper-29.pdf
- CheckThat! 2026 lab overview: https://arxiv.org/abs/2602.09516 ; site: https://checkthat.gitlab.io/
- Glockner et al. 2022, Missing Counter-Evidence, EMNLP: https://aclanthology.org/2022.emnlp-main.397/
- Schlichtkrull et al. 2023, AVeriTeC, NeurIPS Datasets and Benchmarks: https://arxiv.org/abs/2305.13117
- Chen et al. 2024, Complex Claim Verification with Evidence Retrieved in the Wild, NAACL: https://aclanthology.org/2024.naacl-long.196/
- Mu et al. 2023, It's about Time: chronological splits for rumour detection, Findings EACL: https://aclanthology.org/2023.findings-eacl.55.pdf
- Ji et al. 2023, A Critical Study on Data Leakage in Recommender System Offline Evaluation, TOIS: https://dl.acm.org/doi/10.1145/3569930
- Don't Get Ahead of Yourself: data leakage in sequential recommender evaluation, RecSys 2025: https://dl.acm.org/doi/10.1145/3705328.3759329
- LongEval CLEF 2023: https://clef-longeval-2023.github.io/
- Gorman and Bedrick 2019, We Need to Talk about Standard Splits, ACL: https://aclanthology.org/P19-1267/
- Søgaard et al. 2021, We Need To Talk About Random Splits, EACL: https://aclanthology.org/2021.eacl-main.156/
- Lazaridou et al. 2021, Mind the Gap, NeurIPS: https://proceedings.neurips.cc/paper/2021/hash/f5bf0ba0a17ef18f9607774722f5698c-Abstract.html
- Temporal Leakage in Search-Engine Date-Filtered Web Retrieval, ACL 2026 short: https://aclanthology.org/2026.acl-short.65
- All Leaks Count, Some Count More: temporal contamination in LLM backtesting, Findings EMNLP 2026: https://aclanthology.org/2026.findings-emnlp.1690.pdf
- Simulated Ignorance Fails (pre-cutoff forecasting): https://arxiv.org/abs/2601.13717
- Wang et al. 2024, Multilingual E5 Text Embeddings: https://arxiv.org/abs/2402.05672
- Chen et al. 2024, M3-Embedding (BGE-M3), Findings ACL: https://aclanthology.org/2024.findings-acl.137/
- Feng et al. 2022, LaBSE, ACL: https://aclanthology.org/2022.acl-long.62/
- Zhang et al. 2025, Qwen3 Embedding: https://arxiv.org/abs/2506.05176
- Dadas et al. 2024, PIRB, LREC-COLING: https://aclanthology.org/2024.lrec-main.1117/
- sdadas/mmlw-retrieval-roberta-large: https://huggingface.co/sdadas/mmlw-retrieval-roberta-large
- sdadas/polish-reranker-roberta-v3: https://huggingface.co/sdadas/polish-reranker-roberta-v3
- SIGIR 2027 dates: https://sigir2027.org/
- ECIR 2027 calls: https://www.ecir2027.co.uk/
- NLP4PI 2026 proceedings: https://aclanthology.org/2026.nlp4pi-1.0.pdf
