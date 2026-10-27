<div align="center">
  <h1>temporal-fact-checked-retrieval-eval</h1>
  <p><strong>Retrieval that cannot see the future: a causal evaluation protocol for previously fact-checked claim retrieval.</strong></p>
  <p>Time-respecting indexes, answerability-aware metrics and a Polish focus, on MultiClaim.</p>
  <p>
    <a href="https://github.com/Pawlo77/temporal-fact-checked-retrieval-eval/actions/workflows/test.yaml"><img src="https://github.com/Pawlo77/temporal-fact-checked-retrieval-eval/actions/workflows/test.yaml/badge.svg" alt="Pytest"></a>
    <a href="https://github.com/Pawlo77/temporal-fact-checked-retrieval-eval/actions/workflows/prek.yaml"><img src="https://github.com/Pawlo77/temporal-fact-checked-retrieval-eval/actions/workflows/prek.yaml/badge.svg" alt="Prek Checks"></a>
    <a href="https://github.com/Pawlo77/temporal-fact-checked-retrieval-eval/actions/workflows/codeql.yaml"><img src="https://github.com/Pawlo77/temporal-fact-checked-retrieval-eval/actions/workflows/codeql.yaml/badge.svg" alt="CodeQL"></a>
    <a href="https://www.python.org/"><img src="https://img.shields.io/badge/python-3.12-blue.svg" alt="Python 3.12"></a>
    <a href="LICENSE"><img src="https://img.shields.io/badge/license-Apache%202.0-blue.svg" alt="License"></a>
  </p>
</div>

Previously fact-checked claim retrieval (PFCR) matches a social media post against an archive of fact-checks. Standard benchmarks (MultiClaim, SemEval-2025 Task 7) score systems against an index that also holds fact-checks published after the post, while a fact-checker searching on the day of the post only has the earlier archive. This project measures how much reported performance survives when the index holds only fact-checks published before each query post. It separates the reasons for the drop and releases the protocol for reuse.

> **Status:** planning. The project plan is written and awaits the supervisor's approval; no experiments have been run and no results exist yet.

## What the project does

- **A causal protocol.** Per-query pools of earlier fact-checks and a size-matched random control. The split separates four effects: the gold fact-check not existing yet, a smaller pool, training-data leakage, and missing labels for earlier fact-checks of the same claim.
- **Answerability-aware metrics.** Success@10 and MRR reported unconditionally and on answerable queries, with cluster-bootstrap significance, plus time-to-findability.
- **A ranking check.** Whether the order of retrieval systems changes between the random and the causal protocol.
- **A Polish focus.** Polish is the headline language and English the control; an extended tier adds Spanish, German, Turkish, Czech and Slovak to test whether the penalty tracks archive density.

## Scope

| Tier | Contents |
|---|---|
| Core (the brief) | Polish and English; BM25 with causal-pool statistics, multilingual-e5-large, a cross-lingual or Polish encoder, bge-reranker-v2-m3; random, strict causal and size-matched protocols; gap decomposition; 50 hand-coded failing queries |
| Extended (gated) | Sibling qrels with an LLM judge panel, more languages, a second dated dataset, a fine-tuned retriever, LLM rerankers from several families (Gemma 3, Apertus, Olmo 3, Llama 3.3, Bielik, Qwen3) |

Out of scope: a new retrieval architecture, judging claim veracity, language-bias analysis. The full plan, with tasks, decision gates and risks, is in [`plans/`](plans/).

## Data and ethics

MultiClaim (Pikuliak et al., EMNLP 2023; [kinit-sk/multiclaim](https://github.com/kinit-sk/multiclaim)) and the SemEval-2025 Task 7 release. The Zenodo records are access-restricted and research-only: access is requested with an institutional address naming every team member, and the data is never committed or shared outside the named members. No post text appears in the repository, the report or any release; releases contain id lists and code only. Errors are reported in aggregate, with no ranked list of outlets or authors.

## Repository layout

| Path | Contents |
|---|---|
| `src/temporal_fact_checked_retrieval_eval/` | package: `dataset`, `models`, `training`, `orchestration`, `config` |
| `configs/` | experiment configuration |
| `plans/` | one folder per plan: the project plan with its topic research, language scope, LLM selection and risk register |
| `research/` | one note per paper read, in five areas, with verified citations |
| `knowledge/` | Obsidian vault: the assigned brief and the EDEN cluster guide (`knowledge/compute/`) |
| `report/` | LaTeX report |
| `notebooks/`, `outputs/` | analysis notebooks and run outputs, kept out of git |

The repository root is an Obsidian vault; notes link with `[[wikilinks]]` and `make vault-check` validates them. Setup, quality gates and the pull-request workflow are in [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Citing

See [`CITATION.cff`](CITATION.cff); GitHub's "Cite this repository" button renders it as APA or BibTeX.

## License

Apache License 2.0. See [LICENSE](LICENSE).

Copyright 2026 Pawel Pozorski.
