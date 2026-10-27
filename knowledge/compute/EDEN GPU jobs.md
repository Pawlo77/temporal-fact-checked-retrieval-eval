---
title: "EDEN GPU jobs"
type: handbook
domain: vault
parent: "[[compute]]"
related:
  - "[[EDEN job templates]]"
  - "[[EDEN Slurm basics and partitions]]"
tags: [handbook, hpc]
created: 2026-10-27
updated: 2026-10-27
---
# EDEN GPU jobs

## Requesting GPUs

- `--gres=gpu:N` is the documented form; `--gres=gpu:1` example [V].
- `--gres=gpu:0` explicitly requests none (tutorial CPU job) [V].
- Syntax `gpu[:type]:count`, count defaults to 1 [V:slurm].
- Typed form `--gres=gpu:a100:1` works [V:run]; types: `a100`, `h100`, `h200`, `h200_4g.71gb`, `h200_3g.71gb`, `tesla`.
- `--gres` and `--gpus-per-node` cannot be combined [V:slurm].
- Without a GPU request a job sees no GPU [V].
- Reservations are exclusive [V].

```bash
sinfo -o "%P %N %G"                                 # gres per node
scontrol show node dgx-1 | grep -i gres             # exact gres names and counts
scontrol show node hopper | grep -i -E 'gres|cpu'
```

## Which GPU

- A100 40 GB on `dgx-1`..`dgx-4`, in partitions `short` and `long` [V hardware, [V:run] partition].
- H100 80 GiB `hopper`, H200 140 GiB `hopper-2`: larger batches, long contexts [V hardware].
- RTX 6000 Blackwell 95 GiB on `stud-2`, `stud-3`: teaching queue, students [V].
- Pin node only when needed: `-w dgx-3` [V]; otherwise let the scheduler choose.
- Request 1 GPU unless code uses `DataParallel`/`torchrun`; unused GPUs idle but billed.

## CPU and RAM per GPU

- DGX node: 128 cores and 1-2 TiB for 8 GPUs, i.e. 16 cores and 128-256 GB per GPU as a fair share [V hardware, derived].
- Dataloader workers: `--cpus-per-task=8` for one GPU; tokenisation is the usual bottleneck [U].
- RAM: 2x the on-disk size of the largest array loaded, plus 16 GB [U].

## Sanity check inside a job

```bash
nvidia-smi
python - <<'PY'
import torch
print(torch.__version__, torch.version.cuda, torch.cuda.is_available())
print(torch.cuda.get_device_name(0), torch.cuda.mem_get_info())
PY
```

- Never test CUDA on the login node; no GPU and no `nvidia-smi` there [V:run].
- `CUDA_VISIBLE_DEVICES` is set by Slurm to the allocated GPU [V:run] (a 1-GPU job saw `0`).

## Driver and toolkit [V:run]

- Compute node driver `595.71.05`, reporting CUDA 13.2: current `cu12x` and `cu13x` wheels run.
- A CUDA 12.8 toolkit sits in `/usr/local/cuda-12.8`; `nvcc` is not on `PATH`, so add it only for builds.
- No PyTorch is preinstalled: install it in your own environment ([[EDEN Python environments]]).
- Open-file limit is 1024: raise `ulimit -n` in the job script for many dataloader workers.

## CUDA errors

- `CUDA_ERROR_UNSUPPORTED_PTX_VERSION (222)`: library or PTX mismatch; recompile on the host where it runs or use wheels built for that architecture [V].
- Architectures differ across A100 (sm_80), H100/H200 (sm_90), P100 (sm_60), Blackwell (sm_120); use recent torch wheels (cu12x) [U on exact versions].
- A P100 (`pascal`, sm_60): `torch 2.11.0+cu128` loaded but every matmul failed with an accelerator error, although `torch.cuda.is_bf16_supported()` returned True; use an older torch with sm_60 kernels or another GPU, and do not trust that flag on Pascal [V:run].
- A100 (sm_80): `torch 2.11.0+cu128` works, bf16 supported, host-to-GPU copy 9.9 GiB/s with pinned memory [V:run].
- Blackwell RTX 6000 needs a torch build with sm_120 support [U]; H100 and H200 (sm_90) were not probed because their queues were hours long [V:run].
- `CUDA out of memory`: lower batch size, use fp16/bf16, sort by length, free cache (`torch.cuda.empty_cache()`).
- bf16 requires Ampere or newer; the P100 reported bf16 as supported yet failed (see above), so use fp16 or skip it [V:run].

## VRAM sizing rules of thumb [U]

- Weights: params x 2 B in fp16/bf16; params x 4 B in fp32.
- Inference activations: batch x seq_len x hidden x layers dominated; start with batch 64, seq 256 and double until 80 percent of VRAM.

## Multi-GPU

- `--gres=gpu:4` plus `torchrun --nproc_per_node=4`; only worthwhile for training, not for inference [U].
- Multi-node over InfiniBand is DGX only, 200 Gb/s [V hardware].
