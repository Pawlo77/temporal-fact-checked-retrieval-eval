---
title: "temporal-fact-checked-retrieval-eval"
type: map
domain: index
tags: [moc, temporal-fact-checked-retrieval-eval]
created: 2026-01-01
updated: 2026-10-27
---
# temporal-fact-checked-retrieval-eval

Causal (time-respecting) evaluation of previously fact-checked claim retrieval on MultiClaim, with a Polish focus and an English control. The repository is also an Obsidian vault.

Start here: [[Proposed Task]]. Dashboard: [[Dashboard]]. Open items: [[Fixed issues]]. Literature: [[Research]].

> [!note] State of the code
> Planning phase: the package holds the experiment scaffold only, no retrieval code or results yet. The project plan is [[Proposed Task]]; the assigned brief is [[Original Task]].

## Components

| Note | Role |
|---|---|
| [[Proposed Task]] | Enhanced project: protocol, systems, gap decomposition, deliverables |
| [[Original Task]] | The assigned brief |
| [[Research]] | Verified paper notes by area: claim retrieval, temporal evaluation, methodology, models |
| [[compute]] | EDEN cluster: access, storage, Slurm, GPU jobs, environments, project compute plan |

## Flow

1. Request MultiClaim access and build the dated corpus ([[Proposed Task]]).
2. Build the splits: random, strict causal, size-matched random, cluster-expanded causal.
3. Run BM25, dense, cross-lingual and reranking systems under each protocol ([[compute plan]]).
4. Report Success@10 and MRR with paired bootstrap, then decompose the gap and code 50 failing queries ([[Language scope analysis]]).

## Invariants

- No MultiClaim text enters git or any release; only id lists and code ([[Original Task]]).
- Errors are reported in aggregate; no ranked list of outlets or authors.
- A query counts as answerable only when a gold fact-check predates the post.
- `make check` is the exit criterion: tests, all hooks and the vault check.

## Concepts

## Decisions

## Research

Literature on one question: how much retrieval performance survives a time-respecting index. Index and corrections: [[Research]], [[Research summary]], [[Literature corrections log]].

## Handbook

[[Original Task]] · [[Proposed Task]] · [[Enhanced topic research]] · [[Research summary]] · [[Language scope analysis]] · [[Literature corrections log]] · [[compute]]

## Generated

[[Modules]] · [[Public API]]
