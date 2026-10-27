---
title: "EDEN storage and quotas"
type: handbook
domain: vault
parent: "[[EDEN overview]]"
tags: [handbook, hpc]
created: 2026-10-27
updated: 2026-10-27
---
# EDEN storage and quotas

## Filesystems

| Path | Scope | Backing | Use |
|---|---|---|---|
| `/home2/<group>/<user>` | shared: login node + `dgx-[1-4]` | DDN array, HDD | default for code, venvs, results [V] |
| `/mnt/evafs/groups/<group>/` | group-shared | storage array (path from cheat sheet) | corpora, embeddings, HF cache [U] |
| `/scratch` | shared: login + DGX | 24 NVMe, 332.6 TiB | temporary data during computation only [V] |
| `/raid` | per DGX, not shared | 4x NVMe RAID 0 | I/O-heavy job-local data [V] |
| `/mnt/workspace/dgx-[1-4]` | login node view of each `/raid` | NFS | fetch results from a DGX `/raid` [V] |

- Cheat sheet writes home as `/home2/faculty/<user>`; docs say `/home2/<group>/<login>` [V]; check with `echo $HOME`.
- Each user has a private space and a group space on the array, capped separately [V].
- Users in several groups get each group space [V].
- A full group space blocks new writes for the whole group [V].
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
lfs quota -hp <project-id> /mnt/evafs   # [U] cheat sheet; docs mention no quota command
lfs quota -hg <group> /mnt/evafs        # [U] Lustre group quota form
```

- Description page names Lustre on the AI400X array [V]; whether `/mnt/evafs` is Lustre is [U].

## Retention and backup

- Private space deleted 3 months after account expiry [V].
- Student data on teaching resources is temporary; may be deleted after access ends without notice [V].
- No guarantee of long-term storage or recovery; LTO tape backup is an extra paid service [V].
- Keep code in git; copy final results off the cluster.

## Placement plan for this project

- Code: `$HOME/<project>` (git clone or [[EDEN data sync workflows]]).
- Fact-check corpus, posts, qrels: `/mnt/evafs/groups/<group>/data/` once [U path].
- Embeddings, indexes, run files: `/mnt/evafs/groups/<group>/artifacts/` [U path].
- HF model cache: `/mnt/evafs/groups/<group>/hf_cache` ([[EDEN Python environments]]).
- Temporary heavy I/O (shuffled shards, tokenized caches): `/scratch/<user>/` or `/raid/<user>/` during the job, then copy out.
- `/raid` is per node: a job on `dgx-2` cannot read what a job wrote on `dgx-1`; read via `/mnt/workspace/dgx-N` from the login node.
- Estimated footprint: see [[EDEN project compute plan]].
