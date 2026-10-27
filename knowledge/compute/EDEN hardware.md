---
title: "EDEN hardware"
type: handbook
domain: vault
parent: "[[compute]]"
related:
  - "[[EDEN GPU jobs]]"
  - "[[EDEN Slurm basics and partitions]]"
tags: [handbook, hpc]
created: 2026-10-27
updated: 2026-10-27
---
# EDEN hardware

## Compute nodes (description page, 2026-10-27) [V]

| Node | Machine | CPU per node | GPU | RAM |
|---|---|---|---|---|
| `dgx-1` | NVIDIA DGX A100 | 2x AMD Rome 7742 (128 cores) | 8x A100 40 GB | 2 TiB |
| `dgx-2`..`dgx-4` | NVIDIA DGX A100 | same | 8x A100 40 GiB | 1 TiB |
| `sr-1`..`sr-3` | Lenovo SR665 | 2x EPYC 7413 (48 cores) | none | 3 TiB |
| `hopper` | Lenovo SR675 | 2x EPYC 9534 (64 cores) | 8x H100 PCIe 80 GiB | 1 TiB |
| `hopper-2` | Dell XE9680 | 2x Xeon Platinum 8570 (112 cores) | 8x H200 140 GiB | 2 TiB |
| `pascal` | Dell C4130 | 2x Xeon E5-2695 v4 (36 cores) | 4x Tesla P100 16 GB | 0.5 TiB |
| `stud-1` | Dell R770 | Xeon 6520P (32 cores) | none | 0.74 TiB |
| `stud-2`, `stud-3` | Dell R770 | Xeon 6520P (32 cores) | 2x RTX 6000 Blackwell SE 95 GiB each | 0.74 TiB |

- Virtualization nodes `virt-1`, `virt-2` (Proxmox) are not for jobs [V].
- GPU totals: 32 A100, 8 H200, 8 H100, 4 P100, 4 RTX 6000 Blackwell [V].
- Teaching nodes `stud-*` serve course and thesis students; partition `student` is used in docs examples [V].
- `hopper-2` added Feb 2026; `stud-*` added May 2026 and opened to students Oct 2026 [V].

## Interconnect and storage hardware [V]

- InfiniBand 200 Gb/s on DGX nodes; Ethernet 100 Gb/s everywhere.
- DDN SS9012 array: 1.6 PiB; DDN AI400X: 256 TiB cache.
- DGX local SSD: 3.8 TiB + 15 TiB per node; `/raid` NVMe RAID 0 on DGX.
- Description page and grant text disagree (GPU count 44/48/56, DDN 1.5 vs 1.6 PiB); trust per-node table.

## Notes

- Snapshot from `sfree` (2026-10-27): A100 nodes had 0 to 8 of 8 GPUs free, `hopper` 2 of 8, `hopper-2` 5 of 12 gres, `pascal` 4 of 4; it varies by the hour [V:run].
- P100 lacks bf16 and flash-attention support; use fp16 or skip [U].
- `sr-*` nodes (CPU-only, about 1 TiB RAM visible to Slurm, 48 cores) take CPU-only jobs in partitions `short` and `long` [V:run].
- Login node: Ubuntu 24.04, 8 cores, 62 GB RAM, no GPU, shared by many users at once; keep heavy work off it [V:run].
- `stud-*` nodes and a `student` partition are not visible to an account in the `researchers` group [V:run].
- `hopper-2` exposes 4 whole H200 plus MIG slices (`h200_4g.71gb` x4, `h200_3g.71gb` x4) [V:run].

## Partition per node [V:run]

| Partition | Nodes | GPUs (Slurm gres) | Max time | Default time |
|---|---|---|---|---|
| `short` (default) | `dgx-[1-4]`, `sr-[1-3]` | `a100` x8 per DGX | 1 day | 1 h |
| `long` | `dgx-[1-4]`, `sr-[1-2]` | `a100` x8 per DGX | 5 days | 2 days |
| `experimental` | `pascal` | `tesla` x4 | 5 days | 1 day |
| `hopper` | `hopper` | `h100` x8 | 5 days | 1 day |
| `hopper-2` | `hopper-2` | `h200` x4 + MIG slices | 1 day | 1 day |

- The DGX GPU observed on a compute node was `NVIDIA A100-SXM4-40GB` (40 GiB) [V:run].
- Per-node memory seen by Slurm: about 1 TiB on `dgx-[2-4]`, 2 TiB on `dgx-1` and `hopper-2` [V:run].
