---
title: "EDEN Python environments"
type: handbook
domain: vault
parent: "[[compute]]"
related:
  - "[[EDEN job templates]]"
  - "[[EDEN data sync workflows]]"
  - "[[EDEN GPU jobs]]"
tags: [handbook, hpc]
created: 2026-10-27
updated: 2026-10-27
---
# EDEN Python environments

## Facts

- Docs do not describe `module`, conda, uv or Python versions [V that absent].
- Login node: Python 3.12.3 and `pip` present; `venv` and `ensurepip` import; no `uv`, `conda`, `mamba` and no `module` command; `git`, `rsync`, `tmux`, `screen`, `curl`, `wget`, `lfs` present; no Apptainer, Singularity or Docker [V:run].
- Build environments on the cluster so binary wheels match the OS and CPU [U, standard].
- Home is shared with DGX nodes and the login node, so a venv in home works inside jobs [V].
- Login and compute nodes both reach PyPI and Hugging Face over HTTPS [V:run], so packages and models can also be fetched inside a job.

## Install uv in home (if missing)

```bash
curl -LsSf https://astral.sh/uv/install.sh | env UV_NO_MODIFY_PATH=1 sh     # [V:run]: installed uv 0.13.6 into ~/.local/bin without touching shell profiles
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
- Set `export UV_HTTP_TIMEOUT=120`: the default 30 s timed out on one large wheel in a compute-node job; with the larger timeout `uv sync` of a 145-package project took about 10 s from a warm cache [V:run].
- In a batch or `srun` job `~/.local/bin` is not on `PATH`; add `export PATH="$HOME/.local/bin:$PATH"`, otherwise tests that call `uv` fail (4 of 299 failed without it, all passed with it) [V:run].
- A project `.venv` of 145 packages was 785 MB; PyTorch with `cu128` wheels adds about 6 GB of CUDA libraries to a venv [V:run].
- PyTorch does not install `numpy`; add it if code calls `.numpy()` [V:run].
- If the lock pins a CPU-only torch, add the CUDA index in `pyproject.toml` or run `uv pip install torch --index-url https://download.pytorch.org/whl/cu128`; `torch 2.11.0+cu128` installed and ran on an A100 [V:run].
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
huggingface-cli download <org>/<model>
```

- Compute nodes have internet [V:run], so offline mode is optional; set `export HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1` anyway for reproducible runs that must not fetch files.
- Gated models need a token on the login node only; never write it in scripts or the vault.

## Reproducibility

- Log `pip freeze` or `uv pip freeze > logs/freeze_$SLURM_JOB_ID.txt` at job start.
- Pin seeds and write config copy next to results.
