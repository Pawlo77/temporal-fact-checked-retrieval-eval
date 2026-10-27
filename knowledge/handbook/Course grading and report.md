---
title: "Course grading and report"
type: handbook
domain: vault
parent: "[[temporal-fact-checked-retrieval-eval]]"
tags: [handbook, course, grading, deadlines, report]
created: 2026-10-27
updated: 2026-10-27
---
# Course grading and report

Distilled from the course documents in `_temp/` (Assessment criteria, Course rules, Project topics, Reading list, Overleaf template). The raw PDFs and the template zip stay in `_temp/`, not in the vault.

## Deadlines (2026/27)

| When | What |
|---|---|
| 28.10 | topic selection + proposition form |
| 4.11 | Phase 1 proposal + SOTA analysis (10 pts) |
| 18.11 | mid-term presentation video, SOTA + PoC |
| 2.12 | Phase 2 EDA + PoC + report + merge request (20 pts) |
| 13.01.2027 | Phase 3 final report + presentation video (30 pts) |
| 27.01.2027 | summary and grading |

## Grading (100 core + 5 bonus)

- 5a Q&A questions (individual): 10 pts.
- 5b team project: 60 pts — Phase 1 = 10, Phase 2 = 20, Phase 3 = 30.
- 5c survey presentation: 10 pts.
- 5d exercises (mid-term tests + annotation): 20 pts.
- Pass needs at least 50% of project points (30 of 60) plus the acceptance conditions below.

## Phase 1 criteria (4.11)

- 1.1 State of the art: at least 15 works, each with what it does, on what data, with what result; a table where every published number names the dataset and split (3 pts).
- 1.2 Datasets and status: size, label definition, class balance, licence, how obtained, labelled READY / TO COLLECT / RESTRICTED (3 pts).
- 1.3 Solution concept and plan: pipeline in one figure, metrics chosen before results, 2-3 concrete deliverables, week-by-week plan with named owners (2 pts).
- 1.4 text quality and references (1 pt).
- 1.5 data statement (1 pt).

## Phase 2 (2.12) and Phase 3 (13.01) criteria that shape the plan

- 2.1 working PoC with a first number (4 pts); 2.2 EDA (3); 2.6 README a stranger reproduces one result (2); 2.8 contribution table (required to pass).
- 3.6 uncertainty: main comparison from at least 3 runs with spread, or a stated reason why not (2); 3.7 error analysis, at least 20 misclassified examples grouped into named types (2).

## Required template

ACL 2015 style, not the Interspeech scaffold in `report/`. The course template is `_temp/Overleaf LaTeX template.zip`:

- `project-proposal.tex` — Phase 1, max 4 meaningful pages.
- `project-final-report-structure.tex` — Phase 3, about 9 pages, max 12.
- `reproducibility-checklist.tex` — appendix, graded in Phase 3.
- `acl2015.sty`, `acl.bst` — style and bibliography files.

Swap `report/` to this template when the first report is written.

## Mandatory in every phase (conditions of acceptance, not scored)

- Contribution table: each member, what they did, workload in hours.
- Declaration of LLM use: which tools, for what.
- Data statement: source, licence, personal data, what we do about it (six lines).
- Folder named `surname_surname_surname_surname`, order fixed from Milestone 1; a mismatch costs 5 pts.
- Wrong template costs 5 pts and forces resubmission; late submission costs 5 pts per started week after the one free 48h delay.

## Citation rules

- Cite the published version of every work that has one; preprint-only citations under one third of the bibliography.
- Preferred venues: ACL, EMNLP, NAACL, ACM Computing Surveys.

## Reading list

`_temp/Reading list.pdf` is the course reading list (WUT textbook sections + core classics + recent spotlights per lecture); its recent-spotlight papers are seeds for the SOTA table.
