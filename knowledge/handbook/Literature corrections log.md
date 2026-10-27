---
title: "Literature corrections log"
type: handbook
domain: vault
parent: "[[temporal-fact-checked-retrieval-eval]]"
tags: [handbook, literature, corrections]
created: 2026-10-27
updated: 2026-10-27
related:
  - "[[Research]]"
  - "[[Proposed Task]]"
---
# Literature corrections log

Errors and unsupported claims in the first pass of [[Enhanced topic research]], checked against primary sources on 2026-10-27.

| Claim in first pass | Correction | Paper note |
|---------------------|------------|------------|
| Polish and Turkish were the weakest languages for most teams. | Overstated. The overview says the two unseen languages score generally lower than training languages; in the per-language table Polish is among the lowest for top teams, together with English (PINGAN AI English 0.9160, Polish 0.9260, Turkish 0.9480). | [[SemEval-2025 Task 7]] |
| Top systems used embedder ensembles, per-language fine-tuned rerankers and LLM reranking, PINGAN AI first. | PINGAN AI (mono avg Success@10 0.9601, cross 0.85875) published no system description. Per-language reranker ensembles are QUST_NLP, LLM reranking with RRF is TIFIN India, RACAI uses one fine-tuned LLM-based embedder without reranking. | [[SemEval-2025 Task 7]], [[TIFIN India]] |
| Performance falls as pool size grows (MultiClaim). | Not supported. MultiClaim added random fact-checks (100 to 2,100) and found the BM25-versus-TEM gap depends on pool size; an absolute decline is not stated. Expect higher scores in smaller pools and test it with the size-matched control. | [[MultiClaim]] |
| The pool-size-matched control is unprecedented. | MultiClaim already ran a global pool-size sweep; no prior PFCR work matched pool size per query to a time-restricted pool. | [[MultiClaim]] |
| Chronological splits exist only for rumour detection. | Shaar et al. (Findings NAACL 2022) compared chronological and random splits for PFCR on PolitiFact debates (MAP 0.602 random, 0.429 chronological), with training split only and no date-restricted index. Cite as precedent. | [[Role of Context in PFCR]] |
| CheckThat! 2020-2022 Task 2 used random 70/15/15 English splits. | The 70/15/15 split (999/200/202) is English 2A in 2021; "random" is stated only for Arabic. 2B (debates vs PolitiFact) was omitted; 2022 added a 209-tweet test set; no date restriction of the pool is described; 2020 was not verified. | [[CheckThat 2021 Task 2]], [[CheckThat 2022 Task 2]] |
| Prior Polish PFCR evidence is the SemEval slice and MultiClaim tables. | Also AMC-16K (400 Polish pairs plus crosslingual Polish pairs, lower LLM performance on Polish) and Polish among 47 languages in Ramponi et al. 2025. | [[AMC-16K]], [[Multilingual vs Crosslingual Retrieval]] |
| Polish fact-check sources with at least 50 items: demagog.org.pl, oko.press, sprawdzam.afp.com. | Incomplete: fakenews.pl (320) also qualifies; Konkret24 was not in the rows read. | [[MultiClaim]] |
| `backlink` pairs are post-first by construction; text-identity pairs are not fact-checker links. | Not defined in the v2 record; treat as assumptions to confirm from the data or the authors. | [[MultiClaim Zenodo Records]] |
| SemEval train/dev come from 8 monolingual languages. | Correct for the monolingual track; crosslingual train/dev covers 14 languages (52 combinations). All MultiClaim posts predate 2023, so the test is out-of-time. | [[SemEval-2025 Task 7]] |
| MultiClaim has 31,305 pairs. | Correct, but the stated monolingual (26,774) plus crosslingual (4,212) counts sum to 30,986; recount after data access. | [[MultiClaim]] |
| IR temporal persistence: performance drops as test data moves away from training time (LongEval). | That is the lab's motivation. In 2023 the NDCG change was system-dependent, not a uniform drop. | [[LongEval 2023]] |
| Split methodology: random splits overestimate, prefer biased or time-based splits (Gorman and Bedrick; Søgaard et al.). | Gorman and Bedrick argue for random over standard splits and for significance testing; Søgaard et al. show random splits overestimate and recommend independent test samples, else biased or adversarial splits, not time-based ones. | [[We Need to Talk about Standard Splits]], [[We Need to Talk about Random Splits]] |
| Simulated ignorance does not replicate true ignorance (arXiv). | Now published at IJCAI 2026 (Li, Wang, El Lahib, Xia, Pi); the published abstract reports 470 questions, arXiv v1 reports 477. | [[Simulated Ignorance Fails]] |
| AVeriTeC: evidence must predate the claim. | Also orders train, dev and test temporally; the guarantee is approximate (about 6% of dev answers come from fact-checking domains), which supports sibling qrels. | [[AVeriTeC]] |
| Time-respecting evaluation is new for PFCR. | TREC 2011 Microblog ran query-time evaluation with a compulsory no-future-evidence run; StreamingQA is a rolling-origin precedent. The PFCR-specific claim holds. | [[TREC 2011 Microblog]], [[StreamingQA]] |
| The leakage taxonomy is complete. | Missing statistics leakage: IDF, vocabulary or normalisation computed over the full pool including future fact-checks. Rebuild BM25 statistics per cutoff. | [[TREC 2011 Microblog]] |
| mmlw-retrieval-roberta-large has PIRB NDCG@10 58.46. | 58.46 is the model card figure; the PIRB paper reports 58.06 for the distilled and fine-tuned model, and multilingual-e5-large scores 57.29, so the margin is about 1 point. Cross-lingual Polish-to-English retrieval is plausible but unreported. | [[mmlw-retrieval-roberta-large]], [[PIRB]] |
| Reranker licences are unremarkable. | polish-reranker-roberta-v3 carries the gemma licence (443M parameters, PIRB reranker NDCG@10 66.21); check before releasing derived artefacts. bge-reranker-v2-m3 is Apache-2.0. | [[polish-reranker-roberta-v3]], [[bge-reranker-v2-m3]] |
| Multilingual E5 and Qwen3 Embedding are cited as papers. | Both are arXiv technical reports without a peer-reviewed venue; label them so. | [[Multilingual E5]], [[Qwen3 Embedding]] |
| Don't Get Ahead of Yourself cited as RecSys 2025 work. | Full citation: Le, Liu, Medlar, Glowacka, RecSys '25, pp. 1164-1168 (extended abstract). | [[Dont Get Ahead of Yourself]] |
| LongEval cited by its lab website. | Cite the overview: Alkhalifa et al., CLEF 2023 (LNCS), pp. 440-458. | [[LongEval 2023]] |
| Reference entries lacked authors (El Lahib et al.; Zhang and Stadie). | Add El Lahib, Xia, Li, Wang, Pi 2026 and Zhang and Stadie 2026 (aclanthology.org/2026.findings-emnlp.1690). | [[Temporal Leakage in Date-Filtered Web Retrieval]], [[All Leaks Count]] |
| Venue: ARR deadline 4 Jan 2027 per a deadline aggregator. | Date correct; official source is the ACL 2027 call (Kyoto, 17-22 August 2027). | none (venue item) |
| Venue: SIGIR 2027 short or resource deadlines. | Full-paper deadline 21 Jan 2027 correct; abstract deadline 14 Jan 2027, notification 5 April 2027, conference 18-24 July 2027, San Jose. | none (venue item) |
| Venue: ECIR 2027 resource deadline 2 Nov 2026 too close. | Correct (notification 7 Dec 2026, conference 21-25 March 2027, Southampton); full-paper and reproducibility deadlines have passed. | none (venue item) |
| Venue: FEVER is ACL co-located. | Co-location varies (ACL 2025, EACL 2026); no 2027 call found on 2026-10-27. | none (venue item) |
| Venue: a future CLEF lab proposal. | CLEF 2027 proposals closed on 17 July 2026; the earliest new lab is CLEF 2028, or join an existing 2027 lab (LongEval, CheckThat!). | none (venue item) |

## Confirmed without change

- Task definition of Shaar et al. 2020 [[That is a Known Lie]]; CheckThat! 2025 has no PFCR task ([[CheckThat 2026]]).
- MultiClaim counts (205,751 fact-checks, 28,092 posts) and the post-newer versus post-older result (80.02 versus 80.04 Success@10) [[MultiClaim]].
- MultiClaim v2 sizes and dates [[MultiClaim Zenodo Records]]; MultiClaimNet counts [[MultiClaimNet]]; Vykopal et al. language bias [[Language and Retrieval Bias]].

## Prior causal-index search

- No PFCR paper found that evaluates with a date-restricted index. Closest: the chronological training split of [[Role of Context in PFCR]], date filtering as a retrieval criterion in [[Generative-AI Claim Retrieval]] (worst-performing filter, not a protocol), and MultiClaim's post-newer versus post-older test.
- The novelty claim holds as far as the search reached, but must cite those precedents.
