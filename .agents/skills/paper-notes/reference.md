# Paper notes: writing standard

This project's half of skill `paper-notes`; edit it freely. Every note has the same
sections, words and symbols.

## Layout

```text
research/
  Research.md                  hub: the question and a table of areas
  AGENTS.md                    agent context (tooling, project use)
  protocols/<domain>.yaml      literature-search protocols and outcomes
  <Area>/
    <Area>.md                  folder note: table of its themes or papers
    <Short title>.md           paper note, citekey in frontmatter
    <Theme>/
      <Theme>.md               folder note of the theme
      <Short title>.md
```

File names are the paper's short name (method or system name), never `Year - Author - Title`.

## Placement

| Paper changes | Folder | Tag |
|---------------|--------|-----|
| a PFCR dataset, shared task or benchmark release | `research/Claim Retrieval/Datasets and Benchmarks/` | `theme/datasets` |
| a PFCR or claim-matching method, system or evaluation study | `research/Claim Retrieval/Methods and Systems/` | `theme/methods` |
| language, popularity or other bias in PFCR | `research/Claim Retrieval/Bias/` | `theme/bias` |
| evidence or answer leakage in claim verification | `research/Temporal Evaluation/Leakage in Verification/` | `theme/verification-leakage` |
| chronological splits, time-respecting evaluation, temporal persistence, recsys leakage | `research/Temporal Evaluation/Chronological Evaluation/` | `theme/chronological` |
| LLM parametric or search-based temporal contamination | `research/Temporal Evaluation/LLM Temporal Leakage/` | `theme/llm-leakage` |
| how to split data and what random splits hide | `research/Evaluation Methodology/Data Splits/` | `theme/splits` |
| an embedding model, retriever or reranker used as a system | `research/Retrieval Models/` | `theme/models` |
| an LLM evaluated as reranker or retriever | `research/Language Models/Evaluated LLMs/` | `theme/llm-evaluated` |
| an LLM used as judge or labeller (model card or report) | `research/Language Models/Judge Models/` | `theme/llm-judge-model` |
| reliability, bias or non-determinism of LLM judges and APIs | `research/Language Models/Judging and Reliability/` | `theme/llm-judging` |

## Sections (exact order, no others)

| Section | Contract |
|---------|----------|
| `> [!info] TL;DR` | What the paper changes and the result, 2–4 plain sentences |
| `## Motivation` | The gap before the paper, 3–5 bullets; prior work linked (vault note or verified URL) |
| `## Method` | Notation sentence, definitions, the method; an `Intuition:` sentence next to each key equation |
| `## Key numbers` | 2–5 headline results, each with its setting and baseline |
| `## Experiments` | One bullet per experiment: `**Name:** what was tested; what was found` |
| `## Data` | One bullet per dataset: name, what it is, size |
| `> [!failure] Limitations` | One bullet per failure mode |
| `## Relation to our project` | What we take, test or avoid; links to project notes |
| `## Future work` | Bullets led by `**Done:**` or `**Partly done:**` (with a verified link) or `**Open:**` ending `(searched YYYY-MM)` |

Whole note: 500–1500 words.

## Never

- References to figures, tables or equation numbers: state the finding.
- Copied result tables; abstract paraphrase; "this paper proposes"; TODOs.
- Facts not in the paper or a verified source; citations from memory.
- The same point in two sections.

## Glossary

| Use | Not | Meaning |
|-----|-----|---------|
| PFCR | claim matching, fact-check retrieval | retrieving previously fact-checked claims for a post |
| post | tweet, query, claim (as the query) | the social media text used as the query |
| fact-check | debunk, document | an article in the retrieval pool |
| causal index | time-restricted pool | pool holding only fact-checks published before the post |
| leakage | contamination (for LLM pretraining only) | information from after the query time reaching the evaluation |
| Success@k | recall@k, hit rate | share of queries with a gold fact-check in the top k |

## Notation

Query post $q$ with time $t_q$; fact-check $f$ with time $t_f$; pool $P$; causal pool $P(q) = \{f \in P : t_f < t_q\}$; gold set $G(q)$; rank of the first gold item $r_q$; Success@k $= \frac{1}{|Q|}\sum_q \mathbb{1}[r_q \le k]$; MRR $= \frac{1}{|Q|}\sum_q 1/r_q$. Rename a paper's symbols to these and say so once.

## Tags (vocabulary)

Paper notes carry `type/paper`, one `theme/` and one or more `topic/`:

- `theme/`: `datasets`, `methods`, `bias`, `verification-leakage`, `chronological`, `llm-leakage`, `splits`, `models`, `llm-evaluated`, `llm-judge-model`, `llm-judging`.
- `topic/`: `multilingual`, `polish`, `english`, `temporal`, `leakage`, `dense-retrieval`, `reranking`, `bm25`, `evaluation`, `significance`, `benchmark`, `shared-task`, `embedding`, `llm`, `recsys`, `judge-bias`, `reproducibility` (add values here before using them).

Other notes: `type/hub`, `type/theme`.

## Citation fields

`title` (short name = filename = heading), `aliases` (official title first), `authors`
(full names, published order), `year`, `venue` (with volume and pages), `arxiv` and/or
`doi`, `url` (published version, else arXiv), `citekey`
(`<firstauthor><year><firstword>`), `verified` (`YYYY-MM-DD` the citation and full text were checked; there is no Verification section), `theme`, `tags`. `scripts/verify_citation.py` must
print `OK` for the note.
