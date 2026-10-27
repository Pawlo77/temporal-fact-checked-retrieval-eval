# 2026 - Zhang - All Leaks Count Some Count More

## Citation

- Authors: Zeyu Zhang, Bradly C. Stadie (Northwestern University; Stadie also Bridgewater AIA Labs)
- Title: All Leaks Count, Some Count More: Interpretable Temporal Contamination Detection and Mitigation in LLM Backtesting
- Venue: Findings of the ACL: EMNLP 2026, Budapest, pages 36100-36127
- Year: 2026
- URL: https://aclanthology.org/2026.findings-emnlp.1690/ (PDF: https://aclanthology.org/2026.findings-emnlp.1690.pdf)
- Verified on: 2026-10-27 (Anthology page and PDF excerpts read; the paper exists)

## What it does

- Proposes a claim-level framework: decompose prediction rationales into atomic claims, then apply Shapley values to weight each claim's decision impact.
- Defines Shapley-DCLR (Shapley-weighted Decision-Critical Leakage Rate), the fraction of decision-driving reasoning that is contaminated by post-cutoff knowledge.
- Uses a claim taxonomy C0-C8 split into deterministically safe, requires date verification, and deterministically leaked tiers.
- Proposes TimeSPEC, an inference-time forecasting architecture combining search and supervision; ablates both components; compares to a frozen-snapshot retrieval arm.
- Reports that a hard date filter at the search API is insufficient because leakage propagates through unreliable publication-date metadata and page edits (citing El Lahib et al. 2026).

## Key numbers

- 2,769 instances across three LLMs in the (Search, Supervision) ablation.
- Temporal RAG DCLR of 16.7% / 17.0% / 18.5% (three models) even with metric leakage ruled out.
- Table 3: frozen-snapshot comparison on 159 matched Treatment questions (Qwen3.5-35B).
- Treatment set Autocast 1,942 binary questions; Control set ForecastBench 827.

## Relation to our project

- Shows that parametric and retrieved leakage can be measured at the level of individual reasoning claims; relevant if we use an LLM reranker that produces rationales (RQ5).
- Does NOT cover: retrieval ranking metrics, fact-check archives, PFCR.

## Verification

- OK. Note line "claim-level temporal leakage auditing in LLM backtesting (Findings EMNLP 2026)" matches. Reference list entry should add authors (Zhang and Stadie) and prefer the Anthology landing page over the PDF link.
