---
title: "EDEN data sync workflows"
type: handbook
domain: vault
parent: "[[compute]]"
related:
  - "[[EDEN storage and quotas]]"
  - "[[EDEN Python environments]]"
tags: [handbook, hpc]
created: 2026-10-27
updated: 2026-10-27
---
# EDEN data sync workflows

## Principles

- Code via git or rsync; data once to group storage; results back by rsync [U, practice].
- Gateway home and cluster home are separate (the gateway home is on an NFS share, and a directory present on the cluster home was absent there) [V:run]; direct `rsync -az ./ eden:path/` through the jump host works [V:run], so the two-hop copy is unnecessary.
- Prefer the direct jump-host form (one command) [V that jump form works for ssh].
- Never sync secrets (`.env`, tokens, ssh keys).
- `--exclude='.*'` also drops `.git`, `.venv`, `.env`; list excludes explicitly when you need `.git`.

## Cheat-sheet two-hop sync (code)

```bash
# 1. laptop -> gateway
rsync -avz <dir>/ <user>@<mini-ssh-gateway>:~/<dir>/ \
  --exclude='.*' --exclude='__pycache__/' --exclude='*.pyc' --exclude='*.pyo'

# 2. from the gateway -> cluster home (run on the gateway)
rsync -avz ~/<dir>/ <user>@<eden-login-node>:/home2/<group>/<user>/<dir>/ \
  --exclude='.*' --exclude='__pycache__/' --exclude='*.pyc' --exclude='*.pyo'
```

## One-hop sync via jump host

```bash
rsync -avz --partial --progress \
  -e "ssh -J <mini-login>@<mini-ssh-gateway>" \
  --exclude='.git/' --exclude='.venv/' --exclude='.env' --exclude='__pycache__/' \
  --exclude='*.pyc' --exclude='mlruns/' --exclude='data/' --exclude='artifacts/' \
  ./ <user>@<eden-login-node>:/home2/<group>/<user>/<project>/
```

- Dry run first: add `-n`; use `--delete` only after reading the dry run.
- `--partial --progress` for flaky links.
- With the `eden` ssh alias ([[EDEN access and networking]]): `rsync -avz ./ eden:~/<project>/`.

## Data upload (once)

```bash
rsync -avz --partial --progress -e "ssh -J <mini-login>@<mini-ssh-gateway>" \
  data/raw/ <user>@<eden-login-node>:/mnt/evafs/groups/<group>/data/raw/
```

- Compress many small files first: `tar -cf - data/raw | zstd -T0 > raw.tar.zst`, copy, unpack on the cluster.
- Verify: `rsync -avzc -n` or `sha256sum` on both sides.
- Large datasets: one copy in group space shared by all jobs [V that group space exists, U path].

## Results back

```bash
rsync -avz --partial --progress -e "ssh -J <mini-login>@<mini-ssh-gateway>" \
  <user>@<eden-login-node>:/mnt/evafs/groups/<group>/artifacts/runs/ ./runs_from_eden/
```

- Pull only small result files (run files, metrics); leave large arrays on the cluster.
- Fetch `/raid` results from a DGX through `/mnt/workspace/dgx-N` on the login node [V].
- Archive long-term results elsewhere; no guaranteed backup [V].

## Checks

- Free space before big copies: `df -h /mnt/evafs/groups/<group>`; the path exists [V:run].
- A full group space blocks writes for all members [V].
