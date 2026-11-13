---
title: "Review verification"
type: plan-note
domain: vault
parent: "[[2026-11-11-phase1-feedback-response]]"
tags: [review, feedback, verification, report]
created: 2026-11-11
updated: 2026-11-11
related:
  - "[[Phase 1 feedback]]"
  - "[[Literature corrections]]"
  - "[[Original Task]]"
---
# Review verification

Each item of [[Phase 1 feedback]] checked on 2026-11-11 against `report/checkpoint_1/report.tex` (`L` = line), `mybib.bib`, the paper notes in `research/` and the primary source (ACL Anthology, arXiv, Springer, ACM DL). Verdicts: CORRECT, PARTLY, INCORRECT, UNVERIFIABLE.

## Findings

| ID | Verdict | Evidence | Action |
|---|---|---|---|
| F1 | CORRECT | L71 promises a split for every value; caption L108 softens it to "split or evaluation condition". Pikuliak 0.83 is unsupervised: computed on all 31k pairs, no held-out split (paper Sec. 4). Ramponi 0.8042 is the test partition ([[Multilingual vs Crosslingual Retrieval]]); its pool (test split or all 52,911 claims) is unchecked. Vykopal 82.46: AMC-16K has no split, it is the full 8k monolingual half. Glockner 69.7%: all 16,244 MultiFC misinformation claims. Ounis: 49 judged topics of 50. | Name the condition per row; X1 |
| F2 | CORRECT | arXiv 2305.13117 v3: only train and dev were released at submission and the test split was private. Retrieval analysis is "on the development set". Tables 3-4 do not name the split. L94, L135 say "test". | Relabel as dev |
| F3 | CORRECT | 0-100 at L123 (80.02), L125 (90.3), L127 (82.46), L137 (91.5/47.2); 0-1 elsewhere. | One scale (0-1) |
| F4 | CORRECT | Both values are faithful: CheckThat! 2021 overview gives Aschern 0.883 ([[CheckThat 2021 Task 2]]); Hardalov et al. Table quotes Aschern 88.2 ([[CrowdChecked]]). | Footnote: two sources, keep overview value |
| F5 | CORRECT | `research/protocols/` holds only `example.yaml`. The search exists only as prose in [[Literature corrections]] ("Prior causal-index search"), with no databases, queries or date. | Protocol YAML, cite in report |
| F6 | CORRECT | L157-159 say "sparse positives". The AMC-16K row has numbers (16%, PL 20.25%). | Compute (plan Task 2) |
| F7 | PARTLY | SemEval PL counts are given (L159: 500 posts / 564 pairs). MultiClaim v1/v2 PL/EN are missing. The v1 counts are published and already in [[Language scope]]: PL 453 posts / 6,912 FC, EN 7,307 / 85,814. | Fill published counts now; v2 and dated counts from data |
| F8 | CORRECT | Criterion 1.2 requires, for TO COLLECT, how many items, by when and who annotates ([[Course grading and report]]). Caption L150 omits derived annotations. The failure codebook exists in the internal plan (sec. Failure analysis). | Add TO COLLECT rows |
| F9 | PARTLY | Correct: there is no request date (L161, L234) and the vault has no record of a sent request. Wrong: the card's October request is the MultiClaim Zenodo request ("request access in October rather than November", [[Original Task]]). That request is done: access is granted (L231). The card lists AMC-16K as a secondary set with no deadline. | Send request; log date |
| F10 | PARTLY | Holds for 3 rows ("research use only"). AMC-16K (CC BY-NC-SA 4.0) and MultiClaimNet (CC BY 4.0) name real licences. L235 still has a TODO to paste the clauses. | Quote Zenodo conditions; ask about id-list release |
| F11 | PARTLY | A central quantity is named (L210: "extra Polish temporal cost", DiD at L182). The metric (S@10 or MRR) and the condition (unconditional or answerable) are not fixed. | Fix primary: S@10, unconditional, DiD |
| F12 | PARTLY | W4 is one week (16-23 Dec), so the plan is not four two-week blocks. Each block has one lead plus helpers (L218-224). | Weekly, one owner per task |
| F13 | CORRECT | L171 "mmlw / LaBSE"; W2 (L219) lists BM25, dense and reranker only. | Commit to one model, schedule it |
| F14 | PARTLY | Wrong part: the size-matched control is in Figure 1 (L193: "Protocols: random / causal / size-matched"). Right part: P(q) and the bootstrap are absent. | Add P(q), bootstrap |
| F15 | CORRECT | RQ4 (L63) appears only as "core+ only if time remains" (L223). | Drop to future work or plan |
| F16 | PARTLY | DPR, PoC, LDS, CLEF, TREC, KInIT, WUT, LaBSE, mmlw, GTR, rankSVM and "EN 2A" are undefined. "RIET Lab" is a team name, not an abbreviation. "core+" is glossed at L63. | Expand or drop |
| F17 | CORRECT | Anthology: pp. 29045-29064, DOI 10.18653/v1/2025.emnlp-main.1480; bib has 29057-29076. The note `venue` field has the same error. | Fix bib and note |
| F18 | CORRECT | Anthology title "M3-Embedding: Multi-Linguality, ...", Findings ACL 2024, pp. 2318-2335. The bib has the arXiv title "BGE M3-Embedding: Multi-Lingual...". | Fix bib |
| F19 | PARTLY | Citation-as-subject is real (L75-94). `\citet` is wrong for this template: natbib is not loaded, and acl2015.sty defines `\newcite` (L215). | Use `\newcite` |
| F20 | CORRECT | Data statement says only "errors aggregated" (L233); the card demands no ranked outlet list. | Add sentence |
| F21 | PARTLY | The line is in the course template (`project-proposal.tex` L45). "Restore" is wrong: `report.tex` never had it (absent in a4d4def 4.11 and 0c924b1 6.11). | Add it |
| F22 | PARTLY | Strict `t_f<t_q` (L48) already excludes ties; L226 names the date audit and margin sensitivity. The internal plan fixes the rule (earliest instance, margins 0/1/7 d, bounds); the report does not. | Port the rule to Sec. 4 |
| F23 | CORRECT | RQ2 (L61) lists four components; the card asks for lag, lexical overlap and narrative drift. The internal plan has them as covariates. | Add as covariates |
| F24 | CORRECT | Rules: the declaration names tools and uses; criterion 2.8 wants named tasks and hours consistent with repository history. L261-263: "AI assistants", no tool names. The contribution table was absent on 4.11 (a4d4def) and added in 0c924b1. | Name tools and versions |
| F25 | CORRECT | The judge appears only at L234 in the report. The internal plan specifies a panel (gpt-oss-120b, Command A, Mistral Large 2411), validated on 400 PL AMC-16K pairs. | Specify or remove (meeting) |
| F26 | PARTLY | The logic is sound: a post whose only gold is later has no gold in P(q). The pool is not empty. The report already defines the answerable rate (L183), reports both conditions (L184) and gates on it in W1 (L217). | Report rate as first result |
| F27 | CORRECT | The card puts language bias out of scope. `vykopal2026investigating` is in the bib but never cited. | Cite and delimit |
| F28 | CORRECT | L65 "Hypotheses (pre-registered)"; there is no registry entry. Authorisation is asserted (L231) but not documented. | "prespecified"; list grants |
| F29 | CORRECT | The report does not state equal query sets. The internal plan scores every chain step "on one fixed query set". | State it |
| F30 | CORRECT | Assessment criteria PDF: 2.4 (3 pts) needs every point from the written reviews and the meeting-8 Q&A answered with a named place and a concrete fix; 2.5 (2 pts) extends the Phase 1 table with reviewer and PoC input. Rules section 6: quote each remark, then answer it. | Quote remarks in the rebuttal; add Q&A questions after 25.11 |
| Q1 | CORRECT | Same gap as F22. | Answer in rebuttal |
| Q2 | CORRECT | This is the planned core result; no number exists yet. | Answer after PoC |
| Score | CORRECT | 1.5+1.5+1+0.5+1 = 5.5. | none |
| Praise 1.4 | CORRECT | 19 cited entries, preprint-only: `wang2024multilingual` only. | none |

## Suggested literature

| Work | Metadata | Claimed use | Note |
|---|---|---|---|
| Vykopal 2026 | CORRECT: EACL 2026 long, pp. 5195-5221, DOI ok | CORRECT: language and retrieval bias on AMC-16K | [[Language and Retrieval Bias]] |
| Søgaard 2021 | CORRECT: EACL, pp. 1823-1832, DOI ok | CORRECT: random splits overestimate | [[We Need to Talk about Random Splits]] |
| Kazemi 2021 | CORRECT (full title "... to Scale Global Fact-Checking") pp. 4504-4517 | CORRECT | [[Claim Matching Beyond English]] |
| Alkhalifa 2023 | CORRECT: LNCS 14163, pp. 440-458 | CORRECT: Qwant snapshots June, July, Sept 2022 | [[LongEval 2023]] |
| Urbano 2019 | CORRECT: SIGIR, pp. 505-514 | INCORRECT: the paper recommends the t-test or permutation test, and discontinuing the bootstrap-shift test unless the sample is large. It sets no resample count. | missing; add |

## Errors the review missed

| ID | Evidence | Action |
|---|---|---|
| X1 | Pikuliak 0.83 (L81, L122) is labelled "full pool". Monolingual runs search only same-language fact-checks, and the score averages languages with more than 100 pairs (paper Sec. 4). | Relabel "same-language pool, all pairs" |
| X2 | Hardalov "333k" (L78); the paper has 332,660. | Rounding, keep |
| X3 | The Ramponi note `venue` repeats the wrong pages. | Fix with F17 |

## Checks against the course documents

| Item | Verdict | Evidence | Action |
|---|---|---|---|
| Exceptional-research point 0/1 | UNVERIFIABLE | The criteria PDF lists only bonus B.1 (notebooks, +5) and 5d.3 (discussion, +5); no research bonus | Ask the supervisor; ignore for planning |
| Phase 1 length | not raised | Rules: max 4 meaningful pages; announcement: up to 5 | Phase 2 has no stated limit |
| Rebuttal format | gap in our rebuttal | Rules section 6: "quote the remark, then answer it"; 2.4 scores restatements 0 | Quoted remarks added to `rebuttal.tex` |
| Q&A questions | open | 2.4 includes the questions our team receives in meeting 8 (25.11); none exist yet | Add them to the rebuttal after 25.11 |
| Contribution table | stricter than reviewed | 2.8: named tasks and hours consistent with repository history | Align with git history |
| Total points | inconsistent | Rules 100 core; criteria PDF 105 (tutorial exercises 25) | Ask the supervisor |
