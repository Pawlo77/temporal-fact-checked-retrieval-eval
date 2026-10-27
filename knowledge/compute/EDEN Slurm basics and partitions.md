---
title: "EDEN Slurm basics and partitions"
type: handbook
domain: vault
parent: "[[compute]]"
related:
  - "[[EDEN GPU jobs]]"
  - "[[EDEN job templates]]"
  - "[[EDEN monitoring and troubleshooting]]"
tags: [handbook, hpc]
created: 2026-10-27
updated: 2026-10-27
---
# EDEN Slurm basics and partitions

## Commands

- `sinfo`: partitions, nodes, states [V].
- `squeue`, `squeue -u $USER`: running and pending jobs [V].
- `srun`: real-time commands, tests, interactive shells [V].
- `sbatch`: submit a batch script [V].
- `scontrol show node <node>`, `scontrol show job <id>`, `scontrol show reservations` [V].
- `sfree`: free resources; `pestat`: per-node load; `sshare -l`: fairshare [V].
- `scancel <jobid>` [V].
- `sacct -A <group>`, `sreport cluster accountutilizationbyuser accounts=<group>`, `sshare -laA <group>`: group usage [V].
- All submission goes through the login node [V].

## Flags

| Flag | Meaning | Status |
|---|---|---|
| `-A`, `--account=<group>` | research group account | V |
| `-p`, `--partition=<name>` | queue | V |
| `--cpus-per-task=N` | cores | V |
| `--mem=4G` or `--mem=4000M` | RAM for the whole job | V |
| `--gres=gpu:N` | GPUs; `--gres=gpu:0` for none | V |
| `--time=DD-HH:MM:SS` or `HH:MM:SS` | runtime limit | V |
| `-w <node>` | pin a node, e.g. `dgx-3` | V |
| `--job-name`, `--output=logs/%x_%j.log` | naming, logs; `%j` job id | V |
| `--array=0-23%4` | array, 4 at a time | V:slurm |
| `--dependency=afterok:<id>` | chain jobs | V:slurm |
| `--mail-type`, `--mail-user=<email>` | mail | U on cluster mail relay |

- Put `srun` options before `bash`; in `srun --pty bash --time 00:15:00` the `--time` goes to bash and is ignored [V].
- Slurm does not create the log directory: `mkdir -p logs` first [V].

## Defaults and limits

- Omitted `--time`: Slurm assumes the partition maximum, usually several days [V].
- A long default time can block starting before an upcoming reservation [V].
- Omitted resources can give too few CPUs, no GPU, longer waits, higher billing [V].
- Admins may limit running jobs, runtime, CPUs, GPUs, RAM, disk per user or group, and change them mid-semester [V]; numbers unpublished.
- Priority: FairShare or FairTree [V].
- Group `NormShares` vs `EffectvUsage`; `LevelFairshare` below 1 means over-using share and lowered priority [V].
- Group leaders lose the share without the yearly report [V].

## Partitions

- Partitions visible to an account in the `researchers` group [V:run]: `short` (default; 1 day max, 1 h default), `long` (5 days max, 2 days default, QOS `long-part`), `experimental` (5 days), `hopper` (5 days), `hopper-2` (1 day); node mapping in [[EDEN hardware]].
- `student` is used in docs examples (1 CPU, 4 GB, 30 min interactive) [V] but is not a partition for the `researchers` group [V:run].
- Partition access is by Unix group (`AllowGroups=researchers,...`), not by account [V:run].
- Discover:

```bash
sinfo -o "%P %a %l %D %G %c %m %N"
scontrol show partition
scontrol show node dgx-1 | grep -E 'Gres|CPUTot|RealMemory|Partitions'
sacctmgr show qos format=Name,MaxWall,MaxTRESPU,Priority   # [V:slurm] may be denied
```

- Slurm 26.05.2; `SelectType=cons_tres` with `CR_CORE_MEMORY` (cores and memory are consumable); scheduler `backfill`, priority `multifactor` [V:run].
- `MaxArraySize` 50000 and `MaxJobCount` 50000 [V:run].
- `DefMemPerCPU` is 100 MB: always pass `--mem`, otherwise a job gets almost no memory [V:run].
- Accounting enforces associations and limits (`AccountingStorageEnforce=associations,limits`) [V:run].
- Default account of a new user is `null` with `MaxSubmit=0`: a job without `-A <group>` fails with `AssocMaxSubmitJobLimit` [V:run].
- QOS seen: `normal` (default for jobs, no limits shown), `long-part` (long partition), `student` (20 submitted jobs per user, `cpu=72`, 2 `rtx6000`, `mem=1T` per user), `test-no-fairshare`, `3dgnome` [V:run].
- A reservation `vllm_reservation` holds one H200 and 4 CPUs on `hopper-2` for partition `llm` until 2027-10-05 [V:run].

## Choosing where to run

Look at demand first, then pick the partition, GPU type and time limit that start soonest.

```bash
sfree                                   # free CPUs, GPUs and RAM per node right now [V:run]
squeue -h | wc -l                       # jobs in the queue (89 at the probe) [V:run]
squeue -t PD -o "%.10i %.9P %.12u %.5D %.5C %.8b %.19S %R" | head -20   # who waits, for what, expected start [V:slurm]
squeue --start -u $USER                 # expected start of your pending jobs [V:slurm]
sbatch --test-only -p short -A <group> --gres=gpu:a100:1 -c 8 --mem=32G -t 04:00:00 job.sh   # dry run: reports the planned node and start time, submits nothing [V:slurm]
sprio -l                                # priority terms of pending jobs [V:slurm]
sshare -l                               # fair-share state of your account [V:run]
```

- Live dashboards (status page and the Grafana `eden-overview` dashboard, links in the hub) show node load and GPU use over time; use them to see whether a busy hour will pass.
- `sfree` is the quickest decision aid: it lists free CPUs, GPUs and RAM per node, so you can see which GPU type has room.
- Jobs up to 1 day fit in `short`; longer ones need `long` (5 days, QOS `long-part`, same priority value 0 as `normal`) [V:run].
- The scheduler is `backfill` [V:run], so a job with a realistic `--time` can start in a gap that a maximum-length job cannot [V:slurm].
- A100 40 GB (`dgx-*`, 32 GPUs) is the large default pool; `hopper` (8 H100) and `hopper-2` (H200) are single nodes that fill quickly, so check `sfree` before asking for them.
- CPU-only work: omit `--gres`; `short` and `long` contain both DGX and CPU-only `sr-*` nodes, so Slurm may place it on either; pin `-w sr-3` for a CPU node [V:slurm].
- Many small jobs: use one array (maximum size 50000), not hundreds of separate submissions.
- If nothing is free, shrink the request (fewer CPUs, less RAM, shorter time) instead of waiting for a big node.

## Why pending

- Docs have an FAQ entry for PENDING with free-looking resources; body is a separate page, not fetched [U]. A job needed about one minute to start on a free A100 in `short` [V:run].
- Typical reasons: `Priority`, `Resources`, `ReqNodeNotAvail` (reservation), `AssocGrpCPURunMinutesLimit`/group limits [V:slurm].
- Check: `squeue -u $USER -o "%.10i %.12P %.20j %.8T %.10M %.10l %R"`, `scontrol show job <id> | grep -i reason`.
