---
title: Research
tags: [type/hub]
created: 2026-01-01
parent: "[[temporal-fact-checked-retrieval-eval]]"
---
# Research

Literature on one question: **how much of the reported performance of previously fact-checked claim retrieval (PFCR) survives when a system may search only fact-checks published before the post, and is the penalty larger for Polish than for English?**

A naive "index only earlier fact-checks" filter mixes four effects: the gold fact-check not existing yet, a smaller pool, training-time leakage and missing labels for earlier fact-checks of the same claim. The project separates them with a causal index, answerability-aware metrics and a gap decomposition; see [[Proposed Task]]. State of the literature and verified novelty: [[Research summary]].

## Areas

Each area is a folder with a note of its own name that lists its themes and papers.

| Area | Scope | Notes |
|------|-------|-------|
| [[Claim Retrieval]] | PFCR datasets, shared tasks, methods and systems, language and retrieval bias | 16 |
| [[Temporal Evaluation]] | Chronological splits, query-time retrieval, leakage in claim verification, LLM temporal leakage | 12 |
| [[Evaluation Methodology]] | How data is split and what random and standard splits hide | 3 |
| [[Retrieval Models]] | Embedding models, retrievers and rerankers used as systems | 8 |

Search protocols and outcomes: `protocols/`. Writing standard: `research/AGENTS.md`.
