---
title: "EDEN Python environments"
type: handbook
domain: vault
parent: "[[EDEN overview]]"
tags: [handbook, hpc]
created: 2026-10-27
updated: 2026-10-27
---
# EDEN Python environments

## Facts

- Docs do not describe `module`, conda, uv or Python versions [V that absent].
- Check availability first: `python3 --version; which uv conda; module avail 2>&1 | head` [U].
- Build environments on the cluster so binary wheels match the OS and CPU [U, standard].
- Home is shared with DGX nodes and the login node, so a venv in home works inside jobs [V].
- Compute nodes' internet access is not documented [U]; install packages on the login node.

## Install uv in home (if missing)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh     # [U] needs outbound internet from the login node
export PATH="$HOME/.local/bin:$PATH"
uv --version
```

## Project venv with uv

```bash
cd /home2/<group>/<user>/<project>        # or $HOME/<project>
uv python install 3.12                    # only if system Python is too old
uv sync --frozen                          # from pyproject.toml + uv.lock
source .venv/bin/activate
python -c "import torch; print(torch.__version__, torch.version.cuda)"
```

- `--frozen` installs exactly `uv.lock`.
- If the lock pins a CPU-only torch, add the CUDA index in `pyproject.toml` or run `uv pip install torch --index-url https://download.pytorch.org/whl/cu124` [U on CUDA tag].
- Rebuild instead of copying `.venv` from a laptop (macOS wheels do not run on Linux).

## Plain venv

```bash
python3 -m venv /mnt/evafs/groups/<group>/venvs/nlp      # shared group venv [U path]
source /mnt/evafs/groups/<group>/venvs/nlp/bin/activate
pip install -U pip
pip install -r requirements.txt
```

- Shared group venv: activate in the sbatch script before running [U, cheat sheet].
- One writer only; others use it read-only.

## HuggingFace cache and offline mode

```bash
# ~/.bashrc and every sbatch script
export HF_HOME=/mnt/evafs/groups/<group>/hf_cache
export HF_HUB_CACHE=$HF_HOME/hub
export TRANSFORMERS_CACHE=$HF_HOME/hub     # legacy name, harmless
export SENTENCE_TRANSFORMERS_HOME=$HF_HOME/sbert
```

- Default `~/.cache/huggingface` fills the home space; always set `HF_HOME`.
- Pre-download on the login node:

```bash
mkdir -p "$HF_HOME"
huggingface-cli download BAAI/bge-m3
huggingface-cli download intfloat/multilingual-e5-large
huggingface-cli download BAAI/bge-reranker-v2-m3
```

- Then in jobs: `export HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1` so a missing file fails fast instead of hanging [U that compute nodes lack internet].
- Model ids above are examples; the project's actual list lives in `configs/experiment.yaml`.
- Gated models need a token on the login node only; never write it in scripts or the vault.

## Reproducibility

- Log `pip freeze` or `uv pip freeze > logs/freeze_$SLURM_JOB_ID.txt` at job start.
- Pin seeds and write config copy next to results.
- Related: [[EDEN job templates]], [[EDEN data sync workflows]], [[EDEN GPU jobs]].
