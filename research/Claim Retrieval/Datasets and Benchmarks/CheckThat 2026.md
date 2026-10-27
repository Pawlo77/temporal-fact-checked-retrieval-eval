---
title: "CheckThat 2026"
aliases: ["The CLEF-2026 CheckThat! Lab: Advancing Multilingual Fact-Checking"]
authors: ["Julia Maria Struß", "Sebastian Schellhammer", "Stefan Dietze", "Venktesh V.", "Vinay Setty", "Tanmoy Chakraborty", "Preslav Nakov", "Avishek Anand", "Primakov Chungkham", "Salim Hafid", "Dhruv Sahnan", "Konstantin Todorov"]
year: 2026
venue: "Advances in Information Retrieval (ECIR 2026), Lecture Notes in Computer Science, Springer, pages 325-335"
arxiv: "2602.09516"
doi: "10.1007/978-3-032-21321-1_43"
url: "https://doi.org/10.1007/978-3-032-21321-1_43"
citekey: struss2026clef
verified: 2026-10-27
theme: "[[Datasets and Benchmarks]]"
tags: [type/paper, theme/datasets, topic/shared-task, topic/multilingual, topic/benchmark]
---
# CheckThat 2026

> [!info] TL;DR
> This ECIR lab announcement describes the three CLEF-2026 CheckThat! tasks: source retrieval for scientific web claims (English, German, French), verification of numerical and temporal claims by ranking LLM reasoning traces (English, Spanish, Arabic), and generation of full fact-checking articles with citations (English). It plans tasks and data, not results. PFCR appears in its pipeline figure but is not a 2026 task.

## Motivation

- Earlier editions covered check-worthiness, PFCR, evidence retrieval and verification; the last three added side tasks, and 2026 returns to the verification pipeline.
- Social media posts cite scientific studies informally ("Stanford study shows..."), so the source must be found before the claim can be checked.
- LLMs verify numerical claims worse than other claims, and numbers make false claims look credible.
- Writing the final fact-checking article is time-consuming and had never been a CheckThat! task.

## Method

We write a social media post as $q$; the lab's tasks are not PFCR, so our pool notation is used only for Task 1's candidate papers.

**Task 1, source retrieval.** Given $q$ with an implicit reference to a paper (no URL), retrieve that paper from a candidate pool. Metric: MRR@5.

Intuition: users rarely look past the first five results in known-item search.

**Task 2, numerical and temporal claims.** Given a claim, evidence and 20 reasoning traces from gpt-4o-mini with verdicts, rank the traces by how well they lead to the correct verdict and output a verdict. Metrics: Recall@5 and MRR@5 for traces, macro F1 for verdicts, final rank averaged over macro F1 and Recall@5. New test sets are released "to avoid leakage".

**Task 3, article generation.** Given a claim, its verdict and the evidence documents, write a fact-checking article with inline citations. Metrics: entailment against the expert article, citation correctness and citation completeness; Elo ratings from an LLM judge as a secondary score.

## Key numbers

- Task 1 data: 15,699 English post-paper pairs reused for training; about 1,500 newly annotated pairs per language for German and French.
- Task 2 data: 8,000 English, 2,808 Spanish and 3,260 Arabic claims; 20 reasoning traces per training claim.
- Task 3 data: about 26k training and 3.3k validation examples (WatClaimCheck); test 1.2k examples (987 ExClaim, 220 AmbiguousSnopes).

## Experiments

- **None:** the paper announces the lab before the evaluation; it reports no system results.

## Data

- Task 1: X posts paired with the scientific studies they mention, one shared collection of studies for all three languages.
- Task 2: claims from fact-checking websites with an evidence corpus from the web, reusing the CLEF-2025 numerical-claims data.
- Task 3: WatClaimCheck, ExClaim and the private AmbiguousSnopes set.

> [!failure] Limitations
> - A plan, not an overview: data sizes are targets and no results are given.
> - Task 2's "temporal claims" are claims containing time expressions; time-respecting retrieval is not part of any task.
> - Task 3 gives the gold evidence and verdict, so it skips retrieval and verification.

## Relation to our project

- No PFCR task in 2026, so there is no live shared task to overlap with; a temporal PFCR task stays open as a possible proposal ([[Research summary]]).
- Task 2 handles leakage by releasing new test sets, the shared-task version of our out-of-time concern, but it says nothing about evidence published after the claim ([[Enhanced topic research]]).
- The pipeline figure still places PFCR between check-worthiness and evidence retrieval, which supports framing our work as a pipeline step ([[Proposed Task]]).

## Future work

- **Partly done:** results of the 2026 tasks; the lab's [CLEF 2026 overview](https://doi.org/10.1007/978-3-032-39150-6_23) (Struß et al., 2026) was published but not read for this note.
- **Open:** broader low-resource language coverage, which the organisers plan (searched 2026-10).
- **Open:** a CheckThat! task on PFCR with time-restricted fact-check pools (searched 2026-10).
