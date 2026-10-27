---
title: "compute plan"
type: handbook
domain: vault
parent: "[[compute]]"
related:
  - "[[EDEN hardware]]"
  - "[[EDEN GPU jobs]]"
  - "[[EDEN storage and quotas]]"
  - "[[EDEN data sync workflows]]"
  - "[[EDEN Python environments]]"
  - "[[EDEN job templates]]"
tags: [handbook, hpc]
created: 2026-10-27
updated: 2026-10-27
---
# compute plan

- Every throughput below is an assumed range [U], not a measurement; arithmetic on those assumptions was executed. Replace with measured numbers from the probe job below.
- Project-specific note: the other EDEN notes in [[compute]] are generic cluster documentation.
- Symbols: N = 206,000 fact-checks; Q = queries (posts) per language and protocol; k = rerank depth; D = embedding dim.

## Pipeline stages

| Stage | Resource | Frequency |
|---|---|---|
| BM25 index of N fact-checks | CPU | once per tokeniser/config |
| Dense encode N fact-checks | 1 GPU | once per model |
| Encode Q queries per language | 1 GPU, small | per model and language |
| Dense retrieval (matmul/FAISS) | CPU or GPU | per cell |
| Cross-encoder rerank top-k | 1 GPU | per cell; heaviest |
| Bootstrap evaluation | CPU | per cell |

## Indexing 206k fact-checks (BM25)

- CPU only; no GPU: `--cpus-per-task=8 --mem=16gb --time=00:30:00` [U sizing].
- Index size is a small multiple of raw text; keep it in group space [U].
- CPU-only BM25 and bootstrap can use `sr-*` nodes (3 TiB RAM each) if a partition exposes them [U on partition mapping].
- Tokenisation per language may be single-threaded; extra cores help only if the code parallelises [U].

## Dense encoding of fact-checks

- Models in scope: multilingual dense encoders of ~0.5B parameters (examples `bge-m3`, `multilingual-e5-large`) [U on param counts]; reranker example `bge-reranker-v2-m3`; the actual list lives in `configs/experiment.yaml`.
- Pre-download on the login node (see [[EDEN Python environments]]): `huggingface-cli download BAAI/bge-m3`, `intfloat/multilingual-e5-large`, `BAAI/bge-reranker-v2-m3`.
- Weights in fp16: 0.5B x 2 B = ~1 GB; fp32: ~2 GB.
- Embedding matrix N x D (executed arithmetic):

| D | fp32 | fp16 |
|---|---|---|
| 384 | 0.295 GiB | 0.147 GiB |
| 768 | 0.589 GiB | 0.295 GiB |
| 1024 | 0.786 GiB | 0.393 GiB |

- Store as `.npy` in group space; one file per model; load with `np.load(mmap_mode="r")`.
- Fits entirely in RAM and in any GPU in [[EDEN hardware]].
- Encoding and reranking fit in 16 GB VRAM for 0.5B-parameter models in fp16.
- GPU choice: A100 40 GB (`dgx-1`..`dgx-4`) is the default for encoders and rerankers; H100/H200 are faster but scarcer [U on queue pressure]; see [[EDEN GPU jobs]].
- GPU memory at inference: weights ~1 GB + activations; batch 128, seq 256 fits in 16 GB in fp16 [U]; A100 40 GB leaves headroom.
- Runtime = N / throughput. Assumed 200-1000 docs/s (fp16, seq 256, A100) [U]: 1,030 s (17.2 min) to 206 s (3.4 min).
- Fact-check text length varies; sort by length to cut padding.
- Request: `--gres=gpu:1 --cpus-per-task=8 --mem=64gb --time=02:00:00` (3-10x margin) [U].
- Checkpoint shards of 20k docs so a timeout loses little; skip finished shards on rerun.

## Query encoding

- Q is small per language; encode in the same job as the corpus or in each grid cell if under a minute [U].
- Cache query embeddings per (model, language).

## Dense retrieval

- Exact matmul: Q x N scores; Q=5,000 gives 1.03e9 floats = ~3.8 GiB fp32 if unchunked; chunk queries by 512 [executed arithmetic: 5000 x 206000 x 4 B].
- Keep top-k with `torch.topk` per chunk; no FAISS needed at this N [U].
- CPU is enough (seconds to minutes) [U].

## Cross-encoder reranking

- Pairs = Q x k; each pair is a forward pass of ~0.5B-parameter model [U].
- Assumed 100-500 pairs/s (fp16, seq 384, A100) [U]. Executed arithmetic:

| Q | k | Pairs | At 100 pairs/s | At 500 pairs/s |
|---|---|---|---|---|
| 1,000 | 50 | 50,000 | 8.3 min | 1.7 min |
| 1,000 | 100 | 100,000 | 16.7 min | 3.3 min |
| 5,000 | 100 | 500,000 | 83.3 min | 16.7 min |

- Rerank cost scales with k and Q; choose k from the recall@k curve of the first stage.
- Share first-stage candidates across rerank cells of one language and protocol.
- GPU memory: weights ~1 GB; batch 32 pairs x seq 384 is a few GB [U]; raise batch until 80 percent VRAM.
- Request: `--gres=gpu:1 --mem=48gb --time=02:00:00` per cell, tune after probe [U].

## Bootstrap evaluation

- CPU only; resample queries B times (for example B = 1,000) and recompute the metric on stored rankings [U].
- Vectorise with numpy: ranks array of shape Q; per replicate index sampling; seconds to minutes per cell [U].
- Inputs are run files; no model or GPU; `--cpus-per-task=4 --mem=8gb --time=00:30:00` [U].
- Keep the seed in the run config.

## Job grid: systems x protocols x languages

- Example grid: systems {`bm25`, `dense`, `rerank`} x protocols {`monolingual`, `crosslingual`} x languages {`en`, `de`, `es`, `pt`} = 3 x 2 x 4 = 24 cells; placeholders, take the real axes from `configs/experiment.yaml`.
- Dense models multiply the `dense` and `rerank` axes by the number of models.
- Array: `--array=0-23%4`; array template in [[EDEN job templates]] (CSV columns `a,b,c` = system, protocol, language).
- Task index to cell arithmetic without a CSV:

```bash
SYSTEMS=(bm25 dense rerank); PROTOCOLS=(monolingual crosslingual); LANGS=(en de es pt)
i=$SLURM_ARRAY_TASK_ID
S=${SYSTEMS[$((i / 8))]}; P=${PROTOCOLS[$(((i / 4) % 2))]}; L=${LANGS[$((i % 4))]}
```

- Generate `grid.csv`:

```bash
python - <<'PY' > grid.csv
import itertools
print("system,protocol,lang")
for s, p, l in itertools.product(["bm25", "dense", "rerank"], ["monolingual", "crosslingual"], ["en", "de", "es", "pt"]):
    print(f"{s},{p},{l}")
PY
```

- Order: BM25 index and dense encode first, grid second, bootstrap last (dependency chain in [[EDEN job templates]]: stage1 = BM25 index, stage2 = dense encode, cells = grid, stage4 = bootstrap).
- Cells are idempotent: skip when the run file exists.
- GPU tasks (`dense`, `rerank`) and CPU tasks (`bm25`) go in separate arrays so CPU cells do not hold GPUs.
- Total GPU time = sum over GPU cells of probe-measured minutes; fits well within a few GPU-hours at the assumed rates [U].

## Probe job (replace assumptions)

```bash
#!/usr/bin/env bash
#SBATCH -A <group>
#SBATCH --job-name=probe
#SBATCH --partition=<gpu-partition>
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=48gb
#SBATCH --time=00:30:00
#SBATCH --output=logs/%x_%j.log

set -euo pipefail
cd /home2/<group>/<user>/<project>
source .venv/bin/activate
export HF_HOME=/mnt/evafs/groups/<group>/hf_cache HF_HUB_OFFLINE=1
nvidia-smi --query-gpu=name,memory.total --format=csv
python -m <module> encode --model <hf-model> --limit 5000 --batch-size 128 --fp16 --time-it
python -m <module> rerank --model <hf-reranker> --queries 200 --k 100 --batch-size 32 --time-it
```

- After the run: `sacct -j <jobid> -o Elapsed,MaxRSS` and `seff <jobid>`; extrapolate: docs/s x 206,000 and pairs/s x Q x k.
- Write measured throughput into this note and flip [U] to [V].

## Storage footprint and placement

- Embeddings: 0.3-0.8 GiB per model (table above).
- Run files: one JSONL per cell, ranked ids for Q queries; small (MiB). Pull only these back; leave embeddings on the cluster.
- Code: `$HOME/<project>` (git clone or [[EDEN data sync workflows]]).
- Fact-check corpus, posts, qrels: `/mnt/evafs/groups/<group>/data/` once, one shared copy for all jobs [U path].
- Embeddings, indexes, run files: `/mnt/evafs/groups/<group>/artifacts/` [U path].
- HF model cache: `/mnt/evafs/groups/<group>/hf_cache`; generic setup in [[EDEN Python environments]].
- Quotas and `/scratch`, `/raid`: [[EDEN storage and quotas]].
- The LLM pilot service on EDEN is not used by this project.
