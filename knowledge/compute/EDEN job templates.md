---
title: "EDEN job templates"
type: handbook
domain: vault
parent: "[[EDEN overview]]"
tags: [handbook, hpc]
created: 2026-10-27
updated: 2026-10-27
---
# EDEN job templates

- Replace `<partition>`/`<gpu-partition>` after `sinfo` ([[EDEN Slurm basics and partitions]]).
- `<email>` stays in the local copy of a script; never commit it.
- Create the log dir before submitting: `mkdir -p logs` [V].
- Module name `<module>` stands for the project package entry point.

## Docs hello job [V]

```bash
#!/usr/bin/env bash
#SBATCH --partition student
#SBATCH --account=<group>
#SBATCH --cpus-per-task=1
#SBATCH --gres=gpu:0
#SBATCH --mem=4G
#SBATCH --time=00:10:00
#SBATCH --job-name=hello_test
#SBATCH --output=slurm_logs/hello_test-%j.log

python3 hello.py
```

## CPU job (BM25 index) [cheat sheet, U partition]

```bash
#!/usr/bin/env bash
#SBATCH -A <group>
#SBATCH --job-name=bm25-index
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=16gb
#SBATCH --time=00:30:00
#SBATCH --partition=<partition>
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=<email>
#SBATCH --output=logs/%x_%j.log

set -euo pipefail
pwd; hostname; date
cd /home2/<group>/<user>/<project>
source .venv/bin/activate
export HF_HOME=/mnt/evafs/groups/<group>/hf_cache
python -m <module> index --system bm25
date
```

- Smoke test with `srun` on the same flags before `sbatch`.

## GPU job (dense encoding)

```bash
#!/usr/bin/env bash
#SBATCH -A <group>
#SBATCH --job-name=dense-encode
#SBATCH --partition=<gpu-partition>
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64gb
#SBATCH --time=04:00:00
#SBATCH --output=logs/%x_%j.log

set -euo pipefail
cd /home2/<group>/<user>/<project>
source .venv/bin/activate
export HF_HOME=/mnt/evafs/groups/<group>/hf_cache
export HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1
export TOKENIZERS_PARALLELISM=false
nvidia-smi
uv pip freeze > logs/freeze_${SLURM_JOB_ID}.txt
python -m <module> encode --model <hf-model> --batch-size 128 --fp16 \
  --out /mnt/evafs/groups/<group>/artifacts/emb/<model>.npy
```

## Array job: grid from a CSV

```bash
#!/usr/bin/env bash
#SBATCH -A <group>
#SBATCH --job-name=grid
#SBATCH --partition=<gpu-partition>
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=48gb
#SBATCH --time=02:00:00
#SBATCH --array=0-23%4
#SBATCH --output=logs/%x_%A_%a.log

set -euo pipefail
cd /home2/<group>/<user>/<project>
source .venv/bin/activate
export HF_HOME=/mnt/evafs/groups/<group>/hf_cache HF_HUB_OFFLINE=1

# grid.csv: header + one row per cell: system,protocol,lang
ROW=$(sed -n "$((SLURM_ARRAY_TASK_ID + 2))p" grid.csv)
IFS=, read -r S P L <<< "$ROW"
OUT=/mnt/evafs/groups/<group>/artifacts/runs/${S}_${P}_${L}.jsonl
[ -s "$OUT" ] && { echo "skip $OUT"; exit 0; }       # idempotent
python -m <module> run --system "$S" --protocol "$P" --lang "$L" --out "$OUT"
```

- `%4` caps concurrent tasks; max array size is a cluster setting [U]: `scontrol show config | grep MaxArraySize`.
- Rerun failures: `sbatch --array=3,7,12 grid.sh`.
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

## Dependency chain

```bash
#!/usr/bin/env bash
set -euo pipefail
mkdir -p logs
J1=$(sbatch --parsable bm25_index.sh)
J2=$(sbatch --parsable encode.sh)
J3=$(sbatch --parsable --dependency=afterok:${J1}:${J2} grid.sh)        # waits for the whole array
J4=$(sbatch --parsable --dependency=afterok:${J3} bootstrap.sh)
echo "$J1 $J2 $J3 $J4"
squeue -u "$USER" -o "%.10i %.20j %.8T %.20E"
```

- `afterok` on an array id waits for every task to exit 0 [V:slurm].
- `aftercorr` releases task N after task N of the predecessor array succeeds [V:slurm].
- `afterany` runs regardless of status; `afternotok` for cleanup.
- A failed dependency leaves the job pending with `DependencyNeverSatisfied`; cancel with `scancel`.

## Interactive sessions [V]

```bash
srun -p student -A <group> --cpus-per-task=1 --mem=4G --time=00:30:00 --pty bash
srun -p <gpu-partition> -A <group> --gres=gpu:1 --cpus-per-task=8 --mem=32G --time=01:00:00 --pty bash   # [U partition]
srun -w dgx-3 --time 00:15:00 --pty --account <group> bash
```

- Options before `bash`; `--time` after it is ignored [V].
- Run inside `tmux` ([[EDEN access and networking]]).

## Jupyter job [V]

```bash
#!/bin/bash
#SBATCH --nodes 1
#SBATCH --cpus-per-task 5
#SBATCH --time 03:00:00
#SBATCH --job-name jupyter-notebook
#SBATCH --account=<group>
#SBATCH --output=logs/%x_%j.log

port=<port>
node=$(hostname -s)
source .venv/bin/activate
jupyter-notebook --no-browser --port=${port} --ip=${node}
```

- `squeue -u $USER` for the node, then the tunnel in [[EDEN access and networking]].
