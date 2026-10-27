# temporal-fact-checked-retrieval-eval

Retrieval that cannot see the future: a causal evaluation protocol for previously fact-checked claim retrieval, with a Polish focus and an English control.

Previously fact-checked claim retrieval (PFCR) matches a social media post against an archive of fact-checks. Standard benchmarks (MultiClaim, SemEval-2025 Task 7) score systems against an index that also contains fact-checks published after the post, while a fact-checker searching on the day of the post only has the earlier archive. This project asks how much of the reported performance survives when the index contains only fact-checks published before each query post.

> **Status:** planning and setup. No experiments have been run and no results exist yet; the project plan is in `knowledge/handbook/`.

## Research questions

- How much Success@10 and MRR survive a time-respecting index, on answerable queries and with pool size controlled?
- How is the random-vs-causal gap split between answerability loss, pool composition, training-data leakage and missing labels for earlier debunks of the same claim?
- Is the penalty larger for Polish (thin national fact-check ecosystem) than for English?
- How many days after a post does a relevant fact-check become retrievable (time-to-findability)?

## Planned work

- A temporal split of MultiClaim (index only fact-checks published before each post), released as id lists plus code that rebuilds it from the official files.
- At least four systems under both protocols, in Polish and English: BM25, a multilingual dense retriever, a bilingual or cross-lingual encoder, and a cross-encoder reranker. Metrics: Success@10 and MRR with paired bootstrap significance tests over queries.
- A decomposition of the gap (time lag, lexical overlap, narrative drift) and a manual analysis of 50 newly failing queries.

Not in scope: a new retrieval architecture, judging claim veracity, language-bias analysis.

## Data

MultiClaim (Pikuliak et al., EMNLP 2023; [kinit-sk/multiclaim](https://github.com/kinit-sk/multiclaim)) and the SemEval-2025 Task 7 release. The Zenodo records are access-restricted and research-only: request access with an institutional address, and never commit or re-share the data. Releases contain id lists and code only.

## Ethics

Retrieval errors can make a named journalist or outlet look like a disinformation source. Errors are reported in aggregate, with no ranked list of outlets or authors.

## Repository layout

| Path | Contents |
|---|---|
| `src/temporal_fact_checked_retrieval_eval/` | package: `dataset`, `models`, `training`, `orchestration`, `config` |
| `configs/experiment.yaml` | experiment configuration |
| `knowledge/` | Obsidian vault: the assigned brief and the EDEN cluster guide (`knowledge/compute/`) |
| `plans/` | one folder per plan: the project plan with its research, language scope, LLM selection and risk notes |
| `research/` | one note per paper read, with verified citations |
| `report/` | LaTeX report |
| `notebooks/`, `outputs/` | analysis notebooks and run outputs |

Start with `plans/2026-10-27-temporal-retrieval-eval/`.

## Development

```bash
make install
make check
```

`make mlflow` starts a local MLflow server for experiment tracking. `make help` lists all targets.

## License

Apache License 2.0. See [LICENSE](LICENSE).

Copyright 2026 Pawel Pozorski.
