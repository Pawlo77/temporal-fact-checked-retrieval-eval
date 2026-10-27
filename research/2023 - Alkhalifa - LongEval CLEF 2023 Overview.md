# 2023 - Alkhalifa - LongEval CLEF 2023 Overview

## Citation

- Authors (as far as read; the list was truncated in every source I saw): R. Alkhalifa, I. Bilal, H. Borkakoty, J. Camacho-Collados, R. Deveaud, A. El-Ebshihy, L. Espinosa-Anke, G. Gonzalez-Saez, P. Galuščáková, L. Goeuriot, E. Kochkina, M. Liakata, D. Loureiro, H. T. Madabushi, P. Mulhem, F. Piroi, M. Popel, C. Servan, and further authors not read. Check the full list on the LNCS page before citing.
- Title: Overview of the CLEF-2023 LongEval Lab on Longitudinal Evaluation of Model Performance (LNCS, CLEF 2023 proceedings, pages 440-458, DOI 10.1007/978-3-031-42448-9_28); Extended Overview in CEUR-WS Vol-3497, paper 184
- Venue: CLEF 2023, Thessaloniki, 18-21 September 2023
- Year: 2023
- URLs: lab site https://clef-longeval-2023.github.io/ ; LNCS https://link.springer.com/chapter/10.1007/978-3-031-42448-9_28 ; extended overview https://ceur-ws.org/Vol-3497/paper-184.pdf ; collection paper (Galuščáková et al., SIGIR 2023) https://dl.acm.org/doi/10.1145/3539618.3591921
- Verified on: 2026-10-27 (lab site and CEUR extended overview read)

## What it does

- First CLEF lab on temporal persistence of IR systems and text classifiers; motivation: performance drops as test data moves away from training time.
- Task 1 (retrieval): Qwant French web search data, queries, documents and click-model relevance; within-time (WT, June 2022), short-term (ST) and long-term (LT) test collections; measures NDCG per collection and relative drop vs WT.
- Task 2 (classification): binary sentiment, train 2016, test 2018 (short) and 2021 (long); metric includes Relative Performance Drop.
- Adds manual relevance judgments for 150 sampled queries via pooling.

## Key numbers

- 37 teams registered for Task 1, 25 for Task 2; 14 and 4 teams participated.
- Training data: 672 train queries, 9,656 assessments, 1,570,734 web pages, 98 held-out queries.
- Pool of 73 systems on WT and ST, 63 on LT.
- Task 1 result: the most robust systems were not the top systems; some runs (e.g. NEON_3b) increased NDCG at ST and LT; the top ST systems were stable or decreasing. A participant paper (Keller et al., CEUR Vol-3497 paper 196) reports average retrieval performance improving slightly over time.

## Relation to our project

- Precedent for longitudinal IR evaluation with explicit within-time vs later test collections and relative-drop metrics; usable for our rolling-origin protocol and for a possible CLEF task proposal.
- Its observation that robustness rankings differ from effectiveness rankings supports reporting both the causal score and the random-vs-causal delta per system.
- Does NOT cover: causal restriction of the document pool relative to each query's timestamp (LongEval snapshots the collection at each time step, it does not forbid future documents per query), answerability, fact-checking.

## Verification

- CORRECTED. Note line "IR temporal persistence: LongEval at CLEF 2023 onward (performance drop as test data moves away from training time)" states the lab's motivation as if it were the finding. For the 2023 retrieval task, the overview shows no uniform drop; several systems were stable or improved on ST/LT. Correct statement: "LongEval (CLEF 2023 onward) evaluates IR temporal persistence on successive Qwant snapshots; in 2023 the retrieval drop was system-dependent and not uniform." Reference list should cite the overview paper, not only the lab website.
