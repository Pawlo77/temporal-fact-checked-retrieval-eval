---
name: analysis-figures
description: >-
  Use when computing, testing or quoting quantitative results (methods, seeds, runs,
  benchmarks; statistics, tables, numbers in a report or results note), or when drawing,
  restyling or reviewing report figures and tables.
---

# Analysis and figures

Rules for every number and figure that reaches a report or a results note. Code follows
skill `development` (test first). How-to and review checklists: `references/analysis.md`,
`references/figures.md`. Project paths (figure module, captions, macros): `local.md` in
this folder, when it exists.

## Analysis

- **Unit = run (seed).** Reduce episodes to one value per run first; bootstrap, test and
  count over runs. Key every statistic by (method, configuration); never pool configurations.
- **Interval with every point estimate**, bootstrapped over runs.
- **Multiple comparisons:** Holm within each declared family; name the family.
- **Selection bias:** a configuration picked on some seeds is reported on fresh seeds;
  the tuning-seed gap is tuning optimism, reported as such.
- **Immortal time:** form groups at a landmark (status at time t among units alive at t),
  never by "ever reached". A median over units that reached an event carries the share
  that reached it.
- **Simpson's paradox:** show pooled and within-group associations together; units
  clustered in groups are not independent in a p-value.
- **Censoring:** a value beyond the measured range is "> max" with the censored count,
  never a number. Missing is "not logged", never zero.
- **Baselines:** chance or majority-class beside every accuracy-like score, plus the gain.
- **Scope:** a median is not "every unit"; one seed or one example is an illustration,
  never a result. Associational wording without an experiment.
- **Timings** from a shared or laptop machine are context only; never name a winner.
- **Null simulation:** every derived statistic is tested on a world with no effect
  (result near 0) and one with a known effect (recovered).
- **Traceability:** every quoted number comes from a generated file and reaches the report
  through generated macros. Fact-check each number, count and qualifier against its file.

## Figures

- PNG only, fixed dpi, exact size for the target column; no `bbox_inches="tight"`.
- One theme (seaborn style and context) applied per figure through `matplotlib.rc_context`;
  never global state.
- One quantity and one panel per file; one subfolder per benchmark or budget; LaTeX
  stacks the panels. Tables use the same folders.
- No explanatory text on the image: no notes, question titles, benchmark names,
  "pending". Keep axis and tick labels, data values. Single-panel figures have no title.
- Captions: each figure registers a description and its width in a captions file beside
  its PNGs; a generator writes the notes table (link | width | description).
- One fixed colour per category, shown once in a standalone legend figure; no repeated
  legends. Other legends sit outside the data.
- Nothing cropped, no overlapping text, no lone category label; compact for the column.
- Paper-ready proportions: height from a small set of aspect ratios, fonts sized for 1:1
  inclusion (never scaled in LaTeX). One report variant per figure, at the width it is
  placed at; no low-res duplicate; width recorded with the caption.
- An automated audit over every figure kind, then look at every rendered PNG.

## Pitfalls

- A fix that only adds a sentence to the caption: fix the statistic.
- A test that re-implements the same definition proves nothing; compare with a naive
  loop, a library or a hand-computed toy case.
