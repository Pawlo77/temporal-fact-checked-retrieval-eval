---
title: "Course grading and report"
type: handbook
domain: vault
parent: "[[temporal-fact-checked-retrieval-eval]]"
tags: [handbook, course, grading, deadlines, report]
created: 2026-10-27
updated: 2026-11-11
related:
  - "[[Phase 1 feedback]]"
---
# Course grading and report

Sources: the course documents Course rules, Assessment criteria (read 2026-11-11 from the PDFs) and the Overleaf template. Raw files stay in the gitignored `_temp/` or on the authors' machines. "Nothing is graded that is not on the criteria list."

## Deadlines (2026/27)

| When | What |
|---|---|
| 28.10 | topic selection + one-page proposition form |
| 4.11 | Phase 1 proposal + SOTA (10 pts; rules: max 4 meaningful pages, announcement: up to 5) |
| 13.11 (Fri, meeting 6) | proposal feedback, mandatory; then a mandatory supervisor meeting |
| 18.11 | mid-term presentation video (10 min, SOTA + PoC) |
| 25.11 (meeting 8, 9:15-14:00) | mid-term Q&A, mandatory; every student prepares questions for other teams |
| 2.12 | Phase 2: report, source code (merge request), EDA, PoC, revised SOTA, rebuttals (20 pts) |
| 9.12, 16.12 | project feedback, mandatory |
| 13.01.2027 | Phase 3: final report + 10-min video (faces visible, posted to the LeOn channel); final Q&A, mandatory |
| 20.01, 27.01.2027 | feedback and rebuttals, course summary and grading |

## Grading

| Component | Points |
|---|---|
| 5a Q&A questions (individual; 1 unique, reasonable question = 1 pt, over meetings 8 and 13) | 10 |
| 5b team project: Phase 1 = 10, Phase 2 = 20, Phase 3 = 30 | 60 |
| 5c survey presentation (slides 4, quiz 2, demonstration notebook 4) | 10 |
| 5d exercises: mid-term tests (10), annotation exercise (10); discussion bonus +5 | 20 |
| Bonus: notebook exercises | +5 |

- Rules say 100 core; the criteria PDF says tutorial exercises 25 and core 105, so confirm the total. Grade scale by percentage of 100: below 51% = 2.0, 51-60 = 3.0, 61-70 = 3.5, 71-80 = 4.0, 81-90 = 4.5, 91-100 = 5.0.
- Passing needs at least 30 of 60 project points plus every acceptance condition below.
- Every criterion scores full, half or 0 (5a is per question).

## Conditions of acceptance (not scored; missing = report not graded, score 0 until added)

- Contribution table in every phase: one row per person, named tasks, hours, consistent with repository history.
- Declaration of LLM use in every phase: which tools, for what.
- Submission folder `surname_surname_surname_surname` (all members); the order set at Milestone 1 never changes. Non-compliance: -5 and not accepted.
- Wrong template: -5 once per phase and resubmit. Late: one 48-h delay per semester free; then -5 per started week of that phase.

## Phase 1 criteria (10)

- 1.1 State of the art (3): at least 15 works, each with what it does, on what data, with what result; a table of published numbers with dataset and split for every number.
- 1.2 Datasets and status (3): size, label definition, class balance, licence, how obtained; READY / TO COLLECT / RESTRICTED; for TO COLLECT: how many items, by when, annotated by whom.
- 1.3 Solution concept and plan (2): pipeline in one figure, metrics chosen before results, 2-3 concrete success deliverables, week-by-week plan with named owners.
- 1.4 Text quality and references (1): scientific language, no unexplained abbreviations, published versions cited, preprint-only under one third.
- 1.5 Data statement (1): source, licence, personal data, what you do about it; six lines suffice.

## Phase 2 criteria (20)

| # | Criterion | Pts | Full credit |
|---|---|---|---|
| 2.1 | Working PoC with first result | 4 | pipeline runs end to end on real data and produces a number; number without code or code without number is half |
| 2.2 | Exploratory data analysis | 3 | label and length distributions, duplicates, leakage check between splits, comparison with at least one other dataset (or a sentence why not) |
| 2.3 | Experiment plan and settings | 3 | baselines from at least two method classes (classical, fine-tuned encoder, prompted LLM), hyperparameters, splits, what is measured |
| 2.4 | Rebuttal to reviews and Q&A | 3 | every point answered (fixed, rejected or deferred) from the written reviews and from the meeting-8 Q&A questions; each answer names a place in the report, is checkable, and states the concrete fix; a list of remarks or answers that restate the remark is 0 |
| 2.5 | Revised state of the art | 2 | Phase 1 table extended with reviewer input and PoC-stage findings |
| 2.6 | Repository and README | 2 | a stranger reproduces one result from the README alone |
| 2.7 | Runtime and memory | 1 | training and inference time, hardware, memory, measured |
| 2.8 | Contribution table | 1 | named tasks and hours consistent with repository history |
| 2.9 | Text quality and references | 1 | as 1.4 |

## Phase 3 criteria (30)

3.1 results with analysis (4); 3.2 measurement procedures, ties and failures (3); 3.3 reproducibility: seeds, versions, configs, commands, data version (3); 3.4 rebuttal to all reviews and Q&A including meeting 13 (3); 3.5 final presentation (3); 3.6 uncertainty: at least 3 runs with spread, or a stated reason (2); 3.7 error analysis: at least 20 misclassified examples in named types with counts (2); 3.8 final pipeline and deviations (2); 3.9 revised literature review (1); 3.10 limitations with consequences (1); 3.11 data statement (1); 3.12 metric choice for the label distribution (1); 3.13 references (1); 3.14 language (1); 3.15 self-contained captions (1); 3.16 code quality and README (1).

## What every report contains (Rules section 6)

- Background, problem statement, contributions; related work and dataset descriptions with comparison tables; approach and results with the split of every number; conclusions and future work.
- Rebuttal to every reviewer remark: quote the remark, then answer it.
- Contribution table, data statement, LLM-use declaration, limitations with consequences, uncertainty, error analysis (the last three from Phase 3 criteria).
- Code: merge request to `github.com/grant-TraDA/NLP-2026W` (GPL v3; link confirmed on Teams before Phase 2), processed datasets, README that runs one experiment, trained models, scripts, tests, hyperparameters, seeds, library versions, exact commands.
- Reports: PDF plus the LaTeX project. Non-public data stays in the repository the teaching team names.
- Self-check before submitting: contribution table; LLM declaration; README; measured runtime and memory; split for every number; preprints checked for published versions; data statement; rebuttal at named places; correct template; on time; folder name.

## Required template

ACL 2015 style (Overleaf read link `overleaf.com/read/cfpttcdpsqzg`), not the Interspeech scaffold. Files in `report/checkpoint_1/` (first submission) and `report/checkpoint_2/` (revision):

- `project-proposal.tex` — Phase 1; `project-final-report-structure.tex` — Phase 3 (about 9 pages, max 12); `reproducibility-checklist.tex` — appendix, graded in Phase 3.
- `acl2015.sty`, `acl.bst`, `template-editorial-tips.tex`; references in `mybib.bib`.

## Citation rules

- Cite the published version of every work that has one; preprint-only citations under one third of the bibliography.
- Preferred venues for papers and surveys: ACL, EMNLP, NAACL, ACM Computing Surveys.

## Reading list

`_temp/Reading list.pdf` is the course reading list (WUT textbook sections, core classics, recent spotlights per lecture); its recent-spotlight papers are seeds for the SOTA table.
