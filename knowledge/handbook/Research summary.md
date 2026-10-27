---
title: "Research summary"
type: handbook
domain: vault
parent: "[[temporal-fact-checked-retrieval-eval]]"
tags: [handbook, research, literature, novelty, temporal-evaluation]
created: 2026-10-27
updated: 2026-10-27
---
# Research summary

Literature state for the causal PFCR evaluation in [[Proposed Task]], after verification of every cited source on 2026-10-27. Full evidence, method and references: [[Enhanced topic research]]; language set: [[Language scope analysis]]; corrections: [[research/CORRECTIONS-A.md]], [[research/CORRECTIONS-B.md]].

## State of the art by area

### Previously fact-checked claim retrieval (PFCR)

- Task defined by Shaar et al. (ACL 2020) on Snopes tweets and PolitiFact debate sentences.
- CheckThat! 2021-2022 Task 2 ran PFCR on tweets (English, Arabic) and debates (English) with fixed splits and no date-restricted pool.
- CheckThat! 2025 and 2026 have no PFCR task.
- MultiClaim (EMNLP 2023) is the reference multilingual dataset: 205,751 fact-checks, 39 languages, 28,092 posts, 31,305 pairs.
- MultiClaim v2 (Zenodo 2025) grows to 435k fact-checks, 89k posts, 105k pairs, with three relationship types.
- SemEval-2025 Task 7 tested on out-of-time posts (to March 2024) against a pool reaching May 2024; Polish and Turkish were unseen languages.
- Best SemEval-2025 Task 7 score: PINGAN AI, mono avg S@10 0.9601, cross 0.85875, with no system description.
- Described strong recipes: translation plus fine-tuned embedders with hard negatives, LLM reranking of the top 50 with RRF, per-language reranker ensembles, or one fine-tuned LLM-based embedder.
- Ramponi et al. (EMNLP 2025) find LLM reranking best on a 47-language v2 subset, with random stratified splits.
- AMC-16K (Findings EMNLP 2025) adds 16K human-labelled pairs in 20 languages, including 400 Polish monolingual pairs.
- MultiClaimNet (Findings EMNLP 2025) clusters 85.3K fact-checked claims into 30.9K clusters from LLM similarity labels.
- Language and retrieval bias in PFCR is already published (Vykopal et al., EACL 2026).

### Temporal evaluation of PFCR

- Shaar et al. (Findings NAACL 2022) compared chronological and random splits on PolitiFact debates: reranker MAP 0.602 (sentence random) down to 0.429 (debate chronological).
- That split restricts training data only; no date-restricted verified-claim pool is described.
- MultiClaim ran three temporal analyses over the full index: post-newer vs post-older pairs (80.02 vs 80.04 S@10), post-date quantiles, and a random pool-size sweep (100 to 2,100).
- KInIT's claim retrieval system (arXiv 2504.20668) supports date-range filtering as a retrieval feature, not as an evaluation protocol.
- No PFCR evaluation found restricts the fact-check index to documents published before each query.

### Time-respecting IR and QA

- TREC 2011 Microblog required runs without future evidence, including IDF computed on documents posted after the query.
- StreamingQA (ICML 2022) evaluates dated questions against a growing time-stamped corpus.
- LongEval (CLEF 2023 onward) evaluates on successive collection snapshots; the 2023 change in NDCG was system-dependent, not a uniform drop.

### Temporal leakage in verification and other fields

- Glockner et al. (EMNLP 2022): verification evidence leaks from fact-check articles.
- AVeriTeC (NeurIPS 2023): evidence must predate the claim, splits are temporal, and the guarantee is approximate (about 6% of dev answers from fact-checking domains).
- Chen et al. (NAACL 2024): temporal and fact-check-site constraints sharply reduce veracity accuracy.
- Mu et al. (Findings EACL 2023): random splits overestimate rumour detection.
- Recommender systems: Ji et al. (TOIS 2023) and Le et al. (RecSys 2025) show timeline leakage in offline evaluation.
- LLM contamination: date-filtered web search leaks (ACL 2026 short), claim-level leak auditing (Findings EMNLP 2026), simulated ignorance fails (IJCAI 2026).

### Split methodology

- Gorman and Bedrick (ACL 2019) argue for random over standard splits.
- Søgaard et al. (EACL 2021) rebut them: random splits over-estimate; prefer independent new samples, else biased or adversarial splits.
- Lazaridou et al. (NeurIPS 2021) show temporal degradation of language models.

### Models

- Multilingual dense: mE5 (arXiv technical report) and BGE-M3 (Findings ACL 2024).
- Polish retrieval: mmlw-retrieval-roberta-large scores NDCG@10 58.46 on the PIRB card (58.06 in the paper), about 1 point above mE5-large (57.29).
- Rerankers: bge-reranker-v2-m3 (Apache-2.0) and polish-reranker-roberta-v3 (licence "gemma", PIRB 66.21).
- LLM scale: Qwen3 Embedding and Reranker (arXiv technical report, June 2025, no stated training cutoff).

## Novelty map

| Claim | Closest prior work | What remains new | Confidence |
|---|---|---|---|
| Causal (date-restricted) index for PFCR evaluation | TREC 2011 Microblog (general IR); Shaar et al. 2022 (chronological training split); MultiClaim post-newer/older test | First per-query date-restricted fact-check pool for PFCR | Medium-high: searches found none; Shaar 2022 read via arXiv and excerpt |
| Separating answerability from ranking quality | Glockner et al. 2022 (counter-evidence unavailable for new claims) | Answerable rate plus conditional and unconditional scores for PFCR | High |
| Pool-size-matched control | MultiClaim random pool-size sweep (100 to 2,100) | Matching pool size per query to a time-restricted pool | High for the narrow claim; the general control is not new |
| Statistics leakage (corpus statistics from future documents) | TREC 2011 Microblog "future evidence" rule | Measuring it for PFCR (BM25 full-pool vs causal-pool statistics) | Medium: the concept is old, the measurement is new |
| Training-time leakage (random vs chronological training) | Shaar et al. 2022 (English debates); Mu et al. 2023 (rumours) | Multilingual social-media PFCR, separated from index and answerability effects | Medium |
| Cluster-expanded qrels for earlier siblings | AVeriTeC (earlier fact-checks as legitimate evidence); MultiClaimNet clusters; AMC-16K extra labels | Sibling relevance as a causal-protocol label set for PFCR | Medium-high |
| Time-to-findability metric | StreamingQA and LongEval (time-indexed evaluation) | Days from post until a debunk is retrievable in the top 10 | High |
| Additive gap decomposition | None found | Random to causal chain with paired-bootstrap deltas per component | High |
| Parametric leakage of LLM rerankers on PFCR | Simulated Ignorance Fails; Zhang and Stadie 2026 | Pre- vs post-cutoff query strata on PFCR | Medium |
| Polish-English DiD plus archive-density dose-response | SemEval-2025 Polish slice; AMC-16K Polish; Vykopal et al. 2026 (language bias) | Within-language causal penalty as a function of archive density | Medium; needs supervisor sign-off for extra languages |

## What is NOT claimable

- Time-respecting retrieval evaluation as an idea (TREC 2011 Microblog).
- The first temporal or chronological evaluation of PFCR (Shaar et al. 2022).
- The first pool-size control in PFCR (MultiClaim).
- The first out-of-time PFCR test set (SemEval-2025 Task 7).
- The first rolling or streaming evaluation over a growing corpus (StreamingQA, LongEval).
- Any language-bias finding, or a ranking of languages by absolute score (Vykopal et al., EACL 2026).
- That MultiClaim shows absolute scores fall as the pool grows; it shows the BM25-vs-TEM gap changes.
- That Polish and Turkish were the weakest SemEval languages for most teams; English is as low for several top teams.
- PINGAN AI's method; it is undocumented.
- Polish-to-English quality of mmlw-retrieval-roberta-large; unreported, to be measured.

## Corrections log

- Chronological PFCR splits were described as absent; Shaar et al. 2022 already compared chronological and random splits.
- TREC 2011 Microblog and StreamingQA were missing as precedents for time-respecting evaluation.
- The leakage taxonomy lacked statistics leakage; added with the mitigation of computing BM25 statistics from the causal pool only.
- The pool-size control was called unprecedented; MultiClaim ran a random pool-size sweep.
- MultiClaim was said to show performance falling with pool size; it shows a changing BM25-vs-TEM gap.
- SemEval-2025 top-system methods were attributed to PINGAN AI, which published no description.
- "Polish and Turkish weakest for most teams" was overstated.
- CheckThat! 2021 English splits were called random; the overview says "randomly" only for Arabic, and Subtask 2B (debates) was omitted.
- Prior Polish PFCR evidence omitted AMC-16K and Ramponi et al. 2025.
- The Polish source list omitted fakenews.pl (320).
- v2 relationship semantics (`backlink`, `similarity:identical`, Meta-warning mapping) were stated as facts; they are assumptions.
- SemEval crosslingual train/dev (14 languages) and the pre-2023 MultiClaim post dates were missing.
- MultiClaim pair counts: 31,305 total vs 30,986 from the mono plus cross split; footnoted.
- LongEval was cited for a uniform performance drop; the 2023 change was system-dependent.
- Gorman and Bedrick were grouped with "random splits overestimate"; they argue the opposite.
- Søgaard et al. were said to recommend time-based splits; they recommend independent samples, else biased or adversarial splits.
- Simulated Ignorance Fails was cited as arXiv only; it is IJCAI 2026.
- The mmlw 58.46 figure is the model card's; the PIRB paper reports 58.06.
- mE5 and Qwen3 Embedding are technical reports, not peer-reviewed papers.
- FEVER was called ACL-co-located; its co-location varies (EACL 2026).
- A CLEF task proposal was framed as open; CLEF 2027 proposals closed on 17 July 2026, so CLEF 2028 is the earliest.
- Reference entries lacked authors or cited a website instead of the paper (LongEval, RecSys 2025, ACL 2026 short, Findings EMNLP 2026, TOIS 2023).

## Per-paper index

Verdicts: OK (claim confirmed), CORRECTED (the note's claim was fixed), MISSED (prior work the first pass did not cite).

| Note | Takeaway | Verdict |
|---|---|---|
| [[research/2011 - Ounis - TREC 2011 Microblog Track Overview.md]] | Query-time retrieval with a ban on future documents and future IDF; origin of the causal idea and of statistics leakage | MISSED |
| [[research/2019 - Gorman - We Need to Talk about Standard Splits.md]] | Argues for random over standard splits; cite as the position Søgaard et al. rebut | CORRECTED |
| [[research/2020 - Shaar - That is a Known Lie.md]] | Defines PFCR; Snopes tweets come from fact-check bodies, so gold is post-first by construction | OK |
| [[research/2021 - Kazemi - Claim Matching Beyond English.md]] | Multilingual claim matching; claims recur, motivating sibling relevance; not temporal | OK |
| [[research/2021 - Lazaridou - Mind the Gap.md]] | Temporal generalization of LMs; background for parametric leakage | OK |
| [[research/2021 - Shaar - CheckThat 2021 Task 2 overview.md]] | Tweets and debates PFCR with fixed splits; no date-restricted pool | CORRECTED |
| [[research/2021 - Sogaard - We Need To Talk About Random Splits.md]] | Random splits over-estimate; prefer independent samples, else biased splits | CORRECTED |
| [[research/2022 - Feng - LaBSE.md]] | Classic cross-lingual baseline; weak on asymmetric retrieval | OK |
| [[research/2022 - Glockner - Missing Counter-Evidence.md]] | Verification evidence leaks from later fact-checks; motivates answerability | OK |
| [[research/2022 - Hardalov - CrowdChecked.md]] | Distant supervision for PFCR with training data newer than the test set | OK |
| [[research/2022 - Liska - StreamingQA.md]] | Dated questions over a growing corpus; precedent for rolling-origin | MISSED |
| [[research/2022 - Nakov - CheckThat 2022 Task 2 overview.md]] | New 2022 test set on older training data; no pool restriction | OK |
| [[research/2022 - Shaar - Role of Context in PFCR (chronological split).md]] | Chronological PFCR split already exists (MAP 0.602 to 0.429); training split only | MISSED |
| [[research/2023 - Alkhalifa - LongEval CLEF 2023 Overview.md]] | Snapshot-based temporal IR evaluation; system-dependent change, not a uniform drop | CORRECTED |
| [[research/2023 - Dadas - mmlw-retrieval-roberta-large model card.md]] | Polish retriever; 58.46 is the card figure, 58.06 the paper's | CORRECTED |
| [[research/2023 - Ji - Data Leakage in Recommender Offline Evaluation.md]] | Timeline leakage reorders recommenders; analogue of index leakage | OK |
| [[research/2023 - Mu - Chronological Splits Rumor Detection.md]] | Random splits overestimate rumour detection; supports H5 | OK |
| [[research/2023 - Pikuliak - MultiClaim.md]] | Three temporal analyses over the full index; pool-size sweep is global, not per query | CORRECTED |
| [[research/2023 - Schlichtkrull - AVeriTeC.md]] | Pre-claim evidence constraint and temporal splits; earlier fact-checks count as evidence | OK |
| [[research/2024 - Chen - Complex Claim Verification in the Wild.md]] | Web verification works largely by finding later fact-checks | OK |
| [[research/2024 - Chen - M3-Embedding BGE-M3.md]] | Dense, sparse and multi-vector baseline; base of bge-reranker-v2-m3 | OK |
| [[research/2024 - Dadas - PIRB.md]] | Polish retrieval benchmark; Polish model about 1 point above mE5-large | OK |
| [[research/2024 - Wang - Multilingual E5.md]] | Main dense baseline; arXiv technical report | OK |
| [[research/2025 - Devadiga - TIFIN India at SemEval-2025 Task 7.md]] | Translate, fine-tune with hard negatives, LLM rerank top 50; leakage-testable recipe | OK |
| [[research/2025 - KInIT - MultiClaim v1 and v2 Zenodo records.md]] | Per-instance timestamps exist; semantics, time zone and `backlink` undefined | OK |
| [[research/2025 - Le - Don't Get Ahead of Yourself.md]] | Recsys temporal leakage with a training-size control; extended abstract | OK |
| [[research/2025 - Panchendrarajan - MultiClaimNet.md]] | Claim clusters from LLM similarity; enabler for sibling qrels | OK |
| [[research/2025 - Peng - SemEval-2025 Task 7 overview.md]] | Out-of-time test, pool to May 2024; PINGAN AI undocumented; Polish not uniquely weakest | CORRECTED |
| [[research/2025 - Ramponi - Multilingual vs Crosslingual Retrieval of Fact-Checked Claims.md]] | LLM reranking best on v2; random stratified splits | OK |
| [[research/2025 - Vykopal - Generative-AI-Driven Claim Retrieval System.md]] | Date range as a retrieval filter, not an evaluation protocol | MISSED |
| [[research/2025 - Vykopal - LLMs for Multilingual PFCD (AMC-16K).md]] | 16K human labels incl. Polish; validates the sibling-qrel judge | OK |
| [[research/2025 - Zhang - Qwen3 Embedding.md]] | LLM-scale retriever and reranker; most exposed to parametric leakage | OK |
| [[research/2026 - El Lahib - Temporal Leakage in Date-Filtered Web Retrieval.md]] | Date filters leak via updated pages; supports timestamp leakage | OK |
| [[research/2026 - Li - Simulated Ignorance Fails.md]] | Prompting an LLM to forget does not work; stratify by cutoff instead | CORRECTED |
| [[research/2026 - Struss - CheckThat 2026 lab overview.md]] | No PFCR task in 2025-2026 | OK |
| [[research/2026 - Vykopal - Language and Retrieval Bias in Multilingual PFCD.md]] | Language and popularity bias already published; avoid language-bias framing | OK |
| [[research/2026 - Zhang - All Leaks Count Some Count More.md]] | Claim-level temporal leak auditing in LLM backtesting | OK |
| [[research/n.d. - BAAI - bge-reranker-v2-m3 model card.md]] | Multilingual cross-encoder reranker, Apache-2.0 | OK |
| [[research/n.d. - Dadas - polish-reranker-roberta-v3 model card.md]] | Polish reranker, 8K context, gemma licence | OK |

## Open questions

- Does Shaar et al. 2022 restrict its verified-claim pool by date anywhere in the full paper?
- Was CheckThat! 2020 Task 2 split or indexed by time?
- What do the v1 and v2 timestamps mean: publication, crawl or last update, and in which time zone?
- How is `backlink` defined in v2, and where did v1 Meta-warning pairs go?
- Does "published before April 2025" in v2 bound fact-checks or only posts?
- Why do MultiClaim's mono and cross pair counts sum to 30,986, not 31,305?
- How large is statistics leakage for BM25 on PFCR pools in practice?
- What are the training-data cutoffs of mE5, BGE-M3 and Qwen3 for the parametric strata?
- Does the gemma licence of polish-reranker-roberta-v3 allow releasing derived qrels?
- Will the supervisor approve the five extra languages of [[Language scope analysis]]?
- Is a FEVER 2027 workshop announced, and when is the CLEF 2028 lab proposal deadline?
