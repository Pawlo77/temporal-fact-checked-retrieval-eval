---
title: "Phase 1 feedback response plan"
type: plan
domain: vault
parent: "[[temporal-fact-checked-retrieval-eval]]"
status: draft
created: 2026-11-11
updated: 2026-11-11
tags: [plan, feedback, report, phase2]
related:
  - "[[Phase 1 feedback]]"
  - "[[Review verification]]"
  - "[[2026-10-27-temporal-retrieval-eval|Project plan]]"
  - "[[Course grading and report]]"
---
# Phase 1 Feedback Response Plan

**Status:** draft

**Goal:** Answer every point of [[Phase 1 feedback]] (F1-F30, Q1-Q2) with a verified fix in `report/checkpoint_2/`, a rebuttal (criterion 2.4) and an extended SOTA table (2.5), submitted with Phase 2 on 2.12. The mandatory fixes F24 and F25 come first.

**Architecture:** [[Review verification]] gives a verdict and evidence per item. Research re-checks the notes behind Table 1. Data work fills Table 2 only from published counts or script output. Report fixes are mapped to F-ids. The rebuttal cites each fix by section and quotes source evidence where the review is wrong. Most fixes port text that already exists in the [[2026-10-27-temporal-retrieval-eval|Project plan]] (timestamps, judge protocol, codebook, fixed query set).

**Tech Stack:** Obsidian notes (skills `paper-notes`, `literature-search`); Python 3.12 with uv on EDEN for counts, logged to MLflow; LaTeX ACL 2015 (skill `latex-papers`); `make check`, `make vault-check`.

Owners: PP = Paweł Pozorski, MJ = Mateusz Jarosz, PF = Paweł Florek, JC = Jan Cwalina.

---
### Task 1: Research re-check and novelty search (11-17 Nov)

**Files:**
- Modify: notes behind Table 1 in `research/` (venue, numbers, split or pool); [[Literature corrections]]
- Create: `research/Evaluation Methodology/<Urbano note>.md`, `research/protocols/causal-index-pfcr.yaml`

- [ ] **Step 1:** Re-read each Table 1 number in its source and record split, pool and scale in the note. MJ: CheckThat 2021/22, CrowdChecked, SemEval, TIFIN, Ramponi (which pool gives 0.8042), AMC-16K. PP: MultiClaim (X1: same-language pool, all pairs), That is a Known Lie, Role of Context. PF: AVeriTeC (dev, F2), TREC 2011 (49 topics), StreamingQA, Missing Counter-Evidence, Chronological Splits.
- [x] **Step 2:** Fix the Ramponi note pages to 29045-29064 (F17, X3); note the published BGE-M3 title (F18). Owner MJ.
- [ ] **Step 3:** Independent review: each owner cross-checks another owner's notes (PP→PF→MJ→JC→PP) and logs disagreements in [[Literature corrections]].
- [ ] **Step 4:** Add an Urbano et al. 2019 note via skill `paper-notes`. It recommends the t-test or permutation test, and the bootstrap only for large samples, so it does not justify the bootstrap. Re-check the existing notes for Vykopal 2026, Søgaard 2021, Kazemi 2021 and LongEval 2023 against [[Review verification]]. Owner JC.
- [x] **Step 5:** (done 2026-11-11: 1,738 retrieved, 240 kept, 6 adjacent works, none PFCR with a per-query pre-post index; no full-text notes) Write the novelty-claim protocol per skill `literature-search` (OpenAlex, arXiv, forward citations of MultiClaim, SemEval-2025 T7, Shaar 2022 and TREC 2011; since 2019; queries on date-restricted, causal, temporal index for claim retrieval). Run the harvest, screen it, and fill `outcome` with counts and the date (F5). Owner PP.

### Task 2: Table 2 numbers (11-24 Nov)

**Files:**
- Create: the count script in `src/temporal_fact_checked_retrieval_eval/dataset/` with tests, or extend the protocol module from the Project plan W1
- Modify: `configs/experiment.yaml` (dataset paths only)

Known without data (cite the source; Polish/English splits in [[Language scope]]):

| Quantity | Value | Source |
|---|---|---|
| MultiClaim v1 PL / EN posts, FC | 453 / 6,912; 7,307 / 85,814 | Pikuliak 2023 Table 5 |
| v1 dated posts | 26,337 of 28,092 | Pikuliak 2023 |
| v2 subset PL / EN mono pairs | 1,309; 19,341 | Ramponi 2025 Table 4 (curated subset, not v2 itself) |
| ST7 test PL / EN posts, pairs, pool | 500/564/8,796; 500/740/145,287 | Peng 2025 Table 2 (English pairs corrected from 574 to 740 after counting `pairs_test_monolingual.csv`) |
| AMC-16K relevant share | 16% overall, PL mono 20.25%, 400 PL mono pairs | Vykopal 2025 |

Must be computed from data (never estimated in the report):

- [x] **Step 1:** (done 2026-11-11 with `scripts/corpus_stats.py` from PR 18; v1 has no post language, so v1 PL/EN stay on paper counts) For each of v1, v2 and ST7 (all, PL, EN): posts, pairs, FC, dated posts and dated FC; gold pairs per post (mean, median); gold FC per post; share of FC with at least one linked post (F6, F7). Owner PP.
- [x] **Step 2:** (done: v1 85%, v2 93%, v2 PL 89% post-first; Polish answerable posts 152, 14 and 9 at margins 0, 1, 7 days) Share of pairs with the post before the FC (H1), and the answerable rate per language at margins 0, 1 and 7 days, which gives the Polish answerable count (F7, F26). Owner PP, review PF.
- [x] **Step 3:** (same-day pairs and multi-instance counts measured; exact-second ties not counted separately) Tied-timestamp count and multi-instance share (F22, Q1). Owner PF.
- [ ] **Step 4:** Send the AMC-16K request to KInIT and log the date. PP drafts; the team sends from a university address (F9).
- [ ] **Step 5:** Copy the Zenodo access conditions verbatim for v1, v2 and ST7. Ask the authors in writing whether id lists may be redistributed (F10, F28). Owner PP.

### Task 3: Report fixes into `report/checkpoint_2/` (18-28 Nov)

**Files:**
- Modify: `report/checkpoint_2/report.tex`, `report/checkpoint_2/mybib.bib`

| Section | F-ids | Fix | Owner |
|---|---|---|---|
| Front | F21 | Add the template credit line (from `project-proposal.tex` L45); fix the folder-name TODO | JC |
| 1 Goal | F11, F15, F28 | Primary claim: S@10, unconditional, strict causal vs random, PL-EN DiD, with answerable-only secondary. Drop RQ4 to future work unless an owner and metric are agreed. Rename "pre-registered" to "prespecified (frozen in git before results)" | PF |
| 2 SOTA | F1-F5, F16, F19, F27, X1 | Per-row split or condition; AVeriTeC dev; one 0-1 scale; Aschern footnote; search protocol sentence; expand abbreviations; `\newcite`; cite Vykopal 2026 to delimit scope | MJ |
| Bib | F17, F18 | Ramponi pages; published M3-Embedding title | MJ |
| 3 Data | F6-F10 | Task 2 numbers; TO COLLECT rows for split id lists and 50 failure codes (codebook, 2 annotators, kappa, W3, PF/JC); AMC-16K request date; licence terms | PP |
| 4 Plan | F12-F14, F22, F23, F26, F29 | Weekly plan, one owner per task; one 4th encoder in W2 (decide at the meeting, default LaBSE for PL→EN); Figure 1 with P(q) and bootstrap; timestamp rule (earliest instance, margins, bounds); lag, overlap and drift as covariates; answerable rate as first result; all protocols on one query set | PF (figure), PP (protocol) |
| 5 Data stmt | F20, F25, F28 | No per-outlet or per-author ranking. Judge: specify (panel, released prompt, Yes/No labels, validation on AMC-16K PL+EN mono pairs, Cohen's kappa, accept at kappa ≥ 0.6) or remove if AMC-16K is not received by 25 Nov. List the access grants | JC |
| 7 LLM use | F24 | Name each tool and model version, and what it did; give concrete per-member tasks in the contribution table | JC |

- [ ] **Step 1:** Apply the fixes; every number traces to a note or to Task 2 output.
- [ ] **Step 2:** Build the PDF and check the ACL 2015 template and page limit.

### Task 4: Rebuttal and extended SOTA table (25 Nov-1 Dec)

**Files:**
- Modify: `report/checkpoint_2/report.tex` (rebuttal section or appendix, Table 1)

- [ ] **Step 1:** Rebuttal table: F-id | quoted remark | response | where fixed (section, table, line); rules section 6 require the quote and criterion 2.4 scores restated remarks 0. Owner JC, review PP.
- [ ] **Step 1b:** After the 25.11 Q&A, add every question our team received to the same table (2.4). Owner JC.
- [ ] **Step 2:** Polite corrections with evidence from [[Review verification]]: F14 (size-matched already in Figure 1), F21 (line was never present, now added), F9 (the card's October request was MultiClaim, granted), F19 (`\newcite` in this template), F26 (gate already planned), Urbano (supports t-test or permutation; we keep the cluster bootstrap for clustered queries and add a paired permutation check).
- [ ] **Step 3:** Answer Q1 with the timestamp rule and Task 2 counts. Answer Q2 with the PoC number (random vs strict causal vs size-matched on one query set) or state when it comes.
- [x] **Step 4:** (four cited works added to Table 1; Urbano not cited; PoC-stage findings still to add) Extended SOTA table (2.5): the current 15 works plus the five suggested ones (number, dataset, split each; Urbano and Søgaard as method rows with no score). Owner MJ.

### Task 5: Supervisor meeting (by 13 Nov)

- [ ] **Step 1:** Propose slots: Fri 13 Nov (meeting 6 is the mandatory proposal-feedback meeting; the supervisor offers a 7-hour shift), or Wed 18 Nov course hours. PP drafts and the team sends.
- [ ] **Step 2:** Agenda: 4th encoder; primary metric; judge kept or removed (F25); RQ4 kept or dropped; AMC-16K status; id-list release; contribution-table format; the five review points we contest. Owner PP; JC takes minutes into this note.

### Task 7: Phase 2 scope beyond the feedback (criteria 2.1-2.3, 2.6-2.8)

Taken from the Assessment criteria PDF; none of it is in the feedback, all of it is graded on 2.12.

- [ ] **Step 1:** PoC (2.1, 4 pts): pipeline end to end on real data with one number (random vs strict causal vs size-matched, one query set). Owner MJ.
- [ ] **Step 2:** EDA (2.2, 3 pts): label and length distributions, duplicates, leakage check between splits, comparison with one more dataset or a sentence why not. Reuse Task 2 counts. Owner PP.
- [ ] **Step 3:** Experiment plan (2.3, 3 pts): baselines from at least two method classes (BM25 classical; e5 or mmlw fine-tuned encoder; reranker or prompted LLM), hyperparameters, splits, measures. Owner PF.
- [ ] **Step 4:** README and merge request to `github.com/grant-TraDA/NLP-2026W` that a stranger can run for one result (2.6); measured runtime, hardware and memory (2.7). Owners PF, MJ.
- [ ] **Step 5:** Contribution table with named tasks and hours consistent with git history (2.8); revised SOTA table (2.5, Task 4). Owner JC.
- [ ] **Step 6:** Mid-term video (18.11) and meeting-8 Q&A (25.11); each member prepares questions for other teams (5a). All.

### Task 6: Deadline 2.12

| Week | Deliverable | Owner |
|---|---|---|
| 11-17 Nov | Task 1, Task 2 steps 4-5, meeting | PP, MJ, PF, JC |
| 18 Nov | Mid-term video (SOTA + PoC) | PF |
| 18-24 Nov | Task 2 steps 1-3, Task 3 draft | PP, PF |
| 25 Nov-1 Dec | Task 3 final, Task 4, PoC number | MJ, JC |
| 2 Dec | Submit Phase 2 via skill `ship` | PP |

- [ ] **Step 1:** `make check` green, PDF rebuilt, rebuttal covers F1-F30 and Q1-Q2.
