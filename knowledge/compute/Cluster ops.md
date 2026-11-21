---
title: "Cluster ops"
type: map
domain: vault
parent: "[[temporal-fact-checked-retrieval-eval]]"
tags: [map, hpc]
created: 2026-11-21
updated: 2026-11-21
---
# Cluster ops

Rules, tooling and notes for the Slurm clusters this project uses live in the repository `Pawlo77/cluster-ops` (private; cloned to `~/cluster-ops` on a cluster), not in this vault, so one fix reaches every project.

- EDEN (WUT MiNI): `clusters/eden/` holds the rules (`~/AGENTS.md` on the cluster), the home folder layout and the hardware, partition and quota notes.
- Any Slurm cluster: `docs/slurm/measure.md` (size requests from measurements) and `docs/slurm/contract.md` (what a project provides for the `swatch` dashboard).

Keep only project-specific steps here: the account, the job scripts and the per-model resource profiles.
