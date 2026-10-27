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

## Why pending

- Docs have an FAQ entry for PENDING with free-looking resources; body is a separate page, not fetched [U]. A job needed about one minute to start on a free A100 in `short` [V:run]."),
])
edit("EDEN storage and quotas.md",[
("| corpora, embeddings, HF cache [U] |","| corpora, embeddings, HF cache; `/mnt/evafs/groups/<group>` exists for many groups "+V+" |"),
("| `/scratch` | shared: login + DGX | 24 NVMe, 332.6 TiB | temporary data during computation only [V] |","| `/scratch` | docs: login + DGX | 24 NVMe, 332.6 TiB | temporary data during computation only [V]; `/scratch/shared` exists on the login node but not on `dgx-2` "+V+" |"),
("lfs quota -hp <project-id> /mnt/evafs   # [U] cheat sheet; docs mention no quota command","lfs quota -h -u $USER /mnt/evafs     # per-user usage; quota 0k means no limit "+V),
("lfs quota -hg <group> /mnt/evafs        # [U] Lustre group quota form","lfs quota -h -g <unix-group> /mnt/evafs   # group usage "+V+"; the `researchers` group showed no limit"),
("- Description page names Lustre on the AI400X array [V]; whether `/mnt/evafs` is Lustre is [U].","- `/mnt/evafs` is Lustre, 1.6 PB with about 445 TB free at the probe, mounted on login and compute nodes "+V+".
- `df -h $HOME` reports a 200 GB filesystem for the home mount although the user quota is unlimited; treat 200 GB as the practical home limit until tested "+V+"; use group space for large data.
- `$HOME` is `/home2/faculty/<user>` [V:run].
- A compute node has a local `/` of 1.8 TB (about 1.6 TB free) and `/dev/shm` of 504 GB; both are local and temporary [V:run].
- `/raid` does not exist on the login node, as expected for a per-DGX mount [V:run].
- Typical reasons: `Priority`, `Resources`, `ReqNodeNotAvail` (reservation), `AssocGrpCPURunMinutesLimit`/group limits [V:slurm].
- Check: `squeue -u $USER -o "%.10i %.12P %.20j %.8T %.10M %.10l %R"`, `scontrol show job <id> | grep -i reason`.
