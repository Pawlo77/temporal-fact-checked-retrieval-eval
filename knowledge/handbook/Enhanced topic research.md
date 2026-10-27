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

Builds on [[Original Task]]. Sources checked on 2026-10-27 and re-verified the same day against primary sources (per-paper notes in `research/`, corrections in [[research/CORRECTIONS-A.md]] and [[research/CORRECTIONS-B.md]]); every claim below carries a URL in the reference list. Counts quoted from papers are the papers' numbers, not ours; our own counts come only after the data request is granted. Team-level synthesis: [[Research summary]].

## Recommended enhanced topic

### Title

**Retrieval that cannot see the future: a causal evaluation protocol for previously fact-checked claim retrieval, with answerability-aware metrics and a Polish-English contrast**

### Pitch

Previously fact-checked claim retrieval (PFCR) is scored on MultiClaim and SemEval-2025 Task 7 against a search pool that contains fact-checks published after the query post, while a fact-checker querying at post time only has the archive up to that moment. Time-respecting retrieval evaluation itself is old (TREC 2011 Microblog banned future documents and future corpus statistics), and a chronological training split for PFCR exists on English political debates (Shaar et al. 2022), but no PFCR evaluation found restricts the fact-check index by date. We define a causal (time-respecting) protocol for PFCR, show that a naive "index only earlier fact-checks" filter conflates four effects (gold disappearing, pool shrinkage, supervised-training leakage, missing relevance labels for earlier sibling debunks), and decompose the random-vs-causal gap into those components across at least four retrieval families on Polish (focus language) and English (high-archive anchor). The release is a split, cluster-expanded relevance labels for earlier debunks, and a time-to-findability metric for the deployment question "if I search for this post on day t, will the debunk be there, and how many days after posting does it become findable?".

### Research questions

- RQ1: How much of the Success@10 and MRR reported under the standard protocol survives a causal index, on answerable queries only, after controlling for pool size?
- RQ2: Which share of the random-vs-causal gap comes from (a) answerability loss, (b) pool composition, (c) training-set leakage in fine-tuned models, (d) missing labels for earlier same-claim fact-checks?
- RQ3: Is the causal penalty larger for Polish than for English, and does archive density explain it (fewer earlier siblings, longer post-to-debunk lags, more cross-lingual-only earlier debunks)? Language set and dose-response design: [[Language scope analysis]].
- RQ4: How long after a post does the first relevant fact-check become retrievable (time-to-findability), and how does it differ by language and system?
- RQ5: Do LLM rerankers gain from parametric knowledge of debunks published after the query (parametric temporal leakage), measured on queries before vs after model knowledge cutoffs?

### Hypotheses

- H1: Most gold pairs are post-before-fact-check, because the dataset is built from fact-checkers linking the posts they debunked; a causal index makes these queries unanswerable by their own gold.
- H2: On the answerable subset, the causal score falls below the random score once pool size is matched, because later fact-checks restate the post wording (lexical leakage) more than earlier ones do.
- H3: Pair relationship type predicts lag sign. Assumption to confirm from the data or with the dataset authors: `backlink` pairs (fact-check body links the post) are post-first by construction, and `claimreview_schema` pairs contain more recurring claims where the debunk is older. The v2 record does not define `backlink` or say where v1 Meta-warning pairs are mapped.
- H4: The Polish causal penalty (difference-in-differences vs English) is positive and larger for lexical BM25 than for multilingual dense retrievers, because cross-lingual earlier debunks exist for viral international claims.
- H5: Fine-tuned retrievers trained on a random split lose more under causal evaluation than zero-shot retrievers, because training pairs include near-duplicates of future test claims (Shaar et al. 2022 saw MAP fall from 0.602 to 0.429 under a chronological split on debates, without separating drift from leakage).
- H6: Cluster-expanded labels recover a measurable share of "unanswerable" queries, so the strict causal score under-states deployable value; the true number lies between the strict and expanded scores.

### Contributions claimed

- A causal protocol for PFCR (date-restricted fact-check index per query) and a leakage taxonomy (index, statistics, answerability, training, label, parametric, timestamp leakage); the protocol adapts the TREC 2011 Microblog "no future evidence" rule to PFCR, and the control matches pool size per query to the time-restricted pool (MultiClaim varied pool size globally with random fact-checks; no prior PFCR work matched pool size to a time-restricted pool).
- The first measurement of the random-vs-causal-index gap on MultiClaim / SemEval-2025 Task 7 data, decomposed into additive components with paired-bootstrap intervals, for 4+ systems from BM25 to LLM reranking.
- Training-time leakage for multilingual social-media PFCR (random vs chronological training on MultiClaim), extending the debate-level chronological split of Shaar et al. 2022.
- A Polish-vs-English difference-in-differences estimate of the causal penalty, with a power analysis that states the minimum detectable effect.
- Released split definitions, cluster-expanded qrels for earlier same-claim debunks (LLM-proposed, human-validated on Polish), and a time-to-findability curve per language.
- A coded analysis of 50 newly failing queries with a shared failure codebook (narrative drift, lexical leakage, cross-lingual-only debunk, missing label, timestamp error).

## Novelty map

### What already exists (not novel)

- Time-respecting IR evaluation: TREC 2011 Microblog (Ounis et al.) ran "At time t, find tweets about topic X" with a compulsory run banning future evidence, defined to include IDF computed on tweets posted after the query time; constrained and unconstrained runs reported separately.
- Dated queries against a growing time-stamped corpus: StreamingQA (Liska et al., ICML 2022), a precedent for the rolling-origin protocol and for separating index freshness from parametric freshness.
- PFCR task definition: Shaar et al., ACL 2020, "That is a Known Lie" (Snopes tweets; PolitiFact debate sentences, not social-media posts).
- Chronological train/test splits for PFCR: Shaar et al., Findings NAACL 2022 (PolitiFact debates; reranker MAP 0.602 sentence-level random, 0.590 debate-level random, 0.539 semi-chronological, 0.429 debate-level chronological); training split only, one verified-claim collection (16,636 claims) with no date restriction described, no answerability or pool-size separation, English only.
- CheckThat! 2021-2022 Task 2: 2A tweets (English vs 13,835 Snopes claims; Arabic) and 2B debates (English vs PolitiFact); English 2A split 70/15/15 in 2021 (999/200/202; "randomly" stated only for Arabic) with a new 209-tweet test in 2022; no date restriction of the verified-claim pool described. CheckThat! 2020 not verified.
- CheckThat! 2025 and 2026 dropped PFCR; 2026 tasks are scientific-claim source retrieval, numerical/temporal claim verification, and fact-check article generation. No open PFCR lab task to collide with.
- MultiClaim (Pikuliak et al., EMNLP 2023): 205,751 fact-checks in 39 languages, 28,092 posts in 27 languages, 31,305 pairs (the paper's mono 26,774 plus cross 4,212 sum to 30,986; recount after access).
- MultiClaim temporal analyses, all to cite: post-newer vs post-older pairs give "virtually the same performance" (80.02 vs 80.04 monolingual S@10 for GTR-T5) over the full index, concluding no measurable leak; performance over 20 post-date quantiles (a COVID-19 drop at the start of 2020); a pool-size sweep adding random fact-checks (pool 100 to 2,100) showing the BM25-vs-TEM gap depends on pool size. None removes future fact-checks per query, so they do not answer our RQ1.
- MultiClaim also annotates about 7x more valid pairs than labelled; an input for sibling labels, not a competitor.
- SemEval-2025 Task 7 (Peng et al.): monolingual train/dev from MultiClaim (8 languages), crosslingual train/dev over 14 languages (52 combinations); all MultiClaim posts predate 2023; test posts newly collected up to March 2024 with Polish and Turkish as unannounced languages; the test pool contains fact-checks up to May 2024, so test posts can still be matched to later fact-checks. Out-of-time test posts, not a causal index.
- SemEval-2025 Task 7 systems: top-ranked PINGAN AI (mono avg S@10 0.9601, cross 0.85875) published no system description; described top systems use translation plus fine-tuned embedders with hard negatives (TIFIN India, fact check AI), LLM reranking of the top 50 with RRF (TIFIN India), per-language fine-tuned reranker ensembles (QUST_NLP), or a single fine-tuned LLM-based embedder without reranking (RACAI).
- SemEval-2025 Task 7 languages: the overview reports that the two unseen languages (Polish, Turkish) score generally lower than training languages; in Table 8 Polish is among the lowest-scoring languages for top teams, together with English (PINGAN AI eng 0.9160, pol 0.9260, tur 0.9480).
- MultiClaim v2 (Zenodo 2025): 435k fact-checks, 89k posts, 105k pairs, posts published before April 2025 (whether this also bounds fact-checks is not stated); relationship types `claimreview_schema`, `backlink`, `similarity:identical`.
- Ramponi, Rovera, Moro, Tonelli, EMNLP 2025: multilingual vs crosslingual PFCR on a MultiClaim v2 subset, 47 languages including Polish, best results from LLM reranking followed by fine-tuning with similarity-sampled negatives; random split stratified by language; only `claim_review` and `backlink` pairs used; no temporal protocol.
- Vykopal et al., Findings EMNLP 2025: AMC-16K, 16,000 manually annotated post-claim pairs (8K monolingual, 8K crosslingual) over 20 languages including 400 Polish monolingual pairs, LLMs as PFCR detectors; lower LLM performance for Polish and other Slavic languages.
- Vykopal et al., EACL 2026: language bias and retrieval bias (popular claims retrieved disproportionately) on AMC-16K. This is the "language-bias analysis already published"; do not claim it.
- Vykopal et al., arXiv 2504.20668: a claim retrieval system with date range as a natural-language filter criterion (the worst-performing filter); a retrieval feature, not an evaluation protocol.
- MultiClaimNet (Panchendrarajan et al., Findings EMNLP 2025): 85.3K MultiClaim claims grouped into 30.9K clusters across 78 languages from LLM-annotated similarity, with timestamps and URLs. Enabler for sibling relevance, not a temporal evaluation.
- Temporal leakage in evidence retrieval for verification: Glockner et al., EMNLP 2022 (evidence leaked from fact-check articles); AVeriTeC, NeurIPS 2023 (evidence must predate the claim; splits ordered temporally; the guarantee is approximate, about 6% of dev answers come from fact-checking domains, mostly earlier fact-checks of the same claim, which supports sibling qrels); Chen et al., NAACL 2024 (temporal and fact-check-site constraints sharply reduce veracity accuracy, showing web retrieval works largely because it finds later fact-checks). These target verification with web evidence, not matching posts to a fact-check archive.
- Chronological splits in misinformation classification: Mu et al., Findings EACL 2023 (rumour detection overestimated under random splits).
- Recommender systems: Ji, Sun, Zhang, Li, TOIS 2023 (data leakage from ignoring the global timeline); Le et al., RecSys 2025 extended abstract comparing temporal leave-one-out with split-by-timepoint, with a training-size control.
- IR temporal persistence: LongEval (CLEF 2023 onward) evaluates systems on successive Qwant snapshots; in 2023 the change in NDCG was system-dependent, not a uniform drop (Alkhalifa et al., CLEF 2023 overview); it snapshots collections, it does not forbid future documents per query.
- LLM temporal contamination: date-filtered web search still leaks post-cutoff information (El Lahib et al., ACL 2026 short); claim-level temporal leakage auditing in LLM backtesting (Zhang and Stadie, Findings EMNLP 2026); simulated ignorance does not replicate true ignorance (Li et al., IJCAI 2026; arXiv 2601.13717).
- Split methodology: Gorman and Bedrick (ACL 2019) argue for random over standard splits and for significance testing; Søgaard et al. (EACL 2021) show random splits over-estimate performance on new samples and recommend independent test samples, else biased/adversarial splits (temporal drift only in an appendix); Lazaridou et al., NeurIPS 2021 (temporal generalization).

### What is new here

- Causal (date-restricted) fact-check index for PFCR evaluation, as distinct from out-of-time test posts (SemEval), a post-newer/older comparison over a full index (MultiClaim), or a chronological training split over an undated pool (Shaar et al. 2022); the general time-respecting idea is TREC 2011 Microblog's.
- Separating answerability from ranking quality: the strict causal score mixes "gold does not exist yet" with "system fails"; no PFCR paper found reports both.
- Per-query pool-size-matched control: we expect absolute scores to rise in smaller pools (MultiClaim showed pool size changes the BM25-vs-TEM gap, not an absolute decline), so an uncontrolled comparison can understate the penalty; MultiClaim's random-addition sweep is the precedent, matching to a time-restricted pool is new.
- Cluster-expanded qrels for earlier debunks of the same claim, turning "unanswerable by gold" into "answerable by an earlier sibling" (AVeriTeC treats earlier fact-checks as legitimate evidence for verification; not done for PFCR).
- Time-to-findability as a deployment metric (days from post until a relevant fact-check is retrievable in the top 10).
- Training-time leakage for multilingual social-media PFCR (MultiClaim/SemEval), extending the debate-level chronological split of Shaar et al. 2022 and separating it from index and answerability effects.
- Statistics leakage measured for PFCR: BM25 with full-pool vs causal-pool corpus statistics.
- Parametric temporal leakage of LLM rerankers on PFCR, measured with pre- and post-cutoff query strata.
- Polish-English difference-in-differences with an explicit power statement, plus the archive-density dose-response of [[Language scope analysis]]; prior Polish PFCR evidence: SemEval-2025 test (500 posts, 564 pairs; per-team Polish S@10 in Table 8), MultiClaim v1 tables (6,912 fact-checks, 453 posts), AMC-16K Polish annotations and LLM results (Vykopal et al. 2025), and Polish as one of 47 languages in Ramponi et al. 2025.
- Confidence: these claims hold as far as searches on 2026-10-27 reached; Shaar et al. 2022 was read via arXiv and an excerpt, so a date restriction of its pool cannot be fully ruled out.

## Method outline

### Data and timestamps

- Corpora: MultiClaim v1 (Zenodo 7737983), MultiClaim v2 (Zenodo 15413169), SemEval-2025 Task 7 (Zenodo 14989176); AMC-16K as a manually checked secondary set.
- Polish in v1 (paper Table 5): 6,912 fact-checks, 453 posts. Polish sources with at least 50 fact-checks visible in Table 6 include demagog.org.pl 4,292, oko.press 1,872, sprawdzam.afp.com 458, fakenews.pl 320; Konkret24 not seen in the Table 6 rows read.
- Polish in the SemEval-2025 test: 500 posts, 8,796 claims, 564 pairs.
- English is the largest monolingual block (Snopes 18,376 and PolitiFact 9,029 fact-checks in v1).
- Post time: in v2 `instances` is a list of (unix timestamp, platform) (the v1 record says "timestamps" without "unix"); define `t_post` as the earliest instance; the v1 paper had dates for 26,337 of 28,092 posts, so missing dates must be dropped and reported.
- Fact-check time: `instances` is a list of (timestamp, URL); one fact-check can have several instances (several outlets or republications); define `t_fc` as the earliest instance and keep the per-instance list for a sensitivity run.
- Timestamp granularity, time zone and semantics (publication vs crawl vs update) are undocumented in both records; compare at day resolution with a configurable margin (0, ±1, ±7 days) and report sensitivity.
- `similarity:identical` pairs in v2 are, on our reading of "(for identical claims)", added by text identity rather than by a fact-checker (interpretation, to confirm); report them separately, as Ramponi et al. dropped them.

### Protocol definitions

- Random protocol: the published setup; full language pool (monolingual) or full pool (crosslingual); all gold pairs.
- Strict causal protocol: for query post q, pool P(q) = {f : t_fc(f) < t_post(q) − margin}; query is answerable iff at least one gold fact-check is in P(q); BM25 statistics come from P(q) only (below).
- Size-matched random control: for each q, sample |P(q)| fact-checks from the full pool, always keeping gold, to isolate pool-size effects from time effects.
- Cluster-expanded causal protocol: relevance extended to earlier fact-checks in the same MultiClaimNet cluster or judged relevant by the annotation step below.
- Rolling-origin protocol: monthly cutoffs T; index (and its corpus statistics) grows to all fact-checks before T; queries are posts in [T, T+1 month); report the series and its mean; this is the streaming deployment view (precedents: StreamingQA, LongEval).
- Delayed-query protocol: re-query q at t_post + Δ for Δ in {0, 1, 3, 7, 30, 90} days; yields the time-to-findability curve.
- Training regimes for fine-tuned systems: random training split vs chronological training split (train strictly before the earliest test post); same hyperparameters and steps.
- Reporting: random and causal results in separate tables per system, as TREC 2011 Microblog reported constrained and unconstrained runs.

### Leakage taxonomy

- Index leakage: future fact-checks in the pool.
- Statistics leakage: corpus statistics such as BM25 IDF, document-length normalisation, vocabulary or any other index-level statistic computed over the full pool, including fact-checks published after the query, even when those documents are filtered from results (TREC 2011 Microblog's definition of future evidence).
- Answerability leakage: queries counted as answerable only because their debunk was written later.
- Training leakage: supervised pairs from the future, or near-duplicate claims of test queries, in training data.
- Label leakage: relevance labels exist only because a fact-checker later linked post and debunk; earlier siblings are unlabelled.
- Parametric leakage: LLM or embedder pretraining corpora contain post-query fact-checks.
- Timestamp leakage: wrong or updated dates (republication, last-modified dates, time zones) moving documents across the cutoff.

### Systems

- S1 BM25 on original text and on the provided English translation (Pyserini or bm25s); Polish via a Polish analyzer or the provided translation; IDF and average document length computed from the causal pool only (document frequencies kept as cumulative counts by `t_fc`, so the statistics at any cutoff are a lookup, not a reindex); one sensitivity row with full-pool statistics measures statistics leakage.
- S2 multilingual dense: multilingual-e5-large(-instruct) and BGE-M3 (dense; optionally its sparse and multi-vector modes as a hybrid); encode the pool once and apply time masks at search time.
- S3 bilingual or Polish-specialised encoder: sdadas/mmlw-retrieval-roberta-large (PIRB NDCG@10 58.46 per model card; paper Table 3: 58.06; mE5-large 57.29) and LaBSE as the classic cross-lingual baseline; mmlw was distilled on 60M Polish-English pairs, so Polish-to-English retrieval is plausible but unreported; measure it.
- S4 cross-encoder reranker over the S2 top-100: BAAI/bge-reranker-v2-m3 (Apache-2.0) and sdadas/polish-reranker-roberta-v3 (443M parameters, 8,192-token context, PIRB reranker NDCG@10 66.21; licence "gemma", check before releasing derived artefacts).
- S5 LLM-scale: Qwen3-Embedding-8B as a retriever and Qwen3-Reranker-8B or an open instruction LLM as a listwise reranker; used for the parametric-leakage strata (released June 2025, no training cutoff stated).
- S6 fine-tuned: multilingual-e5 fine-tuned on MultiClaim pairs under the random and chronological training regimes (H5).
- Hold encoder, translation, text fields (claim plus title) and top-k fixed across protocols; only the pool, its statistics and the training data change.

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
- Statistics leakage is reported beside the chain for BM25 (full-pool vs causal-pool statistics at the strict causal step).
- Per-query covariates for regression on the per-query delta: post-to-debunk lag (log days, signed), lexical overlap (token Jaccard and BM25 score between post and gold), cross-lingual gold flag, relationship type, cluster size, earlier-sibling count, causal pool size, topic (BERTopic or LLM label), platform, OCR-only text flag.
- Narrative drift: LLM judge rates whether the earliest relevant fact-check and the post express the same claim, a variant, or an updated narrative; validated on a human-labelled sample.

### Annotation plan

- 50 newly failing queries (correct under random, wrong under causal) per the brief, stratified by language (25 Polish, 25 English) and system family; two annotators, Cohen's kappa reported.
- Codebook: answerability (no earlier relevant fact-check exists), lexical leakage (later debunk quotes the post), narrative drift, cross-lingual-only earlier debunk, missing label (an earlier relevant fact-check exists but is unlabelled), timestamp error, multimodal-only claim (image or video needed; MultiClaim attributes 13 of 100 checked pairs to this).
- Sibling qrels: for strict-causal-unanswerable Polish queries, pool the top-10 earlier fact-checks from S2, S4 and S5 and have an LLM judge relevance; humans relabel a random 200 Polish and 200 English judgments to report LLM-human agreement; AMC-16K Polish labels serve as an extra check of the judge; release only judged ids, never raw post text.

## Risks and mitigations

- Date reliability: timestamps may be crawl or update times, not publication times; check a 100-item sample per language against the live URL date; run margin sensitivity; report the share of pairs whose lag sign flips within ±7 days.
- Post dates missing for some posts (1,755 of 28,092 in v1 by the paper's own count): exclude and report; test whether exclusion correlates with language.
- Small Polish answerable set: a strict causal filter may leave only a fraction of Polish queries answerable; pool v1, v2 and the SemEval test (deduplicated by post id and text) and use cluster-expanded labels to raise the answerable count.
- Statistics leakage: a date filter applied after retrieval over a full-pool BM25 index still uses future IDF; build BM25 statistics from the causal pool only (cumulative document frequencies by date) and report the full-pool variant as a sensitivity row.
- Statistical power (sketch below): pre-register the minimum detectable effect and report CIs, not only p-values.
- Translated duplicates and near-duplicate fact-checks: deduplicate by normalised claim text and MultiClaimNet clusters before counting siblings; keep cross-outlet duplicates in the pool because they exist in deployment.
- Pool-size confound: always report the size-matched control alongside the strict causal score.
- Fine-tuning leakage via pretrained encoders: multilingual-e5, BGE-M3 and Qwen3 may have seen MultiClaim-era fact-checks; flag as parametric leakage, compare pre- and post-release query strata, do not claim it is removed; do not rely on prompting an LLM to "pretend it is date t" (simulated ignorance fails).
- Access terms: data is research-only, request from an institutional e-mail, no re-sharing, no deanonymisation; release split definitions as id lists, timestamps cutoffs and code that rebuilds splits from the official files, never post text.
- Ethics on named outlets and journalists: report errors per language and per system, not per outlet or author; no ranked list of outlets; quote no full posts in the paper; paraphrase failure examples.
- Overlap with the KInIT group (dataset authors, very active; their arXiv 2504.20668 system already offers date-range filtering): cite MultiClaim's three temporal analyses explicitly and frame the protocol as a complement; consider contacting them for v2 access and timestamp semantics.
- Overlap with Shaar et al. 2022: cite as the closest PFCR precedent; claim only the index restriction, the decomposition and the multilingual setting.
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
- Per-language counts with v2 and the dose-response power are in [[Language scope analysis]].

## Venue strategy

- Primary: ACL Rolling Review targeting ACL 2027 main or Findings (ARR submission deadline 4 January 2027 AoE per the ACL 2027 call; commitment deadline TBD; ACL 2027 is 17-22 August 2027 in Kyoto; papers not accepted to main are considered for Findings); framing as an evaluation-methodology paper with a resource.
- IR alternative: SIGIR 2027 short or resource track (abstract deadline 14 January 2027, full-paper deadline 21 January 2027, notification 5 April 2027, short and resource dates TBA; conference 18-24 July 2027, San Jose); ECIR 2027 resource track (submission 2 November 2026, notification 7 December 2026; conference 21-25 March 2027, Southampton) is too close for results, and its full-paper and reproducibility deadlines have passed.
- Workshops: FEVER (co-location varies: ACL 2025, EACL 2026; no 2027 CFP found on 2026-10-27), NLP4PI (2026 edition held 28 October 2026 in Budapest at EMNLP; target 2027), and a findings-style short if the gap is small but well-measured.
- CheckThat!: no PFCR task in 2025-2026; CLEF 2027 lab proposals closed on 17 July 2026 (CLEF 2027 is 14-17 September 2027, Bucharest), so a temporal PFCR task with a Polish track is a proposal for CLEF 2028 at the earliest (deadline not yet published); in 2027 the only option is joining an existing lab (LongEval or CheckThat!, if running).
- Negative-result fallback: if the causal penalty is small, the paper still stands as "the leakage is answerability, not ranking", plus the time-to-findability resource.

## Alternative directions considered

- Streaming / rolling-origin evaluation only: high feasibility, moderate novelty (StreamingQA and LongEval are precedents); kept as a protocol variant rather than the headline.
- Recency and age priors in ranking: a model change, borderline "new architecture"; keep as a diagnostic re-scoring baseline at most.
- Abstention and calibration for unanswerable posts (no fact-check exists yet): high practical value and novel for PFCR; second paper or a section if time allows (score threshold selective-retrieval curve on causal unanswerable queries).
- Narrative-drift annotation with LLMs as the main contribution: novel but hard to validate at scale; kept as a decomposition covariate.
- Near-duplicate vs same-claim debunk retrieval benchmark: overlaps MultiClaimNet clustering; kept as the sibling-qrel step.
- Cross-lingual temporal effects (earlier debunk exists only in another language): included as a covariate and a code in the failure analysis, not a separate study, to avoid language-bias framing.
- Reranking robustness under causal pools: subsumed by S4 and S5 rows.
- Parametric leakage of LLM rerankers as a standalone paper: novel, but needs clean post-cutoff queries (MultiClaim v2 up to April 2025 helps); kept as RQ5.
- Veracity of retrieved claims, new retrievers, language-bias study: out of scope by the brief.

## Reference list

Per-paper verification notes are in `research/`; corrections in [[research/CORRECTIONS-A.md]] (claim-retrieval literature) and [[research/CORRECTIONS-B.md]] (methodology, models, venues).

- Ounis, Macdonald, Lin, Soboroff 2011, Overview of the TREC-2011 Microblog Track, TREC 2011: https://trec.nist.gov/pubs/trec20/papers/MICROBLOG.OVERVIEW.pdf ; note [[research/2011 - Ounis - TREC 2011 Microblog Track Overview.md]]
- Shaar et al. 2020, That is a Known Lie, ACL: https://aclanthology.org/2020.acl-main.332/ ; note [[research/2020 - Shaar - That is a Known Lie.md]]
- Shaar, Alam, Da San Martino, Nakov 2022, The Role of Context in Detecting Previously Fact-Checked Claims, Findings NAACL, pp. 1619-1631: https://aclanthology.org/2022.findings-naacl.122/ ; arXiv: https://arxiv.org/abs/2104.07423 ; note [[research/2022 - Shaar - Role of Context in PFCR (chronological split).md]]
- Pikuliak et al. 2023, Multilingual Previously Fact-Checked Claim Retrieval (MultiClaim), EMNLP: https://aclanthology.org/2023.emnlp-main.1027/ ; arXiv HTML with tables: https://arxiv.org/html/2305.07991v2 ; note [[research/2023 - Pikuliak - MultiClaim.md]]
- MultiClaim v1 Zenodo record: https://zenodo.org/records/7737983 ; note [[research/2025 - KInIT - MultiClaim v1 and v2 Zenodo records.md]]
- MultiClaim v2 Zenodo record: https://zenodo.org/records/15413169
- MultiClaim code: https://github.com/kinit-sk/multiclaim
- Peng et al. 2025, SemEval-2025 Task 7 overview: https://aclanthology.org/2025.semeval-1.323/ ; note [[research/2025 - Peng - SemEval-2025 Task 7 overview.md]]
- SemEval-2025 Task 7 data on Zenodo: https://zenodo.org/records/14989176
- Devadiga et al. 2025, TIFIN India at SemEval-2025, SemEval: https://aclanthology.org/2025.semeval-1.299/ ; note [[research/2025 - Devadiga - TIFIN India at SemEval-2025 Task 7.md]]
- Ramponi, Rovera, Moro, Tonelli 2025, Multilingual vs Crosslingual Retrieval of Fact-Checked Claims, EMNLP: https://aclanthology.org/2025.emnlp-main.1480/ ; note [[research/2025 - Ramponi - Multilingual vs Crosslingual Retrieval of Fact-Checked Claims.md]]
- Vykopal et al. 2025, LLMs for Multilingual Previously Fact-Checked Claim Detection (AMC-16K), Findings EMNLP: https://aclanthology.org/2025.findings-emnlp.852/ ; note [[research/2025 - Vykopal - LLMs for Multilingual PFCD (AMC-16K).md]]
- Vykopal et al. 2025, A Generative-AI-Driven Claim Retrieval System, arXiv preprint: https://arxiv.org/abs/2504.20668 ; note [[research/2025 - Vykopal - Generative-AI-Driven Claim Retrieval System.md]]
- Vykopal et al. 2026, Investigating Language and Retrieval Bias in Multilingual PFCD, EACL: https://aclanthology.org/2026.eacl-long.240/ ; note [[research/2026 - Vykopal - Language and Retrieval Bias in Multilingual PFCD.md]]
- Panchendrarajan et al. 2025, MultiClaimNet, Findings EMNLP: https://aclanthology.org/2025.findings-emnlp.599/ ; data: https://zenodo.org/records/15100352 ; note [[research/2025 - Panchendrarajan - MultiClaimNet.md]]
- Kazemi et al. 2021, Claim Matching Beyond English, ACL: https://aclanthology.org/2021.acl-long.347/ ; note [[research/2021 - Kazemi - Claim Matching Beyond English.md]]
- Hardalov et al. 2022, CrowdChecked, AACL: https://aclanthology.org/2022.aacl-main.22/ ; note [[research/2022 - Hardalov - CrowdChecked.md]]
- Shaar et al. 2021, CheckThat! 2021 Task 2 overview, CEUR-WS: https://ceur-ws.org/Vol-2936/paper-29.pdf ; note [[research/2021 - Shaar - CheckThat 2021 Task 2 overview.md]]
- Nakov et al. 2022, CheckThat! 2022 Task 2 overview, CEUR-WS: https://ceur-ws.org/Vol-3180/paper-29.pdf ; note [[research/2022 - Nakov - CheckThat 2022 Task 2 overview.md]]
- Struss et al. 2026, The CLEF-2026 CheckThat! Lab, ECIR: https://arxiv.org/abs/2602.09516 ; site: https://checkthat.gitlab.io/ ; note [[research/2026 - Struss - CheckThat 2026 lab overview.md]]
- Glockner et al. 2022, Missing Counter-Evidence, EMNLP: https://aclanthology.org/2022.emnlp-main.397/ ; note [[research/2022 - Glockner - Missing Counter-Evidence.md]]
- Schlichtkrull et al. 2023, AVeriTeC, NeurIPS Datasets and Benchmarks: https://arxiv.org/abs/2305.13117 ; note [[research/2023 - Schlichtkrull - AVeriTeC.md]]
- Chen et al. 2024, Complex Claim Verification with Evidence Retrieved in the Wild, NAACL: https://aclanthology.org/2024.naacl-long.196/ ; note [[research/2024 - Chen - Complex Claim Verification in the Wild.md]]
- Mu et al. 2023, It's about Time: chronological splits for rumour detection, Findings EACL: https://aclanthology.org/2023.findings-eacl.55/ ; note [[research/2023 - Mu - Chronological Splits Rumor Detection.md]]
- Ji, Sun, Zhang, Li 2023, A Critical Study on Data Leakage in Recommender System Offline Evaluation, TOIS: https://dl.acm.org/doi/10.1145/3569930 ; note [[research/2023 - Ji - Data Leakage in Recommender Offline Evaluation.md]]
- Le, Liu, Medlar, Glowacka 2025, Don't Get Ahead of Yourself: A Critical Study on Data Leakage in Offline Evaluation of Sequential Recommenders, RecSys '25, pp. 1164-1168 (extended abstract): https://dl.acm.org/doi/10.1145/3705328.3759329 ; note [[research/2025 - Le - Don't Get Ahead of Yourself.md]]
- Alkhalifa et al. 2023, Overview of the CLEF-2023 LongEval Lab on Longitudinal Evaluation of Model Performance, CLEF 2023 (LNCS), pp. 440-458: https://link.springer.com/chapter/10.1007/978-3-031-42448-9_28 ; extended overview CEUR-WS Vol-3497 paper 184 ; note [[research/2023 - Alkhalifa - LongEval CLEF 2023 Overview.md]]
- Liska et al. 2022, StreamingQA, ICML (PMLR 162): https://proceedings.mlr.press/v162/liska22a.html ; note [[research/2022 - Liska - StreamingQA.md]]
- Gorman and Bedrick 2019, We Need to Talk about Standard Splits, ACL: https://aclanthology.org/P19-1267/ ; note [[research/2019 - Gorman - We Need to Talk about Standard Splits.md]]
- Søgaard et al. 2021, We Need To Talk About Random Splits, EACL: https://aclanthology.org/2021.eacl-main.156/ ; note [[research/2021 - Sogaard - We Need To Talk About Random Splits.md]]
- Lazaridou et al. 2021, Mind the Gap, NeurIPS: https://proceedings.neurips.cc/paper/2021/hash/f5bf0ba0a17ef18f9607774722f5698c-Abstract.html ; note [[research/2021 - Lazaridou - Mind the Gap.md]]
- El Lahib, Xia, Li, Wang, Pi 2026, Temporal Leakage in Search-Engine Date-Filtered Web Retrieval, ACL 2026 short: https://aclanthology.org/2026.acl-short.65/ ; note [[research/2026 - El Lahib - Temporal Leakage in Date-Filtered Web Retrieval.md]]
- Zhang and Stadie 2026, All Leaks Count, Some Count More: temporal contamination in LLM backtesting, Findings EMNLP: https://aclanthology.org/2026.findings-emnlp.1690/ ; note [[research/2026 - Zhang - All Leaks Count Some Count More.md]]
- Li, Wang, El Lahib, Xia, Pi 2026, Simulated Ignorance Fails: A Systematic Study of LLM Behaviors on Forecasting Problems Before Model Knowledge Cutoff, IJCAI 2026: https://ijcai.org/proceedings/2026/650 ; arXiv 2601.13717 ; note [[research/2026 - Li - Simulated Ignorance Fails.md]]
- Wang et al. 2024, Multilingual E5 Text Embeddings: A Technical Report, arXiv technical report: https://arxiv.org/abs/2402.05672 ; note [[research/2024 - Wang - Multilingual E5.md]]
- Chen et al. 2024, M3-Embedding (BGE-M3), Findings ACL: https://aclanthology.org/2024.findings-acl.137/ ; note [[research/2024 - Chen - M3-Embedding BGE-M3.md]]
- Feng et al. 2022, LaBSE, ACL: https://aclanthology.org/2022.acl-long.62/ ; note [[research/2022 - Feng - LaBSE.md]]
- Zhang et al. 2025, Qwen3 Embedding, arXiv technical report: https://arxiv.org/abs/2506.05176 ; note [[research/2025 - Zhang - Qwen3 Embedding.md]]
- Dadas et al. 2024, PIRB, LREC-COLING: https://aclanthology.org/2024.lrec-main.1117/ ; note [[research/2024 - Dadas - PIRB.md]]
- sdadas/mmlw-retrieval-roberta-large: https://huggingface.co/sdadas/mmlw-retrieval-roberta-large ; note [[research/2023 - Dadas - mmlw-retrieval-roberta-large model card.md]]
- sdadas/polish-reranker-roberta-v3: https://huggingface.co/sdadas/polish-reranker-roberta-v3 ; note [[research/n.d. - Dadas - polish-reranker-roberta-v3 model card.md]]
- BAAI/bge-reranker-v2-m3: https://huggingface.co/BAAI/bge-reranker-v2-m3 ; note [[research/n.d. - BAAI - bge-reranker-v2-m3 model card.md]]
- ACL 2027 call for main conference papers: https://2027.aclweb.org/calls/main/
- SIGIR 2027 dates: https://sigir2027.org/
- ECIR 2027 resource papers call: https://www.ecir2027.co.uk/call-for-resource-papers
- FEVER workshop: https://fever.ai/
- NLP4PI 2026 proceedings: https://aclanthology.org/2026.nlp4pi-1.0.pdf
