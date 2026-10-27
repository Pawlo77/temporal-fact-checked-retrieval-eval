# 2025 - Vykopal - LLMs for Multilingual PFCD (AMC-16K)

## Citation

- Authors: Ivan Vykopal, Matúš Pikuliak, Simon Ostermann, Tatiana Anikina, Michal Gregor, Marian Simko
- Title: Large Language Models for Multilingual Previously Fact-Checked Claim Detection
- Venue: Findings of the ACL: EMNLP 2025, Suzhou, pages 15741-15765
- Year: 2025
- URL: https://aclanthology.org/2025.findings-emnlp.852/ (abstract page and PDF read)
- Verified on: 2026-10-27

## What it does

- Treats PFCD as binary relevance classification of post-claim pairs and evaluates seven open LLMs (7B to 123B) with five prompting strategies, in original language and English translation.
- Builds AMC-16K from MultiClaim: for monolingual, 400 pairs for each of 20 languages; for crosslingual, top-100 retrieved claims in other languages, 400 pairs for each of 20 language pairs.
- Six annotators label Yes / No / Cannot tell; Fleiss' kappa 0.60 before and 0.62 after annotation.
- Metrics: Macro F1, TNR, FNR; Appendix F reports retrieval S@10/MAP/MRR of embedding models on MultiClaim and AMC-16K (Multilingual E5 Large best on AMC-16K).

## Key numbers

- 16,000 pairs = 8K monolingual + 8K crosslingual; 20 languages; 16% of pairs labelled relevant overall; above 30% for English, Malay, Portuguese, German.
- Polish (pol) is one of the 20 monolingual languages; crosslingual pairs include pol-hbs, ces-pol, hun-pol.
- Top LLMs reach Macro F1 above 80%; crosslingual average drop about 4.5%.
- Appendix: lower monolingual LLM performance for Czech, Hungarian, Polish and Slovak ("lower capabilities in Slavic languages"); Llama3.1 8B produced 568 wrong-language outputs for Polish.

## Relation to our project

- Not novel for us: LLM relevance judgments for PFCR, and human-annotated relevance beyond the fact-checker links (AMC-16K labels pairs the original data did not link).
- AMC-16K gives a Polish human-labelled relevance sample we can use to validate our LLM sibling-qrel judge (our annotation plan) and to estimate LLM-human agreement on Polish.
- No temporal dimension: pairs are sampled by retrieval rank without date constraints, so AMC-16K relevance labels may include later fact-checks; usable for label validation, not for causal evaluation as-is.

## Verification

- Status: OK.
- Line 62 ("AMC-16K, 16,000 manually annotated post-claim pairs over 20 languages, LLMs as PFCR detectors") correct; add that it is 8K monolingual + 8K crosslingual and includes Polish.
- Line 81 should cite AMC-16K as prior Polish PFCR evidence (see CORRECTIONS-A).
