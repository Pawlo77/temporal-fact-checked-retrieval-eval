---
title: "EDEN access and networking"
type: handbook
domain: vault
parent: "[[compute]]"
tags: [handbook, hpc]
created: 2026-10-27
updated: 2026-10-27
---
# EDEN access and networking

## Accounts and groups

- Access requires approval of a research group leader [V].
- Students: ask a group leader to request the account; without a leader, ask a supervisor to request a new group [V].
- MiNI staff: join a group or request own group; people outside MiNI contact the HPC team individually [V].
- Course and thesis access on teaching nodes (`stud-*`): the coordinator or supervisor files a request form linked from the HPC news page [V].
- Group leader: MiNI academic employee with a signed declaration; files a yearly activity report, else all group users lose access until filed [V].
- Group name: lowercase Latin letters, digits, hyphens, up to 16 characters, permanent, tied to the leader not a project [V].
- Group name is the Slurm account: pass `-A <group>` so hours are billed correctly [V].
- Student access: course or bachelor/engineering thesis up to 1 semester, master's thesis up to 2 semesters [V].
- Private space deleted 3 months after expiry; reminders 1 month and 1 week before [V].
- Blocked or expired accounts deleted after 3+ months; inactive accounts after 12+ months [V].
- Login to EDEN may differ from the faculty gateway login [V].
- Some cluster web services (for example the wiki's Redmine) use the cluster's own CA; install the CA certificate from the wiki page `pl:topics:certyfikat_x509` (per-OS steps for Linux, Windows, macOS, Firefox) to avoid browser warnings [V:run]. Browsers can read the wiki; automated fetchers get 403 [V:run].

## Hosts

- Login node (access host): the only entry point; collects, queues, starts and monitors jobs [V].
- Direct ssh to compute nodes is impossible; use `srun`/`sbatch` through the login node [V].
- Login node must not run computations [V].
- Login node is reachable by ssh from the faculty internal network [V].
- Faculty ssh gateway and cluster login node are two different servers [V].
- Outside the faculty network: go through the faculty gateway (faculty IT ssh service page) [V].

## Connect

```bash
# from the faculty network [V]
ssh <user>@<eden-login-node>

# from outside, one hop with jump host [V]
ssh -J <mini-login>@<mini-ssh-gateway> <user>@<eden-login-node>

# explicit two-step form (cheat sheet); the gateway host is the one beginning with `ssh.`; the bare faculty domain timed out from outside the campus network [V:run]
ssh <user>@<mini-ssh-gateway>
ssh <user>@<eden-login-node>
```

## ssh config

```sshconfig
Host eden
    HostName <eden-login-node>
    User <user>
    ProxyJump <mini-login>@<mini-ssh-gateway>
    ServerAliveInterval 60
    ServerAliveCountMax 5
```

- Then `ssh eden`, `rsync ... eden:path`, `scp file eden:path` work [V:run].
- Keep this file in `~/.ssh/config`, never in the vault.
- Key auth: `ssh-copy-id` to both hops works and removes both password prompts [V:run]; add `ControlMaster auto`, `ControlPath ~/.ssh/cm-%r@%h:%p` and `ControlPersist 10m` so repeat connections reuse one login.

## Sessions that survive disconnects

- Interactive `srun --pty` ends when ssh drops; use `tmux` or `screen` [V].

```bash
tmux new -s eden
# work, detach with Ctrl-b d
tmux attach -t eden
```

## Port forwarding (Jupyter, TensorBoard, MLflow)

- Pick a port above 1024, start the service on the compute node, tunnel from the laptop [V].

```bash
ssh -L <port>:<node>:<port> -J <mini-login>@<mini-ssh-gateway> <user>@<eden-login-node>
# browse http://localhost:<port>/
```

- Batch script for Jupyter: [[EDEN job templates]].

## Other services

- LLM pilot service on EDEN (OpenAI-compatible chat endpoint, one model on one H200, key on request, all conversations logged) [V].
- Cluster status page: https://eden-status.mini.pw.edu.pl [V]; Grafana: https://edenstatus.mini.pw.edu.pl/d/7I8DDL3nz/eden-overview?orgId=1 (link from the maintainer).
- Contact and rules pages: https://hpc.mini.pw.edu.pl/contact/, https://hpc.mini.pw.edu.pl/rules/ [V].
