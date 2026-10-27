---
title: "compute"
type: handbook
domain: vault
parent: "[[temporal-fact-checked-retrieval-eval]]"
tags: [handbook, hpc]
created: 2026-10-27
updated: 2026-10-27
---
# compute

## Cluster

- EDEN: HPC cluster of the Faculty of Mathematics and Information Science (MiNI), Warsaw University of Technology [V].
- Docs: https://hpc.mini.pw.edu.pl; wiki: https://hpc.mini.pw.edu.pl/dokuwiki/doku.php [V].
- Scheduler: Slurm; reserved resources are exclusive, availability is not guaranteed [V].
- OS: Ubuntu or DGX OS on all nodes [V].
- Placeholders used in every note: `<user>`, `<group>`, `<email>`, `<mini-ssh-gateway>`, `<eden-login-node>`; real values stay out of the vault.

## Live status

- Status page: https://eden-status.mini.pw.edu.pl [V].
- Grafana dashboard `eden-overview` (node load, GPU use, queue over time): https://edenstatus.mini.pw.edu.pl/d/7I8DDL3nz/eden-overview?orgId=1 (link from the maintainer; opens in a browser, not read by a script).
- From the shell: `sfree`, `squeue`, `sinfo`; how to read demand and choose a partition is in [[EDEN Slurm basics and partitions]] under "Choosing where to run".

## Notes

- [[EDEN access and networking]]: accounts, groups, ssh hops, tmux, Jupyter tunnel.
- [[EDEN hardware]]: nodes, GPUs, interconnect, storage hardware.
- [[EDEN storage and quotas]]: home, group, `/scratch`, `/raid`, retention.
- [[EDEN Slurm basics and partitions]]: commands, flags, time format, fairshare.
- [[EDEN GPU jobs]]: gres syntax, node choice, VRAM, CUDA errors.
- [[EDEN Python environments]]: uv or venv, torch wheels, HF cache, offline mode.
- [[EDEN data sync workflows]]: rsync hops, excludes, data upload.
- [[EDEN job templates]]: CPU, GPU, array, dependency chain, interactive, Jupyter.
- [[EDEN monitoring and troubleshooting]]: queue, efficiency, pending reasons, pitfalls.
- [[EDEN resource profiling]]: real vs allocated usage, speed tracking and bottleneck diagnosis.

## Legend

- **[V]**: verified on the EDEN docs (crawl of 2026-10-27, English and Polish wiki pages, rules, description, news).
- **[V:slurm]**: verified on SchedMD Slurm documentation (https://slurm.schedmd.com); generic Slurm, not confirmed on EDEN.
- **[V:run]**: verified by read-only commands and one 4-minute GPU test job on the cluster on 2026-10-27 (login node and a compute node).
- **[U]**: unverified: cheat sheet, standard Slurm default, or estimate; test on the cluster.

## Cheat-sheet quick path

```bash
ssh -J <user>@<mini-ssh-gateway> <user>@<eden-login-node>     # [V] one-hop form
mkdir -p logs
sinfo; sfree                                                   # partitions, free resources
srun -p student -A <group> --cpus-per-task=1 --mem=4G --time=00:30:00 --pty bash   # [V]
sbatch job.sh; squeue -u $USER; scancel <jobid>
```
