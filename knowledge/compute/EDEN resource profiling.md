---
title: "EDEN resource profiling"
type: handbook
domain: vault
parent: "[[compute]]"
related:
  - "[[EDEN monitoring and troubleshooting]]"
  - "[[EDEN GPU jobs]]"
  - "[[EDEN Slurm basics and partitions]]"
  - "[[EDEN job templates]]"
tags: [handbook, hpc]
created: 2026-10-27
updated: 2026-10-27
---
# EDEN resource profiling

Measure what a job really uses against what it was allocated, so the next run asks for the minimum, and find the bottleneck (disk, RAM, CPU, GPU feeding). Status markers follow the legend in [[compute]]; nothing here is verified on EDEN yet unless marked.

## After the run

```bash
sacct -j <jobid> -o JobID,State,Elapsed,TotalCPU,AllocCPUS,ReqMem,MaxRSS,AveRSS,MaxVMSize,AveDiskRead,AveDiskWrite,AllocTRES%40   # [V:slurm]
```

- CPU efficiency = `TotalCPU / (Elapsed x AllocCPUS)`; far below 1 means too many cores or an I/O wait [V:slurm].
- Memory efficiency = `MaxRSS / ReqMem`; request `1.2 x MaxRSS` next time [V:slurm].
- `MaxRSS` and the disk fields are filled only if the accounting gather plugin is on: check `scontrol show config | grep -i -E 'JobAcctGather|AcctGatherProfile'` [U].
- `seff` is not installed [V:run]; compute the two ratios from `sacct` instead.

## While it runs

```bash
sstat -j <jobid>.batch -o JobID,AveCPU,MaxRSS,AveRSS,MaxDiskRead,MaxDiskWrite   # [V:slurm, needs the gather plugin]
srun --jobid=<jobid> --overlap --pty nvidia-smi                                  # GPU view inside the allocation [V:slurm, U on EDEN]
```

- `nvidia-smi` exists on GPU compute nodes and not on the login node [V:run].

## Inside the job

```bash
nvidia-smi --query-gpu=timestamp,utilization.gpu,utilization.memory,memory.used,power.draw --format=csv -l 5 > logs/gpu_$SLURM_JOB_ID.csv &   # [V:slurm]
/usr/bin/time -v python -m <module> ...                                          # peak RSS, I/O wait counts [standard, U that installed]
```

- Python side: `psutil` samples CPU, RAM and disk counters; MLflow can log them with `MLFLOW_ENABLE_SYSTEM_METRICS_LOGGING=true` (needs `psutil` and `pynvml`) [standard, U on EDEN].
- Log throughput (items per second) per phase: data loading, forward, backward, write.

## Reading the numbers

| Observation | Likely bottleneck | Check or fix |
|---|---|---|
| GPU utilization below 70 percent with high CPU use | dataloader or tokenisation | more `--cpus-per-task`, pre-tokenise |
| GPU utilization low, CPU low, long reads | disk or network read | copy to node-local disk or `/dev/shm`, pack small files |
| Utilization spiky, step time varies | many small files on Lustre | one archive or `.npy` per shard (docs measure about 0.7 MiB/s for small files) [V] |
| `MaxRSS` near `ReqMem`, swap or kills | RAM | raise `--mem`, stream, use memory maps |
| GPU memory full, utilization high | batch fits, compute bound | profile kernels; nothing to allocate more |
| Many idle cores in `TotalCPU` | over-allocated CPUs | cut `--cpus-per-task` |

## Right-sizing procedure

1. Run a small slice (a few minutes) with generous limits and the sampling above.
2. Read `MaxRSS`, GPU utilization and throughput; set `--mem` to 1.2 x `MaxRSS`, `--cpus-per-task` to the core count that keeps the GPU busy, `--time` to 1.3 x the measured time.
3. Re-run and compare the ratios; record them in the experiment config.

## Raw hardware speed checks

- Disk: `dd if=/dev/zero of=<path>/t bs=1M count=1024 oflag=direct` on home, group space, `/dev/shm` and node-local `/`; docs give 669 MiB/s for home and 1.3 GiB/s for `/raid` [V docs].
- RAM and CPU: a short `python -c` loop with `numpy` timing is enough to compare nodes; use `pestat` for node load [V:run].
- GPU: copy bandwidth and matmul throughput through `torch` on one device; compare A100, H100 and H200 only when the queue allows [U].
