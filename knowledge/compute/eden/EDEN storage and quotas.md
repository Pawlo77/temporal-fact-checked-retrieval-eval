---
title: "EDEN storage and quotas"
type: handbook
domain: vault
parent: "[[EDEN compute]]"
related:
  - "[[EDEN data sync workflows]]"
  - "[[EDEN Python environments]]"
tags: [handbook, hpc]
created: 2026-10-27
updated: 2026-11-18
---
# EDEN storage and quotas

## Filesystems

| Path | Scope | Backing | Use |
|---|---|---|---|
| `/home2/<group>/<user>` | shared: login node + `dgx-[1-4]` | DDN array, HDD | default for code, venvs, results [V] |
| `/mnt/evafs/groups/<group>/` | group-shared | storage array (path from cheat sheet) | corpora, embeddings, HF cache; `/mnt/evafs/groups/<group>` exists for many groups [V:run] |
| `/scratch` | shared: login + DGX | 24 NVMe, 332.6 TiB | temporary data during computation only [V]; `/scratch/shared` exists on the login node but `/scratch` is absent on `dgx-2` and `pascal` [V:run] |
| `/raid` | per DGX, not shared | 4x NVMe RAID 0 | I/O-heavy job-local data [V] |
| `/mnt/workspace/dgx-[1-4]` | login node view of each `/raid` | NFS | fetch results from a DGX `/raid` [V] |

- Cheat sheet writes home as `/home2/faculty/<user>`; docs say `/home2/<group>/<login>` [V]; check with `echo $HOME`.
- Each user has a private space and a group space on the array, capped separately [V].
- Users in several groups get each group space [V].
- A full group space blocks new writes for the whole group [V].
- `/mnt/evafs/groups/<group>` is owned by `root:<group>` with mode `2770`; it is writable only for members of that Unix group. A Slurm account name does not imply Unix membership: an account in the `researchers` group but not in `<group>` could list the parent and not write [V:run]; check with `id`.
- Numeric quotas are not published [V that absent; values U].
- Local node disks are shared and temporary; remove or archive after a run [V].

## Measured write speeds (docs, `dd`, simplified) [V]

| Target | 1 GiB file | 1000 x 512 B files |
|---|---|---|
| home (DDN) | 669.2 MiB/s | 721.4 KiB/s |
| `/scratch` | 684.7 MiB/s | 735.5 KiB/s |
| `/raid` | 1.3 GiB/s | 4.1 MiB/s |

- Many small files are slow everywhere; pack with `tar` or store embeddings as one `.npy`.
- Docs warn real I/O differs with access pattern and load [V].

## Quota checks

```bash
id                                   # uid, gids
df -h $HOME                          # filesystem free space (shared array, not your quota) [V:slurm n/a, standard]
du -sh $HOME/* 2>/dev/null | sort -h # biggest dirs
lfs quota -h -p $(lfs project -d ~ | awk '{print $1}') /mnt/evafs   # home project quota: bytes and files [V:run]
lfs quota -h -u $USER /mnt/evafs     # per-user usage; quota 0k means no limit [V:run]
lfs quota -h -g <unix-group> /mnt/evafs   # group usage [V:run]; the `researchers` group showed no limit
```

- `/mnt/evafs` is Lustre, 1.6 PB with about 445 TB free at the probe, mounted on login and compute nodes [V:run].
- The home directory is a Lustre project with its own quota: 200 GB and 200,000 files [V:run]. The user quota shows no limit, and `df -h $HOME` shows the 200 GB but not the file count.
- At either limit every write fails with `Disk quota exceeded` while `df` still shows free space; the file count ran out first in one project [V:run]. Use group space for large data.
- `$HOME` is `/home2/faculty/<user>` [V:run].
- A compute node has a local `/` of 1.8 TB (about 1.6 TB free) and `/dev/shm` of 504 GB; both are local and temporary [V:run].
- `/raid` does not exist on the login node or on `pascal`, and exists on `dgx-2` [V:run].

## Keeping disk use low

- Count files, not only bytes: a PyTorch `.venv` holds about 64,000 files and its `__pycache__` folders about 20,000 more; set `PYTHONDONTWRITEBYTECODE=1` in job scripts and keep one `.venv` per project [V:run].
- Clear package caches after installs: `uv cache clean`, `pip cache purge` (the uv cache reached 45,802 files, [[EDEN Python environments]]) [V:run].
- Stream large intermediates (features, activations, encoded codes) through the next step in chunks instead of caching them on disk; write only what the results need.
- Delete regenerable artefacts once the results are recorded: encoded features or codes, raw dataset downloads and archives already unpacked, caches. Keep the code and configs that regenerate them.
- Check the quota before and after a large run (`lfs quota -h -p $(lfs project -d ~ | awk '{print $1}') /mnt/evafs`).

## End of a project

Pack the results into one compressed archive and keep it on EDEN only, not on the laptop and not in git:

```bash
cd ~ && mkdir -p archive
tar --exclude=.venv --exclude='__pycache__' --exclude='.cache' --exclude='*_cache' \
  --exclude=<project>/data -cf - <project> | zstd -19 -T0 > archive/<project>-<date>.tar.zst   # [U] zstd on the login node; else gzip
sha256sum archive/<project>-<date>.tar.zst > archive/<project>-<date>.tar.zst.sha256
```

- Leave out everything regenerable: `.venv`, caches, datasets that can be downloaded again, features that the code rebuilds.
- Check the archive (`zstd -t`, `sha256sum -c`), then delete the unpacked project folder.
- The archive lives as long as the account: private space is deleted 3 months after account expiry (below).

## Retention and backup

- Private space deleted 3 months after account expiry [V].
- Student data on teaching resources is temporary; may be deleted after access ends without notice [V].
- No guarantee of long-term storage or recovery; LTO tape backup is an extra paid service [V].
- Keep code in git and the finished results in one archive on EDEN ("End of a project"); copy only small summaries off the cluster.

## Scratch and raid

- Temporary heavy I/O: `/scratch/<user>/` or `/raid/<user>/` during the job, then copy out.
- `/raid` is per node: a job on `dgx-2` cannot read what a job wrote on `dgx-1`; read via `/mnt/workspace/dgx-N` from the login node.
