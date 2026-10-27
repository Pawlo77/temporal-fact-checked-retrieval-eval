---
title: "EDEN overview"
type: handbook
domain: vault
parent: "[[temporal-fact-checked-retrieval-eval]]"
tags: [handbook, hpc]
created: 2026-10-27
updated: 2026-10-27
---
# EDEN overview

## Cluster

- EDEN: HPC cluster of the Faculty of Mathematics and Information Science (MiNI), Warsaw University of Technology [V].
- Docs: https://hpc.mini.pw.edu.pl; wiki: https://hpc.mini.pw.edu.pl/dokuwiki/doku.php; live status: https://eden-status.mini.pw.edu.pl [V].
- Scheduler: Slurm; reserved resources are exclusive, availability is not guaranteed [V].
- OS: Ubuntu or DGX OS on all nodes [V].
- Placeholders used in every note: `<user>`, `<group>`, `<email>`, `<mini-ssh-gateway>`, `<eden-login-node>`; real values stay out of the vault.

## Notes

- [[EDEN access and networking]]: accounts, groups, ssh hops, tmux, Jupyter tunnel.
- [[EDEN hardware]]: nodes, GPUs, interconnect, storage hardware.
- [[EDEN storage and quotas]]: home, group, `/scratch`, `/raid`, retention.
- [[EDEN Slurm basics and partitions]]: commands, flags, time format, fairshare.
- [[EDEN GPU jobs]]: gres syntax, node choice, VRAM, CUDA errors.
- [[EDEN Python environments]]: uv or venv, torch wheels, HF cache, offline mode.
- [[EDEN data sync workflows]]: rsync hops, excludes, corpus placement.
- [[EDEN job templates]]: CPU, GPU, array, dependency chain, interactive, Jupyter.
- [[EDEN monitoring and troubleshooting]]: queue, efficiency, pending reasons, pitfalls.
- [[EDEN project compute plan]]: sizing for indexing, encoding, reranking, bootstrap; job grid.

## Legend

- **[V]**: verified on the EDEN docs (crawl of 2026-10-27, English and Polish wiki pages, rules, description, news).
- **[V:slurm]**: verified on SchedMD Slurm documentation (https://slurm.schedmd.com); generic Slurm, not confirmed on EDEN.
- **[U]**: unverified: cheat sheet, standard Slurm default, or estimate; test on the cluster.

## Verification status (crawl 2026-10-27)

- Crawled: home news, `description`, `rules`, wiki pages `en:first_steps:tutorial`, `pl:first_steps:storage`, `pl:first_steps:slurm_overview`, `pl:first_steps:access`, `pl:topics:cluster_description`, `pl:topics:grupy_badawcze`, `pl:info:access_host`, `pl:info:jupyter`, `pl:faq:cuda:cuda`, `pl:faq:slurm_queue`, `pl:llm:description`.
- Empty ("This topic does not exist yet") in the English namespace: `en:first_steps:storage`, `en:first_steps:slurm_overview`, `en:faq:slurm_queue`, `en:info:jupyter`, `en:topics:cluster_description`; the Polish pages carry the content.
- Web search found no third-party EDEN guides; only generic Slurm docs.
- Still unverified: GPU partition names and per-partition time limits, typed gres names (`gpu:a100:1`), numeric quotas, CPU/RAM defaults per partition, `module` availability, `uv` installed, compute-node internet, backup of home, max array size, max jobs per user, exact two-hop ssh flow, `lfs quota` working.
- Resolve by running on the login node: `sinfo -o "%P %l %D %G %c %m"`, `scontrol show partition`, `scontrol show config | grep -i -E 'MaxArray|MaxJob'`, `module avail`, `which uv`, `sshare -l`.
- Docs inconsistency: description page says 1.6 PiB DDN SS9012; grant text says 1.5 PiB, 44 or 48 GPUs; use the per-node table in [[EDEN hardware]].

## Cheat-sheet quick path

```bash
ssh -J <user>@<mini-ssh-gateway> <user>@<eden-login-node>     # [V] one-hop form
mkdir -p logs
sinfo; sfree                                                   # partitions, free resources
srun -p student -A <group> --cpus-per-task=1 --mem=4G --time=00:30:00 --pty bash   # [V]
sbatch job.sh; squeue -u $USER; scancel <jobid>
```
