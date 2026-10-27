---
title: "EDEN Slurm basics and partitions"
type: handbook
domain: vault
parent: "[[EDEN overview]]"
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

- `student`: appears in all docs examples, 1 CPU, 4 GB, 30 min interactive [V].
- Other partition names (`short`, GPU, CPU): not published; `short` appears in the cheat sheet [U].
- Discover: 

```bash
sinfo -o "%P %a %l %D %G %c %m %N"
scontrol show partition
scontrol show node dgx-1 | grep -E 'Gres|CPUTot|RealMemory|Partitions'
sacctmgr show qos format=Name,MaxWall,MaxTRESPU,Priority   # [V:slurm] may be denied
```

- Record the findings in this note and flip [U] to [V].

## Why pending

- Docs have an FAQ entry for PENDING with free-looking resources; body is a separate page, not fetched [U].
- Typical reasons: `Priority`, `Resources`, `ReqNodeNotAvail` (reservation), `AssocGrpCPURunMinutesLimit`/group limits [V:slurm].
- Check: `squeue -u $USER -o "%.10i %.12P %.20j %.8T %.10M %.10l %R"`, `scontrol show job <id> | grep -i reason`.

## Related

- [[EDEN GPU jobs]], [[EDEN job templates]], [[EDEN monitoring and troubleshooting]].
