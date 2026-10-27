---
title: "EDEN monitoring and troubleshooting"
type: handbook
domain: vault
parent: "[[compute]]"
related:
  - "[[EDEN Slurm basics and partitions]]"
  - "[[EDEN storage and quotas]]"
tags: [handbook, hpc]
created: 2026-10-27
updated: 2026-10-27
---
# EDEN monitoring and troubleshooting

## Monitoring

```bash
sfree                                   # free resources [V]
pestat                                  # per-node load [V]
sinfo                                   # partitions, node states [V]
squeue -u $USER                         # own jobs [V]
squeue -u $USER -o "%.10i %.12P %.20j %.8T %.10M %.10l %.6D %R"
scontrol show job <jobid>               # reason, node, limits [V]
scontrol show reservations              # maintenance windows [V]
sshare -l                               # fairshare [V]
sshare -laA <group>                     # group + members [V]
sacct -A <group> -S 2026-10-01 -o JobID,JobName,Partition,State,Elapsed,MaxRSS,AllocTRES%40
seff <jobid>                            # not installed on EDEN [V:run]; use `sacct -j <jobid> -o JobID,Elapsed,MaxRSS,AllocTRES%40` instead
sacct -j <jobid> --format=JobID,State,ExitCode,Elapsed,MaxRSS,ReqMem   # [V:slurm]
tail -f logs/<name>_<jobid>.log
scancel <jobid>; scancel -u $USER       # cancel one / all
```

- Web status: https://eden-status.mini.pw.edu.pl [V].
- Grafana dashboard `eden-overview`: https://edenstatus.mini.pw.edu.pl/d/7I8DDL3nz/eden-overview?orgId=1 (link from the maintainer, not crawled).
- GPU use during a run: `srun --jobid=<jobid> --overlap nvidia-smi` [V:slurm, U on cluster policy]; or log `nvidia-smi --query-gpu=utilization.gpu,memory.used --format=csv -l 30 &` inside the script.
- Group usage reports: `sreport cluster accountutilizationbyuser accounts=<group>` [V].

## Pending reasons

- `Priority`: others ahead; fairshare low [V].
- `Resources`: waiting for free GPUs or RAM [V:slurm].
- `ReqNodeNotAvail, Reserved for maintenance`: reservation; shorten `--time` [V].
- `AssocGrp*Limit` or `QOS*Limit`: group or user cap [V:slurm].
- `DependencyNeverSatisfied`: predecessor failed; `scancel` [V:slurm].
- Over-requesting (time, RAM, GPUs) delays start; request what `seff` shows plus 20 percent.

## Failure table

| Symptom | Cause | Fix |
|---|---|---|
| job rejected at submit, `AssocMaxSubmitJobLimit` | missing or wrong `-A` (default account `null` cannot submit) | add `-A <group>` [V:run] |
| job gone, no log | log dir absent | `mkdir -p logs` [V] |
| `TIMEOUT` | `--time` too short | measure on a slice, raise |
| `OUT_OF_MEMORY` / `Killed` | `--mem` too low | raise; check `MaxRSS` via `sacct` |
| `CUDA out of memory` | batch too large | halve batch, fp16, sort by length |
| `no CUDA device` | no `--gres=gpu` or login node | request GPU [V] |
| `CUDA_ERROR_UNSUPPORTED_PTX_VERSION` | arch/PTX mismatch | rebuild or use matching wheel [V] |
| HF download hangs | transient network or Hub outage (compute nodes have internet [V:run]) | retry; pre-download, `HF_HUB_OFFLINE=1` |
| `Disk quota exceeded` / write fails | full group space | free space, move data [V] |
| `srun --pty` ended | ssh drop | `tmux` [V] |
| import errors for compiled libs | venv built elsewhere | rebuild on cluster |
| job waits though cluster looks free | fairshare, reservation, limits | `scontrol show job` [V] |

## Common pitfalls

- Computing on the login node; use `srun`/`sbatch` [V].
- `rsync --exclude='.*'` removes `.venv` and `.env` ([[EDEN data sync workflows]]).
- Models downloaded to `~/.cache`; set `HF_HOME` ([[EDEN Python environments]]).
- Results left in `/scratch` or `/raid`; copy to group space [V].
- Default `--time` takes partition max and may not start before a reservation [V].
- Committing `<email>`, usernames or hostnames from scripts.
- Rules: group leader must file yearly report or group loses access [V].
