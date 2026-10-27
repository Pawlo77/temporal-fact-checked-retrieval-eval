---
title: "EDEN notifications and job control"
type: handbook
domain: vault
parent: "[[compute]]"
related:
  - "[[EDEN monitoring and troubleshooting]]"
  - "[[EDEN resource profiling]]"
  - "[[EDEN job templates]]"
  - "[[EDEN Slurm basics and partitions]]"
tags: [handbook, hpc]
created: 2026-10-27
updated: 2026-10-27
---
# EDEN notifications and job control

How to find out that a job started, finished or failed, and how to run long work so a failure costs little. Markers follow the legend in [[compute]]; mail delivery on EDEN is not verified yet.

## Slurm mail

```bash
#SBATCH --mail-type=BEGIN,END,FAIL,TIME_LIMIT_80   # [V:slurm]
#SBATCH --mail-user=<email>                         # [V] in the cheat sheet; relay delivery [U]
```

- `END` and `FAIL` are the useful pair; `TIME_LIMIT_80` warns at 80 percent of `--time` [V:slurm].
- For arrays add `ARRAY_TASKS` or mail arrives per task, which floods an inbox [V:slurm].
- Whether the cluster relays mail to outside addresses is [U]; test with a 1-minute job before relying on it.
- Spam filters may drop the first message: check the junk folder once.

## Alternatives without a mail relay

- Compute nodes reach the internet over HTTPS [V:run], so a job can notify a chat or push service with `curl` at its end; keep the webhook URL in a file outside the repository (mode 600), never in scripts or the vault.
- A dependent notification job: `sbatch --dependency=afterany:<id> notify.sh`, where `notify.sh` reads `sacct -j <id>` and posts the state; `afternotok` fires only on failure [V:slurm].
- A trap in the batch script reports the exit code even when Python crashes: `trap 'echo "exit $? at $(date)" >> logs/status_$SLURM_JOB_ID.txt' EXIT` [standard].

## Following jobs

```bash
squeue -u $USER -o "%.10i %.9P %.20j %.8T %.10M %.10l %R"   # [V:run]
sacct -u $USER -S today -o JobID,JobName,State,ExitCode,Elapsed,NodeList   # [V:run]
tail -F logs/<name>_<jobid>.log                                              # [standard]
watch -n 30 'squeue -u $USER'                                                # [standard]
scontrol show job <jobid> | grep -E 'JobState|Reason|RunTime|StartTime|NodeList'   # [V:slurm]
```

- Run the watching shell in `tmux` so a dropped connection does not end it [V].
- Arrays: `squeue -u $USER -r` lists each task; `sacct -j <arrayid> -o JobID,State` shows failed indices to rerun with `--array=<list>` [V:slurm].

## Surviving timeouts and failures

- `--signal=B:USR1@300` sends `USR1` to the batch shell 5 minutes before the limit, so the script can save a checkpoint and exit [V:slurm, U on EDEN].
- `--requeue` lets Slurm restart a job after a node failure; the script must resume from its checkpoint and be idempotent [V:slurm, U whether requeue is allowed on EDEN].
- Write results per cell, skip cells whose output exists, and keep the grid in an array so a failed cell reruns alone ([[EDEN job templates]]).
- Pin each cell's seed and config in its output directory so a rerun is comparable.
- `scancel <jobid>` ends a job; `scancel -u $USER --state=PENDING` clears only the queue [V:slurm].

## Good habits

- Set `--time` from measured runs ([[EDEN resource profiling]]); an overlong limit delays start and can block before a reservation [V].
- One job log per task: `--output=logs/%x_%A_%a.log` for arrays [V:slurm].
- Never leave an interactive `srun --pty` allocation idle: it holds its GPU [V].
- Check [[EDEN Slurm basics and partitions]] before submitting to see which node pool has room.
