---
title: "Phase 1 feedback"
type: handbook
domain: vault
parent: "[[temporal-fact-checked-retrieval-eval]]"
tags: [handbook, course, feedback, report, grading]
created: 2026-11-11
related:
  - "[[Course grading and report]]"
  - "[[2026-11-11-phase1-feedback-response]]"
---
# Phase 1 feedback

Reviewer's assessment of the 4.11 proposal (resubmitted 7.11, checkpoint 1: `report/checkpoint_1/`). Items keep the reviewer's wording in short form; ids (F1, ...) are used by the response plan and the rebuttal.

## Score

| Criterion | Points | Max |
|---|---|---|
| 1.1 State of the art | 1.5 | 3 |
| 1.2 Datasets and status | 1.5 | 3 |
| 1.3 Solution concept and plan | 1 | 2 |
| 1.4 Text quality and references | 0.5 | 1 |
| 1.5 Data statement | 1 | 1 |
| **Total** | **5.5** | **10** |

No formal penalty; exceptional-research point 0/1 (needs a completed, verifiable contribution beyond the rubric). Two corrections are mandatory before final approval: F25 (judge validation) and F24 (name the LLM tools).

Rules cross-check: see [[Course grading and report]] and the last table of [[Review verification]]. Instructor's announcement (11.11): a meeting with the supervisor to discuss this report is mandatory for every team; propose time slots (Friday, 7-hour shift, or another day) and prepare corrections for Phase 2.

## Findings

### 1.1 State of the art

- F1: Table 1 claims "every value names the dataset and the split"; rows missing a split: Pikuliak 0.83 (unsupervised numbers use all post-fact-check pairs, no held-out split; say so), Ramponi 0.804 (which partition of 80-10-10), Vykopal 82.46, Glockner 69.7%, Ounis P@30 (topic set).
- F2: Schlichtkrull macro-F1 0.23/0.49 is labelled "AVeriTeC test"; the paper's baseline analysis is on the development set (check its Tables 3-4).
- F3: mixed scales (0-1 and 0-100); use one.
- F4: Aschern CheckThat! 2021 is 0.883 (MAP@5, Shaar 2021) in one place and 88.2 (vs Hardalov) in another; reconcile or explain.
- F5: novelty claim "No PFCR evaluation we found restricts the fact-check index per query" needs a stated search protocol (databases, queries, date).
- Praise: 15 works genuinely described; spot-checked numbers correct.

### 1.2 Datasets and status

- F6: class balance is not a number ("sparse positives"); give gold pairs per post, gold fact-checks per post, share of fact-checks with at least one linked post, per dataset.
- F7: Polish and English subset sizes missing (posts, pairs, fact-checks, dated ones) for MultiClaim v1/v2; estimate the Polish answerable count from data at hand.
- F8: datasets the team creates (causal split id lists, 50 hand-coded failure annotations) need rows labelled TO COLLECT with size, label definition (failure-code scheme), date, annotator (plan: Florek/Cwalina, W3).
- F9: AMC-16K is RESTRICTED "to be requested" with no request date; the topic card asked for requests in October.
- F10: licence column describes access terms; name the actual terms document (Zenodo conditions) and say whether redistributing id lists is allowed.

### 1.3 Solution concept and plan

- F11: no primary metric; designate one metric and condition for the central claim, e.g. S@10, unconditional, difference-in-differences PL vs EN, before results.
- F12: plan is four two-week blocks with one owner for heterogeneous tasks; make it weekly with one owner per task.
- F13: fourth system undecided ("mmlw / LaBSE") and absent from W2; commit to one model and schedule it (card requires four systems).
- F14: Figure 1 lacks the per-query date filter P(q), the size-matched control and the bootstrap.
- F15: RQ4 (LLM rerankers, core+) has no metric, data or owner; plan it or drop it.

### 1.4 Text quality and references

- F16: undefined abbreviations: DPR, PoC, LDS, CLEF, TREC, KInIT, WUT, LaBSE, mmlw, GTR, RIET, rankSVM, "EN 2A", "core+".
- F17: Ramponi et al. 2025 pages are 29045-29064 (DOI 10.18653/v1/2025.emnlp-main.1480), not 29057-29076.
- F18: Chen et al. 2024 uses the arXiv title "BGE M3-embedding ..." with the Findings of ACL venue; published title "M3-Embedding: Multi-Linguality, Multi-Functionality, Multi-Granularity Text Embeddings Through Self-Knowledge Distillation".
- F19: citations used as sentence subjects should be textual (`\citet`).
- Praise: 1 of 19 references preprint-only.

### 1.5 Data statement

- Full credit. Phase 2 improvement (F20): state that no per-outlet or per-author error ranking will be published.

### Further revisions and checks

- F21: restore the template credit line "Template: Anna Wróblewska (Warsaw University of Technology), adapted from the ACL 2015 ..." under the author block.
- F22: define handling of tied timestamps, uncertain original publication dates and missing earlier sibling fact-checks in the causal pool (Sec. 4).
- F23: add the card's gap factors (time lag between post and debunk, lexical overlap, narrative drift) to the decomposition, or justify replacing them; RQ2 currently lists answerability, pool size, training leakage, missing sibling labels.
- F24: name every LLM tool and model in the declaration (Section 7); contribution table (added 7.11) is accepted; in Phase 2 give concrete tasks, not role areas.
- F25: mandatory: "AMC-16K is secondary (LLM-judge validation only)" but no judge appears in the plan; remove it or specify judge model, prompt, output labels and validation against the human Yes/No labels (sample size, agreement measure, acceptance threshold).
- F26: H1 (most gold pairs are post-before-fact-check) implies the strict pool holds no gold item for most queries, so unconditional numbers mostly measure answerability; report the per-language answerable rate as the first Phase 2 result.
- F27: cite the published language-bias analysis the card puts out of scope, to delimit the contribution.
- F28: document restricted-data authorisations; distinguish prespecified from formally preregistered analysis (the report says "pre-registered").
- F29: test temporal, full-index and size-matched controls on equal query sets; quantify future-information leakage with matched historical and size-matched controls.
- F30: Phase 2 needs a rebuttal answering every point and naming where each fix is made (criterion 2.4) and an extended SOTA table (2.5) including the works below.

### Questions for the rebuttal

- Q1: how are tied publication dates, missing historical fact-checks and uncertain timestamps handled?
- Q2: can you show the effect of a strictly time-respecting index against an unrestricted index and a size-matched control?

### Suggested literature (verify metadata before citing)

| Work | Why |
|---|---|
| Vykopal et al. 2026, language and retrieval bias in multilingual PFCR, EACL 2026 long, pp. 5195-5221, 10.18653/v1/2026.eacl-long.240 | the published language-bias analysis; delimits scope; PL-vs-EN confound |
| Søgaard et al. 2021, We Need To Talk About Random Splits, EACL, pp. 1823-1832, 10.18653/v1/2021.eacl-main.156 | random splits overestimate performance |
| Kazemi et al. 2021, Claim Matching Beyond English, ACL-IJCNLP, pp. 4504-4517, 10.18653/v1/2021.acl-long.347 | multilingual claim matching |
| Alkhalifa et al. 2023, CLEF-2023 LongEval overview, LNCS, pp. 440-458, 10.1007/978-3-031-42448-9_28 | time-stamped snapshots benchmark |
| Urbano et al. 2019, Statistical Significance Testing in IR, SIGIR, pp. 505-514, 10.1145/3331184.3331259 | justifies paired bootstrap and resample count |

## Reviewer remarks to verify

The review states some facts about the report and sources; the response plan checks each against the text and the papers before acting.
